#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
PY="/home/qiaosir/miniconda3/envs/LLM/bin/python"

cd "$ROOT"
mkdir -p logs/_gpt checkpoints/_ensemble report_md/_gpt/json_gpt

for nl in 1.2 1.5 1.8; do
  echo "Starting R10D NL=${nl}..."
  ckpt_dir="checkpoints/_ensemble/V4_hybrid_nl${nl}"
  mkdir -p "$ckpt_dir"
  
  "$PY" -u train_tinyvit_ensemble.py \
    --mode train \
    --experiment V4 \
    --dataset cifar10 \
    --epochs 100 \
    --batch-size 64 \
    --num-workers 0 \
    --pin-memory off \
    --gpu-resize \
    --early-stop-patience 10 \
    --device cuda \
    --amp \
    --seed 123 \
    --nl-ltp "${nl}" \
    --nl-ltd "-${nl}" \
    --noise-mode uniform \
    --save-dir "$ckpt_dir" \
    --log-path "logs/_gpt/r10d_nl${nl}.log" > "logs/_gpt/r10d_nl${nl}_out.log" 2>&1

  echo "Evaluating R10D NL=${nl}..."
  "$PY" eval_fresh_instances_postfix.py \
    --checkpoint "${ckpt_dir}/V4_hybrid_standard_noise_hat_best.pt" \
    --exp-id V4 \
    --model-type tinyvit \
    --device cuda \
    --nl-ltp "${nl}" \
    --nl-ltd "-${nl}" \
    --noise-mode uniform \
    --num-instances 10 \
    --mc-runs 5 \
    --output "report_md/_gpt/json_gpt/r10d_nl${nl}_fresh_eval.json" >> "logs/_gpt/r10d_nl${nl}_eval.log" 2>&1
done

echo "R10D complete!"