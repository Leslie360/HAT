# Tiny-ViT Results (GPT)

| Mode | Exp | Name | Dataset | Primary Metric | Checkpoint |
|:-----|:----|:-----|:--------|:---------------|:-----------|
| train | V1 | V1_fp32_digital_baseline | flowers102 | best_acc=97.97% @ epoch 10 | `checkpoints/_gpt/flowers102/V1_fp32_digital_baseline_best.pt` |
| train | V3 | V3_hybrid_standard_noise_standard_train | flowers102 | best_acc=4.81% @ epoch 34 | `checkpoints/_gpt/flowers102/V3_hybrid_standard_noise_standard_train_best.pt` |
| train | V4 | V4_hybrid_standard_noise_hat | flowers102 | best_acc=22.48% @ epoch 94 | `checkpoints/_gpt/flowers102/V4_hybrid_standard_noise_hat_best.pt` |

## Notes

- `eval` mode reports repeated-run statistics for noisy experiments when `--eval-runs > 1`.
- `retention-sweep` reuses the ConvNeXt-style time grid and Monte Carlo summary format.
- These result files are GPT-scoped scratch artifacts and do not replace the canonical experiment reports.
