#!/usr/bin/env bash
# Watcher for R1 clean anchor training completion
LOGFILE="/home/qiaosir/projects/compute_vit/logs/_gpt/r1_clean_anchor_train_20260423_131610.log"
JSONFILE="/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/r1_clean_anchor_train.json"
CKPT="/home/qiaosir/projects/compute_vit/checkpoints/_gpt/r1_clean_anchor/V4_hybrid_standard_noise_hat_r1_clean_anchor_first_order_best.pt"

echo "[watch_r1] started at $(date --iso-8601=seconds)"
echo "[watch_r1] monitoring: $LOGFILE"

while true; do
  sleep 60
  if [ -f "$LOGFILE" ]; then
    LAST_EPOCH=$(grep -oE 'Epoch\s+[0-9]+/100' "$LOGFILE" | tail -1 | grep -oE '[0-9]+' | head -1)
    LAST_TEST=$(grep -oE 'test_acc=[0-9]+\.[0-9]+' "$LOGFILE" | tail -1)
    echo "[watch_r1] $(date +%H:%M:%S) last_epoch=$LAST_EPOCH $LAST_TEST"
  fi
  if [ -f "$CKPT" ] && [ -f "$JSONFILE" ]; then
    echo "[watch_r1] CHECKPOINT and JSON detected at $(date --iso-8601=seconds)"
    grep -E 'Epoch\s+([0-9]+)/100' "$LOGFILE" | tail -5
    break
  fi
done
echo "[watch_r1] completed at $(date --iso-8601=seconds)"
