"""
Evaluate a HAT-trained checkpoint under various noise configurations.

Loads a saved checkpoint, monkey-patches attention for analog KV injection,
and reports PPL on WikiText-2 test.
"""

import math
import os
import sys
import json
import argparse

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analog_kv_cache import AnalogKVCacheConfig
from analog_layers import AnalogLinearConfig
from p3_hat_train import patch_model_for_hat, evaluate_ppl


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint_dir", type=str, required=True)
    parser.add_argument("--n_states", type=int, default=256)
    parser.add_argument("--sigma_c2c", type=float, default=0.01)
    parser.add_argument("--sigma_d2d", type=float, default=0.0)
    parser.add_argument("--analog_layers", type=str, default=None,
                        help="Override analog layers (auto-loads from hat_config.json if not set)")
    parser.add_argument("--d2d-seed", type=int, default=None, dest="d2d_seed",
                        help="D2D noise pattern seed (auto-loads from hat_config.json if not set)")
    parser.add_argument("--max_length", type=int, default=512)
    parser.add_argument("--output_dir", type=str, default=None)
    parser.add_argument("--device", type=str, default="cuda")
    parser.add_argument("--retention_step_time", type=float, default=0.0,
                        help="Retention decay step time in seconds per token position.")
    args = parser.parse_args()

    # Default output_dir: parent of checkpoint_dir
    if args.output_dir is None:
        args.output_dir = os.path.dirname(args.checkpoint_dir.rstrip('/'))

    # Auto-load hat_config.json from checkpoint for analog_layers + d2d_seed
    hat_config_path = os.path.join(args.checkpoint_dir, "hat_config.json")
    d2d_seed = args.d2d_seed
    analog_layers = set(int(x) for x in args.analog_layers.split(",")) if args.analog_layers else None
    if os.path.isfile(hat_config_path):
        with open(hat_config_path) as f:
            hat_cfg = json.load(f)
        if analog_layers is None and "analog_layers" in hat_cfg:
            analog_layers = set(hat_cfg["analog_layers"])
            print(f"Auto-loaded analog_layers from hat_config.json: {analog_layers}")
        if d2d_seed is None and "d2d_seed" in hat_cfg:
            d2d_seed = hat_cfg["d2d_seed"]
            print(f"Auto-loaded d2d_seed from hat_config.json: {d2d_seed}")
    if d2d_seed is None:
        d2d_seed = 0xD2D  # backward compat: old checkpoints without hat_config.json, d2d_seed=53714

    analog_cfg = AnalogLinearConfig(
        n_states=args.n_states,
        sigma_c2c=args.sigma_c2c,
        sigma_d2d=args.sigma_d2d,
    )

    print(f"Loading checkpoint from {args.checkpoint_dir}...")
    model = AutoModelForCausalLM.from_pretrained(
        args.checkpoint_dir,
        torch_dtype=torch.float32,
    )
    tokenizer = AutoTokenizer.from_pretrained(args.checkpoint_dir)
    tokenizer.pad_token = tokenizer.eos_token
    model = model.to(args.device)

    print("Patching attention layers for analog KV...")
    patch_model_for_hat(model, analog_cfg, analog_layers,
                        max_length=args.max_length,
                        retention_step_time=args.retention_step_time,
                        d2d_seed=d2d_seed)

    print(f"\nEvaluating PPL (C2C={args.sigma_c2c}, D2D={args.sigma_d2d})...")
    ppl = evaluate_ppl(model, tokenizer, args.device, max_length=args.max_length)
    print(f"PPL: {ppl:.2f}")

    result = {
        "checkpoint_dir": args.checkpoint_dir,
        "n_states": args.n_states,
        "sigma_c2c": args.sigma_c2c,
        "sigma_d2d": args.sigma_d2d,
        "d2d_seed": d2d_seed,
        "retention_step_time": args.retention_step_time,
        "analog_layers": sorted(analog_layers) if analog_layers else list(range(model.config.num_hidden_layers)),
        "ppl": ppl,
    }

    out_file = os.path.join(
        args.output_dir,
        f"eval_{args.checkpoint_dir.rstrip('/').split('/')[-1]}_c2c{args.sigma_c2c}_d2d{args.sigma_d2d}.json"
    )
    with open(out_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_file}")


if __name__ == "__main__":
    main()
