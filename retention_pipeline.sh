#!/bin/bash
# Retention Pipeline — Runs after lm-eval finishes on GPUs 4/5/6/7
set -e
CKPT_410M=/home/lisq753/projects/HAT_kv107/paper2/results/remote107/checkpoints/p410m_fixed500_fullmodel_seed42
CKPT_28B=/home/lisq753/projects/HAT_kv107/paper2/results/remote107/checkpoints/p28b_fixed500_seed42
CKPT_69B=/home/lisq753/projects/HAT_kv107/paper2/results/remote107/checkpoints/p69b_fixed500_seed42
OUT=/home/lisq753/projects/HAT_kv107/paper2/results/remote107
PYTHON=/home/lisq753/miniconda3/envs/LLM/bin/python
SCRIPT=/home/lisq753/projects/HAT/HAT/p3_hat_eval.py

wait_lm_eval() {
    local GPU=$1
    echo "[$(date)] GPU $GPU: Waiting for lm-eval to finish..."
    while pgrep -f "p3_hat_lm_eval.py" > /dev/null; do
        sleep 60
    done
    echo "[$(date)] GPU $GPU: lm-eval done, starting retention."
}

# GPU 4: 410M retention sweep
(
    wait_lm_eval 4
    for rst in 0.0 0.01 0.1 1.0 10.0; do
        echo "[$(date)] GPU 4: 410M retention_step_time=$rst"
        CUDA_VISIBLE_DEVICES=4 $PYTHON $SCRIPT --checkpoint_dir $CKPT_410M \
            --sigma_c2c 0.01 --sigma_d2d 0.02 --retention_step_time $rst \
            --max_length 512 --device cuda --fp16 --output_dir $OUT
    done
    echo "[$(date)] GPU 4: ALL DONE."
) > $OUT/retention_gpu4.log 2>&1 &

# GPU 5: 2.8B retention sweep
(
    wait_lm_eval 5
    for rst in 0.0 0.01 0.1 1.0 10.0; do
        echo "[$(date)] GPU 5: 2.8B retention_step_time=$rst"
        CUDA_VISIBLE_DEVICES=5 $PYTHON $SCRIPT --checkpoint_dir $CKPT_28B \
            --sigma_c2c 0.01 --sigma_d2d 0.02 --retention_step_time $rst \
            --max_length 512 --device cuda --fp16 --output_dir $OUT
    done
    echo "[$(date)] GPU 5: ALL DONE."
) > $OUT/retention_gpu5.log 2>&1 &

# GPU 6: 6.9B retention sweep (short)
(
    wait_lm_eval 6
    for rst in 0.0 0.01 0.1; do
        echo "[$(date)] GPU 6: 6.9B retention_step_time=$rst"
        CUDA_VISIBLE_DEVICES=6 $PYTHON $SCRIPT --checkpoint_dir $CKPT_69B \
            --sigma_c2c 0.01 --sigma_d2d 0.02 --retention_step_time $rst \
            --max_length 512 --device cuda --fp16 --output_dir $OUT
    done
    echo "[$(date)] GPU 6: ALL DONE."
) > $OUT/retention_gpu6.log 2>&1 &

# GPU 7: 6.9B retention sweep (extreme)
(
    wait_lm_eval 7
    for rst in 1.0 10.0; do
        echo "[$(date)] GPU 7: 6.9B retention_step_time=$rst"
        CUDA_VISIBLE_DEVICES=7 $PYTHON $SCRIPT --checkpoint_dir $CKPT_69B \
            --sigma_c2c 0.01 --sigma_d2d 0.02 --retention_step_time $rst \
            --max_length 512 --device cuda --fp16 --output_dir $OUT
    done
    echo "[$(date)] GPU 7: ALL DONE."
) > $OUT/retention_gpu7.log 2>&1 &

echo "[$(date)] Retention pipeline launched. Will start after lm-eval finishes."
