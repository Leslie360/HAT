# Kimi Draft Self-Audit: Internal Consistency Check
**Date:** 2026-04-24
**Auditor:** Kimi (self-audit)
**Scope:** K-DRAFT-1 through K-DRAFT-6 + chapter_7 flag

## Method

Cross-reference every numerical claim, placeholder, and narrative statement across all Kimi drafts to detect:
1. Internal contradictions (number A in one draft contradicts number B in another)
2. Missing error bars or inconsistent precision
3. Stale references to deprecated narrative
4. Claims that exceed evidence
5. Placeholder inconsistencies

---

## Bug-Immune Canonical Numbers (Cross-Draft Check)

| Number | Source | K-DRAFT-1 | K-DRAFT-2 | K-DRAFT-3 | K-DRAFT-4 | K-DRAFT-6 | Status |
|:-------|:-------|:---------:|:---------:|:---------:|:---------:|:---------:|:------:|
| Ensemble HAT @ NL=1.0 | 86.37±1.54% | ✅ | ✅ | ✅ | ✅ | ✅ | **Consistent** |
| Proportional HAT @ NL=1.0 | 97.37±0.05% | ✅ | — | ✅ | — | — | **Consistent** |
| OPECT zero-shot | 88.53±0.08% | — | ✅ | ✅ | — | — | **Consistent** |
| Standard HAT collapse @ NL=1.0 | 10.00% | — | — | — | — | — | Not in drafts (OK) |

**Finding:** All canonical bug-immune numbers are consistent across drafts. No contradictions.

---

## Placeholder Check

| Placeholder | K-DRAFT-1 | K-DRAFT-2 | K-DRAFT-3 | K-DRAFT-4 | K-DRAFT-6 | Status |
|:------------|:---------:|:---------:|:---------:|:---------:|:---------:|:------:|
| `[CX-M1 pending]` | ✅ | ✅ | ✅ | ✅ | ✅ | **Consistent** |
| `[CX-M2 pending]` | ✅ | — | — | — | ✅ | Only where needed |
| `[CX-M3 pending]` | ✅ (M3/M4) | — | — | — | ✅ | Only where needed |
| `[TBD]` | — | — | — | ✅ (residual gap) | — | Correctly localized |

**Finding:** Placeholder usage is consistent and appropriately scoped.

---

## Narrative Consistency

| Narrative Element | K-DRAFT-1 | K-DRAFT-2 | K-DRAFT-3 | K-DRAFT-4 | K-DRAFT-6 | Status |
|:------------------|:---------:|:---------:|:---------:|:---------:|:---------:|:------:|
| "falsifying ~30% ceiling" | ✅ | ✅ | ✅ | — | ✅ | **Consistent** |
| "commit 33bed9c" | ✅ | ✅ | ✅ | ✅ | ✅ | **Consistent** |
| "pre-fix retracted" | ✅ | ✅ | ✅ | ✅ | ✅ | **Consistent** |
| "two bugs: branch swap + nl multiplier" | ✅ | ✅ | ✅ | ✅ | ✅ | **Consistent** |
| 90.88% = eval-only NL swap (NOT legitimate) | ✅ | — | — | — | ✅ | **Consistent** |

**Finding:** Narrative is fully consistent across all drafts. No stale structural-limit language remains.

---

## Issues Found and Fixed

### Issue #1: Missing error bar in K-DRAFT-4
**Location:** `06_discussion.tex.kimi_draft_v2`, line 5
**Before:** `...versus 86.37\% under canonical conditions...`
**After:** `...versus 86.37$\pm$1.54\% under canonical conditions...`
**Severity:** 🟡 Low — cosmetic; does not affect meaning.

### Issue #2: Missing error bar in K-DRAFT-6
**Location:** `chapter_5_failure_modes.tex.kimi_draft_v2`, line 13
**Before:** `（Ensemble HAT 86.37\%）`
**After:** `（Ensemble HAT 86.37$\pm$1.54\%）`
**Severity:** 🟡 Low — cosmetic; does not affect meaning.

---

## Claims vs Evidence Audit

| Claim in Draft | Evidence Status | Risk |
|:---------------|:----------------|:----:|
| "post-fix HAT recovers to ~82%" | Supported by postfix_standard_hat (82.63%) and postfix_ensemble_hat (81.69%), but M-series replication pending | 🟡 Moderate — preliminary evidence strong, but not yet replicated |
| "~30% floor was software artifact" | Post-fix recovery +52 pp strongly supports this; no contradictory evidence | 🟢 Low — well-supported |
| "proportional-noise may improve beyond uniform" | CX-M3/M4 pending; no evidence yet | 🟡 Moderate — explicitly framed as hypothesis, not claim |
| "residual gap is [TBD] pp" | No evidence; placeholder correctly used | 🟢 Low — honest uncertainty |

---

## Conclusion

**Kimi drafts are internally consistent.** All bug-immune numbers match across drafts. All placeholders are used consistently. The retraction narrative is uniform. No stale structural-limit language survives.

**Two cosmetic fixes applied** (missing ±1.54% error bars in K-DRAFT-4 and K-DRAFT-6). No material issues remain.

**Blocking dependency:** CX-M1/M2/M3 results needed to resolve placeholders. Once numbers land, K-AUDIT-FINAL can verify that every cited number appears in either canonical JSON or M-series JSON.
