#!/usr/bin/env bash
# Smoke A: First-order only, 1 epoch, post dual-bug fix
set -euo pipefail

REPO_DIR="/home/qiaosir/projects/compute_vit"
PYTHON_BIN="/home/qiaosir/miniconda3/envs/LLM/bin/python"

cd "$REPO_DIR"

# Verify canonical commit
git log --oneline -1 | grep -q "49cacef" || {
    echo "ERROR: Not on canonical commit 49cacef"
    exit 1
}

LOG="$REPO_DIR/logs/_gpt/smoke_a_first_order_$(date +%Y%m%d_%H%M%S).log"

echo "[$(date '+%F %T')] Smoke A Launch — First-order only, 1 epoch"
echo "[$(date '+%F %T')] Git HEAD: $(git rev-parse --short HEAD)"

exec "$PYTHON_BIN" scripts/_gpt/run_tinyvit_groupwise_nl_comp.py \
    --protected-group all \
    --protected-nl-ltp 1.0 \
    --protected-nl-ltd -1.0 \
    --name-suffix _smoke_a_first_order \
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
    --save-dir checkpoints/_gpt/smoke_a_first_order \
    --log-interval 1 \
    --log-path "$LOG" \
    2>&1 | tee "$LOG"
