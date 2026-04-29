#!/usr/bin/env python3
"""
Unit tests for analog_layers.py

Verifies:
  1. AnalogLinear output shape and basic forward pass
  2. Quantization produces exactly n_states unique conductance levels
  3. D2D noise is fixed across forward calls
  4. C2C noise causes output variation across forward calls
  5. STE gradient flows through quantization (weight.grad is non-zero)
  6. Retention decay changes output for t > 0
  7. convert_to_hybrid replaces correct Tiny-ViT linear + patch-embed conv layers
"""

import sys
import torch
import torch.nn as nn

from analog_layers import (
    AnalogLinear, AnalogLinearConfig, AnalogConv2d,
    convert_to_hybrid, convert_resnet_to_analog, ste_quantize,
    InverseGammaPreprocessor, PhotocurrentSimulator,
    ADCQuantizer, ADCConfig, EnergyProfiler, EnergyConstants,
    disable_sparsity_tracking, enable_sparsity_tracking,
    get_sparsity_report, reset_sparsity_tracking,
)

PASS = 0
FAIL = 0


def check(name: str, condition: bool, detail: str = ""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  [PASS] {name}")
    else:
        FAIL += 1
        print(f"  [FAIL] {name} — {detail}")


def test_output_shape():
    print("\n== Test 1: Output shape ==")
    layer = AnalogLinear(64, 128)
    x = torch.randn(2, 10, 64)  # batch=2, seq=10, features=64
    y = layer(x)
    check("output shape", y.shape == (2, 10, 128), f"got {y.shape}")
    check("output is finite", torch.isfinite(y).all().item(), "output has inf/nan")


def test_scale_recovery_preserves_linear_weights():
    print("\n== Test 1b: Scale recovery preserves linear weights ==")
    x = torch.tensor([[2.0, -1.0]])

    digital = nn.Linear(2, 2, bias=False)
    with torch.no_grad():
        digital.weight.copy_(torch.tensor([[1.0, 0.0], [0.0, -1.0]]))
    y_digital = digital(x)

    cfg = AnalogLinearConfig(
        n_states=16, sigma_c2c=0, sigma_d2d=0,
        noise_enabled=False, restore_weight_scale=True
    )
    analog = AnalogLinear(2, 2, bias=False, config=cfg)
    with torch.no_grad():
        analog.weight.copy_(digital.weight)
    y_analog = analog(x)

    check("linear scale recovery matches digital",
          torch.allclose(y_digital, y_analog, atol=1e-6),
          f"digital={y_digital.tolist()}, analog={y_analog.tolist()}")


def test_quantization_levels():
    print("\n== Test 2: Quantization levels ==")
    for n_states in [4, 8, 16, 64]:
        cfg = AnalogLinearConfig(n_states=n_states, sigma_c2c=0, sigma_d2d=0, noise_enabled=False)
        layer = AnalogLinear(32, 32, config=cfg)
        # Manually run weight_to_conductance
        G_pos, G_neg = layer._weight_to_conductance(layer.weight)
        unique_pos = torch.unique(G_pos).numel()
        # Should have at most n_states unique values
        check(
            f"n_states={n_states}: unique G_pos <= {n_states}",
            unique_pos <= n_states,
            f"got {unique_pos} unique values"
        )


def test_d2d_noise_fixed():
    print("\n== Test 3: D2D noise is fixed across forward calls ==")
    cfg = AnalogLinearConfig(sigma_c2c=0, sigma_d2d=0.10)
    layer = AnalogLinear(32, 32, config=cfg)
    layer.eval()

    # D2D noise buffer should not change between forward calls
    d2d_before = layer.d2d_noise.clone()
    x = torch.randn(1, 32)
    _ = layer(x)
    d2d_after = layer.d2d_noise.clone()
    check("d2d_noise unchanged", torch.equal(d2d_before, d2d_after))


def test_c2c_noise_varies():
    print("\n== Test 4: C2C noise causes output variation ==")
    cfg = AnalogLinearConfig(sigma_c2c=0.05, sigma_d2d=0)
    layer = AnalogLinear(64, 64, config=cfg)
    layer.eval()

    x = torch.randn(1, 64)
    torch.manual_seed(42)
    y1 = layer(x)
    torch.manual_seed(99)
    y2 = layer(x)
    # With C2C noise, two forward passes should give different outputs
    check("outputs differ with C2C", not torch.allclose(y1, y2, atol=1e-6),
          "outputs are identical — C2C noise may not be working")

    # Without noise, outputs should be identical
    cfg_no_noise = AnalogLinearConfig(sigma_c2c=0, sigma_d2d=0, noise_enabled=False)
    layer_clean = AnalogLinear(64, 64, config=cfg_no_noise)
    layer_clean.eval()
    x2 = torch.randn(1, 64)
    y3 = layer_clean(x2)
    y4 = layer_clean(x2)
    check("outputs identical without noise", torch.allclose(y3, y4, atol=1e-8))


def test_proportional_noise_scales_with_state():
    print("\n== Test 4b: Proportional noise scales with state ==")
    cfg = AnalogLinearConfig(
        sigma_c2c=0.0,
        sigma_d2d=0.10,
        noise_enabled=True,
        noise_mode="proportional",
    )
    layer = AnalogLinear(2, 1, bias=False, config=cfg)
    with torch.no_grad():
        layer.d2d_noise.fill_(cfg.G_max - cfg.G_min)

    G_pos = torch.tensor([[10.0, 2.0]])
    G_neg = torch.tensor([[1.0, 1.0]])
    base = G_pos - G_neg
    noisy = layer._apply_noise(G_pos, G_neg)
    added = (noisy - base).abs()

    check("proportional D2D noise larger on large conductance state",
          added[0, 0].item() > added[0, 1].item(),
          f"added={added.tolist()}")


def test_ste_gradient():
    print("\n== Test 5: STE gradient flows ==")
    cfg = AnalogLinearConfig(sigma_c2c=0, sigma_d2d=0, noise_enabled=False)
    layer = AnalogLinear(32, 16, config=cfg)
    layer.train()

    x = torch.randn(4, 32)
    y = layer(x)
    loss = y.sum()
    loss.backward()

    check("weight.grad is not None", layer.weight.grad is not None)
    if layer.weight.grad is not None:
        grad_nonzero = (layer.weight.grad != 0).any().item()
        check("weight.grad has non-zero entries", grad_nonzero,
              f"grad norm = {layer.weight.grad.norm().item():.6f}")

    if layer.bias is not None:
        check("bias.grad is not None", layer.bias.grad is not None)


def test_nonlinear_update_scaling():
    print("\n== Test 5b: Nonlinear update scaling ==")
    # Post-33bed9c: grad<0 triggers LTP branch (potentiation / weight increase).
    x_ltp = torch.tensor([2.0, 9.0], requires_grad=True)
    y_ltp = ste_quantize(x_ltp, n_levels=16, x_min=1.0, x_max=10.0, nl_ltp=3.0, nl_ltd=-1.0)
    (-y_ltp.sum()).backward()
    check("LTP scaling favors low-conductance states",
          abs(x_ltp.grad[0].item()) > abs(x_ltp.grad[1].item()),
          f"grad={x_ltp.grad.tolist()}")

    # Post-33bed9c: grad>=0 triggers LTD branch (depression / weight decrease).
    x_ltd = torch.tensor([2.0, 9.0], requires_grad=True)
    y_ltd = ste_quantize(x_ltd, n_levels=16, x_min=1.0, x_max=10.0, nl_ltp=1.0, nl_ltd=-3.0)
    y_ltd.sum().backward()
    check("LTD scaling favors high-conductance states",
          abs(x_ltd.grad[1].item()) > abs(x_ltd.grad[0].item()),
          f"grad={x_ltd.grad.tolist()}")

    x_identity = torch.tensor([2.0, 9.0], requires_grad=True)
    y_identity = ste_quantize(x_identity, n_levels=16, x_min=1.0, x_max=10.0, nl_ltp=1.0, nl_ltd=-1.0)
    y_identity.sum().backward()
    check("NL=1 keeps STE identity",
          torch.allclose(x_identity.grad, torch.ones_like(x_identity)),
          f"grad={x_identity.grad.tolist()}")


def test_retention_decay():
    print("\n== Test 6: Retention decay ==")
    # No retention
    cfg_t0 = AnalogLinearConfig(
        retention_enabled=False, inference_time=0,
        sigma_c2c=0, sigma_d2d=0, noise_enabled=False
    )
    layer_t0 = AnalogLinear(32, 32, config=cfg_t0)
    layer_t0.eval()

    # With retention at t=1000s
    cfg_t1000 = AnalogLinearConfig(
        retention_enabled=True, inference_time=1000.0,
        sigma_c2c=0, sigma_d2d=0, noise_enabled=False
    )
    layer_t1000 = AnalogLinear(32, 32, config=cfg_t1000)
    layer_t1000.eval()
    # Copy same weights
    layer_t1000.weight.data.copy_(layer_t0.weight.data)
    if layer_t1000.bias is not None:
        layer_t1000.bias.data.copy_(layer_t0.bias.data)

    x = torch.randn(1, 32)
    y_t0 = layer_t0(x)
    y_t1000 = layer_t1000(x)

    check("retention changes output",
          not torch.allclose(y_t0, y_t1000, atol=1e-6),
          "outputs identical — retention may not be working")

    # Decay factor at t=1000s should be approximately A_0 = 0.6
    # (exponential terms vanish: exp(-1000/0.14) ≈ 0, exp(-1000/0.61) ≈ 0)
    # So output should be ~60% of t=0 output magnitude (approximately)
    ratio = y_t1000.abs().mean() / (y_t0.abs().mean() + 1e-8)
    check(f"decay ratio ≈ 0.6 (got {ratio:.3f})",
          0.3 < ratio.item() < 0.9,
          f"ratio = {ratio.item():.3f}, expected near 0.6")


def test_retention_recalibrate_scale_restores_clean_output():
    print("\n== Test 6b: Retention scale recalibration restores clean output ==")
    x = torch.tensor([[1.5, -0.5]])
    weight = torch.tensor([[0.8, -0.3], [-0.4, 0.6]])

    cfg_t0 = AnalogLinearConfig(
        retention_enabled=False,
        sigma_c2c=0,
        sigma_d2d=0,
        noise_enabled=False,
        restore_weight_scale=True,
    )
    layer_t0 = AnalogLinear(2, 2, bias=False, config=cfg_t0)

    cfg_ret_no_fix = AnalogLinearConfig(
        retention_enabled=True,
        inference_time=1.0,
        sigma_c2c=0,
        sigma_d2d=0,
        noise_enabled=False,
        restore_weight_scale=True,
        retention_recalibrate_scale=False,
    )
    layer_ret_no_fix = AnalogLinear(2, 2, bias=False, config=cfg_ret_no_fix)

    cfg_ret_fix = AnalogLinearConfig(
        retention_enabled=True,
        inference_time=1.0,
        sigma_c2c=0,
        sigma_d2d=0,
        noise_enabled=False,
        restore_weight_scale=True,
        retention_recalibrate_scale=True,
    )
    layer_ret_fix = AnalogLinear(2, 2, bias=False, config=cfg_ret_fix)

    with torch.no_grad():
        for layer in (layer_t0, layer_ret_no_fix, layer_ret_fix):
            layer.weight.copy_(weight)

    y_t0 = layer_t0(x)
    y_ret_no_fix = layer_ret_no_fix(x)
    y_ret_fix = layer_ret_fix(x)

    err_no_fix = (y_t0 - y_ret_no_fix).abs().max().item()
    err_fix = (y_t0 - y_ret_fix).abs().max().item()

    check("retention without recalibration changes output",
          err_no_fix > 1e-3,
          f"err_no_fix={err_no_fix:.6f}")
    check("retention recalibration restores clean output",
          torch.allclose(y_t0, y_ret_fix, atol=1e-6),
          f"t0={y_t0.tolist()}, fixed={y_ret_fix.tolist()}, err={err_fix:.6f}")


def test_retention_scales_d2d_preserves_noisy_output():
    print("\n== Test 6c: Retention-scaled D2D preserves noisy output ==")
    x = torch.tensor([[1.0, -0.75]])
    weight = torch.tensor([[0.7, -0.2], [-0.5, 0.9]])
    d2d = torch.tensor([[0.30, -0.15], [0.05, -0.20]])

    cfg_t0 = AnalogLinearConfig(
        retention_enabled=False,
        sigma_c2c=0,
        sigma_d2d=0.10,
        noise_enabled=True,
        restore_weight_scale=True,
    )
    layer_t0 = AnalogLinear(2, 2, bias=False, config=cfg_t0)

    cfg_ret_scale_only = AnalogLinearConfig(
        retention_enabled=True,
        inference_time=1.0,
        sigma_c2c=0,
        sigma_d2d=0.10,
        noise_enabled=True,
        restore_weight_scale=True,
        retention_recalibrate_scale=True,
        retention_scales_d2d=False,
    )
    layer_ret_scale_only = AnalogLinear(2, 2, bias=False, config=cfg_ret_scale_only)

    cfg_ret_scale_and_d2d = AnalogLinearConfig(
        retention_enabled=True,
        inference_time=1.0,
        sigma_c2c=0,
        sigma_d2d=0.10,
        noise_enabled=True,
        restore_weight_scale=True,
        retention_recalibrate_scale=True,
        retention_scales_d2d=True,
    )
    layer_ret_scale_and_d2d = AnalogLinear(2, 2, bias=False, config=cfg_ret_scale_and_d2d)

    with torch.no_grad():
        for layer in (layer_t0, layer_ret_scale_only, layer_ret_scale_and_d2d):
            layer.weight.copy_(weight)
            layer.d2d_noise.copy_(d2d)

    y_t0 = layer_t0(x)
    y_scale_only = layer_ret_scale_only(x)
    y_scale_and_d2d = layer_ret_scale_and_d2d(x)

    err_scale_only = (y_t0 - y_scale_only).abs().max().item()
    err_scale_and_d2d = (y_t0 - y_scale_and_d2d).abs().max().item()

    check("scale-only retention still perturbs noisy output",
          err_scale_only > 1e-3,
          f"err_scale_only={err_scale_only:.6f}")
    check("scale+d2d retention restores noisy output",
          torch.allclose(y_t0, y_scale_and_d2d, atol=1e-6),
          f"t0={y_t0.tolist()}, fixed={y_scale_and_d2d.tolist()}, err={err_scale_and_d2d:.6f}")


def test_invalid_analog_config_rejected():
    print("\n== Test 6d: Invalid analog config rejected ==")
    try:
        AnalogLinearConfig(noise_mode="mystery")
        check("invalid noise_mode rejected", False, "expected ValueError")
    except ValueError:
        check("invalid noise_mode rejected", True)

    try:
        AnalogLinearConfig(G_min=2.0, G_max=2.0)
        check("degenerate conductance span rejected", False, "expected ValueError")
    except ValueError:
        check("degenerate conductance span rejected", True)

    try:
        AnalogLinearConfig(inl_table=torch.tensor([1.0, 0.5, 2.0]))
        check("non-monotonic INL table rejected", False, "expected ValueError")
    except ValueError:
        check("non-monotonic INL table rejected", True)


def test_convert_to_hybrid():
    print("\n== Test 7: convert_to_hybrid ==")
    try:
        import timm
        model = timm.create_model('tiny_vit_5m_224', pretrained=False, num_classes=1000)
    except ImportError:
        print("  [SKIP] timm not available")
        return

    cfg = AnalogLinearConfig(noise_enabled=False, sigma_c2c=0, sigma_d2d=0)
    model = convert_to_hybrid(model, config=cfg, verbose=True)

    analog_linear_count = sum(1 for m in model.modules() if isinstance(m, AnalogLinear))
    analog_conv_count = sum(1 for m in model.modules() if isinstance(m, AnalogConv2d))
    # Expected: 10 blocks × 4 layers (qkv, proj, fc1, fc2) = 40
    # Stage 1: 2 blocks × 4 = 8
    # Stage 2: 6 blocks × 4 = 24
    # Stage 3: 2 blocks × 4 = 8
    # Total = 40
    expected_linear = 40
    expected_conv = 2
    check(f"AnalogLinear count = {expected_linear}",
          analog_linear_count == expected_linear,
          f"got {analog_linear_count}")
    check(f"AnalogConv2d count = {expected_conv}",
          analog_conv_count == expected_conv,
          f"got {analog_conv_count}")
    check("patch_embed.conv1 converted",
          isinstance(model.patch_embed.conv1.conv, AnalogConv2d),
          f"got {type(model.patch_embed.conv1.conv).__name__}")
    check("patch_embed.conv2 converted",
          isinstance(model.patch_embed.conv2.conv, AnalogConv2d),
          f"got {type(model.patch_embed.conv2.conv).__name__}")

    # Verify forward pass still works
    x = torch.randn(1, 3, 224, 224)
    try:
        with torch.no_grad():
            y = model(x)
        check("forward pass succeeds", True)
        check("output shape (1, 1000)", y.shape == (1, 1000), f"got {y.shape}")
    except Exception as e:
        check("forward pass succeeds", False, str(e))


def test_ste_quantize_unit():
    print("\n== Test 8: STE quantize unit test ==")
    x = torch.tensor([1.0, 3.0, 5.5, 7.0, 10.0], requires_grad=True)
    y = ste_quantize(x, n_levels=4, x_min=1.0, x_max=10.0)
    # 4 levels at: 1.0, 4.0, 7.0, 10.0
    expected = torch.tensor([1.0, 4.0, 7.0, 7.0, 10.0])
    check("quantize values correct",
          torch.allclose(y, expected, atol=0.1),
          f"got {y.data.tolist()}, expected {expected.tolist()}")

    # Test gradient passthrough
    y.sum().backward()
    check("STE grad = ones", torch.allclose(x.grad, torch.ones_like(x)),
          f"got {x.grad.tolist()}")


def test_analog_conv2d():
    print("\n== Test 13: AnalogConv2d ==")
    cfg = AnalogLinearConfig(n_states=16, sigma_c2c=0.05, sigma_d2d=0.10, noise_enabled=True)
    conv = AnalogConv2d(3, 16, kernel_size=3, stride=1, padding=1, config=cfg)

    x = torch.randn(2, 3, 8, 8)
    y = conv(x)
    check("AnalogConv2d output shape", y.shape == (2, 16, 8, 8), f"got {y.shape}")
    check("AnalogConv2d output finite", torch.isfinite(y).all().item())

    # STE gradient flows
    conv.train()
    y2 = conv(x)
    y2.sum().backward()
    check("AnalogConv2d grad flows", conv.weight.grad is not None and (conv.weight.grad != 0).any().item())

    # D2D fixed
    d2d_before = conv.d2d_noise.clone()
    _ = conv(x)
    check("AnalogConv2d D2D fixed", torch.equal(d2d_before, conv.d2d_noise))

    cfg_scaled = AnalogLinearConfig(
        n_states=16, sigma_c2c=0, sigma_d2d=0,
        noise_enabled=False, restore_weight_scale=True
    )
    conv_scaled = AnalogConv2d(1, 1, kernel_size=1, stride=1, padding=0, bias=False, config=cfg_scaled)
    ref_conv = nn.Conv2d(1, 1, kernel_size=1, stride=1, padding=0, bias=False)
    with torch.no_grad():
        ref_conv.weight.fill_(1.0)
        conv_scaled.weight.copy_(ref_conv.weight)
    x_small = torch.randn(1, 1, 4, 4)
    y_ref = ref_conv(x_small)
    y_scaled = conv_scaled(x_small)
    check("AnalogConv2d scale recovery matches digital",
          torch.allclose(y_ref, y_scaled, atol=1e-6),
          f"max diff = {(y_ref - y_scaled).abs().max().item():.6f}")


def test_invalid_layer_dimensions_rejected():
    print("\n== Test 13a: Invalid layer dimensions rejected ==")
    try:
        AnalogLinear(0, 4)
        check("AnalogLinear rejects in_features=0", False, "expected ValueError")
    except ValueError:
        check("AnalogLinear rejects in_features=0", True)

    try:
        AnalogConv2d(3, 4, kernel_size=3, groups=2)
        check("AnalogConv2d rejects bad channel/group pairing", False, "expected ValueError")
    except ValueError:
        check("AnalogConv2d rejects bad channel/group pairing", True)

    try:
        AnalogConv2d(3, 4, kernel_size=0)
        check("AnalogConv2d rejects non-positive kernel_size", False, "expected ValueError")
    except ValueError:
        check("AnalogConv2d rejects non-positive kernel_size", True)


def test_sparsity_tracking():
    print("\n== Test 13b: Activation sparsity tracking ==")
    model = nn.Sequential(
        AnalogLinear(4, 3, config=AnalogLinearConfig(noise_enabled=False)),
        AnalogConv2d(1, 1, kernel_size=1, bias=False, config=AnalogLinearConfig(noise_enabled=False)),
    )
    enable_sparsity_tracking(model)

    x_linear = torch.tensor([[0.0, 0.0, 1.0, -1.0]])
    _ = model[0](x_linear)
    x_conv = torch.tensor([[[[0.0, 1.0], [0.0, 0.0]]]])
    _ = model[1](x_conv)

    report = get_sparsity_report(model)
    check("tracked two analog layers", report["tracked_layers"] == 2, f"got {report['tracked_layers']}")
    check("tracked passes > 0", report["tracked_passes"] > 0, f"got {report['tracked_passes']}")
    check("model relative sparsity > 0",
          report["model_mean_relative_zero_frac"] > 0.0,
          f"got {report['model_mean_relative_zero_frac']}")
    check("model absolute sparsity > 0",
          report["model_mean_absolute_zero_frac"] > 0.0,
          f"got {report['model_mean_absolute_zero_frac']}")
    check("relative sparsity <= absolute sparsity",
          report["model_mean_relative_zero_frac"] <= report["model_mean_absolute_zero_frac"],
          f"rel={report['model_mean_relative_zero_frac']}, abs={report['model_mean_absolute_zero_frac']}")
    first_layer = report["layers"][0]
    check("layer report includes dual sparsity metrics",
          "mean_relative_zero_frac" in first_layer and "mean_absolute_zero_frac" in first_layer,
          f"keys={sorted(first_layer.keys())}")

    disable_sparsity_tracking(model)
    reset_sparsity_tracking(model)
    cleared = get_sparsity_report(model)
    check("reset clears tracked passes", cleared["tracked_passes"] == 0, f"got {cleared['tracked_passes']}")
    check("reset clears relative sparsity",
          cleared["model_mean_relative_zero_frac"] == 0.0,
          f"got {cleared['model_mean_relative_zero_frac']}")
    check("reset clears absolute sparsity",
          cleared["model_mean_absolute_zero_frac"] == 0.0,
          f"got {cleared['model_mean_absolute_zero_frac']}")


def test_convert_resnet_to_analog():
    print("\n== Test 14: convert_resnet_to_analog ==")
    import torchvision.models as models
    model = models.resnet18(weights=None, num_classes=10)
    model.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
    model.maxpool = nn.Identity()

    cfg = AnalogLinearConfig(noise_enabled=False, sigma_c2c=0, sigma_d2d=0)
    model = convert_resnet_to_analog(model, config=cfg, skip_first_conv=False, verbose=False)

    n_analog_conv = sum(1 for m in model.modules() if isinstance(m, AnalogConv2d))
    n_analog_linear = sum(1 for m in model.modules() if isinstance(m, AnalogLinear))
    check(f"ResNet analog conv count > 0", n_analog_conv > 0, f"got {n_analog_conv}")
    check(f"ResNet analog linear count = 1", n_analog_linear == 1, f"got {n_analog_linear}")

    # Forward pass
    x = torch.randn(1, 3, 32, 32)
    with torch.no_grad():
        y = model(x)
    check("ResNet analog forward succeeds", y.shape == (1, 10), f"got {y.shape}")


def test_inverse_gamma():
    print("\n== Test 9: InverseGammaPreprocessor ==")
    # gamma=1.0 should be identity
    prep_id = InverseGammaPreprocessor(gamma_phys=1.0)
    x = torch.tensor([0.1, 0.5, 0.9])
    P_in, noise_var = prep_id(x)
    check("gamma=1.0 is identity", torch.allclose(P_in, x, atol=1e-6))
    check("noise_var = alpha * P_in", torch.allclose(noise_var, P_in, atol=1e-6))

    # gamma=0.5: P_in = X^2
    prep_05 = InverseGammaPreprocessor(gamma_phys=0.5)
    P_in_05, _ = prep_05(x)
    expected = x ** 2.0
    check("gamma=0.5: P_in = X^2", torch.allclose(P_in_05, expected, atol=1e-5),
          f"got {P_in_05.tolist()}, expected {expected.tolist()}")

    # gamma=2.0: P_in = X^0.5 = sqrt(X)
    prep_20 = InverseGammaPreprocessor(gamma_phys=2.0)
    P_in_20, _ = prep_20(x)
    expected_20 = torch.sqrt(x)
    check("gamma=2.0: P_in = sqrt(X)", torch.allclose(P_in_20, expected_20, atol=1e-5))

    # Output shape preserved
    x_batch = torch.rand(2, 3, 8, 8)
    P_out, nv = prep_05(x_batch)
    check("batch shape preserved", P_out.shape == x_batch.shape)


def test_photocurrent_simulator():
    print("\n== Test 10: PhotocurrentSimulator ==")
    sim = PhotocurrentSimulator(alpha=1.0, I_dark=0.01, gamma_phys=0.7, shot_noise=False)
    x = torch.tensor([0.1, 0.5, 0.9])

    # Raw mode: I = alpha * X^gamma + I_dark
    I_raw = sim(x, mode='raw')
    expected_raw = 1.0 * torch.pow(x, 0.7) + 0.01
    check("raw mode correct", torch.allclose(I_raw, expected_raw, atol=1e-5),
          f"got {I_raw.tolist()}")

    # Compensated mode with inverse-gamma input: should linearize
    prep = InverseGammaPreprocessor(gamma_phys=0.7)
    P_in, _ = prep(x)
    I_comp = sim(P_in, mode='compensated')
    # I_comp = alpha * (X^(1/0.7))^0.7 + I_dark = alpha * X + I_dark
    expected_comp = 1.0 * x + 0.01
    check("compensated mode linearizes", torch.allclose(I_comp, expected_comp, atol=1e-4),
          f"got {I_comp.tolist()}, expected {expected_comp.tolist()}")

    # With shot noise, outputs should vary
    sim_noisy = PhotocurrentSimulator(alpha=1.0, I_dark=0.01, gamma_phys=0.7, shot_noise=True)
    x2 = torch.rand(1, 64)
    torch.manual_seed(42)
    y1 = sim_noisy(x2, mode='raw')
    torch.manual_seed(99)
    y2 = sim_noisy(x2, mode='raw')
    check("shot noise causes variation", not torch.allclose(y1, y2, atol=1e-8))


def test_adc_quantizer():
    print("\n== Test 11: ADCQuantizer ==")
    # Test with no DNL (clean quantization)
    cfg_clean = ADCConfig(adc_bits=2, dnl_sigma=0.0, I_min=0.0, I_max=1.0)
    adc_clean = ADCQuantizer(config=cfg_clean)
    adc_clean.eval()

    # 2-bit = 4 levels: 0.0, 0.333, 0.667, 1.0
    x = torch.tensor([0.0, 0.15, 0.4, 0.8, 1.0])
    y = adc_clean(x)
    # 0.0→0, 0.15→0, 0.4→1/3, 0.8→2/3, 1.0→1.0
    expected = torch.tensor([0.0, 0.0, 1/3, 2/3, 1.0])
    check("2-bit quantization levels",
          torch.allclose(y, expected, atol=0.05),
          f"got {y.tolist()}")

    # 8-bit should have 256 levels — quantization error < 1/255
    cfg_8bit = ADCConfig(adc_bits=8, dnl_sigma=0.0)
    adc_8bit = ADCQuantizer(config=cfg_8bit)
    adc_8bit.eval()
    x8 = torch.rand(100)
    y8 = adc_8bit(x8)
    max_error = (y8 - x8).abs().max().item()
    check("8-bit max error < 1/255", max_error < 1.0/255 + 1e-6,
          f"max error = {max_error:.6f}")

    # DNL distortion should shift levels
    cfg_dnl = ADCConfig(adc_bits=4, dnl_sigma=0.5)
    adc_dnl = ADCQuantizer(config=cfg_dnl)
    adc_dnl.eval()
    check("DNL offsets are non-zero",
          adc_dnl.dnl_offsets.abs().sum().item() > 0)

    # STE gradient in training mode
    cfg_ste = ADCConfig(adc_bits=4, dnl_sigma=0.0)
    adc_ste = ADCQuantizer(config=cfg_ste)
    adc_ste.train()
    x_grad = torch.rand(10, requires_grad=True)
    y_grad = adc_ste(x_grad)
    y_grad.sum().backward()
    check("ADC STE gradient flows", x_grad.grad is not None and (x_grad.grad != 0).any().item())


def test_energy_profiler():
    print("\n== Test 12: EnergyProfiler ==")
    profiler = EnergyProfiler()

    # Add one analog layer: 128×64, batch=1 token
    profiler.add_analog_layer(M=128, N=64, batch_tokens=1)
    check("analog MACs counted", profiler.op_counts['analog_MACs'] == 128 * 64)
    check("ADC conversions counted", profiler.op_counts['ADC_conversions'] == 128)
    check("DAC conversions counted", profiler.op_counts['DAC_conversions'] == 64)

    # Add digital layer
    profiler.add_digital_layer(n_MACs=1000, precision='INT8')
    check("digital MACs counted", profiler.op_counts['digital_MACs'] == 1000)

    # Add special ops
    profiler.add_softmax(n_elements=256)
    profiler.add_layernorm(n_elements=512)

    # Total energy should be positive
    total = profiler.total_energy()
    check("total energy > 0", total > 0, f"got {total}")

    # Summary should have all keys
    s = profiler.summary()
    check("summary has percentage", 'percentage' in s)
    check("summary has latency", 'total_latency_us' in s and s['total_latency_us'] > 0, f"got {s.get('total_latency_us')}")
    check("percentages sum to ~100",
          abs(sum(s['percentage'].values()) - 100.0) < 0.1,
          f"sum = {sum(s['percentage'].values()):.1f}")

    latency = profiler.estimate_latency()
    check("latency estimate > 0", latency["total_latency_us"] > 0.0, f"got {latency['total_latency_us']}")

    # GPU comparison
    total_MACs = 128 * 64 + 1000
    comp = profiler.compare_with_fp32_gpu(total_MACs)
    check("energy reduction > 1",
          comp['energy_reduction_ratio'] > 1.0,
          f"ratio = {comp['energy_reduction_ratio']:.2f}")

    # Reset clears everything
    profiler.reset()
    check("reset clears energy", profiler.total_energy() == 0.0)


def test_inl_quantization():
    print("\n== Test 13: INL quantization levels ==")
    n_states = 4
    # Non-uniform table: 1.0, 2.5, 3.0, 10.0 (G_min=1.0, G_max=10.0)
    inl_table = torch.tensor([1.0, 2.5, 3.0, 10.0])
    cfg = AnalogLinearConfig(n_states=n_states, sigma_c2c=0, sigma_d2d=0, noise_enabled=False, inl_table=inl_table)
    layer = AnalogLinear(4, 4, config=cfg)

    # Test ste_quantize directly
    x = torch.tensor([1.1, 2.4, 2.8, 9.0])
    y = ste_quantize(x, n_states, 1.0, 10.0, inl_table=inl_table)
    expected = torch.tensor([1.0, 2.5, 3.0, 10.0])
    check("ste_quantize with INL table", torch.allclose(y, expected), f"got {y.tolist()}")

    # Test AnalogLinear weight_to_conductance
    # Force weights to map to specific normalized values
    # W_pos_norm = W_pos / w_abs_max. W_pos_norm in [0, 1].
    # G = G_min + W_pos_norm * (G_max - G_min)
    # For G_min=1, G_max=10, G_range=9:
    # G = 1 + W_pos_norm * 9
    # W_pos_norm = (G - 1) / 9
    # G=1.0 -> W_pos_norm=0.0
    # G=2.5 -> W_pos_norm=1.5/9 = 0.1666
    # G=3.0 -> W_pos_norm=2.0/9 = 0.2222
    # G=10.0 -> W_pos_norm=1.0
    with torch.no_grad():
        layer.weight.copy_(torch.tensor([
            [0.0, 0.16, 0.23, 1.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0]
        ]))
    G_pos, G_neg = layer._weight_to_conductance(layer.weight)
    unique_pos = torch.sort(torch.unique(G_pos))[0]
    # Should only contain values from inl_table
    check("AnalogLinear with INL table: unique values match",
          all(val in inl_table for val in unique_pos.tolist()),
          f"got {unique_pos.tolist()}")


if __name__ == "__main__":
    print("=" * 60)
    print("Testing analog_layers.py")
    print("=" * 60)

    test_ste_quantize_unit()
    test_output_shape()
    test_scale_recovery_preserves_linear_weights()
    test_quantization_levels()
    test_d2d_noise_fixed()
    test_c2c_noise_varies()
    test_proportional_noise_scales_with_state()
    test_ste_gradient()
    test_nonlinear_update_scaling()
    test_retention_decay()
    test_retention_recalibrate_scale_restores_clean_output()
    test_retention_scales_d2d_preserves_noisy_output()
    test_invalid_analog_config_rejected()
    test_convert_to_hybrid()
    test_analog_conv2d()
    test_invalid_layer_dimensions_rejected()
    test_sparsity_tracking()
    test_convert_resnet_to_analog()
    test_inverse_gamma()
    test_photocurrent_simulator()
    test_adc_quantizer()
    test_energy_profiler()
    test_inl_quantization()

    print("\n" + "=" * 60)
    print(f"Results: {PASS} passed, {FAIL} failed")
    print("=" * 60)

    sys.exit(0 if FAIL == 0 else 1)
