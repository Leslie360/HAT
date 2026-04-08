## 2026-04-05 Codex
### Purpose
- Prepare the codebase and paper narrative for future in-house measured device data.
- Keep the current literature-anchored experiments reproducible while making the simulator ready for measured-profile substitution.

### Recommended Raw Measurement Buckets
- `multilevel_programming.csv`
  - Use to estimate `G_min`, `G_max`, `n_states`
- `cycle_repeatability.csv`
  - Repeated read/program at the same target state
  - Use to estimate `sigma_c2c`
- `device_to_device_stats.csv`
  - Multiple nominally identical devices or array cells
  - Use to estimate `sigma_d2d`
- `retention_curve.csv`
  - Use to fit `A_0`, `tau_1`, `tau_2`

### Simulator Mapping
- `G_min`, `G_max`
  - Conductance window after normalization / filtering
- `n_states`
  - Effective resolvable conductance states, not just nominal programming levels
- `sigma_c2c`
  - Read-to-read or cycle-to-cycle relative variability in the conductance domain
- `sigma_d2d`
  - Fixed mismatch across cells/devices after programming
- `A_0`, `tau_1`, `tau_2`
  - Double-exponential retention fit
- `gamma_phys`, `I_dark`, `responsivity_alpha`
  - Front-end optical response for the physical phototransistor path
- `NL_LTP`, `NL_LTD`, `pulse_count_max`
  - Plasticity / update nonlinearity descriptors
  - Important for the materials story even though the current main training path does not yet use them as a first-class update model

### Code Entry Points
- Device comparison:
  - `python run_device_comparison.py --device-profile-json device_profiles/example_measured_device_profile_gpt.json`
- Noise / ADC sweep:
  - `python run_noise_sweep.py --model-type tinyvit --experiment V4 --device-profile-json device_profiles/example_measured_device_profile_gpt.json`
- ImageNet eval-only:
  - `python eval_imagenet_analog.py --val-dir /path/to/imagenet/val --device-profile-json device_profiles/example_measured_device_profile_gpt.json`

### Paper Positioning
- Current manuscript uses literature-anchored priors for reproducible development-stage experiments.
- Final cross-disciplinary paper should explicitly present the current study as a simulation pipeline designed to be replaced or calibrated by in-house measured device statistics.
- When measured data arrives, the most important paper change is not only swapping numbers, but showing the material-to-system linkage:
  - measured conductance window -> quantization/state bottleneck
  - measured stochastic variation -> HAT/noise robustness
  - measured retention curve -> recalibration and long-time deployment behavior

### Practical Note
- For materials-facing presentation, avoid describing `sigma_c2c` and `sigma_d2d` as abstract hyperparameters only.
- Prefer wording like:
  - "fitted from repeated programming/reading statistics"
  - "estimated from cross-device conductance dispersion"
  - "calibrated from measured retention decay"
- Likewise, `NL_LTP / NL_LTD` should be presented as fitted pulse-update nonlinearity from measured conductance-vs-pulse curves, not as arbitrary simulator knobs.
