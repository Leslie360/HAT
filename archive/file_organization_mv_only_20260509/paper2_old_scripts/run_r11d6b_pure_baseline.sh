#!/bin/bash
set -e
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH

CKPT_DIR="paper2_aihwkit_baseline/checkpoints/r11d_6b_pure_baseline"
LOG="paper2_aihwkit_baseline/logs/r11d_6b_pure_baseline_$(date +%Y%m%d_%H%M%S).log"
mkdir -p "$CKPT_DIR" paper2_aihwkit_baseline/logs

echo "=== R11D-6b: 8-bit Pure Baseline (negligible modifier 1e-4) ===" | tee "$LOG"
/home/qiaosir/miniconda3/envs/aihwkit/bin/python \
    paper2_aihwkit_baseline/train_aihwkit_baseline.py \
    --run-id r11d_6b_pure_baseline \
    --seed 42 \
    --epochs 100 \
    --batch-size 64 \
    --lr 0.001 \
    --wd 0.05 \
    --workers 0 \
    --device cuda \
    --save-dir "$CKPT_DIR" \
    --log-interval 1 \
    --inp-res 0.00390625 \
    --out-res 0.00390625 \
    --modifier-std-dev 0.0001 \
    --early-stop-patience 20 \
    2>&1 | tee -a "$LOG"

echo "=== R11D-6b training complete ==="
