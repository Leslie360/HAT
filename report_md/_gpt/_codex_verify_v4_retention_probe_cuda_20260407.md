# Tiny-ViT Results (GPT)


## Retention Sweep

- Source experiment: `V4_hybrid_standard_noise_hat`
- Checkpoint: `/home/qiaosir/projects/compute_vit/checkpoints/V4_hybrid_standard_noise_hat_best.pt`
- Saved epoch: 99
- Checkpoint best accuracy: 91.94%
- MC runs per time point: 3

| Exp | Dataset | Time (s) | Accuracy | Checkpoint |
|:----|:--------|---------:|:---------|:-----------|
| V4 | cifar10 | 0 | 91.77 +/- 0.28% (3 runs) | `/home/qiaosir/projects/compute_vit/checkpoints/V4_hybrid_standard_noise_hat_best.pt` |
| V4 | cifar10 | 1 | 82.29 +/- 1.02% (3 runs) | `/home/qiaosir/projects/compute_vit/checkpoints/V4_hybrid_standard_noise_hat_best.pt` |
| V4 | cifar10 | 10 | 79.71 +/- 0.34% (3 runs) | `/home/qiaosir/projects/compute_vit/checkpoints/V4_hybrid_standard_noise_hat_best.pt` |
| V4 | cifar10 | 100 | 78.76 +/- 0.47% (3 runs) | `/home/qiaosir/projects/compute_vit/checkpoints/V4_hybrid_standard_noise_hat_best.pt` |

## Notes

- `eval` mode reports repeated-run statistics for noisy experiments when `--eval-runs > 1`.
- `retention-sweep` reuses the ConvNeXt-style time grid and Monte Carlo summary format.
- These result files are GPT-scoped scratch artifacts and do not replace the canonical experiment reports.
