#!/bin/bash
# R11D-2 watcher — auto fresh eval + conditional R11D-3 launch
set -euo pipefail

cd /home/qiaosir/projects/compute_vit
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:${LD_LIBRARY_PATH:-}
PYTHON=~/miniconda3/envs/aihwkit/bin/python
TRAIN=paper2_aihwkit_baseline/train_aihwkit_baseline.py
EVAL=paper2_aihwkit_baseline/eval_aihwkit_fresh.py
CKPT_DIR=paper2_aihwkit_baseline/checkpoints/r11d_2_sigma020
LOG=paper2_aihwkit_baseline/logs/r11d2_watcher.log

echo "[watcher] $(date -Is) starting R11D-2 watch" | tee -a "$LOG"

# Wait for training process to finish
while pgrep -f "r11d2_sigma020" >/dev/null; do
    sleep 60
done

echo "[watcher] $(date -Is) R11D-2 training ended" | tee -a "$LOG"

# Run fresh eval if best.pt exists
if [[ -s "${CKPT_DIR}/best.pt" ]]; then
    echo "[watcher] $(date -Is) running fresh eval" | tee -a "$LOG"
    $PYTHON $EVAL \
        --checkpoint "${CKPT_DIR}/best.pt" \
        --n-fresh 10 \
        --workers 0 \
        --device cuda \
        --output "${CKPT_DIR}/fresh_eval.json" | tee -a "$LOG"

    # Parse result
    MEAN=$($PYTHON -c "import json; print(json.load(open('${CKPT_DIR}/fresh_eval.json'))['mean'])")
    echo "[watcher] $(date -Is) fresh mean = ${MEAN}%" | tee -a "$LOG"

    # Conditional R11D-3: only if fresh mean > 80%
    if (( $(echo "$MEAN > 80.0" | bc -l) )); then
        echo "[watcher] $(date -Is) R11D-2 fresh mean > 80%, launching R11D-3 (sigma=0.30)" | tee -a "$LOG"
        nohup $PYTHON $TRAIN \
            --run-id r11d3_sigma030 \
            --seed 42 --epochs 100 --batch-size 64 --lr 5e-4 --wd 0.05 \
            --workers 0 --device cuda \
            --save-dir paper2_aihwkit_baseline/checkpoints/r11d_3_sigma030 \
            --log-interval 1 \
            --inp-res 0.00390625 --out-res 0.00390625 \
            --modifier-std-dev 0.30 \
            --early-stop-patience 20 \
            > paper2_aihwkit_baseline/logs/r11d3_sigma030.log 2>&1 &
        echo "[watcher] $(date -Is) R11D-3 launched" | tee -a "$LOG"
    else
        echo "[watcher] $(date -Is) R11D-2 fresh mean <= 80%, skipping R11D-3 to save GPU" | tee -a "$LOG"
    fi
else
    echo "[watcher] $(date -Is) best.pt missing, skip eval" | tee -a "$LOG"
fi

echo "[watcher] $(date -Is) watch complete" | tee -a "$LOG"
