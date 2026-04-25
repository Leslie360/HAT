#!/bin/bash
# Post-fix evaluation script for Ensemble HAT severe-NL checkpoint
# Run this AFTER training completes

set -e
PROJECT=/home/qiaosir/projects/compute_vit
PYTHON=/home/qiaosir/miniconda3/envs/LLM/bin/python
CHECKPOINT=$PROJECT/checkpoints/_gpt/postfix_reruns/V4_hybrid_standard_noise_hat_best.pt

echo "=== Post-Fix Fresh Instance Evaluation ==="
echo "Checkpoint: $CHECKPOINT"
echo ""

if [ ! -f "$CHECKPOINT" ]; then
    echo "ERROR: Checkpoint not found: $CHECKPOINT"
    echo "Training may not have completed yet."
    exit 1
fi

# 1. Same-instance evaluation (sanity check)
echo "1. Same-instance evaluation..."
$PYTHON train_tinyvit_ensemble.py --mode eval --experiment V4 \
    --checkpoint "$CHECKPOINT" --dataset cifar10 --eval-runs 5 --amp \
    --nl-ltp 2.0 --nl-ltd -2.0

# 2. Fresh-instance evaluation (10 instances x 5 MC runs)
echo ""
echo "2. Fresh-instance evaluation (10x5)..."
$PYTHON eval_fresh_instances_postfix.py \
    --checkpoint "$CHECKPOINT" --exp-id V4 --model-type tinyvit \
    --num-instances 10 --mc-runs 5 \
    --nl-ltp 2.0 --nl-ltd -2.0 --noise-mode uniform \
    --output report_md/_gpt/json_gpt/postfix_ensemble_hat_v4_nl20_fresh_eval.json

echo ""
echo "=== Evaluation Complete ==="
