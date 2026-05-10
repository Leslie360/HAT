#!/usr/bin/env bash
# R11D-4: AIHWKit PCM Device Model — launch script
# Trains Tiny-ViT-5M on CIFAR-10 with PCMPresetUnitCell, then runs fresh eval.
set -euo pipefail

cd /home/qiaosir/projects/compute_vit
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:${LD_LIBRARY_PATH:-}
PY=/home/qiaosir/miniconda3/envs/aihwkit/bin/python

RUN_ID="r11d_4_pcm"
OUT_DIR="paper2_aihwkit_baseline/checkpoints/${RUN_ID}"
LOG_DIR="paper2_aihwkit_baseline/logs"
mkdir -p "${OUT_DIR}" "${LOG_DIR}"

TS=$(date +%Y%m%d_%H%M%S)
TRAIN_LOG="${LOG_DIR}/${RUN_ID}_${TS}.log"

echo "[r11d_4_pcm] $(date -Is) — launching training"

nohup "${PY}" paper2_aihwkit_baseline/r11d4_train_pcm.py \
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
    2>&1 | tee "${TRAIN_LOG}" &

TRAIN_PID=$!
echo "[r11d_4_pcm] Train PID: ${TRAIN_PID} (log: ${TRAIN_LOG})"

# Wait for training to finish
wait "${TRAIN_PID}"
TRAIN_RC=$?
echo "[r11d_4_pcm] Training exit code: ${TRAIN_RC}"

# Check training result
if [[ ! -s "${OUT_DIR}/best.pt" ]]; then
    echo "[r11d_4_pcm] FATAL: best.pt not found after training (exit ${TRAIN_RC})"
    exit 1
fi

echo "[r11d_4_pcm] best.pt found, launching fresh eval (10 instances × 5 MC)"

EVAL_LOG="${LOG_DIR}/${RUN_ID}_fresh_eval_${TS}.log"
"${PY}" paper2_aihwkit_baseline/eval_aihwkit_fresh.py \
    --checkpoint "${OUT_DIR}/best.pt" \
    --n-fresh 10 \
    --mc-repeats 5 \
    --workers 0 \
    --device cuda \
    --output "${OUT_DIR}/fresh_eval.json" \
    2>&1 | tee "${EVAL_LOG}"

EVAL_RC=$?

if [[ -s "${OUT_DIR}/fresh_eval.json" ]]; then
    MEAN=$("${PY}" -c "import json; print(json.load(open('${OUT_DIR}/fresh_eval.json')).get('mean','?'))")
    STD=$("${PY}" -c "import json; print(json.load(open('${OUT_DIR}/fresh_eval.json')).get('std','?'))")
    echo "[r11d_4_pcm] Fresh eval mean=${MEAN} std=${STD}"
else
    echo "[r11d_4_pcm] Fresh eval output missing (eval RC=${EVAL_RC})"
fi

echo "[r11d_4_pcm] $(date -Is) — complete"
