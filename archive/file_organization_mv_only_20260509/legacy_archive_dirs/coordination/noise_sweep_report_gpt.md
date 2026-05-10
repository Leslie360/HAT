# Noise Sweep Results (GPT)

- Generated: `2026-04-05 13:27:30`
- Model: `tinyvit`
- Experiment: `V4`
- Sweep type: `adc`
- Eval runs per point: `10`
- Checkpoint: `auto`

## Current Invocation

| Sweep | Sigma C2C | Sigma D2D | ADC | Accuracy |
|:------|-----------:|-----------:|:----|:---------|
| adc | 0.05 | 0.1 | 3-bit | 10.62 +/- 0.31% (10 runs) |
| adc | 0.05 | 0.1 | 4-bit | 27.10 +/- 0.56% (10 runs) |
| adc | 0.05 | 0.1 | 6-bit | 80.50 +/- 0.60% (10 runs) |
| adc | 0.05 | 0.1 | 8-bit | 81.06 +/- 0.21% (10 runs) |
| adc | 0.05 | 0.1 | 10-bit | 81.36 +/- 0.61% (10 runs) |
| adc | 0.05 | 0.1 | ideal | 91.60 +/- 0.25% (10 runs) |

## Combined Artifact Summary

- Total rows in merged artifact: `48`
- JSON: `report_md/_gpt/json_gpt/noise_sweep_results_gpt.json`
- CSV: `report_md/_gpt/csv_gpt/noise_sweep_results_gpt.csv`
- Figure refreshed: `paper/figures/fig9_noise_sensitivity.png`

## Notes

- `noise` sweep scans the continuous `(sigma_c2c, sigma_d2d)` grid with retention disabled.
- `adc` sweep keeps the checkpoint's base noise regime and adds fixed per-layer ADC quantizers during inference.
- Results are GPT-scoped append-only scratch artifacts for the paper pipeline.
