#!/bin/bash
export CUDA_VISIBLE_DEVICES=0
cd /home/qiaosir/projects/compute_vit

echo "Starting GM-E3: Retention Sensitivity..."
/home/qiaosir/miniconda3/envs/LLM/bin/python3 -u run_retention_sensitivity.py > logs/_gpt/retention_sensitivity.log 2>&1

echo "Starting GM-E5: Combined Stress Test..."
/home/qiaosir/miniconda3/envs/LLM/bin/python3 -u run_combined_nonideality.py > logs/_gpt/combined_stress.log 2>&1

echo "All hardening experiments complete."
