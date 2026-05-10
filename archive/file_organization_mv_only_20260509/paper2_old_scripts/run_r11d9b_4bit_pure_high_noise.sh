#!/bin/bash
# R11D-9b: 4-bit pure baseline with HIGH noise (modifier_std_dev=0.01)
# Purpose: Prove that generic Gaussian noise cannot rescue 4-bit pure quantization.

set -e
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH

CKPT_DIR="paper2_aihwkit_baseline/checkpoints/r11d_9b_4bit_pure_high_noise"
LOG="paper2_aihwkit_baseline/logs/r11d_9b_4bit_pure_high_noise_$(date +%Y%m%d_%H%M%S).log"
mkdir -p "$CKPT_DIR" paper2_aihwkit_baseline/logs

echo "=== R11D-9b: 4-bit Pure + High Noise (mod=0.01) ===" | tee "$LOG"

/home/qiaosir/miniconda3/envs/aihwkit/bin/python \
    paper2_aihwkit_baseline/train_aihwkit_baseline.py \
    --run-id r11d_9b_4bit_pure_high_noise \
    --epochs 100 \
    --batch-size 64 \
    --lr 0.001 \
    --wd 0.05 \
    --device cuda \
    --workers 0 \
    --save-dir "$CKPT_DIR" \
    --log-interval 1 \
    --inp-res 0.0625 \
    --out-res 0.0625 \
    --modifier-std-dev 0.01 \
    --early-stop-patience 20 \
    2>&1 | tee -a "$LOG"

echo "=== R11D-9b complete ==="
