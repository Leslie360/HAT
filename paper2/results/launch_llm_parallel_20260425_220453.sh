#!/usr/bin/env bash
set -euo pipefail
cd /home/qiaosir/projects/compute_vit
PY=/home/qiaosir/miniconda3/envs/LLM/bin/python
mkdir -p logs/_gpt paper2/results
run_job() {
  local name="$1"; shift
  local log="logs/_gpt/${name}.log"
  echo "[launch] $name -> $log"
  nohup "$PY" -u paper2/src/train_llm_hybrid.py "$@" > "$log" 2>&1 &
  local pid=$!
  echo "$pid" > "paper2/results/${name}.pid"
  echo "[pid] $name $pid"
}
COMMON=(--model EleutherAI/pythia-410m-deduped --device cuda --dtype float32 --local-files-only --hybrid --high-precision-analog --train-scope last_block --max-length 64 --steps 200)
run_job w2_llm_hp_nonnoise_lb200_${ts} "${COMMON[@]}" --lr 1e-5
sleep 8
run_job w2_llm_hp_noise005002_r10_lr5e6_lb200_${ts} "${COMMON[@]}" --noise-enabled --sigma-d2d 0.05 --sigma-c2c 0.02 --resample-every 10 --lr 5e-6
sleep 8
run_job w2_llm_hp_noise010005_r10_lr1e6_lb200_${ts} "${COMMON[@]}" --noise-enabled --sigma-d2d 0.10 --sigma-c2c 0.05 --resample-every 10 --lr 1e-6
