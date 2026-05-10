#!/bin/bash
# R11D-8-SWA: Stochastic Weight Averaging continuation from R11D-8 best checkpoint

set -e
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:$LD_LIBRARY_PATH

CKPT="paper2_aihwkit_baseline/checkpoints/r11d_8_hat_inspired_pcm/best.pt"
CKPT_DIR="paper2_aihwkit_baseline/checkpoints/r11d_8_hat_inspired_pcm_swa"
LOG="paper2_aihwkit_baseline/logs/r11d_8_swa_$(date +%Y%m%d_%H%M%S).log"
mkdir -p "$CKPT_DIR" paper2_aihwkit_baseline/logs

if [ ! -f "$CKPT" ]; then
    echo "ERROR: $CKPT not found. R11D-8 must complete first."
    exit 1
fi

echo "=== R11D-8-SWA: SWA continuation from best.pt ===" | tee "$LOG"
echo "Source checkpoint: $CKPT" | tee -a "$LOG"

/home/qiaosir/miniconda3/envs/aihwkit/bin/python \
    paper2_aihwkit_baseline/r11d_hat_pcm.py \
    --run-id r11d_8_hat_inspired_pcm_swa \
    --epochs 25 \
    --batch-size 64 \
    --lr 5e-4 \
    --wd 0.05 \
    --device cuda \
    --workers 0 \
    --save-dir "$CKPT_DIR" \
    --log-interval 1 \
    --hat-std-dev 5.0 \
    --hat-mode scaled \
    --hat-start-epoch 1 \
    --resume "$CKPT" \
    2>&1 | tee -a "$LOG"

echo "=== R11D-8-SWA complete ==="
