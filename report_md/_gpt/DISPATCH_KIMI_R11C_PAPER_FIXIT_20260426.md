# DISPATCH KIMI R11C — Paper Fix-It Pass (11 issues)
**Date:** 2026-04-26 16:30 CST
**Issued by:** Claude
**Assignee:** Kimi
**Authority:** CLAUDE_PROJECT_SELF_AUDIT_20260426 + CLAUDE_ROUND11_ROLE_REASSIGNMENT_PLAN
**Priority:** HIGH (paper integrity — submission-blocking)
**Time budget:** ~1-2 days

---

## 0. Mission

Close 11 outstanding paper integrity + structure issues from Claude's project self-audit. Most are surgical edits. Two are paper-structure refactors (08_appendix relocation + figure renumbering). All preserve numerical claims; this is presentation + integrity polish.

---

## 1. CRITICAL — Paper data integrity

### C1 — V6 PHANTOM
**Status: ✅ Already fixed by Claude** in supplementary.tex L132. Was `95.82 ± 0.12`, now `82.58 (single-seed)`. Real value from `tinyvit_v2v7_results_gpt.json`. Inform if you see V6 cited elsewhere with the wrong number — grep `95.82` across `paper/`.

### C2 — Broken cross-references

**3 broken refs to fix:**

**C2.1**: `Supplementary Note S-Verification` referenced in `05_results.tex:41` doesn't exist as a labeled supp note. The FP32-no-AMP confirmation text is in `supplementary.tex` §S1. Fix: change reference to `Supplementary Information S1` (or whatever §S1's actual label is).

**C2.2**: `Supplementary Fig.~S-Resampling-Cadence` referenced in `S_theory_ensemble_hat.tex:33` doesn't exist. Either:
- (a) Add the figure (out of scope for R11C; flag for Round-12)
- (b) Remove reference (your call — pick whichever preserves the theoretical argument)

**C2.3**: `tab:r10d-nl-interpolation` referenced in `05_results.tex:101` lives in `supplementary.tex:724`. Cross-doc reference resolves to `??` because main.tex doesn't `\input{supplementary.tex}`.

Two options:
- (a) Move table into main text (counts against page budget H1)
- (b) Replace with prose: "Detailed NL-interpolation results are provided in the Supplementary Information"

Pick (b) for compactness.

### C3 — C2C noise mis-classified
`02_related_work.tex:7` lists "C2C noise, D2D mismatch, nonlinear write" all as "fixed per hardware instance". 

**Wrong**: C2C noise is per-forward-pass (not per-instance). Only D2D mismatch is per-instance.

Fix: rewrite that sentence to:
> "Hardware-induced perturbations decompose into device-to-device (D2D) mismatch—spatially structured and fixed for a given fabricated instance—and cycle-to-cycle (C2C) noise—stochastic per-read with zero mean."

### C4 — V7 contradiction
Two places contradict:
- `03_methodology.tex:50`: "V7 evaluates retention drift"
- `04_experimental_setup.tex:24`: "V7 & Legacy retention-aware model, excluded from canonical claims"

Resolve. Recommended: **mark V7 as legacy**, exclude from active discussion.

Fix in `03_methodology.tex:50`: rewrite sentence to refer to V8 (which is the "corrected retention-aware follow-up" in current §5.3) and note V7 is legacy.

### C5 — Introduction MLP-path claim invalidated
`01_introduction.tex:9` says: "localization of NL=2.0 surrogate failure primarily to the MLP path"

But `supplementary.tex:719` says: under revised gradient-scaling recipe, fresh-instance transfer recovers regardless of which path is protected (claim no longer holds).

Fix: rewrite intro §9 to:
> "and by characterizing the post-hoc behavior of severe nonlinear write under a revised gradient-scaling recipe, recovering deployment accuracy to the ~80-82% band."

This avoids claiming MLP-path-specific localization.

---

## 2. HIGH — Paper structure

### H1 — Main 16 pages too long; move appendix to supplementary
Nature Electronics typical Article: 4 pages + 4 supp figures, OR 8 pages with extended figs. We're at 16 main + supp. Cut.

**Action:**
- `08_appendix.tex` (~1,200 words, currently in main) → move to `supplementary.tex` as new section §S-X
- Update `main.tex` to no longer `\include{08_appendix}` 
- Update any in-main cross-references to point to supplementary

After H1: main should be ~8-10 pages.

### H2 — Figure numbering discontinuous
Main uses Fig 4, 5, 10. Fig 1, 2, 3, 6, 7, 8, 9 only in supp. `fig11_energy_breakdown` orphan.

Coordinate with Gemini R11B-1 (figure inventory audit). Once Gemini delivers renumbering plan:
- Main figures get contiguous Fig 1, 2, 3, ...
- Supp figures get Fig S1, S2, ...
- Update all `\ref{fig:...}` in `paper/latex_gpt/sections/*.tex` + `supplementary.tex`
- Verify `fig11_energy_breakdown.pdf` either gets a `\ref` somewhere OR moves to deprecated/

### H3 — 6 duplicate labels
Per audit: `tab:v4-three-seed-summary`, `tab:provenance`, `tab:sensitivity`, `tab:retention-comparison`, `supp:theory-ensemble-hat`, `eq:weight-perturbation`.

For each: rename to a unique label (suggest prefixing with section like `tab:supp-v4-three-seed-summary` for the supp version), update all references.

### H4 — 4 orphan files
- `08_appendix.tex` — addressed in H1 (move to supp)
- `S_energy_provenance.tex` — Round-10 R10H output, never `\input`'d. Fix: add `\input{supplementary/S_energy_provenance}` at appropriate location in `supplementary.tex`
- `S_opect_distribution.tex` — Round-10 R10C output, never `\input`'d. Same fix.
- `S_theory_ensemble_hat_clean.tex` — appears to be duplicate of `S_theory_ensemble_hat.tex`. Check + remove the unused one.

### H5 — `\branchatag` review macro active
`main.tex:25` has `\branchatag` macro/command that's a review-mode artifact. Remove or comment out. Should be a 1-line fix.

### H6 — Conclusion gap statement incomplete
`07_conclusion.tex:7` says "5pp gap to NL=1.0" but doesn't mention the 15pp gap to digital baseline (which is in abstract + results).

Fix: extend the sentence to:
> "leaving a residual ~5 pp gap to the canonical NL=1.0 baseline and ~15 pp gap to the digital reference, primarily due to the joint effect of nonlinear write dynamics and fresh-instance transfer."

---

## 3. R10E AIHWKit comparison integration (when fresh-eval lands)

R10E AIHWKit fresh-eval is running now (Claude-launched, ~30-45 min ETA). When it lands:

1. Read JSON: `paper2_aihwkit_baseline/checkpoints/fresh_eval.json`
2. Extract mean ± std + 10 per-instance accs
3. Drop into Discussion §6.x as a paragraph using Codex's template (CODEX_R10E_AIHWKIT_BASELINE_REPORT_20260425.md §2.4):

> "Direct experimental comparison to AIHWKit \citep{rasch2021aihwkit} under matched canonical settings yields fresh-instance accuracy of [X.XX ± Y.YY%], compared to our Ensemble HAT's 86.16 ± 0.19%. The [LARGE GAP / ROUGH MATCH] reflects [interpretation depending on outcome]."

Three outcome interpretations (use the matching one):
- AIHWKit ~10%: "...reflects AIHWKit's lack of cross-instance training discipline; both methods collapse on fresh hardware..."
- AIHWKit 60-80%: "...indicating partial cross-instance robustness inherent to AIHWKit's noise injection, but Ensemble HAT's structured per-epoch resampling delivers stronger generalization."
- AIHWKit ~85%+: "...indicating AIHWKit's analog noise injection achieves comparable cross-instance generalization; Ensemble HAT's contribution lies in the explicit cross-instance discipline + theoretical grounding."

4. Coordinate with Gemini for `figS_aihwkit_comparison.pdf` rendering

---

## 4. Workflow

### Day 1 (~6 hours)
- Morning: C2-C5 surgical text fixes (~2 hours)
- Afternoon: H1 appendix relocation (~2 hours)  
- Evening: H3-H6 fixes (~2 hours)

### Day 2 (~4 hours, after Gemini delivers figure inventory)
- H2 figure renumbering (with Gemini coordination)
- H4 orphan file integration
- R10E paragraph integration

### Final pass (~1 hour)
- Compile: `cd paper/latex_gpt && latexmk -pdf main.tex`
- Verify RC 0, zero undefined refs
- Verify wordcount: main body ~5,200-5,700 (post-H1)
- Hand off to Claude for integration

---

## 5. Constraints (HARD)

- **No content additions** beyond R10E paragraph
- **No numerical changes** (V6 PHANTOM was fabrication, not a claim — that's why we removed)
- **Zone discipline preserved**: 3A/3B/3C unchanged
- **No bug-retrospective phrasing**
- **Word count post-fix**: ≤ 5,700 main body

---

## 6. Deliverables

| File | Action |
|:--|:--|
| `paper/latex_gpt/sections/01_introduction.tex` | EDIT (C5) |
| `paper/latex_gpt/sections/02_related_work.tex` | EDIT (C3) |
| `paper/latex_gpt/sections/03_methodology.tex` | EDIT (C4) |
| `paper/latex_gpt/sections/04_experimental_setup.tex` | EDIT (C4) |
| `paper/latex_gpt/sections/05_results.tex` | EDIT (C2.1, C2.3) |
| `paper/latex_gpt/sections/06_discussion.tex` | EDIT (R10E paragraph) |
| `paper/latex_gpt/sections/07_conclusion.tex` | EDIT (H6) |
| `paper/latex_gpt/sections/08_appendix.tex` | MOVE to supp (H1) |
| `paper/latex_gpt/main.tex` | EDIT (\branchatag remove H5) |
| `paper/latex_gpt/supplementary.tex` | EDIT (incorporate H1 + add H4 \input + H3 label rename) |
| `paper/latex_gpt/supplementary/S_theory_ensemble_hat.tex` | EDIT (C2.2) |
| `KIMI_R11C_PAPER_FIXIT_REPORT_20260426.md` | NEW (per-issue change log) |

---

## 7. Cold-start refs

- `CLAUDE_PROJECT_SELF_AUDIT_20260426.md` — full issue list
- `CLAUDE_ROUND11_ROLE_REASSIGNMENT_PLAN_20260426.md` — master plan
- `report_md/_gpt/json_gpt/tinyvit_v2v7_results_gpt.json` — V6 real number source
- `CODEX_R10E_AIHWKIT_BASELINE_REPORT_20260425.md` — R10E template paragraph

**No deadline.** ~1-2 days expected. Coordinate with Gemini R11B for H2 figure numbering.
