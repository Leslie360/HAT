# Consolidated NL Sweep (2026-04-17)

| Source | Regime | NL | Best acc | Best epoch | Final / eval acc | Status | Notes |
|:--|:--|--:|--:|--:|--:|:--|:--|
| legacy_gm_e4 | historical | 1.2 | 59.46 | 0 | 10.11 | collapse | epoch-0 best from legacy landscape scan |
| legacy_gm_e4 | historical | 1.5 | 58.01 | 0 | 9.52 | collapse | epoch-0 best from legacy landscape scan |
| legacy_gm_e4 | historical | 1.8 | 56.84 | 0 | 9.94 | collapse | epoch-0 best from legacy landscape scan |
| task35_v4_nl2_hat | canonical | 2.0 | 27.37 | 15 | 13.83 | collapse | canonical V4 NL=2.0 training run |
| task35_v4_nl2_hat_eval | canonical_eval | 2.0 | 27.72 |  | 27.72 | eval_summary | 10-run evaluation mean ± std = 27.72 ± 0.82 |
| legacy_gm_e4 | historical | 2.2 | 56.43 | 0 | 9.22 | collapse | epoch-0 best from legacy landscape scan |
| legacy_gm_e4 | historical | 2.5 | 53.56 | 0 | 10.22 | collapse | epoch-0 best from legacy landscape scan |
| task23_v4_nl3 | canonical | 3.0 | 27.54 | 12 | 13.91 | collapse | canonical V4 NL=3.0 training run |
| task24_v4_nl1p5_rerun | canonical_rerun | 1.5 | 19.01 | 1 | 9.76 | collapse | host-WSL rerun; rebuttal-side evidence of recipe instability |

## Use guidance

- `task35_v4_nl2_hat_eval` remains the canonical manuscript-facing severe-NL point.
- `task24_v4_nl1p5_rerun` is reviewer-facing evidence that instability already appears at lower NL under the present recipe.
- `legacy_gm_e4` points are real CUDA evidence and useful for rebuttal/landscape framing, but should be explicitly labeled historical rather than mixed into the main manuscript without caveat.
