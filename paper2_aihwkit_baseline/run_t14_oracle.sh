#!/bin/bash
# T1-4: Noise-Free PCM Oracle
# Train with PCM but modifier_std_dev=0 (no per-forward noise)
# Compare against R11D-5a (PCM + σ=0.10) to isolate noise contribution

set -e
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH
PYTHON=/home/qiaosir/miniconda3/envs/aihwkit/bin/python
TRAIN="/home/qiaosir/projects/compute_vit/paper2_aihwkit_baseline/r11d4_train_pcm.py"

run_id="r11d_5a_pcm_oracle_noise_free"
seed=42
log="paper2_aihwkit_baseline/logs/${run_id}_$(date +%Y%m%d_%H%M%S).log"
ckpt_dir="paper2_aihwkit_baseline/checkpoints/${run_id}"
mkdir -p "$ckpt_dir" paper2_aihwkit_baseline/logs

echo "=== T1-4 Oracle: PCM 8-bit, modifier_std_dev=0 ===" | tee "$log"
$PYTHON "$TRAIN" \
    --run-id "$run_id" \
    --seed "$seed" \
    --epochs 100 \
    --batch-size 128 \
    --lr 0.001 \
    --wd 0.05 \
    --momentum 0.0 \
    --device cuda \
    --workers 0 \
    --save-dir "$ckpt_dir" \
    --log-interval 1 \
    --inp-res 0.00390625 \
    --out-res 0.00390625 \
    --modifier-std-dev 0.0 \
    --early-stop-patience 0 \
    2>&1 | tee -a "$log"
echo "=== T1-4 Oracle complete ===" | tee -a "$log"
