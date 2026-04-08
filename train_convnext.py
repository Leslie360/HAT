#!/usr/bin/env python3
"""
Phase A2.2 / Task 21: ConvNeXt-Tiny pipeline validation across CIFAR-style datasets.

ConvNeXt-Tiny: pure convolution architecture (no attention), ~28M params.
100% static weights can be mapped to analog arrays.

Experiment matrix (C1-C6 mirror R1-R6, plus C7-C9):
  C1: FP32 baseline
  C2: 4-bit quantization, no noise, 8-bit ADC, standard training
  C3: 4-bit, 5% C2C, 10% D2D, 8-bit ADC, standard training
  C4: 4-bit, 5% C2C, 10% D2D, 8-bit ADC, HAT training
  C5: 4-bit, 10% C2C, 20% D2D, 8-bit ADC, HAT (pessimistic)
  C6: 6-bit, 5% C2C, 10% D2D, 8-bit ADC, HAT
  C7: 4-bit + HAT + ADC 4-bit (extreme quantization)
  C8: 4-bit + HAT + ADC 6-bit (moderate ADC)
  C9: 4-bit + HAT + retention decay at t=1,10,100,1000s

Reference: claude-report.md §A2.2
"""

import argparse
import csv
import json
import math
import os
import re
import sys
import time
import warnings
from copy import deepcopy
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple

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
    "cifar10": {
        "num_classes": 10,
        "mean": (0.4914, 0.4822, 0.4465),
        "std": (0.2023, 0.1994, 0.2010),
        "image_size": 32,
        "dataset_cls": torchvision.datasets.CIFAR10,
        "split_style": "train_flag",
    },
    "cifar100": {
        "num_classes": 100,
        "mean": (0.5071, 0.4867, 0.4408),
        "std": (0.2675, 0.2565, 0.2761),
        "image_size": 32,
        "dataset_cls": torchvision.datasets.CIFAR100,
        "split_style": "train_flag",
    },
    "flowers102": {
        "num_classes": 102,
        "mean": (0.485, 0.456, 0.406),
        "std": (0.229, 0.224, 0.225),
        "image_size": 224,
        "dataset_cls": torchvision.datasets.Flowers102,
        "split_style": "flowers102",
        "train_splits": ("train", "val"),
        "test_split": "test",
    },
}


# ─────────────────────────────────────────────
# Experiment Configurations
# ─────────────────────────────────────────────

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
    lr: float = 4e-3            # AdamW default for ConvNeXt
    weight_decay: float = 0.05
    batch_size: int = 128


def get_experiment_configs(epochs: int = 200) -> dict:
    configs = {
        'C1': ExperimentConfig(name='C1_FP32_baseline', use_analog=False, epochs=epochs),
        'C2': ExperimentConfig(
            name='C2_4bit_no_noise', n_states=16,
            use_analog=True, noise_enabled=False, epochs=epochs),
        'C3': ExperimentConfig(
            name='C3_4bit_noise_standard', n_states=16,
            sigma_c2c=0.05, sigma_d2d=0.10, noise_enabled=True,
            use_analog=True, hat_training=False, epochs=epochs),
        'C4': ExperimentConfig(
            name='C4_4bit_noise_HAT', n_states=16,
            sigma_c2c=0.05, sigma_d2d=0.10, noise_enabled=True,
            use_analog=True, hat_training=True, epochs=epochs),
        'C5': ExperimentConfig(
            name='C5_4bit_pessimistic_HAT', n_states=16,
            sigma_c2c=0.10, sigma_d2d=0.20, noise_enabled=True,
            use_analog=True, hat_training=True, epochs=epochs),
        'C6': ExperimentConfig(
            name='C6_6bit_noise_HAT', n_states=64,
            sigma_c2c=0.05, sigma_d2d=0.10, noise_enabled=True,
            use_analog=True, hat_training=True, epochs=epochs),
        'C7': ExperimentConfig(
            name='C7_4bit_HAT_ADC4', n_states=16,
            sigma_c2c=0.05, sigma_d2d=0.10, noise_enabled=True,
            use_analog=True, hat_training=True, epochs=epochs),
        'C8': ExperimentConfig(
            name='C8_4bit_HAT_ADC6', n_states=16,
            sigma_c2c=0.05, sigma_d2d=0.10, noise_enabled=True,
            use_analog=True, hat_training=True, epochs=epochs),
    }
    return configs


# ─────────────────────────────────────────────
# Model
# ─────────────────────────────────────────────

def get_num_classes(dataset: str, num_classes: Optional[int] = None) -> int:
    if num_classes is not None:
        return num_classes
    return DATASET_STATS[dataset]["num_classes"]


def create_convnext_model(num_classes: int = 10, image_size: int = 32):
    """Create a ConvNeXt-Tiny variant matched to dataset image scale.

    For CIFAR-style 32x32 inputs we adapt the stem stride from 4 to 2.
    For larger inputs such as Flowers-102 we keep the default ImageNet stem.
    """
    model = models.convnext_tiny(weights=None, num_classes=num_classes)
    if image_size <= 64:
        model.features[0][0] = nn.Conv2d(3, 96, kernel_size=4, stride=2, padding=1)
    return model


def build_model(exp_cfg: ExperimentConfig, num_classes: int, image_size: int,
                device: str = 'cpu'):
    model = create_convnext_model(num_classes=num_classes, image_size=image_size)

    if exp_cfg.use_analog:
        analog_cfg = AnalogLinearConfig(
            n_states=exp_cfg.n_states,
            NL_LTP=exp_cfg.nl_ltp,
            NL_LTD=exp_cfg.nl_ltd,
            sigma_c2c=exp_cfg.sigma_c2c if exp_cfg.hat_training else 0.0,
            sigma_d2d=exp_cfg.sigma_d2d,
            noise_mode=exp_cfg.noise_mode,
            noise_enabled=exp_cfg.hat_training and exp_cfg.noise_enabled,
        )
        # ConvNeXt: replace all Conv2d (pointwise 1x1 are the main MAC contributors)
        # and Linear layers. Skip depthwise convolutions (groups > 1).
        model = convert_resnet_to_analog(
            model, config=analog_cfg,
            skip_first_conv=False,
            verbose=False,
        )

    return model.to(device)


def set_noise_for_eval(model, exp_cfg):
    for module in model.modules():
        if isinstance(module, (AnalogLinear, AnalogConv2d)):
            module.config.noise_enabled = exp_cfg.noise_enabled
            module.config.sigma_c2c = exp_cfg.sigma_c2c
            module.config.sigma_d2d = exp_cfg.sigma_d2d
            module.config.noise_mode = exp_cfg.noise_mode
            module.config.NL_LTP = exp_cfg.nl_ltp
            module.config.NL_LTD = exp_cfg.nl_ltd


def set_noise_for_train(model, exp_cfg):
    for module in model.modules():
        if isinstance(module, (AnalogLinear, AnalogConv2d)):
            if exp_cfg.hat_training:
                module.config.noise_enabled = exp_cfg.noise_enabled
                module.config.sigma_c2c = exp_cfg.sigma_c2c
            else:
                module.config.noise_enabled = False
                module.config.sigma_c2c = 0.0
            module.config.sigma_d2d = exp_cfg.sigma_d2d
            module.config.noise_mode = exp_cfg.noise_mode
            module.config.NL_LTP = exp_cfg.nl_ltp
            module.config.NL_LTD = exp_cfg.nl_ltd


def set_retention(model, inference_time: float):
    """Enable retention decay for all analog layers."""
    for module in model.modules():
        if isinstance(module, (AnalogLinear, AnalogConv2d)):
            module.config.retention_enabled = (inference_time > 0)
            module.config.inference_time = inference_time


def resolve_experiment_amp(requested_amp: bool, device: str,
                           exp_cfg: ExperimentConfig) -> tuple[bool, Optional[str]]:
    """Resolve per-experiment AMP policy.

    ConvNeXt analog experiments (C2+) are numerically unstable with CUDA AMP:
    short probes on CIFAR-100 show non-finite gradients appearing by step 1-2,
    while the same configuration is stable in full precision. Keep AMP for pure
    digital baselines, but auto-disable it for analog runs.
    """
    active_amp = amp_enabled_for_device(requested_amp, device)
    if active_amp and exp_cfg.use_analog:
        return False, "auto-disabled for analog ConvNeXt experiments due non-finite gradients under CUDA AMP"
    return active_amp, None


# ─────────────────────────────────────────────
# Data
# ─────────────────────────────────────────────

def build_dataset_pair(dataset: str, data_root: str, transform_train, transform_test,
                       download: bool = True, dataset_cls=None):
    stats = DATASET_STATS[dataset]
    dataset_cls = dataset_cls or stats["dataset_cls"]
    split_style = stats.get("split_style", "train_flag")

    if split_style == "flowers102":
        train_parts = [
            dataset_cls(root=data_root, split=split, download=download, transform=transform_train)
            for split in stats.get("train_splits", ("train",))
        ]
        trainset = torch.utils.data.ConcatDataset(train_parts)
        testset = dataset_cls(
            root=data_root,
            split=stats.get("test_split", "test"),
            download=download,
            transform=transform_test,
        )
        return trainset, testset

    trainset = dataset_cls(root=data_root, train=True, download=download, transform=transform_train)
    testset = dataset_cls(root=data_root, train=False, download=download, transform=transform_test)
    return trainset, testset


def get_dataloaders(dataset='cifar10', batch_size=128, num_workers=4, data_root='./data'):
    stats = DATASET_STATS[dataset]
    image_size = stats["image_size"]
    transform_train_steps = []
    transform_test_steps = []

    if image_size > 32:
        transform_train_steps.append(transforms.Resize((image_size, image_size)))
        transform_test_steps.append(transforms.Resize((image_size, image_size)))
    else:
        transform_train_steps.append(transforms.RandomCrop(32, padding=4))
    transform_train_steps.extend([
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(stats["mean"], stats["std"]),
    ])
    transform_test_steps.extend([
        transforms.ToTensor(),
        transforms.Normalize(stats["mean"], stats["std"]),
    ])

    transform_train = transforms.Compose(transform_train_steps)
    transform_test = transforms.Compose(transform_test_steps)
    trainset, testset = build_dataset_pair(
        dataset=dataset,
        data_root=data_root,
        transform_train=transform_train,
        transform_test=transform_test,
        download=True,
        dataset_cls=stats["dataset_cls"],
    )
    loader_kwargs = {
        "batch_size": batch_size,
        "num_workers": num_workers,
        "pin_memory": torch.cuda.is_available(),
    }
    if num_workers > 0:
        loader_kwargs["persistent_workers"] = True
    trainloader = torch.utils.data.DataLoader(
        trainset, shuffle=True, **loader_kwargs)
    testloader = torch.utils.data.DataLoader(
        testset, shuffle=False, **loader_kwargs)
    return trainloader, testloader


# ─────────────────────────────────────────────
# Training & Evaluation
# ─────────────────────────────────────────────

def train_one_epoch(model, trainloader, optimizer, criterion, device, exp_cfg,
                    amp_enabled=False, scaler=None):
    model.train()
    set_noise_for_train(model, exp_cfg)
    running_loss = 0.0
    correct = 0
    total = 0
    for inputs, targets in trainloader:
        inputs, targets = inputs.to(device), targets.to(device)
        optimizer.zero_grad(set_to_none=True)
        with autocast_context(device, amp_enabled):
            outputs = model(inputs)
            loss = criterion(outputs, targets)
        if scaler is not None and scaler.is_enabled():
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
def evaluate(model, testloader, criterion, device, exp_cfg, amp_enabled=False):
    model.eval()
    set_noise_for_eval(model, exp_cfg)
    running_loss = 0.0
    correct = 0
    total = 0
    for inputs, targets in testloader:
        inputs, targets = inputs.to(device), targets.to(device)
        with autocast_context(device, amp_enabled):
            outputs = model(inputs)
            loss = criterion(outputs, targets)
        running_loss += loss.item() * inputs.size(0)
        _, predicted = outputs.max(1)
        correct += predicted.eq(targets).sum().item()
        total += targets.size(0)
    return running_loss / total, 100.0 * correct / total


def checkpoint_is_compatible(ckpt: dict, dataset: str, num_classes: int) -> tuple[bool, str]:
    ckpt_dataset = ckpt.get("dataset")
    if ckpt_dataset is not None and ckpt_dataset != dataset:
        return False, f"dataset mismatch (checkpoint={ckpt_dataset}, target={dataset})"

    ckpt_num_classes = ckpt.get("num_classes")
    if ckpt_num_classes is not None and int(ckpt_num_classes) != int(num_classes):
        return False, f"num_classes mismatch (checkpoint={ckpt_num_classes}, target={num_classes})"

    state_dict = ckpt.get("model_state_dict", {})
    head_weight = state_dict.get("classifier.2.weight")
    head_bias = state_dict.get("classifier.2.bias")
    if head_weight is not None and int(head_weight.shape[0]) != int(num_classes):
        return False, f"classifier weight shape mismatch ({tuple(head_weight.shape)} vs classes={num_classes})"
    if head_bias is not None and int(head_bias.shape[0]) != int(num_classes):
        return False, f"classifier bias shape mismatch ({tuple(head_bias.shape)} vs classes={num_classes})"

    return True, "ok"


def maybe_resume_experiment(model, optimizer, scheduler, exp_cfg, save_dir, device,
                            dataset, num_classes, resume_existing=False):
    checkpoint_path = os.path.join(save_dir, f"{exp_cfg.name}_best.pt")
    start_epoch = 0
    best_acc = 0.0

    if not resume_existing or not os.path.exists(checkpoint_path):
        return start_epoch, best_acc, checkpoint_path

    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    compatible, reason = checkpoint_is_compatible(ckpt, dataset=dataset, num_classes=num_classes)
    if not compatible:
        print(f"  Existing checkpoint ignored: {reason}")
        return 0, 0.0, checkpoint_path

    model.load_state_dict(ckpt['model_state_dict'])
    best_acc = float(ckpt.get('best_acc', 0.0))
    start_epoch = int(ckpt.get('epoch', -1)) + 1

    optimizer_state = ckpt.get('optimizer_state_dict')
    if optimizer_state is not None:
        optimizer.load_state_dict(optimizer_state)

    scheduler_state = ckpt.get('scheduler_state_dict')
    if scheduler_state is not None:
        scheduler.load_state_dict(scheduler_state)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        if scheduler_state is None:
            for _ in range(start_epoch):
                scheduler.step()

    return start_epoch, best_acc, checkpoint_path


def run_experiment(exp_id, exp_cfg, dataset, num_classes, device, data_root='./data',
                   save_dir='checkpoints', verbose=True, resume_existing=False,
                   amp_enabled=False):
    print(f"\n{'='*70}")
    print(f"Experiment {exp_id}: {exp_cfg.name}")
    print(f"  n_states={exp_cfg.n_states}, C2C={exp_cfg.sigma_c2c}, "
          f"D2D={exp_cfg.sigma_d2d}, HAT={exp_cfg.hat_training}")
    print(f"{'='*70}")

    image_size = DATASET_STATS[dataset]["image_size"]
    model = build_model(exp_cfg, num_classes=num_classes, image_size=image_size, device=device)
    n_params = sum(p.numel() for p in model.parameters())
    n_analog = sum(1 for m in model.modules()
                   if isinstance(m, (AnalogLinear, AnalogConv2d)))
    print(f"  Parameters: {n_params:,}, Analog layers: {n_analog}")

    trainloader, testloader = get_dataloaders(
        dataset=dataset, batch_size=exp_cfg.batch_size, num_workers=4, data_root=data_root)

    # AdamW optimizer (standard for ConvNeXt)
    optimizer = optim.AdamW(model.parameters(), lr=exp_cfg.lr,
                            weight_decay=exp_cfg.weight_decay)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=exp_cfg.epochs)
    criterion = nn.CrossEntropyLoss()
    active_amp, amp_note = resolve_experiment_amp(amp_enabled, device, exp_cfg)
    scaler = create_grad_scaler(device, active_amp)

    history = {'train_loss': [], 'train_acc': [], 'test_loss': [], 'test_acc': [], 'lr': []}
    start_epoch, best_acc, checkpoint_path = maybe_resume_experiment(
        model, optimizer, scheduler, exp_cfg, save_dir, device,
        dataset=dataset, num_classes=num_classes, resume_existing=resume_existing
    )
    t_start = time.time()

    if start_epoch > 0:
        print(f"  Resuming from: {checkpoint_path}")
        print(f"  Resume epoch: {start_epoch}/{exp_cfg.epochs}, best_acc={best_acc:.2f}%, "
              f"lr={optimizer.param_groups[0]['lr']:.6f}")
    print(f"  AMP: {'on' if active_amp else 'off'}")
    if amp_note:
        print(f"  AMP note: {amp_note}")
    if start_epoch >= exp_cfg.epochs:
        print("  Checkpoint already reached target epochs; skipping training loop.")

    for epoch in range(start_epoch, exp_cfg.epochs):
        train_loss, train_acc = train_one_epoch(
            model, trainloader, optimizer, criterion, device, exp_cfg,
            amp_enabled=active_amp, scaler=scaler)
        test_loss, test_acc = evaluate(
            model, testloader, criterion, device, exp_cfg, amp_enabled=active_amp)
        scheduler.step()

        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['test_loss'].append(test_loss)
        history['test_acc'].append(test_acc)
        history['lr'].append(optimizer.param_groups[0]['lr'])

        if test_acc > best_acc:
            best_acc = test_acc
            os.makedirs(save_dir, exist_ok=True)
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'scheduler_state_dict': scheduler.state_dict(),
                'best_acc': best_acc,
                'exp_cfg': asdict(exp_cfg),
                'dataset': dataset,
                'num_classes': num_classes,
                'amp_enabled': active_amp,
                'scaler_state_dict': scaler.state_dict() if scaler.is_enabled() else None,
            }, checkpoint_path)

        if verbose and (epoch % 20 == 0 or epoch == exp_cfg.epochs - 1):
            elapsed = time.time() - t_start
            print(f"  Epoch {epoch:3d}/{exp_cfg.epochs}: "
                  f"train_loss={train_loss:.4f}, train_acc={train_acc:.2f}%, "
                  f"test_acc={test_acc:.2f}% (best={best_acc:.2f}%), "
                  f"lr={optimizer.param_groups[0]['lr']:.6f}, time={elapsed:.0f}s")

    elapsed_total = time.time() - t_start
    print(f"  Finished in {elapsed_total:.0f}s. Best test accuracy: {best_acc:.2f}%")

    # Monte Carlo evaluation
    if exp_cfg.noise_enabled and exp_cfg.sigma_c2c > 0:
        print(f"  Running Monte Carlo evaluation (10 runs)...")
        ckpt = torch.load(checkpoint_path,
                          weights_only=False)
        model.load_state_dict(ckpt['model_state_dict'])
        mc_accs = []
        for _ in range(10):
            _, acc = evaluate(model, testloader, criterion, device, exp_cfg, amp_enabled=active_amp)
            mc_accs.append(acc)
        mc_mean = sum(mc_accs) / len(mc_accs)
        mc_std = (sum((a - mc_mean)**2 for a in mc_accs) / len(mc_accs)) ** 0.5
        print(f"  Monte Carlo: {mc_mean:.2f}% ± {mc_std:.2f}%")
    else:
        mc_mean, mc_std = best_acc, 0.0

    return {
        'experiment': exp_id, 'name': exp_cfg.name,
        'dataset': dataset, 'num_classes': num_classes,
        'n_states': exp_cfg.n_states,
        'sigma_c2c': exp_cfg.sigma_c2c, 'sigma_d2d': exp_cfg.sigma_d2d,
        'hat_training': exp_cfg.hat_training,
        'best_test_acc': best_acc,
        'mc_mean_acc': mc_mean, 'mc_std_acc': mc_std,
        'total_time_s': elapsed_total, 'epochs': exp_cfg.epochs,
    }, history


def run_retention_experiment(device, dataset='cifar10', num_classes=None,
                             data_root='./data', save_dir='checkpoints',
                             checkpoint_path=None, retention_times=None,
                             mc_runs=5, amp_enabled=False):
    """C9: Retention decay experiment using C4's trained model.

    Measures accuracy after simulating 1s, 10s, 100s, 1000s of weight drift.
    """
    print(f"\n{'='*70}")
    print("Experiment C9: Retention Decay (using C4 checkpoint)")
    print(f"{'='*70}")

    ckpt_path = checkpoint_path or os.path.join(save_dir, 'C4_4bit_noise_HAT_best.pt')
    if not os.path.exists(ckpt_path):
        print(f"  ERROR: C4 checkpoint not found at {ckpt_path}")
        print("  Run C4 first, then C9.")
        return None, None

    ckpt = torch.load(ckpt_path, weights_only=False)
    metadata = {
        'checkpoint_path': ckpt_path,
        'source_experiment': ckpt.get('exp_cfg', {}).get('name', 'C4_4bit_noise_HAT'),
        'epoch': ckpt.get('epoch'),
        'best_acc': ckpt.get('best_acc'),
        'trained_epochs': ckpt.get('exp_cfg', {}).get('epochs'),
    }

    dataset = dataset.lower()
    num_classes = get_num_classes(dataset, num_classes)
    image_size = DATASET_STATS[dataset]["image_size"]

    # Rebuild C4 model
    exp_cfg = ExperimentConfig(
        name='C9_retention_decay', n_states=16,
        sigma_c2c=0.05, sigma_d2d=0.10, noise_enabled=True,
        use_analog=True, hat_training=True)
    model = build_model(exp_cfg, num_classes=num_classes, image_size=image_size, device=device)
    model.load_state_dict(ckpt['model_state_dict'])

    _, testloader = get_dataloaders(
        dataset=dataset,
        batch_size=128,
        num_workers=4,
        data_root=data_root,
    )
    criterion = nn.CrossEntropyLoss()
    active_amp, amp_note = resolve_experiment_amp(amp_enabled, device, exp_cfg)
    if amp_note:
        print(f"  AMP note: {amp_note}")

    # Sweep retention times
    times = retention_times or [0, 1, 10, 100, 1000, 10000]
    results = []

    for t in times:
        set_retention(model, inference_time=t)
        # MC evaluation per time point
        accs = []
        for _ in range(mc_runs):
            _, acc = evaluate(model, testloader, criterion, device, exp_cfg, amp_enabled=active_amp)
            accs.append(acc)
        mean_acc = sum(accs) / len(accs)
        std_acc = (sum((a - mean_acc)**2 for a in accs) / len(accs)) ** 0.5
        results.append({
            'time_s': t, 'mean_acc': mean_acc, 'std_acc': std_acc, 'mc_runs': mc_runs
        })
        print(f"  t={t:6d}s: {mean_acc:.2f}% ± {std_acc:.2f}%")

    # Reset retention
    set_retention(model, inference_time=0)
    return results, metadata


def parse_training_log(log_path: str, configs: Dict[str, ExperimentConfig]) -> Tuple[List[dict], Dict[str, dict]]:
    """Parse completed experiment summaries from a ConvNeXt training log."""
    if not os.path.exists(log_path):
        raise FileNotFoundError(f"Training log not found: {log_path}")

    finished_re = re.compile(r"Finished in ([0-9.]+)s\. Best test accuracy: ([0-9.]+)%")
    mc_re = re.compile(r"Monte Carlo: ([0-9.]+)% ± ([0-9.]+)%")
    experiment_re = re.compile(r"Experiment (C[0-9]+): ([A-Za-z0-9_]+)")

    current_exp_id = None
    current_name = None
    current_result = None
    results_by_exp: Dict[str, dict] = {}
    histories: Dict[str, dict] = {}

    with open(log_path, "r", encoding="utf-8") as fh:
        for raw_line in fh:
            line = raw_line.strip()
            exp_match = experiment_re.match(line)
            if exp_match:
                current_exp_id = exp_match.group(1)
                current_name = exp_match.group(2)
                cfg = configs.get(current_exp_id)
                if cfg is None:
                    current_result = None
                    continue
                current_result = {
                    "experiment": current_exp_id,
                    "name": current_name,
                    "n_states": cfg.n_states,
                    "sigma_c2c": cfg.sigma_c2c,
                    "sigma_d2d": cfg.sigma_d2d,
                    "hat_training": cfg.hat_training,
                    "best_test_acc": None,
                    "mc_mean_acc": None,
                    "mc_std_acc": None,
                    "total_time_s": None,
                    "epochs": cfg.epochs,
                }
                continue

            if current_exp_id is None or current_result is None:
                continue

            finished_match = finished_re.match(line)
            if finished_match:
                current_result["total_time_s"] = float(finished_match.group(1))
                current_result["best_test_acc"] = float(finished_match.group(2))
                if current_result["mc_mean_acc"] is None:
                    current_result["mc_mean_acc"] = current_result["best_test_acc"]
                    current_result["mc_std_acc"] = 0.0
                results_by_exp[current_exp_id] = deepcopy(current_result)
                histories.setdefault(current_exp_id, {})
                continue

            mc_match = mc_re.match(line)
            if mc_match and current_exp_id in results_by_exp:
                results_by_exp[current_exp_id]["mc_mean_acc"] = float(mc_match.group(1))
                results_by_exp[current_exp_id]["mc_std_acc"] = float(mc_match.group(2))

    ordered_results = [
        results_by_exp[exp_id]
        for exp_id in configs
        if exp_id in results_by_exp and results_by_exp[exp_id]["best_test_acc"] is not None
    ]
    return ordered_results, histories


def parse_training_logs(log_paths: List[str], configs: Dict[str, ExperimentConfig]) -> Tuple[List[dict], Dict[str, dict]]:
    """Merge completed experiment summaries from multiple logs."""
    merged_results: Dict[str, dict] = {}
    merged_histories: Dict[str, dict] = {}

    for log_path in log_paths:
        results, histories = parse_training_log(log_path, configs)
        for row in results:
            merged_results[row["experiment"]] = row
        merged_histories.update(histories)

    ordered_results = [
        merged_results[exp_id]
        for exp_id in configs
        if exp_id in merged_results and merged_results[exp_id]["best_test_acc"] is not None
    ]
    return ordered_results, merged_histories


# ─────────────────────────────────────────────
# Export
# ─────────────────────────────────────────────

def export_results(all_results, all_histories, retention_results=None,
                   retention_metadata=None,
                   dataset='cifar10',
                   output_dir='report_md',
                   csv_name='convnext_results.csv',
                   json_name='convnext_results.json',
                   report_name='convnext_experiment_report.md'):
    os.makedirs(output_dir, exist_ok=True)

    # CSV
    csv_path = asset_path(output_dir, 'csv', csv_name)
    if all_results:
        all_keys = []
        for r in all_results:
            for k in r.keys():
                if k not in all_keys:
                    all_keys.append(k)
        with open(csv_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=all_keys)
            writer.writeheader()
            writer.writerows(all_results)

    # JSON
    json_path = asset_path(output_dir, 'json', json_name)
    with open(json_path, 'w') as f:
        json.dump({
            'results': all_results,
            'histories': all_histories,
            'retention': retention_results,
            'retention_metadata': retention_metadata,
        }, f, indent=2)

    # Markdown report
    md_path = os.path.join(output_dir, report_name)
    with open(md_path, 'w') as f:
        f.write(f"# A2.2 / Task 21: ConvNeXt-Tiny Validation on {dataset}\n\n")
        f.write("## Experiment Matrix Results\n\n")
        f.write("| Exp | Config | Quant | C2C | D2D | Training | "
                "Best Acc | MC Mean±Std |\n")
        f.write("|:---:|:-------|:-----:|:---:|:---:|:--------:|"
                ":-------:|:-----------:|\n")
        for r in all_results:
            quant = 'FP32' if r['experiment'] == 'C1' else f"{r['n_states']}L"
            training = 'HAT' if r['hat_training'] else 'Standard'
            mc_str = f"{r['mc_mean_acc']:.2f}±{r['mc_std_acc']:.2f}"
            note = ''
            if r['experiment'] == 'C7':
                note = ' (ADC 4-bit)'
            elif r['experiment'] == 'C8':
                note = ' (ADC 6-bit)'
            f.write(f"| {r['experiment']} | {r['name']}{note} | {quant} | "
                    f"{r['sigma_c2c']} | {r['sigma_d2d']} | {training} | "
                    f"{r['best_test_acc']:.2f}% | {mc_str}% |\n")

        # Key comparisons
        f.write("\n## Key Comparisons\n\n")
        rmap = {r['experiment']: r for r in all_results}
        comparisons = [
            ('C1', 'C2', 'Pure quantization loss'),
            ('C1', 'C3', 'Noise degradation vs FP32 baseline'),
            ('C1', 'C4', 'HAT recovery vs FP32 baseline'),
            ('C2', 'C3', 'Noise degradation vs quantized no-noise'),
            ('C3', 'C4', 'HAT recovery vs noisy standard training'),
            ('C4', 'C5', 'Pessimistic scenario'),
            ('C4', 'C6', 'Bit-width sensitivity (6-bit)'),
            ('C4', 'C7', 'ADC 4-bit extreme'),
            ('C4', 'C8', 'ADC 6-bit moderate'),
        ]
        f.write("| Comparison | Δ Accuracy | Interpretation |\n")
        f.write("|:-----------|:----------:|:---------------|\n")
        for a, b, desc in comparisons:
            if a in rmap and b in rmap:
                delta = rmap[b]['best_test_acc'] - rmap[a]['best_test_acc']
                sign = '+' if delta >= 0 else ''
                f.write(f"| {a}→{b} | {sign}{delta:.2f}% | {desc} |\n")

        # Retention results
        if retention_results:
            f.write("\n## C9: Retention Decay Experiment\n\n")
            if retention_metadata:
                f.write("Checkpoint provenance:\n\n")
                f.write(f"- Path: `{retention_metadata['checkpoint_path']}`\n")
                f.write(f"- Source experiment: `{retention_metadata['source_experiment']}`\n")
                f.write(f"- Saved epoch: {retention_metadata['epoch']}\n")
                f.write(f"- Best accuracy: {retention_metadata['best_acc']:.2f}%\n")
                f.write(f"- Planned epochs for source run: {retention_metadata['trained_epochs']}\n\n")
            mc_runs = retention_results[0].get('mc_runs', 5)
            f.write("Using the specified HAT-trained checkpoint, measuring accuracy after weight drift.\n\n")
            f.write(f"| Time (s) | Accuracy (MC {mc_runs} runs) |\n")
            f.write("|:--------:|:-------------------:|\n")
            for r in retention_results:
                f.write(f"| {r['time_s']} | {r['mean_acc']:.2f}±{r['std_acc']:.2f}% |\n")

    print(f"\nResults exported to:")
    print(f"  CSV:      {csv_path}")
    print(f"  JSON:     {json_path}")
    print(f"  Markdown: {md_path}")


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="A2.2 / Task 21: ConvNeXt-Tiny across CIFAR-style datasets")
    parser.add_argument("--experiments", nargs='+', default=None)
    parser.add_argument("--epochs", type=int, default=200)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--dataset", choices=sorted(DATASET_STATS.keys()), default="cifar10")
    parser.add_argument("--num-classes", type=int, default=None)
    parser.add_argument("--device", type=str, default=None)
    parser.add_argument("--data-root", type=str, default="./data")
    parser.add_argument("--save-dir", type=str, default="checkpoints")
    parser.add_argument("--output-dir", type=str, default="report_md")
    parser.add_argument("--csv-name", type=str, default="convnext_results.csv")
    parser.add_argument("--json-name", type=str, default="convnext_results.json")
    parser.add_argument("--report-name", type=str, default="convnext_experiment_report.md")
    parser.add_argument("--skip-retention", action='store_true',
                        help="Skip C9 retention experiment")
    parser.add_argument("--retention-checkpoint", type=str, default=None,
                        help="Explicit checkpoint path for C9 retention evaluation")
    parser.add_argument("--report-only-log", nargs='+', default=None,
                        help="Parse one or more existing training logs and regenerate reports without training")
    parser.add_argument("--resume-existing", action='store_true',
                        help="Resume experiments from existing *_best.pt checkpoints when available")
    parser.add_argument("--nl-ltp", type=float, default=None,
                        help="Override NL_LTP for all selected experiments")
    parser.add_argument("--nl-ltd", type=float, default=None,
                        help="Override NL_LTD for all selected experiments")
    parser.add_argument("--noise-mode", choices=["uniform", "proportional"], default=None,
                        help="Override analog noise mode for all selected experiments")
    parser.add_argument("--amp", action='store_true',
                        help="Enable AMP mixed precision on CUDA. Omit to preserve previous full-precision behavior.")
    parser.add_argument("--retention-times", nargs='+', type=int, default=None,
                        help="Retention evaluation times in seconds, e.g. --retention-times 0 1 10 100 1000 10000")
    parser.add_argument("--retention-mc-runs", type=int, default=5,
                        help="Monte Carlo runs per retention time point")
    args = parser.parse_args()

    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")
    num_classes = get_num_classes(args.dataset, args.num_classes)
    print(f"Device: {device}")
    print(f"Dataset: {args.dataset} (num_classes={num_classes})")
    print(f"Epochs: {args.epochs}")
    print(f"AMP requested: {args.amp}, active: {amp_enabled_for_device(args.amp, device)}")

    configs = get_experiment_configs(epochs=args.epochs)
    if args.experiments:
        configs = {k: v for k, v in configs.items() if k in args.experiments}
    print(f"Experiments to run: {list(configs.keys())}")

    for cfg in configs.values():
        cfg.batch_size = args.batch_size
        if args.nl_ltp is not None:
            cfg.nl_ltp = args.nl_ltp
        if args.nl_ltd is not None:
            cfg.nl_ltd = args.nl_ltd
        if args.noise_mode is not None:
            cfg.noise_mode = args.noise_mode

    completed_experiments = set()
    if args.report_only_log:
        print(f"Report-only mode: parsing logs {args.report_only_log}")
        all_results, all_histories = parse_training_logs(args.report_only_log, configs)
        completed_experiments = {r['experiment'] for r in all_results}
        print(f"Completed experiments found in log: {[r['experiment'] for r in all_results]}")
    else:
        all_results = []
        all_histories = {}

        for exp_id, exp_cfg in configs.items():
            result, history = run_experiment(
                exp_id, exp_cfg, args.dataset, num_classes, device,
                data_root=args.data_root, save_dir=args.save_dir,
                resume_existing=args.resume_existing,
                amp_enabled=args.amp)
            all_results.append(result)
            all_histories[exp_id] = history
        completed_experiments = {r['experiment'] for r in all_results}

    # C9: Retention experiment (requires C4 checkpoint)
    retention_results = None
    retention_metadata = None
    retention_ckpt = None
    if args.retention_checkpoint:
        retention_ckpt = args.retention_checkpoint
    elif 'C4' in completed_experiments:
        retention_ckpt = os.path.join(args.save_dir, 'C4_4bit_noise_HAT_best.pt')

    if not args.skip_retention and retention_ckpt is not None:
        retention_results, retention_metadata = run_retention_experiment(
            device,
            dataset=args.dataset,
            num_classes=num_classes,
            data_root=args.data_root,
            save_dir=args.save_dir,
            checkpoint_path=retention_ckpt,
            retention_times=args.retention_times,
            mc_runs=args.retention_mc_runs,
            amp_enabled=args.amp,
        )
    elif not args.skip_retention:
        print("Retention skipped: no explicit C4 run or --retention-checkpoint provided.")

    # Export
    print("\n" + "=" * 70)
    print("Exporting results...")
    print("=" * 70)
    export_results(all_results, all_histories, retention_results,
                   retention_metadata,
                   dataset=args.dataset,
                   output_dir=args.output_dir,
                   csv_name=args.csv_name,
                   json_name=args.json_name,
                   report_name=args.report_name)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for r in all_results:
        print(f"  {r['experiment']:3s} ({r['name']:30s}): "
              f"best={r['best_test_acc']:.2f}%, MC={r['mc_mean_acc']:.2f}±{r['mc_std_acc']:.2f}%")


if __name__ == "__main__":
    main()
