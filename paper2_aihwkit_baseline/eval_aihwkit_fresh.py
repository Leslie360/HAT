#!/usr/bin/env python3
"""
R10E: AIHWKit fresh-instance evaluation.
Run 10 inference repetitions with fresh D2D noise realizations.
Supports CPU and GPU.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from statistics import mean, stdev

import numpy as np
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms

from aihwkit.nn import AnalogLinear
from aihwkit.simulator.configs import InferenceRPUConfig
from aihwkit.simulator.parameters.inference import WeightModifierParameter, WeightModifierType

sys.stdout.reconfigure(line_buffering=True)


def make_rpu_config():
    cfg = InferenceRPUConfig()
    cfg.forward.inp_res = 1.0 / 256.0
    cfg.forward.out_res = 1.0 / 256.0
    cfg.modifier.type = WeightModifierType.ADD_NORMAL
    cfg.modifier.std_dev = 0.10
    cfg.modifier.enable_during_test = True  # apply noise during eval for fresh-instance measurement
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


def build_model(num_classes=10):
    import timm
    model = timm.create_model("tiny_vit_5m_224", num_classes=num_classes, pretrained=False)
    replace_linear_with_analog(model, make_rpu_config())
    return model


def get_test_loader(batch_size=64, num_workers=2, pin=False):
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])
    test_ds = torchvision.datasets.CIFAR10(root="./data", train=False, download=True, transform=transform)
    return torch.utils.data.DataLoader(test_ds, batch_size=batch_size, shuffle=False, num_workers=num_workers, pin_memory=pin)


@torch.no_grad()
def evaluate_fresh(model, loader, device, seed):
    """Evaluate with a fresh noise realization."""
    torch.manual_seed(seed)
    np.random.seed(seed)
    model.eval()
    correct = 0
    total = 0
    all_preds = []
    all_targets = []
    for inputs, targets in loader:
        inputs, targets = inputs.to(device), targets.to(device)
        outputs = model(inputs)
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()
        all_preds.extend(predicted.cpu().tolist())
        all_targets.extend(targets.cpu().tolist())
    acc = 100.0 * correct / total
    return acc, all_preds, all_targets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--n-fresh", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--output", default="paper2_aihwkit_baseline/checkpoints/fresh_eval.json")
    args = parser.parse_args()

    device = torch.device(args.device)
    print(f"Loading checkpoint: {args.checkpoint}")

    model = build_model(num_classes=10)
    # AIHWKit checkpoints embed InferenceRPUConfig — torch>=2.6 weights_only=True
    # blocks unpickling. Trust local checkpoint, allow full unpickling.
    ckpt = torch.load(args.checkpoint, map_location=device, weights_only=False)
    model.load_state_dict(ckpt["model_state_dict"])
    model = model.to(device)

    test_loader = get_test_loader(batch_size=args.batch_size, num_workers=args.workers, pin=device.type == "cuda")

    results = []
    print(f"Running {args.n_fresh} fresh-instance evaluations...")
    for i in range(args.n_fresh):
        seed = 1000 + i
        acc, preds, targets = evaluate_fresh(model, test_loader, device, seed)
        results.append({"instance": i, "seed": seed, "accuracy": round(acc, 4)})
        print(f"  Fresh instance {i+1}/{args.n_fresh}: {acc:.2f}%")

    accs = [r["accuracy"] for r in results]
    mean_acc = mean(accs)
    std_acc = stdev(accs) if len(accs) > 1 else 0.0

    print(f"\nFresh-instance mean: {mean_acc:.2f}% ± {std_acc:.2f}%")

    output = {
        "checkpoint": args.checkpoint,
        "n_fresh": args.n_fresh,
        "device": str(device),
        "mean": round(mean_acc, 4),
        "std": round(std_acc, 4),
        "instances": results,
        "time": datetime.now().isoformat(),
    }
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
