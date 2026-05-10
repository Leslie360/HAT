# Codex + CC Parallel Workplan

Date: 2026-05-10
Owner: Codex commander
Scope: Coordinate Codex and the separate CC model without write conflicts.

## Current accepted state

- Paper1 final narrative polish is complete, CC author-review minor edits are integrated, and the final release bundle has been refreshed. Current external tarball SHA is `343ae03de1dfd9c198ae614548dee14bddf04131e160598bc064f5d8544500f6`.
- Root and `compute_vit` worktrees are in commit-prep state. No new commit or push has been performed in this final integration pass.
- Remote review clones are canonical at `/home/qiaosir/projects/remote_reviews/105` and `/home/qiaosir/projects/remote_reviews/107`.
- Paper2/107 is not claim-locked. The Gemini "locked" statements are superseded by strict review and CC metadata harvest.
- Current 107 files under `compute_vit/paper2/results/` and `compute_vit/paper2/src/` are draft audit artifacts only.
- CN thesis is compiled; EN thesis is compiled after CC prose-flow polish and Codex post-figure/layout integration. Current CN/EN logs have no overfull hbox entries.

## Non-conflict ownership

### Codex owns

- `/home/qiaosir/projects/BROADCAST.md`
- `compute_vit/coordination/active/CODEX_CC_PARALLEL_WORKPLAN_20260510.md`
- `compute_vit/coordination/remote_tasks/107/CODEX_107_EVIDENCE_GATE_LEDGER_20260510.md`
- Final integration decisions for `compute_vit/paper2/README.md`, `compute_vit/paper2/PROVENANCE_107_20260510.tsv`, `compute_vit/paper2/src/`, and `compute_vit/paper2/results/`.
- Paper1 active-manuscript edits, release-bundle refresh, and final acceptance decisions.
- Thesis final integration after CC reports, including rebuilds triggered by shared Paper1 figure assets.

### CC owns

- Read-only Paper1 author review after Codex polish pass 2.
- Write-only deliverables under `compute_vit/coordination/agent_reports/Claude/`:
  - `CC_107_REMOTE_METADATA_HARVEST_20260510.md`
  - optional `CC_107_OLD_VS_CORRECTED_MAP_20260510.tsv`
  - optional `CC_107_COMMAND_AND_CODE_PATHS_20260510.tsv`
  - `CC_PAPER1_AUTHOR_REVIEW_20260510.md`
  - `CC_THESIS_EN_COMPLETION_20260510.md`
  - `CC_THESIS_EN_PROSE_FLOW_POLISH_20260510.md`

### Shared no-write zones

- CC must not edit `compute_vit/paper1/`, `compute_vit/paper/latex_gpt`, or `compute_vit/manuscripts/paper1/`; CC reads Paper1 only and reports findings.
- Do not move, delete, or copy checkpoints, datasets, or large payloads.
- Do not edit `/home/qiaosir/projects/remote_reviews/105` or `/home/qiaosir/projects/remote_reviews/107`; read only.
- Do not run training or GPU jobs unless the user explicitly asks.
- Do not push.

## Immediate parallel tracks

### Track C1 - Codex gate ledger

Codex will produce a gate ledger that records which Paper2/107 requirements are open, blocked, or satisfied. It will not promote any 107 result to claim-bearing status unless all metadata gates pass.

Expected output:

- `compute_vit/coordination/remote_tasks/107/CODEX_107_EVIDENCE_GATE_LEDGER_20260510.md`

### Track C2 - CC remote metadata harvest

CC should inspect the remote 107 clone and answer these questions without modifying remote files:

1. What exact git branch and SHA produced the P8 corrected-noise JSON files?
2. What file/function implements the corrected-noise path?
3. Are exact train/eval commands recoverable from scripts, logs, shell launchers, or state files?
4. Are dataset split, context length, stride, batch size, analog-layer list, train seed, D2D seed, and C2C seed semantics recoverable?
5. Are checkpoint paths and hashes recoverable without copying checkpoint payloads?
6. Can old-vs-corrected rows be mapped from `RESULTS_SUMMARY.md` and current JSONs without mixing incompatible conditions?
7. Which rows are still blocked because metadata cannot be recovered?

Expected output:

- `compute_vit/coordination/agent_reports/Claude/CC_107_REMOTE_METADATA_HARVEST_20260510.md`

Status: complete. Codex integrated the outcome as `107 CLAIM LOCK BLOCKED - RERUN/MANIFEST REQUIRED`.

### Track C3 - CC Paper1 read-only author review

CC completed:

- `coordination/remote_tasks/paper1/CC_PAPER1_AUTHOR_REVIEW_TASKLIST_20260510.md`

Output:

- `coordination/agent_reports/Claude/CC_PAPER1_AUTHOR_REVIEW_20260510.md`

Codex integrated the minor findings and refreshed the Paper1 release bundle.

### Track C4 - CC English thesis prose-flow pass

CC completed:

- `coordination/remote_tasks/thesis/CC_THESIS_EN_PROSE_FLOW_POLISH_20260510.md`

Output:

- `coordination/agent_reports/Claude/CC_THESIS_EN_PROSE_FLOW_POLISH_20260510.md`

Codex rebuilt CN and EN thesis PDFs after the Paper1 figure refresh so embedded figures no longer carry old `86.37/1.54` labels.

## Integration rule

After CC writes a report, Codex will integrate only the report findings, not remote payloads. For 107, metadata remains incomplete and Paper2 drafting stays blocked. For Paper1 and thesis, Codex has integrated the completed CC reports and rebuilt release/PDF artifacts.

## Current priority order

1. Lock coordination and avoid write conflicts.
2. Keep 107 audit-only and route unblocking through signed manifest or minimal rerun.
3. Preserve Paper1 release-refreshed state unless the user asks for another wording pass or submission packaging.
4. Finish thesis formal metadata after user/university values are confirmed.
5. User approval required before any push or large-file action.
