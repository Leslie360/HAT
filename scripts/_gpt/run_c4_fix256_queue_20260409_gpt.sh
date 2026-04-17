#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
PY="/home/qiaosir/miniconda3/envs/LLM/bin/python"
LOG_DIR="$ROOT/logs/_gpt/multi_seed"
SAVE_ROOT="$ROOT/checkpoints/_gpt/multi_seed_fix256"
DRIVER_LOG="$ROOT/logs/_gpt/c4_fix256_queue_20260409.log"

mkdir -p "$LOG_DIR" "$SAVE_ROOT"

{
  echo "============================================================"
  echo "[$(date '+%F %T')] Starting C4-fix-v2 queue (BS=256, AMP=off)"
  echo "ROOT=$ROOT"
  echo "SAVE_ROOT=$SAVE_ROOT"
  echo "LOG_DIR=$LOG_DIR"
} | tee -a "$DRIVER_LOG"

cd "$ROOT"

for SEED in 42 123 2026; do
  SAVE_DIR="$SAVE_ROOT/C4_fix256_s${SEED}"
  TRAIN_LOG="$LOG_DIR/multi_seed_C4_fix256_s${SEED}.log"
  EVAL_LOG="$LOG_DIR/multi_seed_C4_fix256_s${SEED}_eval.log"
  CKPT="$SAVE_DIR/C4_4bit_noise_HAT_best.pt"

  mkdir -p "$SAVE_DIR"

  {
    echo "------------------------------------------------------------"
    echo "[$(date '+%F %T')] TRAIN start: C4 seed=${SEED}"
    echo "save_dir=$SAVE_DIR"
    echo "train_log=$TRAIN_LOG"
  } | tee -a "$DRIVER_LOG"

  "$PY" -u train_convnext.py \
    --dataset cifar10 \
    --seed "$SEED" \
    --batch-size 256 \
    --save-dir "$SAVE_DIR" \
    --mode train \
    --experiments C4 \
    --num-workers 4 \
    2>&1 | tee "$TRAIN_LOG"

  {
    echo "[$(date '+%F %T')] TRAIN end: C4 seed=${SEED}"
    echo "checkpoint=$CKPT"
  } | tee -a "$DRIVER_LOG"

  if [[ ! -f "$CKPT" ]]; then
    echo "[$(date '+%F %T')] Missing checkpoint after train: $CKPT" | tee -a "$DRIVER_LOG"
    exit 1
  fi

  {
    echo "[$(date '+%F %T')] EVAL start: C4 seed=${SEED}"
    echo "eval_log=$EVAL_LOG"
  } | tee -a "$DRIVER_LOG"

  "$PY" -u train_convnext.py \
    --dataset cifar10 \
    --seed "$SEED" \
    --batch-size 256 \
    --checkpoint "$CKPT" \
    --eval-runs 10 \
    --mode eval \
    --experiments C4 \
    2>&1 | tee "$EVAL_LOG"

  echo "[$(date '+%F %T')] EVAL end: C4 seed=${SEED}" | tee -a "$DRIVER_LOG"
done

echo "[$(date '+%F %T')] C4-fix-v2 queue finished successfully." | tee -a "$DRIVER_LOG"
