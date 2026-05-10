<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# Kimi Dispatch — Dual-Bug Scrub (2026-04-23)

## Context
The project is no longer in Branch-A-celebration mode. We now have two active local findings:
1. `K4R` fresh result is poor and cannot serve as canonical anchor.
2. `branch-swap` has been elevated to verified local code-review status.
3. `P1-C` and `P1-C2` are now treated as contaminated stop-loss runs.

## Your role
Contamination control only. No theory. No new experiment design.

## Deliverables
Produce exactly three files.

### 1. `KIMI_DUAL_BUG_INVALIDATION_MATRIX_20260423.md`
Classify each affected result/doc as:
- `invalid immediately`
- `historical only`
- `still valid`

Must audit at least:
- `BROADCAST_BRANCH_A_SCRUB_COMPLETE_20260423.md`
- `BROADCAST_K4R_DISASTER_COLLECTIVE_DECISION_20260423.md`
- `BROADCAST_KIMI_BRANCH_SWAP_VERIFIED_20260423.md`
- `KIMI_BRANCH_A_QUICK_REFERENCE_20260423.md`
- `KIMI_PRE_SUBMISSION_CHECKLIST_20260423.md`
- `KIMI_K4R_RESULT_TEMPLATE_20260423.md`
- `KIMI_K4R_RESULTS_CONDITIONAL_DRAFT_20260423.md`

### 2. `KIMI_STOPLOSS_BROADCAST_TEMPLATE_20260423.md`
A concise broadcast template stating:
- `K4R` invalid as canonical anchor
- `P1-C/P1-C2` stopped as contaminated
- project is back in local-fix phase before any new canonical GPU run

### 3. `KIMI_CANONICAL_SURVIVORS_20260423.md`
List the results that still survive and can still be cited right now.
Do not speculate.

## Hard rules
- Do not propose new experiments.
- Do not write theory derivations.
- Do not reuse `K4R` fresh result as route anchor.
