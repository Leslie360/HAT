# DISPATCH KIMI-ROUND6 — Root README + Pre-Submission Checklist
**Date:** 2026-04-25 01:30 CST
**Issued by:** Claude
**Assignee:** Kimi
**Priority:** LOW (housekeeping)
**Time budget:** ~45 min total

---

## Part A (R6-1) — Root README Key Results table patch

### Issue
Per Gemini Round-4 audit pending item: top-level `/home/qiaosir/projects/compute_vit/README.md` Key Results table contains the `30.53%` figure (zone 3B contamination). Erratum header is present, but the table itself wasn't patched.

This is the **repository front door** — first thing any visitor sees. Inconsistency with the rest of the manuscript discipline is bad optics.

### Action
1. Locate the Key Results table in `README.md` (likely lines 10-30 area)
2. Either:
   - **Option A**: Replace `30.53%` row with the post-fix Stage-2 number (`81.13±1.07% Standard / 80.71±0.47% Ensemble / 80.66±0.02% Proportional`) with neutral wording per §5.7 discipline
   - **Option B**: Remove the row entirely, replace with placeholder pointing to paper §5.7
   
   Choose Option A (more informative, still safe).
3. Strip "30.53%" appearance anywhere else in the README
4. Keep the existing Erratum header for historical clarity but remove "previously reported ~30% structural ceiling" language if it appears in body text
5. Verify with grep:
   ```bash
   grep -n "30\.53\|27\.72\|32\.12\|structural ceiling\|severe-NL ceiling" /home/qiaosir/projects/compute_vit/README.md
   # → 0 matches expected (excluding any disclaimer-tagged historical mentions)
   ```

### Constraints
- No bug-retrospective language ("post-fix", "33bed9c", "software artifact")
- Use "hook diagnostic" not "deployment-fidelity" for ADC numbers
- Match §5.7 wording style (neutral protocol terms)

### Time: ~15 min

---

## Part B (R6-5) — Pre-submission checklist refresh

### Scope
Refresh `KIMI_PRE_SUBMISSION_CHECKLIST_20260423.md` to reflect post-Round-5 manuscript state. Many items in the old checklist are stale.

### Updates needed

1. **Manuscript state** — mark these items COMPLETE:
   - All severe-NL numbers locked to Stage-2 per-instance numbers
   - Cover letter v6 in `cover_letter.tex` canonical
   - Theory derivation integrated into supplementary
   - Wager 2013, Tobin 2017 in bib
   - All sidecars merged into canonical .tex files
   - Gemini Round-5 integration verified

2. **Pending items** — keep open:
   - 8×40GB cross-arch results integration (after T1 trigger)
   - Measured-D2D Supp Note S-HW population (after T3 trigger)
   - Hostile-review v2 pass (Round-7)
   - Final pdflatex compile + figure QA pass
   - Zenodo bundle preparation
   - Reviewer + editor suggestion list
   - PhD defense clearance for submission gate

3. **New items** — add:
   - Add explicit ADC-on hook-diagnostic disclosure in cover letter (verify present)
   - Confirm `analog_layers.py` NL-guard + AMP decorators are in main commit (not just patches)
   - Verify `test_dual_bug_fix.py` + `test_groupwise_nl_wrapper.py` + `test_adc_perinstance_calibration.py` are all green at submission commit

4. **Remove stale items**:
   - Anything referring to severe-NL ceiling, 30%, 27.72%, etc.
   - Anything assuming NC submission (we're targeting Nat Electronics)
   - Anything assuming pre-Stage-2 numbers

### Format
Keep existing checklist structure. Mark items with:
- ✅ DONE (with date)
- ⌛ PENDING (with trigger)
- ⏳ STANDING (always-on monitor)
- ❌ REMOVED (stale)

### Time: ~30 min

### Deliverable
Updated `paper/latex_gpt/KIMI_PRE_SUBMISSION_CHECKLIST_20260423.md` (or rename to `_20260425.md` if cleaner)

---

## Reporting
Append status to AGENT_SYNC when both parts complete. No need for separate broadcast — these are housekeeping.
