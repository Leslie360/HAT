#!/usr/bin/env bash
# Post-K4R Immediate Action Script
# Run this manually after K4R fresh-instance eval completes

set -euo pipefail

REPO_DIR="/home/qiaosir/projects/compute_vit"
PYTHON_BIN="/home/qiaosir/miniconda3/envs/LLM/bin/python"

cd "$REPO_DIR"

echo "=========================================="
echo "Post-K4R Analysis Pipeline"
echo "=========================================="
echo ""

# 1. Check eval JSON exists
JSON="$REPO_DIR/report_md/_gpt/json_gpt/cx_k4r_fresh_eval.json"
if [ ! -f "$JSON" ]; then
    echo "ERROR: Eval JSON not found: $JSON"
    echo "Wait for fresh-instance eval to complete first."
    exit 1
fi

echo "[1/4] Eval JSON found: $JSON"

# 2. Run analysis script
echo "[2/4] Running analysis..."
"$PYTHON_BIN" scripts/_gpt/analyze_k4r_fresh_eval.py \
    --json "$JSON" \
    --out "$REPO_DIR/report_md/_gpt/KIMI_K4R_FRESH_EVAL_REPORT.md"

# 3. Fill result template
echo "[3/4] Updating result template..."
CROSS_MEAN=$(python3 -c "import json; d=json.load(open('$JSON')); print(f'{d[\"cross_instance_mean\"]:.2f}')")
CROSS_STD=$(python3 -c "import json; d=json.load(open('$JSON')); print(f'{d[\"cross_instance_std\"]:.2f}')")
TRAIN_BEST=$(python3 -c "import json; d=json.load(open('$JSON')); print(f'{d[\"train_best_acc\"]:.2f}')")

sed -i "s/\[FILL\] train best acc/${TRAIN_BEST}%/" "$REPO_DIR/report_md/_gpt/KIMI_K4R_RESULT_TEMPLATE_20260423.md"
sed -i "s/\[FILL\] cross-instance mean/${CROSS_MEAN}%/" "$REPO_DIR/report_md/_gpt/KIMI_K4R_RESULT_TEMPLATE_20260423.md"
sed -i "s/\[FILL\] cross-instance std/${CROSS_STD}%/" "$REPO_DIR/report_md/_gpt/KIMI_K4R_RESULT_TEMPLATE_20260423.md"

# 4. Determine P1 direction
echo "[4/4] P1 Decision Gate..."
python3 << PYEOF
import json
with open("$JSON") as f:
    d = json.load(f)
mean = d["cross_instance_mean"]
print(f"K4R fresh-instance: {mean:.2f}%")
if mean >= 85.0:
    print("→ P1-A: Parity achieved. Schedule α-sweep, K5 diagnostic, OPECT re-eval.")
elif mean >= 80.0:
    print("→ P1-B: Near parity. Schedule α-down sweep, joint MLP-linear + Ensemble HAT.")
else:
    print("→ P1-C: Significant degradation. Schedule first-order-only ablation, theory review.")
PYEOF

echo ""
echo "=========================================="
echo "Done. Reports written to:"
echo "  - report_md/_gpt/KIMI_K4R_FRESH_EVAL_REPORT.md"
echo "  - report_md/_gpt/KIMI_K4R_RESULT_TEMPLATE_20260423.md"
echo "=========================================="
