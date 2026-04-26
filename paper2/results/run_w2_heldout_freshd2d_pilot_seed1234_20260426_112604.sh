#!/usr/bin/env bash
set -uo pipefail
ROOT="/home/qiaosir/projects/compute_vit"
cd "$ROOT"
PY="/home/qiaosir/miniconda3/envs/LLM/bin/python"
STAMP="20260426_112604"
mkdir -p logs/_gpt paper2/results
export PYTHONUNBUFFERED=1
export CUDA_VISIBLE_DEVICES=0
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
run_job() {
  local scope="$1"
  local name="w2_heldout_freshd2d_${scope}_n005002_lb1000_seed1234_${STAMP}"
  local log="logs/_gpt/${name}.log"
  echo "[launch] ${name} -> ${log}"
  (
    timeout 5400 "$PY" -u paper2/src/train_llm_hybrid.py \
      --model EleutherAI/pythia-410m-deduped \
      --device cuda \
      --dtype float32 \
      --local-files-only \
      --train-scope last_block \
      --eval-text-set heldout \
      --max-length 64 \
      --steps 1000 \
      --eval-repeats 5 \
      --seed 1234 \
      --hybrid \
      --high-precision-analog \
      --analog-scope "$scope" \
      --noise-enabled \
      --sigma-d2d 0.005 \
      --sigma-c2c 0.002 \
      --resample-every 10 \
      --fresh-d2d-instances 10 \
      --fresh-d2d-repeats 5 \
      --lr 5e-6 \
      > "$log" 2>&1
    code=$?
    echo "$code" > "paper2/results/${name}.exit"
    echo "[exit] ${name} ${code}"
    exit "$code"
  ) &
  echo "$!" > "paper2/results/${name}.pid"
}
run_job all
run_job mlp
wait
