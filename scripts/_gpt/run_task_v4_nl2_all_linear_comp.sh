#!/usr/bin/env bash
set -euo pipefail
STAMP="${1:-$(date +%Y%m%d_%H%M%S)}"
ROOT="/home/qiaosir/projects/compute_vit"
PYTHON_BIN="/home/qiaosir/miniconda3/envs/LLM/bin/python"
cd "$ROOT"
mkdir -p logs/_gpt report_md/_gpt/json_gpt report_md/_gpt/csv_gpt checkpoints/_gpt/nl_mitigation/v4_nl2_all_linear_comp
exec "$PYTHON_BIN" scripts/_gpt/run_tinyvit_groupwise_nl_comp.py \
  --protected-group all \
  --protected-nl-ltp 1.0 \
  --protected-nl-ltd -1.0 \
  --name-suffix _nl2_all_linear_comp \
  --mode train \
  --dataset cifar10 \
  --experiments V4 \
  --device cuda \
  --pretrained \
  --amp \
  --resume-existing \
  --nl-ltp 2.0 \
  --nl-ltd -2.0 \
  --save-dir "$ROOT/checkpoints/_gpt/nl_mitigation/v4_nl2_all_linear_comp" \
  --log-interval 5 \
  --log-path "$ROOT/logs/_gpt/train_tinyvit_v4_nl2_all_linear_comp_${STAMP}.log" \
  --results-json-path "$ROOT/report_md/_gpt/json_gpt/v4_nl2_all_linear_comp_train_results_gpt.json" \
  --results-csv-path "$ROOT/report_md/_gpt/csv_gpt/v4_nl2_all_linear_comp_train_results_gpt.csv" \
  --results-md-path "$ROOT/report_md/_gpt/v4_nl2_all_linear_comp_train_results_gpt.md"
