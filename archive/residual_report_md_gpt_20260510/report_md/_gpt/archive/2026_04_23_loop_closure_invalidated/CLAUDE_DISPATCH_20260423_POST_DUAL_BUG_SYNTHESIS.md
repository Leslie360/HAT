# Claude Dispatch — Post Dual-Bug Synthesis Prep (2026-04-23)

## Context
- `K4R` same-instance strong, fresh-instance poor.
- `K4R` is no longer acceptable as canonical anchor.
- `P1-C` and `P1-C2` have been stopped as contaminated after branch-swap verification.
- Project is now in stop-loss / local-fix phase.

## Deliverables
Produce exactly two files.

### 1. `CLAUDE_STOPLOSS_SYNTHESIS_TEMPLATE_20260423.md`
Sections:
- `What failed`
- `What remains valid`
- `What is now frozen`
- `Minimal fix set`
- `Minimal rerun set`
- `Manuscript / rebuttal wording consequences`

### 2. `CLAUDE_PATCH_GATING_MATRIX_20260423.md`
For each doc class, classify:
- `patch now`
- `patch after fixes`
- `do not touch`

Must include:
- `paper/latex_gpt/*`
- `远端/*.md`
- `report_md/_gpt/*route*`
- `report_md/_gpt/*checklist*`

## Hard rules
- No new scientific claims.
- No result reinterpretation beyond current invalidation status.
