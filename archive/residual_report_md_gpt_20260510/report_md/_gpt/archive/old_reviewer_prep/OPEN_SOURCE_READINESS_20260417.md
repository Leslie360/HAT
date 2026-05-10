# Open-Source Readiness Audit

Date: 2026-04-17

## Scope

This audit covers the code and public-facing docs intended for an open-source release, with special attention to:

- hardcoded local paths
- references to private measured-data trees
- runnable public CLI entrypoints
- basic end-to-end closure for the public workflow

The following areas are treated as internal and should not be shipped as part of the public release bundle:

- `_archive/`
- `logs/`
- `report_md/`
- `数据_博士/`

## Fixed In This Pass

1. Replaced hardcoded local repo paths in active scripts with repo-relative bootstrap logic via `repo_bootstrap.py`.
2. Replaced hardcoded CrossSim paths with environment-driven discovery (`CROSSSIM_ROOT`) plus a repo-relative fallback.
3. Added public install manifests:
   - `requirements.txt`
   - `requirements-optional.txt`
4. Added a one-command public smoke-test helper:
   - `scripts/run_public_smoke_test.sh`
5. Removed private/raw-data assumptions from public docs and examples.
6. Changed measured-profile defaults from `doctor_*` naming to generic `measured_*` naming in public entrypoints:
   - `eval_measured_profile.py`
   - `scripts/_gpt/profile_auto_fitter_gpt.py`
7. Kept raw measured-data fitting explicit:
   - public mode requires `--raw-data-root`
   - demo mode remains available without private data
8. Deleted tracked `.pyc` files from the release set.
9. Fixed latent runtime issues in:
   - `train_tinyvit.py`
   - `train_convnext.py`
   - `inference_analysis_utils.py`
   - `experiment_nonideality_sweep.py`

## Verification Completed

### Syntax / import surface

- Full `py_compile` pass on non-archived Python files:
  - result: `compiled 105 python files`

### Unit tests

- `python -m unittest discover -p 'test*.py'`
  - result: `Ran 51 tests ... OK`

### Public smoke checks

- `bash scripts/run_public_smoke_test.sh`
  - result: passed when run with an explicit interpreter override (`PYTHON_BIN=...`)
- `python scripts/_gpt/profile_auto_fitter_gpt.py --demo ...`
  - result: passed, writes demo profile + audit outputs
- `python train_tinyvit.py --mode dry-run --experiment V4 --dataset cifar10`
  - result: passed
- `python run_device_comparison.py --help`
  - result: passed
- `python run_noise_sweep.py --help`
  - result: passed
- `python run_layer_sensitivity.py --help`
  - result: passed
- `python eval_measured_profile.py --help`
  - result: passed

### Leak scan

A tracked-file scan over code and public-facing docs found no remaining matches for:

- `/home/qiaosir`
- `DESKTOP-TLKV5NU`
- `2622507532@qq.com`
- `doctor_measured_profiles`
- `doctor_measured_profile`
- `DOCTOR_MEASURED_PROFILE_AUDIT`
- `数据_博士`
- `file:///home/qiaosir`

This clean result applies after excluding explicitly internal directories:

- `_archive/`
- `logs/`
- `report_md/`

## Residual Release Risks

1. The repository still contains internal materials and private-data references under excluded directories. These must not be included in the public release bundle.
2. CrossSim- and AIHWKIT-related flows are optional and require external installation. The public docs now reflect this, but they are not zero-dependency workflows.
3. Full training/evaluation still depends on datasets and checkpoints; the verified public closure here is:
   - install dependencies
   - run demo profile fitter
   - run dry-run / CLI entrypoints
   - execute tested utilities

## Release Recommendation

The active codebase is in acceptable shape for an open-source release if the published bundle excludes:

- `_archive/`
- `logs/`
- `report_md/`
- `数据_博士/`

For the code and public docs that are actually intended to ship, the current state is:

- path-safe
- test-clean
- syntax-clean
- demo/smoke runnable
- no remaining private-path markers in tracked release-facing files
