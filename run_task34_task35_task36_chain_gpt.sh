#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
STAMP="${1:-$(date +%Y%m%d_%H%M%S)}"

cd "$ROOT"

echo "[$(date '+%Y-%m-%d %H:%M:%S %z')] Starting Task 34 (V4 proportional HAT)"
bash "$ROOT/run_task34_v4_proportional_hat_gpt.sh" "$STAMP"

echo "[$(date '+%Y-%m-%d %H:%M:%S %z')] Starting Task 35 (V4 NL=2.0 HAT)"
bash "$ROOT/run_task35_v4_nl2_hat_gpt.sh" "$STAMP" "0.0005"

echo "[$(date '+%Y-%m-%d %H:%M:%S %z')] Starting Task 36 (C4 proportional HAT)"
bash "$ROOT/run_task36_c4_proportional_hat_gpt.sh" "$STAMP"

echo "[$(date '+%Y-%m-%d %H:%M:%S %z')] Task 34/35/36 chain completed"
