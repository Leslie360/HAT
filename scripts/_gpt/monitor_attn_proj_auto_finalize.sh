#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="/home/qiaosir/projects/compute_vit"
PYTHON_BIN="/home/qiaosir/miniconda3/envs/LLM/bin/python"
ATTN_JSON="$REPO_DIR/report_md/_gpt/json_gpt/v4_nl2_attn_proj_linear_comp_train_results_gpt.json"
LOG_PATH="$REPO_DIR/logs/_gpt/monitor_attn_proj_auto_finalize.log"
STAMP_MD="$REPO_DIR/report_md/_gpt/AUTO_FINALIZE_TRIGGERED_20260418.md"

mkdir -p "$(dirname "$LOG_PATH")"
cd "$REPO_DIR"

{
  echo "[$(date '+%F %T')] watcher armed"
  while pgrep -f 'run_tinyvit_groupwise_nl_comp.py --protected-group attn_proj' >/dev/null; do
    sleep 60
  done
  echo "[$(date '+%F %T')] attn_proj process drained"

  for _ in $(seq 1 40); do
    if [ -f "$ATTN_JSON" ]; then
      break
    fi
    sleep 15
  done

  if [ ! -f "$ATTN_JSON" ]; then
    echo "[$(date '+%F %T')] attn_proj JSON not found after drain; aborting finalize"
    exit 1
  fi

  echo "[$(date '+%F %T')] running auto finalize"
  "$PYTHON_BIN" scripts/_gpt/auto_finalize_nl_ablation.py

  cat > "$STAMP_MD" <<EOF
# Auto Finalize Triggered — 2026-04-18

- Trigger time: $(date '+%F %T')
- Trigger: attn_proj-only lane drained and result JSON appeared
- Finalize script: \
  - \\`scripts/_gpt/auto_finalize_nl_ablation.py\\`
- Updated targets:
  - \\`report_md/_gpt/SUPP_TABLE_NL_ABLATION_SCAFFOLD.md\\`
  - \\`report_md/_gpt/NL_LANE_RESULTS_20260418.md\\`
  - \\`report_md/_gpt/CLAUDE_A_DECISION_FINAL_20260418.md\\`
EOF

  echo "[$(date '+%F %T')] finalize complete"
} >> "$LOG_PATH" 2>&1
