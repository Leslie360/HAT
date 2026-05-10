#!/bin/bash
# R11D-HAT-PCM v2: scaled noise + smaller std_dev smoke test.

set -e
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH

LOG="paper2_aihwkit_baseline/logs/r11d_hat_pcm_v2_smoke_$(date +%Y%m%d_%H%M%S).log"
mkdir -p paper2_aihwkit_baseline/logs
mkdir -p paper2_aihwkit_baseline/checkpoints/r11d_hat_pcm_v2

# Test with scaled mode and per-layer scalar D2D at std_dev=5.0
/home/qiaosir/miniconda3/envs/aihwkit/bin/python \
    paper2_aihwkit_baseline/r11d_hat_pcm.py \
    --run-id r11d_hat_pcm_v2_smoke \
    --epochs 3 \
    --batch-size 32 \
    --lr 5e-4 \
    --wd 0.05 \
    --device cuda \
    --workers 0 \
    --save-dir paper2_aihwkit_baseline/checkpoints/r11d_hat_pcm_v2_smoke \
    --log-interval 1 \
    --hat-std-dev 5.0 \
    --hat-mode scaled \
    --hat-start-epoch 1 \
    2>&1 | tee "$LOG"

echo ""
echo "=== Smoke test v2 complete ==="
echo "Log: $LOG"
