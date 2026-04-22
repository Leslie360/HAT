#!/usr/bin/env bash
set -euo pipefail
cd /home/qiaosir/projects/compute_vit
LOG=logs/_gpt/cx_k3_continuation_driver_20260421.log
PIDFILE=logs/_gpt/cx_k3_continuation_driver_20260421.pid
: > "$LOG"
nohup /home/qiaosir/miniconda3/envs/LLM/bin/python scripts/_gpt/run_cx_k3_continuation.py >> "$LOG" 2>&1 < /dev/null &
echo $! > "$PIDFILE"
echo "pid=$(cat "$PIDFILE")"
