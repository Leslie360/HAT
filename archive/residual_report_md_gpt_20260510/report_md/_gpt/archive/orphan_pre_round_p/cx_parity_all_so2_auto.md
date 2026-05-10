> **⚠️ [INVALID — pre-ab56c2d]** This result was produced on code with wrong second-order signs (positive ltp_corr / ltd_corr). It is invalid under Branch A canonical semantics. Do not cite.

# Tiny-ViT Results (GPT)

| Mode | Exp | Name | Dataset | Primary Metric | Checkpoint |
|:-----|:----|:-----|:--------|:---------------|:-----------|
| train | V4 | V4_hybrid_standard_noise_hat_all_so2_auto | cifar10 | best_acc=83.34% @ epoch 0 | `/home/qiaosir/projects/compute_vit/checkpoints/_gpt/cx_parity_minimal/all_so2_auto/V4_hybrid_standard_noise_hat_all_so2_auto_best.pt` |

## Notes

- `eval` mode reports repeated-run statistics for noisy experiments when `--eval-runs > 1`.
- `retention-sweep` reuses the ConvNeXt-style time grid and Monte Carlo summary format.
- These result files are GPT-scoped scratch artifacts and do not replace the canonical experiment reports.
