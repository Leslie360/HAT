#!/usr/bin/env bash
set -euo pipefail
ROOT="/home/qiaosir/projects/compute_vit"
STAMP="$(date +%Y%m%d_%H%M%S)"
LOG="$ROOT/logs/_gpt/cx_k4_alpha_continuation_${STAMP}.log"
nohup /home/qiaosir/miniconda3/envs/LLM/bin/python -u "$ROOT/scripts/_gpt/run_cx_k4_alpha_continuation.py" >"$LOG" 2>&1 &
echo "$!" > "$ROOT/tmp/cx_k4_alpha_continuation.pid"
echo "PID=$!"
echo "LOG=$LOG"
