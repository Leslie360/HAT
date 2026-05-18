#!/bin/bash
set -euo pipefail

PY="/home/lisq753/miniconda3/envs/LLM/bin/python"
SCRIPT="/home/lisq753/projects/HAT/HAT/p3_hat_lm_eval.py"
OUT="/home/lisq753/projects/HAT_kv107/paper2/results/remote107"
CKPT_BASE="/home/lisq753/projects/HAT_kv107/paper2/results/remote107/checkpoints"

# p28b last2
echo "[$(date +%H:%M:%S)] p28b last2 clean"
CUDA_VISIBLE_DEVICES=5 "$PY" "$SCRIPT" \
  --checkpoint_dir "$CKPT_BASE/p28b_last2_fixed500_seed42" \
  --tasks lambada_openai,hellaswag,arc_easy \
  --max_length 2048 --fp16 --device cuda --output_dir "$OUT" \
  > "$OUT/gpu5_p28b_last2_clean.log" 2>&1

echo "[$(date +%H:%M:%S)] p28b last2 analog"
CUDA_VISIBLE_DEVICES=5 "$PY" "$SCRIPT" \
  --checkpoint_dir "$CKPT_BASE/p28b_last2_fixed500_seed42" \
  --tasks lambada_openai,hellaswag,arc_easy \
  --analog --max_length 2048 --fp16 --device cuda --output_dir "$OUT" \
  > "$OUT/gpu5_p28b_last2_analog.log" 2>&1

# p28b last4
echo "[$(date +%H:%M:%S)] p28b last4 clean"
CUDA_VISIBLE_DEVICES=5 "$PY" "$SCRIPT" \
  --checkpoint_dir "$CKPT_BASE/p28b_last4_fixed500_seed42" \
  --tasks lambada_openai,hellaswag,arc_easy \
  --max_length 2048 --fp16 --device cuda --output_dir "$OUT" \
  > "$OUT/gpu5_p28b_last4_clean.log" 2>&1

echo "[$(date +%H:%M:%S)] p28b last4 analog"
CUDA_VISIBLE_DEVICES=5 "$PY" "$SCRIPT" \
  --checkpoint_dir "$CKPT_BASE/p28b_last4_fixed500_seed42" \
  --tasks lambada_openai,hellaswag,arc_easy \
  --analog --max_length 2048 --fp16 --device cuda --output_dir "$OUT" \
  > "$OUT/gpu5_p28b_last4_analog.log" 2>&1

echo "[$(date +%H:%M:%S)] GPU5 batch complete."
