#!/bin/bash
# Progressive Quantization Pipeline (8-bit -> 6-bit -> 4-bit PCM)
# Purpose: Smoother 4-bit convergence via curriculum learning

set -e
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH
PYTHON=/home/qiaosir/miniconda3/envs/aihwkit/bin/python
TRAIN="/home/qiaosir/projects/compute_vit/paper2_aihwkit_baseline/r11d11_train_progressive.py"
LOG_DIR="/home/qiaosir/projects/compute_vit/paper2_aihwkit_baseline/logs"
CKPT_DIR="/home/qiaosir/projects/compute_vit/paper2_aihwkit_baseline/checkpoints"

mkdir -p "$LOG_DIR" "$CKPT_DIR"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# --- Phase 1: 8-bit PCM (Epoch 1-30) ---
RUN_8BIT="r11d11_prog_8bit"
log "=== Phase 1: 8-bit PCM ==="
$PYTHON "$TRAIN" \
    --run-id "$RUN_8BIT" \
    --epochs 30 \
    --batch-size 128 \
    --lr 0.001 \
    --wd 0.05 \
    --device cuda \
    --inp-res 0.00390625 \
    --out-res 0.00390625 \
    --modifier-std-dev 0.10 \
    --save-dir "$CKPT_DIR/$RUN_8BIT" \
    2>&1 | tee "$LOG_DIR/${RUN_8BIT}_$(date +%Y%m%d_%H%M%S).log"

# --- Phase 2: 6-bit PCM (Epoch 31-60) ---
RUN_6BIT="r11d11_prog_6bit"
log "=== Phase 2: 6-bit PCM ==="
$PYTHON "$TRAIN" \
    --run-id "$RUN_6BIT" \
    --epochs 30 \
    --batch-size 128 \
    --lr 0.0005 \
    --wd 0.05 \
    --device cuda \
    --inp-res 0.015625 \
    --out-res 0.015625 \
    --modifier-std-dev 0.10 \
    --save-dir "$CKPT_DIR/$RUN_6BIT" \
    --resume "$CKPT_DIR/$RUN_8BIT/last.pt" \
    2>&1 | tee "$LOG_DIR/${RUN_6BIT}_$(date +%Y%m%d_%H%M%S).log"

# --- Phase 3: 4-bit PCM (Epoch 61-100) ---
RUN_4BIT="r11d11_prog_4bit"
log "=== Phase 3: 4-bit PCM ==="
$PYTHON "$TRAIN" \
    --run-id "$RUN_4BIT" \
    --epochs 40 \
    --batch-size 128 \
    --lr 0.0001 \
    --wd 0.05 \
    --device cuda \
    --inp-res 0.0625 \
    --out-res 0.0625 \
    --modifier-std-dev 0.10 \
    --save-dir "$CKPT_DIR/$RUN_4BIT" \
    --resume "$CKPT_DIR/$RUN_6BIT/last.pt" \
    2>&1 | tee "$LOG_DIR/${RUN_4BIT}_$(date +%Y%m%d_%H%M%S).log"

log "=== Progressive Quantization Pipeline Complete ==="
