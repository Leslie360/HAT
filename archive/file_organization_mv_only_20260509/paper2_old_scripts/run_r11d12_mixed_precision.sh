#!/bin/bash
# Spatial Mixed-Precision Pilot (Work-2 Exploration)
# Strategy: Protect patch_embed and head at 8-bit PCM, others 4-bit PCM.

set -e
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH
PYTHON=/home/qiaosir/miniconda3/envs/aihwkit/bin/python
PROJECT=/home/qiaosir/projects/compute_vit
TRAIN="$PROJECT/paper2_aihwkit_baseline/r11d12_mixed_precision.py"
LOG_DIR="$PROJECT/paper2_aihwkit_baseline/logs"

mkdir -p "$LOG_DIR"

RUN_ID="r11d12_spatial_mixed_p1"
echo "Launching Mixed-Precision Pilot: $RUN_ID"

nohup $PYTHON "$TRAIN" \
    --run-id "$RUN_ID" \
    --epochs 100 \
    --layers-8bit "patch_embed,head" \
    --modifier-std-dev 0.1 \
    2>&1 | tee "$LOG_DIR/${RUN_ID}_$(date +%Y%m%d_%H%M%S).log" &

echo "Experiment launched in background."
