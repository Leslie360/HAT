#!/usr/bin/env bash
set -euo pipefail

cd /home/qiaosir/projects/compute_vit
source /home/qiaosir/miniconda3/etc/profile.d/conda.sh
conda activate LLM
python scripts/_gpt/run_cx_k3_dgeff_stageA.py
