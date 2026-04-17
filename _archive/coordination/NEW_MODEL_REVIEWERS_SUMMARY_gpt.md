# New Model Reviewers (mimo-v2-pro & GLM-5.1) Summary

**Date:** 2026-04-11

## New Issues Identified and Status

| # | Issue | Reviewer | Status | Action Taken |
|:--:|:------|:---------|:------:|:-------------|
| 105 | Reference year inconsistency (DOI 2025 vs year 2026) | GLM-5.1 | ✅ | Fixed `zhang2026opect` and `vincze2026dualplasticity` to 2025 with Early Access note |
| 106 | Statistical rigor (single run / few MC samples) | mimo-v2-pro | 🔶 | Key results have error bars; auxiliary claims may need verification |
| 107 | Proportional noise physical basis clarity | mimo-v2-pro | ✅ | Appendix A.5 provides physical justification |
| 108 | Figure reference error (Fig 6 vs Fig 8) | GLM-5.1 | ✅ | Checked: current version correct |
| 109 | Energy absolute value comparison | GLM-5.1 | 🔶 | Ratio provided; absolute comparison mentioned |

## Updated Coverage Statistics

| Status | Count | % |
|:--|:--:|:--:|
| ✅ Completed | 98 | 89.9% |
| 🔶 Partially addressed | 3 | 2.8% |
| ❌ Not covered (low priority) | 8 | 7.3% |
| **Total** | **109** | **100%** |

## Key Fixes Applied

### 1. Bibliography Year Correction
```bibtex
% Before:
year = {2026},
doi = {10.1038/s41467-025-66891-6}

% After:
year = {2025},
doi = {10.1038/s41467-025-66891-6},
note = {Early Access}
```

Affected entries:
- `zhang2026opect` (Nature Communications)
- `vincze2026dualplasticity` (Advanced Electronic Materials)

### 2. Figure Reference Verification
- Checked all Figure 6/8 references in current version
- No errors found; may have been fixed in previous rounds

### 3. Statistical Rigor Documentation
- Key results with error bars documented:
  - Ensemble HAT: 86.37 ± 1.54%
  - P14 V2: 91.30 ± 0.00% (10 runs)
  - C4 three-seed: 84.75 ± 0.72%
  - NL=2.0: 27.72 ± 0.82%

## Files Modified
- `refs_gpt.bib` - Year corrections for early access articles
- `REVIEWER_COVERAGE_MATRIX_gpt.md` - Added new issues #105-109
