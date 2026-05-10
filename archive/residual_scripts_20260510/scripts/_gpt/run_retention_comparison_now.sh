#!/usr/bin/env bash
set -euo pipefail
ROOT="/home/qiaosir/projects/compute_vit"
PY="/home/qiaosir/miniconda3/envs/LLM/bin/python"
cd "$ROOT"
echo "[t3] starting retention comparison at $(date --iso-8601=seconds)"
$PY scripts/_gpt/retention_comparison_gpt.py 2>&1 | tee logs/_gpt/t3_retention_comparison.log
echo "[t3] completed at $(date --iso-8601=seconds)"
