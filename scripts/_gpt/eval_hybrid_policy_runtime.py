#!/usr/bin/env python3
"""Evaluate a hybrid policy by per-layer noise control (NO weight splicing).

Loads a single analog checkpoint, then applies per-layer noise settings
based on deployment policy:
  - digital_fallback: noise_enabled=False, sigma_c2c=0, sigma_d2d=0
  - cim_keep: original analog settings
  - cim_calibrate: analog with calibration

This avoids feature distribution mismatch from checkpoint splicing.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from statistics import mean, stdev

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import torch
import torch.nn as nn

from analog_layers import AnalogConv2d, AnalogLinear
from run_tinyvit_groupwise_nl_comp import build_selector
import train_tinyvit_ensemble as base
from train_tinyvit_ensemble import (
    TinyViTExperimentConfig,
    build_model,
    evaluate,
    get_dataloaders,
    resample_all_d2d_noise,
)
from train_tinyvit import set_seed

AnalogModule = (AnalogLinear, AnalogConv2d)


def apply_hybrid_policy_to_model(model: nn.Module, policy: dict, digital_mode: bool = True):
    """Apply deployment policy to model by modifying per-layer config."""
    policies_by_layer = {p["layer_name"]: p for p in policy["policies"]}
    
    for name, module in model.named_modules():
        if not isinstance(module, AnalogModule):
            continue
        
        # Match layer name to policy
        layer_key = name
        if layer_key not in policies_by_layer:
            layer_key = name + ".weight"
        if layer_key not in policies_by_layer:
            continue
        
        action = policies_by_layer[layer_key]["action"]
        
        if action == "digital_fallback" and digital_mode:
            # Disable analog noise for digital fallback
            module.config.noise_enabled = False
            module.config.sigma_c2c = 0.0
            module.config.sigma_d2d = 0.0
        elif action == "cim_calibrate":
            # Keep analog but enable calibration mode
            pass  # TODO: implement calibration


def evaluate_hybrid_policy(
    checkpoint_path: str,
    policy_json: str,
    device: str,
    fresh_instances: int,
    eval_runs: int,
    data_root: str,
    num_workers: int,
    resample_scope: str = "all",
    dataset: str | None = None,
    eval_batch_size: int | None = None,
    num_classes: int | None = None,
) -> dict:
    print(f"\nHybrid policy eval: resample_scope='{resample_scope}'")
    print(f"Checkpoint: {checkpoint_path}", flush=True)
    
    with open(policy_json) as f:
        policy = json.load(f)
    
    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    exp_cfg_dict = ckpt.get("exp_cfg", {})
    valid_keys = {f.name for f in __import__("dataclasses").fields(TinyViTExperimentConfig)}
    filtered = {k: v for k, v in exp_cfg_dict.items() if k in valid_keys}
    cfg = TinyViTExperimentConfig(**filtered)
    resolved_dataset = dataset or ckpt.get("dataset") or "cifar10"
    head_weight = (ckpt.get("model_state_dict") or {}).get("head.fc.weight")
    resolved_num_classes = num_classes
    if resolved_num_classes is None:
        if ckpt.get("num_classes") is not None:
            resolved_num_classes = int(ckpt["num_classes"])
        elif head_weight is not None:
            resolved_num_classes = int(head_weight.shape[0])
        else:
            resolved_num_classes = 10
    resolved_batch_size = eval_batch_size or 256
    
    _, testloader = get_dataloaders(
        dataset=resolved_dataset,
        batch_size=resolved_batch_size,
        data_root=data_root,
        num_workers=num_workers,
    )
    criterion = nn.CrossEntropyLoss()
    
    instance_means = []
    instance_rows = []
    
    for instance_idx in range(fresh_instances):
        seed = 42 + instance_idx * 100
        set_seed(seed)
        model = build_model(cfg, num_classes=resolved_num_classes, device=device, pretrained=False)
        model.load_state_dict(ckpt["model_state_dict"], strict=True)
        
        # Apply hybrid policy BEFORE resampling
        apply_hybrid_policy_to_model(model, policy, digital_mode=True)
        
        # Then resample D2D for remaining analog layers
        if resample_scope == "all":
            resampled = resample_all_d2d_noise(model)
        elif resample_scope == "none":
            resampled = 0
        else:
            # Selective resampling
            selector = build_selector(resample_scope)
            resampled = 0
            for name, m in model.named_modules():
                if hasattr(m, "resample_d2d_noise") and callable(m.resample_d2d_noise):
                    if selector(name):
                        m.resample_d2d_noise()
                        resampled += 1
        
        losses = []
        accs = []
        for _ in range(eval_runs):
            loss, acc = evaluate(model, testloader, criterion, device, cfg, amp_enabled=False)
            losses.append(float(loss))
            accs.append(float(acc))
        
        mean_acc = mean(accs)
        print(
            f"  instance {instance_idx + 1:02d}/{fresh_instances}: "
            f"mean_acc={mean_acc:.2f}% eval_runs={eval_runs} resampled={resampled}",
            flush=True,
        )
        instance_means.append(mean_acc)
        instance_rows.append(
            {
                "instance_index": instance_idx,
                "seed": seed,
                "resampled_modules": resampled,
                "resample_scope": resample_scope,
                "eval_runs": eval_runs,
                "test_loss_mean": mean(losses),
                "test_acc_mean": mean_acc,
                "test_acc_std": stdev(accs) if len(accs) > 1 else 0.0,
                "test_acc_raw": accs,
            }
        )
    
    result = {
        "checkpoint_path": checkpoint_path,
        "policy_json": policy_json,
        "train_best_acc": float(ckpt.get("best_acc", float("nan"))),
        "fresh_instances": fresh_instances,
        "mc_runs_per_instance": eval_runs,
        "resample_scope": resample_scope,
        "dataset": resolved_dataset,
        "num_classes": resolved_num_classes,
        "eval_batch_size": resolved_batch_size,
        "cross_instance_mean": mean(instance_means),
        "cross_instance_std": stdev(instance_means) if len(instance_means) > 1 else 0.0,
        "instance_means": instance_means,
        "instances": instance_rows,
    }
    print(
        f"Completed scope='{resample_scope}': {result['cross_instance_mean']:.2f}% +/- "
        f"{result['cross_instance_std']:.2f}% across {fresh_instances} fresh instances",
        flush=True,
    )
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--policy-json", required=True)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--fresh-instances", type=int, default=5)
    parser.add_argument("--eval-runs", type=int, default=3)
    parser.add_argument("--data-root", default="./data")
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--resample-scope", choices=["all", "none", "mlp", "qkv", "attn_proj", "patch_embed"], default="all")
    parser.add_argument("--dataset", default=None)
    parser.add_argument("--num-classes", type=int, default=None)
    parser.add_argument("--eval-batch-size", type=int, default=None)
    parser.add_argument("--json-out", default="report_md/_gpt/json_gpt/hybrid_policy_eval.json")
    args = parser.parse_args()
    
    result = evaluate_hybrid_policy(
        checkpoint_path=args.checkpoint,
        policy_json=args.policy_json,
        device=args.device,
        fresh_instances=args.fresh_instances,
        eval_runs=args.eval_runs,
        data_root=args.data_root,
        num_workers=args.num_workers,
        resample_scope=args.resample_scope,
        dataset=args.dataset,
        eval_batch_size=args.eval_batch_size,
        num_classes=args.num_classes,
    )
    
    out_path = Path(args.json_out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"JSON saved to: {out_path}")


if __name__ == "__main__":
    main()
