#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="${REPO_DIR:-/home/qiaosir/projects/compute_vit}"
PYTHON_BIN="${PYTHON_BIN:-/home/qiaosir/miniconda3/envs/LLM/bin/python}"
LOG_DIR="$REPO_DIR/logs/_gpt"

mkdir -p "$LOG_DIR" "$REPO_DIR/checkpoints/_gpt/j1d_parity_fix" \
  "$REPO_DIR/report_md/_gpt/json_gpt" "$REPO_DIR/report_md/_gpt/csv_gpt"

WATCH_LOG="$LOG_DIR/j1d_parity_fix_watch_20260422.log"
RUN_LOG="$LOG_DIR/j1d_parity_fix_20260422.log"

{
  echo "[$(date '+%F %T')] watcher armed"
  while pgrep -f "V4_hybrid_standard_noise_hat_k4_alpha_0p25" >/dev/null; do
    echo "[$(date '+%F %T')] waiting for K4 alpha=0.25 to finish"
    sleep 120
  done

  echo "[$(date '+%F %T')] K4 alpha=0.25 no longer active; launching parity fix"
  exec "$PYTHON_BIN" scripts/_gpt/run_tinyvit_groupwise_nl_comp.py \
    --protected-group mlp \
    --protected-nl-ltp 1.0 \
    --protected-nl-ltd -1.0 \
    --use-second-order-ste \
    --delta-g-eff -1.0 \
    --name-suffix _j1d_parity_fix \
    --mode train \
    --dataset cifar10 \
    --experiments V4 \
    --epochs 1 \
    --batch-size 64 \
    --num-workers 0 \
    --device cuda \
    --amp \
    --nl-ltp 2.0 \
    --nl-ltd -2.0 \
    --warm-start-from checkpoints/V4_hybrid_standard_noise_hat_best.pt \
    --save-dir checkpoints/_gpt/j1d_parity_fix \
    --log-interval 1 \
    --log-path "$RUN_LOG" \
    --results-json-path report_md/_gpt/json_gpt/j1d_parity_fix_20260422.json \
    --results-csv-path report_md/_gpt/csv_gpt/j1d_parity_fix_20260422.csv \
    --results-md-path report_md/_gpt/j1d_parity_fix_20260422.md
} >>"$WATCH_LOG" 2>&1
