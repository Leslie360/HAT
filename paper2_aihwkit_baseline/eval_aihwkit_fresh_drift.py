#!/usr/bin/env python3
"""Combined fresh-instance + drift evaluation for AIHWKit PCM checkpoints.

This complements the separate fresh-only and drift-only evaluators. For each
requested drift time, it rebuilds a fresh model from the checkpoint, applies
AIHWKit drift, enables test-time weight modifier noise, and evaluates multiple
fresh noise realizations.
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
from aihwkit.simulator.parameters.inference import WeightModifierType

sys.stdout.reconfigure(line_buffering=True)


def make_rpu_config(inp_res=1.0 / 256.0, out_res=1.0 / 256.0, modifier_std_dev=0.10):
    cfg = InferenceRPUConfig()
    cfg.forward.inp_res = inp_res
    cfg.forward.out_res = out_res
    cfg.modifier.type = WeightModifierType.ADD_NORMAL
    cfg.modifier.std_dev = modifier_std_dev
    cfg.modifier.enable_during_test = True
    return cfg


def replace_linear_with_analog(module, rpu_config):
    for name, child in list(module.named_children()):
        if isinstance(child, nn.Linear):
            analog = AnalogLinear(
                child.in_features,
                child.out_features,
                bias=child.bias is not None,
                rpu_config=rpu_config,
            )
            with torch.no_grad():
                analog.set_weights(child.weight, child.bias)
            setattr(module, name, analog)
        else:
            replace_linear_with_analog(child, rpu_config)


def build_model(num_classes=10, inp_res=1.0 / 256.0, out_res=1.0 / 256.0, modifier_std_dev=0.10):
    import timm

    model = timm.create_model("tiny_vit_5m_224", num_classes=num_classes, pretrained=False)
    replace_linear_with_analog(model, make_rpu_config(inp_res, out_res, modifier_std_dev))
    return model


def get_test_loader(batch_size=64, num_workers=0, pin=False):
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])
    test_ds = torchvision.datasets.CIFAR10(root="./data", train=False, download=True, transform=transform)
    return torch.utils.data.DataLoader(
        test_ds,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin,
    )


@torch.no_grad()
def evaluate_once(model, loader, device, seed):
    torch.manual_seed(seed)
    np.random.seed(seed)
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
    model.eval()  # drift_analog_weights requires eval mode
    n_drifted = 0
    for module in model.modules():
        if hasattr(module, "drift_analog_weights"):
            module.drift_analog_weights(t_inference=t_inference)
            n_drifted += 1
    return n_drifted


def format_time(t):
    if t == 0:
        return "0s"
    if t < 3600:
        return f"{t:.0f}s"
    if t < 86400:
        return f"{t / 3600:.0f}h"
    return f"{t / 86400:.0f}d"


def tile_audit(model):
    rows = []
    for name, module in model.named_modules():
        if hasattr(module, "analog_tiles"):
            for idx, tile in enumerate(module.analog_tiles()):
                rc = tile.rpu_config
                rows.append({
                    "name": name,
                    "tile_idx": idx,
                    "modifier_type": str(rc.modifier.type),
                    "modifier_std_dev": rc.modifier.std_dev,
                    "modifier_enable_during_test": rc.modifier.enable_during_test,
                    "device": str(type(rc.device).__name__) if hasattr(rc, "device") else "N/A",
                })
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--drift-times", type=float, nargs="+", default=[0.0, 3600.0, 86400.0])
    parser.add_argument("--n-fresh", type=int, default=5)
    parser.add_argument("--mc-repeats", type=int, default=3)
    parser.add_argument("--fresh-seed-base", type=int, default=7000)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--workers", type=int, default=0)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--output", default=None)
    parser.add_argument("--inp-res", type=float, default=None)
    parser.add_argument("--out-res", type=float, default=None)
    parser.add_argument("--modifier-std-dev", type=float, default=None)
    args = parser.parse_args()

    device = torch.device(args.device)
    print(f"[FreshDrift] Loading checkpoint: {args.checkpoint}")
    ckpt = torch.load(args.checkpoint, map_location=device, weights_only=False)
    ckpt_args = ckpt.get("args", {})
    ckpt_rpu = ckpt.get("rpu_config_spec", {})
    pcm_preset = ckpt_rpu.get("pcm_preset") or ckpt_args.get("pcm_preset")
    if not pcm_preset:
        raise RuntimeError("Fresh+drift eval requires a PCM checkpoint with pcm_preset provenance")

    inp_res = args.inp_res if args.inp_res is not None else ckpt_rpu.get("forward_inp_res", ckpt_args.get("inp_res", 1.0 / 256.0))
    out_res = args.out_res if args.out_res is not None else ckpt_rpu.get("forward_out_res", ckpt_args.get("out_res", 1.0 / 256.0))
    modifier_std_dev = args.modifier_std_dev if args.modifier_std_dev is not None else ckpt_rpu.get("modifier_std_dev", ckpt_args.get("modifier_std_dev", 0.10))
    drift_times = sorted(args.drift_times)

    print(
        "[FreshDrift] Config: "
        f"pcm_preset={pcm_preset}, inp_res={inp_res}, out_res={out_res}, "
        f"modifier_std_dev={modifier_std_dev}, drift_times={drift_times}, "
        f"n_fresh={args.n_fresh}, mc_repeats={args.mc_repeats}"
    )

    loader = get_test_loader(args.batch_size, args.workers, pin=device.type == "cuda")
    if args.output is None:
        args.output = os.path.join(os.path.dirname(args.checkpoint), "fresh_drift_eval.json")

    all_results = []
    first_audit = None
    for time_idx, t in enumerate(drift_times):
        model = build_model(10, inp_res, out_res, modifier_std_dev)
        model.load_state_dict(ckpt["model_state_dict"])

        eval_cfg = make_rpu_config(inp_res, out_res, modifier_std_dev)
        for module in model.modules():
            if hasattr(module, "replace_rpu_config"):
                module.replace_rpu_config(eval_cfg)

        model = model.to(device)
        if t > 0:
            n_drifted = apply_drift(model, t)
        else:
            n_drifted = 0

        audit = tile_audit(model)
        if first_audit is None:
            first_audit = audit
        audit_ok = all(row["modifier_enable_during_test"] for row in audit)
        print(f"[FreshDrift] t={format_time(t)} drifted={n_drifted} tile_audit_all_enabled={audit_ok}")
        if not audit_ok:
            raise RuntimeError("Test-time modifier was not enabled on all analog tiles")

        instance_rows = []
        for i in range(args.n_fresh):
            mc_rows = []
            for j in range(args.mc_repeats):
                seed = args.fresh_seed_base + time_idx * 10000 + i * 100 + j
                acc = evaluate_once(model, loader, device, seed)
                mc_rows.append({"mc": j, "seed": seed, "accuracy": round(acc, 4)})
            accs = [row["accuracy"] for row in mc_rows]
            instance_rows.append({
                "instance": i,
                "seed_base": args.fresh_seed_base + time_idx * 10000 + i * 100,
                "accuracy": round(mean(accs), 4),
                "mc_std": round(stdev(accs), 4) if len(accs) > 1 else 0.0,
                "mc_runs": mc_rows,
            })
        inst_accs = [row["accuracy"] for row in instance_rows]
        result = {
            "t_inference_seconds": t,
            "t_label": format_time(t),
            "n_drifted_layers": n_drifted,
            "mean": round(mean(inst_accs), 4),
            "std": round(stdev(inst_accs), 4) if len(inst_accs) > 1 else 0.0,
            "instances": instance_rows,
        }
        all_results.append(result)
        print(f"[FreshDrift]   -> {result['mean']:.2f}% +/- {result['std']:.2f}%")

        del model
        torch.cuda.empty_cache()

    output = {
        "checkpoint": args.checkpoint,
        "drift_times_seconds": drift_times,
        "n_fresh": args.n_fresh,
        "mc_repeats": args.mc_repeats,
        "fresh_seed_base": args.fresh_seed_base,
        "rpu_config_spec": {
            "forward_inp_res": inp_res,
            "forward_out_res": out_res,
            "modifier_type": "ADD_NORMAL",
            "modifier_std_dev": modifier_std_dev,
            "modifier_enable_during_test": True,
            "pcm_preset": pcm_preset,
        },
        "results": all_results,
        "tile_audit": first_audit or [],
        "tile_audit_all_enabled": all(row["modifier_enable_during_test"] for row in (first_audit or [])),
        "device": str(device),
        "time": datetime.now().isoformat(),
    }
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)
    print(f"[FreshDrift] Saved: {args.output}")


if __name__ == "__main__":
    main()
