#!/usr/bin/env bash
set -eo pipefail
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}
PYTHON=/home/qiaosir/miniconda3/envs/aihwkit/bin/python
SCRIPT=/home/qiaosir/projects/compute_vit/paper2_aihwkit_baseline/r11d4_train_pcm.py
LOG="/home/qiaosir/projects/compute_vit/paper2_aihwkit_baseline/logs/r11d_5c_pcm_$(date +%Y%m%d_%H%M%S).log"
mkdir -p "$(dirname "$LOG")"
echo "=== R11D-5c PCM (lr=1e-3, momentum=0.9) ===" | tee -a "$LOG"
nohup "$PYTHON" "$SCRIPT" \
    --run-id r11d_5c_pcm \
    --epochs 100 \
    --batch-size 64 \
    --lr 0.001 \
    --momentum 0.9 \
    --wd 0.05 \
    --device cuda \
    --workers 0 \
    --save-dir paper2_aihwkit_baseline/checkpoints/r11d_5c_pcm \
    --log-interval 1 \
    2>&1 | tee -a "$LOG" > /dev/null &
echo "PID: $!"
echo "Log: $LOG"
