# Tiny-ViT Results (GPT)

| Mode | Exp | Name | Dataset | Primary Metric | Checkpoint |
|:-----|:----|:-----|:--------|:---------------|:-----------|
| train | V1 | V1_fp32_digital_baseline | cifar10 | best_acc=97.48% @ epoch 99 | `checkpoints/V1_fp32_digital_baseline_best.pt` |

## Notes

- `eval` mode reports repeated-run statistics for noisy experiments when `--eval-runs > 1`.
- These result files are GPT-scoped scratch artifacts and do not replace the canonical experiment reports.
