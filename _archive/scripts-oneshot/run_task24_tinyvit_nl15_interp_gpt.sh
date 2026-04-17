#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
PY="/home/qiaosir/miniconda3/envs/LLM/bin/python"
TS="${1:-$(date +%Y%m%d_%H%M%S)}"

mkdir -p "$ROOT/logs/_gpt" "$ROOT/checkpoints/_gpt/task24" "$ROOT/report_md/_gpt/json_gpt" "$ROOT/report_md/_gpt/csv_gpt"

"$PY" - <<'PY'
import sys, torch
if not torch.cuda.is_available():
    sys.stderr.write(
        'CUDA preflight failed: torch.cuda.is_available() is False. '
        'In this workspace the WSL CUDA runtime appears broken (libcuda/libnvidia-ml missing), so this run cannot start until GPU runtime is restored.\n'
    )
    sys.exit(2)
print('CUDA preflight OK:', torch.cuda.get_device_name(0))
PY

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Task 24 start: Tiny-ViT V4 NL=1.5 interpolation"

exec "$PY" "$ROOT/train_tinyvit_ensemble.py" \
  --mode train \
  --experiment V4 \
  --dataset cifar10 \
  --device cuda \
  --pretrained \
  --amp \
  --resume-existing \
  --nl-ltp 1.5 \
  --nl-ltd -1.5 \
  --save-dir "$ROOT/checkpoints/_gpt/task24/v4_nl_interp15" \
  --results-json-path "$ROOT/report_md/_gpt/json_gpt/v4_nl_interp15_results_gpt.json" \
  --results-csv-path "$ROOT/report_md/_gpt/csv_gpt/v4_nl_interp15_results_gpt.csv" \
  --results-md-path "$ROOT/report_md/_gpt/v4_nl_interp15_results_gpt.md" \
  --log-path "$ROOT/logs/_gpt/train_tinyvit_v4_nl_interp15_${TS}_gpt.log"
