# Device Profile Guide

This project uses a profile-driven abstraction so that literature priors and
measured device statistics can enter the same training and evaluation pipeline.

## Core Schema

The loader lives in `device_profile_utils.py`. A valid profile should provide:

- `device_type`: human-readable profile name
- `G_min` and either `G_max` or `dynamic_range`
- `n_states`
- `sigma_c2c`
- `sigma_d2d`
- `noise_mode`: `uniform` or `proportional`
- `source`

Optional fields:

- retention: `A_0`, `tau_1`, `tau_2`
- photoresponse: `gamma_phys`, `I_dark`, `responsivity_alpha`
- plasticity: `NL_LTP`, `NL_LTD`, `pulse_count_max`
- `inl_table`
- `profile_kind`
- `notes`

## Example

```json
{
  "source": "Zhang et al. Nature Communications 17, 197 (2026)",
  "profiles": [
    {
      "device_type": "Zhang 2026 OPECT",
      "G_min": 1.0,
      "G_max": 47.3,
      "n_states": 34,
      "sigma_c2c": 0.02,
      "sigma_d2d": 0.03,
      "noise_mode": "uniform",
      "retention": {
        "A_0": 0.6,
        "tau_1": 0.14,
        "tau_2": 0.61
      },
      "profile_kind": "literature"
    }
  ]
}
```

## Validation Rules

The public loader now rejects invalid profiles early.

- `G_min > 0`
- `G_max > G_min`
- `dynamic_range > 1.0`
- `n_states >= 2`
- `sigma_c2c >= 0`, `sigma_d2d >= 0`
- `noise_mode` must be `uniform` or `proportional`
- retention constants must be positive when present
- `A_0` must lie in `[0, 1]`
- `inl_table` must be strictly increasing

## Loading Paths

Profiles are typically loaded through:

- `run_device_comparison.py --device-profile-json ...`
- `eval_literature_profile.py`
- `eval_measured_profile.py`

The same schema supports canonical literature priors, synthetic sweeps, and
literature-derived case studies.

## Result Bundle

`eval_measured_profile.py` now emits a user-facing run bundle by default under:

- `outputs/measured_profile_runs/<run_id>/`

The bundle is the intended first stop after a run completes:

- `run_summary.md`: human-readable summary with checkpoint, profile list, accuracy table, and input coverage when audit metadata are available
- `metrics.csv`: compact machine-friendly metric table
- `profiles_used.json`: exact profile payload applied during the run
- `results.json`: full JSON evaluation payload

If the input profile JSON has a matching audit JSON, the bundle also includes:

- `profile_audit.json`

For the doctoral measured-profile flow, this means users no longer need to inspect
multiple `_gpt` artifacts manually to understand what was consumed, what was only
archived, and what final accuracy the run produced.
