#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
PY="/home/qiaosir/miniconda3/envs/LLM/bin/python"
TS="${1:-$(date +%Y%m%d_%H%M%S)}"

LOG_DIR="$ROOT/logs/_gpt"
mkdir -p "$LOG_DIR"

V4_CKPT="$ROOT/checkpoints/V4_hybrid_standard_noise_hat_best.pt"
LOG_PATH="$LOG_DIR/v4_proportional_noise_${TS}_gpt.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Task 24 start: V4 proportional-noise eval"
"$PY" "$ROOT/run_noise_sweep.py" \
  --model-type tinyvit \
  --experiment V4 \
  --checkpoint "$V4_CKPT" \
  --dataset cifar10 \
  --device cuda \
  --amp \
  --eval-runs 10 \
  --sweep-type noise \
  --sigma-c2c-values 0.05 \
  --sigma-d2d-values 0.10 \
  --noise-mode proportional \
  --preserve-checkpoint-d2d \
  --output-dir "$ROOT/report_md/_gpt" \
  --json-name "v4_proportional_noise_results_gpt.json" \
  --csv-name "v4_proportional_noise_results_gpt.csv" \
  --report-name "v4_proportional_noise_report_gpt.md" \
  --sparsity-json-name "v4_proportional_noise_sparsity_gpt.json" \
  --sparsity-csv-name "v4_proportional_noise_sparsity_gpt.csv" \
  --figure-output-dir "$ROOT/paper/figures" \
  --log-path "$LOG_PATH"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Task 24 done"
