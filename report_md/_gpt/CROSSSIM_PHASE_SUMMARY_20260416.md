# CrossSim Phase Summary — 2026-04-16

## Scope

Checkpoint and evaluation target:

- checkpoint: `checkpoints/C4_4bit_noise_HAT_best.pt`
- dataset: `cifar10`
- samples per phase: `1000`
- ADC bits: `8`
- weight bits: `4`

Artifacts:

- clean baseline: `/home/qiaosir/projects/compute_vit/report_md/_gpt/crosssim_clean_baseline.json`
- low noise: `/home/qiaosir/projects/compute_vit/report_md/_gpt/crosssim_low_noise.json`
- standard noise: `/home/qiaosir/projects/compute_vit/report_md/_gpt/crosssim_standard_noise.json`

## Results

| Phase | Noise setting | Our framework | CrossSim | Gap (ours - CrossSim) |
|:--|:--|--:|--:|--:|
| Phase 1 | clean (`sigma_c2c=0`, `sigma_d2d=0`) | 86.20% | 83.70% | 2.50 pp |
| Phase 2 | low noise (`sigma_c2c=1%`, `sigma_d2d=1%`) | 85.90 ± 0.28% | 82.87 ± 0.29% | 3.03 pp |
| Phase 3 | standard noise (`sigma_c2c=5%`, `sigma_d2d=5%`) | 81.63 ± 0.56% | 67.20 ± 2.67% | 14.43 pp |

## Phase 3 detail

Our-framework accuracies:

- `82.4`, `81.1`, `81.4`

CrossSim accuracies:

- `63.6`, `70.0`, `68.0`

Saved from:

- `/home/qiaosir/projects/compute_vit/logs/_gpt/crosssim_standard.log`
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/crosssim_standard_noise.json`

## Interpretation

1. The clean baseline remains reasonably aligned: CrossSim is lower than the in-framework evaluation, but not catastrophically so.
2. The gap grows only slightly at the `1%/1%` setting.
3. The gap becomes large at the canonical `5%/5%` mapping, where CrossSim underestimates accuracy by `14.43 pp` and shows much larger run-to-run spread.
4. This supports the current working conclusion already noted in the JSON files: the generic CrossSim `programming_error/read_noise` parameterization is materially harsher than the framework's fixed-D2D + per-forward-C2C implementation under the present mapping.

## Runtime note

CrossSim standard-noise runtime is much heavier than the framework-side evaluation:

- our framework total: `3.34 s` for 3 runs
- CrossSim total: `16083.42 s` for 3 runs

The standard-noise phase is therefore complete and no background CrossSim run remains active.
