#!/usr/bin/env python3
"""Apply a hybrid deployment policy by splicing analog and digital checkpoints.

Given:
  - analog checkpoint (e.g., R1 with full analog layers)
  - digital checkpoint (e.g., V2 with no noise)
  - deployment policy from hybrid_runtime_compiler.py

Produces a hybrid model state dict where:
  - CIM layers come from the analog checkpoint
  - digital_fallback layers come from the digital checkpoint
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import torch


def load_state_dict(path: str):
    ckpt = torch.load(path, map_location="cpu", weights_only=False)
    return ckpt.get("model_state_dict", ckpt)


def apply_policy(analog_ckpt_path: str, digital_ckpt_path: str, policy_json: str, output_path: str):
    analog_sd = load_state_dict(analog_ckpt_path)
    digital_sd = load_state_dict(digital_ckpt_path)
    
    with open(policy_json) as f:
        policy_data = json.load(f)
    
    policies = {p["layer_name"]: p for p in policy_data["policies"]}
    
    hybrid_sd = {}
    source_stats = {"analog": 0, "digital": 0, "unknown": 0}
    
    for key in analog_sd.keys():
        # Find which layer this key belongs to
        layer_name = key.replace(".weight", "").replace(".bias", "").replace(".running_mean", "").replace(".running_var", "").replace(".num_batches_tracked", "")
        
        # Try exact match first
        policy = policies.get(layer_name)
        if policy is None:
            # Try with .weight suffix
            policy = policies.get(layer_name + ".weight")
        
        if policy is None:
            # Default: keep analog
            hybrid_sd[key] = analog_sd[key]
            source_stats["analog"] += 1
            continue
        
        action = policy["action"]
        if action == "digital_fallback":
            hybrid_sd[key] = digital_sd[key]
            source_stats["digital"] += 1
        else:
            hybrid_sd[key] = analog_sd[key]
            source_stats["analog"] += 1
    
    # Save hybrid checkpoint
    output_ckpt = {
        "model_state_dict": hybrid_sd,
        "hybrid_policy": policy_data,
        "source_analog": analog_ckpt_path,
        "source_digital": digital_ckpt_path,
    }
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    torch.save(output_ckpt, output_path)
    
    print(f"Hybrid checkpoint saved to: {output_path}")
    print(f"  Layers from analog: {source_stats['analog']}")
    print(f"  Layers from digital: {source_stats['digital']}")
    print(f"  Unknown (default analog): {source_stats['unknown']}")
    return output_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--analog-ckpt", required=True, help="Analog checkpoint (e.g., R1)")
    parser.add_argument("--digital-ckpt", required=True, help="Digital checkpoint (e.g., V2)")
    parser.add_argument("--policy-json", required=True, help="Deployment policy JSON")
    parser.add_argument("--output", required=True, help="Output hybrid checkpoint path")
    args = parser.parse_args()
    
    apply_policy(args.analog_ckpt, args.digital_ckpt, args.policy_json, args.output)


if __name__ == "__main__":
    main()
