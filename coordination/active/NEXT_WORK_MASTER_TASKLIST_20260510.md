# Compute-ViT Next Work Master Tasklist — 2026-05-10

## Purpose

This tasklist converts the current post-release state into parallel, thesis-useful workstreams. It assumes Paper1 release work is commit-managed, Remote 107 stays on the company server, and the local GPU should be used for thesis/Paper3 experiments rather than idling.

## Current ground truth

- Paper1 is in release-candidate state after final narrative polish and release refresh.
- Current external Paper1 release tarball SHA256: `343ae03de1dfd9c198ae614548dee14bddf04131e160598bc064f5d8544500f6`.
- Paper2/107 remains `107 CLAIM LOCK BLOCKED - RERUN/MANIFEST REQUIRED`; current 107 plots/tables are audit-only.
- Active thesis source lanes:
  - CN: `thesis/cn/`
  - EN: `thesis/en/`
- XJTU template assets exist under `thesis/xjtu_template/`, but active thesis builds currently use `ctexbook` / `report`, not `XJTU-thesis.cls`.
- Local GPU should run thesis/Paper3 directions while company server handles 107.

## Workstream A — Repository closeout and commit hygiene

### A1. Finish local commit hygiene
- Status: conservative Markdown cleanup pass completed locally; `coordination/active/AGENT_SYNC_gpt.md` is now a deprecated compatibility stub and important current context is consolidated in `coordination/agent_reports/Claude/CC_LEGACY_MARKDOWN_CONSOLIDATED_HANDOFF_20260510.md`.
- Owner: Claude single-commander mode unless user reassigns.
- Action:
  - Review and commit or further adjust the Markdown cleanup files.
  - Keep tarball external unless user explicitly force-adds it.
  - Do not push without explicit user command.

### A2. External artifact record
- Status: needs one final stable note after all commits.
- Output:
  - `coordination/agent_reports/Claude/CC_EXTERNAL_ARTIFACT_RECORD_20260510.md`
- Must include:
  - Paper1 tarball path and SHA.
  - Whether tarball is tracked or external.
  - Whether release `cover_letter.pdf` is tracked.

## Workstream B — XJTU thesis-template migration

### B0. Template audit
- Goal: understand `thesis/xjtu_template/XJTU-thesis.cls` without moving active thesis.
- Output:
  - `coordination/agent_reports/Claude/CC_XJTU_TEMPLATE_AUDIT_20260510.md`
- Check:
  - Required metadata fields.
  - Expected directory structure.
  - Engine requirements.
  - Bibliography style.
  - Figure path handling.

### B1. Create safe XJTU submission lane
- Goal: do not overwrite `thesis/cn/`; create a separate formal submission lane.
- Proposed path:
  - `thesis/xjtu_submission/`
- Inputs:
  - Content from `thesis/cn/*.tex`.
  - Metadata pending user confirmation.
- Output:
  - `thesis/xjtu_submission/main.tex`
  - `thesis/xjtu_submission/main.pdf`
  - migration notes.

### B2. Formal metadata collection
- Blocked on user/university info:
  - advisor name/title
  - college/department
  - degree wording
  - university wording
  - date
  - confidentiality / originality declaration requirements

## Workstream C — Local GPU thesis/Paper3 experiments

### C0. GPU safety gate
- Before any local run:
  - run `nvidia-smi`.
  - confirm no existing training active.
  - avoid 100% VRAM saturation.
  - default batch size should target bs>=128 where possible, reduce only on OOM.
  - tee every script output to `logs/` with timestamp.

### C1. Mixed-precision analog mapping P0 — first priority
- Goal: use local GPU for a low-risk extension of Paper1 PCM precision-retention frontier.
- Task spec:
  - `coordination/remote_tasks/thesis/LOCAL_GPU_MIXED_PRECISION_P0_TASKLIST_20260510.md`
- Expected outputs:
  - per-layer sensitivity TSV
  - layer-sensitivity figure
  - report under `coordination/agent_reports/Codex/` or `Claude/` depending owner
- Thesis value:
  - precision frontier chapter / Paper3 seed.

### C2. Drift-aware SAM / Analog-SAM
- Goal: optimize flatness along physical drift direction.
- Task spec:
  - `coordination/remote_tasks/thesis/LOCAL_GPU_DRIFT_AWARE_SAM_TASKLIST_20260510.md`
- Start only after C1 P0 produces sensitivity/infrastructure confidence.

### C3. Spatial variance / IR-drop / floorplan-aware mapping
- Goal: map layer sensitivity to tile quality and nonuniform chip profiles.
- Task spec:
  - `coordination/remote_tasks/thesis/LOCAL_GPU_SPATIAL_VARIANCE_TASKLIST_20260510.md`
- Start after C1 or if mixed precision is blocked.

### C4. CNN-vs-ViT fresh-instance Ensemble HAT comparison
- Goal: close thesis architecture-generality gap.
- Task spec:
  - `coordination/remote_tasks/thesis/LOCAL_GPU_CNN_VS_VIT_HAT_TASKLIST_20260510.md`
- Start when local GPU has spare bandwidth.

## Workstream D — Remote 107 / Paper2 KV-cache

### D1. Remote 107 manifest/rerun unblock
- Location: company server, not local GPU.
- Current gate: blocked.
- Required:
  - per-row metadata envelope
  - exact command
  - code SHA
  - dataset/protocol fields
  - checkpoint SHA256
  - old-vs-corrected comparison
- Existing task/report paths:
  - `coordination/remote_tasks/107/CODEX_107_EVIDENCE_GATE_LEDGER_20260510.md`
  - `coordination/remote_tasks/107/REMOTE_107_METADATA_RECOVERY_OR_MINIMAL_RERUN_REQUEST_20260510.md`
  - `coordination/agent_reports/Claude/CC_107_REMOTE_METADATA_HARVEST_20260510.md`

### D2. Paper2 manuscript skeleton after gate
- Do not draft claim-bearing sections until D1 passes.
- Safe now:
  - method skeleton
  - evidence gate description
  - non-claim-bearing outlook text

## Workstream E — Future thesis integration

### E1. Thesis chapter mapping
- Map each new workstream into final thesis:
  - Paper1: algorithm-device boundary / hardware-instance overfitting.
  - 107: analog KV-cache / LLM memory chapter.
  - Mixed precision: precision-retention frontier extension.
  - Drift-aware SAM: physics-aligned optimization.
  - Spatial variance: floorplan-aware deployment.
  - CNN-vs-ViT: architecture generality.

### E2. Evidence grading
- Every result must be labeled:
  - claim-bearing
  - audit-only
  - pilot/provisional
  - future work

## Immediate next actions

1. Resolve deprecated `AGENT_SYNC_gpt.md` state.
2. Write XJTU template audit (B0).
3. Write local GPU mixed-precision P0 tasklist (C1).
4. Check GPU state before any experiment launch.
5. Keep 107 on company-server path.
