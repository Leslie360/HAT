#!/usr/bin/env python3
"""
Training loop for ViT-Small / DeiT-Small on TinyImageNet.
Adapted from train_tinyvit.py for cross-architecture HAT validation.
"""

import argparse
import csv
import json
import os
import random
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from statistics import mean, stdev
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
from PIL import Image

try:
    import timm
except ImportError:
    print("ERROR: timm is required.")
    sys.exit(1)

from analog_layers import AnalogConv2d, AnalogLinear, AnalogLinearConfig, convert_to_hybrid
from amp_utils import amp_enabled_for_device, autocast_context, create_grad_scaler
from tinyvit_hybrid_utils import classify_tinyvit_layer

sys.stdout.reconfigure(line_buffering=True)

# ─────────────────────────────────────────────
# TinyImageNet Dataset
# ─────────────────────────────────────────────

class TinyImageNetDataset(torch.utils.data.Dataset):
    def __init__(self, root: str, split: str = "train", transform=None):
        self.root = Path(root)
        self.split = split
        self.transform = transform
        self.samples = []
        self.class_to_idx = {}
        self._load()

    def _load(self):
        if self.split == "train":
            train_dir = self.root / "train"
            for idx, class_dir in enumerate(sorted(train_dir.iterdir())):
                if not class_dir.is_dir():
                    continue
                self.class_to_idx[class_dir.name] = idx
                images_dir = class_dir / "images"
                for img_path in sorted(images_dir.glob("*.JPEG")):
                    self.samples.append((str(img_path), idx))
        else:
            # val split
            val_dir = self.root / "val" / "images"
            anno_path = self.root / "val" / "val_annotations.txt"
            # Build class list from wnids.txt
            wnids_path = self.root / "wnids.txt"
            with open(wnids_path) as f:
                wnids = [line.strip() for line in f if line.strip()]
            self.class_to_idx = {wnid: i for i, wnid in enumerate(sorted(wnids))}
            with open(anno_path) as f:
                for line in f:
                    parts = line.strip().split("\t")
                    if len(parts) >= 2:
                        img_name, wnid = parts[0], parts[1]
                        img_path = val_dir / img_name
                        if img_path.exists():
                            self.samples.append((str(img_path), self.class_to_idx[wnid]))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, index):
        path, target = self.samples[index]
        img = Image.open(path).convert("RGB")
        if self.transform:
            img = self.transform(img)
        return img, target


# ─────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────

@dataclass
class ViTTinyImageNetConfig:
    name: str
    arch: str = "vit_small_patch16_224"
    hat_type: str = "standard"  # standard | ensemble | proportional
    num_classes: int = 200
    n_states: int = 16
    nl_ltp: float = 1.0
    nl_ltd: float = -1.0
    sigma_c2c: float = 0.05
    sigma_d2d: float = 0.10
    noise_mode: str = "uniform"
    noise_enabled: bool = True
    hat_training: bool = False
    epochs: int = 100
    batch_size: int = 128
    lr: float = 5e-4
    weight_decay: float = 0.05
    warmup_epochs: int = 5
    seed: Optional[int] = None


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)


def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True


def ensure_parent_dir(path: Optional[str]):
    if not path:
        return
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


class RunLogger:
    def __init__(self, path: Optional[str] = None):
        self.path = path
        self._fh = None
        if path:
            ensure_parent_dir(path)
            self._fh = open(path, "w", encoding="utf-8")

    def log(self, message: str = ""):
        stamped = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}" if message else ""
        print(stamped)
        if self._fh is not None:
            self._fh.write(stamped + "\n")
            self._fh.flush()

    def close(self):
        if self._fh is not None:
            self._fh.close()
            self._fh = None


def get_dataloaders(data_root: str, batch_size: int = 128, num_workers: int = 8, seed: Optional[int] = None):
    transform_train = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomResizedCrop(224, scale=(0.7, 1.0)),
        transforms.RandomHorizontalFlip(),
        transforms.TrivialAugmentWide(),
        transforms.ToTensor(),
        transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
    ])
    transform_test = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
    ])

    trainset = TinyImageNetDataset(data_root, split="train", transform=transform_train)
    testset = TinyImageNetDataset(data_root, split="val", transform=transform_test)

    generator = torch.Generator().manual_seed(seed) if seed is not None else None
    loader_kwargs = {
        "batch_size": batch_size,
        "num_workers": num_workers,
        "pin_memory": torch.cuda.is_available(),
        "prefetch_factor": 4,
    }
    if num_workers > 0:
        loader_kwargs["persistent_workers"] = True

    trainloader = torch.utils.data.DataLoader(
        trainset, shuffle=True, generator=generator, **loader_kwargs
    )
    testloader = torch.utils.data.DataLoader(
        testset, shuffle=False, **loader_kwargs
    )
    return trainloader, testloader


def build_model(exp_cfg: ViTTinyImageNetConfig, device: str, pretrained: bool = True, compile_model: bool = False) -> nn.Module:
    model = timm.create_model(exp_cfg.arch, pretrained=pretrained, num_classes=exp_cfg.num_classes)
    if exp_cfg.hat_type != "digital":
        analog_cfg = AnalogLinearConfig(
            n_states=exp_cfg.n_states,
            NL_LTP=exp_cfg.nl_ltp,
            NL_LTD=exp_cfg.nl_ltd,
            sigma_c2c=exp_cfg.sigma_c2c if exp_cfg.hat_training else 0.0,
            sigma_d2d=exp_cfg.sigma_d2d,
            noise_mode=exp_cfg.noise_mode,
            noise_enabled=exp_cfg.hat_training and exp_cfg.noise_enabled,
            restore_weight_scale=True,
        )
        model = convert_to_hybrid(model, config=analog_cfg, verbose=False)
    model = model.to(device)
    if compile_model and hasattr(torch, "compile"):
        try:
            model = torch.compile(model, mode="max-autotune")
        except Exception as e:
            print(f"[WARN] torch.compile failed: {e}, falling back to eager mode")
    return model


def set_noise_for_train(model: nn.Module, exp_cfg: ViTTinyImageNetConfig):
    for module in model.modules():
        if isinstance(module, (AnalogLinear, AnalogConv2d)):
            if exp_cfg.hat_training:
                module.config.noise_enabled = exp_cfg.noise_enabled
                module.config.sigma_c2c = exp_cfg.sigma_c2c
            elif exp_cfg.noise_enabled:
                module.config.noise_enabled = True
                module.config.sigma_c2c = 0.0
            else:
                module.config.noise_enabled = False
                module.config.sigma_c2c = 0.0
            module.config.sigma_d2d = exp_cfg.sigma_d2d
            module.config.noise_mode = exp_cfg.noise_mode
            module.config.NL_LTP = exp_cfg.nl_ltp
            module.config.NL_LTD = exp_cfg.nl_ltd


def set_noise_for_eval(model: nn.Module, exp_cfg: ViTTinyImageNetConfig):
    for module in model.modules():
        if isinstance(module, (AnalogLinear, AnalogConv2d)):
            module.config.noise_enabled = exp_cfg.noise_enabled
            module.config.sigma_c2c = exp_cfg.sigma_c2c
            module.config.sigma_d2d = exp_cfg.sigma_d2d
            module.config.noise_mode = exp_cfg.noise_mode
            module.config.NL_LTP = exp_cfg.nl_ltp
            module.config.NL_LTD = exp_cfg.nl_ltd


def resample_all_d2d_noise(model: nn.Module):
    count = 0
    for m in model.modules():
        if hasattr(m, "resample_d2d_noise") and callable(m.resample_d2d_noise):
            m.resample_d2d_noise()
            count += 1
    return count


def train_one_epoch(model, loader, optimizer, criterion, device, exp_cfg, amp_enabled=False, scaler=None):
    model.train()
    set_noise_for_train(model, exp_cfg)
    running_loss, correct, total = 0.0, 0, 0
    for inputs, targets in loader:
        inputs, targets = inputs.to(device), targets.to(device)
        optimizer.zero_grad(set_to_none=True)
        with autocast_context(device, amp_enabled):
            outputs = model(inputs)
            loss = criterion(outputs, targets)
        if scaler and scaler.is_enabled():
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            loss.backward()
            optimizer.step()
        running_loss += loss.item() * inputs.size(0)
        _, predicted = outputs.max(1)
        correct += predicted.eq(targets).sum().item()
        total += targets.size(0)
    return running_loss / total, 100.0 * correct / total


@torch.no_grad()
def evaluate(model, loader, criterion, device, exp_cfg, amp_enabled=False):
    model.eval()
    set_noise_for_eval(model, exp_cfg)
    running_loss, correct, total = 0.0, 0, 0
    for inputs, targets in loader:
        inputs, targets = inputs.to(device), targets.to(device)
        with autocast_context(device, amp_enabled):
            outputs = model(inputs)
            loss = criterion(outputs, targets)
        running_loss += loss.item() * inputs.size(0)
        _, predicted = outputs.max(1)
        correct += predicted.eq(targets).sum().item()
        total += targets.size(0)
    return running_loss / total, 100.0 * correct / total


def build_training_checkpoint_payload(model, optimizer, scheduler, scaler, exp_cfg, epoch, best_acc, best_epoch, history, amp_enabled, device_name):
    payload = {
        "epoch": epoch,
        "best_epoch": best_epoch,
        "best_acc": best_acc,
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "exp_cfg": asdict(exp_cfg),
        "dataset": "tiny_imagenet",
        "num_classes": exp_cfg.num_classes,
        "history": history,
        "amp_enabled": amp_enabled,
        "seed": exp_cfg.seed,
        "cuda_device_name": device_name,
        "pytorch_version": torch.__version__,
    }
    if scheduler is not None:
        payload["scheduler_state_dict"] = scheduler.state_dict()
    if scaler is not None and hasattr(scaler, "is_enabled") and scaler.is_enabled():
        payload["scaler_state_dict"] = scaler.state_dict()
    return payload


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--arch", choices=["vit_small_patch16_224", "deit_small_patch16_224"], default="vit_small_patch16_224")
    parser.add_argument("--hat-type", choices=["standard", "ensemble", "proportional", "digital"], default="standard")
    parser.add_argument("--seed", type=int, default=123)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--lr", type=float, default=5e-4)
    parser.add_argument("--weight-decay", type=float, default=0.05)
    parser.add_argument("--warmup-epochs", type=int, default=5)
    parser.add_argument("--data-root", type=str, default="./data/tiny-imagenet-200")
    parser.add_argument("--save-dir", type=str, default="checkpoints/_gpt/cross_arch_tinyimagenet")
    parser.add_argument("--num-workers", type=int, default=8)
    parser.add_argument("--amp", action="store_true")
    parser.add_argument("--compile", action="store_true", help="Use torch.compile for acceleration")
    parser.add_argument("--device", type=str, default=None)
    parser.add_argument("--log-path", type=str, default=None)
    parser.add_argument("--pretrained", action="store_true", default=True)
    parser.add_argument("--nl-ltp", type=float, default=1.0)
    parser.add_argument("--nl-ltd", type=float, default=-1.0)
    parser.add_argument("--sigma-c2c", type=float, default=0.05)
    parser.add_argument("--sigma-d2d", type=float, default=0.10)
    args = parser.parse_args()

    set_seed(args.seed)
    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")
    amp_enabled = amp_enabled_for_device(args.amp, device)
    if device.startswith("cuda"):
        device_idx = int(device.split(":")[-1]) if ":" in device else 0
        device_name = torch.cuda.get_device_name(device_idx)
    else:
        device_name = "cpu"

    noise_mode = args.hat_type if args.hat_type == "proportional" else "uniform"
    hat_training = args.hat_type in ("ensemble", "proportional")
    noise_enabled = args.hat_type != "digital"

    exp_cfg = ViTTinyImageNetConfig(
        name=f"{args.arch}_{args.hat_type}_seed{args.seed}",
        arch=args.arch,
        hat_type=args.hat_type,
        num_classes=200,
        nl_ltp=args.nl_ltp,
        nl_ltd=args.nl_ltd,
        sigma_c2c=args.sigma_c2c,
        sigma_d2d=args.sigma_d2d,
        noise_mode=noise_mode,
        noise_enabled=noise_enabled,
        hat_training=hat_training,
        epochs=args.epochs,
        batch_size=args.batch_size,
        lr=args.lr,
        weight_decay=args.weight_decay,
        warmup_epochs=args.warmup_epochs,
        seed=args.seed,
    )

    save_dir = os.path.join(args.save_dir, f"{args.arch}_{args.hat_type}_seed{args.seed}")
    os.makedirs(save_dir, exist_ok=True)
    best_path = os.path.join(save_dir, "best.pt")
    last_path = os.path.join(save_dir, "last.pt")

    log_path = args.log_path or os.path.join(save_dir, "train.log")
    logger = RunLogger(log_path)

    logger.log("=" * 70)
    logger.log(f"Training {args.arch} with HAT={args.hat_type} on TinyImageNet")
    logger.log(f"  seed={args.seed}, batch={args.batch_size}, lr={args.lr}, device={device}")
    logger.log(f"  amp={'on' if amp_enabled else 'off'}, pretrained={args.pretrained}")
    logger.log(f"  noise: C2C={args.sigma_c2c}, D2D={args.sigma_d2d}, mode={noise_mode}")
    logger.log("=" * 70)

    model = build_model(exp_cfg, device, pretrained=args.pretrained, compile_model=args.compile)
    trainloader, testloader = get_dataloaders(
        args.data_root, batch_size=args.batch_size, num_workers=args.num_workers, seed=args.seed
    )
    logger.log(f"Train samples: {len(trainloader.dataset)}, Test samples: {len(testloader.dataset)}")

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)
    scaler = create_grad_scaler(device, amp_enabled)

    # Cosine with warmup
    total_steps = len(trainloader) * args.epochs
    warmup_steps = len(trainloader) * args.warmup_epochs
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)

    history = {"train_loss": [], "train_acc": [], "test_loss": [], "test_acc": [], "lr": []}
    best_acc = 0.0
    best_epoch = -1

    # Early stopping
    early_stop_patience = 10
    epochs_without_improvement = 0

    for epoch in range(args.epochs):
        if exp_cfg.hat_training:
            resample_all_d2d_noise(model)

        current_lr = optimizer.param_groups[0]["lr"]
        train_loss, train_acc = train_one_epoch(
            model, trainloader, optimizer, criterion, device, exp_cfg, amp_enabled, scaler
        )
        test_loss, test_acc = evaluate(model, testloader, criterion, device, exp_cfg, amp_enabled)

        history["train_loss"].append(train_loss)
        history["train_acc"].append(train_acc)
        history["test_loss"].append(test_loss)
        history["test_acc"].append(test_acc)
        history["lr"].append(current_lr)

        improved = test_acc > best_acc
        if improved:
            best_acc = test_acc
            best_epoch = epoch
            epochs_without_improvement = 0
        else:
            epochs_without_improvement += 1

        logger.log(
            f"Epoch {epoch:3d}/{args.epochs}: "
            f"train_loss={train_loss:.4f}, train_acc={train_acc:.2f}%, "
            f"test_acc={test_acc:.2f}% (best={best_acc:.2f}%), lr={current_lr:.6f}"
        )

        payload = build_training_checkpoint_payload(
            model, optimizer, scheduler, scaler, exp_cfg, epoch, best_acc, best_epoch, history, amp_enabled, device_name
        )
        torch.save(payload, last_path)
        if improved:
            torch.save(payload, best_path)

        scheduler.step()

        if epochs_without_improvement >= early_stop_patience:
            logger.log(f"[EARLY STOP] No improvement for {early_stop_patience} epochs.")
            break

    logger.log(f"Finished. Best accuracy: {best_acc:.2f}% at epoch {best_epoch}")
    logger.close()


if __name__ == "__main__":
    main()
