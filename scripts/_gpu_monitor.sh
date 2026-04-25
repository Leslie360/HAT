#!/bin/bash
while true; do
    clear
    echo "=== $(date '+%H:%M:%S') GPU MONITOR ==="
    nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total,temperature.gpu --format=csv,noheader 2>/dev/null
    echo ""
    echo "=== TRAINING PROCESSES ==="
    ps aux | grep "train_tinyvit_ensemble" | grep -v grep | wc -l | xargs echo "Active processes:"
    echo ""
    echo "=== CHECKPOINT MTIMES ==="
    for f in checkpoints/_gpt/postfix_standard_hat/*last.pt checkpoints/_gpt/postfix_proportional/*last.pt; do
        [ -f "$f" ] && echo "$(basename $(dirname $f)): $(stat -c %Y "$f" | xargs -I{} date -d @{} '+%H:%M:%S')"
    done
    echo ""
    echo "=== FRESH EVAL STATUS ==="
    [ -f report_md/_gpt/json_gpt/postfix_ensemble_hat_v4_nl20_fresh_eval.json ] && echo "Ensemble HAT fresh eval: DONE"
    sleep 10
done
