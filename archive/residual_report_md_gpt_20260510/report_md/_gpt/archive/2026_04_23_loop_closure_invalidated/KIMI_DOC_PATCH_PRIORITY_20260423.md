<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# KIMI Document Patch Priority
**Date:** 2026-04-23

## Patch immediately
- `report_md/_gpt/CODEX_ROUTE_DECISION_20260422.md` (Add errata noting provenance invalidation).
- `report_md/_gpt/KIMI_BRANCH_A_QUICK_REFERENCE_20260423.md` (Update with dual-bug discovery).
- `远端/REMOTE_HOLDING_PATTERN_20260423.md` (If not already present, ensure remote is halted).

## Patch after local code fix
- `远端/INDEX.md` (Update with the canonical commit containing the atomic fix).
- `远端/REMOTE_HANDOFF_PACKET_20260422.md` (Update code sync point).
- `远端/REMOTE_ROUTE_DECISION_20260422.md` (Clarify the corrected physics engine).

## Patch only after first clean rerun
- `report_md/_gpt/KIMI_PRE_SUBMISSION_CHECKLIST_20260423.md` (Numbers and final narrative).
- `paper/latex_gpt/sections/05_results.tex`
- `paper/thesis_cn/chapter_5_failure_modes.tex`
