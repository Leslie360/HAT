#!/usr/bin/env bash
# CX-K4R: K4 alpha=0.25 rerun on FIXED backward (fast anchor)
set -euo pipefail

REPO_DIR="/home/qiaosir/projects/compute_vit"
PYTHON_BIN="/home/qiaosir/miniconda3/envs/LLM/bin/python"
LOG_DIR="$REPO_DIR/logs/_gpt"

cd "$REPO_DIR"

# Verify we are on fixed code
git log --oneline -1 | grep -q "nl multiplier" || {
    echo "ERROR: backward fix not committed. Abort."
    exit 1
}

# Delete old incomplete checkpoint if any
rm -rf "$REPO_DIR/checkpoints/_gpt/cx_k4_alpha/k4_alpha_0p25"

mkdir -p "$LOG_DIR"

LOG="$LOG_DIR/cx_k4r_alpha_0p25_$(date +%Y%m%d_%H%M%S).log"

echo "[$(date '+%F %T')] K4R alpha=0.25 launch on FIXED backward"
echo "[$(date '+%F %T')] Git HEAD: $(git rev-parse --short HEAD)"
echo "[$(date '+%F %T')] Log: $LOG"

exec "$PYTHON_BIN" scripts/_gpt/run_tinyvit_groupwise_nl_comp.py \
    --protected-group all \
    --protected-nl-ltp 1.0 \
    --protected-nl-ltd -1.0 \
    --use-second-order-ste \
    --delta-g-eff -1.0 \
    --second-order-alpha 0.25 \
    --name-suffix _k4_alpha_0p25 \
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
    --save-dir checkpoints/_gpt/cx_k4_alpha/k4_alpha_0p25 \
    --log-interval 5 \
    --log-path "$LOG" \
    --results-json-path report_md/_gpt/json_gpt/cx_k4r_train_k4_alpha_0p25.json \
    --results-csv-path report_md/_gpt/csv_gpt/cx_k4r_train_k4_alpha_0p25.csv \
    --results-md-path report_md/_gpt/cx_k4r_train_k4_alpha_0p25.md \
    2>&1 | tee "$LOG"
