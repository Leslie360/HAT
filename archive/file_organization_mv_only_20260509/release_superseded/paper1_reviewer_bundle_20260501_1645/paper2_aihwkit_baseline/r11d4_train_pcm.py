#!/usr/bin/env python3
"""
R11D-4: AIHWKit head-to-head with PCM device model.
Replicates R10E recipe exactly except device model: PCMPresetUnitCell.
"""

import argparse
import hashlib
import json
import os
import random
import subprocess
import sys
import time
import traceback
from datetime import datetime

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms

from aihwkit.nn import AnalogLinear
from aihwkit.optim import AnalogSGD
from aihwkit.simulator.configs import InferenceRPUConfig
from aihwkit.simulator.parameters.inference import WeightModifierParameter, WeightModifierType

sys.stdout.reconfigure(line_buffering=True)

DATASET_STATS = {
    "cifar10": {
        "num_classes": 10,
        "mean": (0.4914, 0.4822, 0.4465),
        "std": (0.2023, 0.1994, 0.2010),
        "dataset_cls": torchvision.datasets.CIFAR10,
    },
}

PCM_PRESET_REGISTRY = [
    ("aihwkit.simulator.presets", "PCMPresetUnitCell"),
    ("aihwkit.simulator.presets", "PCMPresetDevice"),
    ("aihwkit.simulator.presets.devices", "PCMPresetDevice"),
]


def _resolve_pcm_preset():
    """Try PCM presets in order. Returns (device_instance, name_string) or raises."""
    last_err = None
    for module_path, class_name in PCM_PRESET_REGISTRY:
        try:
            import importlib
            mod = importlib.import_module(module_path)
            cls = getattr(mod, class_name)
            instance = cls()
            print(f"[PCM] Resolved preset: {module_path}.{class_name}")
            return instance, class_name
        except (ImportError, AttributeError, Exception) as e:
            last_err = e
            print(f"[PCM] {module_path}.{class_name} failed: {e}")
    raise ImportError(
        f"No usable PCM device preset found. Tried: "
        f"{[f'{m}.{c}' for m, c in PCM_PRESET_REGISTRY]}. "
        f"Last error: {last_err}"
    )


def get_dataloaders(dataset_name="cifar10", batch_size=64, num_workers=2, pin=False):
    stats = DATASET_STATS[dataset_name]
    transform_train = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(stats["mean"], stats["std"]),
    ])
    transform_test = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(stats["mean"], stats["std"]),
    ])
    train_ds = stats["dataset_cls"](root="./data", train=True, download=True, transform=transform_train)
    test_ds = stats["dataset_cls"](root="./data", train=False, download=True, transform=transform_test)
    train_loader = torch.utils.data.DataLoader(
        train_ds, batch_size=batch_size, shuffle=True,
        num_workers=num_workers, pin_memory=pin
    )
    test_loader = torch.utils.data.DataLoader(
        test_ds, batch_size=batch_size, shuffle=False,
        num_workers=num_workers, pin_memory=pin
    )
    return train_loader, test_loader, stats["num_classes"]


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_commit_hash():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL, text=True,
        ).strip()
    except Exception:
        return "unknown"


def make_rpu_config(inp_res=1.0 / 256.0, out_res=1.0 / 256.0, modifier_std_dev=0.10):
    pcm_device, pcm_name = _resolve_pcm_preset()
    cfg = InferenceRPUConfig()
    cfg.forward.inp_res = inp_res
    cfg.forward.out_res = out_res
    cfg.device = pcm_device
    cfg.modifier.type = WeightModifierType.ADD_NORMAL
    cfg.modifier.std_dev = modifier_std_dev
    cfg.modifier.enable_during_test = False
    return cfg, pcm_name


def replace_linear_with_analog(module, rpu_config, parent_name=""):
    for name, child in list(module.named_children()):
        full_name = f"{parent_name}.{name}" if parent_name else name
        if isinstance(child, nn.Linear):
            analog_layer = AnalogLinear(
                in_features=child.in_features,
                out_features=child.out_features,
                bias=child.bias is not None,
                rpu_config=rpu_config,
            )
            with torch.no_grad():
                analog_layer.set_weights(child.weight, child.bias)
            setattr(module, name, analog_layer)
        else:
            replace_linear_with_analog(child, rpu_config, full_name)


def build_model(num_classes=10, inp_res=1.0 / 256.0, out_res=1.0 / 256.0, modifier_std_dev=0.10):
    import timm
    model = timm.create_model("tiny_vit_5m_224", num_classes=num_classes, pretrained=False)
    rpu_config, pcm_name = make_rpu_config(
        inp_res=inp_res,
        out_res=out_res,
        modifier_std_dev=modifier_std_dev,
    )
    replace_linear_with_analog(model, rpu_config)
    return model, rpu_config, pcm_name


def train_epoch(model, loader, optimizer, criterion, device):
    model.train()
    total_loss = 0.0
    correct = 0
    total = 0
    for inputs, targets in loader:
        inputs, targets = inputs.to(device), targets.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * inputs.size(0)
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()
    return total_loss / total, 100.0 * correct / total


@torch.no_grad()
def evaluate(model, loader, criterion, device):
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0
    for inputs, targets in loader:
        inputs, targets = inputs.to(device), targets.to(device)
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        total_loss += loss.item() * inputs.size(0)
        _, predicted = outputs.max(1)
        total += targets.size(0)
        correct += predicted.eq(targets).sum().item()
    return total_loss / total, 100.0 * correct / total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--lr", type=float, default=5e-4)
    parser.add_argument("--wd", type=float, default=0.05)
    parser.add_argument("--momentum", type=float, default=0.0)
    parser.add_argument("--workers", type=int, default=0)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--save-dir", default="paper2_aihwkit_baseline/checkpoints/r11d_4_pcm_fixed")
    parser.add_argument("--log-interval", type=int, default=10)
    parser.add_argument("--inp-res", type=float, default=1.0 / 256.0)
    parser.add_argument("--out-res", type=float, default=1.0 / 256.0)
    parser.add_argument("--modifier-std-dev", type=float, default=0.10)
    parser.add_argument("--early-stop-patience", type=int, default=0)
    parser.add_argument("--early-stop-min-delta", type=float, default=0.0)
    parser.add_argument("--run-id", default="r11d_4_pcm_fixed")
    args = parser.parse_args()

    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)

    os.makedirs(args.save_dir, exist_ok=True)
    device = torch.device(args.device)

    print(f"=== R11D-4 AIHWKit PCM Device Model ===")
    print(f"Device: {device}")
    print(f"PyTorch: {torch.__version__}")
    print(
        "Config: "
        f"run_id={args.run_id}, epochs={args.epochs}, bs={args.batch_size}, lr={args.lr}, "
        f"inp_res={args.inp_res}, out_res={args.out_res}, modifier_std_dev={args.modifier_std_dev}"
    )

    # --- Resolve PCM preset early so we fail fast ---
    print("[PCM] Resolving device preset...")
    try:
        _rpu_config, pcm_name = make_rpu_config(
            inp_res=args.inp_res,
            out_res=args.out_res,
            modifier_std_dev=args.modifier_std_dev,
        )
    except ImportError as e:
        print(f"[FATAL] {e}", file=sys.stderr)
        sys.exit(2)

    train_loader, test_loader, num_classes = get_dataloaders(
        batch_size=args.batch_size, num_workers=args.workers,
        pin=device.type == "cuda"
    )

    # --- OOM wrapper: try batch_size, fall back to batch_size//2 ---
    batch_size_tried = args.batch_size
    try:
        model, rpu_config, pcm_name = build_model(
            num_classes=num_classes,
            inp_res=args.inp_res,
            out_res=args.out_res,
            modifier_std_dev=args.modifier_std_dev,
        )
        model = model.to(device)
    except RuntimeError as e:
        if "out of memory" in str(e).lower() and args.batch_size > 32:
            print(f"[OOM] batch_size={args.batch_size} OOM. Retrying with batch_size=32")
            torch.cuda.empty_cache()
            args.batch_size = 32
            batch_size_tried = 32
            train_loader, test_loader, num_classes = get_dataloaders(
                batch_size=args.batch_size, num_workers=args.workers,
                pin=device.type == "cuda"
            )
            model, rpu_config, pcm_name = build_model(
                num_classes=num_classes,
                inp_res=args.inp_res,
                out_res=args.out_res,
                modifier_std_dev=args.modifier_std_dev,
            )
            model = model.to(device)
        else:
            raise

    n_analog = sum(1 for _ in model.modules() if isinstance(_, AnalogLinear))
    print(f"AnalogLinear layers: {n_analog}")
    print(f"PCM preset: {pcm_name}")
    print(f"Dataset: CIFAR-10, {len(train_loader.dataset)} train, {len(test_loader.dataset)} test")

    criterion = nn.CrossEntropyLoss()
    # Use AnalogSGD to trigger PCM pulse-update physics via post_update_step()
    optimizer = AnalogSGD(model.parameters(), lr=args.lr, momentum=args.momentum, weight_decay=args.wd)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs, eta_min=1e-6)

    best_acc = 0.0
    best_epoch = -1
    history = []
    start_time = time.time()
    rpu_config_spec = {
        "forward_inp_res": args.inp_res,
        "forward_out_res": args.out_res,
        "modifier_type": "ADD_NORMAL",
        "modifier_std_dev": args.modifier_std_dev,
        "modifier_enable_during_test": False,
        "pcm_preset": pcm_name,
    }
    provenance = {
        "run_id": args.run_id,
        "commit_hash": git_commit_hash(),
        "code_sha256": sha256_file(__file__),
        "cuda_device_name": torch.cuda.get_device_name(device) if device.type == "cuda" else "cpu",
        "pytorch_version": torch.__version__,
        "exp_cfg": vars(args),
        "rpu_config_spec": rpu_config_spec,
        "pcm_preset_used": pcm_name,
        "optimizer": "AnalogSGD",
        "optimizer_change_note": (
            "Replaced AdamW with AnalogSGD to trigger post_update_step "
            "for PCM pulse-update physics during training."
        ),
    }

    for epoch in range(args.epochs):
        t0 = time.time()
        train_loss, train_acc = train_epoch(model, train_loader, optimizer, criterion, device)
        test_loss, test_acc = evaluate(model, test_loader, criterion, device)
        scheduler.step()
        epoch_time = time.time() - t0

        # --- Divergence detection (NaN within first 5 epochs) ---
        if torch.isnan(torch.tensor(train_loss)) or torch.isnan(torch.tensor(test_loss)):
            if epoch < 5:
                diag = {
                    "epoch": epoch + 1,
                    "train_loss": float(train_loss) if not isinstance(train_loss, float) else train_loss,
                    "test_loss": float(test_loss) if not isinstance(test_loss, float) else test_loss,
                    "train_acc": float(train_acc),
                    "test_acc": float(test_acc),
                    "grad_norms": [],
                }
                for p in model.parameters():
                    if p.grad is not None:
                        diag["grad_norms"].append(p.grad.norm().item())
                diag_path = os.path.join(args.save_dir, "divergence_diagnostics.json")
                with open(diag_path, "w") as f:
                    json.dump(diag, f, indent=2)
                print(f"[DIVERGENCE] NaN detected at epoch {epoch+1}. Diagnostics dumped to {diag_path}")
                sys.exit(3)
            else:
                print(f"[WARN] NaN detected at epoch {epoch+1} (>5), continuing...")

        history.append({
            "epoch": epoch + 1,
            "train_loss": round(train_loss, 4),
            "train_acc": round(train_acc, 4),
            "test_loss": round(test_loss, 4),
            "test_acc": round(test_acc, 4),
            "lr": round(optimizer.param_groups[0]["lr"], 6),
            "epoch_time_sec": round(epoch_time, 1),
        })

        if test_acc > best_acc + args.early_stop_min_delta:
            best_acc = test_acc
            best_epoch = epoch
            ckpt = os.path.join(args.save_dir, "best.pt")
            torch.save({
                "epoch": epoch,
                "model_state_dict": model.state_dict(),
                "test_acc": test_acc,
                "args": vars(args),
                "rpu_config_spec": rpu_config_spec,
                "provenance": provenance,
            }, ckpt)

        if (epoch + 1) % args.log_interval == 0 or epoch == 0 or epoch == args.epochs - 1:
            elapsed = time.time() - start_time
            eta = elapsed / (epoch + 1) * (args.epochs - epoch - 1) if epoch > 0 else 0
            print(f"Epoch {epoch+1:3d}/{args.epochs} | Train {train_acc:.2f}% | Test {test_acc:.2f}% | Best {best_acc:.2f}% | {epoch_time:.1f}s/epoch | ETA {eta/3600:.1f}h")

        if args.early_stop_patience > 0 and best_epoch >= 0:
            epochs_without_improvement = epoch - best_epoch
            if epochs_without_improvement >= args.early_stop_patience:
                print(
                    f"Early stop at epoch {epoch+1}: no test_acc improvement for "
                    f"{args.early_stop_patience} epochs."
                )
                break

    total_elapsed = time.time() - start_time
    print(f"\n=== Complete ===")
    print(f"Best test accuracy: {best_acc:.2f}%")
    print(f"Total time: {total_elapsed/3600:.2f}h")
    print(f"Finish: {datetime.now().isoformat()}")

    # Save last.pt
    last_ckpt = os.path.join(args.save_dir, "last.pt")
    torch.save({
        "epoch": epoch,
        "model_state_dict": model.state_dict(),
        "test_acc": test_acc,
        "args": vars(args),
        "rpu_config_spec": rpu_config_spec,
        "provenance": provenance,
    }, last_ckpt)

    hist_path = os.path.join(args.save_dir, "training_history.json")
    oom_info = {"oom_retry_batch_size": batch_size_tried} if batch_size_tried != args.batch_size else {}
    with open(hist_path, "w") as f:
        json.dump({
            "best_acc": best_acc,
            "total_seconds": total_elapsed,
            "history": history,
            "args": vars(args),
            "aihwkit_version": "1.1.0",
            "rpu_config": str(rpu_config),
            "rpu_config_spec": rpu_config_spec,
            "provenance": provenance,
            "pcm_preset_used": pcm_name,
            **oom_info,
            "device": str(device),
            "finish_time": datetime.now().isoformat(),
        }, f, indent=2)
    print(f"Saved: {hist_path}")


if __name__ == "__main__":
    main()
