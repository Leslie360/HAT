#!/usr/bin/env bash
# Pipeline: 5-bit PCM multiseed (seed456 -> seed789)
# Train + fresh eval + drift eval, sequential to avoid GPU OOM
set -euo pipefail

export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:${LD_LIBRARY_PATH:-}
PROJECT=/home/qiaosir/projects/compute_vit
PYTHON=/home/qiaosir/miniconda3/envs/aihwkit/bin/python
TRAIN=$PROJECT/paper2_aihwkit_baseline/train_aihwkit_baseline.py
FRESH=$PROJECT/paper2_aihwkit_baseline/eval_aihwkit_fresh.py
DRIFT=$PROJECT/paper2_aihwkit_baseline/eval_aihwkit_drift.py
LOGDIR=$PROJECT/paper2_aihwkit_baseline/logs
CKPTDIR=$PROJECT/paper2_aihwkit_baseline/checkpoints
mkdir -p "$LOGDIR"

cd "$PROJECT"

run_seed() {
  local SEED=$1
  local RUN="r11d_5bit_pcm_seed${SEED}"
  local OUT="$CKPTDIR/$RUN"
  local TLOG="$LOGDIR/${RUN}_train_$(date +%Y%m%d_%H%M%S).log"
  local FLOG="$LOGDIR/${RUN}_fresh_eval_$(date +%Y%m%d_%H%M%S).log"
  local DLOG="$LOGDIR/${RUN}_drift_eval_$(date +%Y%m%d_%H%M%S).log"

  if [[ -f "$OUT/training_history.json" && -f "$OUT/best.pt" ]]; then
    echo "[pipeline] $RUN already trained; skipping train"
  else
    mkdir -p "$OUT"
    echo "[pipeline] === TRAIN $RUN ===" | tee "$TLOG"
    "$PYTHON" "$TRAIN" \
      --run-id "$RUN" \
      --seed "$SEED" \
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
      2>&1 | tee -a "$TLOG"
    test -f "$OUT/best.pt"
  fi

  if [[ -f "$OUT/fresh_eval.json" ]]; then
    echo "[pipeline] $RUN fresh_eval already exists; skipping"
  else
    echo "[pipeline] === FRESH EVAL $RUN ===" | tee "$FLOG"
    "$PYTHON" "$FRESH" \
      --checkpoint "$OUT/best.pt" \
      --n-fresh 10 \
      --mc-repeats 5 \
      --workers 0 \
      --device cuda \
      --output "$OUT/fresh_eval.json" \
      --inp-res 0.03125 \
      --out-res 0.03125 \
      --modifier-std-dev 0.10 \
      2>&1 | tee -a "$FLOG"
  fi

  if [[ -f "$OUT/drift_eval.json" ]]; then
    echo "[pipeline] $RUN drift_eval already exists; skipping"
  else
    echo "[pipeline] === DRIFT EVAL $RUN ===" | tee "$DLOG"
    "$PYTHON" "$DRIFT" \
      --checkpoint "$OUT/best.pt" \
      --workers 0 \
      --device cuda \
      --output "$OUT/drift_eval.json" \
      --inp-res 0.03125 \
      --out-res 0.03125 \
      --modifier-std-dev 0.10 \
      2>&1 | tee -a "$DLOG"
  fi

  echo "[pipeline] $RUN complete"
}

run_seed 456
run_seed 789

echo "[pipeline] ALL DONE"
