#!/bin/bash
set -euo pipefail
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:/usr/lib/wsl/lib:${LD_LIBRARY_PATH:-}
PY=/home/qiaosir/miniconda3/envs/aihwkit/bin/python

cd /home/qiaosir/projects/compute_vit

RUN_ID="r11d_4_pcm_fixed"
OUT_DIR="paper2_aihwkit_baseline/checkpoints/${RUN_ID}"
LOG_DIR="paper2_aihwkit_baseline/logs"
mkdir -p "${OUT_DIR}" "${LOG_DIR}"

TS=$(date +%Y%m%d_%H%M%S)
TRAIN_LOG="${LOG_DIR}/${RUN_ID}_${TS}.log"
EVAL_LOG="${LOG_DIR}/${RUN_ID}_fresh_eval_${TS}.log"
DRIFT_LOG="${LOG_DIR}/${RUN_ID}_drift_eval_${TS}.log"

echo "[${RUN_ID}] $(date -Is) — STEP 1: training with AnalogSGD"
"${PY}" paper2_aihwkit_baseline/r11d4_train_pcm.py \
  --run-id "${RUN_ID}" \
  --seed 42 \
  --epochs 100 \
  --batch-size 64 \
  --lr 5e-4 \
  --wd 0.05 \
  --workers 0 \
  --device cuda \
  --save-dir "${OUT_DIR}" \
  --log-interval 1 \
  --inp-res 0.00390625 \
  --out-res 0.00390625 \
  --modifier-std-dev 0.10 \
  --early-stop-patience 20 \
  2>&1 | tee "${TRAIN_LOG}"

echo "[${RUN_ID}] $(date -Is) — STEP 2: fresh eval (10 instances x 5 MC)"
"${PY}" paper2_aihwkit_baseline/eval_aihwkit_fresh.py \
  --checkpoint "${OUT_DIR}/best.pt" \
  --n-fresh 10 \
  --mc-repeats 5 \
  --workers 0 \
  --device cuda \
  --output "${OUT_DIR}/fresh_eval.json" \
  2>&1 | tee "${EVAL_LOG}"

echo "[${RUN_ID}] $(date -Is) — STEP 3: drift eval (t=0s, 1h, 24h)"
"${PY}" paper2_aihwkit_baseline/eval_aihwkit_drift.py \
  --checkpoint "${OUT_DIR}/best.pt" \
  --workers 0 \
  --device cuda \
  --output "${OUT_DIR}/drift_eval.json" \
  2>&1 | tee "${DRIFT_LOG}"

echo "[${RUN_ID}] $(date -Is) — complete"
