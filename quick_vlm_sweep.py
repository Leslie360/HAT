#!/usr/bin/env python3
"""
Quick VLM sweep: clean vs selective last1/last2/last4 on multiple images.
Loads model once, runs all configs sequentially.

Usage:
    CUDA_VISIBLE_DEVICES=3 python quick_vlm_sweep.py
"""

import os
import sys
import json
import time

sys.path.insert(0, '/home/lisq753/projects/HAT/HAT')
from p3_hat_vlm_eval import load_model_for_eval, generate, patch_vlm_for_hat
from analog_layers import AnalogLinearConfig

MODEL = "Qwen/Qwen3-VL-2B-Instruct"
DEVICE = "cuda"
FP16 = True

IMAGES = [
    ("/tmp/test_vlm.jpg", "cat"),
    ("/tmp/vlm_landscape.jpg", "landscape"),
    ("/tmp/vlm_person.jpg", "person"),
    ("/tmp/vlm_interior.jpg", "interior"),
    ("/tmp/vlm_chart.png", "chart"),
]

PROMPT = "Describe this image in detail."

CONFIGS = [
    ("clean", None, None),
    ("last1", "27", None),
    ("last2", "26,27", None),
    ("last4", "24,25,26,27", None),
]

ANALOG_CFG = AnalogLinearConfig(n_states=256, sigma_c2c=0.01, sigma_d2d=0.02)

OUT_DIR = "/home/lisq753/projects/HAT_kv107/paper2/results/remote107/vlm_sweep_20260511"
os.makedirs(OUT_DIR, exist_ok=True)


def main():
    print(f"Loading {MODEL}...")
    model, processor, family = load_model_for_eval(MODEL, device=DEVICE, fp16=FP16)

    num_layers = getattr(model.config, "num_hidden_layers", None)
    if num_layers is None and hasattr(model.config, "text_config"):
        num_layers = model.config.text_config.num_hidden_layers

    for img_path, tag in IMAGES:
        print(f"\n{'='*60}")
        print(f"Image: {tag} ({img_path})")
        print(f"{'='*60}")

        # Clean generation (once per image)
        print("\n--- CLEAN ---")
        start = time.time()
        clean_text = generate(model, processor, img_path, PROMPT, device=DEVICE, max_new_tokens=128)
        clean_time = time.time() - start
        print(clean_text[:200] + "..." if len(clean_text) > 200 else clean_text)
        print(f"Time: {clean_time:.1f}s")

        for cfg_name, layers_str, _ in CONFIGS[1:]:
            print(f"\n--- {cfg_name.upper()} ---")
            analog_layers = set(int(x) for x in layers_str.split(","))

            # Re-patch model (simpler than unpatching: just re-register buffers on target layers)
            # But patch_vlm_for_hat monkey-patches all matching layers each time.
            # To avoid double-patching, we reload the model... or we can restore original forwards first.
            # Simpler: reload model for each config to guarantee clean state.
            # However that's slow. Alternative: store _original_forward and restore before re-patching.
            pass

        # Save per-image results after all configs
        # (Will implement below)

    print("\nDone.")


if __name__ == "__main__":
    main()
