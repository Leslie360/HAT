#!/usr/bin/env bash
set -euo pipefail
ROOT="/home/qiaosir/projects/compute_vit"
PY="/home/qiaosir/miniconda3/envs/LLM/bin/python"
TS="${1:-$(date +%Y%m%d_%H%M%S)}"
STATUS_JSON="$ROOT/report_md/_gpt/json_gpt/cx_adc_extra_parallel_status.json"
cd "$ROOT"
mkdir -p logs/_gpt report_md/_gpt/json_gpt
cat > "$STATUS_JSON" <<EOF
{
  "phase": "parallel_running",
  "run_id": "CX-M5/CX-M6 ADC8 + CX-M1/CX-M3 ADC6",
  "message": "extra_adc_parallel_eval",
  "timestamp": "$(date -Is)",
  "log_timestamp": "$TS",
  "parallelism_added": 4
}
EOF
run_one() {
  local tag="$1" exp="$2" noise="$3" ckpt="$4" out="$5" bits="$6"
  "$PY" scripts/_gpt/eval_fresh_instances_adc_ablation.py \
    --checkpoint "$ckpt" \
    --exp-id "$exp" \
    --model-type tinyvit \
    --device cuda \
    --nl-ltp 2.0 \
    --nl-ltd -2.0 \
    --noise-mode "$noise" \
    --num-instances 10 \
    --mc-runs 5 \
    --adc-bits "$bits" \
    --adc-dnl-sigma 0.5 \
    --adc-calibration-batches 2 \
    --num-workers 2 \
    --output "$out" \
    > "logs/_gpt/${tag}_adc${bits}_fresheval_${TS}.log" 2>&1
}
run_one "cx-m5" "V3" "uniform" \
  "checkpoints/_gpt/postfix_m_series/cx_m5_standard_seed456/V3_hybrid_standard_noise_standard_train_best.pt" \
  "report_md/_gpt/json_gpt/cx_m5_adc_fresh_eval.json" 8 & p1=$!
run_one "cx-m6" "V4" "uniform" \
  "checkpoints/_gpt/postfix_m_series/cx_m6_ensemble_seed456/V4_hybrid_standard_noise_hat_best.pt" \
  "report_md/_gpt/json_gpt/cx_m6_adc_fresh_eval.json" 8 & p2=$!
run_one "cx-m1" "V3" "uniform" \
  "checkpoints/_gpt/postfix_m_series/cx_m1_standard_seed123/V3_hybrid_standard_noise_standard_train_best.pt" \
  "report_md/_gpt/json_gpt/cx_m1_adc6_fresh_eval.json" 6 & p3=$!
run_one "cx-m3" "V4" "proportional" \
  "checkpoints/_gpt/postfix_m_series/cx_m3_proportional_seed123/V4_hybrid_standard_noise_hat_best.pt" \
  "report_md/_gpt/json_gpt/cx_m3_adc6_fresh_eval.json" 6 & p4=$!
failed=0
for p in "$p1" "$p2" "$p3" "$p4"; do
  if ! wait "$p"; then failed=1; fi
done
if [[ "$failed" -eq 0 ]]; then phase="complete"; else phase="failed"; fi
cat > "$STATUS_JSON" <<EOF
{
  "phase": "$phase",
  "run_id": "CX-M5/CX-M6 ADC8 + CX-M1/CX-M3 ADC6",
  "message": "extra_adc_parallel_eval_done",
  "timestamp": "$(date -Is)",
  "log_timestamp": "$TS",
  "parallelism_added": 4
}
EOF
exit "$failed"
