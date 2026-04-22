#!/usr/bin/env bash

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PYTHON="${PYTHON:-python}"
MULTI_LOG_DIR="$ROOT/logs/_gpt/multi_seed"
MULTI_CKPT_DIR="$ROOT/checkpoints/_gpt/multi_seed"
DRIVER_LOG="$ROOT/logs/_gpt/fw1_c4_fix_queue_20260409_retry.log"
NUM_WORKERS=0

mkdir -p "$MULTI_LOG_DIR" "$MULTI_CKPT_DIR" "$(dirname "$DRIVER_LOG")"

timestamp() {
  date '+%Y-%m-%d %H:%M:%S'
}

driver_log() {
  echo "[$(timestamp)] $*" | tee -a "$DRIVER_LOG"
}

banner() {
  local logfile="$1"
  local title="$2"
  {
    echo
    echo "======================================================================"
    echo "[$(timestamp)] $title"
    echo "======================================================================"
  } >> "$logfile"
}

run_logged() {
  local desc="$1"
  local logfile="$2"
  shift 2

  driver_log "START | $desc"
  banner "$logfile" "$desc"
  (
    cd "$ROOT"
    "$@"
  ) 2>&1 | tee -a "$logfile"
  local rc=${PIPESTATUS[0]}
  if [[ $rc -eq 0 ]]; then
    driver_log "DONE  | $desc"
  else
    driver_log "FAIL  | $desc | rc=$rc"
  fi
  return "$rc"
}

train_done() {
  local train_log="$1"
  local best_ckpt="$2"
  [[ -f "$train_log" ]] && [[ -f "$best_ckpt" ]] && rg -q "Finished\\. Best accuracy:" "$train_log"
}

eval_done() {
  local eval_log="$1"
  [[ -f "$eval_log" ]] && rg -q "Eval summary:" "$eval_log"
}

run_c4_seed() {
  local seed="$1"
  local save_dir="$MULTI_CKPT_DIR/C4_fix_s${seed}"
  local train_log="$MULTI_LOG_DIR/multi_seed_C4_fix_s${seed}.log"
  local eval_log="$MULTI_LOG_DIR/multi_seed_C4_fix_s${seed}_eval.log"
  local best_ckpt="$save_dir/C4_4bit_noise_HAT_best.pt"

  mkdir -p "$save_dir"

  if train_done "$train_log" "$best_ckpt"; then
    driver_log "SKIP  | C4 seed=${seed} train already complete"
  else
    run_logged \
      "C4 seed=${seed} train (BS=128, no AMP)" \
      "$train_log" \
      "$PYTHON" -u train_convnext.py \
      --dataset cifar10 \
      --seed "$seed" \
      --batch-size 128 \
      --save-dir "$save_dir" \
      --mode train \
      --experiments C4 \
      --num-workers "$NUM_WORKERS"
  fi

  if train_done "$train_log" "$best_ckpt"; then
    if eval_done "$eval_log"; then
      driver_log "SKIP  | C4 seed=${seed} eval already complete"
    else
      run_logged \
        "C4 seed=${seed} eval x10" \
        "$eval_log" \
        "$PYTHON" -u train_convnext.py \
        --dataset cifar10 \
      --seed "$seed" \
      --batch-size 128 \
      --checkpoint "$best_ckpt" \
      --eval-runs 10 \
      --mode eval \
        --experiments C4
    fi
  else
    driver_log "WARN  | C4 seed=${seed} train incomplete; eval skipped"
  fi
}

main() {
  driver_log "Queue boot: C4 fix rerun with BS=128 and no AMP"
  driver_log "Driver log: $DRIVER_LOG"
  driver_log "Multi-seed log dir: $MULTI_LOG_DIR"

  local failures=()
  for seed in 42 123 2026; do
    run_c4_seed "$seed" || failures+=("C4 seed=$seed")
  done

  if [[ ${#failures[@]} -eq 0 ]]; then
    driver_log "Queue finished with no recorded failures."
  else
    driver_log "Queue finished with failures: ${failures[*]}"
  fi
}

main "$@"
