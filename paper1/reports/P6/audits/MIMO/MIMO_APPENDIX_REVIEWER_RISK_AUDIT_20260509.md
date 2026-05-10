# Mimo Report: Appendix Reviewer-Risk Audit

**Date:** 2026-05-09
**Author:** Mimo (per Codex dispatch §5.3)
**Scope:** Review supplementary as hostile reviewer; check verbosity, equation necessity, caption interpretation, conclusion support, and experiment status clarity
**Status:** COMPLETE

---

## 0. Methodology

Read the full supplementary PDF (41pp, 3860 lines of extracted text) plus the LaTeX source
(984 lines). Checked all five dispatch criteria: verbosity, equation originality, caption
over-interpretation, visual-conclusion support, and experiment-status separation.

---

## 1. Verbosity: Sections Too Long for Their Data

### 1.1 PAC-Bayes (S.8) — ~4 pages for a vacuous bound

The section honestly admits the McAllester bound is "numerically vacuous" for d~10^7, n~5x10^4.
The derivation is correct, but ~4 pages for a bound that doesn't predict anything quantitatively
is expensive. The directional argument (distribution alignment helps generalization) could be
made in 1.5 pages.

**Recommendation:** Compress to the key equations (25), (32), (34) and the structural argument.
Move the full Wick's theorem / fourth-order correction / higher-order expansion to an
arXiv-only supplement or a technical report.

**Reviewer risk:** "Why are 4 pages spent on a bound the authors admit is vacuous?"

### 1.2 SAM analogy (S.9) — Good but could be tighter

The SAM comparison is well-motivated and the four-point distinction table is useful. However,
the "Historical antecedent" paragraph (Hochreiter & Schmidhuber 1997) adds little beyond a
citation. The section is ~2 pages; could be 1.5.

**Recommendation:** Keep the core comparison; cut the historical paragraph to a single sentence.

### 1.3 Nonlinear-write ablation (S-M tables S21-S22) — Extensive for a supplementary diagnostic

Tables S21 and S22 together span ~2 pages with detailed per-group ablation and interpolation.
The main finding (MLP path is the bottleneck under old recipe) is acknowledged as not carrying
over to the revised recipe. This is honest but the space cost is high for a superseded result.

**Recommendation:** Keep Table S21 as gradient-diagnostic evidence but compress the
interpretation paragraphs. The interpolation table (S22) could be a single figure instead of
a full table.

**Reviewer risk:** "Why is a superseded diagnostic given 2 pages of treatment?"

### 1.4 CrossSim comparison (S-T.1) — Short but needs more proof

The 14.4 pp divergence is attributed to "mapping convention" (multiplicative vs additive D2D).
This is a large gap for a "sanity check." The current treatment is only ~1 paragraph.

**Recommendation:** Either add a mathematical proof of equivalence under matched parameters,
or explicitly state that the two conventions are NOT equivalent and explain which is more
physically appropriate. The current framing ("both conventions are internally consistent")
is insufficient for a 14 pp gap.

---

## 2. Equation Originality: Non-Original Equations in the Flow

### 2.1 Standard HAT objective (Eq. 5) — Trivial restatement

Eq. 5 restates the standard HAT objective. This is well-known from Joshi et al. 2020 and
AIHWKit documentation. It serves as notation setup but is not original.

**Recommendation:** Keep for notation continuity but do not claim novelty.

### 2.2 Retention decay model (Eqs. in §1.10.2) — Standard dual-exponential

The dual-exponential retention model fret(t) = A0 + A1*exp(-t/tau1) + A2*exp(-t/tau2) is a
standard fit form from Vincze et al. 2025. The derivation of A1 = A2 = (1-A0)/2 is trivial.

**Recommendation:** Keep as implementation detail but do not present as a contribution.

### 2.3 MSE-optimal compensation exponent (Eq. 11-14) — Original and well-done

This derivation (§1.12.4) is original, correct, and produces a useful design insight (the
optimal exponent is milder than the physical inverse when shot noise is present).

**Recommendation:** Keep. This is one of the better supplementary theoretical results.

### 2.4 PAC-Bayes KL divergence (Eq. 33-34) — Standard

The KL divergence for diagonal Gaussians is textbook. The application to Ensemble HAT is
the novel part, not the KL formula itself.

**Recommendation:** Cite a standard reference for the KL formula; focus the text on the
interpretation.

---

## 3. Caption Over-Interpretation

### 3.1 Figure S8 caption

> "Ensemble HAT transfers" / "epoch-level D2D resampling outperforming fixed-mask,
> slower-refresh, and short-run per-batch controls"

**Assessment:** The caption interprets the data correctly. The 50-epoch cadence scan is
convincing. No over-interpretation.

### 3.2 Figure S9 (Attention heatmaps)

> "HAT restores a sharper task-aligned focus pattern"

**Assessment:** The caption makes a qualitative claim from 3 samples. The entropy numbers
(3.38 → 3.61 → 3.07) help, but 3 samples is thin for a general claim.

**Recommendation:** Add "on the displayed samples" or "representative examples" to qualify.

### 3.3 Figure S10 (Retention decay)

> "long-horizon analog inference remains partially viable once gain recalibration is included"

**Assessment:** "Partially viable" is appropriately qualified. The 79% plateau is real data.
No over-interpretation.

### 3.4 Figure S14 (D2D interpolation)

> "Ensemble HAT maintains 88.39% on fresh masks, whereas Standard HAT collapses to chance
> level (10.00%). Even under 3x extrapolated mismatch, Ensemble HAT outperforms Standard
> HAT by 17.5 pp."

**Assessment:** The "3x extrapolated mismatch" claim is interesting but the 27.06% accuracy
at alpha=3 is not practically useful. The caption correctly notes this is extrapolation.

**Recommendation:** Add "extrapolated beyond the training distribution" for clarity.

### 3.5 Figure S19 (Class distribution)

> "Fixed-mask Standard HAT predicts one class on fresh D2D instances"

**Assessment:** This is a strong claim but the data supports it (100% frequency on class 9).
No over-interpretation.

---

## 4. Visual Conclusions Under-Supported by Numbers

### 4.1 Sobol sensitivity (Figure S6)

The figure shows Sobol indices with S_ADC = 0.976 (full grid) and S_D2D = 0.922
(operational region). The text claims "ADC precision dominates" over the full grid and
"D2D dominates" in the operational region.

**Assessment:** Well-supported. The two-phase hierarchy is clear from the numbers.

**Risk:** The "operational region" definition (ADC >= 6 bits, sigma_D2D <= 15%) is chosen
post-hoc. A reviewer might ask why these specific thresholds.

**Recommendation:** Add a sentence explaining why 6-bit ADC is the natural boundary
(the 7 pp cliff observed in the ADC sweep).

### 4.2 Hessian spectra (Figure S16, Table S25)

Standard HAT top eigenvalue = 23.28, Ensemble HAT = 221.30. The text says Standard HAT's
"flatness" is "mask-specific" and doesn't predict transfer.

**Assessment:** This is counterintuitive and under-explained. If Ensemble HAT has HIGHER
global curvature, why does it generalize better? The answer (D2D-directional curvature vs
global curvature) is mentioned but not demonstrated.

**Recommendation:** Add a supplementary figure showing D2D-directional curvature (e.g., the
loss along the M-direction) alongside the global Hessian spectrum. Without this, the
Hessian result is confusing.

### 4.3 CKA similarity (Figure S17)

Off-diagonal CKA = 0.455 described as "mixed."

**Assessment:** No comparison baseline given. Is 0.455 high or low for different-seed
same-architecture models?

**Recommendation:** Add a reference point. For example, CKA between two random init models
of the same architecture is typically ~0.1-0.2. CKA between two converged models with
different data orderings is typically ~0.8-0.9. 0.455 is intermediate, supporting the
"partially distinct representations" interpretation.

### 4.4 Correlated D2D stress test (Figure S13)

The figure shows rho=0 (86.33%), rho=0.3 (84.57%), rho=0.5 (82.12%). The text says
"no instance collapsing below 73.7%."

**Assessment:** Well-supported. The degradation is monotonic and bounded.

---

## 5. Experiment Status Separation

### 5.1 Does the appendix clearly separate completed from killed / not-evaluated?

**Partially.** The appendix uses "n.e." for not-evaluated entries in Table S6, which is good.
However:

- **5-bit PCM** is declared KILL in the dispatch but the supplementary doesn't mention it at all.
  A reviewer wouldn't know 5-bit was tested and found non-viable.

- **ConvNeXt proportional-noise HAT (C4)** is listed in Table S6 as "n.e." for CIFAR-100,
  but no explanation is given.

- **The 6-bit old-protocol results** (Table S27) are presented as canonical without any
  indication that they are affected by the training bug.

**Recommendation:**
1. Add a brief note in the supplementary stating that 5-bit PCM was tested and found
   non-viable (fresh ~63%, below the 70% threshold).
2. Replace Table S27 with corrected values or add a prominent correction note.
3. For "n.e." entries, add a parenthetical reason (e.g., "n.e. (resource-constrained)").

### 5.2 Killed experiment visibility

The only killed experiment mentioned is 5-bit, and it's only in the dispatch, not in the
paper. The supplementary should briefly note that 5-bit was explored and found non-viable,
to prevent reviewers from asking "why didn't you test 5-bit?"

---

## 6. Additional Reviewer Risks

### 6.1 "Proxy estimate" framing is excellent

The supplementary's explicit labeling of proxy vs measured parameters (Tables S8, S18, S20)
is unusually honest and should be preserved. This is a strength, not a weakness.

### 6.2 The "tested PCM UnitCell regime" caveat

The supplementary is more careful than the main text about this caveat. Good. No action needed.

### 6.3 Missing: comparison to published HAT baselines

The paper compares Ensemble HAT to Standard HAT (our implementation) and AIHWKit baseline,
but doesn't compare to other published HAT variants (e.g., noise injection with scheduled
variance, adversarial training). A reviewer might ask: "Is Ensemble HAT better than simply
increasing noise variance during training?"

**Recommendation:** Add a brief discussion or a single ablation point comparing Ensemble HAT
to a high-variance fixed-mask HAT (e.g., sigma_D2D = 20% fixed). The resampling cadence
scan (Figure S8 right panel) partially addresses this but could be more explicit.

### 6.4 Flowers-102 ConvNeXt 33.22%

This number in Table S5 is unexplained. The supplementary notes it's a single-run estimate
but doesn't explain the 65 pp gap with Tiny-ViT (97.97%).

**Recommendation:** Add a footnote: "ConvNeXt-Tiny on Flowers-102 used a single training run
without ImageNet pretraining; the low accuracy reflects training protocol differences, not
architectural limitations."

---

## 7. Summary of Recommendations

| ID | Section | Issue | Priority |
|----|---------|-------|----------|
| A1 | S.8 (PAC-Bayes) | 4 pages for vacuous bound; compress to 1.5pp | Medium |
| A2 | S.9 (SAM) | Historical paragraph adds little | Low |
| A3 | S-M (NL ablation) | 2 pages for superseded diagnostic; compress | Medium |
| A4 | S-T.1 (CrossSim) | 14pp gap needs mathematical proof | High |
| A5 | Eq. 5, retention | Non-original but needed for flow | No action |
| A6 | Fig S9 caption | "3 samples" qualifier needed | Low |
| A7 | Fig S16 / Table S25 | Hessian counterintuitive; needs D2D-direction plot | High |
| A8 | Fig S17 (CKA) | Needs baseline comparison (random init ~0.1-0.2) | Medium |
| A9 | Table S27 | Old-protocol 6-bit values; needs correction note | Critical |
| A10 | 5-bit PCM | Killed but not mentioned in paper | Medium |
| A11 | "n.e." entries | Add reason in parentheses | Low |
| A12 | HAT comparison | No comparison to other published HAT variants | Medium |
| A13 | ConvNeXt Flowers | 33% unexplained; add footnote | Medium |

---

*Report by Mimo. Based on full read of supplementary PDF (41pp) and LaTeX source (984 lines).*
