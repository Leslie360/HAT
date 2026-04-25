#!/usr/bin/env bash
# CX-K4R Fresh Eval: 10 fresh instances × 5 MC passes on Branch A canonical checkpoint
set -euo pipefail

REPO_DIR="/home/qiaosir/projects/compute_vit"
PYTHON_BIN="/home/qiaosir/miniconda3/envs/LLM/bin/python"

cd "$REPO_DIR"

# Verify Branch A canonical code
git log --oneline -1 | grep -qE "Branch A|user-ratified STE semantics|nl multiplier" || {
    echo "ERROR: Not on Branch A canonical code. Abort."
    exit 1
}

# Find the best checkpoint from K4R
CHECKPOINT_DIR="$REPO_DIR/checkpoints/_gpt/cx_k4_alpha/k4_alpha_0p25"
if [ ! -d "$CHECKPOINT_DIR" ]; then
    echo "ERROR: K4R checkpoint dir not found: $CHECKPOINT_DIR"
    exit 1
fi

BEST_CKPT=$(ls -t "$CHECKPOINT_DIR"/*_best.pt 2>/dev/null | head -1)
if [ -z "$BEST_CKPT" ]; then
    echo "ERROR: No best checkpoint found in $CHECKPOINT_DIR"
    exit 1
fi

echo "[$(date '+%F %T')] K4R Fresh Eval launch"
echo "[$(date '+%F %T')] Git HEAD: $(git rev-parse --short HEAD)"
echo "[$(date '+%F %T')] Checkpoint: $BEST_CKPT"

LOG="$REPO_DIR/logs/_gpt/cx_k4r_fresh_eval_$(date +%Y%m%d_%H%M%S).log"

exec "$PYTHON_BIN" scripts/_gpt/eval_joint_fresh_instance.py \
    --checkpoint "$BEST_CKPT" \
    --protected-group all \
    --protected-nl-ltp 1.0 \
    --protected-nl-ltd -1.0 \
    --use-second-order-ste \
    --delta-g-eff -1.0 \
    --second-order-alpha 0.25 \
    --fresh-instances 10 \
    --eval-runs 5 \
    --device cuda \
    --data-root data \
    --num-workers 0 \
    --json-out "$REPO_DIR/report_md/_gpt/json_gpt/cx_k4r_fresh_eval.json" \
    2>&1 | tee "$LOG"
