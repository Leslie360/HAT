#!/usr/bin/env bash
set -uo pipefail
cd /home/qiaosir/projects/compute_vit
PY=/home/qiaosir/miniconda3/envs/LLM/bin/python
RUN_ID=20260425_221406
mkdir -p logs/_gpt paper2/results
run_job() {
  local scope="$1"
  local name="w2_llm_scope_${scope}_noise005002_r10_lr5e6_lb200_${RUN_ID}"
  local log="logs/_gpt/${name}.log"
  echo "[launch] $name -> $log"
  ("$PY" -u paper2/src/train_llm_hybrid.py     --model EleutherAI/pythia-410m-deduped     --device cuda     --dtype float32     --local-files-only     --hybrid     --analog-scope "$scope"     --high-precision-analog     --noise-enabled     --sigma-d2d 0.05     --sigma-c2c 0.02     --resample-every 10     --train-scope last_block     --max-length 64     --steps 200     --lr 5e-6 > "$log" 2>&1; code=$?; echo "$code" > "paper2/results/${name}.exit"; echo "[exit] $name $code") &
  echo "$!" > "paper2/results/${name}.pid"
}
run_job qkv
sleep 10
run_job attention_output
sleep 10
run_job mlp
while true; do
  date '+[monitor] %F %T'
  nvidia-smi --query-gpu=index,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits || true
  for log in logs/_gpt/w2_llm_scope_*_${RUN_ID}.log; do echo "--- $log"; tail -n 3 "$log" 2>/dev/null || true; done
  live=0
  for p in paper2/results/w2_llm_scope_*_${RUN_ID}.pid; do pid=$(cat "$p"); if kill -0 "$pid" 2>/dev/null; then live=1; fi; done
  [[ $live -eq 0 ]] && break
  sleep 30
done
wait
