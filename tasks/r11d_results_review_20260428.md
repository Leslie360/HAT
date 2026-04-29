# R11D Fair-Comparison Results — Critic Review Required

**task_id:** r11d_results_review_20260428
**priority:** P0
**type:** RESULTS_REVIEW
**deadline:** 2h

---

## 1. Context

R11D fair-comparison experiment suite completed overnight. Four runs now have full train + fresh eval + drift eval results:

| Experiment | Precision | Device Model | lr | Train Best | Fresh Eval (10 inst) | Drift (0h→1h→24h) |
|:-----------|:----------|:-------------|:---|:-----------|:---------------------|:-------------------|
| R11D-5a | 8-bit | PCM preset | 1e-3 | **76.96%** | **76.74±0.09%** | 76.70→76.72→76.73% |
| R11D-6b | 8-bit | Pure baseline (mod=1e-4) | 1e-3 | **88.64%** | **88.39±0.17%** | 88.35→12.21→10.0% ⚠️ |
| R11D-7 | 4-bit | PCM preset | 1e-3 | **76.54%** | **76.61±0.07%** | 76.61→75.01→73.42% |
| R11D-8 | 8-bit | HAT-inspired PCM | 1e-3 | **76.12%** | **76.11±0.10%** | 76.13→76.25→76.16% |

---

## 2. Key Findings Requiring Review

### Finding A: HAT-inspired PCM does NOT outperform standard PCM

R11D-8 (HAT-inspired) is **0.84pp WORSE** than R11D-5a (standard PCM) on training accuracy, and **0.63pp WORSE** on fresh eval.

**Possible interpretations:**
1. Per-epoch D2D resampling is fundamentally incompatible with PCM's nonlinear update physics
2. `std_dev=5.0` in weight domain is too large for PCM (v2 fix may still be miscalibrated)
3. aihwkit's AnalogSGD already provides implicit noise averaging that makes explicit resampling redundant
4. Implementation bug in `r11d_hat_pcm.py` v2 (per-layer scalar D2D may not match canonical HAT's behavior)

### Finding B: 4-bit PCM ≈ 8-bit PCM

R11D-7 (4-bit PCM) achieves 76.54% train / 76.61% fresh vs R11D-5a (8-bit PCM) 76.96% / 76.74%. Difference is <0.5pp.

**Implication:** PCM's bottleneck is the device model itself, not bit-width. This is strong evidence that R11D-1's 14.64% was a hyperparameter failure (lr=5e-4), not a 4-bit precision collapse.

### Finding C: Drift eval anomaly on R11D-6b (non-PCM)

R11D-6b (pure baseline, InferenceRPUConfig, NOT PCM) shows catastrophic drift: 88.35% → 12.21% → 10.0%.

**Likely cause:** `eval_aihwkit_drift.py` applies `drift_analog_weights()` which may have no physical meaning on non-PCM InferenceRPUConfig, or aihwkit handles drift differently for non-PCM presets.

---

## 3. Review Questions for Critic

**Q1 — Narrative Pivot:** Given R11D-8 < R11D-5a, should Paper-2 abandon the "HAT improves PCM" narrative and pivot to "4-bit PCM is viable" as the main contribution?

**Q2 — R11D-8 Tuning:** Should we retry R11D-8 with:
- Lower `std_dev` (e.g., 2.0 or 1.0 instead of 5.0)?
- Different `hat-mode` (additive instead of scaled)?
- Different `hat-start-epoch` (e.g., 5 or 10 instead of 1)?

**Q3 — Drift Eval Fix:** Is the R11D-6b drift result scientifically meaningful? Should non-PCM models be excluded from drift evaluation, or does the eval script need a PCM-preset check?

**Q4 — Missing Comparison:** Should we add:
- R11D-9: 4-bit pure baseline (to isolate whether 4-bit itself is the problem or PCM)
- R11D-10: Ensemble HAT canonical (custom AnalogLinear) at 8-bit for true apples-to-apples?

**Q5 — Manuscript Integration:** How do these results change the PCM section of Paper-2? Options:
- (a) Frame as "PCM hyperparameter sensitivity" (R11D-5a vs R11D-4 vs R11D-1)
- (b) Frame as "4-bit PCM viability" (R11D-7 vs R11D-1)
- (c) Frame as "HAT-inspired PCM as regularizer" (R11D-8 ≈ R11D-5a, not worse despite extra noise)
- (d) Drop HAT-inspired PCM entirely, focus on PCM baseline characterization

---

## 4. Deliverable

Write review to: `outputs/r11d_results_review_20260428.md`

Include:
- Verdict on each Q1-Q5
- Recommended next experiments (if any)
- Revised Paper-2 narrative outline

---

## 5. Files for Verification

- Training logs: `paper2_aihwkit_baseline/logs/r11d_{5a,6b,7,8}_*.log`
- Checkpoints: `paper2_aihwkit_baseline/checkpoints/r11d_{5a,6b,7,8}/best.pt`
- Fresh eval JSONs: `paper2_aihwkit_baseline/checkpoints/r11d_{5a,6b,7,8}/fresh_eval.json`
- Drift eval JSONs: `paper2_aihwkit_baseline/checkpoints/r11d_{5a,6b,7,8}/drift_eval.json`
- Training history JSONs: `paper2_aihwkit_baseline/checkpoints/r11d_{5a,6b,7,8}/training_history.json`
- HAT script: `paper2_aihwkit_baseline/r11d_hat_pcm.py`
