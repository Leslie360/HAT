#!/usr/bin/env bash
set -uo pipefail
cd /home/qiaosir/projects/compute_vit
PY=/home/qiaosir/miniconda3/envs/LLM/bin/python
RUN_ID=20260425_220737
mkdir -p logs/_gpt paper2/results
run_job() {
  local name="$1"; shift
  local log="logs/_gpt/${name}.log"
  echo "[launch] $name -> $log"
  ("$PY" -u paper2/src/train_llm_hybrid.py "$@" > "$log" 2>&1; code=$?; echo "$code" > "paper2/results/${name}.exit"; echo "[exit] $name $code") &
  echo "$!" > "paper2/results/${name}.pid"
}
COMMON=(--model EleutherAI/pythia-410m-deduped --device cuda --dtype float32 --local-files-only --hybrid --high-precision-analog --train-scope last_block --max-length 64 --steps 200)
run_job w2_llm_hp_nonnoise_lb200_${RUN_ID} "${COMMON[@]}" --lr 1e-5
sleep 12
run_job w2_llm_hp_noise005002_r10_lr5e6_lb200_${RUN_ID} "${COMMON[@]}" --noise-enabled --sigma-d2d 0.05 --sigma-c2c 0.02 --resample-every 10 --lr 5e-6
sleep 12
run_job w2_llm_hp_noise010005_r10_lr1e6_lb200_${RUN_ID} "${COMMON[@]}" --noise-enabled --sigma-d2d 0.10 --sigma-c2c 0.05 --resample-every 10 --lr 1e-6
while true; do
  date '+[monitor] %F %T'
  nvidia-smi --query-gpu=index,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits || true
  for log in logs/_gpt/w2_llm_*_${RUN_ID}.log; do echo "--- $log"; tail -n 3 "$log" 2>/dev/null || true; done
  live=0
  for p in paper2/results/w2_llm_*_${RUN_ID}.pid; do pid=$(cat "$p"); if kill -0 "$pid" 2>/dev/null; then live=1; fi; done
  [[ $live -eq 0 ]] && break
  sleep 30
done
wait
