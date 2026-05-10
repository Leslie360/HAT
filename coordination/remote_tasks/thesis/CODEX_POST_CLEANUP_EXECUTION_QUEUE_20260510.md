# Claude Dispatch — Post-Cleanup Thesis/GPU Execution Queue — 2026-05-10

## Role mode

- Claude/CC is now single commander and executor.
- No Codex executor is assumed available.
- User will arrange external review separately.
- Do not use deprecated `coordination/active/AGENT_SYNC_gpt.md` as active task source.

## Current state

- Old archive Markdown/PDF/image junk has been cleaned.
- Current handoff: `coordination/active/CLAUDE_TASK_gpt.md`.
- Consolidated cleanup report: `coordination/agent_reports/Claude/CC_LEGACY_MARKDOWN_CONSOLIDATED_HANDOFF_20260510.md`.
- Artifact cleanup report: `coordination/agent_reports/Claude/CC_ARCHIVE_ARTIFACT_CLEANUP_20260510.md`.
- Paper1 external artifact record: `coordination/agent_reports/Claude/CC_EXTERNAL_ARTIFACT_RECORD_20260510.md`.

## Hard boundaries

- No push.
- No broad `git add -A`.
- No active Paper1 release/manuscript edits unless user asks.
- No checkpoint/data deletion or movement.
- No edits to `remote_reviews/`.
- No local GPU job unless `nvidia-smi` shows safe capacity.
- Tee every command output to `logs/`.

## Execution priority

### P0 — Mixed precision local-GPU probe

Task file:

`coordination/remote_tasks/thesis/LOCAL_GPU_MIXED_PRECISION_P0_TASKLIST_20260510.md`

Expected first output:

- `thesis/results/mixed_precision/layer_inventory_20260510.tsv`
- `thesis/results/mixed_precision/layer_sensitivity_20260510.tsv`
- `thesis/figures/mixed_precision/fig_layer_sensitivity_20260510.png`
- `coordination/agent_reports/Codex/LOCAL_GPU_MIXED_PRECISION_P0_REPORT_20260510.md`

Do not start if another local GPU job is active or VRAM headroom is unsafe.

### P1 — XJTU thesis migration skeleton

Task:

- Use `thesis/xjtu_submission/README.md` and `METADATA_TODO_20260510.md`.
- Use audit: `coordination/agent_reports/Claude/CC_XJTU_TEMPLATE_AUDIT_20260510.md`.

Allowed now:

- skeleton copy/planning.
- path mapping report.
- compile environment check.

Blocked:

- final metadata insertion.
- official PDF claim.
- overwriting `thesis/cn/` or `thesis/en/`.

### P2 — Deferred local GPU lanes

After P0 or if P0 is blocked:

- `coordination/remote_tasks/thesis/LOCAL_GPU_DRIFT_AWARE_SAM_TASKLIST_20260510.md`
- `coordination/remote_tasks/thesis/LOCAL_GPU_SPATIAL_VARIANCE_TASKLIST_20260510.md`
- `coordination/remote_tasks/thesis/LOCAL_GPU_CNN_VS_VIT_HAT_TASKLIST_20260510.md`

### P3 — Remote 107

Keep 107 on company-server path. Local results remain audit-only until manifest/rerun gate passes.

Current decision:

`107 CLAIM LOCK BLOCKED - RERUN/MANIFEST REQUIRED`

Use:

- `coordination/remote_tasks/107/REMOTE_107_METADATA_RECOVERY_OR_MINIMAL_RERUN_REQUEST_20260510.md`

## Reporting requirement

Every executor report must include:

- exact commands.
- log paths.
- output paths.
- GPU preflight if any GPU was used.
- evidence grade: claim-bearing / audit-only / pilot / future work.
- remaining risks.
