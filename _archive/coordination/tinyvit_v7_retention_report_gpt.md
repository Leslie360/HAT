# Tiny-ViT Results (GPT)


## Retention Sweep

- Source experiment: `V7_hybrid_hat_with_retention`
- Checkpoint: `checkpoints/V7_hybrid_hat_with_retention_best.pt`
- Saved epoch: 95
- Checkpoint best accuracy: 87.88%
- MC runs per time point: 10

| Exp | Dataset | Time (s) | Accuracy | Checkpoint |
|:----|:--------|---------:|:---------|:-----------|
| V7 | cifar10 | 0 | 19.61 +/- 0.33% (10 runs) | `checkpoints/V7_hybrid_hat_with_retention_best.pt` |
| V7 | cifar10 | 1 | 18.45 +/- 0.30% (10 runs) | `checkpoints/V7_hybrid_hat_with_retention_best.pt` |
| V7 | cifar10 | 10 | 18.27 +/- 0.39% (10 runs) | `checkpoints/V7_hybrid_hat_with_retention_best.pt` |
| V7 | cifar10 | 100 | 18.13 +/- 0.32% (10 runs) | `checkpoints/V7_hybrid_hat_with_retention_best.pt` |
| V7 | cifar10 | 1000 | 18.23 +/- 0.31% (10 runs) | `checkpoints/V7_hybrid_hat_with_retention_best.pt` |
| V7 | cifar10 | 10000 | 18.07 +/- 0.39% (10 runs) | `checkpoints/V7_hybrid_hat_with_retention_best.pt` |

## Notes

- `eval` mode reports repeated-run statistics for noisy experiments when `--eval-runs > 1`.
- `retention-sweep` reuses the ConvNeXt-style time grid and Monte Carlo summary format.
- These result files are GPT-scoped scratch artifacts and do not replace the canonical experiment reports.
