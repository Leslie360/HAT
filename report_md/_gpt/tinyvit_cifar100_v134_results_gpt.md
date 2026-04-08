# Tiny-ViT Results (GPT)

| Mode | Exp | Name | Dataset | Primary Metric | Checkpoint |
|:-----|:----|:-----|:--------|:---------------|:-----------|
| train | V1 | V1_fp32_digital_baseline | cifar100 | best_acc=86.94% @ epoch 94 | `checkpoints/_gpt/cifar100/V1_fp32_digital_baseline_best.pt` |
| train | V3 | V3_hybrid_standard_noise_standard_train | cifar100 | best_acc=44.06% @ epoch 64 | `checkpoints/_gpt/cifar100/V3_hybrid_standard_noise_standard_train_best.pt` |
| train | V4 | V4_hybrid_standard_noise_hat | cifar100 | best_acc=65.48% @ epoch 85 | `checkpoints/_gpt/cifar100/V4_hybrid_standard_noise_hat_best.pt` |

## Notes

- `eval` mode reports repeated-run statistics for noisy experiments when `--eval-runs > 1`.
- `retention-sweep` reuses the ConvNeXt-style time grid and Monte Carlo summary format.
- These result files are GPT-scoped scratch artifacts and do not replace the canonical experiment reports.
