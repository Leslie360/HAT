# Gemini G-AUDIT-CODE Report
Commit audited: 33bed9c
Auditor: Gemini
Date: 2026-04-24

## Summary
- Total checks performed: 8
- Pass: 5
- Fail: 3
- Flag-for-review: 0

## Per-check results

### Check 3.1 LTP/LTD branch consistency
- Status: PASS
- File:line reference: analog_layers.py:L226-L236
- Finding: The code extracts absolute values `nl_ltp = abs(ctx.nl_ltp)` and `nl_ltd = abs(ctx.nl_ltd)` before applying the exponent `nl - 1.0`. This correctly prevents fractional negative powers from producing imaginary numbers while preserving the proper magnitude scaling. The `torch.where(grad_output >= 0, ...)` logic correctly routes LTP vs. LTD updates based on the gradient sign.

### Check 3.2 Second-order Taylor correction
- Status: PASS
- File:line reference: analog_layers.py:L245-L258
- Finding: The second-order term properly uses `-0.5 * (nl - 1.0) * pow(...)`. The extraneous `nl` multiplier from the pre-fix code is gone. At `NL=1.0`, `math.isclose` correctly catches it and sets the correction to `torch.zeros_like(grad_output)`, cleanly vanishing the term.

### Check 3.3 Numerical stability near boundaries
- Status: FAIL
- File:line reference: analog_layers.py:L248-L253 & L184
- Finding: The clamp minimum is `eps = 1e-8`. If `NL` is between 1 and 2 (e.g., `NL=1.5`), the exponent `(nl_ltp - 2.0)` evaluates to `-0.5`. This means `pow(eps, -0.5)` evaluates to `10000`, causing a massive gradient explosion in the second-order correction term near the conductance boundaries. Furthermore, under AMP (`float16`), `1e-8` underflows to `0.0`, resulting in `Inf`/`NaN` errors, and the `StraightThroughQuantize` class lacks the required `@custom_fwd` and `@custom_bwd` decorators from `torch.cuda.amp` to properly manage mixed-precision casting.

### Check 3.4 Gradient-flow correctness in STE
- Status: PASS
- File:line reference: analog_layers.py:L207-L210
- Finding: The STE backward pass directly calculates and returns `grad_input` based on the unmodified `grad_output`. `x_clamped` is correctly detached via `ctx.save_for_backward()`. In the forward pass, device noise (D2D/C2C) is added strictly after `ste_quantize`, meaning the non-differentiable noise generation logic does not incorrectly entangle with the STE backward graph.

### Check 3.5 Ensemble mask resampling
- Status: PASS
- File:line reference: analog_layers_ensemble.py:L281-L284 & L1073-L1083
- Finding: The mask uses `torch.randn_like()`, perfectly guaranteeing zero-mean Gaussian mismatch. The `resample_all_d2d_noise(model)` function is correctly hooked into `train_tinyvit_ensemble.py`'s per-epoch loop. Because the mismatch mask is registered as a buffer, `DataParallel` naturally broadcasts it on each forward pass, maintaining synchronization across GPUs.

### Check 3.6 Noise injection order
- Status: FAIL
- File:line reference: analog_layers.py:L608-L623 (AnalogConv2d.forward)
- Finding: The noise injection order perfectly matches `W_effective = (W_ideal * (1 + M_D2D)) + ξ_C2C` for proportional noise because `C2C` references `W_eff` which already includes the `D2D` mismatch. However, the requirement to "then ADC-quantize the output current" is totally missing. `ADCQuantizer` is implemented in the file but is never called inside `AnalogLinear` or `AnalogConv2d`!

### Check 3.7 Scale recovery calibration
- Status: FAIL
- File:line reference: analog_layers.py:L620-L621
- Finding: The scale recovery calibration uses the noise-free maximum weight, which is correct. However, scale recovery is multiplied directly into `W_eff` *before* the convolution operation (`F.conv2d`). This physically represents recovering the digital scale inside the analog crossbar arrays rather than digitally after the ADC. Given Check 3.6 proved the ADC is missing entirely, this order incorrectly delegates all MAC operations back to high-dynamic-range floating point.

### Check 3.8 Configuration flag consistency
- Status: PASS
- File:line reference: train_tinyvit_ensemble.py:L406-L422
- Finding: The checkpoint payload builder (`build_training_checkpoint_payload`) correctly saves `exp_cfg` (which tracks `nl_ltp`, `nl_ltd`, `noise_mode`, `hat_training`, `sigma_d2d`, `sigma_c2c`, `batch_size`) as an `asdict` dictionary. `amp_enabled` and `seed` are correctly saved as top-level keys in the payload dict.

## Latent issues found (if any)
- **High Severity** (analog_layers.py:L248): 2nd-order gradient explosion when `1 < NL < 2`.
- **High Severity** (analog_layers.py:L621): `ADCQuantizer` is never invoked. Crossbar current remains unquantized continuous floating-point before the digital scale recovery is preemptively applied to the weights.
- **Moderate Severity** (analog_layers.py:L184): Missing `torch.cuda.amp` decorators in STE function risking `float16` underflow when evaluating `eps=1e-8`.

## Third-bug hypothesis
Yes, there is a major third bug. The simulation fundamentally bypasses ADC quantization. `ADCQuantizer` is defined but entirely omitted from the `forward()` pipeline of `AnalogConv2d` and `AnalogLinear`. Because scale recovery (`_conductance_to_weight_scale`) is then multiplied directly into the weights before the spatial convolution (`F.conv2d`), the simulation executes mathematically equivalent float32 MACs instead of quantized analog currents.

Additionally, the second-order Taylor correction contains a latent gradient explosion bug for any sweeps evaluating $1 < NL < 2$, because $(NL - 2.0)$ becomes negative, turning the small `eps` into a massive division-by-zero equivalent.

## Recommendations
1. Redesign `AnalogConv2d.forward` and `AnalogLinear.forward` to execute `F.conv2d(x, W_eff)`, pass the resulting current tensor through `ADCQuantizer()`, and *then* multiply by `_conductance_to_weight_scale()`.
2. Add `@custom_fwd` and `@custom_bwd` decorators to `StraightThroughQuantize`.
3. Wrap the second-order correction in `StraightThroughQuantize.backward` to clamp `nl - 2.0` strictly `>= 0`, or disable it when $NL < 2.0$.