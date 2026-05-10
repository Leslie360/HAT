# Noise Sweep Results (GPT)

- Generated: `2026-04-05 13:35:08`
- Model: `tinyvit`
- Experiment: `V2`
- Sweep type: `noise`
- Eval runs per point: `10`
- Checkpoint: `/home/qiaosir/projects/compute_vit/checkpoints/V2_hybrid_no_noise_best.pt`

## Current Invocation

| Sweep | Sigma C2C | Sigma D2D | ADC | Accuracy |
|:------|-----------:|-----------:|:----|:---------|
| noise | 0.05 | 0.1 | native | 97.39 +/- 0.00% (10 runs) |

## Combined Artifact Summary

- Total rows in merged artifact: `1`
- JSON: `report_md/_gpt/json_gpt/v2_under_noise_results_gpt.json`
- CSV: `report_md/_gpt/csv_gpt/v2_under_noise_results_gpt.csv`
- Figure refreshed: `paper/figures/fig9_noise_sensitivity.png`

## Notes

- `noise` sweep scans the continuous `(sigma_c2c, sigma_d2d)` grid with retention disabled.
- `adc` sweep keeps the checkpoint's base noise regime and adds fixed per-layer ADC quantizers during inference.
- Results are GPT-scoped append-only scratch artifacts for the paper pipeline.
