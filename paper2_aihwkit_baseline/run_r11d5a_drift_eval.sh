#!/bin/bash
# R11D-5a Drift Eval: 0s / 1h / 24h

set -e
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH

CKPT="paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm/best.pt"
SAVE="paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm/drift_eval.json"
LOG="paper2_aihwkit_baseline/logs/r11d_5a_drift_eval_$(date +%Y%m%d_%H%M%S).log"
mkdir -p paper2_aihwkit_baseline/logs

echo "=== R11D-5a Drift Eval (0s / 1h / 24h) ===" | tee "$LOG"
/home/qiaosir/miniconda3/envs/aihwkit/bin/python \
    paper2_aihwkit_baseline/eval_aihwkit_drift.py \
    --checkpoint "$CKPT" \
    --batch-size 64 \
    --device cuda \
    --output "$SAVE" \
    2>&1 | tee -a "$LOG"

echo ""
echo "=== Drift eval complete ==="
echo "Result: $SAVE"
echo "Log: $LOG"
