# CLAUDE — Loop RE-OPENED, Yesterday's Closure Invalidated
**Date:** 2026-04-24
**Authority:** `BROADCAST_HALT_AND_REPLICATE_20260424.md`
**Invalidates:** `CLAUDE_LOOP_CLOSURE_DECLARATION_20260423.md`
**Status:** 🛑 paper-1 NOT submit-ready. Frozen-file edits reverted. Awaiting CX-M{1,2,3,4} replication.

---

## 1. Why this memo exists

Codex bug audit (`CODEX_CROSS_REVIEW_RERUN_20260423.md`) at commit `33bed9c` identified two sign/scaling bugs in the analog STE that **invalidate every result generated under the pre-fix code**, including:

- All CX-J1 / J1b / J1c / J1d series
- All CX-K1 / K2 / K3 / K4 / K5 series
- The N=30 = 38.95 ± 9.85% number used as the basis for yesterday's loop closure
- The Hartigan p=0.98 unimodality test (the test math is correct; the data feeding it was bug-contaminated)

Post-fix legitimate runs (Standard HAT 82.63%, Ensemble HAT 81.69%, both single-seed at NL=2.0 from scratch on commit `33bed9c`) **falsify the structural-limit narrative**.

The Proportional HAT 90.88% reported in `KIMI_FULL_REPORT_20260424.md` is **not** a NL=2.0 result — checkpoint metadata shows `exp_cfg.nl_ltp=1.0`, eval JSON forced `nl_ltp=2.0`. It is an evaluation-only NL swap on a NL=1.0-trained model and must not be used as a paper claim.

## 2. Reverts applied

| File | Action |
|:--|:--|
| `paper/latex_gpt/sections/00_abstract.tex` | Removed appended "N=30 / Hartigan p=0.98 / multi-basin" sentence |
| `paper/latex_gpt/sections/05_results.tex` | Removed inserted "softmax-Lipschitz" paragraph and signature-figure block |
| `paper/latex_gpt/sections/06_discussion.tex` | Removed inserted "small-sample artifact" sentence in Limitations |
| `paper/latex_gpt/cover_letter_v3.tex` | Removed inserted Hartigan sentence and Ablation Coverage Note paragraph |
| `paper/figures/fig_structural_limit_signature.{png,pdf}` | Moved to `paper/figures/deprecated_20260424/` |

The four section files now match the pre-2026-04-23 structural-limit narrative as it stood before yesterday's edits. **However**, that narrative itself is now known to be wrong. Further rewrites are deferred to post-replication.

## 3. What is now legitimate

Code: commit `33bed9c`. Two bugs fixed:
- LTP/LTD branch swap (positive gradient → LTD, negative → LTP)
- Removed extraneous `nl` multiplier in second-order STE

Verified by:
- Codex 367-line audit (`CODEX_CROSS_REVIEW_RERUN_20260423.md`)
- Codex test pass: `test_dual_bug_fix.py` 5/5, `test_groupwise_nl_wrapper.py` 8/8
- Kimi independent arithmetic verification (`KIMI_FULL_REPORT_20260424.md` Section A)

Provisional post-fix numbers (single-seed each, awaiting M-series replication):
- Standard HAT @ NL=2.0 (V3, postfix_standard_hat): **82.63 ± 0.56%** fresh
- Ensemble HAT @ NL=2.0 (V4, postfix_reruns): **81.69 ± 0.64%** fresh

**Both crush the previously claimed ~30% ceiling. The structural-limit story was a software bug.**

## 4. What is now invalid

- All pre-fix CX-J*, CX-K* fresh-instance numbers (the same-instance training accuracies remain valid as training-loss diagnostics, but fresh-instance behavior is suspect because the gradient was corrupted)
- The Hartigan dip test result at p=0.98 (test correct, data wrong)
- The bimodal-vs-structural-limit debate as it played out 2026-04-21 to 04-23 (both interpretations were debating bug-contaminated data)
- The Proportional HAT 90.88% headline (NL=1.0 train / NL=2.0 eval mismatch)

## 5. What stays

- Rule B re-activates on the 5 paper-1 frozen files until next legitimate closure.
- Work 2 (KV-cache) deferred to Round R remains untouched (no GPU contention).
- All Codex / Kimi / Gemini deliverables that are bug-fix-aware (commit `33bed9c` or later) remain valid.
- The bug fix itself stays.
- Honest disclosure obligation: any future paper-1 submission must mention the bug fix in the cover letter.

## 6. Next steps (per BROADCAST_HALT_AND_REPLICATE_20260424.md)

| Owner | Task | Status |
|:--|:--|:--|
| **Claude** | Revert 5 paper-1 edits + quarantine signature figure + write this memo | ✅ Done |
| **Codex** | CX-M1 Standard HAT NL=2.0 seed-B replication | ⏳ Awaiting |
| **Codex** | CX-M2 Ensemble HAT NL=2.0 seed-B replication | ⏳ Awaiting |
| **Codex** | CX-M3 Proportional HAT NL=2.0 from scratch | ⏳ Awaiting |
| **Codex** | CX-M4 Proportional HAT NL=2.0 seed B (conditional on M3) | ⏳ Conditional |
| **Kimi** | K-RETRACT add Erratum to `KIMI_FULL_REPORT_20260424.md` | ⏳ Awaiting |
| **Gemini** | Stand down until M-series lands | ⏳ Standby |
| **Claude** | Write `CLAUDE_LOOP_CLOSURE_DECLARATION_20260424B.md` once M-series + new diff land | ⏳ Future |

## 7. ETA

- ~1 week if M1+M2 replicate consistently and we accept "Standard/Ensemble HAT @ NL=2.0 → 82%" as the headline (drop proportional-HAT story).
- ~2 weeks if M3+M4 also land and proportional-HAT @ NL=2.0 from scratch is added to the manuscript.
- Either path requires a fresh single-shot rewrite of paper-1 §5 and the cover letter, plus a new signature figure.

## 8. One-line summary

Paper-1 is not submit-ready. Yesterday's closure was based on bug-contaminated data. Two seeds of post-fix Standard HAT (~82%) and Ensemble HAT (~82%) at NL=2.0 must replicate before next closure. Cover letter must disclose the bug fix.
