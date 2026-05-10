# DISPATCH — Kimi GPU Queue 2026-05-08

Date: 2026-05-08
Owner: Kimi
Coordinator: Codex
Reviewers: DS + Mimo
Resource observed by Codex: local RTX 5070 Ti 16GB, idle enough to run jobs now.

## 0. Ruling

GPU should run now, but only on jobs that can change a decision. The immediate queue is:

1. Close the contaminated 5-bit PCM question.
2. Then settle the 6-bit seed456 instability if GPU remains idle.
3. Do not launch new broad R11D branches until these two are closed.

Remote 107 remains the high-upside KV-cache line. Local GPU should focus on PCM precision/provenance closure.

## 1. Critical Warning: Old 5-bit Pipeline Is Invalid For seed456/789

Do not use `paper2_aihwkit_baseline/pipeline_5bit_pcm_multiseed.sh` as-is.

The script sets:

```bash
TRAIN=$PROJECT/paper2_aihwkit_baseline/train_aihwkit_baseline.py
```

So seed456 and seed789 were trained by the baseline script, not the strict PCM script. Their logs start with `R10E AIHWKit Baseline`, and their drift JSONs were skipped with `pcm_preset=None`.

Conclusion:

- old seed123 is only a pilot/reference;
- old seed456/789 are not valid PCM evidence;
- corrected 5-bit runs must use `r11d4_train_pcm_extended.py --pcm-preset PCMPresetUnitCell`.

## 2. Global Execution Rules

- Run one training job at a time on the local 5070 Ti.
- Eval immediately after each training run.
- Use new output directories; never overwrite old contaminated checkpoints.
- Record exact command, git SHA, git status, checkpoint path, log path, fresh JSON, drift JSON.
- Use early stop: `--early-stop-patience 10 --early-stop-min-delta 0.05`.
- If a run cannot produce physically meaningful drift JSON, stop that line and report.

## 3. P0 — Strict 5-bit PCM Gate

### Question

Is 5-bit PCM a real intermediate point, or was the previous result pipeline contamination?

### P0-A: Run strict seed123 first

Expected time: about 1.5 GPU-hour including eval.

```bash
cd /home/qiaosir/projects/compute_vit
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:${LD_LIBRARY_PATH:-}
PY=/home/qiaosir/miniconda3/envs/aihwkit/bin/python
RUN=r11d_5bit_pcm_strict_seed123_20260508
OUT=paper2_aihwkit_baseline/checkpoints/${RUN}
mkdir -p "$OUT" paper2_aihwkit_baseline/logs

$PY paper2_aihwkit_baseline/r11d4_train_pcm_extended.py \
  --run-id "$RUN" \
  --seed 123 \
  --epochs 100 \
  --batch-size 128 \
  --lr 0.001 \
  --wd 0.05 \
  --device cuda \
  --workers 0 \
  --save-dir "$OUT" \
  --log-interval 1 \
  --inp-res 0.03125 \
  --out-res 0.03125 \
  --modifier-std-dev 0.10 \
  --pcm-preset PCMPresetUnitCell \
  --early-stop-patience 10 \
  --early-stop-min-delta 0.05 \
  2>&1 | tee paper2_aihwkit_baseline/logs/${RUN}_train.log

$PY paper2_aihwkit_baseline/eval_aihwkit_fresh.py \
  --checkpoint "$OUT/best.pt" \
  --n-fresh 10 \
  --mc-repeats 5 \
  --workers 0 \
  --device cuda \
  --output "$OUT/fresh_eval.json" \
  --inp-res 0.03125 \
  --out-res 0.03125 \
  --modifier-std-dev 0.10 \
  2>&1 | tee paper2_aihwkit_baseline/logs/${RUN}_fresh_eval.log

$PY paper2_aihwkit_baseline/eval_aihwkit_drift_extended.py \
  --checkpoint "$OUT/best.pt" \
  --workers 0 \
  --device cuda \
  --output "$OUT/drift_eval.json" \
  --inp-res 0.03125 \
  --out-res 0.03125 \
  --modifier-std-dev 0.10 \
  --drift-times 0 3600 86400 \
  2>&1 | tee paper2_aihwkit_baseline/logs/${RUN}_drift_eval.log
```

### P0-A kill/continue

After seed123:

- If `pcm_preset_used` is missing or not `PCMPresetUnitCell`, stop and send to DS/Codex.
- If `drift_eval.json` contains `skipped=true`, stop and send to DS/Codex.
- If best test is below 70%, do not run 5-bit seed456/789 yet. Report 5-bit as likely non-frontier and ask Codex whether to kill.
- If best test is at least 70% and drift eval is valid, continue to P0-B.

### P0-B: Expand only if P0-A passes

Run seed456 and seed789 using the exact same command, changing only:

```bash
SEED=456
RUN=r11d_5bit_pcm_strict_seed456_20260508
```

and then:

```bash
SEED=789
RUN=r11d_5bit_pcm_strict_seed789_20260508
```

Required output:

- `report_md/_gpt/KIMI_GPU_5BIT_PCM_STRICT_RESULT_20260508.md`

Required verdict:

- `LOCK`: 5-bit is clean and should enter precision-frontier table.
- `KILL`: 5-bit remains poor or drift/provenance invalid.
- `PROVISIONAL`: mixed seeds, needs Codex arbitration.

## 4. P1 — 6-bit seed456 Strict Settlement

Run only after P0 is closed or paused.

### Question

Is the old 6-bit seed456 failure a seed instability or another provenance/script issue?

Use strict PCM extended script and a new output directory.

```bash
cd /home/qiaosir/projects/compute_vit
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:${LD_LIBRARY_PATH:-}
PY=/home/qiaosir/miniconda3/envs/aihwkit/bin/python
RUN=r11d_6bit_pcm_strict_seed456_20260508
OUT=paper2_aihwkit_baseline/checkpoints/${RUN}
mkdir -p "$OUT" paper2_aihwkit_baseline/logs

$PY paper2_aihwkit_baseline/r11d4_train_pcm_extended.py \
  --run-id "$RUN" \
  --seed 456 \
  --epochs 100 \
  --batch-size 128 \
  --lr 0.001 \
  --wd 0.05 \
  --device cuda \
  --workers 0 \
  --save-dir "$OUT" \
  --log-interval 1 \
  --inp-res 0.015625 \
  --out-res 0.015625 \
  --modifier-std-dev 0.10 \
  --pcm-preset PCMPresetUnitCell \
  --early-stop-patience 10 \
  --early-stop-min-delta 0.05 \
  2>&1 | tee paper2_aihwkit_baseline/logs/${RUN}_train.log

$PY paper2_aihwkit_baseline/eval_aihwkit_fresh.py \
  --checkpoint "$OUT/best.pt" \
  --n-fresh 10 \
  --mc-repeats 5 \
  --workers 0 \
  --device cuda \
  --output "$OUT/fresh_eval.json" \
  --inp-res 0.015625 \
  --out-res 0.015625 \
  --modifier-std-dev 0.10 \
  2>&1 | tee paper2_aihwkit_baseline/logs/${RUN}_fresh_eval.log

$PY paper2_aihwkit_baseline/eval_aihwkit_drift_extended.py \
  --checkpoint "$OUT/best.pt" \
  --workers 0 \
  --device cuda \
  --output "$OUT/drift_eval.json" \
  --inp-res 0.015625 \
  --out-res 0.015625 \
  --modifier-std-dev 0.10 \
  --drift-times 0 3600 86400 \
  2>&1 | tee paper2_aihwkit_baseline/logs/${RUN}_drift_eval.log
```

Kill/continue:

- If best test is below 70%, report 6-bit as unstable; do not rerun more seeds.
- If best test is at least 74% and drift drop is near 8-bit, update the 6-bit table as stable but not a unique sweet point.
- If drift eval skips, stop and send to DS/Codex.

Required output:

- `report_md/_gpt/KIMI_GPU_6BIT_SEED456_STRICT_RESULT_20260508.md`

## 5. P2 — Eval-Only Canonical Recheck

Run only if P0/P1 finish and GPU remains idle.

Purpose: no new science; just prove locked 4-bit/8-bit checkpoints still eval under current code.

Targets:

- `r11d_7_pcm_4bit_seed123`
- `r11d_7_pcm_4bit_seed456_clean`
- `r11d_7_pcm_4bit_seed789`
- `r11d_5a_pcm_seed123`
- `r11d_5a_pcm_seed456`
- `r11d_5a_pcm_seed789`

Run fresh + drift eval only. Do not retrain.

Required output:

- `report_md/_gpt/KIMI_GPU_CANONICAL_4BIT_8BIT_REEVAL_20260508.md`

Kill/continue:

- If eval differs by more than 0.5 pp from locked numbers, pause and send to DS/Codex.
- If all match, mark Paper-1 PCM frontier eval path as reproducible.

## 6. Remote GPU Notes

### 107

107 should continue `REMOTE107_NEXT_TASKS_20260507B.md`:

- baseline reconciliation;
- paired HAT checkpoint ablations;
- train metadata export;
- EPSC proxy stress;
- optional Pythia-1B only after P0/P1.

Kimi should not duplicate 107 locally.

### 105

When 105 returns, run only the minimal seed789 block first:

- deit digital seed789;
- deit proportional seed789;
- vit digital seed789;
- vit proportional seed789.

Do not expand ensemble/standard until those four are reviewed.

## 7. Reporting Format

Every Kimi GPU report must start with:

| Task | Status | GPU hours | Best/source | Fresh | Drift 1d | Verdict |
|---|---:|---:|---:|---:|---:|---|

Then include:

1. exact commands;
2. git SHA and git status summary;
3. checkpoint paths;
4. log paths;
5. JSON paths;
6. metadata audit: `pcm_preset_used`, `inp_res`, `out_res`, `modifier_std_dev`;
7. kill/continue decision;
8. one-sentence paper impact.

## 8. DS/Mimo Review Assignment

DS reviews:

- whether corrected 5-bit/6-bit scripts are truly PCM;
- whether drift eval is physically meaningful;
- whether current metrics match locked tables.

Mimo reviews:

- whether the narrative should say `5-bit killed`, `5-bit exploratory`, or `5-bit enters frontier`;
- whether 6-bit should be described as unstable, redundant with 8-bit, or a useful transition point.

## 9. Codex Position

Start P0-A immediately. It is short and decision-critical. If P0-A fails, do not spend more GPU on 5-bit until Codex reviews the failure. If P0-A passes, finish 5-bit 3-seed. Then run P1 seed456 strict 6-bit once.
