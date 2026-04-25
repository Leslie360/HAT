#!/usr/bin/env bash
set -euo pipefail
ROOT="/home/qiaosir/projects/compute_vit"
TS_BASE="$1"
SESSION="cx_adc_ablation_mseries_${TS_BASE}"
cd "$ROOT"
while true; do
  if [[ -s report_md/_gpt/json_gpt/cx_m1_adc_fresh_eval.json && \
        -s report_md/_gpt/json_gpt/cx_m2_adc_fresh_eval.json && \
        -s report_md/_gpt/json_gpt/cx_m3_adc_fresh_eval.json && \
        -s report_md/_gpt/json_gpt/cx_m4_adc_fresh_eval.json ]]; then
    echo "[$(date -Is)] phase1 JSONs exist; killing duplicate-capable session $SESSION"
    tmux kill-session -t "$SESSION" 2>/dev/null || true
    exit 0
  fi
  sleep 8
done
