# CrossSim Clean Baseline Audit — 2026-04-16

## Status

The latest full clean-baseline rerun does **not** satisfy the original `>85%` CrossSim gate.

## Canonical artifact sources

- JSON: [crosssim_clean_baseline.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/crosssim_clean_baseline.json)
- Log: [crosssim_clean.log](/home/qiaosir/projects/compute_vit/logs/_gpt/crosssim_clean.log)
- Script: [run_crosssim_convnext.py](/home/qiaosir/projects/compute_vit/run_crosssim_convnext.py)

## Latest validated result

Latest JSON timestamp:

- `2026-04-16T13:28:17`

Observed clean-baseline accuracy on CIFAR-10, first 1000 samples:

| Path | Accuracy |
|:--|--:|
| Our framework (`sigma_c2c=0`, `sigma_d2d=0`, ADC=8b) | 86.20% |
| CrossSim clean (`alpha_noise=0`, `alpha_error=0`, ADC=8b) | 83.70% |

Dispatch gate under the latest rerun:

- `our framework > 85%`: pass
- `CrossSim > 85%`: fail

## Important note on superseded earlier runs

Earlier clean-baseline runs on the same day logged `CrossSim = 90.70%`, but those runs were later superseded by a newer full rerun that overwrote the canonical JSON/log artifacts.

The project should therefore use the latest artifact state above, not the earlier provisional number.

## Interpretation

The current clean-baseline mismatch is moderate rather than catastrophic:

- CrossSim clean is not collapsing to random chance.
- But it remains `2.50 pp` below the framework clean result on the same 1000-sample slice.
- This means the CrossSim path is now plausible enough for exploratory comparison, but it still does not meet the original strict alignment gate.

## Root-cause history

The earlier `10.60%` failure was caused by incorrect ADC calibration semantics in `run_crosssim_convnext.py`.

The broken version used ordinary PyTorch output min/max as CrossSim ADC ranges. The fixed version now uses CrossSim-native ADC profiling:

1. convert the effective digital model with ADC profiling enabled
2. collect profiled ADC inputs via `get_profiled_adc_inputs(...)`
3. calibrate limits with `calibrate_adc_limits(...)`
4. rebuild the final CrossSim model with calibrated limits

That fix removed the catastrophic failure, but the latest full rerun still shows a residual clean-gap (`86.20%` vs `83.70%`).

## Current implication for CX-4

- Phase 1 is no longer a strict pass under the latest canonical artifacts.
- Phase 2 low-noise results can still be used as exploratory data.
- Phase 3 standard-noise should be treated as conditional / in-progress until its runtime behavior and accuracy are confirmed.
