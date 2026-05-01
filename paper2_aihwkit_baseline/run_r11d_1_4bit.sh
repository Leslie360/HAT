#!/usr/bin/env bash
set -u
cd /home/qiaosir/projects/compute_vit || exit 2
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:${LD_LIBRARY_PATH:-}
echo "[wrapper] start $(date -Is) pid=$$"
trap 'echo "[wrapper] got SIGHUP $(date -Is)"' HUP
trap 'echo "[wrapper] got SIGTERM $(date -Is)"; exit 143' TERM
/home/qiaosir/miniconda3/envs/aihwkit/bin/python paper2_aihwkit_baseline/train_aihwkit_baseline.py \
  --run-id r11d_1_4bit \
  --seed 42 \
  --epochs 100 \
  --batch-size 64 \
  --lr 5e-4 \
  --wd 0.05 \
  --workers 0 \
  --device cuda \
  --save-dir paper2_aihwkit_baseline/checkpoints/r11d_1_4bit \
  --log-interval 1 \
  --inp-res 0.0625 \
  --out-res 0.0625 \
  --modifier-std-dev 0.10 \
  --early-stop-patience 20
rc=$?
echo "[wrapper] exit rc=$rc $(date -Is)"
exit $rc
