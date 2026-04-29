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


def make_rpu_config(inp_res=1.0 / 256.0, out_res=1.0 / 256.0, modifier_std_dev=0.10):
    cfg = InferenceRPUConfig()
    cfg.forward.inp_res = inp_res
    cfg.forward.out_res = out_res
    cfg.modifier.type = WeightModifierType.ADD_NORMAL
    cfg.modifier.std_dev = modifier_std_dev
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


def build_model(num_classes=10, inp_res=1.0 / 256.0, out_res=1.0 / 256.0, modifier_std_dev=0.10):
    import timm
    model = timm.create_model("tiny_vit_5m_224", num_classes=num_classes, pretrained=False)
    replace_linear_with_analog(
        model,
        make_rpu_config(
            inp_res=inp_res,
            out_res=out_res,
            modifier_std_dev=modifier_std_dev,
        ),
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
    parser.add_argument("--mc-repeats", type=int, default=1)
    parser.add_argument("--fresh-seed-base", type=int, default=1000)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--output", default="paper2_aihwkit_baseline/checkpoints/fresh_eval.json")
    parser.add_argument("--inp-res", type=float, default=None)
    parser.add_argument("--out-res", type=float, default=None)
    parser.add_argument("--modifier-std-dev", type=float, default=None)
    args = parser.parse_args()

    device = torch.device(args.device)
    print(f"Loading checkpoint: {args.checkpoint}")

    # AIHWKit checkpoints embed InferenceRPUConfig — torch>=2.6 weights_only=True
    # blocks unpickling. Trust local checkpoint, allow full unpickling.
    ckpt = torch.load(args.checkpoint, map_location=device, weights_only=False)
    ckpt_args = ckpt.get("args", {})
    ckpt_rpu = ckpt.get("rpu_config_spec", {})
    inp_res = args.inp_res
    out_res = args.out_res
    modifier_std_dev = args.modifier_std_dev
    if inp_res is None:
        inp_res = ckpt_rpu.get("forward_inp_res", ckpt_args.get("inp_res", 1.0 / 256.0))
    if out_res is None:
        out_res = ckpt_rpu.get("forward_out_res", ckpt_args.get("out_res", 1.0 / 256.0))
    if modifier_std_dev is None:
        modifier_std_dev = ckpt_rpu.get("modifier_std_dev", ckpt_args.get("modifier_std_dev", 0.10))
    print(
        "Eval config: "
        f"inp_res={inp_res}, out_res={out_res}, modifier_std_dev={modifier_std_dev}, "
        f"n_fresh={args.n_fresh}, mc_repeats={args.mc_repeats}"
    )

    model = build_model(
        num_classes=10,
        inp_res=inp_res,
        out_res=out_res,
        modifier_std_dev=modifier_std_dev,
    )
    model.load_state_dict(ckpt["model_state_dict"])

    # Fix: load_state_dict restores analog_tile_state which may overwrite
    # the enable_during_test flag. Force re-apply the eval RPU config
    # with enable_during_test=True on every AnalogLinear layer.
    eval_rpu_cfg = make_rpu_config(
        inp_res=inp_res,
        out_res=out_res,
        modifier_std_dev=modifier_std_dev,
    )
    n_replaced = 0
    for module in model.modules():
        if hasattr(module, "replace_rpu_config"):
            module.replace_rpu_config(eval_rpu_cfg)
            n_replaced += 1
    print(f"[FIX] Replaced RPU config on {n_replaced} AnalogLinear layers (enable_during_test=True)")

    # Tile audit: record actual config of each analog tile after load+fix
    tile_audit = []
    for name, module in model.named_modules():
        if hasattr(module, "analog_tiles"):
            for j, tile in enumerate(module.analog_tiles()):
                rc = tile.rpu_config
                tile_audit.append({
                    "name": name,
                    "tile_idx": j,
                    "modifier_type": str(rc.modifier.type),
                    "modifier_std_dev": rc.modifier.std_dev,
                    "modifier_enable_during_test": rc.modifier.enable_during_test,
                    "device": str(type(rc.device).__name__) if hasattr(rc, "device") else "N/A",
                })
    print(f"Tile audit: {len(tile_audit)} tiles, all enable_during_test={all(t['modifier_enable_during_test'] for t in tile_audit)}")

    model = model.to(device)

    test_loader = get_test_loader(batch_size=args.batch_size, num_workers=args.workers, pin=device.type == "cuda")

    results = []
    print(f"Running {args.n_fresh} fresh-instance evaluations × {args.mc_repeats} MC repeats...")
    for i in range(args.n_fresh):
        mc_runs = []
        for j in range(args.mc_repeats):
            seed = args.fresh_seed_base + i * 100 + j
            acc, preds, targets = evaluate_fresh(model, test_loader, device, seed)
            mc_runs.append({"mc": j, "seed": seed, "accuracy": round(acc, 4)})
        mc_accs = [r["accuracy"] for r in mc_runs]
        inst_mean = mean(mc_accs)
        inst_std = stdev(mc_accs) if len(mc_accs) > 1 else 0.0
        results.append({
            "instance": i,
            "seed_base": args.fresh_seed_base + i * 100,
            "accuracy": round(inst_mean, 4),
            "mc_std": round(inst_std, 4),
            "mc_runs": mc_runs,
        })
        print(
            f"  Fresh instance {i+1}/{args.n_fresh}: "
            f"{inst_mean:.2f}% ± {inst_std:.2f}%"
        )

    accs = [r["accuracy"] for r in results]
    mean_acc = mean(accs)
    std_acc = stdev(accs) if len(accs) > 1 else 0.0

    print(f"\nFresh-instance mean: {mean_acc:.2f}% ± {std_acc:.2f}%")

    output = {
        "checkpoint": args.checkpoint,
        "n_fresh": args.n_fresh,
        "mc_repeats": args.mc_repeats,
        "fresh_seed_base": args.fresh_seed_base,
        "device": str(device),
        "rpu_config_spec": {
            "forward_inp_res": inp_res,
            "forward_out_res": out_res,
            "modifier_type": "ADD_NORMAL",
            "modifier_std_dev": modifier_std_dev,
            "modifier_enable_during_test": True,
        },
        "mean": round(mean_acc, 4),
        "std": round(std_acc, 4),
        "instances": results,
        "tile_audit": tile_audit,
        "tile_audit_all_enabled": all(t["modifier_enable_during_test"] for t in tile_audit),
        "time": datetime.now().isoformat(),
    }
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
