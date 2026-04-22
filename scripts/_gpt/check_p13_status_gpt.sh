#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MAIN_LOG="${ROOT}/logs/_gpt/p13_aihwkit_full_cifar10_gpu_r2.log"
HEARTBEAT_LOG="${ROOT}/logs/_gpt/p13_runtime_heartbeat.log"
WATCH_LOG="${ROOT}/logs/_gpt/watch_p13_r2_and_post_queue.log"
P13_MD="${ROOT}/report_md/_gpt/P13_aihwkit_full_result.md"
P13_JSON="${ROOT}/report_md/_gpt/json_gpt/p13_aihwkit_full_result.json"

echo "=== P13 Status Summary ==="
echo "Time: $(date '+%F %T %Z')"
echo

echo "[tmux]"
tmux ls 2>/dev/null | rg 'p13_full_r2|p13_r2_watch|p13_heartbeat' || echo "No matching tmux sessions."
echo

echo "[processes]"
for pid in $(pgrep -f 'aihwkit_shared_regime_benchmark_gpt.py|watch_p13_r2_and_post_queue_gpt.sh|watch_pid_heartbeat_gpt.sh' || true); do
  ps -p "$pid" -o pid=,etime=,%cpu=,%mem=,rss=,cmd=
done
echo

if [[ -f "${HEARTBEAT_LOG}" ]]; then
  echo "[heartbeat tail]"
  tail -n 5 "${HEARTBEAT_LOG}"
  echo
fi

if [[ -f "${MAIN_LOG}" ]]; then
  echo "[main log tail]"
  tail -n 10 "${MAIN_LOG}"
  echo
fi

if [[ -f "${WATCH_LOG}" ]]; then
  echo "[watcher tail]"
  tail -n 10 "${WATCH_LOG}"
  echo
fi

echo "[artifacts]"
for path in "${P13_MD}" "${P13_JSON}"; do
  if [[ -f "${path}" ]]; then
    stat --printf='%n | size=%s bytes | mtime=%y\n' "${path}"
  else
    echo "${path} | MISSING"
  fi
done
