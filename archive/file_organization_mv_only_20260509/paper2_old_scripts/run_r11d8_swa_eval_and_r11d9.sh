#!/bin/bash
# Pipeline: R11D-8-SWA eval -> R11D-9 training, zero GPU idle time

set -e
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH
PROJECT=/home/qiaosir/projects/compute_vit
PYTHON=/home/qiaosir/miniconda3/envs/aihwkit/bin/python
LOG="$PROJECT/gpu_pipeline_$(date +%Y%m%d_%H%M%S).log"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG"
}

CKPT_SWA="$PROJECT/paper2_aihwkit_baseline/checkpoints/r11d_8_hat_inspired_pcm_swa/best.pt"
OUT_SWA="$PROJECT/paper2_aihwkit_baseline/checkpoints/r11d_8_hat_inspired_pcm_swa"

# Phase 1: SWA fresh eval
log "=== Phase 1: R11D-8-SWA fresh eval ==="
$PYTHON "$PROJECT/paper2_aihwkit_baseline/eval_aihwkit_fresh.py" \
    --checkpoint "$CKPT_SWA" \
    --n-fresh 10 \
    --batch-size 64 \
    --device cuda \
    --output "$OUT_SWA/fresh_eval.json" \
    2>&1 | tee -a "$LOG"
log "Fresh eval done."

# Phase 2: SWA drift eval
log "=== Phase 2: R11D-8-SWA drift eval ==="
$PYTHON "$PROJECT/paper2_aihwkit_baseline/eval_aihwkit_drift.py" \
    --checkpoint "$CKPT_SWA" \
    --batch-size 64 \
    --device cuda \
    --output "$OUT_SWA/drift_eval.json" \
    2>&1 | tee -a "$LOG"
log "Drift eval done."

# Phase 3: R11D-9 training
log "=== Phase 3: Launch R11D-9 (4-bit pure baseline) ==="
bash "$PROJECT/paper2_aihwkit_baseline/run_r11d9_4bit_pure_baseline.sh" \
    2>&1 | tee -a "$LOG"
log "R11D-9 training launched/complete."

log "=== Pipeline complete ==="
