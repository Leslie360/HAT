#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
PY="/home/qiaosir/miniconda3/envs/LLM/bin/python"
TS="${1:-$(date +%Y%m%d_%H%M%S)}"
STATUS_JSON="$ROOT/report_md/_gpt/json_gpt/cx_fresh_eval_mseries_status.json"

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
  "log_timestamp": "$TS"
}
EOF
}

run_eval() {
  local run_id="$1"
  local exp_id="$2"
  local noise_mode="$3"
  local checkpoint="$4"
  local output="$5"
  local log="logs/_gpt/${run_id,,}_fresheval_${TS}.log"

  write_status "running" "$run_id" "fresh_eval"
  "$PY" eval_fresh_instances_postfix.py \
    --checkpoint "$checkpoint" \
    --exp-id "$exp_id" \
    --model-type tinyvit \
    --device cuda \
    --nl-ltp 2.0 \
    --nl-ltd -2.0 \
    --noise-mode "$noise_mode" \
    --num-instances 10 \
    --mc-runs 5 \
    --output "$output" \
    > "$log" 2>&1
}

write_status "starting" "CX-MSERIES" "sequential fresh eval"

run_eval "CX-M1" "V3" "uniform" \
  "checkpoints/_gpt/postfix_m_series/cx_m1_standard_seed123/V3_hybrid_standard_noise_standard_train_best.pt" \
  "report_md/_gpt/json_gpt/cx_m1_fresh_eval.json"
run_eval "CX-M2" "V4" "uniform" \
  "checkpoints/_gpt/postfix_m_series/cx_m2_ensemble_seed123/V4_hybrid_standard_noise_hat_best.pt" \
  "report_md/_gpt/json_gpt/cx_m2_fresh_eval.json"
run_eval "CX-M3" "V4" "proportional" \
  "checkpoints/_gpt/postfix_m_series/cx_m3_proportional_seed123/V4_hybrid_standard_noise_hat_best.pt" \
  "report_md/_gpt/json_gpt/cx_m3_fresh_eval.json"
run_eval "CX-M4" "V4" "proportional" \
  "checkpoints/_gpt/postfix_m_series/cx_m4_proportional_seed456/V4_hybrid_standard_noise_hat_best.pt" \
  "report_md/_gpt/json_gpt/cx_m4_fresh_eval.json"
run_eval "CX-M5" "V3" "uniform" \
  "checkpoints/_gpt/postfix_m_series/cx_m5_standard_seed456/V3_hybrid_standard_noise_standard_train_best.pt" \
  "report_md/_gpt/json_gpt/cx_m5_fresh_eval.json"
run_eval "CX-M6" "V4" "uniform" \
  "checkpoints/_gpt/postfix_m_series/cx_m6_ensemble_seed456/V4_hybrid_standard_noise_hat_best.pt" \
  "report_md/_gpt/json_gpt/cx_m6_fresh_eval.json"

write_status "building_report" "CX-MSERIES" "build parity report"
"$PY" scripts/_gpt/build_mseries_parity_report.py

write_status "complete" "CX-MSERIES" "fresh eval and parity report complete"
