#!/bin/bash
# R11D-HAT-PCM: Ensemble HAT + PCM quick test (3 epochs) to validate code.
# Full run will be queued after R11D-5a completes.

set -e
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH

LOG="paper2_aihwkit_baseline/logs/r11d_hat_pcm_smoke_$(date +%Y%m%d_%H%M%S).log"
mkdir -p paper2_aihwkit_baseline/logs
mkdir -p paper2_aihwkit_baseline/checkpoints/r11d_hat_pcm

# Quick smoke test: 3 epochs, batch 32 to fit alongside R11D-5a
/home/qiaosir/miniconda3/envs/aihwkit/bin/python \
    paper2_aihwkit_baseline/r11d_hat_pcm.py \
    --run-id r11d_hat_pcm_smoke \
    --epochs 3 \
    --batch-size 32 \
    --lr 5e-4 \
    --wd 0.05 \
    --device cuda \
    --workers 0 \
    --save-dir paper2_aihwkit_baseline/checkpoints/r11d_hat_pcm_smoke \
    --log-interval 1 \
    --hat-std-dev 0.10 \
    --hat-start-epoch 1 \
    2>&1 | tee "$LOG"

echo ""
echo "=== Smoke test complete ==="
echo "Log: $LOG"
