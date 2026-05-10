#!/bin/bash
# P14-B: CIFAR-10 data-volume ablation for Tiny-ViT V4

set -euo pipefail

PYTHON_BIN="${PYTHON_BIN:-${PYTHON:-python}}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SEED=42
FRACTIONS=("0.10" "0.25" "0.50" "1.00")

echo "Starting P14-B: Tiny-ViT V4 CIFAR-10 data-fraction ablation"

for FRACTION in "${FRACTIONS[@]}"; do
  FRACTION_TAG="${FRACTION/./p}"
  SAVE_DIR="${ROOT}/checkpoints/_gpt/tinyvit_data_ablation/v4_f${FRACTION_TAG}_s${SEED}"
  TRAIN_LOG="${ROOT}/logs/_gpt/train_tinyvit_cifar10_v4_datafrac_${FRACTION_TAG}_s${SEED}_gpt.log"
  EVAL_LOG="${ROOT}/logs/_gpt/eval_tinyvit_cifar10_v4_datafrac_${FRACTION_TAG}_s${SEED}_gpt.log"

  echo "Training V4 with data_fraction=${FRACTION} (seed=${SEED})"
  "${PYTHON_BIN}" -u "${ROOT}/train_tinyvit.py" \
    --dataset cifar10 \
    --experiment V4 \
    --epochs 100 \
    --batch-size 128 \
    --seed "${SEED}" \
    --pretrained \
    --amp \
    --data-fraction "${FRACTION}" \
    --save-dir "${SAVE_DIR}" \
    --num-workers 4 \
    2>&1 | tee "${TRAIN_LOG}"

  echo "Evaluating V4 with data_fraction=${FRACTION} (seed=${SEED})"
  "${PYTHON_BIN}" -u "${ROOT}/train_tinyvit.py" \
    --dataset cifar10 \
    --experiment V4 \
    --mode eval \
    --batch-size 128 \
    --seed "${SEED}" \
    --pretrained \
    --amp \
    --data-fraction "${FRACTION}" \
    --checkpoint "${SAVE_DIR}/V4_hybrid_standard_noise_hat_best.pt" \
    --eval-runs 10 \
    2>&1 | tee "${EVAL_LOG}"
done

echo "P14-B data ablation complete."
