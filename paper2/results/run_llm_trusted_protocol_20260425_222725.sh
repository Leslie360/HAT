#!/usr/bin/env bash
set -uo pipefail
cd /home/qiaosir/projects/compute_vit
PY=/home/qiaosir/miniconda3/envs/LLM/bin/python
RUN_ID=20260425_222725
mkdir -p logs/_gpt paper2/results
run_job() {
  local name="$1"; shift
  local log="logs/_gpt/${name}.log"
  echo "[launch] $name -> $log"
  ("$PY" -u paper2/src/train_llm_hybrid.py "$@" > "$log" 2>&1; code=$?; echo "$code" > "paper2/results/${name}.exit"; echo "[exit] $name $code") &
  echo "$!" > "paper2/results/${name}.pid"
}
BASE=(--model EleutherAI/pythia-410m-deduped --device cuda --dtype float32 --local-files-only --train-scope last_block --max-length 64 --steps 300 --eval-repeats 5 --seed 1234)
HYB=("${BASE[@]}" --hybrid --high-precision-analog)
run_job w2_trusted_digital_lb300_seed1234_${RUN_ID} "${BASE[@]}" --lr 1e-5
sleep 5
run_job w2_trusted_hybrid_all_nonnoise_lb300_seed1234_${RUN_ID} "${HYB[@]}" --analog-scope all --lr 1e-5
sleep 5
run_job w2_trusted_attention_output_n010005_lb300_seed1234_${RUN_ID} "${HYB[@]}" --analog-scope attention_output --noise-enabled --sigma-d2d 0.01 --sigma-c2c 0.005 --resample-every 10 --lr 5e-6
sleep 5
run_job w2_trusted_qkv_n005002_lb300_seed1234_${RUN_ID} "${HYB[@]}" --analog-scope qkv --noise-enabled --sigma-d2d 0.005 --sigma-c2c 0.002 --resample-every 10 --lr 5e-6
sleep 5
run_job w2_trusted_mlp_n005002_lb300_seed1234_${RUN_ID} "${HYB[@]}" --analog-scope mlp --noise-enabled --sigma-d2d 0.005 --sigma-c2c 0.002 --resample-every 10 --lr 5e-6
sleep 5
run_job w2_trusted_all_n005002_lb300_seed1234_${RUN_ID} "${HYB[@]}" --analog-scope all --noise-enabled --sigma-d2d 0.005 --sigma-c2c 0.002 --resample-every 10 --lr 5e-6
while true; do
  date '+[monitor] %F %T'
  nvidia-smi --query-gpu=index,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits || true
  for log in logs/_gpt/w2_trusted_*_${RUN_ID}.log; do echo "--- $log"; tail -n 2 "$log" 2>/dev/null || true; done
  live=0
  for p in paper2/results/w2_trusted_*_${RUN_ID}.pid; do pid=$(cat "$p"); if kill -0 "$pid" 2>/dev/null; then live=1; fi; done
  [[ $live -eq 0 ]] && break
  sleep 30
done
wait
