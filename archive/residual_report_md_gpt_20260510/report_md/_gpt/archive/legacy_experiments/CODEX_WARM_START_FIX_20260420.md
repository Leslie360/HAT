# Codex Warm-Start Fix — 2026-04-20

## Problem

Round M joint-training smoke exposed a real resume-semantics bug:

- naive reuse of a canonical Ensemble HAT checkpoint inherited
  - saved epoch counters,
  - optimizer state,
  - scheduler state,
  - scaler state,
  - best-accuracy tracking.

This made checkpoint reuse unsafe for warm-start experiments, because a short pilot could immediately skip training if the copied checkpoint had already reached the target epoch budget.

## Fix

Implemented a dedicated weights-only warm-start path in:

- `train_tinyvit_ensemble.py`

New CLI flag:

- `--warm-start-from <checkpoint>`

Behavior:

1. load `model_state_dict` only;
2. validate dataset / classifier compatibility using the existing checkpoint guard;
3. do **not** restore:
   - `epoch`
   - `best_acc`
   - `best_epoch`
   - `optimizer_state_dict`
   - `scheduler_state_dict`
   - `scaler_state_dict`
   - training history;
4. require `--resume-existing` and `--warm-start-from` to be mutually exclusive.

## Validation

Validation run:

- command family: `scripts/_gpt/run_tinyvit_groupwise_nl_comp.py`
- regime: `V4`, `CIFAR-10`, `1 epoch`
- warm-start source: `checkpoints/V4_hybrid_standard_noise_hat_best.pt`
- save dir: `checkpoints/_gpt/warm_start_fix_smoke`

Artifacts:

- log: `logs/_gpt/warm_start_fix_smoke_20260420.log`
- JSON: `report_md/_gpt/json_gpt/warm_start_fix_smoke.json`
- CSV: `report_md/_gpt/csv_gpt/warm_start_fix_smoke.csv`
- MD: `report_md/_gpt/warm_start_fix_smoke.md`

Observed behavior:

- log explicitly reports:
  - `Warm-start mode: weights only; epoch/best/optimizer/scheduler state reset.`
  - `Warm-start ready: start_epoch=0/1`
- training did **not** skip due to stale epoch counters
- `best_acc` tracking worked normally:
  - `Epoch 0/1 ... test_acc=81.71% (best=81.71%)`
  - `Finished. Best accuracy: 81.71% at epoch 0`

## Verdict

`CX-GA` is complete.

The warm-start path is now safe for future Round O / thesis-only joint-training runs. No submission-facing manuscript numbers depend on this patch.
