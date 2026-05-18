#!/bin/bash
set -euo pipefail

PY="/home/lisq753/miniconda3/envs/LLM/bin/python"
SCRIPT="/home/lisq753/projects/HAT/HAT/p3_hat_lm_eval.py"
OUT="/home/lisq753/projects/HAT_kv107/paper2/results/remote107"
CKPT_BASE="/home/lisq753/projects/HAT_kv107/paper2/results/remote107/checkpoints"

# p69b last2
echo "[$(date +%H:%M:%S)] p69b last2 clean"
CUDA_VISIBLE_DEVICES=6 "$PY" "$SCRIPT" \
  --checkpoint_dir "$CKPT_BASE/p69b_hat_last2_fixed500_seed42_seed42" \
  --tasks lambada_openai,hellaswag,arc_easy \
  --max_length 2048 --fp16 --device cuda --output_dir "$OUT" \
  > "$OUT/gpu6_p69b_last2_clean.log" 2>&1

echo "[$(date +%H:%M:%S)] p69b last2 analog"
CUDA_VISIBLE_DEVICES=6 "$PY" "$SCRIPT" \
  --checkpoint_dir "$CKPT_BASE/p69b_hat_last2_fixed500_seed42_seed42" \
  --tasks lambada_openai,hellaswag,arc_easy \
  --analog --max_length 2048 --fp16 --device cuda --output_dir "$OUT" \
  > "$OUT/gpu6_p69b_last2_analog.log" 2>&1

# p69b last4
echo "[$(date +%H:%M:%S)] p69b last4 clean"
CUDA_VISIBLE_DEVICES=6 "$PY" "$SCRIPT" \
  --checkpoint_dir "$CKPT_BASE/p69b_hat_last4_fixed500_seed42_seed42" \
  --tasks lambada_openai,hellaswag,arc_easy \
  --max_length 2048 --fp16 --device cuda --output_dir "$OUT" \
  > "$OUT/gpu6_p69b_last4_clean.log" 2>&1

echo "[$(date +%H:%M:%S)] p69b last4 analog"
CUDA_VISIBLE_DEVICES=6 "$PY" "$SCRIPT" \
  --checkpoint_dir "$CKPT_BASE/p69b_hat_last4_fixed500_seed42_seed42" \
  --tasks lambada_openai,hellaswag,arc_easy \
  --analog --max_length 2048 --fp16 --device cuda --output_dir "$OUT" \
  > "$OUT/gpu6_p69b_last4_analog.log" 2>&1

echo "[$(date +%H:%M:%S)] GPU6 batch complete."
