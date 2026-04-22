# Tiny-ViT Results (GPT)

| Mode | Exp | Name | Dataset | Primary Metric | Checkpoint |
|:-----|:----|:-----|:--------|:---------------|:-----------|
| train | V4 | V4_hybrid_standard_noise_hat_second_order_ste | cifar10 | best_acc=91.02% @ epoch 78 | `checkpoints/_gpt/second_order_ste/V4_hybrid_standard_noise_hat_second_order_ste_best.pt` |

## Notes

- `eval` mode reports repeated-run statistics for noisy experiments when `--eval-runs > 1`.
- `retention-sweep` reuses the ConvNeXt-style time grid and Monte Carlo summary format.
- These result files are GPT-scoped scratch artifacts and do not replace the canonical experiment reports.
