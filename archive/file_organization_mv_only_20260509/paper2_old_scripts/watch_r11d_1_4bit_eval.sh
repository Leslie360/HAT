#!/usr/bin/env bash
set -euo pipefail
cd /home/qiaosir/projects/compute_vit
export LD_LIBRARY_PATH=/home/qiaosir/miniconda3/envs/aihwkit/lib:${LD_LIBRARY_PATH:-}
train_session=codex_r11d1_4bit
out_dir=paper2_aihwkit_baseline/checkpoints/r11d_1_4bit
eval_log=paper2_aihwkit_baseline/logs/r11d_1_4bit_fresh_eval_$(date +%Y%m%d_%H%M%S).log
echo "[watcher] start $(date -Is), waiting for tmux session ${train_session}"
while tmux has-session -t "${train_session}" 2>/dev/null; do
  sleep 60
done
echo "[watcher] train session ended $(date -Is)"
if [[ ! -s "${out_dir}/best.pt" ]]; then
  echo "[watcher] missing ${out_dir}/best.pt; skip fresh eval"
  exit 1
fi
/home/qiaosir/miniconda3/envs/aihwkit/bin/python paper2_aihwkit_baseline/eval_aihwkit_fresh.py \
  --checkpoint "${out_dir}/best.pt" \
  --n-fresh 10 \
  --mc-repeats 5 \
  --workers 0 \
  --device cuda \
  --output "${out_dir}/fresh_eval.json" | tee -a "${eval_log}"
echo "[watcher] fresh eval complete $(date -Is), log=${eval_log}"
