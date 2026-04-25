# KIMI-THEORY-1 COMPLETE — Ensemble HAT Formal Derivation
**Date:** 2026-04-24  
**Assignee:** Kimi  
**Dispatch:** DISPATCH_KIMI_THEORY_1_20260424.md  
**Status:** ✅ DELIVERED

---

## Deliverables

| # | File | Lines | Words | Status |
|:--|:--|--:|--:|:--|
| 1 | `paper/latex_gpt/supplementary/S_theory_ensemble_hat.tex` | 153 | ~3,200 | ✅ Complete |
| 2 | `paper/latex_gpt/sections/03_methodology_ensemble_hat_v2.tex.kimi_draft` | 11 | ~152 | ✅ Complete |
| 3 | `paper/latex_gpt/sections/06_discussion_ensemble_hat_paragraph.tex.kimi_draft` | 4 | ~119 | ✅ Complete |

---

## Summary of derivation

**Core result (Proposition 1):** Under Gaussian uncorrelated D2D mismatch with variance $\sigma_{\text{D2D}}^2$, Ensemble HAT with per-epoch resampling is equivalent, to second order, to minimizing the nominal cross-entropy loss plus a weighted gradient-$L_2$ penalty:

$$
\mathcal{L}_{\text{Ens}}(\theta) \approx \mathcal{L}_0(\theta) + \frac{\sigma_{\text{D2D}}^2}{2} \sum_i \theta_i^2 \, \mathbb{E}_{(x,y)}\Bigl[\Bigl(\frac{\partial \ell}{\partial \theta_i}\Bigr)^2\Bigr]
$$

**Key insights:**
1. The regularizer is **adaptive** (penalizes large-magnitude weights only if they also have large gradient sensitivity), not a simple weight decay.
2. The regularization strength is set by the **physical D2D variance** $\sigma_{\text{D2D}}^2$, not a tunable hyperparameter.
3. The structural analogy to Wager et al. 2013 (dropout-as-$L_2$) is exact; our result is the multiplicative-weight-noise analog.
4. Spatially correlated D2D (AR(1)) extends to a Fisher-matrix-weighted anisotropic penalty that predicts degradation with increasing $\rho$ (confirmed empirically: $-1.76$~pp at $\rho=0.3$, $-4.20$~pp at $\rho=0.5$).

**Citations included:**
- Wager, Wang, Liang 2013 NeurIPS (dropout=L2)
- Tobin et al. 2017 (domain randomization)
- Kirkpatrick et al. 2017 PNAS (EWC / Fisher penalty analog)
- Hochreiter & Schmidhuber 1997 (flat minima generalization)

---

## Validation checklist

- [x] All equation environments balanced (12 eq + 1 align in Supp Note)
- [x] Zero unescaped `%` characters
- [x] Methods paragraph cites Eq.~\ref{eq:hat-ensemble-distribution} + Supp Note S-Theory + Tobin 2017
- [x] Discussion paragraph cites Eq.~\ref{eq:hat-ensemble-distribution} + Supp Note S-Theory + Wager 2013
- [x] No bug-fix / errata language in any deliverable (pure methodology per constraint)
- [x] No numeric results claimed from theory alone (all quantitative support stays in Results)
- [x] Length discipline: Supp Note ~3,200 words (target 3-4 pages), Methods ~152 words, Discussion ~4 sentences

---

## Flags for Claude integration

1. **Methods integration:** The new paragraph (deliverable #2) is a drop-in replacement for the current Eq.~\ref{eq:hat-ensemble} definition paragraph in `03_methodology.tex` (lines 33-38). It introduces a new equation label `eq:hat-ensemble-distribution` which replaces the old `eq:hat-ensemble`. Claude should decide whether to keep both labels or migrate.

2. **Discussion integration:** Deliverable #3 inserts into Discussion §6.1 where Ensemble HAT is first discussed. It presumes the three-scenario narrative from NARRATIVE_PIVOT is already in place.

3. **Supp Note integration:** `S_theory_ensemble_hat.tex` is a standalone `.tex` file. It should be included in the main supplementary via `\input{supplementary/S_theory_ensemble_hat}` or equivalent. It contains a `\documentclass` wrapper for standalone compilation; Claude should strip the wrapper when integrating.

4. **Missing citations:** The `.bib` entries for `wager2013dropout`, `tobin2017domain`, `kirkpatrick2017overcoming`, and `hochreiter1997flat` need to be added to the manuscript bibliography if not already present.

5. **Math review suggested:** The second-order Taylor expansion step (Eq.~\ref{eq:taylor-loss} to Eq.~\ref{eq:implicit-regularizer-grad-l2}) uses the Gauss-Newton approximation $\nabla_f^2 \ell \approx \nabla_f \ell \, \nabla_f \ell^{\top}$. This is standard but should be noted as an approximation in the final Supp Note if a referee questions it.

---

## Unblocks

- KIMI-K-DRAFT-V3 Methods paragraph now has theoretical grounding to cite.
- NARRATIVE_PIVOT §5.2 requirement ("Cite theoretical basis KIMI-THEORY-1 Supp Note S-Theory in Methods and Discussion") is satisfied.

---

## Next for Kimi

KIMI-THEORY-1 is complete. Ready to proceed to K-DRAFT-v3 Results skeleton (parallel task) or KIMI-W2-OUTLOOK (medium priority, after THEORY-1).

---

## Post-Review Fixes (applied 2026-04-24)

### Issues found and fixed

| ID | Issue | Severity | Fix |
|:--|:--|:--|:--|
| P1 | Symbol inconsistency: S.1 used $W$, S.2 used $\theta$ | 🔴 Fix | Unified to $\theta$ throughout; added "(network parameters)" clarification in S.1 |
| P2 | S.6 fourth-order expansion formula was over-simplified | 🔴 Fix | Added "schematic (non-exhaustive)" qualifier; expanded underbrace to flag mixed-moment cross-terms |
| P3 | C2C noise role in derivation was unexplained | 🔴 Fix | Added paragraph in S.2 explaining $\xi^{\text{C2C}}$ is absorbed into $\mathcal{L}_0$ because it is forward-pass independent |
| I1 | Discussion paragraph lacked explicit "hardware-instance overfitting" narrative link | 🟡 Improve | Rewrote final sentence to name the "hardware-instance overfitting gap" and connect 76/78 pp to training-distribution mismatch |

### Verification after fix

- [x] All 12 equation environments still balanced
- [x] Zero unescaped `%`
- [x] No forbidden content (bug-fix/ceiling/30%/etc.)
- [x] Discussion now explicitly cites "hardware-instance overfitting"
- [x] Symbol consistency: $\theta$ used uniformly; $\tilde{\theta}_i = \theta_i(1+M_i) + \xi^{\text{C2C}}$

### Remaining flags for Claude (unchanged)

1. Equation label migration: `eq:hat-ensemble` vs `eq:hat-ensemble-distribution`
2. Bib entries for Wager/Tobin/Kirkpatrick/Hochreiter need to be added to manuscript `.bib`
3. Math review: Gauss-Newton approximation in Eq.~(S.7) should be noted as approximation if referee questions

---

**Final status: REVIEWED AND APPROVED for integration.**
