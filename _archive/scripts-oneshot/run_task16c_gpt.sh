#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

TS="${1:-$(date +%Y%m%d_%H%M%S)}"
PY="/home/qiaosir/miniconda3/envs/LLM/bin/python"

CIFAR_LOG="logs/_gpt/train_tinyvit_cifar100_v134_${TS}_gpt.log"
FLOWERS_LOG="logs/_gpt/train_tinyvit_flowers102_v134_${TS}_gpt.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Task 16c start: CIFAR-100 V1/V3/V4"
"$PY" -u train_tinyvit.py \
  --mode train \
  --dataset cifar100 \
  --experiments V1 V3 V4 \
  --device cuda \
  --pretrained \
  --amp \
  --resume-existing \
  --save-dir checkpoints/_gpt/cifar100 \
  --log-interval 5 \
  --log-path "$CIFAR_LOG" \
  --results-json-path report_md/_gpt/json_gpt/tinyvit_cifar100_v134_results_gpt.json \
  --results-csv-path report_md/_gpt/csv_gpt/tinyvit_cifar100_v134_results_gpt.csv \
  --results-md-path report_md/_gpt/tinyvit_cifar100_v134_results_gpt.md

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Task 16c continue: Flowers-102 V1/V3/V4"
"$PY" -u train_tinyvit.py \
  --mode train \
  --dataset flowers102 \
  --experiments V1 V3 V4 \
  --device cuda \
  --pretrained \
  --amp \
  --resume-existing \
  --save-dir checkpoints/_gpt/flowers102 \
  --log-interval 5 \
  --log-path "$FLOWERS_LOG" \
  --results-json-path report_md/_gpt/json_gpt/tinyvit_flowers102_v134_results_gpt.json \
  --results-csv-path report_md/_gpt/csv_gpt/tinyvit_flowers102_v134_results_gpt.csv \
  --results-md-path report_md/_gpt/tinyvit_flowers102_v134_results_gpt.md

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Task 16c done"
