#!/bin/bash
# PCM Multi-Seed Validation: R11D-5a (8-bit) and R11D-7 (4-bit) with seeds 123, 456
# Purpose: Address biggest reviewer attack surface — all current results are single seed=42

set -e
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH
PYTHON=/home/qiaosir/miniconda3/envs/aihwkit/bin/python
TRAIN="/home/qiaosir/projects/compute_vit/paper2_aihwkit_baseline/train_aihwkit_baseline.py"

run_seed() {
    local run_id="$1"
    local seed="$2"
    local inp_res="$3"
    local out_res="$4"
    local log="paper2_aihwkit_baseline/logs/${run_id}_seed${seed}_$(date +%Y%m%d_%H%M%S).log"
    local ckpt_dir="paper2_aihwkit_baseline/checkpoints/${run_id}_seed${seed}"
    mkdir -p "$ckpt_dir" paper2_aihwkit_baseline/logs

    echo "=== $run_id (seed=$seed) ===" | tee "$log"
    $PYTHON "$TRAIN" \
        --run-id "${run_id}_seed${seed}" \
        --seed "$seed" \
        --epochs 100 \
        --batch-size 64 \
        --lr 0.001 \
        --wd 0.05 \
        --device cuda \
        --workers 0 \
        --save-dir "$ckpt_dir" \
        --log-interval 1 \
        --inp-res "$inp_res" \
        --out-res "$out_res" \
        --modifier-std-dev 0.10 \
        --early-stop-patience 20 \
        2>&1 | tee -a "$log"
    echo "=== $run_id seed=$seed complete ===" | tee -a "$log"
}

# R11D-5a (8-bit PCM) with seeds 123, 456
run_seed "r11d_5a_pcm" 123 0.00390625 0.00390625
run_seed "r11d_5a_pcm" 456 0.00390625 0.00390625

# R11D-7 (4-bit PCM) with seeds 123, 456
run_seed "r11d_7_pcm_4bit" 123 0.0625 0.0625
run_seed "r11d_7_pcm_4bit" 456 0.0625 0.0625

echo "=== ALL PCM MULTI-SEED VALIDATION COMPLETE ==="
