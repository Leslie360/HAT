#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
PY="/home/qiaosir/miniconda3/envs/LLM/bin/python"
TS="${1:-$(date +%Y%m%d_%H%M%S)}"

cd "$ROOT"

QUEUE_LOG="logs/_gpt/cx_m_series_queue_${TS}.log"
STATUS_JSON="report_md/_gpt/json_gpt/cx_m_series_queue_status.json"
mkdir -p logs/_gpt report_md/_gpt/json_gpt report_md/_gpt/csv_gpt checkpoints/_gpt/postfix_m_series

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$QUEUE_LOG"
}

write_status() {
  local phase="$1"
  local task="$2"
  local message="$3"
  cat > "$STATUS_JSON" <<EOF
{
  "phase": "$phase",
  "task": "$task",
  "message": "$message",
  "queue_log": "$QUEUE_LOG",
  "timestamp": "$(date -Is)"
}
EOF
}

json_value() {
  local path="$1"
  local key="$2"
  "$PY" - "$path" "$key" <<'PY'
import json, sys
path, key = sys.argv[1], sys.argv[2]
with open(path, "r", encoding="utf-8") as fh:
    data = json.load(fh)
value = data
for part in key.split("."):
    value = value[part]
print(value)
PY
}

range_guard() {
  local task="$1"
  local json_path="$2"
  local mean
  mean="$(json_value "$json_path" cross_instance_mean)"
  log "$task fresh mean=$mean"
  "$PY" - "$task" "$mean" <<'PY'
import sys
task, mean = sys.argv[1], float(sys.argv[2])
if mean < 70.0 or mean > 90.0:
    raise SystemExit(f"{task} mean {mean:.4f}% outside [70, 90]; stop queue and escalate")
PY
}

wait_for_m1() {
  log "Waiting for active CX-M1 to complete fresh eval"
  write_status "waiting" "CX-M1" "waiting_for_existing_m1"
  while true; do
    if [[ -f report_md/_gpt/json_gpt/cx_m1_fresh_eval.json ]]; then
      log "Found cx_m1_fresh_eval.json"
      range_guard "CX-M1" "report_md/_gpt/json_gpt/cx_m1_fresh_eval.json"
      return
    fi
    if ! pgrep -af "launch_cx_m1_standard_seed123|train_tinyvit_ensemble.py .*postfix_m_series/cx_m1_standard_seed123|eval_fresh_instances_postfix.py .*cx_m1" >/dev/null; then
      log "ERROR: CX-M1 process not found and fresh eval JSON absent"
      write_status "failed" "CX-M1" "process_missing_without_fresh_json"
      exit 10
    fi
    sleep 300
  done
}

run_train_eval() {
  local task="$1"
  local experiment="$2"
  local noise_mode="$3"
  local seed="$4"
  local save_leaf="$5"
  local ckpt_name="$6"

  local save_dir="checkpoints/_gpt/postfix_m_series/${save_leaf}"
  local train_log="logs/_gpt/${task,,}_${TS}.log"
  local eval_log="logs/_gpt/${task,,}_fresh_eval_${TS}.log"
  local train_json="report_md/_gpt/json_gpt/${task,,}_train_result.json"
  local train_csv="report_md/_gpt/csv_gpt/${task,,}_train_result.csv"
  local train_md="report_md/_gpt/CODEX_${task}_TRAIN_RESULT.md"
  local fresh_json="report_md/_gpt/json_gpt/${task,,}_fresh_eval.json"
  local ckpt="${save_dir}/${ckpt_name}"
  local resume_args=()

  write_status "running" "$task" "training"
  log "Starting $task: experiment=$experiment noise=$noise_mode seed=$seed save_dir=$save_dir"

  mkdir -p "$save_dir"
  if [[ -f "$fresh_json" ]]; then
    log "$task fresh JSON already exists; skipping train/eval"
    range_guard "$task" "$fresh_json"
    return
  fi
  if [[ -f "${save_dir}/${ckpt_name/_best.pt/_last.pt}" || -f "$ckpt" ]]; then
    resume_args=(--resume-existing)
    log "$task found existing checkpoint state; resuming same from-scratch run"
  fi

  "$PY" train_tinyvit_ensemble.py \
    --mode train \
    --experiment "$experiment" \
    --dataset cifar10 \
    --epochs 100 \
    --batch-size 64 \
    --num-workers 0 \
    --device cuda \
    --amp \
    --seed "$seed" \
    --nl-ltp 2.0 \
    --nl-ltd -2.0 \
    --noise-mode "$noise_mode" \
    --save-dir "$save_dir" \
    --log-path "$train_log" \
    --results-json-path "$train_json" \
    --results-csv-path "$train_csv" \
    --results-md-path "$train_md" \
    --log-interval 20 \
    "${resume_args[@]}"

  if [[ ! -f "$ckpt" ]]; then
    log "ERROR: $task missing best checkpoint: $ckpt"
    write_status "failed" "$task" "missing_best_checkpoint"
    exit 11
  fi

  write_status "running" "$task" "fresh_eval"
  log "Starting $task fresh eval"
  "$PY" eval_fresh_instances_postfix.py \
    --checkpoint "$ckpt" \
    --exp-id "$experiment" \
    --model-type tinyvit \
    --device cuda \
    --nl-ltp 2.0 \
    --nl-ltd -2.0 \
    --noise-mode "$noise_mode" \
    --num-instances 10 \
    --mc-runs 5 \
    --output "$fresh_json" \
    > "$eval_log" 2>&1

  range_guard "$task" "$fresh_json"
  log "$task complete"
}

main() {
  log "CX-M-series queue started"
  wait_for_m1

  local m1_mean
  m1_mean="$(json_value report_md/_gpt/json_gpt/cx_m1_fresh_eval.json cross_instance_mean)"
  if "$PY" - "$m1_mean" <<'PY'
import sys
mean = float(sys.argv[1])
anchor = 82.6346
sigma = 0.5624475442207914
raise SystemExit(0 if abs(mean - anchor) > 2 * sigma else 1)
PY
  then
    log "CX-M1 differs from postfix_standard_hat by >2 sigma; launching conditional CX-M5"
    run_train_eval "CX_M5" "V3" "uniform" "456" "cx_m5_standard_seed456" "V3_hybrid_standard_noise_standard_train_best.pt"
  else
    log "CX-M1 within 2 sigma of postfix_standard_hat; CX-M5 not needed"
  fi

  run_train_eval "CX_M2" "V4" "uniform" "123" "cx_m2_ensemble_seed123" "V4_hybrid_standard_noise_hat_best.pt"
  run_train_eval "CX_M3" "V4" "proportional" "123" "cx_m3_proportional_seed123" "V4_hybrid_standard_noise_hat_best.pt"

  local m2_mean m3_mean
  m2_mean="$(json_value report_md/_gpt/json_gpt/cx_m2_fresh_eval.json cross_instance_mean)"
  m3_mean="$(json_value report_md/_gpt/json_gpt/cx_m3_fresh_eval.json cross_instance_mean)"
  if "$PY" - "$m2_mean" "$m3_mean" <<'PY'
import sys
m2, m3 = map(float, sys.argv[1:])
raise SystemExit(0 if m3 >= m2 else 1)
PY
  then
    log "CX-M3 is at least as good as uniform CX-M2; launching CX-M4 replication"
    run_train_eval "CX_M4" "V4" "proportional" "456" "cx_m4_proportional_seed456" "V4_hybrid_standard_noise_hat_best.pt"
  else
    log "CX-M3 underperforms uniform CX-M2; dropping proportional replication per rebuild fallback"
  fi

  write_status "complete" "CX-M-series" "queue_finished_or_conditionally_stopped"
  log "CX-M-series queue finished"
}

main "$@"
