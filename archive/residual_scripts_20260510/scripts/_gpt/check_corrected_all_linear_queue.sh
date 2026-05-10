#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"

echo "[tmux]"
tmux ls 2>/dev/null | grep 'corr_allcad_q' || echo "No corrected all-linear queue tmux session."

echo
echo "[process]"
pgrep -af 'run_corrected_all_linear_cadence.py|run_corrected_all_linear_queue.sh' || echo "No matching process."

echo
echo "[logs]"
ls -1t "$ROOT"/logs/_gpt/corrected_all_linear_queue_*.log 2>/dev/null | head -n 1 | while read -r f; do
  echo "queue log: $f"
  tail -n 20 "$f"
done

ls -1t "$ROOT"/logs/_gpt/V4_hybrid_standard_noise_hat_all_linear_r*.log 2>/dev/null | head -n 1 | while read -r f; do
  echo
  echo "runner log: $f"
  tail -n 20 "$f"
done
