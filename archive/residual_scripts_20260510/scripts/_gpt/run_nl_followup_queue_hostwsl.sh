#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
LOG="$ROOT/logs/_gpt/nl_followup_queue_hostwsl.log"
LOCK_DIR="$ROOT/tmp/nl_followup_queue_hostwsl.lock"
QKV_BEST="$ROOT/checkpoints/_gpt/nl_mitigation/v4_nl2_qkv_linear_comp/V4_hybrid_standard_noise_hat_nl2_qkv_linear_comp_best.pt"
ALL_BEST="$ROOT/checkpoints/_gpt/nl_mitigation/v4_nl2_all_linear_comp/V4_hybrid_standard_noise_hat_nl2_all_linear_comp_best.pt"
CADENCE_JSON="$ROOT/report_md/_gpt/json_gpt/fresh_instance_cadence_control.json"

cd "$ROOT"
mkdir -p logs/_gpt tmp
exec >> "$LOG" 2>&1

if ! mkdir "$LOCK_DIR" 2>/dev/null; then
  echo "[$(date '+%F %T')] another host-WSL NL follow-up queue is already active; exiting"
  exit 0
fi
trap 'rm -rf "$LOCK_DIR"' EXIT

echo "[$(date '+%F %T')] host-WSL NL follow-up queue started"

while pgrep -af 'run_tinyvit_groupwise_nl_comp.py.*_nl2_mlp_linear_comp' >/dev/null; do
  echo "[$(date '+%F %T')] waiting for active mlp-linear run to finish"
  sleep 60
done

if pgrep -af 'run_tinyvit_groupwise_nl_comp.py.*_nl2_qkv_linear_comp' >/dev/null; then
  echo "[$(date '+%F %T')] qkv-linear compensation already active; skipping queue launch"
elif [ -f "$QKV_BEST" ]; then
  echo "[$(date '+%F %T')] qkv-linear compensation already completed; skipping queue launch"
else
  echo "[$(date '+%F %T')] starting qkv-linear compensation run"
  bash "$ROOT/scripts/_gpt/run_task_v4_nl2_qkv_linear_comp.sh" "$(date +%Y%m%d_%H%M%S)_queue_qkv"
fi

if pgrep -af 'run_tinyvit_groupwise_nl_comp.py.*_nl2_all_linear_comp' >/dev/null; then
  echo "[$(date '+%F %T')] all-linear compensation already active; skipping queue launch"
elif [ -f "$ALL_BEST" ]; then
  echo "[$(date '+%F %T')] all-linear compensation already completed; skipping queue launch"
else
  echo "[$(date '+%F %T')] starting all-linear compensation run"
  bash "$ROOT/scripts/_gpt/run_task_v4_nl2_all_linear_comp.sh" "$(date +%Y%m%d_%H%M%S)_queue_all"
fi

if pgrep -af 'run_fresh_instance_cadence_control.py' >/dev/null; then
  echo "[$(date '+%F %T')] fresh-instance cadence control already active; skipping queue launch"
elif [ -f "$CADENCE_JSON" ]; then
  echo "[$(date '+%F %T')] fresh-instance cadence control already completed; skipping queue launch"
else
  echo "[$(date '+%F %T')] restarting fresh-instance cadence control evaluation"
  /home/qiaosir/miniconda3/envs/LLM/bin/python run_fresh_instance_cadence_control.py \
    --skip-train \
    --device cuda \
    --num-workers 0
fi

echo "[$(date '+%F %T')] host-WSL NL follow-up queue finished"
