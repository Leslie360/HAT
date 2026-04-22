# Gemini Dispatch — Drudge Wave (Non-GPU, Rule-B Safe)

**Date:** 2026-04-22  
**Owner:** Codex local coordination  
**Priority:** Medium / continuous background  
**Goal:** Offload repetitive, audit-heavy, non-GPU work while local GPU stays on `CX-K3`.

## Hard constraints

1. **Do not run GPU experiments.**
2. **Do not edit frozen paper text.** In particular, do not modify:
   - `paper/00_abstract.md`
   - `paper/05_results.md`
   - `paper/06_discussion.md`
   - `paper/cover_letter*.md`
   - `paper/thesis/chapter_5_*.tex`
   - `paper/paper2/draft_v0/*`
3. **Do not overwrite authoritative experiment summaries.**
4. Write outputs only to:
   - `report_md/_gpt/`
   - optionally new helper notes under `paper/thesis_cn/notes/` if needed, but prefer `_gpt/`.
5. When a number depends on `K3 delta_g_eff=0.25` final landing, use a placeholder such as `[K3-0p25 pending]` rather than inventing a value.

## Current authoritative local state

Use these as ground truth:
- `report_md/_gpt/CODEX_J1D_RECONCILIATION_20260421.md`
- `report_md/_gpt/CODEX_CX_K2_SUMMARY.md`
- `report_md/_gpt/CODEX_CX_K3_PROGRESS_20260422.md`
- `report_md/_gpt/CODEX_REMOTE_J1D_CONFIG_REPORT_20260422.md`

Current accepted interpretation:
- Canonical `J1d` local fresh-instance: `41.53 ± 8.87%`
- `K2` authoritative extension: `38.95 ± 9.85%`
- Completed `K3` points so far:
  - `0.05 -> 36.21 ± 9.61%`
  - `0.10 -> 30.79 ± 11.59%`
  - `0.15 -> 27.85 ± 7.37%`
  - `0.20 -> 33.25 ± 10.29%`
- Current working interpretation: the completed `K3` sweep **does not strengthen** the surrogate-break claim.

## Task list

### G-DR1 — Round-Q memo consistency scrub
Write:
- `report_md/_gpt/GEMINI_ROUND_Q_MEMO_CONSISTENCY_20260422.md`

Check all major `_gpt` memos that mention `J1d`, `K2`, or `K3` and classify each statement as:
- `authoritative`
- `memo-level only`
- `stale / contradicted`

Focus on:
- `CODEX_J1D_*`
- `CODEX_CX_K2_*`
- `CODEX_CX_K3_*`
- older `ceiling-broken` / `branch-A` files

Output a table with:
- file
- claim
- status
- action recommendation

### G-DR2 — Thesis CN dependency map for post-K3 landing
Write:
- `report_md/_gpt/GEMINI_THESIS_CN_POST_K3_DEPENDENCY_20260422.md`

Goal:
- map which Chinese thesis chapters / sections need updates when `K3` final lands
- do **not** edit thesis files yet

Include columns:
- target file
- section topic
- can update now? (`yes/no`)
- depends on `K3-0p25`? (`yes/no`)
- replacement style (`number swap`, `interpretation swap`, `footnote only`)

### G-DR3 — Paper-2 skeleton_v1 placeholder audit
Write:
- `report_md/_gpt/GEMINI_PAPER2_SKELETON_V1_PLACEHOLDER_AUDIT_20260422.md`

Audit `paper/paper2/skeleton_v1/` for:
- missing placeholders where numbers should still be deferred
- stale claims that assume `structural limit confirmed`
- stale claims that assume `surrogate broke ceiling`

Do not edit files. Just produce an audit table.

### G-DR4 — Figure/source-data crosswalk v2
Write:
- `report_md/_gpt/GEMINI_FIGURE_SOURCE_CROSSWALK_V2_20260422.md`

Build a crosswalk for the main figures and the current severe-NL follow-up figures:
- figure id
- current caption intent
- source JSON/CSV/log
- authority level (`canonical`, `supplementary-only`, `provisional`)
- whether current data package is enough for Zenodo/public release

### G-DR5 — Reviewer objection bank for ambiguous-branch narrative
Write:
- `report_md/_gpt/GEMINI_AMBIGUOUS_BRANCH_OBJECTION_BANK_20260422.md`

Need 12 concise reviewer objections with response paths, specifically for the case:
- `J1d/K2/K3` stay in the ambiguous / bimodal regime
- `delta_g_eff` sweep weakens the surrogate-break story

Each objection should have:
- objection
- why it is dangerous
- strongest currently available response
- missing evidence if any

### G-DR6 — Defense attack surface update
Write:
- `report_md/_gpt/GEMINI_DEFENSE_ATTACK_SURFACE_V2_20260422.md`

This is a refresh of defense risks given the new local state:
- `K2` ambiguous-bimodal
- `K3` completed points not beating `K2`

Need:
- 15 likely hostile questions
- short answer
- longer answer
- whether answer depends on `K3-0p25`

### G-DR7 — Submission/release housekeeping backlog map
Write:
- `report_md/_gpt/GEMINI_RELEASE_BACKLOG_MAP_20260422.md`

Summarize all remaining non-experiment work needed for a clean release/submission package, excluding user-owned metadata.

Include buckets:
- can do now
- blocked on user metadata
- blocked on `K3 final`
- optional only

### G-DR8 — One-page branch decision aid
Write:
- `report_md/_gpt/GEMINI_BRANCH_DECISION_AID_20260422.md`

This should be a compact decision sheet for local use after `K3-0p25` lands:
- if `0.25` lifts above `K2`
- if `0.25` roughly matches `K2`
- if `0.25` is worse than `K2`

For each case, provide:
- scientific interpretation
- what not to claim
- best next experiment
- whether paper-2 route changes

## Reporting format

For each completed task, Gemini should produce:
1. the requested markdown file
2. a 5-line summary block suitable for `AGENT_SYNC_gpt.md`
3. no prose edits to frozen manuscript files

## Execution order

Recommended order:
1. `G-DR1`
2. `G-DR5`
3. `G-DR8`
4. `G-DR2`
5. `G-DR3`
6. `G-DR4`
7. `G-DR6`
8. `G-DR7`

## Stop conditions

Stop and report instead of guessing if:
- a task requires editing a frozen file
- a task requires a number not yet landed locally
- two local authoritative memos directly conflict and no reconciliation memo exists
