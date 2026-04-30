# Codex Review Of `107-clean` Branch — 2026-04-30

## Branch Audited

- Branch: `origin/107-clean`
- Commit inspected locally: `ecda16c`
- Local inspection path: `/tmp/hat_107_clean`

## Verdict

This is now a usable clean deliverable branch for Remote 107.

Good properties:

- Small checkout, about 2.6 MB in local inspection.
- No checkpoint blobs.
- Standalone/orphan branch, suitable for server clone without dragging local paper/R11D history.
- `deliverable/code` uses relative imports.
- `--d2d-seed` added to training/eval path.
- `hat_config.json` is written with `analog_layers`, `d2d_seed`, and `n_states`.
- eval auto-loads `analog_layers` and `d2d_seed` from `hat_config.json` unless explicitly overridden.
- `py_compile` passed for core scripts and pipelines.

## Remaining Caveat

`pipeline_d2d_seed.py` currently measures device-specific adaptation if eval uses the same D2D seed stored in the checkpoint metadata.

That is useful, but it is not the same as fresh-device robustness.

Definitions:

- Same-instance/device-specific adaptation: train and eval use the same D2D offset pattern.
- Fresh-device generalization: train checkpoint is fixed, then eval overrides D2D pattern with unseen `--d2d-seed` values.

A paper claim about cross-device or fresh-device robustness requires the second definition.

## Required Correction

Add explicit cross-instance eval runs with `--d2d-seed` override. Do not rely on `hat_config.json` auto-loaded seed for the fresh-device eval table.

