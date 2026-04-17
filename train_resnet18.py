#!/usr/bin/env python3
"""
Phase A2.1: ResNet-18 Full Pipeline Validation on CIFAR-10

Runs the 6-configuration experiment matrix:
  R1: FP32 baseline (standard training, no quantization/noise)
  R2: 4-bit quantization, no noise, 8-bit ADC, standard training
  R3: 4-bit, 5% C2C, 10% D2D, 8-bit ADC, standard training
  R4: 4-bit, 5% C2C, 10% D2D, 8-bit ADC, HAT training
  R5: 4-bit, 10% C2C, 20% D2D, 8-bit ADC, HAT training
  R6: 6-bit, 5% C2C, 10% D2D, 8-bit ADC, HAT training

Key comparisons:
  R1 vs R2: pure quantization loss
  R2 vs R3: noise degradation
  R3 vs R4: HAT recovery (core result)
  R4 vs R5: pessimistic scenario survival
  R4 vs R6: bit-width sensitivity

Reference: claude-report.md §A2.1
"""

import argparse
import csv
import json
import os
import sys
import time
from dataclasses import dataclass, asdict, fields
from typing import Optional

# Unbuffer stdout for real-time log output via tee/pipe
sys.stdout.reconfigure(line_buffering=True)

import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import torchvision.models as models

from analog_layers import (
    AnalogLinear, AnalogLinearConfig, AnalogConv2d,
    convert_resnet_to_analog,
)
from amp_utils import amp_enabled_for_device, autocast_context, create_grad_scaler
from report_asset_paths import asset_path


# ─────────────────────────────────────────────
# Experiment Configurations
# ─────────────────────────────────────────────

@dataclass
class ExperimentConfig:
    """Single experiment configuration."""
    name: str
    n_states: int = 16          # quantization levels (16=4-bit, 64=6-bit)
    sigma_c2c: float = 0.0
    sigma_d2d: float = 0.0
    noise_enabled: bool = False
    use_analog: bool = False     # whether to use AnalogConv2d/AnalogLinear
    hat_training: bool = False   # HAT = noise ON during training
    restore_weight_scale: bool = True # Whether to restore FP32 weight scale

    # Training hyperparameters
    epochs: int = 200
    lr: float = 0.1
    momentum: float = 0.9
    weight_decay: float = 5e-4
    batch_size: int = 128


def load_experiment_config_from_checkpoint(ckpt: dict) -> ExperimentConfig:
    """Rebuild ExperimentConfig with compatibility for legacy ResNet checkpoints.

    Older CIFAR-10 analog checkpoints were saved before `restore_weight_scale`
    was serialized in `exp_cfg`. Those runs used the analog-layer default
    (`False`), while the current ExperimentConfig default is `True`. Falling
    back to the current default breaks legacy checkpoint replay and collapses
    analog accuracy to chance level.
    """
    raw_cfg = dict(ckpt.get("exp_cfg", {}))
    valid = {field.name for field in fields(ExperimentConfig)}
    filtered = {k: v for k, v in raw_cfg.items() if k in valid}
    if "restore_weight_scale" not in raw_cfg:
        filtered["restore_weight_scale"] = False
    return ExperimentConfig(**filtered)


def get_experiment_configs(epochs: int = 200) -> dict:
    """Return the 6 experiment configurations from the plan."""
    configs = {
        'R1': ExperimentConfig(
            name='R1_FP32_baseline',
            use_analog=False, noise_enabled=False,
            epochs=epochs,
        ),
        'R2': ExperimentConfig(
            name='R2_4bit_no_noise',
            n_states=16, sigma_c2c=0.0, sigma_d2d=0.0,
            noise_enabled=False, use_analog=True, hat_training=False,
            epochs=epochs,
        ),
        'R3': ExperimentConfig(
            name='R3_4bit_noise_standard',
            n_states=16, sigma_c2c=0.05, sigma_d2d=0.10,
            noise_enabled=True, use_analog=True, hat_training=False,
            epochs=epochs,
        ),
        'R4': ExperimentConfig(
            name='R4_4bit_noise_HAT',
            n_states=16, sigma_c2c=0.05, sigma_d2d=0.10,
            noise_enabled=True, use_analog=True, hat_training=True,
            epochs=epochs,
        ),
        'R5': ExperimentConfig(
            name='R5_4bit_pessimistic_HAT',
            n_states=16, sigma_c2c=0.10, sigma_d2d=0.20,
            noise_enabled=True, use_analog=True, hat_training=True,
            epochs=epochs,
        ),
        'R6': ExperimentConfig(
            name='R6_6bit_noise_HAT',
            n_states=64, sigma_c2c=0.05, sigma_d2d=0.10,
            noise_enabled=True, use_analog=True, hat_training=True,
            epochs=epochs,
        ),
    }
    return configs


# ─────────────────────────────────────────────
# Model
# ─────────────────────────────────────────────

def create_resnet18_cifar(num_classes: int = 10):
    """Create ResNet-18 adapted for CIFAR-10 (32x32 input).

    Modifications from standard ImageNet ResNet-18:
      - conv1: 3x3 kernel, stride=1, padding=1 (instead of 7x7 stride=2)
      - Remove maxpool
    """
    model = models.resnet18(weights=None, num_classes=num_classes)
    model.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
    model.maxpool = nn.Identity()
    return model


def build_model(exp_cfg: ExperimentConfig, num_classes: int = 10, device: str = 'cpu'):
    """Build model according to experiment configuration.

    For R1 (FP32): standard ResNet-18
    For R2-R6: convert applicable layers to AnalogConv2d/AnalogLinear
    """
    model = create_resnet18_cifar(num_classes=num_classes)

    if exp_cfg.use_analog:
        analog_cfg = AnalogLinearConfig(
            n_states=exp_cfg.n_states,
            sigma_c2c=exp_cfg.sigma_c2c,
            sigma_d2d=exp_cfg.sigma_d2d,
            noise_enabled=exp_cfg.hat_training and exp_cfg.noise_enabled,
            restore_weight_scale=exp_cfg.restore_weight_scale,
        )

        model = convert_resnet_to_analog(
            model, config=analog_cfg,
            skip_first_conv=False,  # include all conv layers for ResNet
            verbose=False,
        )

    return model.to(device)


def set_noise_for_eval(model: nn.Module, exp_cfg: ExperimentConfig):
    """Set noise parameters for evaluation (may differ from training).

    During standard training (R2, R3): noise is OFF during training but
    ON during evaluation to measure true hardware impact.
    During HAT training (R4-R6): noise is ON during both training and eval.
    """
    for module in model.modules():
        if isinstance(module, (AnalogLinear, AnalogConv2d)):
            module.config.noise_enabled = exp_cfg.noise_enabled
            module.config.sigma_c2c = exp_cfg.sigma_c2c
            module.config.sigma_d2d = exp_cfg.sigma_d2d


def set_noise_for_train(model: nn.Module, exp_cfg: ExperimentConfig):
    """Set noise parameters for training.

    HAT training: noise enabled during training (STE gradient through quantization)
    Standard training: noise disabled during training
    """
    for module in model.modules():
        if isinstance(module, (AnalogLinear, AnalogConv2d)):
            if exp_cfg.hat_training:
                module.config.noise_enabled = exp_cfg.noise_enabled
                module.config.sigma_c2c = exp_cfg.sigma_c2c
            else:
                module.config.noise_enabled = False
                module.config.sigma_c2c = 0.0


# ─────────────────────────────────────────────
# Data
# ─────────────────────────────────────────────

def get_dataloaders(dataset: str = "cifar10", batch_size: int = 128, num_workers: int = 4,
                    data_root: str = './data'):
    """CIFAR-10/100 train/test loaders with standard augmentation."""
    if dataset == "cifar10":
        mean, std = (0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)
        ds_class = torchvision.datasets.CIFAR10
    elif dataset == "cifar100":
        mean, std = (0.5071, 0.4867, 0.4408), (0.2675, 0.2565, 0.2761)
        ds_class = torchvision.datasets.CIFAR100
    else:
        raise ValueError(f"Unknown dataset {dataset}")

    transform_train = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean, std),
    ])
    transform_test = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean, std),
    ])

    trainset = ds_class(
        root=data_root, train=True, download=True, transform=transform_train)
    trainloader = torch.utils.data.DataLoader(
        trainset, batch_size=batch_size, shuffle=True, num_workers=num_workers)

    testset = ds_class(
        root=data_root, train=False, download=True, transform=transform_test)
    testloader = torch.utils.data.DataLoader(
        testset, batch_size=batch_size, shuffle=False, num_workers=num_workers)

    return trainloader, testloader


# ─────────────────────────────────────────────
# Training & Evaluation
# ─────────────────────────────────────────────

def train_one_epoch(model, trainloader, optimizer, criterion, device, exp_cfg,
                    amp_enabled=False, scaler=None):
    """Train for one epoch."""
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
    """Evaluate on test set with proper noise configuration."""
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


def run_experiment(exp_id: str, exp_cfg: ExperimentConfig, device: str,
                   dataset: str = "cifar10", seed: int = 42,
                   data_root: str = './data', save_dir: str = 'checkpoints',
                   verbose: bool = True, amp_enabled: bool = False):
    """Run a single experiment configuration end-to-end.

    Returns:
        dict with final metrics and training history
    """
    print(f"\n{'='*70}")
    print(f"Experiment {exp_id}: {exp_cfg.name} on {dataset} (seed={seed})")
    print(f"  n_states={exp_cfg.n_states}, C2C={exp_cfg.sigma_c2c}, "
          f"D2D={exp_cfg.sigma_d2d}, HAT={exp_cfg.hat_training}")
    print(f"{'='*70}")

    import random
    import numpy as np
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)

    num_classes = 100 if dataset == "cifar100" else 10

    # Build model
    model = build_model(exp_cfg, num_classes=num_classes, device=device)
    n_params = sum(p.numel() for p in model.parameters())
    n_analog = sum(1 for m in model.modules()
                   if isinstance(m, (AnalogLinear, AnalogConv2d)))
    print(f"  Parameters: {n_params:,}, Analog layers: {n_analog}")

    # Data
    trainloader, testloader = get_dataloaders(
        dataset=dataset, batch_size=exp_cfg.batch_size, num_workers=4, data_root=data_root)

    # Optimizer & scheduler
    optimizer = optim.SGD(model.parameters(), lr=exp_cfg.lr,
                          momentum=exp_cfg.momentum, weight_decay=exp_cfg.weight_decay)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=exp_cfg.epochs)
    criterion = nn.CrossEntropyLoss()
    scaler = create_grad_scaler(device, amp_enabled)
    active_amp = amp_enabled_for_device(amp_enabled, device)

    # Training loop
    history = {'train_loss': [], 'train_acc': [], 'test_loss': [], 'test_acc': [], 'lr': []}
    best_acc = 0.0
    t_start = time.time()
    print(f"  AMP: {'on' if active_amp else 'off'}")

    for epoch in range(exp_cfg.epochs):
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
            # Save best checkpoint
            os.makedirs(save_dir, exist_ok=True)
            ckpt_path = os.path.join(save_dir, f"{exp_cfg.name}_best.pt")
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'scheduler_state_dict': scheduler.state_dict(),
                'best_acc': best_acc,
                'exp_cfg': asdict(exp_cfg),
                'amp_enabled': active_amp,
                'scaler_state_dict': scaler.state_dict() if scaler.is_enabled() else None,
            }, ckpt_path)

        if verbose and (epoch % 20 == 0 or epoch == exp_cfg.epochs - 1):
            elapsed = time.time() - t_start
            print(f"  Epoch {epoch:3d}/{exp_cfg.epochs}: "
                  f"train_loss={train_loss:.4f}, train_acc={train_acc:.2f}%, "
                  f"test_acc={test_acc:.2f}% (best={best_acc:.2f}%), "
                  f"lr={optimizer.param_groups[0]['lr']:.6f}, "
                  f"time={elapsed:.0f}s")

    elapsed_total = time.time() - t_start
    print(f"  Finished in {elapsed_total:.0f}s. Best test accuracy: {best_acc:.2f}%")

    # Final evaluation with noise (multiple runs for Monte Carlo if noise enabled)
    if exp_cfg.noise_enabled and exp_cfg.sigma_c2c > 0:
        print(f"  Running Monte Carlo evaluation (10 runs)...")
        # Load best checkpoint
        ckpt = torch.load(os.path.join(save_dir, f"{exp_cfg.name}_best.pt"),
                          weights_only=False)
        model.load_state_dict(ckpt['model_state_dict'])

        mc_accs = []
        for i in range(10):
            _, acc = evaluate(model, testloader, criterion, device, exp_cfg, amp_enabled=active_amp)
            mc_accs.append(acc)
        mc_mean = sum(mc_accs) / len(mc_accs)
        mc_std = (sum((a - mc_mean)**2 for a in mc_accs) / len(mc_accs)) ** 0.5
        print(f"  Monte Carlo: {mc_mean:.2f}% ± {mc_std:.2f}%")
    else:
        mc_mean = best_acc
        mc_std = 0.0

    result = {
        'experiment': exp_id,
        'name': exp_cfg.name,
        'n_states': exp_cfg.n_states,
        'sigma_c2c': exp_cfg.sigma_c2c,
        'sigma_d2d': exp_cfg.sigma_d2d,
        'hat_training': exp_cfg.hat_training,
        'best_test_acc': best_acc,
        'mc_mean_acc': mc_mean,
        'mc_std_acc': mc_std,
        'total_time_s': elapsed_total,
        'epochs': exp_cfg.epochs,
    }

    return result, history


# ─────────────────────────────────────────────
# Results Export
# ─────────────────────────────────────────────

def export_results(all_results: list, all_histories: dict,
                   output_dir: str = 'report_md'):
    """Export experiment results to CSV, JSON, and Markdown."""
    os.makedirs(output_dir, exist_ok=True)

    # CSV
    csv_path = asset_path(output_dir, 'csv', 'resnet18_results.csv')
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=all_results[0].keys())
        writer.writeheader()
        writer.writerows(all_results)

    # JSON (results + histories)
    json_path = asset_path(output_dir, 'json', 'resnet18_results.json')
    with open(json_path, 'w') as f:
        json.dump({
            'results': all_results,
            'histories': {k: v for k, v in all_histories.items()},
        }, f, indent=2)

    # Markdown report
    md_path = os.path.join(output_dir, 'resnet18_experiment_report.md')
    with open(md_path, 'w') as f:
        f.write("# A2.1: ResNet-18 Full Pipeline Validation on CIFAR-10\n\n")

        f.write("## Experiment Matrix Results\n\n")
        f.write("| Exp | Config | Quant | C2C | D2D | Training | "
                "Best Acc | MC Mean±Std |\n")
        f.write("|:---:|:-------|:-----:|:---:|:---:|:--------:|"
                ":-------:|:-----------:|\n")

        for r in all_results:
            quant = 'FP32' if not r.get('hat_training') and r['sigma_c2c'] == 0 and r['n_states'] == 16 and r['experiment'] == 'R1' else f"{r['n_states']}L"
            if r['experiment'] == 'R1':
                quant = 'FP32'
            training = 'HAT' if r['hat_training'] else 'Standard'
            mc_str = f"{r['mc_mean_acc']:.2f}±{r['mc_std_acc']:.2f}"
            f.write(f"| {r['experiment']} | {r['name']} | {quant} | "
                    f"{r['sigma_c2c']} | {r['sigma_d2d']} | {training} | "
                    f"{r['best_test_acc']:.2f}% | {mc_str}% |\n")

        f.write("\n## Key Comparisons\n\n")
        results_map = {r['experiment']: r for r in all_results}
        comparisons = [
            ('R1', 'R2', 'Pure quantization loss'),
            ('R2', 'R3', 'Noise degradation'),
            ('R3', 'R4', 'HAT recovery (core result)'),
            ('R4', 'R5', 'Pessimistic scenario survival'),
            ('R4', 'R6', 'Bit-width sensitivity'),
        ]
        f.write("| Comparison | Δ Accuracy | Interpretation |\n")
        f.write("|:-----------|:----------:|:---------------|\n")
        for a, b, desc in comparisons:
            if a in results_map and b in results_map:
                delta = results_map[b]['best_test_acc'] - results_map[a]['best_test_acc']
                sign = '+' if delta >= 0 else ''
                f.write(f"| {a}→{b} | {sign}{delta:.2f}% | {desc} |\n")

    print(f"\nResults exported to:")
    print(f"  CSV:      {csv_path}")
    print(f"  JSON:     {json_path}")
    print(f"  Markdown: {md_path}")


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="A2.1: ResNet-18 Experiments on CIFAR-10")
    parser.add_argument("--experiments", nargs='+', default=None,
                        help="Which experiments to run (e.g., R1 R4). Default: all")
    parser.add_argument("--dataset", type=str, choices=["cifar10", "cifar100"], default="cifar10")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--epochs", type=int, default=200,
                        help="Training epochs (default: 200)")
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--device", type=str, default=None)
    parser.add_argument("--data-root", type=str, default="./data")
    parser.add_argument("--save-dir", type=str, default="checkpoints")
    parser.add_argument("--output-dir", type=str, default="report_md")
    parser.add_argument("--amp", action="store_true",
                        help="Enable AMP mixed precision on CUDA. Omit to preserve previous full-precision behavior.")
    args = parser.parse_args()

    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")
    print(f"Dataset: {args.dataset}")
    print(f"Seed: {args.seed}")
    print(f"Epochs: {args.epochs}")
    print(f"AMP requested: {args.amp}, active: {amp_enabled_for_device(args.amp, device)}")

    # Get experiment configs
    configs = get_experiment_configs(epochs=args.epochs)

    # Filter experiments if specified
    if args.experiments:
        configs = {k: v for k, v in configs.items() if k in args.experiments}
    print(f"Experiments to run: {list(configs.keys())}")

    # Override batch size
    for cfg in configs.values():
        cfg.batch_size = args.batch_size

    # Run experiments
    all_results = []
    all_histories = {}

    for exp_id, exp_cfg in configs.items():
        result, history = run_experiment(
            exp_id, exp_cfg, device,
            dataset=args.dataset,
            seed=args.seed,
            data_root=args.data_root,
            save_dir=args.save_dir,
            amp_enabled=args.amp,
        )
        all_results.append(result)
        all_histories[exp_id] = history

    # Export
    print("\n" + "=" * 70)
    print("All experiments complete. Exporting results...")
    print("=" * 70)
    export_results(all_results, all_histories, output_dir=args.output_dir)

    # Final summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    for r in all_results:
        print(f"  {r['experiment']:3s} ({r['name']:30s}): "
              f"best={r['best_test_acc']:.2f}%, "
              f"MC={r['mc_mean_acc']:.2f}±{r['mc_std_acc']:.2f}%")


if __name__ == "__main__":
    main()
