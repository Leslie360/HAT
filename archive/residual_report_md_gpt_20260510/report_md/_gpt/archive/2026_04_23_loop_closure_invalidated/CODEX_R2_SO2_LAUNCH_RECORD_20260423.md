# Codex R2 SO2 Launch Record

**Date:** 2026-04-23 17:59 CST
**Owner:** Codex
**Status:** Running

## Purpose

R2 is the corrected second-order STE comparison against R1 first-order-only.

R1 established:

- source best: `91.50% @ epoch 96`
- fresh: `34.5612 +- 8.7878%` over `10x5`

R2 tests whether the repaired second-order correction improves or worsens this source/fresh behavior.

## Critical Launch Fix

Before launch, `scripts/_gpt/run_r2_so2_comparison_queue.sh` was corrected from:

- bad: `--use-second-order-ste --delta-g-eff 0.0`

To:

- good: `--use-second-order-ste --delta-g-eff -1.0`

Reason: in `analog_layers.py`, second-order correction activates only when `delta_g_eff > 0.0`. `0.0` is literal zero and would have produced a fake SO2 run. `-1.0` triggers auto-fill from effective module C2C+D2D noise, matching the validated Smoke B protocol.

## Launch Configuration

- git head: `33bed9c`
- script: `scripts/_gpt/run_r2_so2_comparison_queue.sh`
- group: `all`
- protected NL: `(1.0, -1.0)`
- global launch NL: `(2.0, -2.0)`
- SO2: enabled
- `delta_g_eff`: `-1.0` auto-fill
- `second_order_alpha`: `0.25`
- epochs: `100`
- batch size: `64`
- workers: `0`
- warm-start: `checkpoints/V4_hybrid_standard_noise_hat_best.pt`

## Live Early Result

Epoch 0:

- train loss: `0.3592`
- train acc: `88.18%`
- test acc: `76.94%`

Initial interpretation: source training is alive, but same-instance test starts lower than R1 epoch 0 (`83.21%`). Continue at least through epoch 4/9 before judging trajectory.

## Expected Artifacts

- queue log: `logs/_gpt/r2_so2_comparison_queue_*.log`
- train log: `logs/_gpt/r2_so2_comparison_train_*.log`
- train JSON: `report_md/_gpt/json_gpt/r2_so2_comparison_train.json`
- fresh JSON: `report_md/_gpt/json_gpt/r2_so2_comparison_fresh_eval.json`
- checkpoint dir: `checkpoints/_gpt/r2_so2_comparison/`
