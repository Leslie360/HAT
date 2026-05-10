#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
TS="${1:?usage: $0 TIMESTAMP ORIGINAL_TMUX_SESSION}"
ORIGINAL_SESSION="${2:?usage: $0 TIMESTAMP ORIGINAL_TMUX_SESSION}"
M2_LOG="$ROOT/logs/_gpt/cx-m2_fresheval_${TS}.log"
SWITCH_LOG="$ROOT/logs/_gpt/cx_fresh_eval_parallel_switch_${TS}.log"

cd "$ROOT"
mkdir -p logs/_gpt

echo "[$(date -Is)] waiting for CX-M2 clean completion in $M2_LOG" | tee -a "$SWITCH_LOG"
while ! grep -q "Saved to report_md/_gpt/json_gpt/cx_m2_fresh_eval.json" "$M2_LOG" 2>/dev/null; do
  sleep 10
done

echo "[$(date -Is)] CX-M2 complete; stopping sequential runner $ORIGINAL_SESSION" | tee -a "$SWITCH_LOG"
tmux send-keys -t "$ORIGINAL_SESSION" C-c 2>/dev/null || true
sleep 5
tmux kill-session -t "$ORIGINAL_SESSION" 2>/dev/null || true

echo "[$(date -Is)] starting 2-way parallel remaining eval" | tee -a "$SWITCH_LOG"
scripts/_gpt/run_cx_fresh_eval_mseries_parallel_remaining.sh "$TS" 2>&1 | tee -a "$SWITCH_LOG"
