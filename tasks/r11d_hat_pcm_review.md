# Task: Review R11D-HAT-PCM Hybrid Script

**Goal:** Identify bugs, edge cases, and methodological flaws in `paper2_aihwkit_baseline/r11d_hat_pcm.py`.

**Background:**
This script ports Ensemble HAT's per-epoch D2D resampling into aihwkit's PCM framework. It disables per-batch ADD_NORMAL modifier and manually injects D2D noise on tile weights every epoch, while keeping AnalogSGD + PCMPresetUnitCell for real PCM pulse-update physics.

**Files to Review:**
- `paper2_aihwkit_baseline/r11d_hat_pcm.py` (main target)
- `paper2_aihwkit_baseline/r11d4_train_pcm.py` (baseline for diff)
- `analog_layers_ensemble.py` (original HAT reference)

**Key Concerns:**
1. `w_ideal = w_current - old_noise` assumes PCM updates are additive. Is this approximation sound?
2. `set_weights()` on AnalogLinear after AnalogSGD step() — any conflict with post_update_step()?
3. Noise scaling: `std_dev * mean(|weight|)` vs original HAT's `sigma_d2d * G_range`.
4. Element-wise noise per weight vs per-crossbar D2D in original HAT.
5. state_dict() checkpoint safety after set_weights().

**Deliverable:**
Code review report with specific bugs found and recommended fixes.
