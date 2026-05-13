#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
PY="/home/qiaosir/miniconda3/bin/python"
STAMP="$(date +%Y%m%d_%H%M%S)"
MASTER_LOG="$ROOT/logs/overnight_drift_aware_batch_${STAMP}.log"

log() {
  echo "[$(date -Iseconds)] $*" | tee -a "$MASTER_LOG"
}

wait_for_local_gpu_lane() {
  log "Waiting for active local drift/retention GPU lanes to finish..."
  while pgrep -fa "eval_retention_protection_sweep.py|eval_resnet_retention_protection.py|eval_resnet_layer_sensitivity.py" >/dev/null; do
    sleep 30
  done
  log "No conflicting local GPU eval process detected."
}

run_seed456_drift_profile() {
  local tsv="$ROOT/thesis/results/drift_aware_sam/drift_vectors_profile_seed456_${STAMP}.tsv"
  local json="$ROOT/thesis/results/drift_aware_sam/drift_vectors_profile_seed456_${STAMP}.json"
  log "Running seed456 drift-vector profiling..."
  "$PY" "$ROOT/scripts/profile_drift_vectors.py" \
    --model_type tinyvit \
    --experiment V4 \
    --dataset cifar100 \
    --checkpoint_path "$ROOT/checkpoints/_ensemble/cifar100_seed456/V4_hybrid_standard_noise_hat_best.pt" \
    --device cuda \
    --times 0,1000,10000,86400 \
    --tsv_out "$tsv" \
    --json_out "$json" \
    2>&1 | tee -a "$MASTER_LOG"
  log "Seed456 drift profile done: $tsv"
}

build_seed456_drift_ranking() {
  local drift_tsv="$ROOT/thesis/results/drift_aware_sam/drift_vectors_profile_seed456_${STAMP}.tsv"
  local rank_tsv="$ROOT/thesis/results/drift_aware_sam/drift_aware_ranking_seed456_1000s_${STAMP}.tsv"
  log "Building seed456 drift-aware ranking..."
  "$PY" "$ROOT/scripts/build_drift_aware_ranking.py" \
    --drift_tsv "$drift_tsv" \
    --reference_sensitivity_tsv "$ROOT/thesis/results/mixed_precision/layer_sensitivity_full42_summary_20260510.tsv" \
    --retention_time 1000 \
    --output_tsv "$rank_tsv" \
    2>&1 | tee -a "$MASTER_LOG"
  log "Seed456 drift-aware ranking done: $rank_tsv"
}

run_seed456_drift_protection() {
  local rank_tsv="$ROOT/thesis/results/drift_aware_sam/drift_aware_ranking_seed456_1000s_${STAMP}.tsv"
  local raw_tsv="$ROOT/thesis/results/drift_aware_sam/drift_aware_protection_seed456_10x3_${STAMP}.tsv"
  local summary_tsv="$ROOT/thesis/results/drift_aware_sam/drift_aware_protection_seed456_10x3_summary_${STAMP}.tsv"
  log "Running seed456 full 10x3 drift-aware protection..."
  "$PY" "$ROOT/scripts/eval_retention_protection_sweep.py" \
    --model_type tinyvit \
    --experiment V4 \
    --dataset cifar100 \
    --checkpoint_path "$ROOT/checkpoints/_ensemble/cifar100_seed456/V4_hybrid_standard_noise_hat_best.pt" \
    --sensitivity_tsv "$rank_tsv" \
    --k_values 0,30,42 \
    --retention_times 0,1000,10000 \
    --num_instances 10 \
    --mc_runs 3 \
    --batch_size 128 \
    --device cuda \
    --base_seed 20260520 \
    --recalibrate_scale \
    --scale_d2d \
    --tsv_out "$raw_tsv" \
    --summary_out "$summary_tsv" \
    2>&1 | tee -a "$MASTER_LOG"
  log "Seed456 full 10x3 drift-aware protection done: $summary_tsv"
}

main() {
  log "Overnight drift-aware batch start."
  wait_for_local_gpu_lane
  run_seed456_drift_profile
  build_seed456_drift_ranking
  run_seed456_drift_protection
  log "Overnight drift-aware batch complete."
}

main "$@"
