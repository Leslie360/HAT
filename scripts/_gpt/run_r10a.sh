#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
PY="/home/qiaosir/miniconda3/envs/LLM/bin/python"

cd "$ROOT"
mkdir -p logs/_gpt checkpoints/_ensemble/V4_hybrid_seed456 checkpoints/_ensemble/V4_hybrid_seed789 report_md/_gpt/json_gpt

echo "Starting R10A seed 456..."
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
  --seed 456 \
  --nl-ltp 1.0 \
  --nl-ltd -1.0 \
  --noise-mode uniform \
  --save-dir checkpoints/_ensemble/V4_hybrid_seed456 \
  --log-path logs/_gpt/r10a_seed456.log > logs/_gpt/r10a_seed456_out.log 2>&1

echo "Evaluating R10A seed 456..."
"$PY" eval_fresh_instances_postfix.py \
  --checkpoint checkpoints/_ensemble/V4_hybrid_seed456/V4_hybrid_standard_noise_hat_best.pt \
  --exp-id V4 \
  --model-type tinyvit \
  --device cuda \
  --nl-ltp 1.0 \
  --nl-ltd -1.0 \
  --noise-mode uniform \
  --num-instances 10 \
  --mc-runs 5 \
  --output report_md/_gpt/json_gpt/r10a_seed456_fresh_eval.json >> logs/_gpt/r10a_seed456_eval.log 2>&1

echo "Starting R10A seed 789..."
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
  --seed 789 \
  --nl-ltp 1.0 \
  --nl-ltd -1.0 \
  --noise-mode uniform \
  --save-dir checkpoints/_ensemble/V4_hybrid_seed789 \
  --log-path logs/_gpt/r10a_seed789.log > logs/_gpt/r10a_seed789_out.log 2>&1

echo "Evaluating R10A seed 789..."
"$PY" eval_fresh_instances_postfix.py \
  --checkpoint checkpoints/_ensemble/V4_hybrid_seed789/V4_hybrid_standard_noise_hat_best.pt \
  --exp-id V4 \
  --model-type tinyvit \
  --device cuda \
  --nl-ltp 1.0 \
  --nl-ltd -1.0 \
  --noise-mode uniform \
  --num-instances 10 \
  --mc-runs 5 \
  --output report_md/_gpt/json_gpt/r10a_seed789_fresh_eval.json >> logs/_gpt/r10a_seed789_eval.log 2>&1

echo "R10A complete!"
