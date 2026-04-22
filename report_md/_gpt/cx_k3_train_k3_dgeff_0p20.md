# Tiny-ViT Results (GPT)

| Mode | Exp | Name | Dataset | Primary Metric | Checkpoint |
|:-----|:----|:-----|:--------|:---------------|:-----------|
| train | V4 | V4_hybrid_standard_noise_hat_k3_dgeff_0p20 | cifar10 | best_acc=91.50% @ epoch 93 | `/home/qiaosir/projects/compute_vit/checkpoints/_gpt/cx_k3_dgeff/k3_dgeff_0p20/V4_hybrid_standard_noise_hat_k3_dgeff_0p20_best.pt` |

## Notes

- `eval` mode reports repeated-run statistics for noisy experiments when `--eval-runs > 1`.
- `retention-sweep` reuses the ConvNeXt-style time grid and Monte Carlo summary format.
- These result files are GPT-scoped scratch artifacts and do not replace the canonical experiment reports.
