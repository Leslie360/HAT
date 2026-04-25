#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
PY="/home/qiaosir/miniconda3/envs/LLM/bin/python"
SEED=123
TS="${1:-$(date +%Y%m%d_%H%M%S)}"

cd "$ROOT"

SAVE_DIR="checkpoints/_gpt/postfix_m_series/cx_m1_standard_seed${SEED}"
TRAIN_LOG="logs/_gpt/cx_m1_${TS}.log"
EVAL_LOG="logs/_gpt/cx_m1_fresh_eval_${TS}.log"
STATUS_JSON="report_md/_gpt/json_gpt/cx_m1_status.json"
TRAIN_JSON="report_md/_gpt/json_gpt/cx_m1_train_result.json"
TRAIN_CSV="report_md/_gpt/csv_gpt/cx_m1_train_result.csv"
TRAIN_MD="report_md/_gpt/CODEX_CX_M1_TRAIN_RESULT.md"
FRESH_JSON="report_md/_gpt/json_gpt/cx_m1_fresh_eval.json"
CKPT="$SAVE_DIR/V3_hybrid_standard_noise_standard_train_best.pt"

mkdir -p "$(dirname "$TRAIN_LOG")" "$(dirname "$STATUS_JSON")" "$(dirname "$TRAIN_CSV")" "$SAVE_DIR"

if [[ -f "$SAVE_DIR/V3_hybrid_standard_noise_standard_train_last.pt" || -f "$CKPT" ]]; then
  echo "Refusing to overwrite existing CX-M1 checkpoint directory: $SAVE_DIR" >&2
  exit 2
fi

write_status() {
  local phase="$1"
  local message="$2"
  cat > "$STATUS_JSON" <<EOF
{
  "task": "CX-M1",
  "phase": "$phase",
  "message": "$message",
  "seed": $SEED,
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

write_status "training" "started"

"$PY" train_tinyvit_ensemble.py \
  --mode train \
  --experiment V3 \
  --dataset cifar10 \
  --epochs 100 \
  --batch-size 64 \
  --num-workers 0 \
  --gpu-resize \
  --early-stop-patience 10 \
  --device cuda \
  --amp \
  --seed "$SEED" \
  --nl-ltp 2.0 \
  --nl-ltd -2.0 \
  --noise-mode uniform \
  --save-dir "$SAVE_DIR" \
  --log-path "$TRAIN_LOG" \
  --results-json-path "$TRAIN_JSON" \
  --results-csv-path "$TRAIN_CSV" \
  --results-md-path "$TRAIN_MD" \
  --log-interval 20

write_status "fresh_eval" "training_complete"

if [[ ! -f "$CKPT" ]]; then
  write_status "failed" "missing_best_checkpoint"
  echo "Missing checkpoint after training: $CKPT" >&2
  exit 3
fi

"$PY" eval_fresh_instances_postfix.py \
  --checkpoint "$CKPT" \
  --exp-id V3 \
  --model-type tinyvit \
  --device cuda \
  --nl-ltp 2.0 \
  --nl-ltd -2.0 \
  --noise-mode uniform \
  --num-instances 10 \
  --mc-runs 5 \
  --output "$FRESH_JSON" \
  > "$EVAL_LOG" 2>&1

write_status "complete" "fresh_eval_complete"
