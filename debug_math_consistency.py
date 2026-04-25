#!/usr/bin/env python3
"""
Math Consistency Debugger for analog_layers.py
Verifies that every code path matches the mathematical formulas exactly.
"""
import sys
import torch
import numpy as np

sys.path.insert(0, ".")
from analog_layers import StraightThroughQuantize, AnalogLinear, AnalogLinearConfig

def test_ste_forward_formula():
    """Verify: x_quant = round((x_clamped - xmin) / (xmax - xmin) * (L-1)) / (L-1) * (xmax - xmin) + xmin"""
    x = torch.tensor([0.1, 0.5, 0.9, 1.2, -0.2])
    n_levels = 4
    xmin, xmax = 0.0, 1.0
    q = StraightThroughQuantize.apply(x, n_levels, xmin, xmax, 1.0, -1.0)
    x_clamped = torch.clamp(x, xmin, xmax)
    scale = xmax - xmin
    x_norm = (x_clamped - xmin) / scale
    x_quant_manual = torch.round(x_norm * (n_levels - 1)) / (n_levels - 1) * scale + xmin
    assert torch.allclose(q, x_quant_manual, atol=1e-5)
    print("✅ STE forward pass matches formula")

def test_first_order_branch_mapping():
    """
    Correct mapping (post-fix):
    grad_output >= 0 (LTD): scale = ((x - xmin)/span)^(abs(nl_ltd)-1)
    grad_output < 0 (LTP):  scale = ((xmax - x)/span)^(abs(nl_ltp)-1)
    """
    x = torch.tensor([0.3, 0.7], requires_grad=True)
    n_levels = 16
    xmin, xmax = 0.0, 1.0
    nl_ltp, nl_ltd = 2.0, -2.0
    q = StraightThroughQuantize.apply(x, n_levels, xmin, xmax, nl_ltp, nl_ltd)
    
    # LTD branch (positive grad)
    grad_pos = torch.autograd.grad(q, x, grad_outputs=torch.tensor([1.0, 1.0]), retain_graph=True)[0]
    span = xmax - xmin
    ltd_scale_manual = torch.pow((x.detach() - xmin) / span, abs(nl_ltd) - 1.0)
    grad_pos_manual = torch.tensor([1.0, 1.0]) * ltd_scale_manual
    assert torch.allclose(grad_pos, grad_pos_manual, atol=1e-5)
    
    # LTP branch (negative grad)
    x.grad = None
    grad_neg = torch.autograd.grad(q, x, grad_outputs=torch.tensor([-1.0, -1.0]), retain_graph=False)[0]
    ltp_scale_manual = torch.pow((xmax - x.detach()) / span, abs(nl_ltp) - 1.0)
    grad_neg_manual = torch.tensor([-1.0, -1.0]) * ltp_scale_manual
    assert torch.allclose(grad_neg, grad_neg_manual, atol=1e-5)
    
    print("✅ First-order branch mapping matches formula (post-fix)")

def test_second_order_formula():
    """
    Formula: correction = alpha * where(grad >= 0, grad * ltd_corr, grad * ltp_corr)
    ltp_corr = -0.5 * (abs(nl_ltp) - 1) * (ltp_ratio)^(abs(nl_ltp) - 2) * delta_g
    ltd_corr = -0.5 * (abs(nl_ltd) - 1) * (ltd_ratio)^(abs(nl_ltd) - 2) * delta_g
    """
    x = torch.tensor([0.3], requires_grad=True)
    n_levels, xmin, xmax = 16, 0.0, 1.0
    nl_ltp, nl_ltd = 2.0, -2.0
    delta_g, alpha = 0.1, 1.0
    
    q = StraightThroughQuantize.apply(x, n_levels, xmin, xmax, nl_ltp, nl_ltd, None, True, delta_g, alpha)
    x2 = torch.tensor([0.3], requires_grad=True)
    q2 = StraightThroughQuantize.apply(x2, n_levels, xmin, xmax, nl_ltp, nl_ltd, None, False, delta_g, alpha)
    
    grad_so = torch.autograd.grad(q, x, grad_outputs=torch.tensor([1.0]), retain_graph=False)[0]
    grad_fo = torch.autograd.grad(q2, x2, grad_outputs=torch.tensor([1.0]), retain_graph=False)[0]
    
    span = xmax - xmin
    x_val = 0.3
    ltd_ratio = (x_val - xmin) / span
    ltd_corr_manual = -0.5 * (abs(nl_ltd) - 1.0) * (ltd_ratio ** (abs(nl_ltd) - 2.0)) * delta_g
    correction_manual = alpha * 1.0 * ltd_corr_manual
    expected_grad = grad_fo + correction_manual
    
    assert torch.allclose(grad_so, expected_grad, atol=1e-5)
    print("✅ Second-order correction matches formula")

def test_nl_propagation():
    """Verify: CLI arg -> exp_cfg -> AnalogLinearConfig -> forward ctx -> backward"""
    from train_tinyvit_ensemble import TinyViTExperimentConfig, build_model
    
    exp_cfg = TinyViTExperimentConfig(
        name="test_nl_prop",
        use_hybrid=True, noise_enabled=True,
        sigma_c2c=0.05, sigma_d2d=0.10, hat_training=True,
        nl_ltp=2.5, nl_ltd=-3.0,
    )
    model = build_model(exp_cfg, num_classes=10, device="cpu", pretrained=False)
    
    nl_values = []
    for module in model.modules():
        if isinstance(module, AnalogLinear):
            nl_values.append((module.config.NL_LTP, module.config.NL_LTD))
    
    assert len(nl_values) > 0
    for ltp, ltd in nl_values:
        assert abs(ltp - 2.5) < 1e-6, f"NL_LTP mismatch: {ltp} != 2.5"
        assert abs(ltd - (-3.0)) < 1e-6, f"NL_LTD mismatch: {ltd} != -3.0"
    
    print(f"✅ NL propagation verified across {len(nl_values)} AnalogLinear layers")

def test_d2d_resampling():
    """Verify resample_all_d2d_noise() changes D2D buffers"""
    from train_tinyvit_ensemble import TinyViTExperimentConfig, build_model, resample_all_d2d_noise
    
    exp_cfg = TinyViTExperimentConfig(
        name="test_d2d", use_hybrid=True, noise_enabled=True,
        sigma_c2c=0.05, sigma_d2d=0.10, hat_training=True,
    )
    torch.manual_seed(42)
    model = build_model(exp_cfg, num_classes=10, device="cpu", pretrained=False)
    
    initial_d2d = []
    for module in model.modules():
        if isinstance(module, AnalogLinear) and hasattr(module, 'd2d_noise'):
            initial_d2d.append(module.d2d_noise.clone())
    
    count = resample_all_d2d_noise(model)
    assert count > 0
    
    new_d2d = []
    for module in model.modules():
        if isinstance(module, AnalogLinear) and hasattr(module, 'd2d_noise'):
            new_d2d.append(module.d2d_noise.clone())
    
    all_same = all(torch.allclose(a, b) for a, b in zip(initial_d2d, new_d2d))
    assert not all_same, "D2D noise did NOT change after resampling!"
    print(f"✅ D2D resampling verified: {count} modules, buffers changed")

def test_full_pipeline_no_noise():
    """Verify AnalogLinear with zero noise matches manual computation through full pipeline"""
    config = AnalogLinearConfig(
        n_states=16, sigma_c2c=0.0, sigma_d2d=0.0,
        noise_enabled=True, noise_mode="uniform", restore_weight_scale=False
    )
    layer = AnalogLinear(10, 5, config=config)
    x = torch.randn(2, 10)
    
    with torch.no_grad():
        out_layer = layer(x)
        # Manual: the layer does _weight_to_conductance -> _apply_noise -> _conductance_to_weight_scale -> linear
        # With sigma=0 and restore_weight_scale=False, the scaling factor is 1.0
        # The differential pair conductance is quantized, but with no noise
        G_pos, G_neg = layer._weight_to_conductance(layer.weight)
        W_eff = G_pos - G_neg  # no noise
        scale = layer._conductance_to_weight_scale(layer.weight, W_eff)
        W_scaled = W_eff * scale
        out_manual = torch.nn.functional.linear(x, W_scaled, layer.bias)
    
    assert torch.allclose(out_layer, out_manual, atol=1e-4), \
        f"Full pipeline mismatch:\n  max diff: {(out_layer - out_manual).abs().max().item()}"
    print("✅ Full analog pipeline verified (zero-noise baseline)")

def test_full_pipeline_with_scale_recovery():
    """Verify scale recovery path: w_abs_max / G_range"""
    config = AnalogLinearConfig(
        n_states=16, sigma_c2c=0.0, sigma_d2d=0.0,
        noise_enabled=True, noise_mode="uniform", restore_weight_scale=True
    )
    layer = AnalogLinear(10, 5, config=config)
    x = torch.randn(2, 10)
    
    with torch.no_grad():
        out_layer = layer(x)
        G_pos, G_neg = layer._weight_to_conductance(layer.weight)
        W_eff = G_pos - G_neg
        scale = layer._conductance_to_weight_scale(layer.weight, W_eff)
        # With restore_weight_scale=True, scale = w_abs_max / G_range
        w_abs_max = layer.weight.abs().max() + 1e-8
        G_range = config.G_max - config.G_min
        expected_scale = w_abs_max / G_range
        assert abs(scale.item() - expected_scale.item()) < 1e-4
        W_scaled = W_eff * scale
        out_manual = torch.nn.functional.linear(x, W_scaled, layer.bias)
    
    assert torch.allclose(out_layer, out_manual, atol=1e-4)
    print("✅ Scale recovery path verified")

def test_amp_autocast_safety():
    """Verify custom autograd function works with AMP autocast"""
    x = torch.tensor([0.5], requires_grad=True)
    with torch.cuda.amp.autocast(enabled=True):
        q = StraightThroughQuantize.apply(x, 16, 0.0, 1.0, 2.0, -2.0)
        loss = q.sum()
    loss.backward()
    assert x.grad is not None
    assert torch.isfinite(x.grad)
    print("✅ AMP autocast compatibility verified")

def run_all_tests():
    print("=" * 60)
    print("MATH CONSISTENCY DEBUG SUITE")
    print("=" * 60)
    test_ste_forward_formula()
    test_first_order_branch_mapping()
    test_second_order_formula()
    test_nl_propagation()
    test_d2d_resampling()
    test_full_pipeline_no_noise()
    test_full_pipeline_with_scale_recovery()
    test_amp_autocast_safety()
    print("=" * 60)
    print("🎉 ALL MATH CONSISTENCY TESTS PASSED")
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()
