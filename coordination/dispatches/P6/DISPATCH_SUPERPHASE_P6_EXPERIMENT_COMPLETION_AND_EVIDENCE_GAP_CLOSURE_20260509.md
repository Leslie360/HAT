# Dispatch Superphase P6 — Experiment Completion And Evidence Gap Closure

**Date:** 2026-05-09
**Issued by:** Codex
**Mode:** extra-long autonomous package
**Expected duration:** 6-12 hours of Kimi work if local GPU experiments are launched; shorter only if hard blockers are proven

## Executive Decision

Paper-1 is submission-ready and remains frozen. However, the experiment program is not fully saturated. P6 closes evidence gaps, strengthens supplement/defense material, and prepares 105/107 remote closure. Do not alter Paper-1 main claims unless Codex later reopens them.

## Agent Roles

- **Kimi:** primary executor. Run all tracks A-H as one long package; do not stop after a single report.
- **DS:** hostile audit after Kimi delivery: scientific drift, statistical rigor, GPU run validity, remote-task precision.
- **Mimo:** reviewer/defense audit after Kimi delivery: clarity, no claim inflation, no Paper-1 contamination.
- **Gemini:** visual/layout only under direct user instruction; no science edits.
- **Codex:** final acceptance and next experiment decision.

## Core Principle

P6 experiments may strengthen supplement, thesis, defense, or Work-2. They do **not** automatically enter Paper-1 main text.

Classify every result as exactly one of:

- `paper1-main-locked` — already frozen, do not change
- `paper1-supplement-candidate`
- `defense-support`
- `thesis-only`
- `work2-kv-cache`
- `future-only`
- `exclude/superseded`

## Track A — Evidence Gap Ledger

### Goal
Build a claim-to-evidence ledger so we know what is complete and what still needs補.

### Required Work

Create a table with columns:

- claim / narrative point
- current evidence file(s)
- source data file(s)
- number of seeds / instances / MC runs
- metric definition
- status: complete / sufficient / weak / missing / superseded
- next action
- classification

Must cover:

1. IdealDevice 8-bit stable baseline.
2. 4-bit pure quantization collapse.
3. Ensemble HAT 4-bit rescue.
4. PCM 8-bit drift-flat point.
5. PCM 6-bit D2D-sensitive transition zone.
6. PCM 4-bit drift-limited regime.
7. 105 cross-architecture proportional HAT validation.
8. 107 analog KV-cache HAT and selective-layer route.
9. Appendix/defense-only supporting analyses.

### Deliverable

`report_md/_gpt/KIMI_P6_TRACK_A_EVIDENCE_GAP_LEDGER_20260509.md`

## Track B — Local Paper-1 Supplement Gap Closure

### Goal
Close local gaps that are safe and useful without changing main claims.

### Required Work

1. Investigate 6-bit PCM seed123 source-history gap:
   - search for training logs/history/checkpoints;
   - determine whether source_best can be recovered without rerun;
   - if not recoverable, decide whether an exact rerun is possible.
2. If exact config and data exist, launch at most one 6-bit seed123 source rerun on local GPU.
3. If rerun is launched:
   - record exact command;
   - log to `logs/_gpt/p6_6bit_seed123_source_rerun_20260509.log` or equivalent;
   - use early stop if no improvement after 10 epochs beyond best;
   - stop on NaN, source collapse, wrong config, or memory error;
   - return source_best only as `paper1-supplement-candidate` until audited.
4. If rerun is not possible, write a defensible reason and do not fabricate the row.
5. Re-run the PCM precision ladder guard after any local data change.

### Deliverable

`report_md/_gpt/KIMI_P6_TRACK_B_LOCAL_PCM_GAP_CLOSURE_20260509.md`

## Track C — Local GPU Long-Run Queue

### Goal
Use idle GPU for bounded补强, not random exploration.

### Required Work

Check `nvidia-smi`, then construct and execute a safe queue in priority order where code/data are present.

Priority queue:

1. **P6-B optional 6-bit seed123 source rerun** if exact config is available.
2. **Existing-data fresh/drift re-eval smoke** for 4/6/8-bit PCM if checkpoints exist and command is known.
3. **Thesis-only proportional HAT fresh eval** if a ready script/checkpoint exists and does not affect Paper-1.
4. **Work-2 local unit/smoke tests** if 107 code is present locally.

Rules:

- Do not launch more than one long GPU job at a time on the 16GB local card unless memory is proven safe.
- Use tmux or nohup logs if runtime exceeds 30 minutes.
- Add explicit early stop: no improvement for 10 epochs or wrong-metric plateau.
- Every GPU run must have a kill criterion before launch.
- If no safe job exists, write why and do not invent one.

### Deliverable

`report_md/_gpt/KIMI_P6_TRACK_C_LOCAL_GPU_EXECUTION_REPORT_20260509.md`

## Track D — Statistical Completion Pack

### Goal
Convert existing data into stronger statistical support without new training.

### Required Work

Using active source data and remote snapshots where appropriate, compute or tabulate:

1. Mean, std, SEM, and 95% CI for key Paper-1 values.
2. Effect sizes for:
   - IdealDevice 4-bit collapse vs Ensemble HAT rescue;
   - PCM 8-bit vs 6-bit fresh accuracy;
   - PCM 4-bit fresh vs 24h drift loss;
   - standard vs ensemble/proportional where 105 data is complete enough.
3. A robustness statement for each effect:
   - strong / moderate / weak / underpowered.
4. Identify any claim that should be softened due to seed count or missing data.

Do not alter manuscript. This is a decision pack.

### Deliverable

`report_md/_gpt/KIMI_P6_TRACK_D_STATISTICAL_COMPLETION_PACK_20260509.md`

## Track E — Remote 105 Closure Package

### Goal
Make 105's next return immediately useful when the server recovers.

### Required Work

Create or update:

`report_md/_gpt/REMOTE_105_PHASE_P6_CLOSURE_TASKLIST_20260509.md`

105 must run/return:

1. Seed789 closure for all rows that were missing after crash.
2. Same-architecture P vs D per seed:
   - `deit_proportional` vs `deit_digital`
   - `vit_proportional` vs `vit_digital`
3. Mean/std across completed seeds.
4. Source metric definition: best epoch test accuracy only.
5. Fresh protocol proof: 10 instances × 5 MC unless changed, D2D per instance, C2C per forward.
6. Exact commands, git SHA, git status, env.
7. One verdict:
   - supplement candidate if same-arch multi-seed supports proportional advantage;
   - future-only if mixed/incomplete;
   - exclude if source metric or split is wrong.

### Deliverable

`report_md/_gpt/KIMI_P6_TRACK_E_REMOTE105_CLOSURE_PACKAGE_20260509.md`

## Track F — Remote 107 Work-2 Closure Package

### Goal
Make 107's corrected-noise rerun decisive rather than another loose result dump.

### Required Work

Create or update:

`report_md/_gpt/REMOTE_107_PHASE_P6_KV_CLOSURE_TASKLIST_20260509.md`

107 must return:

1. Corrected-noise rerun report:
   - old vs corrected absolute values;
   - trend-preservation verdict;
   - superseded claims list.
2. Core math/code packet:
   - KV quantization equation;
   - conductance mapping;
   - C2C injection;
   - D2D injection;
   - retention equation;
   - seed handling;
   - sliding-window PPL scoring;
   - train/test split proof.
3. HAT effectiveness matrix:
   - D2D, C2C, combined;
   - ctx=512 and ctx=1024 where available;
   - pre-HAT and post-HAT;
   - 3-seed stability for key rows.
4. Selective-layer route:
   - last1, last2, last4, all24;
   - pre/post HAT PPL;
   - terminal-layer deployment verdict.
5. Generalization matrix:
   - train D2D=0.04, eval D2D 0.00--0.05;
   - train C2C=0.01, eval C2C 0.00--0.02;
   - combined if time permits.
6. One Work-2 decision:
   - separate paper / appendix pilot / reject.

### Deliverable

`report_md/_gpt/KIMI_P6_TRACK_F_REMOTE107_KV_CLOSURE_PACKAGE_20260509.md`

## Track G — Repo Hygiene Execution Plan, Not Push

### Goal
Prepare the repository for controlled commit without losing data.

### Required Work

1. Verify whether the 37 `.kimi_draft*` deletions are safe and documented.
2. List any remaining draft/stale files with old numbers.
3. Propose `.gitignore` changes, but do not apply unless safe and reversible.
4. Classify tarballs, release directories, remote snapshots, and report files.
5. Produce an exact commit sequence but do not push.

### Deliverable

`report_md/_gpt/KIMI_P6_TRACK_G_REPO_HYGIENE_EXECUTION_PLAN_20260509.md`

## Track H — Final Experiment Completeness Verdict

### Goal
Answer the user's actual question: are experiments complete, and what still needs补?

### Required Work

Write a verdict with three levels:

1. **Submission-ready completeness:** yes/no and why.
2. **Scientific defense completeness:** yes/no and remaining risk.
3. **Future-paper / Work-2 completeness:** yes/no and next blockers.

Must include:

- what is good enough now;
- what is worth補;
- what is not worth running;
- what should wait for 105/107;
- what local GPU should do next.

### Deliverable

`report_md/_gpt/KIMI_P6_FINAL_EXPERIMENT_COMPLETENESS_VERDICT_20260509.md`

## Final Kimi Delivery

Kimi must write:

`report_md/_gpt/KIMI_P6_FINAL_DELIVERY_20260509.md`

It must summarize Tracks A-H and list all launched GPU jobs, all skipped jobs, and why.

## DS Audit After Kimi

DS must write:

`report_md/_gpt/DS_PHASE_P6_HOSTILE_EXPERIMENT_AUDIT_20260509.md`

Audit focus:

- did Kimi overclaim experimental completeness;
- are GPU runs valid and reproducible;
- are statistics appropriate;
- are 105/107 task lists executable;
- did anything contaminate frozen Paper-1.

## Mimo Audit After Kimi

Mimo must write:

`report_md/_gpt/MIMO_PHASE_P6_DEFENSE_READINESS_AUDIT_20260509.md`

Audit focus:

- can a reviewer understand what is complete vs future-only;
- are classifications clear;
- are gaps honestly stated;
- no hidden main-text claim inflation.

## Success Criteria

P6 is complete when:

1. A claim-to-evidence ledger exists.
2. 6-bit seed123 source gap is recovered, rerun, or honestly marked unrecoverable.
3. Local GPU is either running a justified safe job or has a written blocker.
4. Existing data have CIs/effect-size summaries.
5. 105 and 107 have current closure task files.
6. Repo hygiene plan is actionable but non-destructive.
7. Final experiment completeness verdict directly answers what still needs補.
8. DS and Mimo audits pass.

## Stop Conditions

Stop and broadcast immediately if:

- any run would change frozen Paper-1 main claims;
- exact config for a rerun cannot be recovered;
- a GPU job OOMs twice;
- source data and manuscript disagree;
- 107 corrected-noise rerun invalidates the Work-2 trend;
- 105 result suggests cross-architecture validation is not reliable.
