#!/bin/bash
set -e
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH

CKPT_DIR="paper2_aihwkit_baseline/checkpoints/r11d_8_hat_inspired_pcm"
LOG="paper2_aihwkit_baseline/logs/r11d_8_hat_pcm_$(date +%Y%m%d_%H%M%S).log"
mkdir -p "$CKPT_DIR" paper2_aihwkit_baseline/logs

echo "=== R11D-8: HAT-inspired PCM 8-bit full run ===" | tee "$LOG"
/home/qiaosir/miniconda3/envs/aihwkit/bin/python \
    paper2_aihwkit_baseline/r11d_hat_pcm.py \
    --run-id r11d_8_hat_inspired_pcm \
    --epochs 100 \
    --batch-size 64 \
    --lr 0.001 \
    --wd 0.05 \
    --device cuda \
    --workers 0 \
    --save-dir "$CKPT_DIR" \
    --log-interval 1 \
    --hat-std-dev 5.0 \
    --hat-mode scaled \
    --hat-start-epoch 1 \
    --early-stop-patience 20 \
    2>&1 | tee -a "$LOG"

echo "=== R11D-8 training complete ==="
