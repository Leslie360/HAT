#!/usr/bin/env bash
# P1-C2: Sign-reversal ablation (+0.5 positive second-order)
# Tests whether pre-Branch-A "wrong signs" were actually correct.
set -euo pipefail

REPO_DIR="/home/qiaosir/projects/compute_vit"
PYTHON_BIN="/home/qiaosir/miniconda3/envs/LLM/bin/python"

cd "$REPO_DIR"

# Temporarily patch analog_layers.py to use +0.5
cp analog_layers.py analog_layers.py.branch_a_backup
cp analog_layers_ensemble.py analog_layers_ensemble.py.branch_a_backup

sed -i 's/ltp_corr = -0.5 \* nl_ltp/ltp_corr = 0.5 * nl_ltp/g' analog_layers.py
sed -i 's/ltd_corr = -0.5 \* nl_ltd/ltd_corr = 0.5 * nl_ltd/g' analog_layers.py
sed -i 's/ltp_corr = -0.5 \* nl_ltp/ltp_corr = 0.5 * nl_ltp/g' analog_layers_ensemble.py
sed -i 's/ltd_corr = -0.5 \* nl_ltd/ltd_corr = 0.5 * nl_ltd/g' analog_layers_ensemble.py

LOG="$REPO_DIR/logs/_gpt/cx_p1c2_positive_sign_$(date +%Y%m%d_%H%M%S).log"

echo "[$(date '+%F %T')] P1-C2 Sign-Reversal Ablation Launch"
echo "[$(date '+%F %T')] WARNING: Temporarily using POSITIVE +0.5 second-order signs"
echo "[$(date '+%F %T')] This reverts to pre-Branch-A sign convention for ablation only."

"$PYTHON_BIN" scripts/_gpt/run_tinyvit_groupwise_nl_comp.py \
    --protected-group all \
    --protected-nl-ltp 1.0 \
    --protected-nl-ltd -1.0 \
    --use-second-order-ste \
    --delta-g-eff -1.0 \
    --second-order-alpha 0.25 \
    --name-suffix _p1c2_positive_sign \
    --mode train \
    --dataset cifar10 \
    --experiments V4 \
    --epochs 100 \
    --batch-size 64 \
    --num-workers 0 \
    --pin-memory off \
    --device cuda \
    --amp \
    --nl-ltp 2.0 \
    --nl-ltd -2.0 \
    --warm-start-from checkpoints/V4_hybrid_standard_noise_hat_best.pt \
    --save-dir checkpoints/_gpt/cx_p1c2_positive_sign \
    --log-interval 5 \
    --log-path "$LOG" \
    --results-json-path report_md/_gpt/json_gpt/cx_p1c2_positive_sign_train.json \
    2>&1 | tee "$LOG"

# Restore canonical code after training
mv analog_layers.py.branch_a_backup analog_layers.py
mv analog_layers_ensemble.py.branch_a_backup analog_layers_ensemble.py
