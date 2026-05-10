# Root Python Cleanup Audit

Date: 2026-05-10
Scope: `/home/qiaosir/projects/compute_vit` root files

## Current root state

Root Markdown is already clean and limited to:

- `README.md`
- `PROJECT_INDEX.md`
- `WORKSPACE_LAYOUT.md`

Root still contains 21 Python files plus config/license files. This is visually busy, but most Python files are either import-sensitive libraries or documented experiment entrypoints.

## Root Python classification

| Group | Files | Cleanup stance |
|:--|:--|:--|
| Core import-sensitive libraries | `analog_layers.py`, `analog_layers_ensemble.py`, `inference_analysis_utils.py`, `amp_utils.py`, `device_profile_utils.py`, `tinyvit_hybrid_utils.py`, `report_asset_paths.py`, `model_profiling.py`, `physical_noise_pipeline.py`, `hybrid_calibration.py`, `hybrid_runtime_compiler.py` | Do not move directly; many imports and historical scripts assume root import path. Future cleanup needs package migration or compatibility wrappers. |
| Training entrypoints | `train_tinyvit.py`, `train_tinyvit_ensemble.py`, `train_convnext.py`, `train_resnet18.py` | Keep root until wrappers/CLI are introduced; these are user-facing reproducibility commands. |
| Evaluation entrypoints | `eval_fresh_instances.py`, `eval_fresh_instances_postfix.py`, `eval_imagenet_analog.py`, `eval_literature_profile.py`, `eval_measured_profile.py`, `eval_resnet18_checkpoints.py` | Keep root until wrappers/CLI are introduced; these are user-facing evaluation commands. |

## Config and non-Python root files

| File | Stance |
|:--|:--|
| `.gitignore`, `LICENSE`, `environment.yml`, `requirements.txt`, `requirements-optional.txt` | Keep root. Standard repo entry/config files. |
| `auto_fitted_profile.json` | Candidate to move to `device_profiles/` after checking references; do not move blindly. |
| `download_data.sh` | Candidate to move to `scripts/` with a root wrapper, but keep until references are checked. |

## Recommended next cleanup strategy

To make root truly clean without breaking imports:

1. Introduce a package directory, e.g. `compute_vit_core/`, for import-sensitive libraries.
2. Move one library family at a time and update imports in tests/scripts.
3. Keep root wrappers for public commands:
   - `train_*.py`
   - `eval_*.py`
   - `download_data.sh`
4. Move non-public utilities only after grep/import checks.
5. Run tests and key `--help` checks after each small move.

## Current decision

Root Python implementation files were migrated on 2026-05-10:

- implementation modules now live under `src/compute_vit/`;
- user-facing wrappers live under `cli/`;
- `tests/conftest.py` adds `src/compute_vit` to `sys.path` for existing bare-import tests;
- syntax validation passed with `python -m py_compile compute_vit/src/compute_vit/*.py compute_vit/cli/*.py compute_vit/tests/conftest.py`;
- runtime `--help` checks were not used as success criteria because this shell environment lacks `torch`.

Restore script:

`archive/reorg_20260509/restore/ROOT_PYTHON_MIGRATION_20260510_RESTORE.sh`
