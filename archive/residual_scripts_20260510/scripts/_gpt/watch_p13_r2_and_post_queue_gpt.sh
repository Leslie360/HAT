#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
P13_LOG="$REPO_ROOT/logs/_gpt/p13_aihwkit_full_cifar10_gpu_r2.log"
WATCH_LOG="$REPO_ROOT/logs/_gpt/watch_p13_r2_and_post_queue.log"
FINALIZER="$REPO_ROOT/scripts/_gpt/finalize_p13_aihwkit_full_result_gpt.py"
POST_QUEUE="$REPO_ROOT/scripts/_gpt/run_post_p13_ablation_queue_gpt.sh"

{
  echo "[$(date '+%F %T %Z')] watcher start"
  echo "Waiting for p13_full_r2 tmux session to finish..."

  while tmux list-sessions 2>/dev/null | grep -q '^p13_full_r2:'; do
    sleep 30
  done

  echo "[$(date '+%F %T %Z')] p13_full_r2 session ended"
  if [[ -f "$P13_LOG" ]]; then
    echo "--- tail p13 log ---"
    tail -n 40 "$P13_LOG" || true
  fi

  echo "[$(date '+%F %T %Z')] running finalizer"
  python3 "$FINALIZER"

  echo "[$(date '+%F %T %Z')] finalizer ok; launching post-P13 queue"
  bash "$POST_QUEUE" 2>&1 | tee "$REPO_ROOT/logs/_gpt/p14_queue.log"

  echo "[$(date '+%F %T %Z')] watcher complete"
} | tee "$WATCH_LOG"

