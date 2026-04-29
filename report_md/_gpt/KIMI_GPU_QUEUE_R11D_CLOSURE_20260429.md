# Kimi GPU Queue — R11D PCM Closure

**Date:** 2026-04-29  
**Owner:** Kimi GPU scheduler  
**Coordinator:** Codex  
**Scope:** Local R11D AIHWKit/PCM closure only. Do not duplicate Remote 105 multi-dataset or Remote 107 KV-cache tasks.

## 1. Current Verified State

Local GPU is free at Codex check time: RTX 5070 Ti, ~331 MB used, 0% util, no active Python training process.

Corrected source/test results now available:

| Run | Seed | Config | Best test | Final test | Status |
|---|---:|---|---:|---:|---|
| R11D-7 | 123 | 4-bit PCM, `inp_res=out_res=0.0625` | 76.74% | 76.33% | valid |
| R11D-7 | 456 | 4-bit PCM, clean rerun | 77.15% | 76.86% | valid |
| R11D-5a | 123 | 8-bit PCM, `inp_res=out_res=1/256` | 77.00% | 77.00% | valid |
| R11D-5a | 456 | 8-bit PCM | 78.36% | 77.98% | valid |

Two-seed source summaries:

| Config | Mean best test | Sample std | Interpretation |
|---|---:|---:|---|
| 4-bit PCM | 76.95% | 0.29 pp | stable, matches prior seed42 |
| 8-bit PCM | 77.68% | 0.96 pp | slightly higher, still needs seed789 |

Invalid data exclusion remains active:

- Do not use `r11d_7_pcm_4bit_seed456_PARTIAL_PIPEFAIL_BUG_20260429_100717`.
- Do not use killed T1-3 `PCMPresetDevice_seed42` artifacts.
- Do not use T1-4 oracle in paper-facing tables unless rerun under locked provenance.

## 2. Immediate GPU Priority

### P0 — Fresh Eval For Corrected Multi-Seed Checkpoints

Run first. These are short and required before any new long training.

Use `n_fresh=10`, `mc_repeats=5`, `workers=0`.

```bash
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH
PYTHON=/home/qiaosir/miniconda3/envs/aihwkit/bin/python
cd /home/qiaosir/projects/compute_vit
mkdir -p paper2_aihwkit_baseline/logs

for RUN in \
  r11d_7_pcm_4bit_seed123 \
  r11d_7_pcm_4bit_seed456_clean \
  r11d_5a_pcm_seed123 \
  r11d_5a_pcm_seed456; do
  echo "=== Fresh eval: $RUN ==="
  $PYTHON paper2_aihwkit_baseline/eval_aihwkit_fresh.py \
    --checkpoint "paper2_aihwkit_baseline/checkpoints/${RUN}/best.pt" \
    --n-fresh 10 \
    --mc-repeats 5 \
    --batch-size 64 \
    --workers 0 \
    --device cuda \
    --output "paper2_aihwkit_baseline/checkpoints/${RUN}/fresh_eval.json" \
    2>&1 | tee "paper2_aihwkit_baseline/logs/${RUN}_fresh_eval_$(date +%Y%m%d_%H%M%S).log"
  test -f "paper2_aihwkit_baseline/checkpoints/${RUN}/fresh_eval.json"
done
```

Kill criteria:

- If `tile_audit_all_enabled` is false, stop and report.
- If any eval crashes twice, stop and preserve logs.
- Do not silently lower `n_fresh` or `mc_repeats`.

### P1 — Minimal Drift Eval For Corrected Multi-Seed Checkpoints

Run after P0. Use compact time points first: 0, 1h, 24h.

```bash
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH
PYTHON=/home/qiaosir/miniconda3/envs/aihwkit/bin/python
cd /home/qiaosir/projects/compute_vit
mkdir -p paper2_aihwkit_baseline/logs

for RUN in \
  r11d_7_pcm_4bit_seed123 \
  r11d_7_pcm_4bit_seed456_clean \
  r11d_5a_pcm_seed123 \
  r11d_5a_pcm_seed456; do
  echo "=== Drift eval: $RUN ==="
  $PYTHON paper2_aihwkit_baseline/eval_aihwkit_drift_extended.py \
    --checkpoint "paper2_aihwkit_baseline/checkpoints/${RUN}/best.pt" \
    --batch-size 64 \
    --workers 0 \
    --device cuda \
    --drift-times 0 3600 86400 \
    --output "paper2_aihwkit_baseline/checkpoints/${RUN}/drift_eval.json" \
    2>&1 | tee "paper2_aihwkit_baseline/logs/${RUN}_drift_eval_$(date +%Y%m%d_%H%M%S).log"
  test -f "paper2_aihwkit_baseline/checkpoints/${RUN}/drift_eval.json"
done
```

Kill criteria:

- If script reports non-PCM / skipped for these checkpoints, stop. These should be PCM checkpoints.
- If 0s drift eval differs from best test by a large margin, report before continuing.

## 3. Second GPU Priority

### P2 — Add Seed 789 For Paper-Facing 3-Seed Statistics

Only start after P0 and P1 finish and the 2-seed fresh/drift table is summarized.

Run two trainings sequentially on the local single GPU. Do not run in parallel locally.

4-bit PCM seed789:

```bash
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH
PYTHON=/home/qiaosir/miniconda3/envs/aihwkit/bin/python
cd /home/qiaosir/projects/compute_vit
RUN=r11d_7_pcm_4bit_seed789
mkdir -p "paper2_aihwkit_baseline/checkpoints/${RUN}" paper2_aihwkit_baseline/logs
$PYTHON paper2_aihwkit_baseline/r11d4_train_pcm.py \
  --run-id "$RUN" \
  --seed 789 \
  --epochs 100 \
  --batch-size 64 \
  --lr 0.001 \
  --wd 0.05 \
  --momentum 0.0 \
  --device cuda \
  --workers 0 \
  --save-dir "paper2_aihwkit_baseline/checkpoints/${RUN}" \
  --log-interval 1 \
  --inp-res 0.0625 \
  --out-res 0.0625 \
  --modifier-std-dev 0.10 \
  --early-stop-patience 0 \
  2>&1 | tee "paper2_aihwkit_baseline/logs/${RUN}_$(date +%Y%m%d_%H%M%S).log"
test -f "paper2_aihwkit_baseline/checkpoints/${RUN}/training_history.json"
test -f "paper2_aihwkit_baseline/checkpoints/${RUN}/last.pt"
```

8-bit PCM seed789:

```bash
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH
PYTHON=/home/qiaosir/miniconda3/envs/aihwkit/bin/python
cd /home/qiaosir/projects/compute_vit
RUN=r11d_5a_pcm_seed789
mkdir -p "paper2_aihwkit_baseline/checkpoints/${RUN}" paper2_aihwkit_baseline/logs
$PYTHON paper2_aihwkit_baseline/r11d4_train_pcm.py \
  --run-id "$RUN" \
  --seed 789 \
  --epochs 100 \
  --batch-size 64 \
  --lr 0.001 \
  --wd 0.05 \
  --momentum 0.0 \
  --device cuda \
  --workers 0 \
  --save-dir "paper2_aihwkit_baseline/checkpoints/${RUN}" \
  --log-interval 1 \
  --inp-res 0.00390625 \
  --out-res 0.00390625 \
  --modifier-std-dev 0.10 \
  --early-stop-patience 0 \
  2>&1 | tee "paper2_aihwkit_baseline/logs/${RUN}_$(date +%Y%m%d_%H%M%S).log"
test -f "paper2_aihwkit_baseline/checkpoints/${RUN}/training_history.json"
test -f "paper2_aihwkit_baseline/checkpoints/${RUN}/last.pt"
```

After each seed789 training, immediately run P0 fresh eval and P1 drift eval for that run.

Why no early stop: current corrected PCM runs peak late (`seed123` best epoch 97; `seed456` best epoch 97). Early stopping at patience 10 would likely bias the canonical comparison.

## 4. Third Priority / Hold

Do not run these until P0/P1/P2 close:

1. T1-3 PCMPresetDevice comparison. It was previously invalid due wrong cwd/batch/provenance. Only rerun after multi-seed PCM closure, using the fixed `run_pcm_preset_comparison.sh`.
2. Progressive quantization (`R11D11`). Current 8-bit progressive result is poor: best test 44.43%, so it is not on the critical path.
3. Oracle/no-modifier reruns. Diagnostic only unless Claude explicitly asks for a clean provenance rerun.
4. Any 105 architecture/multi-dataset jobs. Remote 105 owns those.
5. Any 107 KV-cache jobs. Remote 107 owns those.

## 5. Required Kimi Return Summary

After P0/P1, return:

```text
run_id, seed, bit_config, best_test, final_test, fresh_mean, fresh_std, drift_0s, drift_1h, drift_24h, status
```

After P2, return 3-seed mean/std for:

```text
4-bit PCM source best, 4-bit PCM fresh, 4-bit PCM drift_24h
8-bit PCM source best, 8-bit PCM fresh, 8-bit PCM drift_24h
```

## 6. Current Decision Target

We need decide whether the paper-facing R11D claim is:

1. **4-bit PCM is already stable and close to 8-bit**, if 3-seed 4-bit source/fresh remains within ~1 pp of 8-bit.
2. **8-bit PCM remains the safer headline**, if 8-bit has materially better mean/stability.
3. **modifier noise is essential regularization**, supported by the oracle diagnostic drop, but only as supplementary unless clean oracle rerun is requested.
