#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <pid> <log_file> [interval_seconds]" >&2
  exit 1
fi

PID="$1"
LOG_FILE="$2"
INTERVAL="${3:-60}"

mkdir -p "$(dirname "$LOG_FILE")"

{
  echo "[$(date '+%F %T %Z')] heartbeat watcher start pid=${PID} interval=${INTERVAL}s"
  while kill -0 "$PID" 2>/dev/null; do
    ps -p "$PID" -o pid=,etime=,%cpu=,%mem=,rss=,cmd= | sed "s/^/[$(date '+%F %T %Z')] /"
    sleep "$INTERVAL"
  done
  echo "[$(date '+%F %T %Z')] heartbeat watcher stop pid=${PID}"
} | tee -a "$LOG_FILE"
