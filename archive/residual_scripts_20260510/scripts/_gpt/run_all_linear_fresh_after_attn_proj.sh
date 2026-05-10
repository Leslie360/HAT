#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/home/qiaosir/projects/compute_vit"
PYTHON_BIN="/home/qiaosir/miniconda3/envs/LLM/bin/python"
LOG_PATH="$REPO_DIR/logs/_gpt/run_all_linear_fresh_after_attn_proj.log"
JSON_PATH="$REPO_DIR/report_md/_gpt/json_gpt/nl_fresh_instance_controls_all_only_20260418.json"
MD_PATH="$REPO_DIR/report_md/_gpt/NL_FRESH_INSTANCE_CONTROLS_all_only_20260418.md"

mkdir -p "$(dirname "$LOG_PATH")"
cd "$REPO_DIR"

{
  echo "[$(date '+%F %T')] waiting for attn_proj-only lane to finish"
  while pgrep -f 'run_tinyvit_groupwise_nl_comp.py --protected-group attn_proj' >/dev/null; do
    sleep 30
  done
  echo "[$(date '+%F %T')] attn_proj-only lane drained; launching all-linear fresh-instance evaluation"
  "$PYTHON_BIN" scripts/_gpt/eval_nl_fresh_instance_controls.py \
    --lanes all \
    --device cuda \
    --num-workers 0 \
    --json-path "$JSON_PATH" \
    --md-path "$MD_PATH"
  echo "[$(date '+%F %T')] all-linear fresh-instance evaluation completed"
} >> "$LOG_PATH" 2>&1
