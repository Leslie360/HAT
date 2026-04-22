# Non-GPU Workset — 2026-04-21

Scope:
- Only tasks allowed during the live GPU loop.
- No edits to Rule B frozen paper text.
- Focus on missing deliverables that increase loop-closure readiness without touching GPU.

Rule-B constraints:
- Forbidden during loop:
  - `paper/00_abstract.md`
  - `paper/05_results.md`
  - `paper/06_discussion.md`
  - `paper/cover_letter*.md`
  - `KIMI_REBUTTAL_MASTER_20260420.md`
  - `paper/thesis/chapter_5_*.tex`
- Allowed during loop:
  - New `_gpt/` memos, checklists, dispatches
  - `paper/thesis_cn/` additions
  - `paper/paper2/skeleton_v0/` support docs
  - Defense, community, packaging, and planning artifacts

Verified missing deliverables worth doing now:
- Kimi-side:
  - `KIMI_CREDIT_V3_20260420.md`
  - `KIMI_ARXIV_CHECKLIST_V2_20260420.md`
  - `KIMI_CONFERENCE_TEMPLATES_20260420.md`
  - `KIMI_POST_SUBMISSION_PLAYBOOK_20260420.md`
  - `KIMI_DEFENSE_SLIDES_CN_20260420.md`
  - `KIMI_DEFENSE_QA_CN_20260420.md`
  - `paper/thesis_cn/chapter_8_outlook.tex`
  - `KIMI_PAPER2_GAP_ANALYSIS_20260420.md`
  - `KIMI_ROUND_Q_ADVANCE_BRIEF_20260420.md`
- Gemini-side:
  - The core `G-GG*` memos mostly exist.
  - The highest-value non-GPU work is synthesis, not regeneration.

Wave-1 split:

Codex:
- Build and maintain this workset.
- Keep `AGENT_SYNC` authoritative.
- Do not touch frozen paper files while `CX-J1d-2` is live.
- Prepare branch-harvest scaffolds and coordination glue only.

Kimi:
- Write missing packaging / defense / thesis-outlook artifacts.
- Prioritize assets that unblock Friday synthesis and post-loop execution.

Gemini:
- Synthesize existing theory memos into branch-aware guidance for Friday.
- Do not regenerate already-existing `G-GG*` memos unless a true gap is found.

Priority order:
1. Kimi packaging docs: CRediT, arXiv checklist, conference templates, post-submission playbook
2. Kimi thesis / defense: Ch.8 outlook, defense slides, defense Q&A
3. Kimi paper-2 gap analysis + Round-Q advance brief
4. Gemini synthesis memos keyed to `J1d` branch outcomes

Expected value:
- Reduces Friday synthesis overhead.
- Avoids idle time while GPU remains occupied.
- Preserves Rule B discipline.
