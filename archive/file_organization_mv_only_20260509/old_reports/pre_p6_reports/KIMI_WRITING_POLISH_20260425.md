# KIMI Writing Polish — Status Report
**Date:** 2026-04-25
**Task:** DISPATCH_KIMI_WRITING_POLISH_20260425.md (Phase 3 of Round-7 Proactive Sprint)
**Assignee:** Kimi
**Status:** IN PROGRESS (skeleton tasks complete; deep audit pending Phase 2)

---

## Completed Tasks

### Task C — Design Rules Callout Box ✅
**File:** `paper/latex_gpt/supplementary/design_rules_box.tex`
**Content:** 7 actionable design rules with quantitative thresholds (6-bit ADC, D2D hierarchy, Ensemble HAT, per-epoch resampling, scale recovery, inverse-gamma, measured calibration).
**Format:** `tcolorbox` environment.
**Note:** `\usepackage{tcolorbox}` added to `main.tex` preamble.

### Task D — Reproducibility Cookbook ✅
**File:** `paper/latex_gpt/supplementary/S_reproducibility.tex`
**Content:** 112 lines, 3-page step-by-step guide covering environment setup, verification suite, canonical Ensemble HAT training, fresh-instance evaluation, ADC ablation, and non-determinism note.
**Status:** Ready for `\input` into main supplementary.

### Task F — Acknowledgments / Funding / Credits Skeleton ✅
**File:** `paper/latex_gpt/acknowledgments_funding_credits.tex`
**Content:** CRediT taxonomy skeleton, funding placeholder, competing interests, data/code availability statement.
**Status:** User to complete funding details before submission.

---

## Pending Tasks (Blocked or Waiting)

### Task A — Opening/Closing Sentences Audit ⏳
**Scope:** All 8 sections (`00_abstract` through `07_conclusion`).
**Status:** Quick scan completed. Deep rewrite deferred until Task B restructuring is finalized (to avoid double work).
**Plan:** Execute after Task B lands.

### Task B — Discussion Narrative Arc Restructuring ⏳
**Scope:** `06_discussion.tex` → Diagnosis → Treatment → Mechanism → Implications → Limitations.
**Status:** BLOCKED on Phase 2 Codex empirical output (Hessian / loss-landscape / CKA analyses needed for §6.3 Mechanism).
**Plan:** Start skeleton restructuring now; populate §6.3 after Phase 2 lands.

### Task E — Figure Captions Self-Contained Audit ⏳
**Scope:** All figures in `paper/figures/`.
**Status:** BLOCKED on Phase 2 new figures (Hessian / loss-landscape / CKA / per-layer).
**Plan:** Audit existing figures now; Phase 2 figures after they land.

---

## Compile Status

| Metric | Value |
|:-------|:------|
| `main.pdf` pages | 20 (was 19 before bib additions) |
| `main.pdf` size | 470 KB |
| Bib entries | 69 unique (was 61) |
| Undefined refs | 4 (pre-existing Round-5 scope) |
| Compile result | ✅ PDF generated (force mode) |

---

## Next Actions

1. **If user approves:** Start Task B skeleton restructuring of `06_discussion.tex` (can proceed without Phase 2 data by leaving §6.3 as placeholder).
2. **If M7 eval completes:** Launch M8/M9 fresh eval, update cross-host parity report.
3. **If Phase 2 lands:** Populate §6.3, integrate new figures, complete Task E.

---

## Deliverables Checklist

| File | Status |
|:-----|:-------|
| `paper/latex_gpt/supplementary/design_rules_box.tex` | ✅ |
| `paper/latex_gpt/supplementary/S_reproducibility.tex` | ✅ |
| `paper/latex_gpt/acknowledgments_funding_credits.tex` | ✅ |
| `paper/latex_gpt/sections/06_discussion.tex` (restructured) | ⏳ |
| `paper/latex_gpt/sections/*.tex` (opening/closing audited) | ⏳ |
| Figure caption edits | ⏳ |
