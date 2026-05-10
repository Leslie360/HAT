# [Codex] 2026-04-15 — Spatial Ablation Quarantine Note

## Decision

Allow the currently running Spatial Correlation Ablation process to finish, but quarantine its output until implementation is fixed and rerun.

## Reason

`run_spatial_ablation.py` labels modes as spatial or i.i.d. by setting:

```python
m.config.spatial_d2d = (mode == 'spatial')
```

However, `spatial_d2d` is not consumed by `AnalogLinear`, `AnalogConv2d`, or the shared noise helpers. The underlying analog forward path continues to use the same `d2d_noise` buffer and `_scaled_noise_from_reference(...)` path regardless of the requested mode.

## Status

Running process:

- PID 8715: `python -u run_spatial_ablation.py`

Current log values are monitor-only and not paper-citable:

- `spatial_fixed`: 87.80%
- `spatial_resample`: 88.15% best
- `iid_epoch`: running

## Rule

If `report_md/_gpt/spatial_ablation.json` appears, treat it as quarantined. Do not cite it, merge it into KP-FIX-2, or use it for the spatial-vs-i.i.d. mechanism claim until the mode switch is implemented in the analog layer/noise path.
