# [Codex] 2026-04-15 13:55 CST — Non-GPU Audit for Kimi/Claude

## Scope

User asked Codex to finish tasks that do not occupy GPU and monitor Kimi's running training. I did not start any new GPU workload.

## Training Monitor Snapshot

| Experiment | Main PID | Status | Current trustworthy state |
|:--|:--:|:--|:--|
| Ensemble HAT Frequency Ablation | 791 | Running | `fixed` and `batch` completed; `epoch` stage started but no epoch output yet |
| Spatial Correlation Ablation | 8715 | Running | `spatial_fixed` and `spatial_resample` completed; now in `iid_epoch` stage |

Current log evidence:

- `logs/ensemble_frequency_ablation.log`: fixed = 87.18%; per-batch = 86.16%; per-epoch still running.
- `logs/spatial_ablation.log`: spatial_fixed = 87.80%; spatial_resample = 88.15% best, with epoch 50 acc = 83.39%; `iid_epoch` stage started.

No final JSON has appeared yet for either running experiment:

- Pending: `report_md/_gpt/ensemble_frequency_ablation.json`
- Pending: `report_md/_gpt/spatial_ablation.json`

## Finding 1 — ConvNeXt ADC Sweep Root Cause Confirmed

`run_convnext_adc_sweep.py` previously changed `cfg.adc_bits`, but that value was not consumed by the ConvNeXt model path:

- `train_convnext.py` `ExperimentConfig` has no declared `adc_bits` field.
- `train_convnext.py:80-87` builds `AnalogLinearConfig` without any ADC field.
- `AnalogLinear.forward()` and `AnalogConv2d.forward()` do not apply ADC quantization.
- ADC support exists separately as `ADCQuantHookManager` in `inference_analysis_utils.py`.

Therefore the identical 4/6/8/10/12-bit ConvNeXt results are a script bug, not evidence of ADC-insensitive ConvNeXt behavior.

### Patch Applied

Patched `run_convnext_adc_sweep.py` to use the existing inference-only ADC hooks:

- Imports `ADCQuantHookManager`, `ModelBundle`, and `calibrate_adc_ranges`.
- Calibrates analog layer output ranges with `calibrate_adc_ranges(..., max_batches=5)`.
- Wraps evaluation with `ADCQuantHookManager(model, output_ranges, adc_bits=adc_bits)`.

Validation:

- `python3 -m py_compile run_convnext_adc_sweep.py` passed.
- No GPU execution was started.

Remaining requirement:

- Kimi should rerun the sweep only after current authorized GPU jobs finish.
- The old `report_md/_gpt/convnext_adc_sweep_results.json` remains invalid and should not be cited.

## Finding 2 — Spatial Correlation Ablation Is Likely Invalid

`run_spatial_ablation.py` attempts to switch spatial vs i.i.d. mode by setting:

```python
m.config.spatial_d2d = (mode == 'spatial')
```

But repo search shows `spatial_d2d` is not read by `AnalogLinear`, `AnalogConv2d`, or noise sampling code. In `AnalogConv2d._apply_noise()`, D2D noise is always taken from `module.d2d_noise` and applied through `_scaled_noise_from_reference(...)`; there is no branch for spatial vs i.i.d. mode.

Implication:

- The running Spatial Correlation Ablation should not be used to support a spatial-vs-i.i.d. claim.
- Its final JSON, if produced, should be quarantined until the implementation is corrected.
- I did not kill PID 8715 because stopping a user-authorized training job is a destructive action and needs explicit approval.

## Recommended Next Non-GPU Actions

1. Do not cite `convnext_adc_sweep_results.json`; rerun only with patched `run_convnext_adc_sweep.py`.
2. Mark `run_spatial_ablation.py` output as invalid unless the `spatial_d2d` mode is implemented in `AnalogLinear/AnalogConv2d`.
3. For KP-FIX-2, wait for `ensemble_frequency_ablation.json`; do not merge partial best-epoch log values into paper tables.
4. For KP-FIX-1, build a no-GPU dry-run checklist first: checkpoint path, model construction path, config diff, and baseline sanity command. Do not launch layer-wise NL until no-NL baseline is verified near 91%.

## Files Touched

- Modified: `run_convnext_adc_sweep.py`
- Added: `AGENT_SYNC/codex_non_gpu_audit_20260415.md`
