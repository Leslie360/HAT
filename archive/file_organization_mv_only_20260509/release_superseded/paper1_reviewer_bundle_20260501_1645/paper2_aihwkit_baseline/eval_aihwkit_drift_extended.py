#!/usr/bin/env python3
"""
Extended drift evaluation with configurable time points.
Usage: python eval_aihwkit_drift_extended.py --checkpoint ... --drift-times 0 3600 21600 ...
"""

import argparse
import json
import os
import sys
from datetime import datetime

import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms

from aihwkit.nn import AnalogLinear
from aihwkit.simulator.configs import InferenceRPUConfig
from aihwkit.simulator.parameters.inference import WeightModifierType

sys.stdout.reconfigure(line_buffering=True)

PCM_PRESET_REGISTRY = [
    ("aihwkit.simulator.presets", "PCMPresetUnitCell"),
    ("aihwkit.simulator.presets", "PCMPresetDevice"),
    ("aihwkit.simulator.presets.devices", "PCMPresetDevice"),
]


def _resolve_pcm_preset(preferred):
    """Strictly resolve the checkpoint's PCM preset; never fall back across presets."""
    candidates = [item for item in PCM_PRESET_REGISTRY if item[1] == preferred]
    if not candidates:
        raise RuntimeError(
            f"Requested PCM preset '{preferred}' not found in registry. "
            f"Available: {[name for _, name in PCM_PRESET_REGISTRY]}."
        )

    last_err = None
    for module_path, class_name in candidates:
        try:
            import importlib

            mod = importlib.import_module(module_path)
            cls = getattr(mod, class_name)
            print(f"[DriftEvalExt] Resolved PCM preset: {module_path}.{class_name}")
            return cls(), class_name
        except (ImportError, AttributeError, Exception) as e:
            last_err = e
            print(f"[DriftEvalExt] {module_path}.{class_name} failed: {e}")

    raise RuntimeError(
        f"Requested PCM preset '{preferred}' failed to load from all candidate modules. "
        f"Tried: {[f'{m}.{c}' for m, c in candidates]}. Last error: {last_err}"
    )


def make_rpu_config(inp_res=1.0 / 256.0, out_res=1.0 / 256.0, modifier_std_dev=0.10, pcm_preset=None):
    pcm_device, pcm_name = _resolve_pcm_preset(pcm_preset)
    cfg = InferenceRPUConfig()
    cfg.forward.inp_res = inp_res
    cfg.forward.out_res = out_res
    cfg.device = pcm_device
    cfg.modifier.type = WeightModifierType.ADD_NORMAL
    cfg.modifier.std_dev = modifier_std_dev
    cfg.modifier.enable_during_test = False
    return cfg, pcm_name


def replace_linear_with_analog(module, rpu_config):
    for name, child in list(module.named_children()):
        if isinstance(child, nn.Linear):
            analog = AnalogLinear(child.in_features, child.out_features, bias=child.bias is not None, rpu_config=rpu_config)
            with torch.no_grad():
                analog.set_weights(child.weight, child.bias)
            setattr(module, name, analog)
        else:
            replace_linear_with_analog(child, rpu_config)


def build_model(num_classes=10, inp_res=1.0 / 256.0, out_res=1.0 / 256.0, modifier_std_dev=0.10, pcm_preset=None):
    import timm
    model = timm.create_model("tiny_vit_5m_224", num_classes=num_classes, pretrained=False)
    rpu_config, pcm_name = make_rpu_config(
        inp_res=inp_res,
        out_res=out_res,
        modifier_std_dev=modifier_std_dev,
        pcm_preset=pcm_preset,
    )
    replace_linear_with_analog(
        model,
        rpu_config,
    )
    return model, pcm_name


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
    n_drifted = 0
    for module in model.modules():
        if hasattr(module, "drift_analog_weights"):
            module.drift_analog_weights(t_inference=t_inference)
            n_drifted += 1
    return n_drifted


def format_time(t):
    if t == 0:
        return "0s (no drift)"
    elif t < 3600:
        return f"{t:.0f}s"
    elif t < 86400:
        return f"{t/3600:.0f}h"
    else:
        return f"{t/86400:.0f}d"


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
    parser.add_argument("--drift-times", type=float, nargs="+", default=[0.0, 3600.0, 86400.0])
    args = parser.parse_args()

    device = torch.device(args.device)
    print(f"[DriftEvalExt] Loading checkpoint: {args.checkpoint}")

    ckpt = torch.load(args.checkpoint, map_location=device, weights_only=False)
    ckpt_args = ckpt.get("args", {})
    ckpt_rpu = ckpt.get("rpu_config_spec", {})

    pcm_preset = ckpt_rpu.get("pcm_preset") or ckpt_args.get("pcm_preset")
    if not pcm_preset:
        print(f"[DriftEvalExt] WARNING: Non-PCM checkpoint. Skipping.")
        return

    inp_res = args.inp_res if args.inp_res is not None else ckpt_rpu.get("forward_inp_res", ckpt_args.get("inp_res", 1.0 / 256.0))
    out_res = args.out_res if args.out_res is not None else ckpt_rpu.get("forward_out_res", ckpt_args.get("out_res", 1.0 / 256.0))
    modifier_std_dev = args.modifier_std_dev if args.modifier_std_dev is not None else ckpt_rpu.get("modifier_std_dev", ckpt_args.get("modifier_std_dev", 0.10))

    drift_times = sorted(args.drift_times)
    print(f"[DriftEvalExt] Config: inp_res={inp_res}, out_res={out_res}, modifier_std_dev={modifier_std_dev}")
    print(f"[DriftEvalExt] PCM preset: {pcm_preset}")
    print(f"[DriftEvalExt] Drift times: {drift_times}")

    test_loader = get_test_loader(batch_size=args.batch_size, num_workers=args.workers, pin=device.type == "cuda")

    if args.output is None:
        ckpt_dir = os.path.dirname(args.checkpoint)
        args.output = os.path.join(ckpt_dir, "extended_drift_eval.json")

    results = []
    for t in drift_times:
        model, resolved_pcm_preset = build_model(
            num_classes=10,
            inp_res=inp_res,
            out_res=out_res,
            modifier_std_dev=modifier_std_dev,
            pcm_preset=pcm_preset,
        )
        model.load_state_dict(ckpt["model_state_dict"])

        rpu_cfg, _ = make_rpu_config(
            inp_res=inp_res,
            out_res=out_res,
            modifier_std_dev=modifier_std_dev,
            pcm_preset=pcm_preset,
        )
        for module in model.modules():
            if hasattr(module, "replace_rpu_config"):
                module.replace_rpu_config(rpu_cfg)

        model = model.to(device)
        model.eval()

        if t > 0:
            n = apply_drift(model, t)
            print(f"[DriftEvalExt] t={format_time(t)}: drifted {n} layers, evaluating...")
        else:
            print(f"[DriftEvalExt] t={format_time(t)}: baseline, evaluating...")

        acc = evaluate(model, test_loader, device)
        results.append({"t_inference_seconds": t, "t_label": format_time(t), "accuracy": round(acc, 4)})
        print(f"[DriftEvalExt]   -> accuracy: {acc:.2f}%")

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
            "pcm_preset": pcm_preset,
            "resolved_pcm_preset": resolved_pcm_preset,
        },
        "device": str(device),
        "time": datetime.now().isoformat(),
    }
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(output, f, indent=2)
    print(f"[DriftEvalExt] Saved: {args.output}")


if __name__ == "__main__":
    main()
