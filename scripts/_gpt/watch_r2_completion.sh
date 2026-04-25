#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
TRAIN_LOG="${1:-$ROOT/logs/_gpt/r2_so2_comparison_train_20260423_175712.log}"
QUEUE_LOG="${2:-$ROOT/logs/_gpt/r2_so2_comparison_queue_20260423_175712.log}"
TRAIN_JSON="$ROOT/report_md/_gpt/json_gpt/r2_so2_comparison_train.json"
FRESH_JSON="$ROOT/report_md/_gpt/json_gpt/r2_so2_comparison_fresh_eval.json"
STATUS="$ROOT/report_md/_gpt/R2_MONITOR_STATUS_20260423.md"

mkdir -p "$(dirname "$STATUS")"
{
  echo "# R2 Monitor Status"
  echo
  echo "Started: $(date --iso-8601=seconds)"
  echo "Train log: $TRAIN_LOG"
  echo "Queue log: $QUEUE_LOG"
  echo
} > "$STATUS"

while true; do
  now="$(date --iso-8601=seconds)"
  latest="$(tail -n 1 "$TRAIN_LOG" 2>/dev/null || true)"
  proc_count="$(pgrep -fc 'run_tinyvit_groupwise_nl_comp.py .*_r2_so2_comparison' || true)"
  {
    echo "## $now"
    echo "- process_count: $proc_count"
    echo "- latest_train_log: $latest"
    if [ -f "$TRAIN_JSON" ]; then echo "- train_json: present"; else echo "- train_json: missing"; fi
    if [ -f "$FRESH_JSON" ]; then echo "- fresh_json: present"; else echo "- fresh_json: missing"; fi
    echo
  } >> "$STATUS"

  if [ -f "$FRESH_JSON" ]; then
    echo "Completed: $(date --iso-8601=seconds)" >> "$STATUS"
    exit 0
  fi

  if [ "$proc_count" = "0" ] && [ -f "$TRAIN_JSON" ] && [ ! -f "$FRESH_JSON" ]; then
    echo "WARNING: training process ended but fresh JSON is missing." >> "$STATUS"
    exit 2
  fi

  sleep 300
done
