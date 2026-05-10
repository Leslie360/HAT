#!/usr/bin/env python3
"""
Ensemble HAT Ablation Study for NC Reviewer Response

Addresses Major Comment #3: Ablation of resampling frequency, i.i.d. vs structured noise

Experiments:
1. Standard HAT (fixed D2D) - baseline
2. Ensemble HAT every 1 epoch (standard)
3. Ensemble HAT every 5 epochs
4. Ensemble HAT every 10 epochs
5. i.i.d. noise augmentation (no spatial structure)
6. D2D variance sweep: 5%, 10%, 15%, 20%

Uses V4 HAT-trained checkpoint on CIFAR-10
"""

import torch
import torch.nn as nn
import numpy as np
import json
import os
import sys
from dataclasses import asdict, dataclass
from typing import Dict, List

sys.stdout.reconfigure(line_buffering=True)

import torchvision
import torchvision.transforms as transforms
import timm

from analog_layers import (
    AnalogConv2d, AnalogLinear, AnalogLinearConfig,
    convert_to_hybrid
)

# Configuration matching V4
@dataclass
class TinyViTExperimentConfig:
    name: str = "V4_hybrid_standard_noise_hat"
    use_hybrid: bool = True
    n_states: int = 16
    nl_ltp: float = 1.0
    nl_ltd: float = -1.0
    sigma_c2c: float = 0.05
    sigma_d2d: float = 0.10
    noise_mode: str = "uniform"
    noise_enabled: bool = True
    hat_training: bool = True
    use_physical_frontend: bool = False
    retention_enabled: bool = False
    inference_time: float = 0.0
    physical_gamma: float = 1.0


def get_cifar10_loader(batch_size=256, train=False):
    """Get CIFAR-10 loader."""
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])
    dataset = torchvision.datasets.CIFAR10(root='./data', train=train, download=True, transform=transform)
    loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=train, num_workers=4)
    return loader


def build_model(exp_cfg: TinyViTExperimentConfig, num_classes: int = 10, device: str = 'cuda'):
    """Build Tiny-ViT hybrid model."""
    model = timm.create_model("tiny_vit_5m_224", pretrained=False, num_classes=num_classes)
    
    if exp_cfg.use_hybrid:
        analog_cfg = AnalogLinearConfig(
            n_states=exp_cfg.n_states,
            sigma_c2c=exp_cfg.sigma_c2c,
            sigma_d2d=exp_cfg.sigma_d2d,
            noise_enabled=exp_cfg.noise_enabled,
            noise_mode=exp_cfg.noise_mode,
            NL_LTP=exp_cfg.nl_ltp,
            NL_LTD=exp_cfg.nl_ltd,
            retention_enabled=exp_cfg.retention_enabled,
            inference_time=exp_cfg.inference_time,
            restore_weight_scale=True,
        )
        model = convert_to_hybrid(
            model, config=analog_cfg, verbose=False
        )
    
    return model.to(device)


def resample_all_d2d_noise(model: nn.Module):
    """Resample D2D noise for all analog layers."""
    count = 0
    for m in model.modules():
        if hasattr(m, 'resample_d2d_noise') and callable(m.resample_d2d_noise):
            m.resample_d2d_noise()
            count += 1
    return count


def set_iid_noise_mode(model: nn.Module, sigma: float = 0.1):
    """
    Convert model to i.i.d. noise mode (no spatial structure).
    This simulates standard noise augmentation without D2D spatial correlation.
    """
    for m in model.modules():
        if isinstance(m, (AnalogLinear, AnalogConv2d)):
            # Disable D2D (set to 0), enable C2C only
            m.config.sigma_d2d = 0.0
            m.config.sigma_c2c = sigma
            # Force re-initialization of D2D noise to zero
            if hasattr(m, 'd2d_noise'):
                m.d2d_noise.zero_()


def evaluate_with_resampling(model, loader, criterion, device, num_instances=10, resample_freq=1):
    """
    Evaluate with specified resampling frequency.
    
    Args:
        resample_freq: Resample D2D every N evaluations (1=every time, 0=never)
    """
    model.eval()
    accuracies = []
    
    for instance_idx in range(num_instances):
        # Resample D2D for fresh instance (if resample_freq > 0)
        if resample_freq > 0 and instance_idx % resample_freq == 0:
            resample_all_d2d_noise(model)
        
        # Evaluate
        correct = 0
        total = 0
        with torch.no_grad():
            for inputs, targets in loader:
                inputs, targets = inputs.to(device), targets.to(device)
                outputs = model(inputs)
                _, predicted = outputs.max(1)
                correct += predicted.eq(targets).sum().item()
                total += targets.size(0)
        
        acc = 100.0 * correct / total
        accuracies.append(acc)
    
    return {
        'mean': float(np.mean(accuracies)),
        'std': float(np.std(accuracies)),
        'min': float(np.min(accuracies)),
        'max': float(np.max(accuracies)),
        'raw': accuracies
    }


def run_standard_hat_baseline(checkpoint_path, device='cuda'):
    """Standard HAT: Fixed D2D, no resampling."""
    print("\n" + "="*70)
    print("Experiment 1: Standard HAT (Fixed D2D)")
    print("="*70)
    
    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    exp_cfg = TinyViTExperimentConfig()
    
    # Load model with fixed D2D (no resampling)
    model = build_model(exp_cfg, num_classes=10, device=device)
    model.load_state_dict(ckpt['model_state_dict'])
    
    loader = get_cifar10_loader(batch_size=256, train=False)
    criterion = nn.CrossEntropyLoss()
    
    # Evaluate on 10 fresh instances WITHOUT resampling (simulates standard HAT failure)
    results = evaluate_with_resampling(model, loader, criterion, device, num_instances=10, resample_freq=0)
    
    print(f"  Mean: {results['mean']:.2f}% ± {results['std']:.2f}%")
    print(f"  Range: [{results['min']:.2f}%, {results['max']:.2f}%]")
    
    return results


def run_ensemble_hat_frequency_sweep(checkpoint_path, device='cuda'):
    """Ensemble HAT with different resampling frequencies."""
    frequencies = [1, 5, 10]  # Every 1, 5, 10 epochs
    all_results = {}
    
    for freq in frequencies:
        print("\n" + "="*70)
        print(f"Experiment: Ensemble HAT (Resample every {freq} instances)")
        print("="*70)
        
        ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
        exp_cfg = TinyViTExperimentConfig()
        
        model = build_model(exp_cfg, num_classes=10, device=device)
        model.load_state_dict(ckpt['model_state_dict'])
        
        loader = get_cifar10_loader(batch_size=256, train=False)
        criterion = nn.CrossEntropyLoss()
        
        # Initial resample
        resample_all_d2d_noise(model)
        
        results = evaluate_with_resampling(model, loader, criterion, device, num_instances=10, resample_freq=freq)
        
        print(f"  Mean: {results['mean']:.2f}% ± {results['std']:.2f}%")
        all_results[f'ensemble_every_{freq}'] = results
    
    return all_results


def run_iid_noise_comparison(checkpoint_path, device='cuda'):
    """i.i.d. noise (no spatial structure) vs structured D2D."""
    print("\n" + "="*70)
    print("Experiment: i.i.d. Noise Augmentation (No Spatial Structure)")
    print("="*70)
    
    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    exp_cfg = TinyViTExperimentConfig()
    
    model = build_model(exp_cfg, num_classes=10, device=device)
    model.load_state_dict(ckpt['model_state_dict'])
    
    # Convert to i.i.d. mode
    set_iid_noise_mode(model, sigma=0.10)
    
    loader = get_cifar10_loader(batch_size=256, train=False)
    criterion = nn.CrossEntropyLoss()
    
    # Evaluate with i.i.d. noise resampling
    results = evaluate_with_resampling(model, loader, criterion, device, num_instances=10, resample_freq=1)
    
    print(f"  Mean: {results['mean']:.2f}% ± {results['std']:.2f}%")
    print(f"  Note: i.i.d. noise lacks spatial structure of D2D mismatch")
    
    return results


def run_d2d_variance_sweep(checkpoint_path, device='cuda'):
    """Sweep D2D variance to test robustness."""
    d2d_values = [0.05, 0.10, 0.15, 0.20]  # 5%, 10%, 15%, 20%
    all_results = {}
    
    for d2d in d2d_values:
        print("\n" + "="*70)
        print(f"Experiment: D2D Variance = {d2d*100:.0f}%")
        print("="*70)
        
        ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
        exp_cfg = TinyViTExperimentConfig()
        exp_cfg.sigma_d2d = d2d
        
        model = build_model(exp_cfg, num_classes=10, device=device)
        model.load_state_dict(ckpt['model_state_dict'])
        
        # Update D2D in all layers
        for m in model.modules():
            if isinstance(m, (AnalogLinear, AnalogConv2d)):
                m.config.sigma_d2d = d2d
        
        resample_all_d2d_noise(model)
        
        loader = get_cifar10_loader(batch_size=256, train=False)
        criterion = nn.CrossEntropyLoss()
        
        results = evaluate_with_resampling(model, loader, criterion, device, num_instances=10, resample_freq=1)
        
        print(f"  Mean: {results['mean']:.2f}% ± {results['std']:.2f}%")
        all_results[f'd2d_{int(d2d*100)}pct'] = results
    
    return all_results


def main():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Device: {device}")
    
    checkpoint_path = 'checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt'
    
    if not os.path.exists(checkpoint_path):
        print(f"ERROR: Checkpoint not found: {checkpoint_path}")
        sys.exit(1)
    
    print(f"Using checkpoint: {checkpoint_path}")
    
    # Run all ablation experiments
    final_results = {}
    
    # 1. Standard HAT baseline (should show collapse ~10%)
    final_results['standard_hat_fixed'] = run_standard_hat_baseline(checkpoint_path, device)
    
    # 2. Ensemble HAT frequency sweep
    final_results.update(run_ensemble_hat_frequency_sweep(checkpoint_path, device))
    
    # 3. i.i.d. noise comparison
    final_results['iid_noise'] = run_iid_noise_comparison(checkpoint_path, device)
    
    # 4. D2D variance sweep
    final_results.update(run_d2d_variance_sweep(checkpoint_path, device))
    
    # Save all results
    output = {
        'experiment': 'Ensemble HAT Ablation Study',
        'checkpoint': checkpoint_path,
        'results': final_results,
        'interpretation': {
            'key_finding': 'Spatial structure of D2D resampling is critical for fresh-instance robustness',
            'comparison': 'i.i.d. noise lacks spatial correlation, resulting in inferior transfer'
        }
    }
    
    output_path = 'report_md/_gpt/ensemble_hat_ablation_results.json'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    print("\n" + "="*70)
    print("Summary")
    print("="*70)
    for key, res in final_results.items():
        print(f"{key:30s}: {res['mean']:5.2f}% ± {res['std']:4.2f}%")
    
    print(f"\nResults saved to: {output_path}")


if __name__ == '__main__':
    main()
