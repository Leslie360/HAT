#!/usr/bin/env bash
set -euo pipefail
cd /home/qiaosir/projects/compute_vit
LOG=logs/_gpt/cx_k3_nocompile_smoke_0p10.log
: > "$LOG"
exec /home/qiaosir/miniconda3/envs/LLM/bin/python scripts/_gpt/run_tinyvit_groupwise_nl_comp.py \
  --protected-group mlp \
  --protected-nl-ltp 1.0 \
  --protected-nl-ltd -1.0 \
  --use-second-order-ste \
  --delta-g-eff 0.10 \
  --name-suffix _k3_nocompile_smoke_0p10 \
  --mode train \
  --dataset cifar10 \
  --experiments V4 \
  --epochs 1 \
  --batch-size 256 \
  --num-workers 2 \
  --device cuda \
  --amp \
  --nl-ltp 2.0 \
  --nl-ltd -2.0 \
  --warm-start-from checkpoints/_gpt/second_order_ste/V4_hybrid_standard_noise_hat_second_order_ste_best.pt \
  --save-dir checkpoints/_gpt/cx_k3_dgeff_smoke/k3_nocompile_smoke_0p10 \
  --log-interval 5 \
  --log-path "$LOG" \
  --results-json-path report_md/_gpt/json_gpt/cx_k3_nocompile_smoke_0p10.json \
  --results-csv-path report_md/_gpt/csv_gpt/cx_k3_nocompile_smoke_0p10.csv \
  --results-md-path report_md/_gpt/cx_k3_nocompile_smoke_0p10.md
