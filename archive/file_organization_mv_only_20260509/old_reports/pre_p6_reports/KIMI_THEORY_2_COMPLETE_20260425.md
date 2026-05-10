# KIMI THEORY 2 — Complete Report
**Date:** 2026-04-25
**Task:** DISPATCH_KIMI_THEORY_2_DEEPENING_20260425.md (Phase 1 of Round-7 Proactive Sprint)
**Assignee:** Kimi
**Authority:** CLAUDE_PROACTIVE_SPRINT_PLAN_20260425.md Phase 1
**Status:** ✅ COMPLETE

---

## Deliverables

| File | Status | Lines / Size |
|:-----|:-------|:-------------|
| `paper/latex_gpt/supplementary/S_theory_ensemble_hat.tex` | ✅ Extended | 232 lines (was 86) |
| `paper/latex_gpt/refs_gpt.bib` | ✅ 8 new entries | 8 additions (6 requested + 2 supplementary) |
| `paper/latex_gpt/sections/06_discussion_theory_paragraph.tex.kimi_draft` | ✅ Drafted | 843 bytes |
| `report_md/_gpt/KIMI_PRE_SUBMISSION_CHECKLIST_20260425.md` | ✅ Refreshed | R6-5 housekeeping |

---

## Content Summary

### §S.7 Higher-order corrections (~600 words)
- Generalized Taylor expansion to arbitrary order in $M$
- Third-order vanishes by Gaussian symmetry
- Fourth-order computed via Wick contractions, scales as $\sigma_{\text{D2D}}^4$
- Identified breakdown regime: large $\sigma$ or near-saturation weights
- Cites \citet{roberts2022principles}

### §S.8 PAC-Bayes generalization bound (~1200 words)
- Posterior $Q$ defined as diagonal Gaussian at trained weights
- Prior $P$ as wide Gaussian at initialization
- McAllester bound derived with explicit KL computation
- KL approximated; dominant term = squared bias + complexity penalty
- Honesty constraint: bound is directional, not numerically tight
- Cites \citet{mcallester1999pac,mcallester1999some,dziugaite2017computing,perez2021tighter}

### §S.9 Flat-minima connection / SAM analogy (~900 words)
- D2D-direction sharpness $\mathcal{S}_{\text{D2D}}$ defined
- Second-order expansion shows equivalence to implicit regularizer
- Structural comparison to SAM \citep{foret2021sharpness}: perturbation distribution, averaging, direction, hyperparameter
- Historical antecedent: \citet{hochreiter1997flat}
- Cites \citet{keskar2017large,andriushchenko2022understanding}

### §S.10 Limitations (~300 words)
- Heavy-tailed D2D
- Spatially correlated D2D
- Per-layer non-uniform $\sigma$
- Coupled C2C noise
- PAC-Bayes vacuousness

---

## Validation Checklist

| # | Check | Result |
|--:|:------|:-------|
| 1 | 8 bib entries added without typos | ✅ All present in `refs_gpt.bib` |
| 2 | Equation environments balanced | ✅ 23 `\begin{equation}` = 23 `\end{equation}` |
| 3 | Zero unescaped `%` | ✅ None found |
| 4 | No empirical numbers (`\d+\.\d+%`) | ✅ None in theory text |
| 5 | No bug-retrospective phrasing | ✅ None found |
| 6 | §S.7 cites Roberts & Yaida 2022 | ✅ |
| 7 | §S.8 cites Dziugaite & Roy 2017 + Pérez-Ortiz 2021 | ✅ |
| 8 | §S.9 cites Hochreiter 1997 + Keskar 2017 + Foret 2021 + Andriushchenko 2022 | ✅ |
| 9 | §S.10 honest limitations, no overclaim | ✅ |
| 10 | Discussion paragraph drafted | ✅ `06_discussion_theory_paragraph.tex.kimi_draft` |

---

## R6 Housekeeping (completed en passant)

| Task | Status | Notes |
|:-----|:-------|:------|
| R6-1: README Key Results table | ✅ Already clean | No 30.53% found; ~81% Stage-2 present |
| R6-5: Pre-submission checklist refresh | ✅ Refreshed | New checklist at `KIMI_PRE_SUBMISSION_CHECKLIST_20260425.md` |

---

## Notes for Round-5 Integration

1. **Bib entries** need to be merged into `main.bbl` at compile time (run `bibtex main` after integration).
2. **Discussion paragraph** is a `.kimi_draft` sidecar; integrate into `06_discussion.tex` §6.1 during Round-5.
3. **Supplementary theory note** extends existing `S_theory_ensemble_hat.tex`; no new file needed.
4. **Cross-reference check**: `\S\ref{supp:theory-ensemble-hat}` is used in S.7-S.10 to refer back to the main proposition; verify this label resolves after integration.

---

## Next Steps (per sprint plan)

1. **Phase 2**: Codex empirical deepening (Hessian / loss landscape / CKA) — independent track, no blocker from Phase 1.
2. **Phase 3**: Kimi writing polish — awaits Phase 1+2 completion.
3. **Phase 4**: Kimi defense tooling — parallel with late Phase 3.

Phase 1 is now **landed and ready for integration**.
