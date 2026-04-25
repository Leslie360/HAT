#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
SESSION="${1:-r2_so2_comparison}"

cd "$ROOT"

if tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "tmux session already exists: $SESSION" >&2
  exit 1
fi

tmux new-session -d -s "$SESSION" "cd '$ROOT' && bash scripts/_gpt/run_r2_so2_comparison_queue.sh"
echo "$SESSION"
