#!/bin/bash
# Work 2 minimum experiment matrix (per Codex Round 5 recommendation)
# Run after block calibration bug is fixed

set -e
CKPT="/home/qiaosir/projects/compute_vit/checkpoints/_gpt/r1_clean_anchor/V4_hybrid_standard_noise_hat_r1_clean_anchor_first_order_best.pt"
DEVICE="cuda"
BASE_CMD="/home/qiaosir/miniconda3/envs/LLM/bin/python /home/qiaosir/projects/compute_vit/scripts/_gpt/run_block_calibration_eval.py"

echo "===== Work 2 Experiment Matrix ====="
echo "Checkpoint: $CKPT"
echo "Start: $(date)"

# E2: all_analog + block_affine_calib (64 samples)
echo ""
echo "=== E2: all_analog + block_calib_64 ==="
$BASE_CMD \
  --checkpoint $CKPT \
  --num-calib-samples 64 \
  --fresh-instances 5 \
  --eval-runs 3 \
  --resample-scope all \
  --calib-target all_blocks \
  --protected-group all \
  --protected-nl-ltp 1.0 \
  --protected-nl-ltd -1.0 \
  --device $DEVICE \
  --json-out report_md/_gpt/json_gpt/work2_e2_all_analog_block_calib_64.json

# E3: mlp_digital_proxy + attention_block_affine_calib (64 samples)
echo ""
echo "=== E3: mlp_digital + attention_block_calib_64 ==="
$BASE_CMD \
  --checkpoint $CKPT \
  --num-calib-samples 64 \
  --fresh-instances 5 \
  --eval-runs 3 \
  --resample-scope all \
  --calib-target attention_only \
  --apply-mlp-digital \
  --protected-group all \
  --protected-nl-ltp 1.0 \
  --protected-nl-ltd -1.0 \
  --device $DEVICE \
  --json-out report_md/_gpt/json_gpt/work2_e3_mlp_digital_attn_block_calib_64.json

# E2b: all_analog + block_calib_16 (sample sensitivity)
echo ""
echo "=== E2b: all_analog + block_calib_16 ==="
$BASE_CMD \
  --checkpoint $CKPT \
  --num-calib-samples 16 \
  --fresh-instances 5 \
  --eval-runs 3 \
  --resample-scope all \
  --calib-target all_blocks \
  --protected-group all \
  --protected-nl-ltp 1.0 \
  --protected-nl-ltd -1.0 \
  --device $DEVICE \
  --json-out report_md/_gpt/json_gpt/work2_e2b_all_analog_block_calib_16.json

# E2c: all_analog + block_calib_128 (sample sensitivity)
echo ""
echo "=== E2c: all_analog + block_calib_128 ==="
$BASE_CMD \
  --checkpoint $CKPT \
  --num-calib-samples 128 \
  --fresh-instances 5 \
  --eval-runs 3 \
  --resample-scope all \
  --calib-target all_blocks \
  --protected-group all \
  --protected-nl-ltp 1.0 \
  --protected-nl-ltd -1.0 \
  --device $DEVICE \
  --json-out report_md/_gpt/json_gpt/work2_e2c_all_analog_block_calib_128.json

# E0 baseline (no calibration, for reference)
echo ""
echo "=== E0: all_analog baseline (no calib) ==="
$BASE_CMD \
  --checkpoint $CKPT \
  --num-calib-samples 0 \
  --fresh-instances 5 \
  --eval-runs 3 \
  --resample-scope all \
  --calib-target all_blocks \
  --protected-group all \
  --protected-nl-ltp 1.0 \
  --protected-nl-ltd -1.0 \
  --device $DEVICE \
  --json-out report_md/_gpt/json_gpt/work2_e0_all_analog_baseline.json

echo ""
echo "===== All experiments completed ====="
echo "End: $(date)"
