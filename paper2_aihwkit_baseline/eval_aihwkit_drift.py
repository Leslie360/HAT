#!/usr/bin/env python3
"""
R11D-4 PCM drift evaluation.
Load a trained checkpoint, apply drift_analog_weights at multiple inference
times (0s baseline, 1h, 24h), and evaluate accuracy on CIFAR-10.

Usage:
    python eval_aihwkit_drift.py \
        --checkpoint paper2_aihwkit_baseline/checkpoints/r11d_4_pcm_fixed/best.pt
"""

import argparse
import json
import os
import sys
from datetime import datetime

import numpy as np
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms

from aihwkit.nn import AnalogLinear
from aihwkit.simulator.configs import InferenceRPUConfig
from aihwkit.simulator.parameters.inference import WeightModifierType

sys.stdout.reconfigure(line_buffering=True)


def make_rpu_config(inp_res=1.0 / 256.0, out_res=1.0 / 256.0, modifier_std_dev=0.10):
    cfg = InferenceRPUConfig()
    cfg.forward.inp_res = inp_res
    cfg.forward.out_res = out_res
    cfg.modifier.type = WeightModifierType.ADD_NORMAL
    cfg.modifier.std_dev = modifier_std_dev
    cfg.modifier.enable_during_test = False  # drift eval measures drift, not D2D noise
    return cfg


def replace_linear_with_analog(module, rpu_config):
    for name, child in list(module.named_children()):
        if isinstance(child, nn.Linear):
            analog = AnalogLinear(child.in_features, child.out_features, bias=child.bias is not None, rpu_config=rpu_config)
            with torch.no_grad():
                analog.set_weights(child.weight, child.bias)
            setattr(module, name, analog)
        else:
            replace_linear_with_analog(child, rpu_config)


def build_model(num_classes=10, inp_res=1.0 / 256.0, out_res=1.0 / 256.0, modifier_std_dev=0.10):
    import timm
    model = timm.create_model("tiny_vit_5m_224", num_classes=num_classes, pretrained=False)
    replace_linear_with_analog(
        model,
        make_rpu_config(inp_res=inp_res, out_res=out_res, modifier_std_dev=modifier_std_dev),
    )
    return model


def get_test_loader(batch_size=64, num_workers=2, pin=False):
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])
    test_ds = torchvision.datasets.CIFAR10(root="./data", train=False, download=True, transform=transform)
    return torch.utils.data.DataLoader(test_ds, batch_size=batch_size, shuffle=False, num_workers=num_workers, pin_memory=pin)


@torch.no_grad()
def evaluate(model, loader, device):
    model.eval()
    correct = 0
    total = 0
    for inputs, targets in loader:
        inputs, targets = inputs.to(device), targets.to(device)
        outputs = model(inputs)
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()
    return 100.0 * correct / total


def apply_drift(model, t_inference):
    """Call drift_analog_weights on every module that supports it (module-level API)."""
    n_drifted = 0
    for module in model.modules():
        if hasattr(module, "drift_analog_weights"):
            module.drift_analog_weights(t_inference=t_inference)
            n_drifted += 1
    return n_drifted


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--output", default=None)
    parser.add_argument("--inp-res", type=float, default=None)
    parser.add_argument("--out-res", type=float, default=None)
    parser.add_argument("--modifier-std-dev", type=float, default=None)
    args = parser.parse_args()

    device = torch.device(args.device)
    print(f"[DriftEval] Loading checkpoint: {args.checkpoint}")

    ckpt = torch.load(args.checkpoint, map_location=device, weights_only=False)
    ckpt_args = ckpt.get("args", {})
    ckpt_rpu = ckpt.get("rpu_config_spec", {})

    # Check if checkpoint was trained with PCM device model
    pcm_preset = ckpt_rpu.get("pcm_preset") or ckpt_args.get("pcm_preset")
    if not pcm_preset:
        print(f"[DriftEval] WARNING: Checkpoint was not trained with a PCM device model (pcm_preset={pcm_preset!r}).")
        print("[DriftEval] Drift evaluation is only physically meaningful for PCM-trained checkpoints.")
        print("[DriftEval] Skipping drift eval. Generate a placeholder JSON with explanation.")

        output = {
            "checkpoint": args.checkpoint,
            "drift_times_seconds": [0.0, 3600.0, 86400.0],
            "results": [],
            "skipped": True,
            "skip_reason": "Checkpoint was not trained with PCM device model. Drift evaluation is not physically meaningful for non-PCM presets.",
            "device": str(device),
            "time": datetime.now().isoformat(),
        }
        if args.output is None:
            ckpt_dir = os.path.dirname(args.checkpoint)
            args.output = os.path.join(ckpt_dir, "drift_eval.json")
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, "w") as f:
            json.dump(output, f, indent=2)
        print(f"[DriftEval] Saved skip marker: {args.output}")
        return

    inp_res = args.inp_res if args.inp_res is not None else ckpt_rpu.get("forward_inp_res", ckpt_args.get("inp_res", 1.0 / 256.0))
    out_res = args.out_res if args.out_res is not None else ckpt_rpu.get("forward_out_res", ckpt_args.get("out_res", 1.0 / 256.0))
    modifier_std_dev = args.modifier_std_dev if args.modifier_std_dev is not None else ckpt_rpu.get("modifier_std_dev", ckpt_args.get("modifier_std_dev", 0.10))

    drift_times = [0.0, 3600.0, 86400.0]
    print(f"[DriftEval] Config: inp_res={inp_res}, out_res={out_res}, modifier_std_dev={modifier_std_dev}")
    print(f"[DriftEval] PCM preset: {pcm_preset}")
    print(f"[DriftEval] Drift times: {drift_times}")

    test_loader = get_test_loader(batch_size=args.batch_size, num_workers=args.workers, pin=device.type == "cuda")

    if args.output is None:
        ckpt_dir = os.path.dirname(args.checkpoint)
        args.output = os.path.join(ckpt_dir, "drift_eval.json")

    results = []
    for t in drift_times:
        # Build fresh model for each time point to avoid cumulative drift artifacts
        model = build_model(num_classes=10, inp_res=inp_res, out_res=out_res, modifier_std_dev=modifier_std_dev)
        model.load_state_dict(ckpt["model_state_dict"])

        # Re-apply eval RPU config (load_state_dict restores checkpoint config)
        rpu_cfg = make_rpu_config(inp_res=inp_res, out_res=out_res, modifier_std_dev=modifier_std_dev)
        for module in model.modules():
            if hasattr(module, "replace_rpu_config"):
                module.replace_rpu_config(rpu_cfg)

        model = model.to(device)
        model.eval()

        if t > 0:
            n = apply_drift(model, t)
            print(f"[DriftEval] t={t:6.0f}s: drifted {n} layers, evaluating...")
        else:
            print(f"[DriftEval] t={t:6.0f}s: baseline (no drift), evaluating...")

        acc = evaluate(model, test_loader, device)
        results.append({"t_inference_seconds": t, "t_label": f"{t:.0f}s" if t > 0 else "0s (no drift)", "accuracy": round(acc, 4)})
        print(f"[DriftEval]   -> accuracy: {acc:.2f}%")

        del model
        torch.cuda.empty_cache()

    output = {
        "checkpoint": args.checkpoint,
        "drift_times_seconds": drift_times,
        "results": results,
        "config": {
            "forward_inp_res": inp_res,
            "forward_out_res": out_res,
            "modifier_type": "ADD_NORMAL",
            "modifier_std_dev": modifier_std_dev,
            "modifier_enable_during_test": False,
        },
        "device": str(device),
        "time": datetime.now().isoformat(),
    }
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)
    print(f"[DriftEval] Saved: {args.output}")


if __name__ == "__main__":
    main()
