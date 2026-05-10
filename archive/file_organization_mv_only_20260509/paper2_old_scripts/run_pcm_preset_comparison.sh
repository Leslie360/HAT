#!/bin/bash
# T1-3 v2: PCM Preset Comparison — PCMPresetUnitCell vs PCMPresetDevice
# Purpose: Verify conclusions do not depend on specific PCM preset choice
# Runs after multi-seed validation completes
# Uses fresh v2 run IDs to avoid historical invalid `PCMPresetDevice_seed42`
# artifact directories.

set -euo pipefail
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH
PROJECT_ROOT="/home/qiaosir/projects/compute_vit"
PYTHON=/home/qiaosir/miniconda3/envs/aihwkit/bin/python
TRAIN="$PROJECT_ROOT/paper2_aihwkit_baseline/r11d4_train_pcm_extended.py"

cd "$PROJECT_ROOT"

if [[ ! -f "$TRAIN" ]]; then
    echo "[FATAL] Strict preset training script not found: $TRAIN" >&2
    exit 2
fi

run_preset() {
    local run_id="$1"
    local preset="$2"
    local seed="$3"
    local inp_res="$4"
    local out_res="$5"
    local log="paper2_aihwkit_baseline/logs/${run_id}_${preset}_seed${seed}_$(date +%Y%m%d_%H%M%S).log"
    local ckpt_dir="paper2_aihwkit_baseline/checkpoints/${run_id}_${preset}_seed${seed}"
    mkdir -p "$ckpt_dir" paper2_aihwkit_baseline/logs

    echo "=== $run_id ($preset, seed=$seed) ===" | tee "$log"
    $PYTHON "$TRAIN" \
        --run-id "${run_id}_${preset}_seed${seed}" \
        --seed "$seed" \
        --epochs 100 \
        --batch-size 64 \
        --lr 0.001 \
        --wd 0.05 \
        --momentum 0.0 \
        --device cuda \
        --workers 0 \
        --save-dir "$ckpt_dir" \
        --log-interval 1 \
        --inp-res "$inp_res" \
        --out-res "$out_res" \
        --modifier-std-dev 0.10 \
        --early-stop-patience 0 \
        --pcm-preset "$preset" \
        2>&1 | tee -a "$log"
    if [[ ! -f "$ckpt_dir/training_history.json" || ! -f "$ckpt_dir/last.pt" ]]; then
        echo "[FATAL] Missing completion artifacts for ${run_id}_${preset}_seed${seed}: $ckpt_dir" | tee -a "$log"
        exit 3
    fi
    echo "=== $run_id $preset seed=$seed complete ===" | tee -a "$log"
}

# 8-bit PCM with PCMPresetDevice (compare against R11D-5a PCMPresetUnitCell seed123)
echo "=== T1-3a v2: 8-bit PCM PCMPresetDevice seed123 ==="
run_preset "t13v2_r11d_5a_pcm" "PCMPresetDevice" 123 0.00390625 0.00390625

# 4-bit PCM with PCMPresetDevice (compare against R11D-7 PCMPresetUnitCell seed123)
echo "=== T1-3b v2: 4-bit PCM PCMPresetDevice seed123 ==="
run_preset "t13v2_r11d_7_pcm_4bit" "PCMPresetDevice" 123 0.0625 0.0625

echo "=== ALL PCM PRESET COMPARISON COMPLETE ==="
