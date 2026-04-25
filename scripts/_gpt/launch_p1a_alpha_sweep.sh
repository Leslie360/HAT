#!/usr/bin/env bash
# P1-A: Alpha sweep (0.1, 0.25, 0.5, 1.0) on group=all uniform-NL
# Run this if K4R fresh-instance mean >= 85%
set -euo pipefail

REPO_DIR="/home/qiaosir/projects/compute_vit"
PYTHON_BIN="/home/qiaosir/miniconda3/envs/LLM/bin/python"

cd "$REPO_DIR"

for ALPHA in 0.1 0.25 0.5 1.0; do
    NAME="k4_alpha_${ALPHA}"
    LOG="$REPO_DIR/logs/_gpt/cx_p1a_alpha_${ALPHA}_$(date +%Y%m%d_%H%M%S).log"
    echo "[$(date '+%F %T')] Launching alpha=$ALPHA"
    
    exec "$PYTHON_BIN" scripts/_gpt/run_tinyvit_groupwise_nl_comp.py \
        --protected-group all \
        --protected-nl-ltp 1.0 \
        --protected-nl-ltd -1.0 \
        --use-second-order-ste \
        --delta-g-eff -1.0 \
        --second-order-alpha "$ALPHA" \
        --name-suffix "_k4_alpha_${ALPHA}" \
        --mode train \
        --dataset cifar10 \
        --experiments V4 \
        --epochs 100 \
        --batch-size 64 \
        --num-workers 0 \
        --pin-memory off \
        --device cuda \
        --amp \
        --nl-ltp 2.0 \
        --nl-ltd -2.0 \
        --warm-start-from checkpoints/V4_hybrid_standard_noise_hat_best.pt \
        --save-dir "checkpoints/_gpt/cx_p1_alpha/${NAME}" \
        --log-interval 5 \
        --log-path "$LOG" \
        2>&1 | tee "$LOG" &
    
    # Wait a bit between launches to avoid GPU OOM
    sleep 30
done

echo "All P1-A alpha sweep jobs launched in background."
