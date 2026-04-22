# Tiny-ViT Results (GPT)

| Mode | Exp | Name | Dataset | Primary Metric | Checkpoint |
|:-----|:----|:-----|:--------|:---------------|:-----------|
| train | V4 | V4_hybrid_standard_noise_hat_j1d_historical_auto | cifar10 | best_acc=46.75% @ epoch 0 | `/home/qiaosir/projects/compute_vit/checkpoints/_gpt/cx_parity_minimal/j1d_historical_auto/V4_hybrid_standard_noise_hat_j1d_historical_auto_best.pt` |

## Notes

- `eval` mode reports repeated-run statistics for noisy experiments when `--eval-runs > 1`.
- `retention-sweep` reuses the ConvNeXt-style time grid and Monte Carlo summary format.
- These result files are GPT-scoped scratch artifacts and do not replace the canonical experiment reports.
