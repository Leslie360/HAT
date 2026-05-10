# Dispatch Superphase P3 — Long Autonomous Work Package

Date: 2026-05-09
Issued by: Codex
Mode: long-running autonomous phase to reduce repeated user instructions
Expected duration: 3-7 days, or until all gates close

## Executive Decision

Paper-1 scientific content is currently frozen. Do not change scientific numbers, figure semantics, or narrative framing unless a concrete guard failure is found.

The next long package has five tracks:

1. P2R release-candidate cleanup and final bundle hardening.
2. Paper-1 clean-room reproducibility and submission readiness.
3. Remote 105/107 result ingestion and separation from Paper-1 claims.
4. Local GPU/non-GPU backlog triage without disturbing Paper-1 freeze.
5. Master status/index consolidation so the user does not need to keep asking where data lives.

## Agent Responsibilities

- **Kimi**: primary executor for all tracks. Kimi should keep working through this whole document without asking for new instructions unless a kill criterion triggers.
- **DS**: audit after Kimi delivers a major checkpoint or final package. Focus on reproducibility, hidden stale artifacts, and code/data provenance.
- **Mimo**: audit after Kimi delivers. Focus on reviewer-facing clarity, package completeness, and whether claims are overreaching.
- **Gemini**: visual/layout only when the user explicitly requests it. Do not edit data semantics.
- **Codex**: final acceptance and next dispatch only after Kimi + DS/Mimo reports.

## Track A — P2R Clean Release Bundle

### Goal
Turn `release_artifacts/paper1_release_candidate_20260509/` into a clean final release candidate without draft/backup contamination.

### Required Work

1. Create a new directory:
   - `release_artifacts/paper1_release_candidate_20260509_clean/`
2. Copy only active release files.
3. Exclude all files matching:
   - `*.bak`, `*.bak_*`, `*kimi_draft*`, `*draft*`, `*temp*`, `*test*`, editor swap files, cache files.
4. Include deprecated old-protocol JSON only under:
   - `source_data/canonical_json/deprecated_20260501_old_protocol/`
5. Verify every included figure is either referenced by LaTeX or intentionally included as source-data/visual evidence. Unreferenced large images should be excluded unless documented.
6. Regenerate:
   - `MANIFEST_FILES.txt`
   - `SHA256SUMS.txt`
   - `RELEASE_README.md`
7. Rerun guards:
   - stale grep on active bundle
   - PDF text stale scan
   - file-size scan
   - no `.pt`/`.pth`/`.ckpt`
   - manifest/hash check

### Deliverable
`report_md/_gpt/KIMI_P3_TRACK_A_P2R_CLEAN_BUNDLE_REPORT_20260509.md`

### Success Criteria
- No draft/backup/temp files in clean bundle.
- No active stale old 6-bit claims.
- No large unexpected files.
- Both PDFs present and fresh.
- Source data and manifests present.

## Track B — Paper-1 Clean-room Reproducibility

### Goal
Prove a fresh reader can understand and rebuild the package from the clean bundle.

### Required Work

1. Create a temporary clean-room directory under `outputs/cleanroom_paper1_YYYYMMDD_HHMM/`.
2. Copy the clean release candidate there.
3. Run build commands from `RELEASE_README.md` exactly.
4. Verify PDFs are generated or already provided as expected.
5. Verify source data consistency:
   - `tab_pcm_precision_ladder.csv`
   - `manifest_canonical_json_20260509.json`
   - `manifest_paper1_spine.json`
6. Write a clean-room report with exact commands and outputs.

### Deliverable
`report_md/_gpt/KIMI_P3_TRACK_B_CLEANROOM_REPRO_REPORT_20260509.md`

### Success Criteria
- Clean-room build path is documented.
- Any warnings are classified as cosmetic or blocking.
- No hidden dependency on raw checkpoints.

## Track C — Remote 105/107 Ingestion

### Goal
Keep remote evidence moving without contaminating Paper-1 release claims.

### Required Work

1. Use `report_md/_gpt/REMOTE_105_107_LONG_TASKLIST_20260509.md` as the canonical remote tasklist.
2. If remote 105 or 107 returns results, ingest them into:
   - `report_md/_gpt/REMOTE_105_107_DATA_ACQUISITION_INDEX_20260507.md`
   - a new dated review file under `report_md/_gpt/`
3. Classify each result:
   - Paper-1 main / Paper-1 supplement / future-only / Work-2 / exclude
4. Do not edit Paper-1 main or supplement for remote results unless Codex explicitly accepts a result into Paper-1.
5. Maintain separate Work-2 notes for 107 analog KV-cache.

### Deliverable
`report_md/_gpt/KIMI_P3_TRACK_C_REMOTE_105_107_INGESTION_REPORT_20260509.md`

### Success Criteria
- 105 and 107 outputs are indexed.
- No cross-contamination between Paper-1 and Work-2.
- Bugs and superseded results are explicitly marked.

## Track D — Local GPU / Non-GPU Backlog Triage

### Goal
Use local resources pragmatically without destabilizing the frozen Paper-1 package.

### Rules

1. Do not launch Paper-1-changing experiments unless a guard failure requires reproduction.
2. If GPUs are idle, prioritize low-risk verification or Work-2 exploratory tasks that do not alter Paper-1 claims.
3. Every GPU job must have:
   - exact command
   - expected duration
   - GPU id
   - kill criterion
   - output path
4. Early stop if no useful movement after the predefined criterion.
5. Non-GPU tasks have priority while release bundle cleanup is incomplete.

### Candidate GPU Tasks

Only run these if Track A/B are not blocked:

1. Work-2 KV local smoke checks if code/data are present locally.
2. Paper-1 clean-room reproduction smoke tests that do not train from scratch.
3. Minimal sanity reruns for source-data guard if a manifest/hash mismatch appears.

### Deliverable
`report_md/_gpt/KIMI_P3_TRACK_D_GPU_BACKLOG_STATUS_20260509.md`

### Success Criteria
- No idle GPU waste if meaningful low-risk tasks are available.
- No untracked GPU jobs.
- No new Paper-1 claims without Codex acceptance.

## Track E — Master Status And Data Map

### Goal
Give the user one place to look instead of repeatedly asking where things are.

### Required Work

Create/update:

1. `report_md/_gpt/PROJECT_MASTER_STATUS_20260509.md`
2. `report_md/_gpt/DATA_LOCATION_INDEX_20260429.md`
3. `report_md/_gpt/REMOTE_105_107_DATA_ACQUISITION_INDEX_20260507.md`

The master status must include:

- Paper-1 current state and clean bundle path.
- Locked canonical PCM numbers.
- Current local GPU status and job queue.
- 105 status.
- 107 status.
- What is frozen vs still experimental.
- What requires user action, if anything.

### Deliverable
`report_md/_gpt/KIMI_P3_TRACK_E_MASTER_STATUS_REPORT_20260509.md`

## Reporting Rules

Kimi should broadcast progress without waiting for the user:

- Start of P3.
- Completion of each track A-E.
- Any blocker.
- Final P3 delivery.

Do not ask the user for routine decisions. Use these defaults:

- If a file is draft/backup/temp: exclude from release bundle.
- If a result is remote and not fully gated: classify as future-only or Work-2.
- If a new experiment might alter Paper-1: do not run it without Codex acceptance.
- If a guard fails: stop, report exact failure, and propose the smallest repair.

## Final P3 Deliverable

When all tracks finish, write:

`report_md/_gpt/KIMI_SUPERPHASE_P3_FINAL_DELIVERY_20260509.md`

Required sections:

1. Track A-E completion table
2. Clean release bundle path
3. Guard outputs summary
4. Clean-room result
5. Remote 105/107 status
6. GPU/backlog status
7. Master data map links
8. Remaining risks
9. Recommended next Codex decision

## Kill Criteria

Stop and broadcast immediately if:

- clean bundle still contains draft/backup files;
- active stale 6-bit claims reappear;
- PDFs fail to build;
- `.pt`/checkpoint files enter release bundle;
- remote results conflict with Paper-1 canonical numbers;
- GPU jobs fail repeatedly or threaten active release files.
