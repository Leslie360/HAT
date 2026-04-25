#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
PY="${PYTHON_BIN:-/home/qiaosir/miniconda3/envs/LLM/bin/python}"
STAMP="$(date +%Y%m%d_%H%M%S)"
LOG="$ROOT/logs/_gpt/corrected_all_linear_queue_${STAMP}.log"

mkdir -p "$ROOT/logs/_gpt"
exec > >(tee -a "$LOG") 2>&1

cd "$ROOT"
echo "[queue] started at $(date --iso-8601=seconds)"

run_one() {
  local interval="$1"
  echo "[queue] launching r${interval} at $(date --iso-8601=seconds)"
  "$PY" scripts/_gpt/run_corrected_all_linear_cadence.py \
    --resample-interval "$interval" \
    --epochs 50 \
    --batch-size 64 \
    --num-workers 0 \
    --device cuda \
    --amp \
    --dataset cifar10 \
    --warm-start-from checkpoints/V4_hybrid_standard_noise_hat_best.pt \
    --use-second-order-ste \
    --delta-g-eff -1.0 \
    --protected-group all \
    --protected-nl-ltp 1.0 \
    --protected-nl-ltd -1.0 \
    --nl-ltp 2.0 \
    --nl-ltd -2.0 \
    --fresh-instances 5 \
    --eval-runs 3 \
    --log-interval 10
  echo "[queue] finished r${interval} at $(date --iso-8601=seconds)"
}

run_one 40
run_one 50
run_one 10

echo "[queue] completed at $(date --iso-8601=seconds)"
