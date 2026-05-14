#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
PY="/home/qiaosir/miniconda3/bin/python"
LOG="$ROOT/logs/postprocess_drift_reg_pilot_seed123_$(date +%Y%m%d_%H%M%S).log"

latest_stamp() {
  local path
  path="$(ls -t "$ROOT"/thesis/results/drift_aware_sam/drift_reg_pilot_train_seed123_*.json 2>/dev/null | head -n 1 || true)"
  if [[ -z "$path" ]]; then
    return 1
  fi
  basename "$path" | sed -E 's/^drift_reg_pilot_train_seed123_(.*)\.json$/\1/'
}

log() {
  echo "[$(date -Iseconds)] $*" | tee -a "$LOG"
}

main() {
  log "Waiting for active drift-regularized pilot stamp..."
  local stamp=""
  while [[ -z "$stamp" ]]; do
    stamp="$(latest_stamp || true)"
    [[ -n "$stamp" ]] || sleep 15
  done
  log "Detected pilot stamp: $stamp"

  local summary="$ROOT/thesis/results/drift_aware_sam/drift_aware_retention_driftreg_seed123_10x3_summary_${stamp}.tsv"
  local baseline_ckpt="$ROOT/checkpoints/_ensemble/cifar100_seed123/V4_hybrid_standard_noise_hat_best.pt"
  local checkpoint="$ROOT/checkpoints/_drift_aware/cifar100_seed123_regw5e-3_t1000/V4_hybrid_standard_noise_hat_best.pt"
  local baseline="$ROOT/thesis/results/drift_aware_sam/drift_aware_protection_seed123_10x3_summary_20260514_011900.tsv"
  local baseline_eval_json="$ROOT/thesis/results/drift_aware_sam/drift_reg_baseline_eval_seed123_${stamp}.json"
  local baseline_eval_csv="$ROOT/thesis/results/drift_aware_sam/drift_reg_baseline_eval_seed123_${stamp}.csv"
  local baseline_eval_md="$ROOT/coordination/agent_reports/Codex/DRIFT_REG_BASELINE_EVAL_SEED123_${stamp}.md"
  local eval_json="$ROOT/thesis/results/drift_aware_sam/drift_reg_pilot_eval_seed123_${stamp}_metadatafix.json"
  local eval_csv="$ROOT/thesis/results/drift_aware_sam/drift_reg_pilot_eval_seed123_${stamp}_metadatafix.csv"
  local eval_md="$ROOT/coordination/agent_reports/Codex/DRIFT_REG_PILOT_EVAL_SEED123_${stamp}_METADATAFIX.md"
  local cmp_tsv="$ROOT/thesis/results/drift_aware_sam/drift_reg_vs_baseline_seed123_${stamp}.tsv"
  local source_cmp_tsv="$ROOT/thesis/results/drift_aware_sam/drift_reg_source_eval_compare_seed123_${stamp}.tsv"

  log "Waiting for retention summary: $summary"
  while [[ ! -f "$summary" ]]; do
    sleep 30
  done
  log "Retention summary detected."

  log "Running matched baseline source eval..."
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
    --checkpoint "$baseline_ckpt" \
    --results-json-path "$baseline_eval_json" \
    --results-csv-path "$baseline_eval_csv" \
    --results-md-path "$baseline_eval_md" \
    2>&1 | tee -a "$LOG"

  log "Running metadata-corrected source eval..."
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
    --checkpoint "$checkpoint" \
    --results-json-path "$eval_json" \
    --results-csv-path "$eval_csv" \
    --results-md-path "$eval_md" \
    2>&1 | tee -a "$LOG"

  log "Comparing retention summary against baseline..."
  "$PY" "$ROOT/scripts/compare_retention_summary_tsv.py" \
    --baseline "$baseline" \
    --candidate "$summary" \
    --baseline-label baseline_seed123 \
    --candidate-label drift_reg_seed123 \
    > "$cmp_tsv"

  log "Comparing matched source eval against baseline..."
  "$PY" - <<PY
import json
from pathlib import Path
baseline = json.loads(Path("$baseline_eval_json").read_text(encoding="utf-8"))[0]
candidate = json.loads(Path("$eval_json").read_text(encoding="utf-8"))[0]
with Path("$source_cmp_tsv").open("w", encoding="utf-8") as fh:
    fh.write("baseline_acc_mean\tcandidate_acc_mean\tdelta_pp\n")
    fh.write(f"{baseline['test_acc_mean']:.6f}\t{candidate['test_acc_mean']:.6f}\t{candidate['test_acc_mean'] - baseline['test_acc_mean']:+.6f}\n")
PY

  log "Postprocess complete."
  log "Baseline eval JSON: $baseline_eval_json"
  log "Eval JSON: $eval_json"
  log "Source compare TSV: $source_cmp_tsv"
  log "Compare TSV: $cmp_tsv"
}

main "$@"
