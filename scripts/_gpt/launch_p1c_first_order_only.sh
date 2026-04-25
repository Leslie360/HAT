#!/usr/bin/env bash
# P1-C: First-order-only ablation (no second-order brake)
# K4R result: 34.99% fresh-instance with SO2 @ α=0.25
# This ablation tests whether the second-order brake itself is the problem.
set -euo pipefail

REPO_DIR="/home/qiaosir/projects/compute_vit"
PYTHON_BIN="/home/qiaosir/miniconda3/envs/LLM/bin/python"

cd "$REPO_DIR"

LOG_DIR="$REPO_DIR/logs/_gpt"
mkdir -p "$LOG_DIR"

LOG="$LOG_DIR/cx_p1c_first_order_only_$(date +%Y%m%d_%H%M%S).log"

echo "[$(date '+%F %T')] P1-C First-Order-Only Ablation Launch"
echo "[$(date '+%F %T')] Git HEAD: $(git rev-parse --short HEAD)"
echo "[$(date '+%F %T')] Rationale: K4R SO2 α=0.25 yielded 34.99% fresh-instance"
echo "[$(date '+%F %T')] This run disables second-order to test if first-order alone recovers transfer."

exec "$PYTHON_BIN" scripts/_gpt/run_tinyvit_groupwise_nl_comp.py \
    --protected-group all \
    --protected-nl-ltp 1.0 \
    --protected-nl-ltd -1.0 \
    --name-suffix _p1c_first_order_only \
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
    --save-dir checkpoints/_gpt/cx_p1c_first_order_only \
    --log-interval 5 \
    --log-path "$LOG" \
    --results-json-path report_md/_gpt/json_gpt/cx_p1c_first_order_only_train.json \
    2>&1 | tee "$LOG"
