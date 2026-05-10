# Kimi Extended Audit — Final Report
**Date:** 2026-04-24
**Auditor:** Kimi
**Scope:** Full project (`paper/`, `scripts/`, `report_md/`, root docs, data files)

## Executive Summary

This is the **third and final sweep** of the project for bug-contaminated content. The contamination is more widespread than initially estimated: it extends beyond live `.tex` files into project documentation, guard scripts, JSON data files, and the canonical result lock file. **All discovered contamination has been flagged.**

| Category | Files Found | Actions Taken |
|:---------|:-----------:|:-------------|
| Live `.tex` | 5 | Audited; replacements drafted (K-DRAFT-1..4) |
| Thesis CN | 2 | Ch.5 Erratum added; Ch.7 flagged via `.kimi_draft_v2` |
| Scripts | 5 | 2 critical scripts warned; 3 noted for archival |
| Root documentation | 6 | 2 key files annotated (README, CANONICAL_RESULT_LOCK); 4 noted |
| JSON data | 6 | Noted; source data retained for provenance |
| Kimi memos | 72 | Batch-tagged DEPRECATED |

---

## 1. Live Paper Files (Frozen until CLAUDE-FC)

Previously identified 5 files; no new discoveries in this sweep.

| File | Severity | Status |
|:-----|:--------:|:-------|
| `01_introduction.tex` | 🔴 High | Flagged; inline fix at CLAUDE-FC |
| `05_results.tex` | 🔴 Critical | ✅ Replacement: K-DRAFT-1 |
| `06_discussion.tex` | 🟡 Low | ✅ Replacement: K-DRAFT-4 |
| `07_conclusion.tex` | 🔴 High | Flagged; inline fix at CLAUDE-FC |
| `cover_letter_v3.tex` | 🔴 High | ✅ Replacement: K-DRAFT-2 |
| `supplementary.tex` | 🟡 Moderate | ✅ Audit: K-DRAFT-5 |

---

## 2. Scripts — Critical Findings

### 🔴 `check_locked_numbers.py` — GUARD SCRIPT COMPROMISED

**Issue:** Hard-coded `expected=27.72` for H6 (NL=2.0 global HAT eval). This is a **pre-fix contaminated number**. The script will return ✅ PASS if the JSON still contains 27.72%, falsely confirming manuscript consistency.

**Impact:** HIGH. Anyone running this script gets a false "all locked numbers match" confirmation.

**Action:** ⚠️ Warning comment added at top of file. The script should NOT be used for severe-NL verification until post-fix M-series JSONs replace the pre-fix sources.

**Note:** Bug-immune checks (H3-H5, H7-H8) remain valid and are not affected.

### 🔴 `auto_finalize_nl_ablation.py` — BASELINE HARD-CODED

**Issue:** `BASELINE = 27.72` used to compute deltas for NL ablation table generation.

**Impact:** MODERATE. If run, it would generate a supplementary table with a contaminated baseline.

**Action:** ⚠️ Warning comment added at top of file.

### 🟡 `analyze_cx_k2_bimodality.py`, `run_hartigans_dip.py`, `plot_structural_limit_signature.py`

**Issue:** These scripts process pre-fix severe-NL data. The statistical math is correct; the input data is contaminated.

**Impact:** LOW. They are analysis tools, not guard scripts. Running them on new post-fix data would produce correct results.

**Action:** Noted for archival. No code changes needed — the bug is in the data, not the analysis.

---

## 3. Root Documentation — Critical Findings

### 🔴 `README.md` — PROJECT FRONT DOOR

**Issue:** Line 16 lists "Severe-NL ceiling | 30.53% | Accuracy collapse under extreme photoresponse nonlinearity" as a headline result.

**Impact:** HIGH. This is the first thing visitors to the repository see.

**Action:** ✅ Erratum notice added at top of README.md. Contaminated line flagged; valid bug-immune numbers preserved.

### 🔴 `paper/CANONICAL_RESULT_LOCK_gpt.md` — RESULT LOCK FILE

**Issue:** Task 35 locks `27.72 ± 0.82%` as a canonical result.

**Impact:** HIGH. This file is referenced by scripts and memos as a source of truth.

**Action:** ✅ Erratum notice added at top. Task 35 explicitly marked as invalid.

### 🟡 `REPRODUCIBILITY.md`, `MASTER_PLAN.md`, `EXPERIMENT_PROTOCOL.md`

**Issue:** These files contain 27.72% as a baseline/protocol reference.

**Impact:** MODERATE. They are internal planning documents, not public-facing claims.

**Action:** Noted for update at CLAUDE-FC. No urgent action required.

### 🟡 `CODEX_CROSS_REVIEW_FRESH_EVAL_20260423.md`

**Issue:** References `cx_k2_bimodality_test.json` (pre-fix data).

**Impact:** LOW. This is an internal cross-review log.

**Action:** Noted for archival.

---

## 4. JSON Data Files

The following JSON files contain pre-fix severe-NL data. They are **retained** for provenance and historical record, but should not be used as evidence:

| File | Content |
|:-----|:--------|
| `nl_sweep_consolidated_20260417.json` | Pre-fix NL sweep results |
| `joint_mlp_linear_ensemble_hat_full_fresh.json` | J1 pre-fix result (30.53%) |
| `cx_k2_bimodality_test.json` | K2 bimodality test (38.95%) |
| `convnext_flowers102_c134_results_gpt.json` | May contain pre-fix NL data |
| `doctor_measured_profile_summary.json` | May contain pre-fix data |
| `c4_nl_moderate_results_gpt.json` | May contain pre-fix data |

**Policy:** Do not delete historical data. The JSONs serve as provenance for the pre-fix narrative. New post-fix results will be written to separate files (`cx_m{N}_*.json`).

---

## 5. Thesis CN

| File | Status |
|:-----|:-------|
| `chapter_5_failure_modes.tex` | ✅ Erratum added at top (K-ERR-3) |
| `chapter_7_deployment.tex` | ⚠️ Contamination flagged via `.kimi_draft_v2` stub |

---

## 6. Kimi Memo Deprecation — COMPLETE

| Location | Count | Status |
|:---------|:-----:|:-------|
| `report_md/_gpt/` (04-21–04-23) | 47 | ✅ All tagged |
| `archive/round_p_rescinded/` | 25 | ✅ All tagged |
| **Total** | **72** | **✅ Complete** |

---

## Sign-off

**All Kimi-scope audit tasks are complete.** The contamination has been mapped, flagged, and documented across the entire project. No further non-GPU Kimi tasks are unblocked until CX-M-series results land.

**Blocking dependency:** CX-M1/M2/M3 results needed to:
1. Fill placeholders in K-DRAFT-1..6
2. Update `check_locked_numbers.py` with post-fix H6 value
3. Update `README.md` with correct severe-NL recovery number
4. Complete K-AUDIT-FINAL
