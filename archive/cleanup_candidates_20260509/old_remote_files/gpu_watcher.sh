#!/bin/bash
# GPU Watcher — Auto-schedule pipeline, zero idle time
# Runs continuously in background, logs to gpu_watcher.log

set -e
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH
PROJECT=/home/qiaosir/projects/compute_vit
PYTHON=/home/qiaosir/miniconda3/envs/aihwkit/bin/python
EVAL_FRESH="$PYTHON paper2_aihwkit_baseline/eval_aihwkit_fresh.py"
EVAL_DRIFT="$PYTHON paper2_aihwkit_baseline/eval_aihwkit_drift.py"
LOG="$PROJECT/gpu_watcher.log"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG"
}

is_running() {
  pgrep -f "$1" > /dev/null 2>&1
}

wait_for_process() {
  local pattern="$1"
  log "Waiting for $pattern to finish..."
  while is_running "$pattern"; do
    sleep 60
  done
  log "$pattern finished."
}

run_eval() {
  local run_id="$1"
  local ckpt="$PROJECT/paper2_aihwkit_baseline/checkpoints/$run_id/best.pt"
  local out_dir="$PROJECT/paper2_aihwkit_baseline/checkpoints/$run_id"

  if [ ! -f "$ckpt" ]; then
    log "WARNING: $ckpt not found, skipping eval for $run_id"
    return 1
  fi

  log "Starting fresh eval for $run_id..."
  $EVAL_FRESH --checkpoint "$ckpt" --n-fresh 10 --batch-size 64 --device cuda --output "$out_dir/fresh_eval.json" 2>&1 | tee -a "$LOG"

  log "Starting drift eval for $run_id..."
  $EVAL_DRIFT --checkpoint "$ckpt" --batch-size 64 --device cuda --output "$out_dir/drift_eval.json" 2>&1 | tee -a "$LOG"

  log "Eval complete for $run_id."
}

# ===== MAIN PIPELINE =====
log "=== GPU Watcher started ==="

# Phase 1: Wait for both R11D-6b and R11D-7 to finish
wait_for_process "r11d_6b_pure_baseline"
R6B_DONE=$(date '+%H:%M:%S')
log "R11D-6b done at $R6B_DONE"

# Check if R11D-7 is still running
if is_running "r11d_7_pcm_4bit"; then
  log "R11D-7 still running, waiting..."
  wait_for_process "r11d_7_pcm_4bit"
fi
R7_DONE=$(date '+%H:%M:%S')
log "R11D-7 done at $R7_DONE"

# Phase 2: Sequential eval (single GPU)
log "=== Phase 2: Evals ==="
run_eval "r11d_6b_pure_baseline"
run_eval "r11d_7_pcm_4bit"

# Phase 3: Launch R11D-8
log "=== Phase 3: Launch R11D-8 ==="
cd "$PROJECT"
nohup bash paper2_aihwkit_baseline/run_r11d8_hat_pcm.sh > /tmp/r11d8_nohup.log 2>&1 &
R8_PID=$!
log "R11D-8 launched, PID=$R8_PID"

# Wait for R11D-8
wait_for_process "r11d_8_hat_inspired_pcm"
R8_DONE=$(date '+%H:%M:%S')
log "R11D-8 done at $R8_DONE"

# Phase 4: R11D-8 eval
log "=== Phase 4: R11D-8 Eval ==="
run_eval "r11d_8_hat_inspired_pcm"

# Phase 5: SWA continuation (if script exists)
if [ -f "$PROJECT/paper2_aihwkit_baseline/run_r11d8_swa.sh" ]; then
  log "=== Phase 5: SWA continuation ==="
  cd "$PROJECT"
  nohup bash paper2_aihwkit_baseline/run_r11d8_swa.sh > /tmp/r11d8_swa_nohup.log 2>&1 &
  wait_for_process "r11d_8_hat_inspired_pcm_swa"
  log "R11D-8-SWA done"
  run_eval "r11d_8_hat_inspired_pcm_swa"
else
  log "No SWA script found, skipping Phase 5"
fi

log "=== GPU Watcher pipeline COMPLETE ==="
