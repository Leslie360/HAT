#!/usr/bin/env bash
# Smoke B: Second-order on, 1 epoch, post dual-bug fix
set -euo pipefail

REPO_DIR="/home/qiaosir/projects/compute_vit"
PYTHON_BIN="/home/qiaosir/miniconda3/envs/LLM/bin/python"

cd "$REPO_DIR"

git log --oneline -1 | grep -q "2bf59db30183edccd838c169e89c1539d1a4f907" || {
    echo "ERROR: Not on canonical commit 2bf59db30183edccd838c169e89c1539d1a4f907"
    exit 1
}

LOG="$REPO_DIR/logs/_gpt/smoke_b_second_order_$(date +%Y%m%d_%H%M%S).log"

echo "[$(date '+%F %T')] Smoke B Launch — Second-order on (α=0.25), 1 epoch"
echo "[$(date '+%F %T')] Git HEAD: $(git rev-parse --short HEAD)"

exec "$PYTHON_BIN" scripts/_gpt/run_tinyvit_groupwise_nl_comp.py \
    --protected-group all \
    --protected-nl-ltp 1.0 \
    --protected-nl-ltd -1.0 \
    --use-second-order-ste \
    --delta-g-eff -1.0 \
    --second-order-alpha 0.25 \
    --name-suffix _smoke_b_second_order \
    --mode train \
    --dataset cifar10 \
    --experiments V4 \
    --epochs 1 \
    --batch-size 64 \
    --num-workers 0 \
    --pin-memory off \
    --device cuda \
    --amp \
    --nl-ltp 2.0 \
    --nl-ltd -2.0 \
    --warm-start-from checkpoints/V4_hybrid_standard_noise_hat_best.pt \
    --save-dir checkpoints/_gpt/smoke_b_second_order \
    --log-interval 1 \
    --log-path "$LOG" \
    2>&1 | tee "$LOG"
