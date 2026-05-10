# Claude/Codex Current Task Handoff — 2026-05-10

## Status

This file is the short current handoff for agents that still read `report_md/_gpt/CLAUDE_TASK_gpt.md` or `coordination/active/CLAUDE_TASK_gpt.md`.

Do not use the old long `AGENT_SYNC_gpt.md` history as the active task source.

## Current canonical files

- Workspace broadcast: `/home/qiaosir/projects/BROADCAST.md`
- Master next-work tasklist: `coordination/active/NEXT_WORK_MASTER_TASKLIST_20260510.md`
- Legacy Markdown consolidation: `coordination/agent_reports/Claude/CC_LEGACY_MARKDOWN_CONSOLIDATED_HANDOFF_20260510.md`
- XJTU template audit: `coordination/agent_reports/Claude/CC_XJTU_TEMPLATE_AUDIT_20260510.md`
- Codex command dashboard: `coordination/active/CODEX_COMMAND_DASHBOARD_20260510.md`

### 0. Claude-only execution mode

- Current mode: Claude acts as single commander and executor.
- No Codex executor is assumed available.
- User will arrange external review separately.
- Current executable queue remains useful as a task queue, but ownership is Claude unless reassigned:
  - `coordination/remote_tasks/thesis/CODEX_POST_CLEANUP_EXECUTION_QUEUE_20260510.md`
- Archive/non-active artifact cleanup report:
  - `coordination/agent_reports/Claude/CC_ARCHIVE_ARTIFACT_CLEANUP_20260510.md`
- Paper1 external artifact record:
  - `coordination/agent_reports/Claude/CC_EXTERNAL_ARTIFACT_RECORD_20260510.md`

### 1. Repository and Markdown hygiene

- Treat `coordination/active/AGENT_SYNC_gpt.md` as a deprecated compatibility stub, not a new append target.
- Keep current work in short scoped files.
- Do not delete active Paper1/Paper2/thesis sources, checkpoint/data paths, or `remote_reviews/`.
- Do not push without explicit user approval.

### 2. XJTU thesis submission lane

- Active thesis sources remain:
  - CN: `thesis/cn/`
  - EN: `thesis/en/`
- XJTU template asset: `thesis/xjtu_template/`.
- Current audit: `coordination/agent_reports/Claude/CC_XJTU_TEMPLATE_AUDIT_20260510.md`.
- Recommended future path: `thesis/xjtu_submission/`.
- Blocked metadata must come from the user/university; do not invent advisor, school, degree wording, defense info, or official dates.

### 3. Local GPU thesis/Paper3 tasks

Start only after `nvidia-smi` confirms safe capacity and no active training conflict.

Priority order:

1. `coordination/remote_tasks/thesis/LOCAL_GPU_MIXED_PRECISION_P0_TASKLIST_20260510.md`
2. `coordination/remote_tasks/thesis/LOCAL_GPU_DRIFT_AWARE_SAM_TASKLIST_20260510.md`
3. `coordination/remote_tasks/thesis/LOCAL_GPU_SPATIAL_VARIANCE_TASKLIST_20260510.md`
4. `coordination/remote_tasks/thesis/LOCAL_GPU_CNN_VS_VIT_HAT_TASKLIST_20260510.md`

Rules:

- tee all script output to timestamped files under `logs/`.
- default batch size target is `bs>=128`; reduce only on OOM.
- avoid 100% VRAM saturation.
- do not run parallel GPU jobs unless explicitly approved.

### 4. Paper2 / Remote 107

- Current gate: `107 CLAIM LOCK BLOCKED - RERUN/MANIFEST REQUIRED`.
- Current local 107 results remain audit-only.
- Required unblock path is remote manifest recovery or minimal corrected-noise rerun.
- Use existing 107 task files under `coordination/remote_tasks/107/`.

### 5. Paper1

- Treat Paper1 release as frozen unless the user asks for another wording or packaging pass.
- Current external tarball SHA is recorded in `NEXT_WORK_MASTER_TASKLIST_20260510.md`.
- Do not change Paper1 source data or release payload casually.

## Expected report after execution

When an executor completes a task, write a short report under `coordination/agent_reports/<Agent>/` with:

- exact commands.
- log paths.
- output paths.
- evidence grade: claim-bearing, audit-only, pilot/provisional, or future work.
- remaining risks.
