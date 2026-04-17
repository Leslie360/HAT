#!/usr/bin/env python3
"""
P13: AIHWKIT shared-regime benchmark.

This script is now execution-ready on CPU:
- loads an existing ResNet-18/CIFAR-10 checkpoint
- evaluates the digital baseline on a fixed CIFAR-10 test subset
- converts the same weights into AIHWKIT analog tiles
- evaluates the AIHWKIT model under a matched shared regime

The goal is a reviewer-facing, minimal numeric comparison rather than a
full-scale benchmark sweep.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
import torchvision
import torchvision.models as models
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Subset

try:
    from aihwkit.nn.conversion import convert_to_analog
    from aihwkit.simulator.configs import InferenceRPUConfig
    from aihwkit.simulator.configs.utils import WeightModifierType, WeightNoiseType
    from aihwkit.inference import PCMLikeNoiseModel
except ImportError as exc:  # pragma: no cover - explicit blocker path
    print("ModuleNotFoundError: No module named 'aihwkit'")
    print("This script is execution-blocked until aihwkit is installed.")
    raise SystemExit(1) from exc


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CHECKPOINT = REPO_ROOT / "checkpoints" / "R1_FP32_baseline_best.pt"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "report_md" / "_gpt"
DEFAULT_JSON_OUT = DEFAULT_OUTPUT_DIR / "json_gpt" / "p13_aihwkit_shared_regime_result.json"
DEFAULT_MD_OUT = DEFAULT_OUTPUT_DIR / "P13_aihwkit_shared_regime_result.md"


@dataclass
class BenchmarkResult:
    checkpoint: str
    checkpoint_epoch: int
    checkpoint_best_acc: float
    digital_device: str
    analog_device: str
    subset_size: int
    train_samples: int
    test_samples: int
    batch_size: int
    eval_runs: int
    quant_bits: int
    adc_bits: int
    sigma_c2c: float
    sigma_d2d: float
    digital_acc: float
    analog_mean_acc: float
    analog_std_acc: float
    delta_acc: float
    finetune_epochs: int
    finetune_loss: Optional[float] = None
    finetune_acc: Optional[float] = None
    wall_clock_s: float = 0.0


def seed_everything(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def build_resnet18_cifar10(num_classes: int = 10) -> nn.Module:
    model = models.resnet18(weights=None, num_classes=num_classes)
    model.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
    model.maxpool = nn.Identity()
    return model


def load_checkpoint(model: nn.Module, checkpoint_path: Path) -> Dict:
    ckpt = torch.load(checkpoint_path, map_location="cpu")
    state_dict = ckpt["model_state_dict"] if isinstance(ckpt, dict) and "model_state_dict" in ckpt else ckpt
    missing, unexpected = model.load_state_dict(state_dict, strict=True)
    if missing or unexpected:
        raise RuntimeError(
            f"Checkpoint mismatch for {checkpoint_path}: missing={missing}, unexpected={unexpected}"
        )
    return ckpt if isinstance(ckpt, dict) else {}


def get_rpu_config(quant_bits: int, adc_bits: int, sigma_c2c: float, sigma_d2d: float) -> InferenceRPUConfig:
    rpu = InferenceRPUConfig()
    rpu.mapping.digital_bias = True
    rpu.mapping.weight_scaling_omega = 1.0
    rpu.mapping.learn_out_scaling = True
    rpu.forward.inp_res = 1.0 / (2**adc_bits - 1)
    rpu.forward.out_res = 1.0 / (2**adc_bits - 1)
    rpu.forward.w_noise_type = WeightNoiseType.ADDITIVE_CONSTANT
    rpu.forward.w_noise = sigma_c2c
    rpu.noise_model = PCMLikeNoiseModel(
        prog_noise_scale=sigma_d2d,
        read_noise_scale=sigma_c2c,
        drift_scale=0.0,
    )
    rpu.modifier.type = WeightModifierType.DISCRETIZE
    rpu.modifier.res = 1.0 / (2**quant_bits - 1)
    return rpu


def build_cifar10_loaders(
    data_root: str,
    batch_size: int,
    num_workers: int,
    seed: int,
    train_samples: int,
    test_samples: int,
) -> Tuple[DataLoader, DataLoader]:
    train_transform = transforms.Compose(
        [
            transforms.RandomCrop(32, padding=4),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
        ]
    )
    test_transform = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
        ]
    )

    trainset = torchvision.datasets.CIFAR10(
        root=data_root, train=True, download=True, transform=train_transform
    )
    testset = torchvision.datasets.CIFAR10(
        root=data_root, train=False, download=True, transform=test_transform
    )

    train_subset = trainset
    test_subset = testset
    if 0 < train_samples < len(trainset):
        g = torch.Generator().manual_seed(seed)
        train_idx = torch.randperm(len(trainset), generator=g)[:train_samples].tolist()
        train_subset = Subset(trainset, train_idx)
    if 0 < test_samples < len(testset):
        g = torch.Generator().manual_seed(seed + 1)
        test_idx = torch.randperm(len(testset), generator=g)[:test_samples].tolist()
        test_subset = Subset(testset, test_idx)

    trainloader = DataLoader(
        train_subset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=False,
    )
    testloader = DataLoader(
        test_subset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=False,
    )
    return trainloader, testloader


@torch.no_grad()
def evaluate(model: nn.Module, loader: DataLoader, device: str) -> float:
    model.eval()
    correct = 0
    total = 0
    for inputs, targets in loader:
        inputs = inputs.to(device)
        targets = targets.to(device)
        outputs = model(inputs)
        pred = outputs.argmax(dim=1)
        correct += (pred == targets).sum().item()
        total += targets.size(0)
    return 100.0 * correct / max(total, 1)


def finetune_one_epoch(
    model: nn.Module,
    loader: DataLoader,
    device: str,
    lr: float,
    weight_decay: float,
) -> Tuple[float, float]:
    model.train()
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=lr, momentum=0.9, weight_decay=weight_decay)
    total = 0
    correct = 0
    loss_sum = 0.0

    for inputs, targets in loader:
        inputs = inputs.to(device)
        targets = targets.to(device)
        optimizer.zero_grad(set_to_none=True)
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        loss_sum += loss.item() * inputs.size(0)
        pred = outputs.argmax(dim=1)
        correct += (pred == targets).sum().item()
        total += targets.size(0)

    return loss_sum / max(total, 1), 100.0 * correct / max(total, 1)


def evaluate_mc(model: nn.Module, loader: DataLoader, device: str, runs: int, seed: int) -> Tuple[float, float, List[float]]:
    accs: List[float] = []
    for i in range(runs):
        run_seed = seed + 1000 + i
        run_start = time.time()
        print(
            f"[P13] AIHWKIT eval run {i + 1}/{runs} start "
            f"(seed={run_seed}, device={device})",
            flush=True,
        )
        seed_everything(seed + 1000 + i)
        run_acc = evaluate(model, loader, device)
        accs.append(run_acc)
        print(
            f"[P13] AIHWKIT eval run {i + 1}/{runs} done: "
            f"acc={run_acc:.2f}% elapsed={time.time() - run_start:.1f}s",
            flush=True,
        )
    mean = float(sum(accs) / len(accs))
    std = float((sum((x - mean) ** 2 for x in accs) / len(accs)) ** 0.5)
    return mean, std, accs


def export_report(result: BenchmarkResult, output_dir: Path, json_out: Path, md_out: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.parent.mkdir(parents=True, exist_ok=True)

    with json_out.open("w") as f:
        json.dump(asdict(result), f, indent=2)

    with md_out.open("w") as f:
        f.write("# P13 AIHWKIT Shared-Regime Benchmark\n\n")
        f.write("| Item | Value |\n")
        f.write("|:--|:--|\n")
        f.write(f"| Checkpoint | `{result.checkpoint}` |\n")
        f.write(f"| Checkpoint epoch | `{result.checkpoint_epoch}` |\n")
        f.write(f"| Checkpoint best acc | `{result.checkpoint_best_acc:.2f}%` |\n")
        f.write(f"| Digital device | `{result.digital_device}` |\n")
        f.write(f"| Analog device | `{result.analog_device}` |\n")
        f.write(f"| Digital accuracy | `{result.digital_acc:.2f}%` |\n")
        f.write(f"| AIHWKIT mean accuracy | `{result.analog_mean_acc:.2f}%` |\n")
        f.write(f"| AIHWKIT std | `{result.analog_std_acc:.2f}%` |\n")
        f.write(f"| Delta (analog - digital) | `{result.delta_acc:+.2f}%` |\n")
        f.write(f"| Test subset size | `{result.test_samples}` |\n")
        f.write(f"| Eval runs | `{result.eval_runs}` |\n")
        f.write(f"| Regime | `quant_bits={result.quant_bits}, adc_bits={result.adc_bits}, sigma_c2c={result.sigma_c2c}, sigma_d2d={result.sigma_d2d}` |\n")
        f.write(f"| Wall clock | `{result.wall_clock_s:.1f}s` |\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="P13: AIHWKIT shared-regime benchmark")
    parser.add_argument("--checkpoint", type=str, default=str(DEFAULT_CHECKPOINT))
    parser.add_argument("--device", type=str, default="cpu")
    parser.add_argument("--analog-device", type=str, default=None)
    parser.add_argument("--data-root", type=str, default=str(REPO_ROOT / "data"))
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--train-samples", type=int, default=0)
    parser.add_argument("--test-samples", type=int, default=1024)
    parser.add_argument("--finetune-epochs", type=int, default=0)
    parser.add_argument("--finetune-lr", type=float, default=1e-4)
    parser.add_argument("--finetune-weight-decay", type=float, default=5e-4)
    parser.add_argument("--quant-bits", type=int, default=4)
    parser.add_argument("--adc-bits", type=int, default=8)
    parser.add_argument("--sigma-c2c", type=float, default=0.05)
    parser.add_argument("--sigma-d2d", type=float, default=0.10)
    parser.add_argument("--eval-runs", type=int, default=10)
    parser.add_argument("--output-dir", type=str, default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--json-out", type=str, default=str(DEFAULT_JSON_OUT))
    parser.add_argument("--md-out", type=str, default=str(DEFAULT_MD_OUT))
    args = parser.parse_args()

    device = args.device
    if device == "cuda" and not torch.cuda.is_available():
        print("CUDA requested but unavailable; falling back to CPU.")
        device = "cpu"
    analog_device = args.analog_device or device
    if analog_device == "cuda" and not torch.cuda.is_available():
        print("Analog CUDA requested but unavailable; falling back to CPU.")
        analog_device = "cpu"

    seed_everything(args.seed)
    start = time.time()

    checkpoint_path = Path(args.checkpoint)
    if not checkpoint_path.exists():
        print(f"Missing checkpoint: {checkpoint_path}")
        print("Use the existing R1 baseline checkpoint or point --checkpoint at a valid .pt file.")
        return 1

    print(f"[P13] digital_device={device}")
    print(f"[P13] analog_device={analog_device}")
    print(f"[P13] checkpoint={checkpoint_path}")
    print(
        f"[P13] shared regime: quant_bits={args.quant_bits}, adc_bits={args.adc_bits}, "
        f"sigma_c2c={args.sigma_c2c}, sigma_d2d={args.sigma_d2d}"
    )

    # Data
    trainloader, testloader = build_cifar10_loaders(
        data_root=args.data_root,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        seed=args.seed,
        train_samples=args.train_samples,
        test_samples=args.test_samples,
    )

    # Digital baseline
    digital_model = build_resnet18_cifar10()
    ckpt = load_checkpoint(digital_model, checkpoint_path)
    checkpoint_epoch = int(ckpt.get("epoch", -1)) if isinstance(ckpt, dict) else -1
    checkpoint_best_acc = float(ckpt.get("best_acc", float("nan"))) if isinstance(ckpt, dict) else float("nan")
    digital_model = digital_model.to(device)
    digital_acc = evaluate(digital_model, testloader, device)
    print(f"[P13] digital subset accuracy: {digital_acc:.2f}%")

    finetune_loss = None
    finetune_acc = None
    if args.finetune_epochs > 0 and args.train_samples > 0:
        for epoch in range(args.finetune_epochs):
            finetune_loss, finetune_acc = finetune_one_epoch(
                digital_model,
                trainloader,
                device=device,
                lr=args.finetune_lr,
                weight_decay=args.finetune_weight_decay,
            )
            print(
                f"[P13] finetune epoch {epoch}: loss={finetune_loss:.4f}, acc={finetune_acc:.2f}%"
            )

    # AIHWKIT analog evaluation
    rpu = get_rpu_config(
        quant_bits=args.quant_bits,
        adc_bits=args.adc_bits,
        sigma_c2c=args.sigma_c2c,
        sigma_d2d=args.sigma_d2d,
    )
    analog_model = convert_to_analog(digital_model.cpu(), rpu, inplace=False, verbose=False)
    try:
        analog_model = analog_model.to(analog_device)
    except Exception as exc:
        if analog_device == "cuda" and "CUDA support" in str(exc):
            print("[P13] AIHWKIT CUDA tiles unavailable; retrying analog model on CPU.")
            analog_device = "cpu"
            analog_model = analog_model.to(analog_device)
        else:
            raise
    analog_mean, analog_std, analog_runs = evaluate_mc(
        analog_model, testloader, device=analog_device, runs=args.eval_runs, seed=args.seed
    )
    print(
        f"[P13] AIHWKIT subset accuracy: {analog_mean:.2f}% ± {analog_std:.2f}% "
        f"over {args.eval_runs} runs"
    )

    result = BenchmarkResult(
        checkpoint=str(checkpoint_path),
        checkpoint_epoch=checkpoint_epoch,
        checkpoint_best_acc=checkpoint_best_acc,
        digital_device=device,
        analog_device=analog_device,
        subset_size=len(testloader.dataset),
        train_samples=args.train_samples,
        test_samples=args.test_samples,
        batch_size=args.batch_size,
        eval_runs=args.eval_runs,
        quant_bits=args.quant_bits,
        adc_bits=args.adc_bits,
        sigma_c2c=args.sigma_c2c,
        sigma_d2d=args.sigma_d2d,
        digital_acc=digital_acc,
        analog_mean_acc=analog_mean,
        analog_std_acc=analog_std,
        delta_acc=analog_mean - digital_acc,
        finetune_epochs=args.finetune_epochs,
        finetune_loss=finetune_loss,
        finetune_acc=finetune_acc,
        wall_clock_s=time.time() - start,
    )

    export_report(result, Path(args.output_dir), Path(args.json_out), Path(args.md_out))
    print(f"[P13] exported JSON: {args.json_out}")
    print(f"[P13] exported MD:   {args.md_out}")
    print(
        f"[P13] summary: digital={result.digital_acc:.2f}%, "
        f"aihwkit={result.analog_mean_acc:.2f}±{result.analog_std_acc:.2f}%, "
        f"delta={result.delta_acc:+.2f}%"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
