#!/bin/bash
# Conditional 6-bit PCM multiseed follow-up. Use only after seed123 pilot passes.

set -euo pipefail
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:${LD_LIBRARY_PATH:-}
PROJECT=/home/qiaosir/projects/compute_vit
PYTHON=/home/qiaosir/miniconda3/envs/aihwkit/bin/python
cd "$PROJECT"
mkdir -p paper2_aihwkit_baseline/logs

for SEED in 456 789; do
  RUN="r11d_6bit_pcm_seed${SEED}"
  if [[ ! -f "paper2_aihwkit_baseline/checkpoints/${RUN}/training_history.json" ]]; then
    mkdir -p "paper2_aihwkit_baseline/checkpoints/${RUN}"
    LOG="paper2_aihwkit_baseline/logs/${RUN}_$(date +%Y%m%d_%H%M%S).log"
    echo "=== 6-bit PCM follow-up training: ${RUN} ===" | tee "$LOG"
    "$PYTHON" paper2_aihwkit_baseline/r11d4_train_pcm.py \
      --run-id "$RUN" \
      --seed "$SEED" \
      --epochs 100 \
      --batch-size 64 \
      --lr 0.001 \
      --wd 0.05 \
      --momentum 0.0 \
      --device cuda \
      --workers 0 \
      --save-dir "paper2_aihwkit_baseline/checkpoints/${RUN}" \
      --log-interval 1 \
      --inp-res 0.015625 \
      --out-res 0.015625 \
      --modifier-std-dev 0.10 \
      --early-stop-patience 0 \
      2>&1 | tee -a "$LOG"
    test -f "paper2_aihwkit_baseline/checkpoints/${RUN}/training_history.json"
    test -f "paper2_aihwkit_baseline/checkpoints/${RUN}/last.pt"
  else
    echo "=== 6-bit follow-up already has training_history.json; skipping training: ${RUN} ==="
  fi

  CKPT="paper2_aihwkit_baseline/checkpoints/${RUN}/best.pt"
  test -f "$CKPT"
  "$PYTHON" paper2_aihwkit_baseline/eval_aihwkit_fresh.py \
    --checkpoint "$CKPT" --n-fresh 10 --mc-repeats 5 --batch-size 64 --workers 0 --device cuda \
    --output "paper2_aihwkit_baseline/checkpoints/${RUN}/fresh_eval.json"
  "$PYTHON" paper2_aihwkit_baseline/eval_aihwkit_drift_extended.py \
    --checkpoint "$CKPT" --batch-size 64 --workers 0 --device cuda --drift-times 0 3600 86400 \
    --output "paper2_aihwkit_baseline/checkpoints/${RUN}/drift_eval.json"
done

echo "=== 6-bit PCM multiseed follow-up complete ==="
