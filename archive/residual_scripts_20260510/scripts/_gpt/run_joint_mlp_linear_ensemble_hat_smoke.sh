#!/usr/bin/env bash
set -euo pipefail
ROOT="/home/qiaosir/projects/compute_vit"
PY="/home/qiaosir/miniconda3/envs/LLM/bin/python"
STAMP="${1:-$(date +%Y%m%d_%H%M%S)}"
SAVE_DIR="$ROOT/checkpoints/_gpt/joint_mlp_linear_ensemble_hat_smoke"
REPORT_DIR="$ROOT/report_md/_gpt"
JSON_DIR="$REPORT_DIR/json_gpt"
CSV_DIR="$REPORT_DIR/csv_gpt"
LOG_DIR="$ROOT/logs/_gpt"
mkdir -p "$SAVE_DIR" "$JSON_DIR" "$CSV_DIR" "$LOG_DIR"
TRAIN_LOG="$LOG_DIR/joint_mlp_linear_ensemble_hat_smoke_${STAMP}.log"
TRAIN_JSON="$JSON_DIR/joint_mlp_linear_ensemble_hat_smoke.json"
TRAIN_CSV="$CSV_DIR/joint_mlp_linear_ensemble_hat_smoke.csv"
TRAIN_MD="$REPORT_DIR/joint_mlp_linear_ensemble_hat_smoke.md"
cd "$ROOT"
"$PY" scripts/_gpt/run_tinyvit_groupwise_nl_comp.py \
  --protected-group mlp \
  --protected-nl-ltp 1.0 \
  --protected-nl-ltd -1.0 \
  --name-suffix _joint_mlp_linear_ensemble_hat_smoke \
  --mode train \
  --dataset cifar10 \
  --experiments V4 \
  --epochs 3 \
  --batch-size 64 \
  --num-workers 0 \
  --device cuda \
  --pretrained \
  --amp \
  --nl-ltp 2.0 \
  --nl-ltd -2.0 \
  --save-dir "$SAVE_DIR" \
  --log-interval 20 \
  --log-path "$TRAIN_LOG" \
  --results-json-path "$TRAIN_JSON" \
  --results-csv-path "$TRAIN_CSV" \
  --results-md-path "$TRAIN_MD"
