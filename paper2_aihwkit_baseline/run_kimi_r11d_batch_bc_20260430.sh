#!/bin/bash
# Kimi local R11D Batch B/C queue.
# Batch B: PCMPresetDevice v2 comparison + eval.
# Batch C: clean no-modifier oracle + eval.

set -euo pipefail
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:${LD_LIBRARY_PATH:-}
PROJECT=/home/qiaosir/projects/compute_vit
PYTHON=/home/qiaosir/miniconda3/envs/aihwkit/bin/python
cd "$PROJECT"
mkdir -p paper2_aihwkit_baseline/logs

run_fresh_and_drift() {
  local run="$1"
  local ckpt="paper2_aihwkit_baseline/checkpoints/${run}/best.pt"
  test -f "$ckpt"

  local flog="paper2_aihwkit_baseline/logs/${run}_fresh_eval_$(date +%Y%m%d_%H%M%S).log"
  echo "=== Fresh eval: ${run} ===" | tee "$flog"
  "$PYTHON" paper2_aihwkit_baseline/eval_aihwkit_fresh.py \
    --checkpoint "$ckpt" \
    --n-fresh 10 \
    --mc-repeats 5 \
    --batch-size 64 \
    --workers 0 \
    --device cuda \
    --output "paper2_aihwkit_baseline/checkpoints/${run}/fresh_eval.json" \
    2>&1 | tee -a "$flog"
  test -f "paper2_aihwkit_baseline/checkpoints/${run}/fresh_eval.json"

  local dlog="paper2_aihwkit_baseline/logs/${run}_drift_eval_$(date +%Y%m%d_%H%M%S).log"
  echo "=== Drift eval: ${run} ===" | tee "$dlog"
  "$PYTHON" paper2_aihwkit_baseline/eval_aihwkit_drift_extended.py \
    --checkpoint "$ckpt" \
    --batch-size 64 \
    --workers 0 \
    --device cuda \
    --drift-times 0 3600 86400 \
    --output "paper2_aihwkit_baseline/checkpoints/${run}/drift_eval.json" \
    2>&1 | tee -a "$dlog"
  test -f "paper2_aihwkit_baseline/checkpoints/${run}/drift_eval.json"
}

# Batch B: strict PCMPresetDevice v2.
bash paper2_aihwkit_baseline/run_pcm_preset_comparison.sh
run_fresh_and_drift "t13v2_r11d_5a_pcm_PCMPresetDevice_seed123"
run_fresh_and_drift "t13v2_r11d_7_pcm_4bit_PCMPresetDevice_seed123"

# Batch C: clean no-modifier oracle under canonical r11d4_train_pcm.py.
ORACLE="r11d_5a_pcm_oracle_seed123_clean"
if [[ ! -f "paper2_aihwkit_baseline/checkpoints/${ORACLE}/training_history.json" ]]; then
  mkdir -p "paper2_aihwkit_baseline/checkpoints/${ORACLE}"
  LOG="paper2_aihwkit_baseline/logs/${ORACLE}_$(date +%Y%m%d_%H%M%S).log"
  echo "=== Clean oracle training: ${ORACLE} ===" | tee "$LOG"
  "$PYTHON" paper2_aihwkit_baseline/r11d4_train_pcm.py \
    --run-id "$ORACLE" \
    --seed 123 \
    --epochs 100 \
    --batch-size 64 \
    --lr 0.001 \
    --wd 0.05 \
    --momentum 0.0 \
    --device cuda \
    --workers 0 \
    --save-dir "paper2_aihwkit_baseline/checkpoints/${ORACLE}" \
    --log-interval 1 \
    --inp-res 0.00390625 \
    --out-res 0.00390625 \
    --modifier-std-dev 0.0 \
    --early-stop-patience 0 \
    2>&1 | tee -a "$LOG"
  test -f "paper2_aihwkit_baseline/checkpoints/${ORACLE}/training_history.json"
  test -f "paper2_aihwkit_baseline/checkpoints/${ORACLE}/last.pt"
else
  echo "=== Clean oracle already has training_history.json; skipping training: ${ORACLE} ==="
fi
run_fresh_and_drift "$ORACLE"

echo "=== Kimi R11D Batch B/C queue complete ==="
