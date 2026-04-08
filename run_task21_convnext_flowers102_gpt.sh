#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
PY="/home/qiaosir/miniconda3/envs/LLM/bin/python"
TS="${1:-$(date +%Y%m%d_%H%M%S)}"

mkdir -p "$ROOT/logs/_gpt"

LOG_PATH="$ROOT/logs/_gpt/train_convnext_flowers102_c134_fix_${TS}_gpt.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Task 21 stage 2 start: Flowers-102 C1/C3/C4"
"$PY" "$ROOT/train_convnext.py" \
  --dataset flowers102 \
  --num-classes 102 \
  --experiments C1 C3 C4 \
  --epochs 100 \
  --batch-size 64 \
  --device cuda \
  --amp \
  --resume-existing \
  --skip-retention \
  --save-dir "$ROOT/checkpoints/_gpt/convnext_flowers102" \
  --output-dir "$ROOT/report_md/_gpt" \
  --csv-name "convnext_flowers102_c134_results_gpt.csv" \
  --json-name "convnext_flowers102_c134_results_gpt.json" \
  --report-name "convnext_flowers102_c134_results_gpt.md" \
  2>&1 | tee "$LOG_PATH"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Task 21 stage 2 done"
