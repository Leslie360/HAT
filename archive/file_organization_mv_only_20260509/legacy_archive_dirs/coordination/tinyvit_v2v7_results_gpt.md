# Tiny-ViT Results (GPT)

| Mode | Exp | Name | Dataset | Primary Metric | Checkpoint |
|:-----|:----|:-----|:--------|:---------------|:-----------|
| train | V2 | V2_hybrid_no_noise | cifar10 | best_acc=97.38% @ epoch 94 | `checkpoints/V2_hybrid_no_noise_best.pt` |
| train | V3 | V3_hybrid_standard_noise_standard_train | cifar10 | best_acc=89.54% @ epoch 99 | `checkpoints/V3_hybrid_standard_noise_standard_train_best.pt` |
| train | V4 | V4_hybrid_standard_noise_hat | cifar10 | best_acc=91.94% @ epoch 99 | `checkpoints/V4_hybrid_standard_noise_hat_best.pt` |
| train | V5 | V5_hybrid_pessimistic_noise_hat | cifar10 | best_acc=88.11% @ epoch 89 | `checkpoints/V5_hybrid_pessimistic_noise_hat_best.pt` |
| train | V6 | V6_hybrid_hat_with_physical_frontend | cifar10 | best_acc=82.58% @ epoch 96 | `checkpoints/V6_hybrid_hat_with_physical_frontend_best.pt` |
| train | V7 | V7_hybrid_hat_with_retention | cifar10 | best_acc=87.88% @ epoch 95 | `checkpoints/V7_hybrid_hat_with_retention_best.pt` |

## Notes

- `eval` mode reports repeated-run statistics for noisy experiments when `--eval-runs > 1`.
- `retention-sweep` reuses the ConvNeXt-style time grid and Monte Carlo summary format.
- These result files are GPT-scoped scratch artifacts and do not replace the canonical experiment reports.
