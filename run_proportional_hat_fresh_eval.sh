#!/bin/bash
# Fresh-instance eval for Proportional HAT (post-fix)
# Usage: bash run_proportional_hat_fresh_eval.sh
cd /home/qiaosir/projects/compute_vit
/home/qiaosir/miniconda3/envs/LLM/bin/python eval_fresh_instances_postfix.py \
  --checkpoint checkpoints/_gpt/postfix_proportional/V4_hybrid_standard_noise_hat_best.pt \
  --exp-id V4 \
  --model-type tinyvit \
  --nl-ltp 2.0 \
  --nl-ltd -2.0 \
  --noise-mode proportional \
  --num-instances 10 \
  --mc-runs 5 \
  > logs/_gpt/postfix_proportional_hat_fresh_eval.log 2>&1
echo "Proportional HAT fresh eval done at $(date)"
