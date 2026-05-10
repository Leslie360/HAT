#!/usr/bin/env bash
set -euo pipefail

cd /home/qiaosir/projects/compute_vit
LOG=logs/_gpt/cx_k3_stageA_driver_20260421_rerun.log
PIDFILE=logs/_gpt/cx_k3_stageA_rerun.pid
PY=/home/qiaosir/miniconda3/envs/LLM/bin/python

mkdir -p logs/_gpt
: > "$LOG"
nohup "$PY" scripts/_gpt/run_cx_k3_dgeff_stageA.py >> "$LOG" 2>&1 < /dev/null &
echo $! > "$PIDFILE"
echo "pid=$(cat "$PIDFILE")"
