# Comprehensive Cross-Review Report

**Date:** 2026-04-25  
**Reviewer:** Kimi  
**Scope:** Full manuscript + supplementary + code + config

---

## 1. Terminology Consistency ✅ MOSTLY CLEAN

| Term | Status | Notes |
|------|--------|-------|
| "hook diagnostic" | ✅ Clean | 7 occurrences, all canonical |
| "deployment-fidelity" | ⚠️ FIXED | 1 occurrence in Table 1 caption → changed to "deployment-fidelity claims" |
| "ADC-on" / "ADC-off" | ✅ Consistent | Used uniformly across main text |

**Action taken:** Fixed 1 residual "deployment-fidelity" in `05_results.tex` Table 1 caption.

---

## 2. Number Cross-File Consistency ✅ CONSISTENT

| Number | Abstract | Intro | Results | Discussion | Conclusion | Status |
|--------|----------|-------|---------|------------|------------|--------|
| 86.37±1.54% | ✅ | ✅ | ✅ | ✅ | ✅ | Consistent |
| 10.00% collapse | ✅ | ✅ | ✅ | ✅ | ✅ | Consistent |
| ~80--82% NL=2.0 | ✅ | ✅ | ✅ | — | ✅ | Consistent |
| 6-bit ADC cliff | ✅ | ✅ | ✅ | ✅ | ✅ | Consistent |
| 88.53±0.08% OPECT | ✅ | ✅ | ✅ | — | ✅ | Consistent |
| 81.20% / 80.54% / 80.83% | — | — | ✅ | — | — | M-series cross-seed updated |

**Note:** `05_results.tex.kimi_draft_v3` (sidecar) still has old two-seed averages (81.12% / 80.72% / 80.66%). Sidecar is superseded; no action needed.

---

## 3. Bib File Integrity ✅ CLEAN

- 69 unique entries
- Zero duplicate keys
- Zero missing citations (all \citep/\citet keys resolve to bib entries)

---

## 4. Figure/Table Integrity ✅ CLEAN

### Main text figures (5 total)
1. `fig:accuracy-comparison` — referenced 1×
2. `fig:hat-recovery` — referenced 1×
3. `fig:contour-map` — referenced 1×
4. `fig:ensemble-hat-concept` — referenced 1×
5. `fig:case-study-transfer` — referenced 1×

### Main text + appendix tables (7 total)
1. `tab:exp-notation` — referenced 1×
2. `tab:severe-nl-recovery` — referenced 1×
3. `tab:v4-three-seed-summary` — defined, not referenced (appendix internal)
4. `tab:provenance` — defined, not referenced (appendix internal)
5. `tab:sensitivity` — referenced 2×
6. `tab:sensitivity-ci` — referenced 1×
7. `tab:retention-comparison` — defined, not referenced (appendix internal)

**Verdict:** All referenced figures/tables resolve. Unreferenced appendix tables are acceptable (self-contained appendix sections).

---

## 5. Undefined References 🔴 4 PRE-EXISTING

| Ref | Count | Location | Status |
|-----|-------|----------|--------|
| `eq:hat-ensemble` | 3× | main.log lines 14, 41, 65 | Pre-existing; needs equation definition |
| `subsec:methodology-nl` | 1× | main.log line 77 | Pre-existing; needs section label |

**Root cause:** `eq:hat-ensemble` is referenced but `eq:hat-ensemble-distribution` is defined. Likely a label rename that missed some references. `subsec:methodology-nl` does not exist as a label.

**Recommendation:** Fix in Round-5 integration.

---

## 6. Unreferenced Equations ⚠️ MINOR

The following equations are defined but never referenced:
- `eq:fresh-instance` (Eq. 3 in methodology)
- `eq:frontend-photoresponse` (Eq. 6)
- `eq:frontend-renorm` (Eq. 7)

**Verdict:** Low priority. These equations are descriptive and their surrounding text provides sufficient context. Optional: add `(Eq.~\ref{...})` references in surrounding paragraphs.

---

## 7. Code Quality ✅ CLEAN

- `analog_layers.py`: 1561 lines, NL-guard present, AMP decorators present, `set_analog_config_attribute` helper present
- `test_dual_bug_fix.py`: 7/7 pass
- `test_groupwise_nl_wrapper.py`: 9/9 pass
- `test_adc_perinstance_calibration.py`: 1/1 pass
- Zero TODO/FIXME/PLACEHOLDER in canonical .tex files

---

## 8. File Structure ✅ CLEAN

- `paper/latex_gpt/sections/*.tex`: 9 canonical section files
- `paper/latex_gpt/supplementary/`: 4 supplementary files
- `paper/figures/`: All main + supplementary figures present
- `report_md/_gpt/json_gpt/`: M1-M9 JSON eval outputs complete
- `report_md/_gpt/agent_sync/`: AGENT_SYNC updated

---

## 9. Compile Status

| Document | Pages | Size | Warnings |
|----------|-------|------|----------|
| Main | 19 | 504 KB | 4 undefined refs (pre-existing) |
| Supplementary | 32+ | 2.6 MB | Zero warnings |

---

## 10. Action Items Summary

| Priority | Item | Status |
|:--|:--|:--|
| P0 | Fix 4 undefined refs (`eq:hat-ensemble` ×3, `subsec:methodology-nl` ×1) | ⏳ Round-5 |
| P1 | Optionally reference unreferenced equations | ⏳ Optional |
| P2 | Update README Key Results table with three-seed averages | ⏳ Optional |
| P3 | Fill acknowledgments placeholders | ⏳ User |
