#!/usr/bin/env bash
set -u
ROOT="/home/qiaosir/projects/compute_vit"
PY="/home/qiaosir/miniconda3/envs/LLM/bin/python"
SCRIPT="$ROOT/scripts/_gpt/empirical_mechanism_20260425.py"
LOG_DIR="$ROOT/logs/_gpt"
TS="${1:-$(date +%Y%m%d_%H%M%S)}"
mkdir -p "$LOG_DIR"
cd "$ROOT" || exit 1

pids=()
tags=()

launch_bg() {
  local tag="$1"; shift
  local log="$LOG_DIR/empirical_${tag}_${TS}.log"
  echo "[launch] $tag -> $log"
  "$PY" "$SCRIPT" "$@" >"$log" 2>&1 &
  local pid=$!
  pids+=("$pid")
  tags+=("$tag")
  echo "[pid] $tag=$pid"
}

launch_bg E3 --job cka --batch-size 128 --num-workers 2
launch_bg E2 --job d2d --batch-size 256 --num-workers 2 --masks 3
launch_bg E4 --job sensitivity --batch-size 256 --num-workers 2
launch_bg E5 --job avg --batch-size 256 --num-workers 2 --instances 10 --mc-runs 5

status=0
for i in "${!pids[@]}"; do
  pid="${pids[$i]}"
  tag="${tags[$i]}"
  if wait "$pid"; then
    echo "[done] $tag"
  else
    rc=$?
    echo "[fail] $tag rc=$rc"
    status=$rc
  fi
done

# Hessian uses second-order autograd. Keep it alone on GPU.
hlog="$LOG_DIR/empirical_E1_${TS}.log"
echo "[launch] E1 -> $hlog"
if "$PY" "$SCRIPT" --job hessian --batch-size 128 --num-workers 2 --hessian-batch 128 --lanczos-steps 50 --hessian-params analog >"$hlog" 2>&1; then
  echo "[done] E1 analog-param Hessian"
else
  rc=$?
  echo "[fail] E1 analog-param Hessian rc=$rc; retrying lighter head-param fallback" | tee -a "$hlog"
  "$PY" "$SCRIPT" --job hessian --batch-size 128 --num-workers 2 --hessian-batch 64 --lanczos-steps 50 --hessian-params head >>"$hlog" 2>&1 || status=$?
fi

rlog="$LOG_DIR/empirical_REPORT_${TS}.log"
echo "[launch] report -> $rlog"
"$PY" "$SCRIPT" --job report >"$rlog" 2>&1 || status=$?

echo "[complete] status=$status ts=$TS"
exit "$status"
