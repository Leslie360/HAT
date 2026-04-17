#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/qiaosir/projects/compute_vit"
PY="/home/qiaosir/miniconda3/envs/LLM/bin/python"
TS="$(date +%Y%m%d_%H%M%S)"

mkdir -p "$ROOT/logs/_gpt"

DRIVER_LOG="$ROOT/logs/_gpt/train_convnext_multidataset_c134_${TS}_driver_gpt.log"
CIFAR100_JSON="convnext_cifar100_c134_results_gpt.json"
CIFAR100_CSV="convnext_cifar100_c134_results_gpt.csv"
CIFAR100_MD="convnext_cifar100_c134_results_gpt.md"
FLOWERS_JSON="convnext_flowers102_c134_results_gpt.json"
FLOWERS_CSV="convnext_flowers102_c134_results_gpt.csv"
FLOWERS_MD="convnext_flowers102_c134_results_gpt.md"

{
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Task 21 start: ConvNeXt cross-dataset validation"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Stage 1: CIFAR-100 C1/C3/C4"
  "$PY" "$ROOT/train_convnext.py" \
    --dataset cifar100 \
    --num-classes 100 \
    --experiments C1 C3 C4 \
    --epochs 200 \
    --batch-size 128 \
    --device cuda \
    --amp \
    --resume-existing \
    --skip-retention \
    --save-dir "$ROOT/checkpoints/_gpt/convnext_cifar100" \
    --output-dir "$ROOT/report_md/_gpt" \
    --csv-name "$CIFAR100_CSV" \
    --json-name "$CIFAR100_JSON" \
    --report-name "$CIFAR100_MD" \
    2>&1

  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Stage 2: Flowers-102 C1/C3/C4"
  "$PY" "$ROOT/train_convnext.py" \
    --dataset flowers102 \
    --num-classes 102 \
    --experiments C1 C3 C4 \
    --epochs 100 \
    --batch-size 64 \
    --device cuda \
    --amp \
    --resume-existing \
    --skip-retention \
    --save-dir "$ROOT/checkpoints/_gpt/convnext_flowers102" \
    --output-dir "$ROOT/report_md/_gpt" \
    --csv-name "$FLOWERS_CSV" \
    --json-name "$FLOWERS_JSON" \
    --report-name "$FLOWERS_MD" \
    2>&1

  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Task 21 done"
} | tee "$DRIVER_LOG"
