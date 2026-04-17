#!/bin/bash
# P14-A: Flowers-102 V2 (no-noise) reviewer-facing control run.

set -euo pipefail

PYTHON_BIN="/home/qiaosir/miniconda3/envs/LLM/bin/python"
ROOT="/home/qiaosir/projects/compute_vit"
SEED="42"
SAVE_DIR="${ROOT}/checkpoints/_gpt/p14_flowers_v2"
TRAIN_LOG="${ROOT}/logs/_gpt/p14_flowers_v2_ablation.log"
EVAL_LOG="${ROOT}/logs/_gpt/p14_flowers_v2_eval.log"

echo "Starting P14-A: Flowers-102 V2 control (seed=${SEED})"

"${PYTHON_BIN}" -u "${ROOT}/train_tinyvit.py" \
  --dataset flowers102 \
  --experiment V2 \
  --epochs 100 \
  --batch-size 64 \
  --seed "${SEED}" \
  --pretrained \
  --amp \
  --save-dir "${SAVE_DIR}" \
  --num-workers 4 \
  2>&1 | tee "${TRAIN_LOG}"

echo "Evaluating Flowers-102 V2 control"
"${PYTHON_BIN}" -u "${ROOT}/train_tinyvit.py" \
  --dataset flowers102 \
  --experiment V2 \
  --mode eval \
  --batch-size 64 \
  --seed "${SEED}" \
  --pretrained \
  --amp \
  --checkpoint "${SAVE_DIR}/V2_hybrid_no_noise_best.pt" \
  --eval-runs 10 \
  2>&1 | tee "${EVAL_LOG}"

echo "P14-A complete. Summary:"
grep -A 5 "Summary" "${EVAL_LOG}" || true
