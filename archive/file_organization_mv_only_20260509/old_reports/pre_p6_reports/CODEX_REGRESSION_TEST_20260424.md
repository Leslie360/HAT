# Codex Regression Test - Eval NL Provenance
Date: 2026-04-24

## Purpose

Prevent recurrence of the false Proportional HAT `90.88%` interpretation, where a checkpoint trained at `NL=1.0/-1.0` was evaluated with forced `NL=2.0/-2.0`.

## Code Changes

- `eval_fresh_instances_postfix.py`
  - Reads checkpoint metadata before evaluation.
  - Defaults `eval NL` and `noise_mode` to checkpoint `exp_cfg`.
  - Rejects CLI-provided NL/noise values that differ from checkpoint metadata unless `--allow-eval-nl-override` is explicit.
  - Writes checkpoint provenance fields into the fresh-eval JSON.

- `test_dual_bug_fix.py`
  - Added `test_eval_provenance_rejects_silent_nl_mismatch`.

## Verification

Command:

```bash
/home/qiaosir/miniconda3/envs/LLM/bin/python -m py_compile eval_fresh_instances_postfix.py test_dual_bug_fix.py train_tinyvit_ensemble.py
/home/qiaosir/miniconda3/envs/LLM/bin/python test_dual_bug_fix.py
```

Result:

- `test_dual_bug_fix.py`: `6` tests passed.

## Operational Effect

M-series fresh eval still passes explicit `--nl-ltp 2.0 --nl-ltd -2.0` because the trained checkpoints are also `NL=2.0/-2.0`.
Any future train/eval NL mismatch now aborts by default and must be consciously marked with `--allow-eval-nl-override`.
