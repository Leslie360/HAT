# Codex Dual-Bug Smoke Results (2026-04-23)

## Smoke A: first-order only
- Command family: `group=all`, no SO2, 1 epoch, warm-start from `checkpoints/V4_hybrid_standard_noise_hat_best.pt`
- Log: `logs/_gpt/smoke_a_first_order_20260423.log`
- Checkpoint: `checkpoints/_gpt/smoke_a_first_order/V4_hybrid_standard_noise_hat_smoke_a_first_order_best.pt`
- Result:
  - train_acc = `88.44%`
  - test_acc = `81.44%`

## Smoke B: corrected SO2
- Command family: `group=all`, SO2 on, `alpha=0.25`, `delta_g_eff=-1.0`, 1 epoch, warm-start from `checkpoints/V4_hybrid_standard_noise_hat_best.pt`
- Log: `logs/_gpt/smoke_b_second_order_fix_20260423.log`
- Checkpoint: `checkpoints/_gpt/smoke_b_second_order_fix/V4_hybrid_standard_noise_hat_smoke_b_second_order_fix_best.pt`
- Result:
  - train_acc = `87.75%`
  - test_acc = `80.29%`

## Decision
- Both smoke runs are numerically sane.
- First-order only is slightly better (`81.44%` vs `80.29%`) and materially cheaper.
- Proceed with `R1` as the first clean canonical rerun:
  - `group=all`
  - no SO2
  - full training
  - `10x5` fresh-instance eval
- Corrected SO2 remains a follow-up comparison line, not the first recovery anchor.
