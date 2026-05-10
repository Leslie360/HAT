#!/bin/bash
# R11D Launch Queue — prepared by Claude
# Run sequentially after R11D-1 completes

set -e
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH
PYTHON=~/miniconda3/envs/aihwkit/bin/python
TRAIN=paper2_aihwkit_baseline/train_aihwkit_baseline.py

echo "=== R11D-2: High-noise stress (sigma=0.20) ==="
$PYTHON $TRAIN \
  --inp-res 0.00390625 --out-res 0.00390625 \
  --modifier-std-dev 0.20 \
  --save-dir paper2_aihwkit_baseline/checkpoints/r11d2 \
  --run-id r11d2_highnoise \
  --device cuda

echo "=== R11D-3: Extreme noise (sigma=0.30) ==="
$PYTHON $TRAIN \
  --inp-res 0.00390625 --out-res 0.00390625 \
  --modifier-std-dev 0.30 \
  --save-dir paper2_aihwkit_baseline/checkpoints/r11d3 \
  --run-id r11d3_extreme \
  --device cuda

echo "=== Queue complete ==="
