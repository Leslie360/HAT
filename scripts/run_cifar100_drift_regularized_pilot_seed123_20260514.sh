#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
PY="/home/qiaosir/miniconda3/bin/python"
STAMP="$(date +%Y%m%d_%H%M%S)"
SAVE_DIR="$ROOT/checkpoints/_drift_aware/cifar100_seed123_regw5e-3_t1000"
LOG="$ROOT/logs/cifar100_drift_regularized_pilot_seed123_${STAMP}.log"
PROFILE_TSV="$ROOT/thesis/results/drift_aware_sam/drift_vectors_profile_driftreg_seed123_${STAMP}.tsv"
PROFILE_JSON="$ROOT/thesis/results/drift_aware_sam/drift_vectors_profile_driftreg_seed123_${STAMP}.json"
RANK_TSV="$ROOT/thesis/results/drift_aware_sam/drift_aware_ranking_driftreg_seed123_1000s_${STAMP}.tsv"
RET_RAW="$ROOT/thesis/results/drift_aware_sam/drift_aware_retention_driftreg_seed123_10x3_${STAMP}.tsv"
RET_SUMMARY="$ROOT/thesis/results/drift_aware_sam/drift_aware_retention_driftreg_seed123_10x3_summary_${STAMP}.tsv"

mkdir -p "$SAVE_DIR"
mkdir -p "$ROOT/logs"

{
  echo "[start] $(date -Iseconds)"
  echo "[save_dir] $SAVE_DIR"
  nvidia-smi --query-gpu=name,memory.total,memory.used,memory.free,utilization.gpu,temperature.gpu --format=csv,noheader

  "$PY" "$ROOT/src/compute_vit/train_tinyvit_ensemble.py" \
    --mode train \
    --experiment V4 \
    --dataset cifar100 \
    --epochs 12 \
    --batch-size 128 \
    --device cuda \
    --data-root "$ROOT/data" \
    --num-workers 4 \
    --pin-memory auto \
    --gpu-resize \
    --amp \
    --seed 123 \
    --save-dir "$SAVE_DIR" \
    --warm-start-from "$ROOT/checkpoints/_ensemble/cifar100_seed123/V4_hybrid_standard_noise_hat_best.pt" \
    --lr-override 1e-4 \
    --drift-reg-weight 0.005 \
    --drift-reg-time 1000 \
    --log-interval 2 \
    --early-stop-patience 6 \
    --results-json-path "$ROOT/thesis/results/drift_aware_sam/drift_reg_pilot_train_seed123_${STAMP}.json" \
    --results-csv-path "$ROOT/thesis/results/drift_aware_sam/drift_reg_pilot_train_seed123_${STAMP}.csv" \
    --results-md-path "$ROOT/coordination/agent_reports/Codex/DRIFT_REG_PILOT_TRAIN_SEED123_${STAMP}.md"

  "$PY" "$ROOT/src/compute_vit/train_tinyvit_ensemble.py" \
    --mode eval \
    --experiment V4 \
    --dataset cifar100 \
    --device cuda \
    --data-root "$ROOT/data" \
    --num-workers 4 \
    --pin-memory auto \
    --gpu-resize \
    --amp \
    --eval-runs 3 \
    --checkpoint "$SAVE_DIR/V4_hybrid_standard_noise_hat_best.pt" \
    --results-json-path "$ROOT/thesis/results/drift_aware_sam/drift_reg_pilot_eval_seed123_${STAMP}.json" \
    --results-csv-path "$ROOT/thesis/results/drift_aware_sam/drift_reg_pilot_eval_seed123_${STAMP}.csv" \
    --results-md-path "$ROOT/coordination/agent_reports/Codex/DRIFT_REG_PILOT_EVAL_SEED123_${STAMP}.md"

  "$PY" "$ROOT/scripts/profile_drift_vectors.py" \
    --model_type tinyvit \
    --experiment V4 \
    --dataset cifar100 \
    --checkpoint_path "$SAVE_DIR/V4_hybrid_standard_noise_hat_best.pt" \
    --device cuda \
    --times 0,1000,10000,86400 \
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
    --batch_size 128 \
    --device cuda \
    --base_seed 20260522 \
    --recalibrate_scale \
    --scale_d2d \
    --tsv_out "$RET_RAW" \
    --summary_out "$RET_SUMMARY"

  echo "[done] $(date -Iseconds)"
} 2>&1 | tee "$LOG"
