#!/bin/bash
# Eval trained Qwen3-VL checkpoint: clean vs last1/last2/last4 analog on 5 images.
# Loads model ONCE per config for isolation.

set -e

MODEL="Qwen/Qwen3-VL-2B-Instruct"
CKPT="/home/lisq753/projects/HAT_kv107/paper2/results/remote107/checkpoints/vlm_hat_last1_fixed500_seed42"
DEVICE="cuda"
PROMPT="Describe this image in detail."
OUT_DIR="/home/lisq753/projects/HAT_kv107/paper2/results/remote107/vlm_trained_eval"
PYTHON="/home/lisq753/miniconda3/envs/LLM/bin/python"
SCRIPT="/home/lisq753/projects/HAT/HAT/p3_hat_vlm_eval.py"

mkdir -p "$OUT_DIR"

declare -a IMAGES=(
    "/tmp/test_vlm.jpg cat"
    "/tmp/vlm_landscape.jpg landscape"
    "/tmp/vlm_person.jpg person"
    "/tmp/vlm_interior.jpg interior"
    "/tmp/vlm_chart.png chart"
)

declare -a CONFIGS=(
    "clean ''"
    "last1 27"
    "last2 26,27"
    "last4 24,25,26,27"
)

for img_entry in "${IMAGES[@]}"; do
    img_path=$(echo "$img_entry" | awk '{print $1}')
    img_tag=$(echo "$img_entry" | awk '{print $2}')

    for cfg_entry in "${CONFIGS[@]}"; do
        cfg_name=$(echo "$cfg_entry" | awk '{print $1}')
        layers=$(echo "$cfg_entry" | awk '{print $2}')

        echo ""
        echo "========================================"
        echo "Image: $img_tag | Config: $cfg_name"
        echo "========================================"

        if [ "$cfg_name" = "clean" ]; then
            CUDA_VISIBLE_DEVICES=3 $PYTHON $SCRIPT \
                --model_name "$MODEL" \
                --checkpoint_dir "$CKPT" \
                --image_path "$img_path" \
                --prompt "$PROMPT" \
                --device "$DEVICE" \
                --fp16 \
                --output_dir "$OUT_DIR" \
                2>&1 | tee "$OUT_DIR/${img_tag}_${cfg_name}.log"
        else
            CUDA_VISIBLE_DEVICES=3 $PYTHON $SCRIPT \
                --model_name "$MODEL" \
                --checkpoint_dir "$CKPT" \
                --image_path "$img_path" \
                --prompt "$PROMPT" \
                --analog \
                --analog_layers "$layers" \
                --n_states 256 \
                --sigma_c2c 0.01 \
                --sigma_d2d 0.02 \
                --device "$DEVICE" \
                --fp16 \
                --output_dir "$OUT_DIR" \
                2>&1 | tee "$OUT_DIR/${img_tag}_${cfg_name}.log"
        fi
    done
done

echo ""
echo "All done. Results in $OUT_DIR"
