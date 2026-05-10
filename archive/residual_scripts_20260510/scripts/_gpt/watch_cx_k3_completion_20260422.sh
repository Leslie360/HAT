#!/usr/bin/env bash
set -euo pipefail
PID=1735310
REPO_DIR="/home/qiaosir/projects/compute_vit"
MAIN_LOG="$REPO_DIR/logs/_gpt/cx_k3_continuation_driver_20260421.log"
OUT_JSON="$REPO_DIR/report_md/_gpt/json_gpt/cx_k3_dgeff_continuation.json"
OUT_MD="$REPO_DIR/report_md/_gpt/CODEX_CX_K3_CONTINUATION_20260421.md"
LOG="$REPO_DIR/logs/_gpt/watch_cx_k3_completion_20260422.log"
STAMP="$REPO_DIR/report_md/_gpt/CX_K3_CONTINUATION_FINAL_STATUS_20260422.md"
{
  echo "[$(date '+%F %T %Z')] completion watcher armed pid=$PID"
  while kill -0 "$PID" 2>/dev/null; do
    sleep 60
  done
  echo "[$(date '+%F %T %Z')] target pid drained"
  for _ in $(seq 1 20); do
    [ -f "$OUT_JSON" ] && break
    sleep 15
  done
  {
    echo "# CX-K3 Continuation Final Status"
    echo
    echo "- Timestamp: $(date '+%F %T %Z')"
    echo "- Target PID: $PID"
    echo "- Aggregate JSON present: $([ -f "$OUT_JSON" ] && echo yes || echo no)"
    echo "- Aggregate MD present: $([ -f "$OUT_MD" ] && echo yes || echo no)"
    echo
    echo "## Driver Tail"
    echo
    echo '```text'
    tail -n 100 "$MAIN_LOG" 2>/dev/null || true
    echo '```'
    if [ -f "$OUT_JSON" ]; then
      echo
      echo "## Aggregate JSON Head"
      echo
      echo '```json'
      sed -n '1,160p' "$OUT_JSON"
      echo '```'
    fi
  } > "$STAMP"
  echo "[$(date '+%F %T %Z')] wrote $STAMP"
} >> "$LOG" 2>&1
