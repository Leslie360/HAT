#!/bin/bash
# Fresh-instance eval for Standard HAT (post-fix)
cd /home/qiaosir/projects/compute_vit
/home/qiaosir/miniconda3/envs/LLM/bin/python eval_fresh_instances_postfix.py \
  --checkpoint checkpoints/_gpt/postfix_standard_hat/V3_hybrid_standard_noise_standard_train_best.pt \
  --exp-id V3 \
  --model-type tinyvit \
  --nl-ltp 2.0 \
  --nl-ltd -2.0 \
  --num-instances 10 \
  --mc-runs 5 \
  > logs/_gpt/postfix_standard_hat_fresh_eval.log 2>&1
echo "Standard HAT fresh eval done at $(date)"
