#!/usr/bin/env bash
set -euo pipefail
cd /home/qiaosir/projects/compute_vit
LOG=logs/_gpt/cx_parity_minimal_driver_20260422.log
PIDFILE=logs/_gpt/cx_parity_minimal_driver_20260422.pid
: > "$LOG"
nohup /home/qiaosir/miniconda3/envs/LLM/bin/python scripts/_gpt/run_cx_parity_minimal_20260422.py >> "$LOG" 2>&1 < /dev/null &
echo $! > "$PIDFILE"
echo "pid=$(cat "$PIDFILE")"
