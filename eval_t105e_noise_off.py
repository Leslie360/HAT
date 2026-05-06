#!/usr/bin/env python3
"""T105-E Ablation: evaluate a proportional checkpoint with noise disabled.
This reveals the "regularization-only" benefit by removing eval-time noise."""
import argparse
import json
import torch
from pathlib import Path

from train_vit_tinyimagenet import (
    ViTTinyImageNetConfig,
    build_model,
    get_dataloaders,
    evaluate,
)
from analog_layers import AnalogLinear, AnalogConv2d
from amp_utils import amp_enabled_for_device


def evaluate_noise_off(checkpoint_path, device, data_root="../data/tiny-imagenet-200", batch_size=None):
    ckpt = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    exp_cfg_dict = ckpt.get("exp_cfg", {})
    exp_cfg = ViTTinyImageNetConfig(**exp_cfg_dict)

    _batch_size = batch_size if batch_size is not None else exp_cfg.batch_size
    model = build_model(exp_cfg, device, pretrained=False)
    model.load_state_dict(ckpt["model_state_dict"], strict=False)

    # Disable all analog noise
    count = 0
    for module in model.modules():
        if isinstance(module, (AnalogLinear, AnalogConv2d)):
            module.config.noise_enabled = False
            module.config.sigma_c2c = 0.0
            module.config.sigma_d2d = 0.0
            count += 1
    print(f"[T105-E] Disabled noise on {count} analog layers")

    _, testloader = get_dataloaders(
        data_root=data_root,
        batch_size=_batch_size,
        num_workers=4,
        seed=None,
    )

    amp_enabled = ckpt.get("amp_enabled", False)
    criterion = torch.nn.CrossEntropyLoss()

    loss, acc = evaluate(model, testloader, criterion, device, exp_cfg, amp_enabled)
    print(f"[T105-E] Noise-off eval: loss={loss:.4f}, acc={acc:.2f}%")

    return {
        "checkpoint_path": str(checkpoint_path),
        "exp_id": exp_cfg.name,
        "mode": "noise_off",
        "test_loss": float(loss),
        "test_acc": float(acc),
        "analog_layers_disabled": count,
        "source_acc": ckpt.get("best_acc"),
        "checkpoint_epoch": ckpt.get("epoch"),
        "checkpoint_best_epoch": ckpt.get("best_epoch"),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--device", default=None)
    parser.add_argument("--data-root", default="../data/tiny-imagenet-200")
    parser.add_argument("--batch-size", type=int, default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")
    result = evaluate_noise_off(args.checkpoint, device, args.data_root, args.batch_size)

    output_path = args.output or f"report_md/_gpt/json_gpt/{Path(args.checkpoint).parent.name}_noise_off.json"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Saved to {output_path}")


if __name__ == "__main__":
    main()
