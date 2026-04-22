# train_tinyvit_ensemble.py Restore Record

Date: 2026-04-22

## Incident

During local worktree validation, `train_tinyvit_ensemble.py` was found in an invalid state:

- path: `train_tinyvit_ensemble.py`
- observed size: `0 bytes`

This was inconsistent with the earlier same-session source inspection and would have invalidated any further local parity or training-script checks.

## Recovery action

Recovery source:
- `git show HEAD:train_tinyvit_ensemble.py`

Recovery method:
- overwrite the zero-byte worktree file using the `HEAD` blob content
- preserve a forensic snapshot of the zero-byte state

Forensic snapshot:
- `report_md/_gpt/train_tinyvit_ensemble.py.zero_byte_snapshot_20260422`

## Post-recovery validation

Validated after restore:

1. Module import restored:
   - `get_v_experiment_configs`
   - `train_one_epoch`
   - `set_noise_for_train`

2. Syntax compile passed for:
   - `train_tinyvit_ensemble.py`
   - `scripts/_gpt/run_tinyvit_groupwise_nl_comp.py`
   - `scripts/_gpt/eval_joint_fresh_instance.py`

3. CLI help regression also fixed:
   - escaped the `%` sign in the `--compile` argparse help string
   - `run_tinyvit_groupwise_nl_comp.py --help` now exits cleanly

## Scope note

This restore does not change any scientific result by itself.
It restores the local training entrypoint to a runnable state so that subsequent parity checks and local reruns can be trusted.
