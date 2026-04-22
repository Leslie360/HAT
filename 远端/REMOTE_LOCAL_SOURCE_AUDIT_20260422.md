# Local Source Audit Summary

Date: 2026-04-22

This note records the local source audit that was triggered after the parity gap review.

## What was found

### 1. Local higher-order wrapper had an ambiguous `delta_g_eff` auto-fill rule

File:
- `scripts/_gpt/run_tinyvit_groupwise_nl_comp.py`

Old behavior:
- `delta_g_eff <= 0` meant auto-fill.
- Auto-fill used nominal `exp_cfg.sigma_d2d + exp_cfg.sigma_c2c`.

Why that matters:
- In standard noisy training, effective train-time `sigma_c2c` can be forced to `0.0`.
- So the old local auto-fill could include C2C that was not actually active in training.

Status:
- Fixed locally.
- New behavior:
  - `delta_g_eff < 0` => auto-fill
  - `delta_g_eff = 0.0` => literal zero
  - auto-fill uses the effective values already written into `module.config`

### 2. Local wrapper did not clear higher-order state when SO2 was disabled

Status:
- Fixed locally.

### 3. Local fresh-eval helper was CIFAR-10-specific

File:
- `scripts/_gpt/eval_joint_fresh_instance.py`

Old behavior:
- hard-coded `cifar10`, `num_classes=10`, `batch_size=256`

Status:
- Fixed locally.
- It now derives dataset / class count from the checkpoint unless overridden.

## What this means

- We did **not** find a hidden source bug that overturns the main paper conclusions.
- We **did** find a real local semantics bug that affects the interpretation of the higher-order parity branch.
- Future local/remote parity work should use the corrected semantics:
  - `delta_g_eff = 0.0` means literal zero
  - negative `delta_g_eff` means auto-fill
