# Pending Issues Summary (未解决问题汇总)

**Generated:** 2026-04-11  
**Total Issues:** 109  
**Pending:** 3 (2.8%)

> Scope note: this file tracks **reviewer issues only**. Nature Communications submission-package items such as reviewer-accessible code, source-data bundle, and submission-system metadata are tracked separately in `report_md/_gpt/NC_SUBMISSION_CHECKLIST_20260412_gpt.md`.

---

## Summary Statistics

| Status | Count | Percentage |
|:------:|:-----:|:----------:|
| ✅ Completed | 106 | 97.2% |
| 🔶 Partially Addressed | 0 | 0.0% |
| ❌ Not Covered | 3 | 2.8% |
| **Total** | **109** | **100%** |

---

## 🔶 Partially Addressed (0 issues)

目前没有处于“部分解决”状态的 reviewer issue。

**Action Required:** None

---

## ❌ Not Covered (3 issues)

这些问题被认定为低优先级或超出论文范围：

### A. Methodology Scope Limitations (2 issues)

| # | Issue | Reviewer | Rationale | Decision |
|:--:|:------|:---------|:----------|:---------|
| 62 | Proportional + NL coupled effects | Qwen | Complex interaction study beyond current scope | Out of scope |
| 45 | Missing ablation studies (general) | Doubao | Additional coupled ablations would significantly expand scope beyond the now-completed targeted controls | Out of scope |

### B. Physical Validation (1 issue)

| # | Issue | Reviewer | Rationale | Decision |
|:--:|:------|:---------|:----------|:---------|
| 53 | NL write validation vs COMSOL | Hunyuan | Device physics simulation beyond scope | Out of scope |

---

## Critical vs Non-Critical Breakdown

### 🔴 Critical (Blocking Submission)
**None** - All critical reviewer concerns have been addressed.

### 🟡 Recommended (Improvement Possible)
**None**

### 🟢 Low Priority (Acknowledged Limitations)
**3 issues** (#45, #53, #62)
- Explicitly acknowledged in §6.6 Limitations
- Standard scope boundaries for simulation paper
- Would require significant new experiments to address

---

## Defensibility Assessment

### For Nature Communications Submission:

| Aspect | Status | Justification |
|:-------|:------:|:--------------|
| Tier 1 Issues (4+ reviewers) | ✅ All resolved | AIHWKIT comparison, energy bounds, state-dependent models addressed |
| Core Technical Claims | ✅ Supported | Key results have statistics, auxiliary single-run controls are labeled, and main findings are reproducible |
| Limitations Disclosure | ✅ Complete | §6.6 explicitly lists all unmodeled effects |
| Methodology Validation | ✅ Adequate | P13 (AIHWKIT) and P14 (ablation) provide validation |

### Response Strategy for Pending Issues:

**For ❌ issues (#45, #53, #62):**
- Standard response: "Acknowledged as limitations in §6.6; addressing these would require [specific additional work] beyond current scope"
- All fall under "future work" category

---

## Recommendations

### Before Submission:
1. ✅ No reviewer-driven action required - all critical and previously partial issues resolved
2. 🔄 Submission-package closeout still required per `NC_SUBMISSION_CHECKLIST_20260412_gpt.md`

### If Reviewers Raise Pending Issues:
- **❌ issues:** Reference §6.6 limitations section; frame as deliberate scope boundaries

---

## Final Assessment

**Reviewer-Issue Readiness:** ✅ **READY**

**Rationale:**
- 97.2% coverage (106/109 issues)
- 0 critical blocking issues
- 0 partially addressed issues
- All Tier 1 (high consensus) reviewer concerns resolved
- Limitations transparently disclosed
- Paper meets NC standards for simulation/methodology contributions

**Outstanding reviewer work:** None required for initial submission

**Outstanding submission-package work:** reviewer-accessible code archive, source-data bundle, and submission-system metadata confirmation

**Potential revisions:** Minor if raised by reviewers
