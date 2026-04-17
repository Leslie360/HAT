# Tiny-ViT Results (GPT)

| Mode | Exp | Name | Dataset | Primary Metric | Checkpoint |
|:-----|:----|:-----|:--------|:---------------|:-----------|
| eval | V4 | V4_hybrid_standard_noise_hat | cifar10 | acc=97.37% +/- 0.05 (10 runs) | `/home/qiaosir/projects/compute_vit/checkpoints/_gpt/task34_v4_proportional_hat/V4_hybrid_standard_noise_hat_best.pt` |

## Notes

- `eval` mode reports repeated-run statistics for noisy experiments when `--eval-runs > 1`.
- `retention-sweep` reuses the ConvNeXt-style time grid and Monte Carlo summary format.
- These result files are GPT-scoped scratch artifacts and do not replace the canonical experiment reports.
