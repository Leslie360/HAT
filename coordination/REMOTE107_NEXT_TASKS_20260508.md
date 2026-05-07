# Remote107 Next Tasks — Post `d8e3b17` Lock

Date: 2026-05-08  
From: Codex coordinator  
To: Remote107 agent  
Branch: `107-clean`  
Current head when issued: `d8e3b17`

## 0. Situation

Your latest push is received and reviewed. The following items are now treated as **locked unless you find a hard bug**:

- K107 canonical raw digital baseline: `22.18 PPL` under `ctx=512, stride=256, batch=1`.
- Old `15.62/15.68` baseline is deprecated for K107 comparisons because it used `1024/512/batch=8`.
- P0-B paired ablation means:
  - B1 HAT checkpoint digital/no patch: `19.0430`
  - B2 patch/no noise: `19.0597`
  - B3 D2D=0.02: `19.4829`
  - B4 D2D=0.05: `19.6437`
- Canonical HAT fine-tuning gain: `22.18 -> 19.04`, about `3.1 PPL`.
- EPSC central proxy `C2C=0.10, D2D=0.10`: max `20.2306 < 25`, PASS.
- Pythia-1B and 2.8B terminal-layer analog KV scale checks are locked:
  - 1B D2D=0.02 mean `14.6021`, D2D=0.05 mean `14.8193`.
  - 2.8B D2D=0.02 mean `13.3345`, D2D=0.05 mean `13.4307`.

Do **not** rerun P0/P1/P2/P3 unless you identify a reproducibility-breaking bug.

## 1. Hard Rules

1. Do not mix evaluator protocols. Every table must state `ctx_len`, `stride`, `batch_size`.
2. Do not cite `15.62/15.68` as K107 baseline except in a baseline-reconciliation note.
3. Do not push checkpoints or large weights.
4. Push only code, JSON/CSV summaries, logs small enough for GitHub, and coordination MD.
5. Every new result must include exact command, git SHA, environment, checkpoint source, and JSON path.
6. If a task is expected to exceed 8 GPU-hours, first write a short plan/estimate MD and stop.

## 2. P0 — Data Freeze Package, No GPU Required

### Task 107-P0-FREEZE

Create a single canonical frozen data packet for K107.

Required output files:

- `coordination/REMOTE107_K107_CANONICAL_FREEZE_20260508.md`
- `deliverable/results_v3/k107_canonical_summary.csv`
- `deliverable/results_v3/k107_plot_ready.json`

The freeze MD must contain these sections:

1. Baseline reconciliation table: current 22.18 vs old 15.62, with evaluator parameters.
2. P0-B paired ablation table: B1/B2/B3/B4 means, std, n, min, max.
3. EPSC stress table: e1-e5 mean, std, max, kill-margin vs 25 PPL.
4. Scale table: 410M/1B/2.8B, D2D=0.02 and 0.05, mean/std/n.
5. Metadata completeness table: train_meta, hat_config, eval JSON, command, git SHA.
6. One paragraph: what is locked, what is deprecated, what remains speculative.

Acceptance criteria:

- One command or script can regenerate `k107_canonical_summary.csv` from committed JSON/CSV files.
- No manual arithmetic without a script or reproducible snippet.
- The numbers must match Codex review:
  - B1 mean `19.0430`
  - B2 mean `19.0597`
  - B3 mean `19.4829`
  - B4 mean `19.6437`
  - EPSC-e2 max `20.2306`
  - 1B D2D=0.02 mean `14.6021`
  - 2.8B D2D=0.02 mean `13.3345`

## 3. P1 — Figure-Ready Scripts, No New Training

### Task 107-P1-FIGDATA

Create plot data and minimal plotting scripts for three future Paper-2/KV figures.

Required files:

- `scripts/plot_k107_ablation.py`
- `scripts/plot_k107_epsc_stress.py`
- `scripts/plot_k107_scale_trend.py`
- output PDFs/PNGs under `deliverable/figures/`

Figure intent:

1. **Paired ablation ladder:** raw digital baseline 22.18 -> HAT digital/no patch 19.04 -> patch/no-noise 19.06 -> D2D=0.02 19.48 -> D2D=0.05 19.64.
2. **EPSC stress:** e1-e5 mean/max with horizontal kill line at 25 PPL.
3. **Scale trend:** Pythia-410M / 1B / 2.8B at D2D=0.02 and 0.05.

Style requirements:

- Use vector PDF plus PNG preview.
- Label evaluator protocol in caption or subtitle.
- Do not overclaim. Use wording: “selective terminal-layer analog KV” and “under K107 evaluator”.

Acceptance criteria:

- Scripts run without GPU.
- Scripts read committed CSV/JSON, not hardcoded values, except for annotation labels.
- Figures are draft-quality for internal review, not final manuscript polish.

## 4. P2 — Method/Code Audit for Selective Optimizer

### Task 107-P2-OPTIMIZER-AUDIT

The Pythia-2.8B run used selective optimizer to avoid OOM. Audit and document exactly what was trainable.

Required output:

- `coordination/REMOTE107_SELECTIVE_OPTIMIZER_AUDIT_20260508.md`

Must answer:

1. Which parameters are optimized for last1 analog KV training?
2. Are non-target layers frozen or merely absent from optimizer?
3. Does `requires_grad` remain true for non-optimized params? If yes, is memory wasted by gradients?
4. Does the fallback to full-model optimizer ever trigger in current scripts?
5. For Pythia-410M/1B/2.8B, list trainable parameter count and total parameter count.
6. Does selective optimizer change the scientific claim compared with full-model HAT?

If you can safely improve the code without changing results:

- Add a `--freeze-non-target-params` option or make selective mode explicitly set `requires_grad=False` outside target layers.
- Do not rerun all experiments unless the audit shows the old optimizer materially changed behavior.

Acceptance criteria:

- Report includes exact parameter counts.
- Report includes a recommendation: keep current results / rerun only metadata / rerun affected scale checks.

## 5. P3 — Optional GPU: 6.9B Feasibility Probe Only If Cheap

### Task 107-P3-6P9B-FEASIBILITY

This is optional. Do not start if it blocks more important cleanup.

Goal: determine whether a Pythia-6.9B last1 analog-KV check is feasible on your hardware with the selective optimizer.

Phase A: no-training dry run

- Load model if available locally.
- Patch only last layer.
- Run a tiny eval smoke on a very small token subset.
- Record VRAM, wall time, and whether OOM occurs.

Phase B: only if Phase A succeeds comfortably

- Run max 20-step HAT smoke, not full 100-step.
- Eval D2D=0.02 on one eval seed.

Stop criteria:

- Any OOM.
- Estimated full run > 8 GPU-hours.
- Requires downloading new model/data.

Required output:

- `coordination/REMOTE107_P3_6P9B_FEASIBILITY_20260508.md`

Acceptance criteria:

- This is a feasibility note only. Do not claim 6.9B validation unless full seed/eval protocol is later completed.

## 6. P4 — No Further Retention Runs Unless a Gap Is Identified

K107-B retention is already complete per your earlier return. Do not rerun retention unless the P0 freeze discovers missing metadata or inconsistent evaluator parameters.

If a gap exists, write `coordination/REMOTE107_RETENTION_GAP_NOTE_20260508.md` first and wait.

## 7. Return Format

For each completed task, push one return file:

- `coordination/REMOTE107_<TASK>_RETURN_20260508.md`

Each return must start with:

| Task | Status | GPU-hours | Changed locked claim? | Verdict |
|---|---:|---:|---:|---|

Then include:

1. exact commands
2. git SHA
3. environment
4. input files
5. output files
6. numeric tables
7. failure/kill criteria if applicable
8. one-sentence recommendation for Codex/Kimi/Gemini

## 8. Priority Order

Execute in this order:

1. `107-P0-FREEZE` — required, no GPU.
2. `107-P1-FIGDATA` — required, no GPU.
3. `107-P2-OPTIMIZER-AUDIT` — required, mostly no GPU.
4. `107-P3-6P9B-FEASIBILITY` — optional GPU only if cheap.
5. `107-P4` retention gap note — only if P0 finds a gap.

## 9. Coordinator Ruling

The current K107 story is strong enough. The next risk is not lack of more runs; it is inconsistent baselines and unclear provenance. Freeze the data, make plot-ready summaries, audit the selective optimizer, and only then consider a 6.9B feasibility probe.
