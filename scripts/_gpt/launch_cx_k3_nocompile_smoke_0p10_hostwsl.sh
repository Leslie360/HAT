#!/usr/bin/env bash
set -euo pipefail
cd /home/qiaosir/projects/compute_vit
LOG=logs/_gpt/cx_k3_nocompile_smoke_0p10.log
PIDFILE=logs/_gpt/cx_k3_nocompile_smoke_0p10.pid
: > "$LOG"
nohup bash scripts/_gpt/cx_k3_nocompile_smoke_0p10.sh >> "$LOG" 2>&1 < /dev/null &
echo $! > "$PIDFILE"
echo "pid=$(cat "$PIDFILE")"
