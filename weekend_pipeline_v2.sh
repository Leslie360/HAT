#!/bin/bash
# Weekend Pipeline v2 — Reliable background execution
set -e
CKPT_28B=/home/lisq753/projects/HAT_kv107/paper2/results/remote107/checkpoints/p28b_fixed500_seed42
CKPT_69B=/home/lisq753/projects/HAT_kv107/paper2/results/remote107/checkpoints/p69b_fixed500_seed42
CKPT_28B_L2=/home/lisq753/projects/HAT_kv107/paper2/results/remote107/checkpoints/p28b_last2_fixed500_seed42
CKPT_28B_L4=/home/lisq753/projects/HAT_kv107/paper2/results/remote107/checkpoints/p28b_last4_fixed500_seed42
OUT=/home/lisq753/projects/HAT_kv107/paper2/results/remote107
PYTHON=/home/lisq753/miniconda3/envs/LLM/bin/python
SCRIPT=/home/lisq753/projects/HAT/HAT/p3_hat_eval.py

wait_lm_eval() {
    local GPU=$1
    echo "[$(date)] GPU $GPU: Waiting for lm-eval to finish..."
    while pgrep -f "p3_hat_lm_eval.py" > /dev/null; do
        sleep 60
    done
    echo "[$(date)] GPU $GPU: lm-eval done, starting pipeline."
}

# GPU 4
(
    wait_lm_eval 4
    for sigma in 0.0 0.01 0.02 0.05 0.10; do
        echo "[$(date)] GPU 4: 2.8B eval sigma_c2c=$sigma"
        CUDA_VISIBLE_DEVICES=4 $PYTHON $SCRIPT --checkpoint_dir $CKPT_28B \
            --sigma_c2c $sigma --sigma_d2d 0.02 --max_length 512 --device cuda --fp16 --output_dir $OUT
    done
    for sigma in 0.0 0.01 0.02 0.05 0.10; do
        echo "[$(date)] GPU 4: 2.8B eval sigma_d2d=$sigma"
        CUDA_VISIBLE_DEVICES=4 $PYTHON $SCRIPT --checkpoint_dir $CKPT_28B \
            --sigma_c2c 0.01 --sigma_d2d $sigma --max_length 512 --device cuda --fp16 --output_dir $OUT
    done
    for n in 128 256 512 1024; do
        echo "[$(date)] GPU 4: 2.8B eval n_states=$n"
        CUDA_VISIBLE_DEVICES=4 $PYTHON $SCRIPT --checkpoint_dir $CKPT_28B \
            --sigma_c2c 0.01 --sigma_d2d 0.02 --n_states $n --max_length 512 --device cuda --fp16 --output_dir $OUT
    done
    echo "[$(date)] GPU 4: ALL DONE."
) > $OUT/weekend_gpu4.log 2>&1 &

# GPU 5
(
    wait_lm_eval 5
    echo "[$(date)] GPU 5: 2.8B last2 clean"
    CUDA_VISIBLE_DEVICES=5 $PYTHON $SCRIPT --checkpoint_dir $CKPT_28B_L2 \
        --sigma_c2c 0.0 --sigma_d2d 0.0 --max_length 512 --device cuda --fp16 --output_dir $OUT
    echo "[$(date)] GPU 5: 2.8B last4 clean"
    CUDA_VISIBLE_DEVICES=5 $PYTHON $SCRIPT --checkpoint_dir $CKPT_28B_L4 \
        --sigma_c2c 0.0 --sigma_d2d 0.0 --max_length 512 --device cuda --fp16 --output_dir $OUT
    echo "[$(date)] GPU 5: 2.8B last2 analog"
    CUDA_VISIBLE_DEVICES=5 $PYTHON $SCRIPT --checkpoint_dir $CKPT_28B_L2 \
        --sigma_c2c 0.01 --sigma_d2d 0.02 --max_length 512 --device cuda --fp16 --output_dir $OUT
    echo "[$(date)] GPU 5: 2.8B last4 analog"
    CUDA_VISIBLE_DEVICES=5 $PYTHON $SCRIPT --checkpoint_dir $CKPT_28B_L4 \
        --sigma_c2c 0.01 --sigma_d2d 0.02 --max_length 512 --device cuda --fp16 --output_dir $OUT
    for seed in 42 123 456 789 2024; do
        echo "[$(date)] GPU 5: 2.8B eval d2d_seed=$seed"
        CUDA_VISIBLE_DEVICES=5 $PYTHON $SCRIPT --checkpoint_dir $CKPT_28B \
            --sigma_c2c 0.01 --sigma_d2d 0.02 --d2d-seed $seed --max_length 512 --device cuda --fp16 --output_dir $OUT
    done
    echo "[$(date)] GPU 5: ALL DONE."
) > $OUT/weekend_gpu5.log 2>&1 &

# GPU 6
(
    wait_lm_eval 6
    for sigma in 0.0 0.01 0.02 0.05 0.10; do
        echo "[$(date)] GPU 6: 6.9B eval sigma_c2c=$sigma"
        CUDA_VISIBLE_DEVICES=6 $PYTHON $SCRIPT --checkpoint_dir $CKPT_69B \
            --sigma_c2c $sigma --sigma_d2d 0.02 --max_length 512 --device cuda --fp16 --output_dir $OUT
    done
    for n in 128 256 512 1024; do
        echo "[$(date)] GPU 6: 6.9B eval n_states=$n"
        CUDA_VISIBLE_DEVICES=6 $PYTHON $SCRIPT --checkpoint_dir $CKPT_69B \
            --sigma_c2c 0.01 --sigma_d2d 0.02 --n_states $n --max_length 512 --device cuda --fp16 --output_dir $OUT
    done
    echo "[$(date)] GPU 6: ALL DONE."
) > $OUT/weekend_gpu6.log 2>&1 &

# GPU 7
(
    wait_lm_eval 7
    for sigma in 0.0 0.01 0.02 0.05 0.10; do
        echo "[$(date)] GPU 7: 6.9B eval sigma_d2d=$sigma"
        CUDA_VISIBLE_DEVICES=7 $PYTHON $SCRIPT --checkpoint_dir $CKPT_69B \
            --sigma_c2c 0.01 --sigma_d2d $sigma --max_length 512 --device cuda --fp16 --output_dir $OUT
    done
    for seed in 42 123 456 789 2024; do
        echo "[$(date)] GPU 7: 6.9B eval d2d_seed=$seed"
        CUDA_VISIBLE_DEVICES=7 $PYTHON $SCRIPT --checkpoint_dir $CKPT_69B \
            --sigma_c2c 0.01 --sigma_d2d 0.02 --d2d-seed $seed --max_length 512 --device cuda --fp16 --output_dir $OUT
    done
    echo "[$(date)] GPU 7: ALL DONE."
) > $OUT/weekend_gpu7.log 2>&1 &

echo "[$(date)] Weekend pipeline v2 launched. 4 background jobs started."
echo "Monitor: tail -f $OUT/weekend_gpu{4,5,6,7}.log"
