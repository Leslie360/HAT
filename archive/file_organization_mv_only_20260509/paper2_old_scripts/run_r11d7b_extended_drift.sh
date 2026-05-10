#!/bin/bash
# R11D-7b: Extended drift eval for R11D-7 (4-bit PCM) with finer time granularity

set -e
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH

PROJECT=/home/qiaosir/projects/compute_vit
PYTHON=/home/qiaosir/miniconda3/envs/aihwkit/bin/python
CKPT="$PROJECT/paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit/best.pt"
OUT="$PROJECT/paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit/extended_drift_eval.json"

echo "=== R11D-7b: Extended Drift Eval (0h,1h,6h,12h,24h,48h,72h) ==="

$PYTHON "$PROJECT/paper2_aihwkit_baseline/eval_aihwkit_drift_extended.py" \
    --checkpoint "$CKPT" \
    --batch-size 64 \
    --device cuda \
    --output "$OUT" \
    --drift-times 0 3600 21600 43200 86400 172800 259200

echo "=== R11D-7b complete ==="
