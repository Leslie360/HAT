#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
TS="${1:-$(date +%Y%m%d_%H%M%S)}"
LOG_DIR="$ROOT/logs/_gpt"
mkdir -p "$LOG_DIR"

DRIVER_LOG="$LOG_DIR/task23_task24_after_task21_${TS}_driver_gpt.log"
exec > >(tee -a "$DRIVER_LOG") 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Stage 3 start: Task 24 + Task 23 after Task 21"

bash "$ROOT/run_task24_v4_proportional_eval_gpt.sh" "$TS"
bash "$ROOT/run_task23_tinyvit_nl_suite_gpt.sh" "$TS"
bash "$ROOT/run_task23_convnext_c4_nl_moderate_gpt.sh" "$TS"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Stage 3 done"
