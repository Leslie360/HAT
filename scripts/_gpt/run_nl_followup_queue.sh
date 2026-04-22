#!/usr/bin/env bash
set -euo pipefail
ROOT="/home/qiaosir/projects/compute_vit"
cd "$ROOT"
LOG="$ROOT/logs/_gpt/nl_followup_queue.log"
mkdir -p "$ROOT/logs/_gpt"
exec >> "$LOG" 2>&1

echo "[$(date '+%F %T')] NL follow-up queue started"
while pgrep -af "run_tinyvit_groupwise_nl_comp.py.*_nl2_mlp_linear_comp" >/dev/null 2>&1; do
  echo "[$(date '+%F %T')] waiting for active mlp-linear run to finish"
  sleep 60
done

echo "[$(date '+%F %T')] starting qkv-linear compensation run"
bash "$ROOT/scripts/_gpt/run_task_v4_nl2_qkv_linear_comp.sh" "$(date +%Y%m%d_%H%M%S)_queue_qkv"

echo "[$(date '+%F %T')] starting all-linear compensation run"
bash "$ROOT/scripts/_gpt/run_task_v4_nl2_all_linear_comp.sh" "$(date +%Y%m%d_%H%M%S)_queue_all"

echo "[$(date '+%F %T')] NL follow-up queue finished"
