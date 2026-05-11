# Compute-ViT Next Work Master Tasklist — 2026-05-10

## Purpose

This tasklist converts the current post-release state into parallel, thesis-useful workstreams. It assumes Paper1 release work is commit-managed, Remote 107 stays on the company server, and the local GPU should be used for thesis/Paper3 experiments rather than idling.

## Current ground truth

- Paper1 is in release-candidate state after final narrative polish and release refresh.
- Current external Paper1 release tarball SHA256: `343ae03de1dfd9c198ae614548dee14bddf04131e160598bc064f5d8544500f6`.
- Remote107 selective-KV is no longer blocked at the evidence-packet level: the 2026-05-11 packet has 41/41 claim-lockable rows, original per-row JSON artifacts, manifest/report, regenerated figure, and a Paper2 source-data package under `paper2/manuscript/source_data/remote107_selective_kv_claim_lock_20260511/`.
- Paper2 claim boundary is narrow: selective terminal-layer KV is supported by the 410M Remote107 2026-05-11 claim-lock packet; all-layer analog KV is rejected; local retention/refresh, token-by-token cache-path probes, and the newer 107-clean Qwen3-VL or 2.8B/6.9B scale-up pushes remain engineering/provisional until claim-locked.
- Active thesis source lanes:
  - CN: `thesis/cn/`
  - EN: `thesis/en/`
  - XJTU submission lane: `thesis/xjtu_submission/`
- Formal thesis metadata is intentionally deferred until graduation/submission timing is close.
- Local GPU should keep running thesis/Paper2/Paper3 exploratory directions when safe; do not idle it just because a document/source-data loop closed.

## Experiment closure status — 2026-05-11 update

| Direction | Status | Next action |
|---|---|---|
| CIFAR-100 Ensemble HAT seed456/seed789 | seed456 completed on 2026-05-11: train best `66.69%`, source eval `66.66±0.03%`, fresh top42 `64.974±0.538%`; seed789 completed on 2026-05-11: train best `65.05%`, source eval `65.07±0.16%`, fresh top42 `62.131±0.985%` | Treat both as provisional multi-seed expansion evidence; note cross-seed variance and do not promote a closed canonical mean until the final seed protocol closes |
| Remote107 selective-KV claim-lock | Closed for current 410M Paper2 claim packet: 41/41 rows archived and packaged | Use only packaged source data for current claim-bearing Paper2 tables/figures |
| Remote107 107-clean scale-up/Qwen3-VL push | Reviewed on `origin/107-clean` through commit `19038b2`; 410M claim-lock artifacts remain present, while Qwen3-VL/2.8B/6.9B are validation/roadmap lanes | Do not promote scale-up/VLM rows into Paper2 main claims until complete manifests, checkpoint hashes, commands, and source-data packages exist |
| Local KV retention/refresh offline diagnostic | Closed as engineering evidence | Keep out of final PPL/energy/endurance claims |
| Local token-by-token WikiText cache-path probes | Closed for engineering ranking: smoke/micro/8-chunk plus claim-lock-aligned local probe exist | Use only as cache-path sanity/ranking evidence; do not pool with Remote107 claim-lock rows |
| Retention/refresh end-to-end long-context claims | Local vision retention×protection 10×3 completed on 2026-05-11: 0s fresh/top30/top42 `58.223±1.386%` / `62.051±0.587%` / `62.248±0.510%`; 1000s `55.596±1.229%` / `59.207±0.608%` / `59.392±0.605%`; 10000s `55.403±1.272%` / `59.223±0.606%` / `59.391±0.482%`; LLM long-context retention remains open | Vision retention result is provisional simulator evidence only; LLM long-context claims still need larger protocol with tau/refresh/energy/endurance budget |
| Mixed-precision analog mapping P0 | Closed for corrected CIFAR-10 pilot: source-D2D restoration is the valid protection semantics; top30 restores to ~85% mean and top42/source checkpoint restores to ~91.7%, while naive 8-bit/fake-digital controls stay near chance | Summarize into thesis/Paper3 evidence; expand only source-D2D/restored-D2D controls if running CIFAR-100 or more seeds |
| Drift-aware SAM / Analog-SAM | Open | Start after mixed-precision P0 corrected pilot is summarized |
| Spatial variance / IR-drop / floorplan-aware mapping | 10×3 synthetic tile-mapping expansion completed on 2026-05-11: sensitivity-aware `50.9413±1.6904%`, random `46.7020±2.2885%`, worst-case `42.5790±3.5225%`, sequential `39.3353±2.9631%`; figure generated | Keep as provisional synthetic stress evidence; do not present as measured floorplan evidence |
| CNN-vs-ViT fresh-instance HAT comparison | Open | Start when local GPU is free and baseline paths are located |
| 5-bit PCM multiseed | Closed/no-run | Do not run seed456/seed789; strict 5-bit is KILL/non-frontier |


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

### D1. Remote 107 claim-lock packet
- Status: completed at the current evidence-packet level on 2026-05-11.
- Current package:
  - `paper2/manuscript/source_data/remote107_selective_kv_claim_lock_20260511/`
- Locked protocol:
  - Pythia-410M.
  - WikiText-2 raw-v1 test.
  - context length 512.
  - non-overlapping stride 512.
  - batch size 1.
  - digital PPL=23.30.
  - 41/41 original JSON artifacts archived and verified.
- Interpretation:
  - last1/last2 selective terminal-layer KV is supported.
  - all24 is a negative control/rejected main route.
  - do not pool with the stale 22.1849 stride-256 candidate lane or local token-by-token probes.

### D2. Local claim-lock-aligned cache-path engineering probe
- Status: completed 2026-05-11 on local RTX 5070 Ti.
- Purpose: local cache-path sanity check only, not a Remote107 substitute.
- Matrix:
  - digital.
  - last1/last2/last4/all24.
  - D2D=0.02 and 0.05.
  - C2C=0.
  - 8-bit KV.
  - local 512-token WikiText probe, 8 chunks.
- Outputs:
  - `paper2/results/W2_CLAIMLOCK_ALIGNED_LOCAL_CACHE_PATH_PROBE_20260511_142925.tsv`
  - `paper2/results/W2_CLAIMLOCK_ALIGNED_LOCAL_CACHE_PATH_PROBE_20260511_142925_RELATIVE.tsv`
  - raw JSONs under `paper2/results/.w2_claimlock_local_cache_probe_20260511_142925/`
  - `logs/w2_claimlock_aligned_local_cache_path_probe_20260511_142925.log`
- Interpretation:
  - supports the same selective-terminal-layer versus all-layer separation as Remote107;
  - remains engineering-only and must not be pooled with Remote107 claim-lock rows.

### D3. Paper2 manuscript skeleton after gate
- Status: figure-led draft written and overview figure installed on 2026-05-11 after D1 passed.
- Draft:
  - `paper2/manuscript/paper2_figure_led_draft_20260511.tex`
- Figure:
  - `paper2/manuscript/figures/fig_paper2_overview_selective_kv.pdf`
  - `paper2/manuscript/figures/fig_paper2_overview_selective_kv.png`
- Style target:
  - claim-first, figure-driven, concise;
  - real three-panel overview figure first;
  - Remote107 claim-lock table/figure as the only current claim-bearing result;
  - local cache-path, offline reconstruction, and retention/refresh probes labeled engineering-only.
- Next:
  - decide whether to convert the draft into the formal Paper2 manuscript template;
  - upgrade retention/refresh from engineering probes to a locked protocol before any energy/endurance or time-dynamic claim.

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

1. Spatial variance 10×3 expansion is now running as background task `b2g1iu7v3`; do not launch another GPU/Python job while it runs. After it finishes, record raw/summary/profile/mapping artifacts in the ledger, update broadcast, and decide whether to plot floorplan tradeoffs or move to drift-aware SAM.
2. Keep all Paper2/107 claim-bearing tables and figures tied to `paper2/manuscript/source_data/remote107_selective_kv_claim_lock_20260511/`.
3. Convert the Paper2 figure-led draft into the formal manuscript template only after preserving the current evidence-boundary table and limitations.
4. Keep seed456 claims provisional until the agreed multi-seed protocol is closed.
5. Do not push, broad-stage, or launch parallel GPU jobs without explicit approval.
