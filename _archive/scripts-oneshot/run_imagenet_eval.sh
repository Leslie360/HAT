#!/bin/bash
export CUDA_VISIBLE_DEVICES=0
cd /home/qiaosir/projects/compute_vit

echo "Starting ImageNet-1K Zero-Shot Evaluation..."
source ~/miniconda3/etc/profile.d/conda.sh
conda activate LLM

python3 -u eval_imagenet_analog.py \
    --batch-size 32 \
    > logs/_gpt/imagenet_eval_gpt.log 2>&1
