#!/bin/bash
set -e
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH

CKPT_DIR="paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit"
LOG="paper2_aihwkit_baseline/logs/r11d_7_pcm_4bit_$(date +%Y%m%d_%H%M%S).log"
mkdir -p "$CKPT_DIR" paper2_aihwkit_baseline/logs

echo "=== R11D-7: PCM 4-bit lr=1e-3 ===" | tee "$LOG"
/home/qiaosir/miniconda3/envs/aihwkit/bin/python \
    paper2_aihwkit_baseline/r11d4_train_pcm.py \
    --run-id r11d_7_pcm_4bit \
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
    2>&1 | tee -a "$LOG"

echo "=== R11D-7 training complete ==="
