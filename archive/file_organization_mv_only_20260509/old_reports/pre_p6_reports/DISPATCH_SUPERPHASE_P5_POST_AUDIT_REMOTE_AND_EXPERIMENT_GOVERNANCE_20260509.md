# Dispatch Superphase P5 — Post-Audit Lock, Remote Coordination, And Experiment Governance

**Date:** 2026-05-09
**Issued by:** Codex
**Mode:** long-running autonomous package
**Expected duration:** several hours of continuous Kimi work, followed by DS/Mimo audit

## Executive Decision

Paper-1 is frozen at P4. The next phase is not figure polish and not new Paper-1 science. P5 exists to lock the package against post-audit drift, make the artifact reproducible from a cold unpack, organize all data locations, and prepare 105/107 remote work so tomorrow's results can be ingested without confusion.

## Agent Roles

- **Kimi:** primary executor for all P5 tracks. Do not stop after one small file; run the full package.
- **DS:** audit after Kimi delivery, focusing on hidden scientific drift, reproducibility, and data-provenance rigor.
- **Mimo:** audit after Kimi delivery, focusing on reviewer-facing clarity and operational completeness.
- **Gemini:** visual-only, only if the user explicitly asks. Do not edit scientific values, captions, or source data.
- **Codex:** final acceptance and next dispatch.

## Non-Negotiable Locks

1. Do not change Paper-1 claims, numbers, captions, or source data unless fixing a documented inconsistency against canonical source data.
2. Locked drift definition: `Delta Drift = retention-eval 0 s accuracy - retention-eval 24 h/1d accuracy`.
3. Reject `Fresh - 24h/1d` as a drift-drop definition for Table 5 unless Codex explicitly reopens the decision.
4. Active Paper-1 artifact: `release_artifacts/paper1_submission_bundle_20260509_final/`.
5. Provenance-only artifact: `release_artifacts/paper1_provenance_archive_20260509/`.
6. 105 and 107 results are future/supplement/Work-2 material unless Codex explicitly accepts them into Paper-1.

## Track A — Post-Audit Scientific Drift Reconciliation

### Goal
Ensure the working manuscript tree and the final submission bundle agree on all locked scientific values after Gemini's post-audit edits.

### Required Work

1. Compare these paths for scientific-number divergences:
   - `paper/latex_gpt/sections/`
   - `paper/latex_gpt/supplementary/`
   - `paper/latex_gpt/source_data/`
   - `release_artifacts/paper1_submission_bundle_20260509_final/sections/`
   - `release_artifacts/paper1_submission_bundle_20260509_final/supplementary/`
   - `release_artifacts/paper1_submission_bundle_20260509_final/source_data/`
2. Specifically grep and inspect:
   - `0.03 pp`, `0.09 pp`, `4.04 pp`
   - `0.04 pp`, `0.07 pp`, `4.01 pp`
   - `Fresh - 24h`, `fresh-eval mean minus 24 h`
   - old 6-bit strings: `77.86`, `77.88`, `77.83`, `77.76`, `78.49`, `Pareto midpoint`, `seed456_full100`
   - obsolete headline strings: `86.37`, `86.36` if used as a final 3-seed claim
3. If a working-tree value disagrees with canonical source data, fix the working tree only after recording the exact mismatch.
4. Rebuild `paper/latex_gpt/main.pdf` and run a PDF text scan.
5. Do not change the P4 final bundle unless a verified blocker is found.

### Deliverable

`report_md/_gpt/KIMI_P5_TRACK_A_POST_AUDIT_RECONCILIATION_20260509.md`

Must include:

- every mismatch found;
- whether it was fixed, left unchanged, or escalated;
- exact grep commands;
- final main PDF text-scan evidence for the Table 5 drift row.

## Track B — Cold-Unpack Submission Reproducibility

### Goal
Verify that the compressed archives are usable as standalone artifacts.

### Required Work

1. Create a clean temporary directory under `outputs/p5_cold_unpack_20260509/`.
2. Untar:
   - `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz`
   - `release_artifacts/paper1_provenance_archive_20260509.tar.gz`
3. In the unpacked submission bundle, run:
   - `sha256sum -c SHA256SUMS.txt`
   - `tectonic main.tex`
   - `latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary_main.tex`
   - `tectonic cover_letter.tex`
   - stale-string scans on `.tex`, `.csv`, `.json`, and PDF text
4. Confirm the original `release_artifacts/paper1_submission_bundle_20260509_final/` still contains no build residue after the cold build.
5. Confirm the provenance archive README clearly says the archive is not active claim material.

### Deliverable

`report_md/_gpt/KIMI_P5_TRACK_B_COLD_UNPACK_REPRO_20260509.md`

Must include:

- unpack path;
- file counts;
- SHA result;
- build result;
- any warnings that matter;
- final verdict: PASS / PARTIAL / FAIL.

## Track C — Data Location And Master Status Consolidation

### Goal
Give the user one authoritative map of where all important data lives so data is not lost.

### Required Work

Create or update these files:

1. `report_md/_gpt/PROJECT_MASTER_STATUS_20260509.md`
2. `report_md/_gpt/DATA_LOCATION_INDEX_20260429.md`
3. `report_md/_gpt/REMOTE_105_107_DATA_ACQUISITION_INDEX_20260507.md`

Each index must separate:

- Paper-1 active submission artifacts;
- Paper-1 source data;
- Paper-1 provenance/deprecated data;
- local GPU experiment outputs;
- 105 server cross-architecture/multidataset results;
- 107 server analog KV-cache results;
- GitHub/remote task files;
- files that are safe to delete later vs files that must not be deleted.

### Deliverable

`report_md/_gpt/KIMI_P5_TRACK_C_DATA_LOCATION_AND_STATUS_20260509.md`

Must include a short "if the user asks where X is" lookup table.

## Track D — Remote 105/107 Task Refresh For GitHub/Server Use

### Goal
Prepare a current long task file that can be copied to GitHub or pulled by the 105/107 servers. This is remote-experiment management only.

### Required Work

Create:

`report_md/_gpt/REMOTE_105_107_PHASE_P5_TASKLIST_20260509.md`

It must contain two independent sections.

### 105 Required Section

105 should return, when available:

1. Full seed789 closure for `deit` and `vit` across `digital`, `standard`, `ensemble`, `proportional`.
2. Same-architecture, same-seed proportional-vs-digital comparisons.
3. Exact commands and environment packet.
4. Fresh-eval protocol details: instances, MC repeats, D2D/C2C sampling.
5. One verdict: strong validation / weak validation / inconclusive.
6. Classification: Paper-1 supplement candidate or future-only; never main claim unless Codex accepts.

Kill criteria:

- reject comparisons that mix architecture, seed, split, or source metric definition;
- reject a proportional advantage claim if it is not same-architecture and multi-seed;
- clearly mark server-crash gaps instead of filling missing rows.

### 107 Required Section

107 should return:

1. Corrected-noise rerun report after the reported noise-algorithm bug.
2. Old-vs-corrected comparison table showing which trends survive.
3. Core math/code packet:
   - KV quantization equation;
   - C2C injection point;
   - D2D injection point;
   - retention update equation;
   - seed handling;
   - sliding-window PPL definition;
   - train/test split proof.
4. HAT effectiveness table:
   - pre/post HAT PPL by D2D/C2C setting;
   - 3-seed stability for key settings;
   - selective-layer vs all-layer results.
5. Next minimal experiments:
   - terminal selective layers: last1, last2, last4, all24;
   - high-noise D2D training generalization: train D2D=0.04, eval D2D 0.00--0.05;
   - C2C generalization: train 0.01, eval 0.00--0.02;
   - combined D2D+C2C if time permits.
6. Classification: Work-2 separate paper / appendix pilot / reject.

Kill criteria:

- stop all claims if base+patch PPL is far from clean baseline without an explanation;
- stop all HAT claims if train/test split or sliding-window scoring is ambiguous;
- do not transfer 107 results into Paper-1.

### Deliverable

`report_md/_gpt/KIMI_P5_TRACK_D_REMOTE_TASK_REFRESH_20260509.md`

Must state whether the remote task file is ready for GitHub copy/push.

## Track E — Local GPU And Experiment Governance Queue

### Goal
Do not waste local GPU, but do not contaminate Paper-1. Prepare a queue that can run when GPU is available.

### Required Work

1. Check current GPU status using `nvidia-smi` if available.
2. Identify all runnable local experiment scripts related to:
   - Paper-1 verification only;
   - Work-2 KV-cache exploratory work;
   - 105/107 result ingestion or replay;
   - thesis-only experiments.
3. Build a prioritized queue with exact command placeholders only where code and data exist.
4. If a GPU experiment is safe, short, and clearly future-only, run at most one smoke test and record output.
5. Do not launch long Paper-1-changing training without Codex approval.

### Deliverable

`report_md/_gpt/KIMI_P5_TRACK_E_GPU_AND_EXPERIMENT_QUEUE_20260509.md`

Must include:

- current GPU status;
- candidate tasks;
- command readiness: ready / needs data / needs code / remote-only;
- estimated duration;
- kill criteria.

## Track F — Repo Hygiene And Commit/Push Plan

### Goal
Prepare a safe commit plan without deleting user work or accidentally pushing huge artifacts.

### Required Work

1. Run `git status --short` from `/home/qiaosir/projects`.
2. Classify changed/untracked files into:
   - should commit;
   - should archive locally;
   - should ignore;
   - should not push;
   - needs user decision.
3. Identify whether `release_artifacts/*.tar.gz` should be tracked or excluded.
4. Produce a conservative commit plan. Do not push unless the user explicitly asks.

### Deliverable

`report_md/_gpt/KIMI_P5_TRACK_F_REPO_HYGIENE_PLAN_20260509.md`

## Final Kimi Delivery

Kimi must write:

`report_md/_gpt/KIMI_P5_FINAL_DELIVERY_20260509.md`

It must summarize all tracks A-F and list exact blockers, if any.

## DS Audit After Kimi

DS must write:

`report_md/_gpt/DS_PHASE_P5_AUDIT_20260509.md`

Audit focus:

- no post-audit scientific drift remains;
- cold-unpack reproducibility is real;
- remote tasks are precise enough to execute;
- data-location map is usable;
- repo plan is conservative.

## Mimo Audit After Kimi

Mimo must write:

`report_md/_gpt/MIMO_PHASE_P5_AUDIT_20260509.md`

Audit focus:

- reviewer-facing artifact completeness;
- user-facing data map clarity;
- remote task clarity;
- no hidden claim inflation.

## Success Criteria

P5 is complete only when:

1. Track A confirms no scientific drift between working tree and final bundle, or all drift is documented and fixed.
2. Track B proves the tarball can be unpacked and rebuilt.
3. Track C gives a single authoritative data-location map.
4. Track D produces a ready-to-send 105/107 task file.
5. Track E gives a realistic GPU/experiment queue without contaminating Paper-1.
6. Track F gives a safe commit/push plan.
7. DS and Mimo both audit the final Kimi delivery.

## Stop Conditions

Stop and broadcast immediately if:

- canonical Paper-1 values differ between source data and final PDF;
- the final submission tarball cannot rebuild;
- a remote result implies a Paper-1 claim change;
- a file deletion is needed to proceed;
- a push would include large binary artifacts or user-private material.
