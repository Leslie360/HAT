# Claude Task: Code Review — R11D-HAT-PCM Hybrid Script

**Date:** 2026-04-27
**Agent:** Codex (coding) + Gemini (critic) + Kimi (doc)
**Source:** `paper2_aihwkit_baseline/r11d_hat_pcm.py` (written by Claude)
**Context:** Ensemble HAT + PCM device model hybrid for Nature Electronics paper

---

## 1. What the code does

Implements per-epoch D2D mismatch resampling on aihwkit `AnalogLinear` tile weights,
while keeping `AnalogSGD` + `PCMPresetUnitCell` for real PCM pulse-update physics.
Key idea: disable aihwkit's per-batch `ADD_NORMAL` modifier; inject D2D noise
manually at epoch boundary; let PCM `post_update_step()` train on the noisy weights.

Two modes:
- `scaled` (default): estimate ideal weight `w_ideal = w_current - old_noise`,
  then add noise scaled by `mean(|w_ideal|)`.
- `additive`: directly add scaled noise to current weights.

---

## 2. Issues found by self-audit (Claude)

### P0 — Approximation in `w_ideal = w_current - old_noise`

**Location:** `resample_all_d2d_noise()`, line ~72
**Problem:** Assumes PCM `post_update_step()` updates weights additively.
PCM is non-linear (sigmoid-like pulse-update). After many epochs,
`w_current - old_noise` may deviate from true ideal weight.
**Impact:** Medium. Noise estimate drifts; D2D resampling loses exact orthogonality.
**Mitigation:** Smoke test (3 epochs) shows convergence ~29% (similar to R11D-4),
suggesting approximation is acceptable for early epochs. Long-term drift unknown.
**Ask reviewers:** Is there a way to extract "programmed weight" vs "noise offset"
from aihwkit `InferenceTile` API? If not, document as known limitation.

### P1 — `state_dict()` / checkpoint safety

**Location:** `torch.save()` calls with `model.state_dict()`
**Problem:** `AnalogLinear.state_dict()` returns `analog_module.shared_weights`.
`set_weights()` updates tile internal state, which IS reflected in `state_dict()`
(verified by test script). BUT: `AnalogSGD.step()` + `post_update_step()` may
update tile state in a way not fully captured by `get_weights()`.
**Impact:** Low. Verified `shared_weights` matches `get_weights()` after `set_weights()`.
**Ask reviewers:** Should we add `get_weights()` snapshot to checkpoint explicitly
for extra safety?

### P1 — Noise magnitude scaling strategy

**Location:** `resample_all_d2d_noise()`, `scale = w_ideal.abs().mean().item()`
**Problem:** Original HAT uses `sigma_d2d * G_range` where `G_range` is full
conductance span. `mean(|weight|)` is an ad-hoc proxy. Could be too small for
some layers (e.g. final classifier head has smaller weights) or too large for others.
**Impact:** Medium. May under/over-noise certain layers.
**Ask reviewers:** Should scaling be per-layer std instead of mean? Should we use
`w.abs().max()` or `w.std()`? Or map weights to conductance domain first?

### P2 — `get_weights()` / `set_weights()` CPU-GPU roundtrip per epoch

**Location:** `resample_all_d2d_noise()`
**Problem:** 41 layers x 2 calls/epoch x 100 epochs = 8,200 CPU-GPU transfers.
Each transfer moves ~0.5MB (TinyViT layer). Total ~4GB of PCIe traffic.
**Impact:** Low. Epoch time ~165s (same as R11D-4), so overhead is negligible.
**Ask reviewers:** Any way to operate directly on GPU tiles without roundtrip?

### P2 — Unused `device` parameter in `init_hat_noise_buffers`

**Location:** `init_hat_noise_buffers(model, std_dev, device="cpu")`
**Problem:** Parameter ignored; buffers always on CPU.
**Impact:** Cosmetic.
**Fix:** Remove parameter or use it.

### P2 — Duplicate `make_rpu_config()` call

**Location:** `main()` calls `make_rpu_config()` early for validation;
`build_model()` calls it again.
**Impact:** Cosmetic. Prints "Resolved preset" twice in log.
**Fix:** Pass pre-resolved `rpu_config` to `build_model()`.

---

## 3. Questions for pipeline review

1. **Codex:** Does `AnalogLinear.set_weights()` correctly propagate through
   `analog_module.set_weights()` for all aihwkit tile types (InferenceTile,
   AnalogTile, etc.)? Any edge case with `bias=None`?

2. **Codex:** `AnalogSGD.step()` calls `tile.post_update_step()` which applies
   PCM pulse-update. If we call `set_weights()` immediately after `step()`,
   does `post_update_step()` get "undone"? In our code we call `set_weights()`
   at the START of the next epoch, so there is a full `evaluate()` call in between.
   Is this sufficient? Should we call `model.eval()` before `set_weights()`?

3. **Gemini:** Is the `scaled` noise formula `randn * std_dev * mean(|w|)`
   physically sound for D2D mismatch? In HAT original, D2D is per-crossbar
   (same offset for all cells in an array). Our implementation is per-weight-element.
   Is this closer to C2C than D2D? Should we add a per-layer scalar offset
   (single random value per layer) instead of element-wise noise?

4. **Gemini:** HAT's canonical result uses `sigma_d2d=0.10`. Our `std_dev=0.10`
   with `mean(|w|)` scaling gives effective ~0.005 std per weight element.
   Is this equivalent to HAT's 0.10? Or should `std_dev` be set to ~1.0 to
   match HAT's noise level?

5. **Kimi:** Document the "approximate HAT" caveat in manuscript terms.
   If HAT PCM results are > 61%, how do we frame this? "HAT-inspired per-epoch
   resampling improves PCM training" or "true Ensemble HAT + PCM"?

---

## 4. Action items

- [ ] Codex: Review `r11d_hat_pcm.py` for logic correctness, edge cases, aihwkit API misuse
- [ ] Codex: Run 10-epoch quick test with `additive` mode; compare to `scaled`
- [ ] Gemini: Critique physical soundness of noise model and scaling strategy
- [ ] Gemini: Suggest `std_dev` tuning (0.10 vs 0.50 vs 1.0)
- [ ] Kimi: Draft manuscript paragraph describing HAT PCM method and caveats
- [ ] Claude: After review, apply fixes and queue full 100-epoch run

---

## 5. Files to review

| File | Purpose |
|------|---------|
| `paper2_aihwkit_baseline/r11d_hat_pcm.py` | Main training script (NEW) |
| `paper2_aihwkit_baseline/r11d4_train_pcm.py` | Baseline PCM script (for diff) |
| `paper2_aihwkit_baseline/run_r11d_hat_pcm.sh` | Launch script |
| `analog_layers_ensemble.py` | Original HAT implementation (reference) |

---

**Priority:** HIGH (blocks full HAT PCM experiment launch)
**Deadline:** Before R11D-5a/5b complete (~2h)
