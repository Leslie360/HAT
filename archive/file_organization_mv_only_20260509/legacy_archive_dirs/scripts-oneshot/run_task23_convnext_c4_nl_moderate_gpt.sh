#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
PY="/home/qiaosir/miniconda3/envs/LLM/bin/python"
TS="${1:-$(date +%Y%m%d_%H%M%S)}"

mkdir -p "$ROOT/logs/_gpt" "$ROOT/checkpoints/_gpt/task23/c4_nl_moderate"

LOG_PATH="$ROOT/logs/_gpt/train_convnext_c4_nl_moderate_${TS}_gpt.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Task 23 start: ConvNeXt C4 NL moderate"
"$PY" "$ROOT/train_convnext.py" \
  --dataset cifar10 \
  --experiments C4 \
  --device cuda \
  --resume-existing \
  --skip-retention \
  --save-dir "$ROOT/checkpoints/_gpt/task23/c4_nl_moderate" \
  --output-dir "$ROOT/report_md/_gpt" \
  --csv-name "c4_nl_moderate_results_gpt.csv" \
  --json-name "c4_nl_moderate_results_gpt.json" \
  --report-name "c4_nl_moderate_results_gpt.md" \
  --nl-ltp 2.0 \
  --nl-ltd -2.0 \
  2>&1 | tee "$LOG_PATH"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Task 23 ConvNeXt C4 NL moderate done"
