#!/usr/bin/env python3
"""
Phase A2.2 / Task 21: ConvNeXt-Tiny pipeline validation across CIFAR-style datasets.
"""

import argparse
import csv
import json
import math
import os
import random
import re
import sys
import time
import warnings
from copy import deepcopy
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import torchvision.models as models

sys.stdout.reconfigure(line_buffering=True)

from analog_layers import (
    AnalogLinear, AnalogLinearConfig, AnalogConv2d,
    convert_resnet_to_analog,
)
from amp_utils import amp_enabled_for_device, autocast_context, create_grad_scaler
from report_asset_paths import asset_path

DATASET_STATS = {
    "cifar10": {"num_classes": 10, "mean": (0.4914, 0.4822, 0.4465), "std": (0.2023, 0.1994, 0.2010), "image_size": 32, "dataset_cls": torchvision.datasets.CIFAR10},
    "cifar100": {"num_classes": 100, "mean": (0.5071, 0.4867, 0.4408), "std": (0.2675, 0.2565, 0.2761), "image_size": 32, "dataset_cls": torchvision.datasets.CIFAR100},
    "flowers102": {"num_classes": 102, "mean": (0.485, 0.456, 0.406), "std": (0.229, 0.224, 0.225), "image_size": 224, "dataset_cls": torchvision.datasets.Flowers102},
}

@dataclass
class ExperimentConfig:
    name: str
    n_states: int = 16
    nl_ltp: float = 1.0
    nl_ltd: float = -1.0
    sigma_c2c: float = 0.0
    sigma_d2d: float = 0.0
    noise_mode: str = "uniform"
    noise_enabled: bool = False
    use_analog: bool = False
    hat_training: bool = False
    epochs: int = 200
    lr: float = 4e-3
    weight_decay: float = 0.05
    inl_table: Optional[List[float]] = None
    batch_size: int = 128

def get_experiment_configs(epochs: int = 200) -> dict:
    return {
        'C1': ExperimentConfig(name='C1_FP32_baseline', use_analog=False, epochs=epochs),
        'C2': ExperimentConfig(name='C2_4bit_no_noise', n_states=16, use_analog=True, noise_enabled=False, epochs=epochs),
        'C3': ExperimentConfig(name='C3_4bit_noise_standard', n_states=16, sigma_c2c=0.05, sigma_d2d=0.10, noise_enabled=True, use_analog=True, hat_training=False, epochs=epochs),
        'C4': ExperimentConfig(name='C4_4bit_noise_HAT', n_states=16, sigma_c2c=0.05, sigma_d2d=0.10, noise_enabled=True, use_analog=True, hat_training=True, epochs=epochs),
    }

def set_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

def build_model(exp_cfg: ExperimentConfig, num_classes: int, image_size: int, device: str = 'cpu'):
    model = models.convnext_tiny(weights=None, num_classes=num_classes)
    if image_size <= 64: model.features[0][0] = nn.Conv2d(3, 96, kernel_size=4, stride=2, padding=1)
    if exp_cfg.use_analog:
        analog_cfg = AnalogLinearConfig(
            n_states=exp_cfg.n_states, NL_LTP=exp_cfg.nl_ltp, NL_LTD=exp_cfg.nl_ltd,
            sigma_c2c=exp_cfg.sigma_c2c if exp_cfg.hat_training else 0.0, sigma_d2d=exp_cfg.sigma_d2d,
            noise_mode=exp_cfg.noise_mode, noise_enabled=exp_cfg.hat_training and exp_cfg.noise_enabled,
            inl_table=torch.tensor(exp_cfg.inl_table, dtype=torch.float32) if exp_cfg.inl_table is not None else None,
        )
        model = convert_resnet_to_analog(model, config=analog_cfg, skip_first_conv=False, verbose=False)
    return model.to(device)

def get_dataloaders(dataset='cifar10', batch_size=128, num_workers=4, data_root='./data'):
    stats = DATASET_STATS[dataset]
    img_sz = stats["image_size"]
    tf_train = transforms.Compose([transforms.Resize((img_sz, img_sz)), transforms.RandomHorizontalFlip(), transforms.ToTensor(), transforms.Normalize(stats["mean"], stats["std"])])
    tf_test = transforms.Compose([transforms.Resize((img_sz, img_sz)), transforms.ToTensor(), transforms.Normalize(stats["mean"], stats["std"])])
    if dataset == "flowers102":
        trainset = torchvision.datasets.Flowers102(root=data_root, split="train", download=True, transform=tf_train)
        testset = torchvision.datasets.Flowers102(root=data_root, split="test", download=True, transform=tf_test)
    else:
        trainset = stats["dataset_cls"](root=data_root, train=True, download=True, transform=tf_train)
        testset = stats["dataset_cls"](root=data_root, train=False, download=True, transform=tf_test)
    return torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True, num_workers=num_workers), torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=False, num_workers=num_workers)

def train_one_epoch(model, loader, optimizer, criterion, device, exp_cfg, amp_enabled=False, scaler=None):
    model.train()
    r_loss, correct, total = 0.0, 0, 0
    for inputs, targets in loader:
        inputs, targets = inputs.to(device), targets.to(device)
        optimizer.zero_grad(set_to_none=True)
        with autocast_context(device, amp_enabled):
            outputs = model(inputs)
            loss = criterion(outputs, targets)
        if scaler: scaler.scale(loss).backward(); scaler.step(optimizer); scaler.update()
        else: loss.backward(); optimizer.step()
        r_loss += loss.item() * inputs.size(0); _, pred = outputs.max(1); correct += pred.eq(targets).sum().item(); total += targets.size(0)
    return r_loss / total, 100.0 * correct / total

@torch.no_grad()
def evaluate(model, loader, criterion, device, exp_cfg, amp_enabled=False):
    model.eval()
    r_loss, correct, total = 0.0, 0, 0
    for inputs, targets in loader:
        inputs, targets = inputs.to(device), targets.to(device)
        with autocast_context(device, amp_enabled):
            outputs = model(inputs)
            loss = criterion(outputs, targets)
        r_loss += loss.item() * inputs.size(0); _, pred = outputs.max(1); correct += pred.eq(targets).sum().item(); total += targets.size(0)
    return r_loss / total, 100.0 * correct / total


def init_training_history() -> dict:
    return {"train_loss": [], "train_acc": [], "test_loss": [], "test_acc": [], "lr": []}


def normalize_training_history(history: Optional[dict]) -> dict:
    normalized = init_training_history()
    if not isinstance(history, dict):
        return normalized
    for key in normalized:
        value = history.get(key, [])
        normalized[key] = list(value) if isinstance(value, list) else []
    return normalized


def get_training_checkpoint_paths(exp_cfg: ExperimentConfig, save_dir: str) -> Tuple[str, str]:
    best_checkpoint_path = os.path.join(save_dir, f"{exp_cfg.name}_best.pt")
    last_checkpoint_path = os.path.join(save_dir, f"{exp_cfg.name}_last.pt")
    return best_checkpoint_path, last_checkpoint_path


def build_training_checkpoint_payload(model: nn.Module, optimizer, scheduler,
                                      exp_cfg: ExperimentConfig,
                                      dataset: str, num_classes: int, epoch: int, best_acc: float,
                                      best_epoch: int, history: dict, amp_enabled: bool,
                                      seed: Optional[int]) -> dict:
    payload = {
        "epoch": epoch,
        "best_epoch": best_epoch,
        "best_acc": best_acc,
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "exp_cfg": asdict(exp_cfg),
        "dataset": dataset,
        "num_classes": num_classes,
        "history": normalize_training_history(history),
        "amp_enabled": amp_enabled,
        "seed": seed,
    }
    if scheduler is not None:
        payload["scheduler_state_dict"] = scheduler.state_dict()
    return payload


def checkpoint_is_compatible(ckpt: dict, dataset: str, num_classes: int) -> Tuple[bool, str]:
    ckpt_dataset = ckpt.get("dataset")
    if ckpt_dataset is not None and ckpt_dataset != dataset:
        return False, f"dataset mismatch (checkpoint={ckpt_dataset}, target={dataset})"
    ckpt_num_classes = ckpt.get("num_classes")
    if ckpt_num_classes is not None and int(ckpt_num_classes) != int(num_classes):
        return False, f"num_classes mismatch (checkpoint={ckpt_num_classes}, target={num_classes})"
    return True, ""


def maybe_resume_experiment(model: nn.Module, optimizer, scheduler, exp_cfg: ExperimentConfig,
                            save_dir: str, device: str, dataset: str, num_classes: int,
                            resume_existing: bool = False):
    best_checkpoint_path, last_checkpoint_path = get_training_checkpoint_paths(exp_cfg, save_dir)
    start_epoch = 0
    best_acc = 0.0
    best_epoch = -1
    history = init_training_history()
    resume_checkpoint_path = None

    if resume_existing:
        if os.path.exists(last_checkpoint_path):
            resume_checkpoint_path = last_checkpoint_path
        elif os.path.exists(best_checkpoint_path):
            resume_checkpoint_path = best_checkpoint_path

    if resume_checkpoint_path is None:
        return start_epoch, best_acc, best_epoch, best_checkpoint_path, last_checkpoint_path, history, None

    ckpt = torch.load(resume_checkpoint_path, map_location=device, weights_only=False)
    compatible, reason = checkpoint_is_compatible(ckpt, dataset=dataset, num_classes=num_classes)
    if not compatible:
        print(f"Skipping resume from {resume_checkpoint_path}: {reason}")
        return start_epoch, best_acc, best_epoch, best_checkpoint_path, last_checkpoint_path, history, None

    try:
        model.load_state_dict(ckpt["model_state_dict"])
    except RuntimeError as exc:
        print(f"Skipping resume from {resume_checkpoint_path}: incompatible state_dict ({exc})")
        return start_epoch, best_acc, best_epoch, best_checkpoint_path, last_checkpoint_path, history, None

    optimizer_state = ckpt.get("optimizer_state_dict")
    if optimizer_state is not None:
        optimizer.load_state_dict(optimizer_state)
    scheduler_state = ckpt.get("scheduler_state_dict")
    if scheduler_state is not None and scheduler is not None:
        scheduler.load_state_dict(scheduler_state)

    start_epoch = int(ckpt.get("epoch", -1)) + 1
    best_acc = float(ckpt.get("best_acc", 0.0))
    best_epoch = int(ckpt.get("best_epoch", ckpt.get("epoch", -1)))
    history = normalize_training_history(ckpt.get("history"))
    return start_epoch, best_acc, best_epoch, best_checkpoint_path, last_checkpoint_path, history, resume_checkpoint_path


def resolve_checkpoint_path(exp_cfg: ExperimentConfig, explicit_checkpoint: Optional[str],
                            checkpoint_dir: str) -> str:
    if explicit_checkpoint:
        return explicit_checkpoint
    best_checkpoint_path, _ = get_training_checkpoint_paths(exp_cfg, checkpoint_dir)
    if not os.path.exists(best_checkpoint_path):
        raise FileNotFoundError(f"Checkpoint not found: {best_checkpoint_path}")
    return best_checkpoint_path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["train", "eval"], default="train")
    parser.add_argument("--experiments", nargs='+', default=['C1'])
    parser.add_argument("--epochs", type=int, default=200)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--dataset", default="cifar10")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--amp", action="store_true")
    parser.add_argument("--checkpoint", type=str, default=None)
    parser.add_argument("--checkpoint-dir", type=str, default=None)
    parser.add_argument("--save-dir", type=str, default="checkpoints")
    parser.add_argument("--data-root", type=str, default="./data")
    parser.add_argument("--num-workers", type=int, default=4)
    parser.add_argument("--eval-runs", type=int, default=1)
    parser.add_argument("--resume-existing", action="store_true")
    parser.add_argument(
        "--noise-mode",
        choices=["uniform", "proportional"],
        default=None,
        help="Override the experiment's configured noise_mode."
    )
    args = parser.parse_args()
    if args.seed is not None:
        set_seed(args.seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    configs = get_experiment_configs(epochs=args.epochs)
    criterion = nn.CrossEntropyLoss()
    for exp_id in args.experiments:
        cfg = configs[exp_id]
        if args.noise_mode is not None:
            cfg.noise_mode = args.noise_mode
        model = build_model(cfg, DATASET_STATS[args.dataset]["num_classes"], DATASET_STATS[args.dataset]["image_size"], device)
        trainloader, testloader = get_dataloaders(
            args.dataset, args.batch_size, num_workers=args.num_workers, data_root=args.data_root
        )

        if args.mode == "eval":
            checkpoint_dir = args.checkpoint_dir or args.save_dir
            checkpoint_path = resolve_checkpoint_path(cfg, args.checkpoint, checkpoint_dir)
            checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
            state_dict = checkpoint.get("model_state_dict", checkpoint)
            model.load_state_dict(state_dict)
            print(
                f"Starting eval for {exp_id} on {args.dataset} "
                f"(Seed: {args.seed}, BS: {args.batch_size}, AMP: {args.amp}, "
                f"noise_mode: {cfg.noise_mode}, checkpoint={checkpoint_path})"
            )
            accuracies: List[float] = []
            losses: List[float] = []
            for run_idx in range(args.eval_runs):
                t_loss, t_acc = evaluate(model, testloader, criterion, device, cfg, args.amp)
                losses.append(t_loss)
                accuracies.append(t_acc)
                print(f"Eval run {run_idx + 1}/{args.eval_runs}: test_loss={t_loss:.4f}, test_acc={t_acc:.2f}%")
            acc_mean = float(np.mean(accuracies))
            acc_std = float(np.std(accuracies, ddof=1)) if len(accuracies) > 1 else 0.0
            print(
                f"Eval summary: checkpoint_epoch={checkpoint.get('epoch')}, "
                f"checkpoint_best_acc={checkpoint.get('best_acc')}, "
                f"test_acc_mean={acc_mean:.2f}%, test_acc_std={acc_std:.2f}%"
            )
            continue

        optimizer = optim.AdamW(model.parameters(), lr=cfg.lr, weight_decay=cfg.weight_decay)
        scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)
        scaler = create_grad_scaler(device, args.amp)
        start_epoch, best_acc, best_epoch, checkpoint_path, last_checkpoint_path, history, resume_checkpoint_path = (
            maybe_resume_experiment(
                model, optimizer, scheduler, cfg, args.save_dir, device,
                dataset=args.dataset, num_classes=DATASET_STATS[args.dataset]["num_classes"],
                resume_existing=args.resume_existing,
            )
        )
        print(
            f"Starting {exp_id} on {args.dataset} "
            f"(Seed: {args.seed}, BS: {args.batch_size}, AMP: {args.amp}, "
            f"noise_mode: {cfg.noise_mode})"
        )
        if resume_checkpoint_path is not None:
            print(
                f"Resuming from {resume_checkpoint_path}: start_epoch={start_epoch}, "
                f"best_acc={best_acc:.2f}%, best_epoch={best_epoch}"
            )
        os.makedirs(args.save_dir, exist_ok=True)
        for epoch in range(start_epoch, args.epochs):
            current_lr = optimizer.param_groups[0]["lr"]
            loss, acc = train_one_epoch(model, trainloader, optimizer, criterion, device, cfg, args.amp, scaler)
            t_loss, t_acc = evaluate(model, testloader, criterion, device, cfg, args.amp)
            history["train_loss"].append(loss)
            history["train_acc"].append(acc)
            history["test_loss"].append(t_loss)
            history["test_acc"].append(t_acc)
            history["lr"].append(current_lr)

            improved = t_acc > best_acc
            if improved:
                best_acc = t_acc
                best_epoch = epoch

            checkpoint_payload = build_training_checkpoint_payload(
                model, optimizer, scheduler, cfg, args.dataset, DATASET_STATS[args.dataset]["num_classes"],
                epoch, best_acc, best_epoch, history, args.amp, args.seed
            )
            torch.save(checkpoint_payload, last_checkpoint_path)
            if improved:
                torch.save(checkpoint_payload, checkpoint_path)
            scheduler.step()

            print(
                f"Epoch {epoch}: train_loss={loss:.4f}, train_acc={acc:.2f}%, "
                f"test_acc={t_acc:.2f}% (best={best_acc:.2f}%), lr={current_lr:.6f}"
            )
        print(f"Finished. Best accuracy: {best_acc:.2f}% at epoch {best_epoch}; checkpoint={checkpoint_path}")

if __name__ == "__main__":
    main()
