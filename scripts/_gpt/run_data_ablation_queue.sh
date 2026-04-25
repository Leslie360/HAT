#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-${PYTHON:-python}}"
STAMP="$(date +%Y%m%d_%H%M%S)"
LOG_DIR="${ROOT}/logs/_gpt"
QUEUE_LOG="${LOG_DIR}/data_ablation_cifar10_queue_${STAMP}.log"
R1_GATE_JSON="${R1_GATE_JSON:-${ROOT}/report_md/_gpt/json_gpt/r1_clean_anchor_fresh_eval.json}"

mkdir -p "${LOG_DIR}"
exec > >(tee -a "${QUEUE_LOG}") 2>&1

echo "[data-ablation] started $(date --iso-8601=seconds)"
echo "[data-ablation] root=${ROOT}"
echo "[data-ablation] python=${PYTHON_BIN}"
echo "[data-ablation] head=$(git -C "${ROOT}" rev-parse --short HEAD)"
echo "[data-ablation] r1_gate_json=${R1_GATE_JSON}"

for FRACTION in 0.1 0.25 0.5 1.0; do
  echo "[data-ablation] launching fraction=${FRACTION}"
  "${PYTHON_BIN}" "${ROOT}/scripts/_gpt/run_data_ablation_cifar10.py" \
    --data-fraction "${FRACTION}" \
    --epochs "${EPOCHS:-100}" \
    --batch-size "${BATCH_SIZE:-128}" \
    --seed "${SEED:-42}" \
    --num-workers "${NUM_WORKERS:-4}" \
    --python-bin "${PYTHON_BIN}" \
    --r1-gate-json "${R1_GATE_JSON}" \
    "$@"
done

echo "[data-ablation] completed $(date --iso-8601=seconds)"
