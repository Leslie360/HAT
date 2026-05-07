"""
Layer-wise analog KV sensitivity sweep.

Evaluates PPL when only a single layer is analog (all others digital).
Uses the pretrained digital model as baseline — no HAT training.
"""

import os
import sys
import time
import json
import subprocess

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

sys.path.insert(0, '/home/lisq753/projects/HAT/HAT')
from analog_kv_cache import AnalogKVCacheConfig
from analog_layers import AnalogLinearConfig
from p3_hat_train import patch_model_for_hat, evaluate_ppl


OUT_DIR = "/home/lisq753/projects/HAT/HAT/deliverable/results_v3/layer_wise"
os.makedirs(OUT_DIR, exist_ok=True)


def eval_layer(layer_idx: int, device: str = "cuda"):
    """Eval PPL when only layer_idx is analog."""
    analog_cfg = AnalogLinearConfig(
        n_states=256,
        sigma_c2c=0.0,
        sigma_d2d=0.02,
    )

    model = AutoModelForCausalLM.from_pretrained(
        "EleutherAI/pythia-410m-deduped",
        torch_dtype=torch.float32,
    )
    tokenizer = AutoTokenizer.from_pretrained("EleutherAI/pythia-410m-deduped")
    tokenizer.pad_token = tokenizer.eos_token
    model = model.to(device)

    patch_model_for_hat(model, analog_cfg, {layer_idx},
                        max_length=512,
                        retention_step_time=0.0,
                        d2d_seed=42)

    ppl = evaluate_ppl(model, tokenizer, device, max_length=512)
    return ppl


def main():
    results = []
    for layer_idx in range(24):
        print(f"[Layer {layer_idx}/23] Evaluating...")
        start = time.time()
        ppl = eval_layer(layer_idx)
        elapsed = time.time() - start
        print(f"  PPL = {ppl:.2f}  ({elapsed:.1f}s)")
        results.append({"layer": layer_idx, "ppl": ppl, "time": elapsed})

    # Save aggregate
    out_file = os.path.join(OUT_DIR, "layer_wise_ppl.json")
    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved: {out_file}")

    # Print table
    print("\nLayer | PPL")
    print("-" * 15)
    for r in results:
        marker = " ***" if r["layer"] == 23 else ""
        print(f"  {r['layer']:2d}  | {r['ppl']:.2f}{marker}")


if __name__ == "__main__":
    main()
