#!/usr/bin/env bash
set -euo pipefail

cd /home/qiaosir/projects/compute_vit

PY=/home/qiaosir/miniconda3/envs/LLM/bin/python

$PY run_noise_sweep.py \
  --model-type tinyvit \
  --experiment V4 \
  --device cuda \
  --amp \
  --eval-runs 10 \
  --log-path logs/_gpt/noise_sweep_tinyvit_v4_gpt.log

$PY run_noise_sweep.py \
  --model-type convnext \
  --experiment C4 \
  --device cuda \
  --amp \
  --eval-runs 10 \
  --log-path logs/_gpt/noise_sweep_convnext_c4_gpt.log

$PY run_noise_sweep.py \
  --model-type tinyvit \
  --experiment V4 \
  --device cuda \
  --amp \
  --eval-runs 10 \
  --sweep-type adc \
  --log-path logs/_gpt/adc_sweep_tinyvit_v4_gpt.log

$PY run_noise_sweep.py \
  --model-type convnext \
  --experiment C4 \
  --device cuda \
  --amp \
  --eval-runs 10 \
  --sweep-type adc \
  --log-path logs/_gpt/adc_sweep_convnext_c4_gpt.log

$PY run_device_comparison.py \
  --device cuda \
  --amp \
  --eval-runs 10 \
  --log-path logs/_gpt/device_comparison_gpt.log

$PY run_layer_sensitivity.py \
  --model-type tinyvit \
  --experiment V4 \
  --device cuda \
  --amp \
  --eval-runs 10 \
  --phase2-mixed \
  --log-path logs/_gpt/layer_sensitivity_tinyvit_v4_gpt.log

$PY run_layer_sensitivity.py \
  --model-type convnext \
  --experiment C4 \
  --device cuda \
  --amp \
  --eval-runs 10 \
  --phase2-mixed \
  --log-path logs/_gpt/layer_sensitivity_convnext_c4_gpt.log

$PY train_tinyvit.py \
  --mode eval \
  --experiment V4 \
  --dataset cifar10 \
  --device cuda \
  --amp \
  --eval-runs 10 \
  --retention-sweep \
  --results-json-path report_md/_gpt/json_gpt/tinyvit_v4_retention_results_gpt.json \
  --results-csv-path report_md/_gpt/csv_gpt/tinyvit_v4_retention_results_gpt.csv \
  --results-md-path report_md/_gpt/tinyvit_v4_retention_results_gpt.md \
  --log-path logs/_gpt/tinyvit_v4_retention_gpt.log

$PY visualize_attention.py \
  --device cuda \
  --log-path logs/_gpt/visualize_attention_gpt.log

$PY paper/plot_paper_figures.py
