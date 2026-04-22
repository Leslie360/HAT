#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${1:-$ROOT/outputs/public_smoke}"

if [[ -n "${PYTHON_BIN:-}" ]]; then
  :
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
else
  echo "No python interpreter found. Set PYTHON_BIN=/path/to/python." >&2
  exit 1
fi

mkdir -p "$OUT_DIR"

echo "[1/5] Import surface"
"$PYTHON_BIN" - <<'PY'
import numpy
import timm
import torch
import torchvision
print("imports_ok")
print(f"torch={torch.__version__}")
print(f"cuda_available={torch.cuda.is_available()}")
PY

echo "[2/5] Demo measured-profile fitter"
"$PYTHON_BIN" "$ROOT/scripts/_gpt/profile_auto_fitter_gpt.py" \
  --demo \
  --output "$OUT_DIR/measured_device_profiles.json" \
  --audit-json "$OUT_DIR/measured_device_profile_summary.json" \
  --audit-md "$OUT_DIR/MEASURED_DEVICE_PROFILE_AUDIT.md"

echo "[3/5] Tiny-ViT dry-run"
"$PYTHON_BIN" "$ROOT/train_tinyvit.py" \
  --mode dry-run \
  --experiment V4 \
  --dataset cifar10 \
  > "$OUT_DIR/train_tinyvit_dry_run.txt"

echo "[4/5] Public CLI entrypoints"
"$PYTHON_BIN" "$ROOT/eval_measured_profile.py" --help > "$OUT_DIR/eval_measured_profile.help.txt"
"$PYTHON_BIN" "$ROOT/run_device_comparison.py" --help > "$OUT_DIR/run_device_comparison.help.txt"
"$PYTHON_BIN" "$ROOT/run_noise_sweep.py" --help > "$OUT_DIR/run_noise_sweep.help.txt"
"$PYTHON_BIN" "$ROOT/run_layer_sensitivity.py" --help > "$OUT_DIR/run_layer_sensitivity.help.txt"

echo "[5/5] Output summary"
cat <<EOF
Public smoke test completed.
Artifacts written to:
  $OUT_DIR

You should now have:
  - measured_device_profiles.json
  - measured_device_profile_summary.json
  - MEASURED_DEVICE_PROFILE_AUDIT.md
  - train_tinyvit_dry_run.txt
  - *.help.txt CLI snapshots
EOF
