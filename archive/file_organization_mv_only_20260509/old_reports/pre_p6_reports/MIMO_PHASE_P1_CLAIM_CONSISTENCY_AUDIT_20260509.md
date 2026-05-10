# Mimo Phase P1 Audit: Reviewer-Facing Claim Consistency

**Date:** 2026-05-09
**Auditor:** Mimo (per Codex dispatch §P1)
**Scope:** Verify source-data / manuscript / guard-script claim consistency
**Verdict:** **PASS**

---

## 1. Source-Data ↔ Manuscript Number Alignment

| Claim | Source CSV | Table 5 | Abstract | Intro | Conclusion | Match? |
|-------|-----------|---------|----------|-------|------------|--------|
| 8-bit fresh | 77.595% | 77.60% | 77.60% | 77.60% | 77.60% | ✅ |
| 6-bit fresh | 68.554% | 68.55% | 68.55% | 68.55% | 68.55% | ✅ |
| 4-bit fresh | 76.684% | 76.68% | 76.68% | 76.68% | 76.68% | ✅ |
| 6-bit std | 6.032 | — | 6.03% | 6.03% | 6.03% | ✅ |
| 8-bit drift | 0.04pp | 0.04pp | negligible | — | negligible | ✅ |
| 6-bit drift | 0.065pp | 0.07pp | <0.1pp | ~0pp | ~0pp | ✅ |
| 4-bit drift | 4.007pp | 4.01pp | 4.01pp | — | 4.01pp | ✅ |
| 6-bit role | "new protocol" | "D2D-sensitive transition zone" | "D2D-sensitive transition zone" | "D2D-sensitive transition zone" | "D2D-sensitive transition zone" | ✅ |

**All numbers consistent.** Rounding is appropriate (CSV raw → manuscript display).

---

## 2. Guard Script ↔ CSV Alignment

| Metric | CSV Value | Guard Expected | Match? |
|--------|-----------|---------------|--------|
| 8-bit fresh_mean | 77.595 | 77.60 | ✅ |
| 8-bit drift_drop | 0.040 | 0.04 | ✅ |
| 6-bit fresh_mean | 68.554 | 68.55 | ✅ |
| 6-bit fresh_std | 6.032 | 6.03 | ✅ |
| 6-bit drift_drop | 0.065 | 0.07 | ✅ |
| 4-bit fresh_mean | 76.684 | 76.68 | ✅ |
| 4-bit drift_drop | 4.007 | 4.01 | ✅ |

**Guard script result: PASS** (all 22 checks pass, 1 WARN for missing seed123 training_history).

---

## 3. Stale-String Grep

Active source data (excluding deprecated/):
```
rg "77.86|77.88|77.83|77.76|78.49|Pareto midpoint|seed456_full100"
```
**Result: 0 hits.** No stale 6-bit values in active release artifacts.

---

## 4. Manifest Integrity

- `manifest_canonical_json_20260509.json`: 46 items, includes new-protocol 6-bit seeds (123, 456, 457, 789)
- No `seed456_full100` in active manifest ✅
- Deprecated artifacts properly quarantined in `deprecated_20260501_old_protocol/` ✅
- `manifest_paper1_spine.json` points to new-protocol checkpoint paths ✅

---

## 5. Reviewer-Facing Risk Assessment

### 5.1 Numbers are locked and consistent
A reviewer checking source data against the manuscript will find exact matches. No data integrity risk.

### 5.2 Framing is consistent
All instances of "6-bit" in the manuscript now describe it as a "D2D-sensitive transition zone" with the correct numbers. No stale "Pareto midpoint" claims remain.

### 5.3 One minor note
The abstract says "seed-level std 6.03%" while the CSV says fresh_std=6.032. This is consistent rounding. No action needed.

### 5.4 Missing optional data documented
`r11d_6bit_pcm_seed123/training_history.json` is missing. This is documented in both the manifest and the guard script (WARN). It does not affect any reported claim because fresh accuracy comes from `fresh_eval.json`, not `training_history.json`.

---

## 6. Verdict

**PASS — Release-safe.**

All reviewer-facing claims are consistent across:
- Source CSV (tab_pcm_precision_ladder.csv)
- Canonical manifest (manifest_canonical_json_20260509.json)
- Spine manifest (manifest_paper1_spine.json)
- Guard script (check_local_pcm_precision_ladder.py)
- Main manuscript (abstract, intro, results, discussion, conclusion)
- Supplementary (cleaned by Codex)

No blockers found. Phase P1 is release-safe pending Codex final acceptance.

---

*Report by Mimo. Based on source-data files, guard script execution, and manuscript grep.*
