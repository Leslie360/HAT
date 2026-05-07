#!/usr/bin/env bash

set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PYTHON="${PYTHON:-python}"
MULTI_LOG_DIR="$ROOT/logs/_gpt/multi_seed"
MULTI_CKPT_DIR="$ROOT/checkpoints/_gpt/multi_seed"
DRIVER_LOG="$ROOT/logs/_gpt/fw1_p2_overnight_queue_20260409.log"
V8_TRAIN_LOG="$ROOT/logs/_gpt/train_v8_retention_aware_resume_20260409.log"
V8_EVAL_LOG="$ROOT/logs/_gpt/eval_v8_retention_aware_resume_20260409.log"

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

run_tinyvit_task() {
  local exp="$1"
  local seed="$2"
  local save_dir="$MULTI_CKPT_DIR/${exp}_s${seed}"
  local train_log="$MULTI_LOG_DIR/multi_seed_${exp}_s${seed}.log"
  local eval_log="$MULTI_LOG_DIR/multi_seed_${exp}_s${seed}_eval.log"
  local ckpt_name="V4_hybrid_standard_noise_hat_best.pt"
  local best_ckpt="$save_dir/$ckpt_name"

  mkdir -p "$save_dir"

  if train_done "$train_log" "$best_ckpt"; then
    driver_log "SKIP  | ${exp} seed=${seed} train already complete"
  else
    run_logged \
      "${exp} seed=${seed} train" \
      "$train_log" \
      "$PYTHON" -u train_tinyvit.py \
      --dataset cifar10 \
      --seed "$seed" \
      --batch-size 256 \
      --save-dir "$save_dir" \
      --mode train \
      --experiment "$exp" \
      --pretrained \
      --amp \
      --num-workers 4 \
      --resume-existing
  fi

  if train_done "$train_log" "$best_ckpt"; then
    if eval_done "$eval_log"; then
      driver_log "SKIP  | ${exp} seed=${seed} eval already complete"
    else
      run_logged \
        "${exp} seed=${seed} eval x10" \
        "$eval_log" \
        "$PYTHON" -u train_tinyvit.py \
        --dataset cifar10 \
        --seed "$seed" \
        --batch-size 256 \
        --checkpoint "$best_ckpt" \
        --eval-runs 10 \
        --mode eval \
        --experiment "$exp" \
        --pretrained \
        --amp
    fi
  else
    driver_log "WARN  | ${exp} seed=${seed} train incomplete; eval skipped"
  fi
}

run_convnext_task() {
  local exp="$1"
  local seed="$2"
  local save_dir="$MULTI_CKPT_DIR/${exp}_s${seed}"
  local train_log="$MULTI_LOG_DIR/multi_seed_${exp}_s${seed}.log"
  local eval_log="$MULTI_LOG_DIR/multi_seed_${exp}_s${seed}_eval.log"
  local ckpt_name
  if [[ "$exp" == "C1" ]]; then
    ckpt_name="C1_FP32_baseline_best.pt"
  else
    ckpt_name="C4_4bit_noise_HAT_best.pt"
  fi
  local best_ckpt="$save_dir/$ckpt_name"

  mkdir -p "$save_dir"

  if train_done "$train_log" "$best_ckpt"; then
    driver_log "SKIP  | ${exp} seed=${seed} train already complete"
  else
    run_logged \
      "${exp} seed=${seed} train" \
      "$train_log" \
      "$PYTHON" -u train_convnext.py \
      --dataset cifar10 \
      --seed "$seed" \
      --batch-size 512 \
      --save-dir "$save_dir" \
      --mode train \
      --experiments "$exp" \
      --amp \
      --num-workers 4 \
      --resume-existing
  fi

  if train_done "$train_log" "$best_ckpt"; then
    if eval_done "$eval_log"; then
      driver_log "SKIP  | ${exp} seed=${seed} eval already complete"
    else
      run_logged \
        "${exp} seed=${seed} eval x10" \
        "$eval_log" \
        "$PYTHON" -u train_convnext.py \
        --dataset cifar10 \
        --seed "$seed" \
        --batch-size 512 \
        --checkpoint "$best_ckpt" \
        --eval-runs 10 \
        --mode eval \
        --experiments "$exp" \
        --amp
    fi
  else
    driver_log "WARN  | ${exp} seed=${seed} train incomplete; eval skipped"
  fi
}

run_v8_resume() {
  local best_ckpt="$ROOT/checkpoints/V8_hybrid_hat_with_retention_aware_training_best.pt"

  run_logged \
    "V8 resume to 50 epochs" \
    "$V8_TRAIN_LOG" \
    "$PYTHON" -u train_tinyvit.py \
    --dataset cifar10 \
    --epochs 50 \
    --batch-size 256 \
    --save-dir checkpoints \
    --mode train \
    --experiment V8 \
    --amp \
    --num-workers 4 \
    --resume-existing

  if [[ -f "$best_ckpt" ]]; then
    if eval_done "$V8_EVAL_LOG"; then
      driver_log "SKIP  | V8 eval already complete"
    else
      run_logged \
        "V8 eval x10" \
        "$V8_EVAL_LOG" \
        "$PYTHON" -u train_tinyvit.py \
        --dataset cifar10 \
        --batch-size 256 \
        --checkpoint "$best_ckpt" \
        --eval-runs 10 \
        --mode eval \
        --experiment V8 \
        --amp
    fi
  else
    driver_log "WARN  | V8 best checkpoint missing after resume attempt; eval skipped"
  fi
}

main() {
  driver_log "Queue boot: FW-1 remaining seeds (V4/C1/C4) then P2 V8 resume"
  driver_log "Driver log: $DRIVER_LOG"
  driver_log "Multi-seed log dir: $MULTI_LOG_DIR"
  driver_log "V8 logs: $V8_TRAIN_LOG | $V8_EVAL_LOG"

  local failures=()

  for seed in 42 123 2026; do
    run_tinyvit_task V4 "$seed" || failures+=("V4 seed=$seed")
  done

  for seed in 42 123 2026; do
    run_convnext_task C1 "$seed" || failures+=("C1 seed=$seed")
  done

  for seed in 42 123 2026; do
    run_convnext_task C4 "$seed" || failures+=("C4 seed=$seed")
  done

  run_v8_resume || failures+=("V8 resume/eval")

  if [[ ${#failures[@]} -eq 0 ]]; then
    driver_log "Queue finished with no recorded failures."
  else
    driver_log "Queue finished with failures: ${failures[*]}"
  fi
}

main "$@"
