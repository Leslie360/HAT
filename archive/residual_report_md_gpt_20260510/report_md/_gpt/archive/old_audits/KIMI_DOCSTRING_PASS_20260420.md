# Docstring Pass – Core compute_vit Modules (2026-04-20)

## Goal
Add module-level and public-API docstrings so a reader of the Zenodo archive can reproduce Fig. 4 without a lab walk-through.

## Modules Identified
The five most-referenced Python modules matching the requested categories:

| # | Category | File | Import references |
|---|----------|------|-------------------|
| 1 | Training loop | `train_tinyvit.py` | 127 |
| 2 | D2D resampler / mismatch injector | `train_tinyvit_ensemble.py` | 24 |
| 3 | Profile loader | `device_profile_utils.py` | 29 |
| 4 | Evaluation harness | `inference_analysis_utils.py` | 41 |
| 5 | Analog layers / STE quantizer | `analog_layers.py` | 71 |

Counts are grep hits for `import <module>` or `from <module>` across `compute_vit/` and `scripts/`.

## Changes per file

### `train_tinyvit.py`
- **Module docstring**: Expanded to describe the file’s role in producing Fig. 4 cross-dataset accuracy bars.
- **Public API docstrings**: Added 1-line docstrings to 26 functions/classes, including:
  - `TinyViTExperimentConfig`, `get_v_experiment_configs`, `build_model`, `get_dataloaders`, `train_one_epoch`, `evaluate`, `set_seed`, `set_noise_for_eval`, `set_noise_for_train`, `set_retention`, `maybe_resume_experiment`, `summarize_eval_runs`, `build_results_markdown`, `export_result_rows`, `resolve_checkpoint_path`, `main`, etc.

### `train_tinyvit_ensemble.py`
- **Module docstring**: Replaced with a paragraph explaining ensemble HAT, per-epoch D2D resampling, and energy estimation.
- **Public API docstrings**: Added 1-line docstrings to 32 top-level functions, including:
  - `resample_all_d2d_noise`, `run_experiment`, `run_eval`, `run_retention_sweep`, `collect_module_shapes`, `build_energy_plan`, `format_experiment_matrix`, `export_dry_run_report`, `run_dry_run`, `main`, and all shared helpers (`build_model`, `evaluate`, `train_one_epoch`, etc.).

### `device_profile_utils.py`
- **Module docstring**: Expanded to explain JSON ingestion and linkage to `inference_analysis_utils.apply_device_profile()`.
- **Public API docstrings**: Added to `load_device_profiles_json`, `select_device_profile`, `profile_to_payload`, `dump_device_profiles_json`.

### `inference_analysis_utils.py`
- **Module docstring**: Expanded to describe Monte-Carlo evaluation, device-profile application, and ADC calibration.
- **Public API docstrings**: Added to 18 functions/classes, including:
  - `ModelBundle`, `iter_analog_modules`, `snapshot_analog_state`, `restore_analog_state`, `apply_device_profile`, `set_uniform_noise`, `set_uniform_retention`, `collect_analog_noise_diagnostics`, `load_model_bundle`, `evaluate_once`, `run_mc_eval`, `calibrate_adc_ranges`, `ADCQuantHookManager.__init__`, `export_rows`, `adc_bits_label`, etc.

### `analog_layers.py`
- **Module docstring**: Appended a sentence linking the layer definitions to Fig. 4 hybrid models.
- **Public API docstrings**: Added to 9 functions/methods, including:
  - `AnalogLinear.resample_d2d_noise`, `AnalogConv2d.resample_d2d_noise`, `AnalogConv2d.forward`, `EnergyProfiler.estimate_latency`, `enable_sparsity_tracking`, `disable_sparsity_tracking`, `reset_sparsity_tracking`, `get_sparsity_report`, `resample_d2d_buffers`.

## Verification
All modified files pass `python3 -m py_compile` without syntax errors. No logic was changed.
