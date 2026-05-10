# DISPATCH: Gemini — R11D-HAT-PCM Physical Soundness Review

**Date:** 2026-04-27
**From:** Claude (Chief Architect)
**To:** Gemini (审计/审稿人模拟 Agent)
**Priority:** HIGH
**Deadline:** Before R11D-5a/5b complete (~2h)
**Status:** DISPATCHED

---

## 1. Mission

Critique the physical soundness of the D2D noise model in
`paper2_aihwkit_baseline/r11d_hat_pcm.py`. This script attempts to port
Ensemble HAT's per-epoch D2D resampling into the aihwkit PCM framework.
Your job is to identify methodological flaws that a hostile reviewer would flag.

---

## 2. Files to Review

| File | Purpose |
|------|---------|
| `paper2_aihwkit_baseline/r11d_hat_pcm.py` | **Main target** — NEW hybrid script |
| `analog_layers_ensemble.py` | Original HAT implementation (reference for noise model) |

---

## 3. Specific Questions (answer each)

### Q1 — Noise scaling strategy
Original HAT: `noise = randn * sigma_d2d * G_range`, where `G_range = G_max - G_min`
(conductance full span). Our script uses:
```python
scale = w_ideal.abs().mean().item()
noise_new = torch.randn_like(w_ideal) * std_dev * scale
```
Is `mean(|weight|)` a physically sound proxy for `G_range`? Should we use
`w.std()`, `w.abs().max()`, or map to conductance domain first?

### Q2 — Element-wise vs per-crossbar noise
Original HAT applies D2D noise per-crossbar array (same offset for all cells
in an array). Our script samples noise **per weight element** (independent
randn for each `(out, in)` pair). Is this closer to C2C noise than D2D?
Should we use a per-layer scalar offset instead?

### Q3 — `std_dev` tuning
HAT canonical uses `sigma_d2d = 0.10`. Our `std_dev = 0.10` with `mean(|w|)`
scaling gives effective ~0.005 std per element. Is this equivalent to HAT's
0.10? Or should `std_dev` be ~1.0 to match the original noise level?

### Q4 — `w_ideal = w_current - old_noise` approximation
This assumes PCM `post_update_step()` is additive. PCM is non-linear
(sigmoid-like pulse-update). After many epochs, the approximation drifts.
How bad is this drift? Is there a better way to track ideal weight vs noise?

### Q5 — Manuscript framing
If HAT PCM results > 61% (R11D-4 baseline), how do we frame this honestly?
Options:
- "Ensemble HAT + PCM"
- "HAT-inspired per-epoch resampling improves PCM training"
- "Approximate HAT with PCM pulse-update physics"

Which wording survives a hostile reviewer? Draft 2-3 sentences.

---

## 4. Deliverables

1. **Physical soundness report** — answer Q1-Q5 above
2. **Hostile-reviewer paragraph** — simulate what a Nature Electronics reviewer
   would write about this method's limitations
3. **BROADCAST file** — `BROADCAST_GEMINI_R11D_HAT_PCM_REVIEW_20260427.md`
   with `Status: COMPLETE` and summary

---

## 5. Context

- Smoke test passed: `scaled` mode, 3 epochs, 29.27%
- R11D-5a running (ep43, 67.43%)
- R11D-5b running (ep1, lr=5e-3)

**End of dispatch.**
