#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/home/qiaosir/projects/compute_vit"
PIDFILE="$REPO_DIR/logs/_gpt/cx_k3_continuation_driver_20260421.pid"
MON_PIDFILE="$REPO_DIR/logs/_gpt/monitor_cx_k3_continuation_20260422.pid"
HB_LOG="$REPO_DIR/logs/_gpt/cx_k3_continuation_heartbeat_20260422.log"
MON_LOG="$REPO_DIR/logs/_gpt/monitor_cx_k3_continuation_20260422.log"
STAMP_MD="$REPO_DIR/report_md/_gpt/CX_K3_CONTINUATION_MONITOR_RESULT_20260422.md"
MAIN_LOG="$REPO_DIR/logs/_gpt/cx_k3_continuation_driver_20260421.log"
OUT_JSON="$REPO_DIR/report_md/_gpt/json_gpt/cx_k3_dgeff_continuation.json"
OUT_MD="$REPO_DIR/report_md/_gpt/CODEX_CX_K3_CONTINUATION_20260421.md"
HB_SCRIPT="$REPO_DIR/scripts/_gpt/watch_pid_heartbeat_gpt.sh"

mkdir -p "$REPO_DIR/logs/_gpt" "$REPO_DIR/report_md/_gpt"

if [ -f "$MON_PIDFILE" ]; then
  OLD_PID="$(tr -d '\r\n' < "$MON_PIDFILE" || true)"
  if [ -n "$OLD_PID" ] && kill -0 "$OLD_PID" 2>/dev/null; then
    echo "[$(date '+%F %T %Z')] monitor already running pid=$OLD_PID" | tee -a "$MON_LOG"
    exit 0
  fi
fi

echo $$ > "$MON_PIDFILE"
cleanup() {
  rm -f "$MON_PIDFILE"
}
trap cleanup EXIT

if [ ! -f "$PIDFILE" ]; then
  echo "[$(date '+%F %T %Z')] missing pidfile: $PIDFILE" | tee -a "$MON_LOG"
  exit 1
fi

PID="$(tr -d '\r\n' < "$PIDFILE")"
if [ -z "$PID" ]; then
  echo "[$(date '+%F %T %Z')] empty pidfile: $PIDFILE" | tee -a "$MON_LOG"
  exit 1
fi

{
  echo "[$(date '+%F %T %Z')] monitor armed pid=$PID self=$$"

  nohup "$HB_SCRIPT" "$PID" "$HB_LOG" 300 >/dev/null 2>&1 &
  HB_PID=$!
  echo "[$(date '+%F %T %Z')] heartbeat watcher pid=$HB_PID"

  while kill -0 "$PID" 2>/dev/null; do
    sleep 60
  done

  echo "[$(date '+%F %T %Z')] target pid drained: $PID"

  for _ in $(seq 1 20); do
    [ -f "$OUT_JSON" ] && break
    sleep 15
  done

  JSON_STATUS="missing"
  MD_STATUS="missing"
  if [ -f "$OUT_JSON" ]; then JSON_STATUS="present"; fi
  if [ -f "$OUT_MD" ]; then MD_STATUS="present"; fi

  {
    echo "# CX-K3 Continuation Monitor Result"
    echo
    echo "- Monitor time: $(date '+%F %T %Z')"
    echo "- Target PID: $PID"
    echo "- Aggregate JSON: $JSON_STATUS"
    echo "- Aggregate summary MD: $MD_STATUS"
    echo
    echo "## Driver Tail"
    echo
    echo '```text'
    tail -n 80 "$MAIN_LOG" 2>/dev/null || true
    echo '```'
    echo
    if [ -f "$OUT_JSON" ]; then
      echo "## Aggregate JSON Head"
      echo
      echo '```json'
      sed -n '1,120p' "$OUT_JSON"
      echo '```'
    fi
  } > "$STAMP_MD"

  echo "[$(date '+%F %T %Z')] monitor complete; wrote $STAMP_MD"
} >> "$MON_LOG" 2>&1
