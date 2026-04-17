# Doctor Measured Profile Validation — 2026-04-16

## Deliverables

- Fitter: `/home/qiaosir/projects/compute_vit/scripts/_gpt/profile_auto_fitter_gpt.py`
- Eval entrypoint: `/home/qiaosir/projects/compute_vit/eval_measured_profile.py`
- Compatibility fixes: `/home/qiaosir/projects/compute_vit/inference_analysis_utils.py`
- Measured profiles JSON: `/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/doctor_measured_profiles.json`
- Fitter diagnostics JSON: `/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/doctor_measured_profile_summary.json`
- Fitter audit markdown: `/home/qiaosir/projects/compute_vit/report_md/_gpt/DOCTOR_MEASURED_PROFILE_AUDIT_20260416.md`

## Raw-data coverage

Consumed directly from `数据_博士`:

- `第三页/a/小图_raw_ppf_points.txt`: direct raw PPF inset points (`ΔT` vs PPF ratio)
- `第三页/a/小图.txt`: `Origin ExpDec1 fit of G` report sheet for the same inset, kept as diagnostics rather than raw source points
- `第三页/b/5-20paule.txt`: pulse-count EPSC curves
- `第三页/c/300-800.txt`: pulse-width EPSC curves
- `第三页/g/图.txt`: 8 RC-state decay curves
- `第三页/h/100sID.txt`: 8-state readout at 100 s
- `第四页/d/256次线性作图.txt`: multistate programming curve
- `第四页/e/s0-s5.txt`: duplicated retention / repeatability curves
- `第四页/i/pot.txt`: photoresponse sweep
- `第20页/16.txt`, `第20页/64.txt`: RC-specific state ladders

Not injected into the JSON profile:

- `第四页/l/pot.txt`: retained as unresolved panel `(l)/(m)` support data
- `第三页/a/大图.txt`: large panel retained as context only

## Fitted profile family

Two measured nonvolatile profiles were emitted:

1. `Doctor OECT Nonvolatile RC-16`
2. `Doctor OECT Nonvolatile RC-64`

Shared fitted properties:

- photoresponse: `gamma_phys = 0.8771`, `I_dark = 3.85385e-10`, `responsivity_alpha = 9.6907e-12`
- retention: `A_0 = 0.9647`, `tau_1 = 10.83`, `tau_2 = 1.9269e8`
- `sigma_d2d = 0.0` by design because no explicit multi-device distribution was present in the supplied PPT export

Profile-specific properties:

- `RC-16`: `G_range = 5.75x`, `sigma_c2c = 0.00272`
- `RC-64`: `G_range = 6.18x`, `sigma_c2c = 0.00369`

## Validation runs

All validation runs used Tiny-ViT V4 on CIFAR-10, `max_samples = 1000`, `eval_runs = 1`.

### Ensemble-HAT checkpoint

Command target:
- `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt`

Results:
- `Doctor OECT Nonvolatile RC-16`: `89.8%`
- `Doctor OECT Nonvolatile RC-64`: `89.2%`

Artifact:
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/doctor_measured_profile_eval.json`

### Standard-HAT checkpoint

Command target:
- `checkpoints/V4_hybrid_standard_noise_hat_best.pt`

Results:
- `Doctor OECT Nonvolatile RC-16`: `10.2%`
- `Doctor OECT Nonvolatile RC-64`: `10.2%`

Artifact:
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/doctor_measured_profile_eval_standard_hat.json`

### Literature anchor for comparison

Command target:
- `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt`
- profile: `Organic OPECT Zhang2025 Literature-Fitted`

Result:
- `89.7%`

Artifact:
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/ensemble_literature_profile_eval.json`

## Interpretation

1. The raw-measurement to JSON fitting path is now real, not a stub.
2. The fitted JSON loads cleanly into the existing simulator stack after the compatibility fixes below.
3. The measured-device substitution result is regime-dependent:
   - on the Ensemble-HAT checkpoint, the doctoral measured profiles remain in the high-accuracy regime (`~89%`)
   - on the standard-HAT checkpoint, the same fresh-profile substitution collapses to chance (`10.2%`)
4. This matches the paper's broader conclusion that fresh-profile / fresh-instance transferability is primarily a training-recipe issue, not just a profile-schema issue.

## Compatibility fixes landed while validating

1. `eval_measured_profile.py`
- replaced the broken `load_profiles` call with `load_device_profiles_json`
- added `--checkpoint-path`
- added subset evaluation support through `--max-samples`
- supports multi-profile JSON evaluation in one invocation

2. `inference_analysis_utils.py`
- fixed Tiny-ViT import fallback so `get_num_classes` and `TinyViTPhysicalFrontEnd` resolve correctly
- fixed `evaluate_once()` so it dispatches correctly across the two Tiny-ViT `evaluate()` signatures
- fixed `apply_device_profile()` to move `inl_table` tensors onto the module device
- fixed `snapshot_analog_state()` / `restore_analog_state()` so `inl_table` survives round-trips cleanly

## Remaining limitation

The third-page PPF inset is now archived in two forms:

- raw points: `第三页/a/小图_raw_ppf_points.txt`
- fit diagnostics: `第三页/a/小图.txt`

Neither is injected into the current JSON profile because the present nonvolatile weight-storage schema has no dedicated short-term facilitation field.
