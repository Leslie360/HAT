#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
cd "$ROOT"

# Ensure conda is available
source ~/miniconda3/etc/profile.d/conda.sh

# Check if environment exists
if ! conda info --envs | grep -q "aihwkit_env"; then
  echo "Creating conda env 'aihwkit_env'..."
  conda create -y -n aihwkit_env python=3.11
  conda activate aihwkit_env
  
  echo "Installing AIHWKit and dependencies..."
  pip install aihwkit torch torchvision matplotlib
else
  conda activate aihwkit_env
fi

mkdir -p logs/_gpt report_md/_gpt/json_gpt checkpoints/_gpt/r10e

echo "Starting AIHWKit real Tiny-ViT conversion feasibility probe (R10E)..."
python scripts/_gpt/train_aihwkit_baseline.py > logs/_gpt/r10e_out.log 2>&1

echo "R10E complete!"
