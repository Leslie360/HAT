#!/bin/bash
# PCM Multi-Seed Validation v2 — CORRECTED
# Uses r11d4_train_pcm.py (PCMPresetUnitCell + AnalogSGD), NOT train_aihwkit_baseline.py
# Purpose: Address reviewer attack surface with VALID PCM multi-seed data

set -euo pipefail
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH
PROJECT_ROOT="/home/qiaosir/projects/compute_vit"
PYTHON=/home/qiaosir/miniconda3/envs/aihwkit/bin/python
TRAIN="$PROJECT_ROOT/paper2_aihwkit_baseline/r11d4_train_pcm.py"

cd "$PROJECT_ROOT"

run_seed() {
    local run_id="$1"
    local seed="$2"
    local inp_res="$3"
    local out_res="$4"
    local log="paper2_aihwkit_baseline/logs/${run_id}_seed${seed}_$(date +%Y%m%d_%H%M%S).log"
    local ckpt_dir="paper2_aihwkit_baseline/checkpoints/${run_id}_seed${seed}"
    mkdir -p "$ckpt_dir" paper2_aihwkit_baseline/logs

    echo "=== $run_id (seed=$seed, PCM preset, AnalogSGD) ===" | tee "$log"
    $PYTHON "$TRAIN" \
        --run-id "${run_id}_seed${seed}" \
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
        2>&1 | tee -a "$log"
    if [[ ! -f "$ckpt_dir/training_history.json" || ! -f "$ckpt_dir/last.pt" ]]; then
        echo "[FATAL] Missing completion artifacts for ${run_id}_seed${seed}: $ckpt_dir" | tee -a "$log"
        exit 3
    fi
    echo "=== $run_id seed=$seed complete ===" | tee -a "$log"
}

# R11D-7 (4-bit PCM) first per Codex instruction
echo "=== STARTING R11D-7 4-bit PCM multi-seed ==="
run_seed "r11d_7_pcm_4bit" 123 0.0625 0.0625
run_seed "r11d_7_pcm_4bit" 456 0.0625 0.0625

# R11D-5a (8-bit PCM) second
echo "=== STARTING R11D-5a 8-bit PCM multi-seed ==="
run_seed "r11d_5a_pcm" 123 0.00390625 0.00390625
run_seed "r11d_5a_pcm" 456 0.00390625 0.00390625

echo "=== ALL PCM MULTI-SEED VALIDATION COMPLETE ==="
