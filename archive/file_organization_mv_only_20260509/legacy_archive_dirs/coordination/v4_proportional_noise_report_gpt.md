# Noise Sweep Results (GPT)

- Generated: `2026-04-06 01:44:52`
- Model: `tinyvit`
- Experiment: `V4`
- Sweep type: `noise`
- Eval runs per point: `10`
- Checkpoint: `/home/qiaosir/projects/compute_vit/checkpoints/V4_hybrid_standard_noise_hat_best.pt`
- Device profile: `checkpoint default / literature prior`
- Noise mode override: `proportional`
- D2D handling: `preserve checkpoint instance`

## Current Invocation

| Sweep | Sigma C2C | Sigma D2D | ADC | Accuracy |
|:------|-----------:|-----------:|:----|:---------|
| noise | 0.05 | 0.1 | native | 10.00 +/- 0.00% (10 runs) |

## Combined Artifact Summary

- Total rows in merged artifact: `1`
- JSON: `/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/v4_proportional_noise_results_gpt.json`
- CSV: `/home/qiaosir/projects/compute_vit/report_md/_gpt/csv_gpt/v4_proportional_noise_results_gpt.csv`
- Figure refreshed: `/home/qiaosir/projects/compute_vit/paper/figures/fig9_noise_sensitivity.png`

## Notes

- `noise` sweep scans the continuous `(sigma_c2c, sigma_d2d)` grid with retention disabled.
- `adc` sweep keeps the checkpoint's base noise regime and adds fixed per-layer ADC quantizers during inference.
- When `--device-profile-json` is provided, array dynamic range, state count, and optional retention constants are loaded from the measured profile before the sweep-specific overrides are applied.
- Results are GPT-scoped append-only scratch artifacts for the paper pipeline.
