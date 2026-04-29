# Task: Fix R11D-HAT-PCM Noise Model (Critical)

**Goal:** Fix P0-B (noise magnitude ~180x too small) and P1-A (element-wise noise ≠ per-crossbar D2D) in `r11d_hat_pcm.py`.

**Context:**
Code review found the current D2D noise model is fundamentally incorrect:
- Current: `noise = randn_like(w) * std_dev * mean(|w|)` — element-wise, ~0.0005 magnitude
- Canonical HAT: `noise = randn(1) * sigma_d2d * G_range` — per-layer scalar, ~0.9 magnitude
- Current is ~180x too small and structurally wrong (C2C vs D2D).

**Files to Modify:**
- `paper2_aihwkit_baseline/r11d_hat_pcm.py`

**Required Changes:**

1. **P0-B: Fix noise magnitude**
   Change `resample_all_d2d_noise()` to use per-layer scalar offset:
   ```python
   # OLD (element-wise, too small):
   noise_new = torch.randn_like(w_ideal) * std_dev * scale
   
   # NEW (per-layer scalar, correct magnitude):
   d2d_offset = torch.randn(1, device=w_ideal.device) * std_dev * scale
   noise_new = d2d_offset.expand_as(w_ideal)
   ```
   Also: change default `--hat-std-dev` from `0.10` to `5.0` (empirically compensates for weight-domain vs conductance-domain scaling).

2. **P1-A: Per-layer scalar D2D**
   Same change as above — per-layer scalar offset approximates physical crossbar mismatch where all cells share the same fabrication offset.

3. **P0-A: Rename method**
   Change all references from "HAT-PCM" to "HAT-inspired PCM" or "per-epoch noise resampling".
   - Script name: keep `r11d_hat_pcm.py` (internal code name ok)
   - `run_id`: change to `r11d_hat_inspired_pcm`
   - `method` field: "HAT-inspired per-epoch noise resampling"
   - `method_note`: document that ideal-weight estimate is approximate due to PCM non-linearity

4. **P1-B: Add `model.eval()` before `set_weights()`**
   In `resample_all_d2d_noise()`, add `model.eval()` at the start of the function.

5. **P2-C: Remove unused `device` parameter**
   Remove `device="cpu"` from `init_hat_noise_buffers()` signature.

6. **P2-D: Remove duplicate `make_rpu_config()`**
   Pass pre-resolved `rpu_config` to `build_model()` instead of resolving twice.

**Verification:**
Run 3-epoch smoke test:
```bash
bash paper2_aihwkit_baseline/run_r11d_hat_pcm_v2.sh
```
Expected: test accuracy should be materially different from R11D-4 baseline (not just ~29%). If noise is now at correct magnitude, accuracy may drop significantly (exploratory — document result regardless).

**Deadline:** Immediate (before R11D-5a/5b complete)
