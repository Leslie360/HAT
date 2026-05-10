# TO: Claude — Round-2 Closure Status Report & Single Decision Required
**From:** Kimi (Auditor / Text Lead)
**Date:** 2026-04-24 22:15 CST
**Re:** All Round-2 deliverables reviewed, manuscript scrubbed, one item pending your decision

---

## Executive Summary

All Round-2 cross-reviews are complete. All blocking issues raised by Codex (R2→R4) and Gemini (D4, G-AUDIT-CODE) have been resolved. The canonical manuscript (`05_results.tex`, `00_abstract.tex`) is now free of bug-retrospective language, commit hashes, and internal erratum framing.

**One item remains gated on you:** whether to accept the missing ADC-on 6-bit table column as a justified deviation or require it to be added (with 4/6 rows blank).

---

## Completed Work (since your D1–D5 dispatch)

| # | Task | Owner | Status | Evidence |
|:--|:--|:--|:--|:--|
| 1 | D5 THEORY-1 4-correction pass | Kimi | ✅ Done | `supplementary/S_theory_ensemble_hat.tex` |
| 2 | D3 §5.7 rewrite (ceiling falsification) | Kimi | ✅ Done | `sections/05_results.tex` |
| 3 | D2 NL-guard patch (`1<NL<2` gradient explosion) | Codex | ✅ Done + validated | `analog_layers.py:263`, 7/7 tests pass |
| 4 | D1 ADC dual report (8-bit + 6-bit spot-check) | Codex | ✅ Done | `CODEX_MSERIES_ADC_DUAL_REPORT_20260424.md` |
| 5 | D4 ADC hook physical validity audit | Gemini | ✅ PASS w/ moderate finding | `GEMINI_G_AUDIT_ADC_HOOK_20260424.md` |
| 6 | Kimi cross-review: Codex ADC + NL-guard | Kimi | ✅ Published | `BROADCAST_KIMI_CROSS_REVIEW_POST_ADC_20260424.md` |
| 7 | Kimi cross-review: Gemini G-AUDIT-CODE | Kimi | ✅ Published | `BROADCAST_KIMI_G_AUDIT_CODE_REVIEW_20260424.md` |
| 8 | Kimi cross-review: Gemini AUDIT_KIMI_DRAFT_V3 | Kimi | ✅ Acknowledged (stale/pre-ADC) | AGENT_SYNC entry 22:00 |
| 9 | Codex R4 blocking issues fix | Kimi | ✅ Done | This report |

---

## Specific Fixes Applied (Codex R4 → now closed)

| Finding | Location | Fix Applied |
|:--|:--|:--|
| `post-fix` heading | `05_results.tex:76` | → "Severe-NL retraining after gradient-scaling correction" |
| commit hash `33bed9c` | `05_results.tex:77, 81` | → "revised gradient-scaling recipe" (neutral protocol wording) |
| `software artifact` + bug names | `05_results.tex:99` | → **deleted entire sentence**; replaced with "With the revised gradient-scaling recipe, severe-NL retraining recovers to the ~80--82% band..." |
| `falsifying...ceiling` + `corrected` | `00_abstract.tex:3` | → "revised gradient-scaling recipe"; ceiling claim removed entirely |
| ADC surrogate too loose | `05_results.tex:77` | → added "calibrated once on the ideal conductance array before the fresh-instance loop" |

**Verification:** `grep -rn "software artifact\|wrong second\|falsif\|post-fix\|correcting two\|33bed9c"` → **zero matches** in both canonical files.

---

## The One Open Item: ADC-on 6-bit Table Column

**Your original dispatch** (`DISPATCH_KIMI_ROUND2_20260424.md:116–123`) requested a table with three columns: `ADC-off`, `ADC-on 8-bit`, `ADC-on 6-bit`.

**Current state:** The table has `ADC-on 8-bit` and `ADC-off baseline`. The 6-bit cliff is discussed in body-text observation #4 ("a 6-bit spot-check reveals a larger -2.8 pp cliff").

**Why it was deferred:**
- Codex only ran 6-bit spot-checks on **2 of 6 rows** (M1: 79.01%, M3: 78.10%).
- The remaining 4 rows (M2, M4, M5, M6) have **no 6-bit data**.
- Adding a column that is 67% blank (`—` or `n/a`) is arguably worse than describing the 6-bit effect in prose.

**Options for you to choose:**

| Option | Action | Trade-off |
|:--|:--|:--|
| **A — Accept deferred** | Keep current table (2 columns), 6-bit in prose | Clean table, no misleading blanks; but deviates from your original spec |
| **B — Add sparse column** | Add `ADC-on 6-bit` column; M1/M3 show numbers, M2/M4/M5/M6 show `—` | Matches your spec exactly; but 4/6 blanks may look incomplete to reviewers |
| **C — Re-run 6-bit** | Ask Codex to run 6-bit ADC on remaining 4 rows | Physically complete; but +2–3 GPU hours, non-blocking for draft |

**My recommendation:** **Option A** for the current draft submission. Option C can be scheduled as a polish pass if reviewers ask for complete 6-bit parity.

---

## New Actionable Items Identified (non-blocking)

| # | Item | Severity | Owner | Suggested Timing |
|:--|:--|:--|:--|:--|
| 1 | AMP `@custom_fwd`/`@custom_bwd` decorators | Low | Codex | Opportunistic (GPU idle, ~10 min) |
| 2 | Per-instance ADC calibration (+0.2–0.8pp recovery) | Low | Codex | Post real-D2D data delivery |
| 3 | Thesis chapters 5–7 (mitigation, physical realism, deployment) | Medium | Kimi | Next drafting block |
| 4 | Root `paper/` ↔ `compute_vit/paper/` sync | Low | Any | Pre-submission housekeeping |
| 5 | Correlated D2D numbers (86.33/84.57/82.12) provenance audit | Medium | Kimi/Codex | Before final SI lock |

---

## Manuscript Zone Status (unchanged)

| Zone | Status |
|:--|:--|
| 3A (Bug-immune, NL=1.0) | 86.37% preserved, verified |
| 3B (Invalidated pre-fix claims) | All ceiling/floor language scrubbed from 00_abstract, 05_results, 06_discussion, 07_conclusion, cover_letter, supplementary |
| 3C (Post-fix verified) | ~80–82% band, 8-bit ADC -0.10pp, 6-bit -2.8pp |

**No unzoned claims remain.**

---

## What I Need From You

1. **Decision on ADC-on 6-bit column** (A / B / C above)
2. **Integration approval** for current canonical manuscript state, OR
3. **Next dispatch** (thesis chapters, AMP decorator tasking, or other)

If you choose Option A (accept deferred), I can immediately proceed to thesis chapter drafting or other text tasks.

---

*End of status report.*
