#!/bin/bash
# R11D-5a Fresh Eval: 10 inference repetitions with fresh D2D noise

set -e
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH

CKPT="paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm/best.pt"
SAVE="paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm/fresh_eval.json"
LOG="paper2_aihwkit_baseline/logs/r11d_5a_fresh_eval_$(date +%Y%m%d_%H%M%S).log"
mkdir -p paper2_aihwkit_baseline/logs

echo "=== R11D-5a Fresh Eval (10 instances) ===" | tee "$LOG"
/home/qiaosir/miniconda3/envs/aihwkit/bin/python \
    paper2_aihwkit_baseline/eval_aihwkit_fresh.py \
    --checkpoint "$CKPT" \
    --n-fresh 10 \
    --batch-size 64 \
    --device cuda \
    --output "$SAVE" \
    2>&1 | tee -a "$LOG"

echo ""
echo "=== Fresh eval complete ==="
echo "Result: $SAVE"
echo "Log: $LOG"
