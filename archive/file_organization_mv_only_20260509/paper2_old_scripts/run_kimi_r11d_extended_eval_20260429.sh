#!/bin/bash
# Kimi R11D next eval queue: extended drift + combined fresh+drift.
# No new training is launched by this script.

set -euo pipefail
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:${LD_LIBRARY_PATH:-}
PROJECT=/home/qiaosir/projects/compute_vit
PYTHON=/home/qiaosir/miniconda3/envs/aihwkit/bin/python
cd "$PROJECT"
mkdir -p paper2_aihwkit_baseline/logs

RUNS=(
  r11d_7_pcm_4bit_seed123
  r11d_7_pcm_4bit_seed456_clean
  r11d_7_pcm_4bit_seed789
  r11d_5a_pcm_seed123
  r11d_5a_pcm_seed456
  r11d_5a_pcm_seed789
)

for RUN in "${RUNS[@]}"; do
  CKPT="paper2_aihwkit_baseline/checkpoints/${RUN}/best.pt"
  OUT="paper2_aihwkit_baseline/checkpoints/${RUN}/extended_drift_eval.json"
  LOG="paper2_aihwkit_baseline/logs/${RUN}_extended_drift_$(date +%Y%m%d_%H%M%S).log"
  test -f "$CKPT"
  echo "=== Extended drift eval: $RUN ===" | tee "$LOG"
  "$PYTHON" paper2_aihwkit_baseline/eval_aihwkit_drift_extended.py \
    --checkpoint "$CKPT" \
    --batch-size 64 \
    --workers 0 \
    --device cuda \
    --drift-times 0 600 1800 3600 10800 21600 43200 86400 172800 259200 \
    --output "$OUT" \
    2>&1 | tee -a "$LOG"
  test -f "$OUT"
done

for RUN in "${RUNS[@]}"; do
  CKPT="paper2_aihwkit_baseline/checkpoints/${RUN}/best.pt"
  OUT="paper2_aihwkit_baseline/checkpoints/${RUN}/fresh_drift_eval.json"
  LOG="paper2_aihwkit_baseline/logs/${RUN}_fresh_drift_$(date +%Y%m%d_%H%M%S).log"
  test -f "$CKPT"
  echo "=== Fresh+drift eval: $RUN ===" | tee "$LOG"
  "$PYTHON" paper2_aihwkit_baseline/eval_aihwkit_fresh_drift.py \
    --checkpoint "$CKPT" \
    --drift-times 0 3600 86400 \
    --n-fresh 5 \
    --mc-repeats 3 \
    --batch-size 64 \
    --workers 0 \
    --device cuda \
    --output "$OUT" \
    2>&1 | tee -a "$LOG"
  test -f "$OUT"
done

echo "=== Kimi R11D extended eval queue complete ==="
