#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
PY="/home/qiaosir/miniconda3/envs/LLM/bin/python"
STAMP="${1:-$(date +%Y%m%d_%H%M%S)}"

SAVE_DIR="$ROOT/checkpoints/_gpt/task34_v4_proportional_hat"
REPORT_DIR="$ROOT/report_md/_gpt"
JSON_DIR="$REPORT_DIR/json_gpt"
CSV_DIR="$REPORT_DIR/csv_gpt"
LOG_DIR="$ROOT/logs/_gpt"

mkdir -p "$SAVE_DIR" "$JSON_DIR" "$CSV_DIR" "$LOG_DIR"

TRAIN_LOG="$LOG_DIR/train_tinyvit_v4_proportional_hat_${STAMP}_gpt.log"
EVAL_PROP_LOG="$LOG_DIR/eval_tinyvit_v4_proportional_hat_prop_${STAMP}_gpt.log"
EVAL_UNIFORM_LOG="$LOG_DIR/eval_tinyvit_v4_proportional_hat_uniform_${STAMP}_gpt.log"

TRAIN_JSON="$JSON_DIR/v4_proportional_hat_train_results_gpt.json"
TRAIN_CSV="$CSV_DIR/v4_proportional_hat_train_results_gpt.csv"
TRAIN_MD="$REPORT_DIR/v4_proportional_hat_train_results_gpt.md"

EVAL_PROP_JSON="$JSON_DIR/v4_proportional_hat_eval_proportional_results_gpt.json"
EVAL_PROP_CSV="$CSV_DIR/v4_proportional_hat_eval_proportional_results_gpt.csv"
EVAL_PROP_MD="$REPORT_DIR/v4_proportional_hat_eval_proportional_results_gpt.md"

EVAL_UNIFORM_JSON="$JSON_DIR/v4_proportional_hat_eval_uniform_results_gpt.json"
EVAL_UNIFORM_CSV="$CSV_DIR/v4_proportional_hat_eval_uniform_results_gpt.csv"
EVAL_UNIFORM_MD="$REPORT_DIR/v4_proportional_hat_eval_uniform_results_gpt.md"

cd "$ROOT"

"$PY" -u train_tinyvit.py \
  --mode train \
  --dataset cifar10 \
  --experiments V4 \
  --epochs 100 \
  --pretrained \
  --device cuda \
  --amp \
  --resume-existing \
  --noise-mode proportional \
  --save-dir "$SAVE_DIR" \
  --log-interval 5 \
  --log-path "$TRAIN_LOG" \
  --results-json-path "$TRAIN_JSON" \
  --results-csv-path "$TRAIN_CSV" \
  --results-md-path "$TRAIN_MD"

"$PY" -u train_tinyvit.py \
  --mode eval \
  --dataset cifar10 \
  --experiments V4 \
  --device cuda \
  --amp \
  --noise-mode proportional \
  --eval-runs 10 \
  --checkpoint-dir "$SAVE_DIR" \
  --log-path "$EVAL_PROP_LOG" \
  --results-json-path "$EVAL_PROP_JSON" \
  --results-csv-path "$EVAL_PROP_CSV" \
  --results-md-path "$EVAL_PROP_MD"

"$PY" -u train_tinyvit.py \
  --mode eval \
  --dataset cifar10 \
  --experiments V4 \
  --device cuda \
  --amp \
  --noise-mode uniform \
  --eval-runs 10 \
  --checkpoint-dir "$SAVE_DIR" \
  --log-path "$EVAL_UNIFORM_LOG" \
  --results-json-path "$EVAL_UNIFORM_JSON" \
  --results-csv-path "$EVAL_UNIFORM_CSV" \
  --results-md-path "$EVAL_UNIFORM_MD"
