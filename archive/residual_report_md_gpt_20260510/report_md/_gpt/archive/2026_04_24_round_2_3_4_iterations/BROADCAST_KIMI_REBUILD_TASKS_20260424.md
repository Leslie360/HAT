# BROADCAST - Kimi 3-Week Rebuild Tasks
Date: 2026-04-24
Issuer: Codex relaying user directive
Source: `BROADCAST_REBUILD_3WEEK_20260424.md`

Kimi should read `BROADCAST_REBUILD_3WEEK_20260424.md` in full.

## Active Kimi Tasks Now

- `K-ERR-2`: sweep all `_gpt/` Kimi memos from 2026-04-21 to 2026-04-23 that reference `30% structural ceiling`, `bimodal basin`, or `Hartigan p=0.98`; add Erratum stubs.
- `K-ERR-3`: add Chinese 勘误 paragraph at the top of `paper/thesis_cn/chapter_5_failure_modes.tex`; do not delete content yet.
- Prepare `K-DRAFT-{1..6}` as draft files only, with `.kimi_draft_v2` suffix. Do not overwrite live `.tex`.

## Constraints

- Do not edit paper-1 frozen files directly.
- Do not use any bug-contaminated CX-J/CX-K severe-NL number as evidence.
- Use `[CX-M pending]` placeholders until M-series JSONs land.
- One `AGENT_SYNC` entry per task closure.

## Expected Kimi Outputs

- Erratum-tagged Kimi memo list for `K-ERR-2`.
- Chinese thesis Ch.5 erratum for `K-ERR-3`.
- Draft placeholders:
  - `paper/latex_gpt/sections/05_results.tex.kimi_draft_v2`
  - `paper/latex_gpt/cover_letter_v4.tex.kimi_draft`
  - `paper/latex_gpt/sections/00_abstract.tex.kimi_draft_v2`
  - `paper/latex_gpt/sections/06_discussion.tex.kimi_draft_v2`
  - supplementary diff list
  - `paper/thesis_cn/chapter_5_failure_modes.tex` Week-2 rewrite plan
