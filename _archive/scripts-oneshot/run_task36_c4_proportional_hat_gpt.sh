#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
PY="/home/qiaosir/miniconda3/envs/LLM/bin/python"
STAMP="${1:-$(date +%Y%m%d_%H%M%S)}"

SAVE_DIR="$ROOT/checkpoints/_gpt/task36_c4_proportional_hat"
REPORT_DIR="$ROOT/report_md/_gpt"
JSON_DIR="$REPORT_DIR/json_gpt"
CSV_DIR="$REPORT_DIR/csv_gpt"
LOG_DIR="$ROOT/logs/_gpt"

mkdir -p "$SAVE_DIR" "$JSON_DIR" "$CSV_DIR" "$LOG_DIR"

TRAIN_LOG="$LOG_DIR/train_convnext_c4_proportional_hat_${STAMP}_gpt.log"

TRAIN_JSON="$JSON_DIR/c4_proportional_hat_train_results_gpt.json"
TRAIN_CSV="$CSV_DIR/c4_proportional_hat_train_results_gpt.csv"
TRAIN_MD="$REPORT_DIR/c4_proportional_hat_train_results_gpt.md"

cd "$ROOT"

"$PY" -u train_convnext.py \
  --dataset cifar10 \
  --experiments C4 \
  --epochs 200 \
  --device cuda \
  --resume-existing \
  --noise-mode proportional \
  --skip-retention \
  --save-dir "$SAVE_DIR" \
  --json-name "$(basename "$TRAIN_JSON")" \
  --csv-name "$(basename "$TRAIN_CSV")" \
  --report-name "$(basename "$TRAIN_MD")" \
  --output-dir "$REPORT_DIR" \
  > "$TRAIN_LOG" 2>&1
