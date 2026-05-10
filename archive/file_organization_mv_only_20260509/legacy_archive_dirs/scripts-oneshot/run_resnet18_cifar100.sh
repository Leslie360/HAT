#!/bin/bash
export CUDA_VISIBLE_DEVICES=0
cd /home/qiaosir/projects/compute_vit

echo "Starting ResNet-18 CIFAR-100 P0 Experiments (R1, R3, R4)..."
source ~/miniconda3/etc/profile.d/conda.sh
conda activate LLM

python3 -u train_resnet18.py \
    --dataset cifar100 \
    --experiments R3 R4 \
    --epochs 200 \
    --seed 42 \
    --amp \
    --save-dir checkpoints/resnet18_cifar100 \
    >> logs/_gpt/resnet18_cifar100_P0.log 2>&1

echo "ResNet-18 CIFAR-100 experiments complete."
