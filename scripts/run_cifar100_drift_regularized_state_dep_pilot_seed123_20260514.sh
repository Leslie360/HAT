#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
PY="/home/qiaosir/miniconda3/bin/python"
STAMP="$(date +%Y%m%d_%H%M%S)"
DRIFT_TAG="${DRIFT_TAG:-regw5e-3_t1000_state_dep}"
DRIFT_EPOCHS="${DRIFT_EPOCHS:-12}"
DRIFT_BATCH_SIZE="${DRIFT_BATCH_SIZE:-128}"
DRIFT_NUM_WORKERS="${DRIFT_NUM_WORKERS:-4}"
DRIFT_SEED="${DRIFT_SEED:-123}"
DRIFT_LR="${DRIFT_LR:-1e-4}"
DRIFT_REG_WEIGHT="${DRIFT_REG_WEIGHT:-0.005}"
DRIFT_REG_TIME="${DRIFT_REG_TIME:-1000}"
DRIFT_EARLY_STOP_PATIENCE="${DRIFT_EARLY_STOP_PATIENCE:-6}"
DRIFT_RET_BASE_SEED="${DRIFT_RET_BASE_SEED:-20260531}"
DRIFT_WARMSTART="${DRIFT_WARMSTART:-$ROOT/checkpoints/_ensemble/cifar100_seed123/V4_hybrid_standard_noise_hat_best.pt}"
DRIFT_REG_INCLUDE_SUBSTRINGS="${DRIFT_REG_INCLUDE_SUBSTRINGS:-stages.3}"
SAVE_DIR="$ROOT/checkpoints/_drift_aware/cifar100_seed123_${DRIFT_TAG}"
LOG="$ROOT/logs/cifar100_drift_regularized_pilot_seed123_${DRIFT_TAG}_${STAMP}.log"
PROFILE_TSV="$ROOT/thesis/results/drift_aware_sam/drift_vectors_profile_driftreg_seed123_${DRIFT_TAG}_${STAMP}.tsv"
PROFILE_JSON="$ROOT/thesis/results/drift_aware_sam/drift_vectors_profile_driftreg_seed123_${DRIFT_TAG}_${STAMP}.json"
RANK_TSV="$ROOT/thesis/results/drift_aware_sam/drift_aware_ranking_driftreg_seed123_1000s_${DRIFT_TAG}_${STAMP}.tsv"
RET_RAW="$ROOT/thesis/results/drift_aware_sam/drift_aware_retention_driftreg_seed123_10x3_${DRIFT_TAG}_${STAMP}.tsv"
RET_SUMMARY="$ROOT/thesis/results/drift_aware_sam/drift_aware_retention_driftreg_seed123_10x3_summary_${DRIFT_TAG}_${STAMP}.tsv"

mkdir -p "$SAVE_DIR" "$ROOT/logs"

{
  echo "[start] $(date -Iseconds)"
  echo "[save_dir] $SAVE_DIR"
  echo "[tag] $DRIFT_TAG"
  nvidia-smi --query-gpu=name,memory.total,memory.used,memory.free,utilization.gpu,temperature.gpu --format=csv,noheader

  "$PY" "$ROOT/src/compute_vit/train_tinyvit_ensemble.py" \
    --mode train \
    --experiment V4 \
    --dataset cifar100 \
    --epochs "$DRIFT_EPOCHS" \
    --batch-size "$DRIFT_BATCH_SIZE" \
    --device cuda \
    --data-root "$ROOT/data" \
    --num-workers "$DRIFT_NUM_WORKERS" \
    --pin-memory auto \
    --gpu-resize \
    --amp \
    --seed "$DRIFT_SEED" \
    --save-dir "$SAVE_DIR" \
    --warm-start-from "$DRIFT_WARMSTART" \
    --lr-override "$DRIFT_LR" \
    --drift-reg-weight "$DRIFT_REG_WEIGHT" \
    --drift-reg-time "$DRIFT_REG_TIME" \
    --drift-reg-state-dependent \
    --drift-reg-include-substrings "$DRIFT_REG_INCLUDE_SUBSTRINGS" \
    --log-interval 2 \
    --early-stop-patience "$DRIFT_EARLY_STOP_PATIENCE" \
    --results-json-path "$ROOT/thesis/results/drift_aware_sam/drift_reg_pilot_train_seed123_${DRIFT_TAG}_${STAMP}.json" \
    --results-csv-path "$ROOT/thesis/results/drift_aware_sam/drift_reg_pilot_train_seed123_${DRIFT_TAG}_${STAMP}.csv" \
    --results-md-path "$ROOT/coordination/agent_reports/Codex/DRIFT_REG_PILOT_TRAIN_SEED123_${DRIFT_TAG}_${STAMP}.md"

  "$PY" "$ROOT/src/compute_vit/train_tinyvit_ensemble.py" \
    --mode eval \
    --experiment V4 \
    --dataset cifar100 \
    --device cuda \
    --data-root "$ROOT/data" \
    --num-workers "$DRIFT_NUM_WORKERS" \
    --pin-memory auto \
    --gpu-resize \
    --amp \
    --eval-runs 3 \
    --checkpoint "$SAVE_DIR/V4_hybrid_standard_noise_hat_best.pt" \
    --results-json-path "$ROOT/thesis/results/drift_aware_sam/drift_reg_pilot_eval_seed123_${DRIFT_TAG}_${STAMP}.json" \
    --results-csv-path "$ROOT/thesis/results/drift_aware_sam/drift_reg_pilot_eval_seed123_${DRIFT_TAG}_${STAMP}.csv" \
    --results-md-path "$ROOT/coordination/agent_reports/Codex/DRIFT_REG_PILOT_EVAL_SEED123_${DRIFT_TAG}_${STAMP}.md"

  "$PY" "$ROOT/scripts/profile_drift_vectors.py" \
    --model_type tinyvit \
    --experiment V4 \
    --dataset cifar100 \
    --checkpoint_path "$SAVE_DIR/V4_hybrid_standard_noise_hat_best.pt" \
    --device cuda \
    --times 0,1000,10000,86400 \
    --state-dependent \
    --tsv_out "$PROFILE_TSV" \
    --json_out "$PROFILE_JSON"

  "$PY" "$ROOT/scripts/build_drift_aware_ranking.py" \
    --drift_tsv "$PROFILE_TSV" \
    --reference_sensitivity_tsv "$ROOT/thesis/results/mixed_precision/layer_sensitivity_full42_summary_20260510.tsv" \
    --retention_time 1000 \
    --output_tsv "$RANK_TSV"

  "$PY" "$ROOT/scripts/eval_retention_protection_sweep.py" \
    --model_type tinyvit \
    --experiment V4 \
    --dataset cifar100 \
    --checkpoint_path "$SAVE_DIR/V4_hybrid_standard_noise_hat_best.pt" \
    --sensitivity_tsv "$RANK_TSV" \
    --k_values 0,30,42 \
    --retention_times 0,1000,10000 \
    --num_instances 10 \
    --mc_runs 3 \
    --batch_size "$DRIFT_BATCH_SIZE" \
    --device cuda \
    --base_seed "$DRIFT_RET_BASE_SEED" \
    --state-dependent-retention \
    --recalibrate_scale \
    --scale_d2d \
    --tsv_out "$RET_RAW" \
    --summary_out "$RET_SUMMARY"

  echo "[done] $(date -Iseconds)"
} 2>&1 | tee "$LOG"
