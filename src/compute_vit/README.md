# src/compute_vit/

Future importable package home for core Python libraries.

Current implementation modules live here. Tests add this directory to `sys.path` through `tests/conftest.py` so existing bare imports continue to work during the migration.

## Intended future contents

- `analog_layers.py`
- `analog_layers_ensemble.py`
- `inference_analysis_utils.py`
- `amp_utils.py`
- `device_profile_utils.py`
- `tinyvit_hybrid_utils.py`
- `report_asset_paths.py`
- `model_profiling.py`
- `physical_noise_pipeline.py`
- `hybrid_calibration.py`
- `hybrid_runtime_compiler.py`

## Migration rule

Move one module family at a time, update imports, keep root compatibility wrappers if needed, then run tests and CLI `--help` checks.
