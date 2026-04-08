# Layer Sensitivity Results (GPT)

- Generated: `2026-04-05 14:12:28`
- Model: `tinyvit`
- Experiment: `V4`
- Eval runs per group: `10`

## Current Invocation

| Phase | Group | Label | Noisy/Pessimistic layers | Accuracy |
|:------|:------|:------|------------------------:|:---------|
| isolated | A | Attention QKV | 10/42 | 91.61 +/- 0.15% (10 runs) |
| isolated | B | Attention Proj | 10/42 | 91.72 +/- 0.21% (10 runs) |
| isolated | C | FFN fc1+fc2 | 20/42 | 91.72 +/- 0.11% (10 runs) |
| isolated | D | Patch Embed | 2/42 | 91.67 +/- 0.25% (10 runs) |
| isolated | E | All analog | 42/42 | 91.61 +/- 0.15% (10 runs) |
| isolated | F | All layers C2C off | 0/42 | 91.70 +/- 0.11% (10 runs) |
| mixed | MIXED | Mixed robust groups: C, B | 30/42 | 9.70 +/- 0.20% (10 runs) |

## Combined Artifact Summary

- Total rows in merged artifact: `7`
- JSON: `report_md/_gpt/json_gpt/layer_sensitivity_results_gpt.json`
- CSV: `report_md/_gpt/csv_gpt/layer_sensitivity_results_gpt.csv`
- Figure refreshed: `paper/figures/fig_layer_sensitivity.png`

## Notes

- Canonical Phase 1 keeps the checkpoint's original D2D buffers for every analog layer and isolates the impact of C2C variability by turning C2C on only for the selected group.
- Optional `--resample-d2d` switches Phase 1 into a stricter fresh-instance ablation mode; this is useful for diagnostics but is not the default paper-facing Task 15 setting.
- Group `E` is the all-analog control and group `F` is the clean control.
- Optional `phase2-mixed` reads the merged Phase 1 rows, ranks groups by accuracy drop from clean control `F`, and assigns pessimistic settings only to the top-K most robust groups.
- Results are GPT-scoped append-only scratch artifacts for the paper pipeline.
