#!/bin/bash
export CUDA_VISIBLE_DEVICES=0
cd /home/qiaosir/projects/compute_vit
/home/qiaosir/miniconda3/envs/LLM/bin/python3 -u experiment_nonideality_gemini.py > logs/_gpt/experiment_nonideality_gemini.log 2>&1
