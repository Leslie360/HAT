#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

PY="${PY:-/home/qiaosir/miniconda3/envs/LLM/bin/python}"
TS="${TS:-$(date +%Y%m%d_%H%M%S)}"
LOG_DIR="logs/_gpt"
JSON_DIR="report_md/_gpt/json_gpt"
STATUS="$JSON_DIR/cx_adc_stage2_status.json"
mkdir -p "$LOG_DIR" "$JSON_DIR"

declare -A EXP=(
  [1]=V3
  [2]=V4
  [3]=V4
  [4]=V4
  [5]=V3
  [6]=V4
)

declare -A NOISE=(
  [1]=uniform
  [2]=uniform
  [3]=proportional
  [4]=proportional
  [5]=uniform
  [6]=uniform
)

declare -A CKPT=(
  [1]="checkpoints/_gpt/postfix_m_series/cx_m1_standard_seed123/V3_hybrid_standard_noise_standard_train_best.pt"
  [2]="checkpoints/_gpt/postfix_m_series/cx_m2_ensemble_seed123/V4_hybrid_standard_noise_hat_best.pt"
  [3]="checkpoints/_gpt/postfix_m_series/cx_m3_proportional_seed123/V4_hybrid_standard_noise_hat_best.pt"
  [4]="checkpoints/_gpt/postfix_m_series/cx_m4_proportional_seed456/V4_hybrid_standard_noise_hat_best.pt"
  [5]="checkpoints/_gpt/postfix_m_series/cx_m5_standard_seed456/V3_hybrid_standard_noise_standard_train_best.pt"
  [6]="checkpoints/_gpt/postfix_m_series/cx_m6_ensemble_seed456/V4_hybrid_standard_noise_hat_best.pt"
)

write_status() {
  local phase="$1"
  local msg="$2"
  shift 2 || true
  "$PY" - "$STATUS" "$phase" "$msg" "$TS" "$@" <<'PY'
import json, sys
from datetime import datetime, timezone, timedelta
path, phase, msg, ts, *extra = sys.argv[1:]
status = {
    "phase": phase,
    "message": msg,
    "timestamp": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
    "log_timestamp": ts,
    "parallelism": 4,
    "adc_bits": 8,
    "adc_dnl_sigma": 0.5,
    "adc_calibration_scope": "per_instance",
    "protocol": "10 fresh instances x 5 MC runs per checkpoint",
    "outputs_expected": [f"report_md/_gpt/json_gpt/cx_m{i}_adc_perinstance_fresh_eval.json" for i in range(1, 7)],
}
if extra:
    status["extra"] = extra
with open(path, "w", encoding="utf-8") as fh:
    json.dump(status, fh, indent=2)
PY
}

run_one() {
  local n="$1"
  local log="$LOG_DIR/cx-m${n}_adc_perinstance_fresheval_${TS}.log"
  local out="$JSON_DIR/cx_m${n}_adc_perinstance_fresh_eval.json"
  echo "[$(date '+%F %T')] START CX-M${n} exp=${EXP[$n]} noise=${NOISE[$n]} out=$out"
  stdbuf -oL -eL "$PY" scripts/_gpt/eval_fresh_instances_adc_ablation.py \
    --checkpoint "${CKPT[$n]}" \
    --exp-id "${EXP[$n]}" \
    --device cuda \
    --num-instances 10 \
    --mc-runs 5 \
    --nl-ltp 2.0 \
    --nl-ltd -2.0 \
    --noise-mode "${NOISE[$n]}" \
    --adc-bits 8 \
    --adc-dnl-sigma 0.5 \
    --adc-calibration-batches 2 \
    --num-workers 2 \
    --output "$out" \
    > "$log" 2>&1
  echo "[$(date '+%F %T')] DONE CX-M${n} log=$log"
}

write_status running "stage2_adc_perinstance_wave1_m1_m4"
run_one 1 & p1=$!
run_one 2 & p2=$!
run_one 3 & p3=$!
run_one 4 & p4=$!
wait "$p1" "$p2" "$p3" "$p4"

write_status running "stage2_adc_perinstance_wave2_m5_m6"
run_one 5 & p5=$!
run_one 6 & p6=$!
wait "$p5" "$p6"

write_status complete "stage2_adc_perinstance_eval_done"
