# Correlated D2D Fresh-Instance Stress Test

- Generated: `2026-04-19T02:02:48.508203`
- Checkpoint: `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt`
- Protocol: `1 fresh D2D instances x 1 MC evaluations per instance on the canonical Tiny-ViT V4 Ensemble HAT checkpoint`
- Correlation model: `separable_ar1_2d`

| Condition | Train best acc (%) | Fresh-instance mean (%) | Cross-instance std (%) |
|:--|--:|--:|--:|
| iid Gaussian | 91.13 | 87.45 | 0.00 |
| correlated rho=0_3 | 91.13 | 86.78 | 0.00 |

## Interpretation

- `iid Gaussian` is the paper-locked fresh-instance baseline for the canonical Ensemble HAT checkpoint.
- `correlated rho=...` keeps the same checkpoint and evaluation protocol but replaces i.i.d. D2D with a spatially correlated AR(1)-style field across the effective crossbar grid.
- The reviewer-facing question is whether Ensemble HAT remains clearly above the collapsed fixed-mask baseline when moderate spatial structure is introduced.
