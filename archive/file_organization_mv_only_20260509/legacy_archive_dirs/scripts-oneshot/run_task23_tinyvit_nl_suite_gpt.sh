#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
PY="/home/qiaosir/miniconda3/envs/LLM/bin/python"
TS="${1:-$(date +%Y%m%d_%H%M%S)}"

mkdir -p "$ROOT/logs/_gpt" "$ROOT/checkpoints/_gpt/task23"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Task 23 start: Tiny-ViT NL suite"

"$PY" "$ROOT/train_tinyvit.py" \
  --mode train \
  --experiment V4 \
  --dataset cifar10 \
  --device cuda \
  --pretrained \
  --amp \
  --resume-existing \
  --nl-ltp 2.0 \
  --nl-ltd -2.0 \
  --save-dir "$ROOT/checkpoints/_gpt/task23/v4_nl_moderate" \
  --results-json-path "$ROOT/report_md/_gpt/json_gpt/v4_nl_moderate_results_gpt.json" \
  --results-csv-path "$ROOT/report_md/_gpt/csv_gpt/v4_nl_moderate_results_gpt.csv" \
  --results-md-path "$ROOT/report_md/_gpt/v4_nl_moderate_results_gpt.md" \
  --log-path "$ROOT/logs/_gpt/train_tinyvit_v4_nl_moderate_${TS}_gpt.log"

"$PY" "$ROOT/train_tinyvit.py" \
  --mode train \
  --experiment V4 \
  --dataset cifar10 \
  --device cuda \
  --pretrained \
  --amp \
  --resume-existing \
  --nl-ltp 3.0 \
  --nl-ltd -3.0 \
  --save-dir "$ROOT/checkpoints/_gpt/task23/v4_nl_severe" \
  --results-json-path "$ROOT/report_md/_gpt/json_gpt/v4_nl_severe_results_gpt.json" \
  --results-csv-path "$ROOT/report_md/_gpt/csv_gpt/v4_nl_severe_results_gpt.csv" \
  --results-md-path "$ROOT/report_md/_gpt/v4_nl_severe_results_gpt.md" \
  --log-path "$ROOT/logs/_gpt/train_tinyvit_v4_nl_severe_${TS}_gpt.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Task 23 Tiny-ViT suite done"
