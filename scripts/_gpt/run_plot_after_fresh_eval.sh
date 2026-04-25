#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
PY="/home/qiaosir/miniconda3/envs/LLM/bin/python"
STATUS_JSON="$ROOT/report_md/_gpt/json_gpt/cx_fresh_eval_mseries_status.json"
PLOT_STATUS="$ROOT/report_md/_gpt/json_gpt/cx_plot_refresh_status.json"
LOG_PATH="$ROOT/logs/_gpt/cx_plot_refresh_$(date +%Y%m%d_%H%M%S).log"

cd "$ROOT"
mkdir -p "$(dirname "$PLOT_STATUS")" "$(dirname "$LOG_PATH")"

write_status() {
  local phase="$1"
  local message="$2"
  cat > "$PLOT_STATUS" <<EOF
{
  "phase": "$phase",
  "message": "$message",
  "timestamp": "$(date -Is)",
  "log_path": "$LOG_PATH"
}
EOF
}

write_status "waiting" "waiting_for_cx_fresh_eval_mseries_complete"

while true; do
  phase="$("$PY" - <<'PY'
import json
from pathlib import Path
p = Path("report_md/_gpt/json_gpt/cx_fresh_eval_mseries_status.json")
if not p.exists():
    print("missing")
else:
    print(json.loads(p.read_text()).get("phase", "unknown"))
PY
)"
  if [[ "$phase" == "complete" ]]; then
    break
  fi
  if [[ "$phase" == "failed" ]]; then
    write_status "blocked" "fresh_eval_failed"
    exit 1
  fi
  sleep 60
done

write_status "running" "plot_refresh"
"$PY" scripts/_gpt/plot_postfix_mseries.py > "$LOG_PATH" 2>&1
write_status "complete" "plot_refresh_complete"
