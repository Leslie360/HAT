#!/bin/bash
# R11D-6c eval: fresh + drift

set -e
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH

PROJECT=/home/qiaosir/projects/compute_vit
PYTHON=/home/qiaosir/miniconda3/envs/aihwkit/bin/python
CKPT="$PROJECT/paper2_aihwkit_baseline/checkpoints/r11d_6c_8bit_pure_high_noise/best.pt"
OUT="$PROJECT/paper2_aihwkit_baseline/checkpoints/r11d_6c_8bit_pure_high_noise"

# Fresh eval
$PYTHON "$PROJECT/paper2_aihwkit_baseline/eval_aihwkit_fresh.py" \
    --checkpoint "$CKPT" --n-fresh 10 --batch-size 64 --device cuda --output "$OUT/fresh_eval.json"

# Drift eval (will skip because non-PCM)
$PYTHON "$PROJECT/paper2_aihwkit_baseline/eval_aihwkit_drift.py" \
    --checkpoint "$CKPT" --batch-size 64 --device cuda --output "$OUT/drift_eval.json"

echo "R11D-6c eval complete"
