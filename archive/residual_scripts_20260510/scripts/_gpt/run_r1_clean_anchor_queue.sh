#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
PY="/home/qiaosir/miniconda3/envs/LLM/bin/python"
STAMP="$(date +%Y%m%d_%H%M%S)"
LOG="$ROOT/logs/_gpt/r1_clean_anchor_queue_${STAMP}.log"
SAVE_DIR="$ROOT/checkpoints/_gpt/r1_clean_anchor"
TRAIN_JSON="$ROOT/report_md/_gpt/json_gpt/r1_clean_anchor_train.json"
FRESH_JSON="$ROOT/report_md/_gpt/json_gpt/r1_clean_anchor_fresh_eval.json"
RUN_NAME="V4_hybrid_standard_noise_hat_r1_clean_anchor_first_order"
BEST_CKPT="$SAVE_DIR/${RUN_NAME}_best.pt"

mkdir -p "$ROOT/logs/_gpt" "$ROOT/report_md/_gpt/json_gpt" "$SAVE_DIR"
exec > >(tee -a "$LOG") 2>&1

cd "$ROOT"
echo "[r1] started at $(date --iso-8601=seconds)"
echo "[r1] git_head=$(git rev-parse --short HEAD)"
echo "[r1] phase=train"

bash scripts/_gpt/run_host_wsl_gpu.sh \
  "$PY scripts/_gpt/run_tinyvit_groupwise_nl_comp.py \
  --protected-group all \
  --protected-nl-ltp 1.0 \
  --protected-nl-ltd -1.0 \
  --name-suffix _r1_clean_anchor_first_order \
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
  --delta-g-eff 0.0 \
  --warm-start-from checkpoints/V4_hybrid_standard_noise_hat_best.pt \
  --save-dir \"$SAVE_DIR\" \
  --log-interval 5 \
  --log-path \"$ROOT/logs/_gpt/r1_clean_anchor_train_${STAMP}.log\" \
  --results-json-path \"$TRAIN_JSON\""

if [ ! -f "$BEST_CKPT" ]; then
  echo "[r1] ERROR: best checkpoint missing: $BEST_CKPT" >&2
  exit 2
fi

echo "[r1] phase=fresh_eval checkpoint=$BEST_CKPT"

bash scripts/_gpt/run_host_wsl_gpu.sh \
  "$PY scripts/_gpt/eval_joint_fresh_instance.py \
  --checkpoint \"$BEST_CKPT\" \
  --device cuda \
  --fresh-instances 10 \
  --eval-runs 5 \
  --data-root ./data \
  --num-workers 0 \
  --dataset cifar10 \
  --eval-batch-size 256 \
  --protected-group all \
  --protected-nl-ltp 1.0 \
  --protected-nl-ltd -1.0 \
  --delta-g-eff 0.0 \
  --json-out \"$FRESH_JSON\""

echo "[r1] completed at $(date --iso-8601=seconds)"
echo "[r1] train_json=$TRAIN_JSON"
echo "[r1] fresh_json=$FRESH_JSON"
