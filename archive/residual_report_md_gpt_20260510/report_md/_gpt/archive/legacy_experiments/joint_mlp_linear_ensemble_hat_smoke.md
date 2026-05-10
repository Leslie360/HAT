# Tiny-ViT Results (GPT)

| Mode | Exp | Name | Dataset | Primary Metric | Checkpoint |
|:-----|:----|:-----|:--------|:---------------|:-----------|
| train | V4 | V4_hybrid_standard_noise_hat_joint_mlp_linear_ensemble_hat_smoke | cifar10 | best_acc=28.44% @ epoch 1 | `/home/qiaosir/projects/compute_vit/checkpoints/_gpt/joint_mlp_linear_ensemble_hat_smoke/V4_hybrid_standard_noise_hat_joint_mlp_linear_ensemble_hat_smoke_best.pt` |

## Notes

- `eval` mode reports repeated-run statistics for noisy experiments when `--eval-runs > 1`.
- `retention-sweep` reuses the ConvNeXt-style time grid and Monte Carlo summary format.
- These result files are GPT-scoped scratch artifacts and do not replace the canonical experiment reports.
