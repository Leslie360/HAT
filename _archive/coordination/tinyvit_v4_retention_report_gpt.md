# Tiny-ViT Results (GPT)


## Retention Sweep

- Source experiment: `V4_hybrid_standard_noise_hat`
- Checkpoint: `checkpoints/V4_hybrid_standard_noise_hat_best.pt`
- Saved epoch: 99
- Checkpoint best accuracy: 91.94%
- MC runs per time point: 10

| Exp | Dataset | Time (s) | Accuracy | Checkpoint |
|:----|:--------|---------:|:---------|:-----------|
| V4 | cifar10 | 0 | 91.63 +/- 0.18% (10 runs) | `checkpoints/V4_hybrid_standard_noise_hat_best.pt` |
| V4 | cifar10 | 1 | 82.66 +/- 0.67% (10 runs) | `checkpoints/V4_hybrid_standard_noise_hat_best.pt` |
| V4 | cifar10 | 10 | 79.13 +/- 0.64% (10 runs) | `checkpoints/V4_hybrid_standard_noise_hat_best.pt` |
| V4 | cifar10 | 100 | 79.05 +/- 0.47% (10 runs) | `checkpoints/V4_hybrid_standard_noise_hat_best.pt` |
| V4 | cifar10 | 1000 | 79.35 +/- 0.72% (10 runs) | `checkpoints/V4_hybrid_standard_noise_hat_best.pt` |
| V4 | cifar10 | 10000 | 79.51 +/- 0.66% (10 runs) | `checkpoints/V4_hybrid_standard_noise_hat_best.pt` |

## Notes

- `eval` mode reports repeated-run statistics for noisy experiments when `--eval-runs > 1`.
- `retention-sweep` reuses the ConvNeXt-style time grid and Monte Carlo summary format.
- These result files are GPT-scoped scratch artifacts and do not replace the canonical experiment reports.
