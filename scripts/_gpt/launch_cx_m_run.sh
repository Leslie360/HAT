#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 6 ]]; then
  echo "Usage: $0 TASK EXPERIMENT NOISE_MODE SEED SAVE_LEAF CKPT_NAME [TIMESTAMP] [NUM_WORKERS]" >&2
  exit 2
fi

ROOT="/home/qiaosir/projects/compute_vit"
PY="/home/qiaosir/miniconda3/envs/LLM/bin/python"
TASK="$1"
EXPERIMENT="$2"
NOISE_MODE="$3"
SEED="$4"
SAVE_LEAF="$5"
CKPT_NAME="$6"
TS="${7:-$(date +%Y%m%d_%H%M%S)}"
NUM_WORKERS="${8:-0}"

cd "$ROOT"

SAVE_DIR="checkpoints/_gpt/postfix_m_series/${SAVE_LEAF}"
TASK_LC="$(echo "$TASK" | tr '[:upper:]' '[:lower:]' | tr '-' '_')"
TRAIN_LOG="logs/_gpt/${TASK_LC}_${TS}.log"
EVAL_LOG="logs/_gpt/${TASK_LC}_fresh_eval_${TS}.log"
STATUS_JSON="report_md/_gpt/json_gpt/${TASK_LC}_status.json"
TRAIN_JSON="report_md/_gpt/json_gpt/${TASK_LC}_train_result.json"
TRAIN_CSV="report_md/_gpt/csv_gpt/${TASK_LC}_train_result.csv"
TRAIN_MD="report_md/_gpt/CODEX_${TASK}_TRAIN_RESULT.md"
FRESH_JSON="report_md/_gpt/json_gpt/${TASK_LC}_fresh_eval.json"
CKPT="$SAVE_DIR/$CKPT_NAME"

mkdir -p "$(dirname "$TRAIN_LOG")" "$(dirname "$STATUS_JSON")" "$(dirname "$TRAIN_CSV")" "$SAVE_DIR"

write_status() {
  local phase="$1"
  local message="$2"
  cat > "$STATUS_JSON" <<EOF
{
  "task": "$TASK",
  "phase": "$phase",
  "message": "$message",
  "experiment": "$EXPERIMENT",
  "noise_mode": "$NOISE_MODE",
  "seed": $SEED,
  "num_workers": $NUM_WORKERS,
  "gpu_resize": true,
  "early_stop_patience": 10,
  "save_dir": "$SAVE_DIR",
  "train_log": "$TRAIN_LOG",
  "eval_log": "$EVAL_LOG",
  "fresh_json": "$FRESH_JSON",
  "timestamp": "$(date -Is)"
}
EOF
}

resume_args=()
last_ckpt="${SAVE_DIR}/${CKPT_NAME/_best.pt/_last.pt}"
if [[ -f "$FRESH_JSON" ]]; then
  write_status "complete" "fresh_json_already_exists"
  echo "$TASK fresh eval already exists: $FRESH_JSON"
  exit 0
fi
if [[ -f "$last_ckpt" || -f "$CKPT" ]]; then
  resume_args=(--resume-existing)
fi

write_status "training" "started"

"$PY" train_tinyvit_ensemble.py \
  --mode train \
  --experiment "$EXPERIMENT" \
  --dataset cifar10 \
  --epochs 100 \
  --batch-size 64 \
  --num-workers "$NUM_WORKERS" \
  --pin-memory off \
  --gpu-resize \
  --early-stop-patience 10 \
  --device cuda \
  --amp \
  --seed "$SEED" \
  --nl-ltp 2.0 \
  --nl-ltd -2.0 \
  --noise-mode "$NOISE_MODE" \
  --save-dir "$SAVE_DIR" \
  --log-path "$TRAIN_LOG" \
  --results-json-path "$TRAIN_JSON" \
  --results-csv-path "$TRAIN_CSV" \
  --results-md-path "$TRAIN_MD" \
  --log-interval 20 \
  "${resume_args[@]}"

write_status "fresh_eval" "training_complete"

if [[ ! -f "$CKPT" ]]; then
  write_status "failed" "missing_best_checkpoint"
  echo "Missing checkpoint after training: $CKPT" >&2
  exit 3
fi

"$PY" eval_fresh_instances_postfix.py \
  --checkpoint "$CKPT" \
  --exp-id "$EXPERIMENT" \
  --model-type tinyvit \
  --device cuda \
  --nl-ltp 2.0 \
  --nl-ltd -2.0 \
  --noise-mode "$NOISE_MODE" \
  --num-instances 10 \
  --mc-runs 5 \
  --output "$FRESH_JSON" \
  > "$EVAL_LOG" 2>&1

write_status "complete" "fresh_eval_complete"
