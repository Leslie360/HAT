#!/bin/bash
export CUDA_VISIBLE_DEVICES=0
cd /home/qiaosir/projects/compute_vit

# GM-E4: Mapping the NL Failure Landscape
# We sweep NL values around the known 2.0 boundary.

NL_VALUES=(1.8 2.2 1.5 1.2 2.5)

for nl in "${NL_VALUES[@]}"; do
    echo "----------------------------------------------------"
    echo "Starting GM-E4: Training with NL_LTP/LTD = $nl"
    echo "----------------------------------------------------"
    # Note: We keep --experiment V4 to load the base config, 
    # but use a specific save-dir to avoid overwriting.
    /home/qiaosir/miniconda3/envs/LLM/bin/python3 -u train_tinyvit_ensemble.py \
        --mode train \
        --experiment V4 \
        --dataset cifar10 \
        --epochs 100 \
        --batch-size 64 \
        --nl-ltp "$nl" \
        --nl-ltd "$nl" \
        --save-dir "checkpoints/gm_e4_nl_scan/nl_${nl}" \
        --log-path "logs/_gpt/gm_e4_nl_${nl}.log" \
        --amp
done

echo "GM-E4 NL Landscape Scan Complete."
