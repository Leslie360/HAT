#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
PY="/home/qiaosir/miniconda3/envs/LLM/bin/python"
TS="${1:-$(date +%Y%m%d_%H%M%S)}"
STATUS_JSON="$ROOT/report_md/_gpt/json_gpt/cx_adc_ablation_mseries_status.json"

cd "$ROOT"
mkdir -p logs/_gpt report_md/_gpt/json_gpt

write_status() {
  local phase="$1"
  local run_id="$2"
  local message="$3"
  cat > "$STATUS_JSON" <<EOF
{
  "phase": "$phase",
  "run_id": "$run_id",
  "message": "$message",
  "timestamp": "$(date -Is)",
  "log_timestamp": "$TS",
  "parallelism": 4,
  "adc_bits": 8,
  "adc_dnl_sigma": 0.5
}
EOF
}

run_adc_eval() {
  local run_id="$1"
  local exp_id="$2"
  local noise_mode="$3"
  local checkpoint="$4"
  local output="$5"
  local log="logs/_gpt/${run_id,,}_adc_fresheval_${TS}.log"

  "$PY" scripts/_gpt/eval_fresh_instances_adc_ablation.py \
    --checkpoint "$checkpoint" \
    --exp-id "$exp_id" \
    --model-type tinyvit \
    --device cuda \
    --nl-ltp 2.0 \
    --nl-ltd -2.0 \
    --noise-mode "$noise_mode" \
    --num-instances 10 \
    --mc-runs 5 \
    --adc-bits 8 \
    --adc-dnl-sigma 0.5 \
    --adc-calibration-batches 2 \
    --num-workers 2 \
    --output "$output" \
    > "$log" 2>&1
}

wait_all() {
  local failed=0
  for pid in "$@"; do
    if ! wait "$pid"; then
      failed=1
    fi
  done
  return "$failed"
}

write_status "parallel_running" "CX-M1/CX-M2/CX-M3/CX-M4" "adc_on_fresh_eval"
run_adc_eval "CX-M1" "V3" "uniform" \
  "checkpoints/_gpt/postfix_m_series/cx_m1_standard_seed123/V3_hybrid_standard_noise_standard_train_best.pt" \
  "report_md/_gpt/json_gpt/cx_m1_adc_fresh_eval.json" &
p1=$!
run_adc_eval "CX-M2" "V4" "uniform" \
  "checkpoints/_gpt/postfix_m_series/cx_m2_ensemble_seed123/V4_hybrid_standard_noise_hat_best.pt" \
  "report_md/_gpt/json_gpt/cx_m2_adc_fresh_eval.json" &
p2=$!
run_adc_eval "CX-M3" "V4" "proportional" \
  "checkpoints/_gpt/postfix_m_series/cx_m3_proportional_seed123/V4_hybrid_standard_noise_hat_best.pt" \
  "report_md/_gpt/json_gpt/cx_m3_adc_fresh_eval.json" &
p3=$!
run_adc_eval "CX-M4" "V4" "proportional" \
  "checkpoints/_gpt/postfix_m_series/cx_m4_proportional_seed456/V4_hybrid_standard_noise_hat_best.pt" \
  "report_md/_gpt/json_gpt/cx_m4_adc_fresh_eval.json" &
p4=$!
wait_all "$p1" "$p2" "$p3" "$p4"

write_status "parallel_running" "CX-M5/CX-M6" "adc_on_fresh_eval"
run_adc_eval "CX-M5" "V3" "uniform" \
  "checkpoints/_gpt/postfix_m_series/cx_m5_standard_seed456/V3_hybrid_standard_noise_standard_train_best.pt" \
  "report_md/_gpt/json_gpt/cx_m5_adc_fresh_eval.json" &
p5=$!
run_adc_eval "CX-M6" "V4" "uniform" \
  "checkpoints/_gpt/postfix_m_series/cx_m6_ensemble_seed456/V4_hybrid_standard_noise_hat_best.pt" \
  "report_md/_gpt/json_gpt/cx_m6_adc_fresh_eval.json" &
p6=$!
wait_all "$p5" "$p6"

write_status "complete" "CX-ADC-MSERIES" "adc_on_fresh_eval_complete"
