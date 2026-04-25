#!/usr/bin/env bash
# Auto-launch R2 after R1 completes successfully
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
R1_BEST="$ROOT/checkpoints/_gpt/r1_clean_anchor/V4_hybrid_standard_noise_hat_r1_clean_anchor_first_order_best.pt"
R1_TRAIN_JSON="$ROOT/report_md/_gpt/json_gpt/r1_clean_anchor_train.json"
R1_FRESH_JSON="$ROOT/report_md/_gpt/json_gpt/r1_clean_anchor_fresh_eval.json"

echo "[auto_chain] started at $(date --iso-8601=seconds)"
echo "[auto_chain] waiting for R1 completion..."

# Wait for R1 checkpoint and JSONs
while true; do
  if [ -f "$R1_BEST" ] && [ -f "$R1_TRAIN_JSON" ] && [ -f "$R1_FRESH_JSON" ]; then
    echo "[auto_chain] R1 outputs detected at $(date --iso-8601=seconds)"
    break
  fi
  sleep 120
done

# Quick sanity check on R1 fresh eval
R1_FRESH_MEAN=$(python3 -c "import json; d=json.load(open('$R1_FRESH_JSON')); print(d.get('cross_instance_mean', 0))" 2>/dev/null || echo "0")
echo "[auto_chain] R1 fresh-instance mean: ${R1_FRESH_MEAN}%"

# Only launch R2 if R1 fresh eval is healthy (>70%)
if (( $(echo "$R1_FRESH_MEAN > 70" | bc -l 2>/dev/null || echo "0") )); then
  echo "[auto_chain] R1 healthy. Launching R2..."
  cd "$ROOT"
  bash scripts/_gpt/launch_r2_so2_comparison_hostwsl.sh r2_so2_comparison
  echo "[auto_chain] R2 launched at $(date --iso-8601=seconds)"
else
  echo "[auto_chain] WARNING: R1 fresh mean ${R1_FRESH_MEAN}% is below 70%. NOT auto-launching R2."
  echo "[auto_chain] Human review required."
fi
