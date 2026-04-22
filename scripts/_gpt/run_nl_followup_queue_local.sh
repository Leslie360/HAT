#!/usr/bin/env bash
set -euo pipefail
ROOT="/home/qiaosir/projects/compute_vit"
LOG="$ROOT/logs/_gpt/nl_followup_queue_local.log"
cd "$ROOT"
mkdir -p logs/_gpt
exec >> "$LOG" 2>&1

echo "[$(date '+%F %T')] local NL follow-up queue started"
while /mnt/c/Windows/System32/wsl.exe -d Ubuntu-22.04 bash -lc "pgrep -af 'run_tinyvit_groupwise_nl_comp.py.*_nl2_mlp_linear_comp' >/dev/null"; do
  echo "[$(date '+%F %T')] waiting for active mlp-linear run to finish"
  sleep 60
done

echo "[$(date '+%F %T')] starting qkv-linear compensation run"
bash "$ROOT/scripts/_gpt/run_host_wsl_gpu.sh" "bash scripts/_gpt/run_task_v4_nl2_qkv_linear_comp.sh $(date +%Y%m%d_%H%M%S)_queue_qkv"

echo "[$(date '+%F %T')] starting all-linear compensation run"
bash "$ROOT/scripts/_gpt/run_host_wsl_gpu.sh" "bash scripts/_gpt/run_task_v4_nl2_all_linear_comp.sh $(date +%Y%m%d_%H%M%S)_queue_all"

echo "[$(date '+%F %T')] restarting fresh-instance cadence control evaluation"
bash "$ROOT/scripts/_gpt/run_host_wsl_gpu.sh" "/home/qiaosir/miniconda3/envs/LLM/bin/python run_fresh_instance_cadence_control.py --skip-train --device cuda --num-workers 0"

echo "[$(date '+%F %T')] local NL follow-up queue finished"
