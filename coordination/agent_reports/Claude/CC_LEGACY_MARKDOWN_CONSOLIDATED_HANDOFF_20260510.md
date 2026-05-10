# Legacy Markdown Consolidated Handoff — 2026-05-10

## Purpose

This file replaces the failed background-agent pass for old/deprecated Markdown cleanup. It consolidates the important retained context and points current agents to short canonical files instead of the 32k-line legacy sync log.

## Cleanup decision

Conservative first pass only.

- Do not delete active Paper1 manuscript/release files.
- Do not edit Paper2 evidence/source files.
- Do not edit active thesis TeX/PDF files.
- Do not touch checkpoint/data paths.
- Do not touch `remote_reviews/` clones.
- Do not run training.
- Do not push.

## Canonical current entrypoints

| Purpose | Current file |
|---|---|
| Cross-workspace broadcast | `/home/qiaosir/projects/BROADCAST.md` |
| Current compute_vit task handoff | `coordination/active/CLAUDE_TASK_gpt.md` |
| Next-work master tasklist | `coordination/active/NEXT_WORK_MASTER_TASKLIST_20260510.md` |
| Codex command dashboard | `coordination/active/CODEX_COMMAND_DASHBOARD_20260510.md` |
| 107 evidence gate ledger | `coordination/remote_tasks/107/CODEX_107_EVIDENCE_GATE_LEDGER_20260510.md` |
| XJTU template audit | `coordination/agent_reports/Claude/CC_XJTU_TEMPLATE_AUDIT_20260510.md` |

## Important retained context

### Paper1

- Paper1 is in release-candidate/final packaging state.
- Current external tarball path: `paper1/release/paper1_submission_bundle_20260509_final.tar.gz`.
- Current tarball SHA256 recorded in the master tasklist: `343ae03de1dfd9c198ae614548dee14bddf04131e160598bc064f5d8544500f6`.
- Release bundle directory and cold-unpack manifest checks were reported as passing in the prior closeout.
- Do not refresh release artifacts unless the user explicitly asks.

### Thesis

- Active CN thesis source: `thesis/cn/`.
- Active EN thesis source: `thesis/en/`.
- XJTU template asset exists at `thesis/xjtu_template/`.
- Active thesis does not currently use `XJTU-thesis.cls`.
- Formal XJTU submission should be created as a separate lane, recommended path `thesis/xjtu_submission/`.

### Paper2 / Remote 107

- Paper2/107 remains claim-lock blocked.
- Current decision: `107 CLAIM LOCK BLOCKED - RERUN/MANIFEST REQUIRED`.
- Existing 107 TSVs/plots are audit-only, not manuscript evidence.
- Remote 107 should stay on company-server path; do not move it to local GPU unless explicitly reassigned.

### Local GPU thesis/Paper3 lanes

Current task specs:

- `coordination/remote_tasks/thesis/LOCAL_GPU_MIXED_PRECISION_P0_TASKLIST_20260510.md`
- `coordination/remote_tasks/thesis/LOCAL_GPU_DRIFT_AWARE_SAM_TASKLIST_20260510.md`
- `coordination/remote_tasks/thesis/LOCAL_GPU_SPATIAL_VARIANCE_TASKLIST_20260510.md`
- `coordination/remote_tasks/thesis/LOCAL_GPU_CNN_VS_VIT_HAT_TASKLIST_20260510.md`

Before any local GPU run:

- run `nvidia-smi`.
- confirm no active training.
- avoid VRAM saturation.
- default batch size target is `bs>=128` where possible, reduce only on OOM.
- tee all script output to timestamped logs under `logs/`.

## Deprecated Markdown handling

### `coordination/active/AGENT_SYNC_gpt.md`

The legacy long-form sync log is too large and mixes stale history with current status. It is being compacted into a compatibility stub that points to this consolidated handoff and current entrypoints.

Historical details remain recoverable from git history if needed. New status should go to root `BROADCAST.md` or the scoped current task/report files above.

### `coordination/active/CLAUDE_TASK_gpt.md`

This file is kept because `report_md/_gpt/CLAUDE_TASK_gpt.md` symlinks to it and external agents may still look there. Its content should be current and short.

### `report_md/_gpt/`

Keep only compatibility index/inventory files and symlinks. Do not put new active task content directly there.

## Cleanup performed in this takeover pass

- Compacted `coordination/active/AGENT_SYNC_gpt.md` from the legacy 32k-line sync ledger into a short deprecated compatibility stub.
- Refreshed `coordination/active/CLAUDE_TASK_gpt.md` as the current short task handoff.
- Updated `coordination/README.md` and `report_md/_gpt/INDEX_CURRENT_20260509.md` so future agents do not treat the old sync log as active.
- Deleted 26 clearly archived stale Markdown files from:
  - `archive/reorg_20260509/report_md_residuals/`
  - `archive/reorg_20260509/paper2_legacy_drafts_20260510/`
  - `archive/cleanup_candidates_20260509/old_remote_files/`
- Cleanup log: `logs/legacy_markdown_cleanup_20260510_154139_20260510.log`.

## Remaining safe cleanup candidates

Do not delete these blindly in this pass. Review before deletion:

- old phase reports under `coordination/audits/` that are already superseded by P8 closeout reports.
- legacy coordination history under `archive/file_organization_mv_only_20260509/legacy_archive_dirs/coordination/`.
- old one-off planning docs that duplicate `NEXT_WORK_MASTER_TASKLIST_20260510.md`.

## Next executor instructions

1. Use `coordination/active/CLAUDE_TASK_gpt.md` as the current short handoff.
2. Use the four local-GPU tasklists only after GPU safety check.
3. Keep 107 evidence audit-only until a signed manifest or minimal rerun arrives.
4. Do not append to the old 32k-line sync log.
5. If more Markdown cleanup is needed, remove only files already covered by this report, an index, or git history.
