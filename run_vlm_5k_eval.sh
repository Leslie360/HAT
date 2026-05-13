#!/bin/bash
# Eval Qwen3-VL 5000-step checkpoint on GPU 6
set -e

CKPT="/home/lisq753/projects/HAT_kv107/paper2/results/remote107/checkpoints/vlm_hat_last1_seed42"
OUT_DIR="/home/lisq753/projects/HAT_kv107/paper2/results/remote107/vlm_5k_eval"
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

        echo "Image: $img_tag | Config: $cfg_name"

        if [ "$cfg_name" = "clean" ]; then
            CUDA_VISIBLE_DEVICES=6 $PYTHON $SCRIPT \
                --model_name Qwen/Qwen3-VL-2B-Instruct \
                --checkpoint_dir "$CKPT" \
                --image_path "$img_path" \
                --prompt "Describe this image in detail." \
                --device cuda --fp16 \
                --output_dir "$OUT_DIR" \
                2>&1 | tee -a "$OUT_DIR/${img_tag}_${cfg_name}.log"
        else
            CUDA_VISIBLE_DEVICES=6 $PYTHON $SCRIPT \
                --model_name Qwen/Qwen3-VL-2B-Instruct \
                --checkpoint_dir "$CKPT" \
                --image_path "$img_path" \
                --prompt "Describe this image in detail." \
                --analog \
                --analog_layers "$layers" \
                --n_states 256 --sigma_c2c 0.01 --sigma_d2d 0.02 \
                --device cuda --fp16 \
                --output_dir "$OUT_DIR" \
                2>&1 | tee -a "$OUT_DIR/${img_tag}_${cfg_name}.log"
        fi
    done
done

echo "All done. Results in $OUT_DIR"
