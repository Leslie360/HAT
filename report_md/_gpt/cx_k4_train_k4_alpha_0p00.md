> **⚠️ [INVALID — pre-ab56c2d]** This result was produced on code with wrong second-order signs (positive ltp_corr / ltd_corr). It is invalid under Branch A canonical semantics. Do not cite.

# Tiny-ViT Results (GPT)

| Mode | Exp | Name | Dataset | Primary Metric | Checkpoint |
|:-----|:----|:-----|:--------|:---------------|:-----------|
| train | V4 | V4_hybrid_standard_noise_hat_k4_alpha_0p00 | cifar10 | best_acc=91.92% @ epoch 95 | `/home/qiaosir/projects/compute_vit/checkpoints/_gpt/cx_k4_alpha/k4_alpha_0p00/V4_hybrid_standard_noise_hat_k4_alpha_0p00_best.pt` |

## Notes

- `eval` mode reports repeated-run statistics for noisy experiments when `--eval-runs > 1`.
- `retention-sweep` reuses the ConvNeXt-style time grid and Monte Carlo summary format.
- These result files are GPT-scoped scratch artifacts and do not replace the canonical experiment reports.
