#!/usr/bin/env bash
set -uo pipefail
cd /home/qiaosir/projects/compute_vit
PY=/home/qiaosir/miniconda3/envs/LLM/bin/python
RUN_ID=20260425_221702
mkdir -p logs/_gpt paper2/results
run_job() {
  local scope="$1"
  local mode="$2"
  local d2d="$3"
  local c2c="$4"
  local resample="$5"
  local name="w2_llm_scope_${scope}_${mode}_lr5e6_lb200_${RUN_ID}"
  local log="logs/_gpt/${name}.log"
  echo "[launch] $name -> $log"
  ("$PY" -u paper2/src/train_llm_hybrid.py     --model EleutherAI/pythia-410m-deduped     --device cuda     --dtype float32     --local-files-only     --hybrid     --analog-scope "$scope"     --high-precision-analog     --noise-enabled     --sigma-d2d "$d2d"     --sigma-c2c "$c2c"     --resample-every "$resample"     --train-scope last_block     --max-length 64     --steps 200     --lr 5e-6 > "$log" 2>&1; code=$?; echo "$code" > "paper2/results/${name}.exit"; echo "[exit] $name $code") &
  echo "$!" > "paper2/results/${name}.pid"
}
for scope in qkv attention_output mlp; do
  run_job "$scope" d2d005 0.05 0.0 10
  sleep 5
  run_job "$scope" c2c002 0.0 0.02 0
  sleep 5
done
while true; do
  date '+[monitor] %F %T'
  nvidia-smi --query-gpu=index,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits || true
  for log in logs/_gpt/w2_llm_scope_*_${RUN_ID}.log; do echo "--- $log"; tail -n 2 "$log" 2>/dev/null || true; done
  live=0
  for p in paper2/results/w2_llm_scope_*_${RUN_ID}.pid; do pid=$(cat "$p"); if kill -0 "$pid" 2>/dev/null; then live=1; fi; done
  [[ $live -eq 0 ]] && break
  sleep 30
done
wait
