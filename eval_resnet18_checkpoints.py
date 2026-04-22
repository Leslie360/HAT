#!/usr/bin/env python3
"""
Evaluate ResNet-18 checkpoints with the same build/load path used in training.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import torch
import torch.nn as nn

from train_resnet18 import build_model, evaluate, get_dataloaders, load_experiment_config_from_checkpoint

DEFAULT_CHECKPOINTS = (
    ("checkpoints/R1_FP32_baseline_best.pt", "cifar10", 10),
    ("checkpoints/R2_4bit_no_noise_best.pt", "cifar10", 10),
    ("checkpoints/R4_4bit_noise_HAT_best.pt", "cifar10", 10),
    ("checkpoints/resnet18_cifar100/R1_FP32_baseline_best.pt", "cifar100", 100),
    ("checkpoints/resnet18_cifar100/R4_4bit_noise_HAT_best.pt", "cifar100", 100),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument("--device", default=None)
    parser.add_argument("--output", default="")
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    device = torch.device(args.device or ("cuda" if torch.cuda.is_available() else "cpu"))
    print(f"Using device: {device}")

    rows = []
    criterion = nn.CrossEntropyLoss()

    for ckpt_path, dataset, num_classes in DEFAULT_CHECKPOINTS:
        if not os.path.exists(ckpt_path):
            print(f"[-] Skipping missing checkpoint: {ckpt_path}")
            continue

        print(f"\n[+] Evaluating {ckpt_path} on {dataset}")
        ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
        exp_cfg = load_experiment_config_from_checkpoint(ckpt)
        model = build_model(exp_cfg, num_classes=num_classes, device=str(device))
        model.load_state_dict(ckpt["model_state_dict"], strict=True)
        _, test_loader = get_dataloaders(
            dataset,
            batch_size=args.batch_size,
            num_workers=args.num_workers,
        )
        loss, acc = evaluate(model, test_loader, criterion, str(device), exp_cfg)
        expected = float(ckpt.get("best_acc", 0.0))
        delta = float(acc - expected)
        print(f"    expected={expected:.2f}% eval={acc:.2f}% delta={delta:+.2f} loss={loss:.4f}")
        rows.append(
            {
                "checkpoint": ckpt_path,
                "dataset": dataset,
                "expected_best_acc": expected,
                "eval_acc": float(acc),
                "delta": delta,
                "loss": float(loss),
            }
        )

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for row in rows:
        status = "OK" if abs(row["delta"]) < 0.5 else "MISMATCH"
        print(
            f"{status:8s} {row['checkpoint']}: "
            f"{row['eval_acc']:.2f}% vs {row['expected_best_acc']:.2f}%"
        )

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("w", encoding="utf-8") as fh:
            json.dump(rows, fh, indent=2)
        print(f"\nSaved JSON summary to {output_path}")


if __name__ == "__main__":
    main()
