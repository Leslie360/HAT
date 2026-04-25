#!/usr/bin/env python3
"""
Layer-Wise Write Nonlinearity (NL) Sensitivity Analysis

Addresses Major Comment #2: NL=2.0 impact on different ViT modules

Experiments:
Inject NL=2.0 into specific layers while keeping others linear (NL=1.0)
Identify which architectural components are most sensitive to write nonlinearity.

Target modules:
- Patch embedding (conv)
- QKV projections (attention input)
- Attention output projection
- MLP layers (feed-forward)
"""

import torch
import torch.nn as nn
import numpy as np
import json
import os
import sys
from dataclasses import dataclass
from typing import List, Tuple

sys.stdout.reconfigure(line_buffering=True)

import torchvision
import torchvision.transforms as transforms
import timm

from analog_layers import (
    AnalogConv2d, AnalogLinear, AnalogLinearConfig,
    convert_to_hybrid
)


@dataclass
class ExperimentConfig:
    name: str
    n_states: int = 16
    sigma_c2c: float = 0.05
    sigma_d2d: float = 0.10
    noise_enabled: bool = True
    # NL configuration: which layers get NL=2.0
    nl_patches: float = 1.0  # Patch embedding
    nl_qkv: float = 1.0      # QKV projections
    nl_attn_out: float = 1.0 # Attention output
    nl_mlp: float = 1.0      # MLP layers
    nl_default: float = 1.0  # All other layers


def get_cifar10_loader(batch_size=256, train=False):
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])
    dataset = torchvision.datasets.CIFAR10(root='./data', train=train, download=True, transform=transform)
    loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=train, num_workers=4)
    return loader


def build_model_with_layer_nl(exp_cfg: ExperimentConfig, num_classes: int = 10, device: str = 'cuda'):
    """
    Build model with layer-specific NL configuration.
    
    This function creates separate AnalogLinearConfig for different layer types
    to enable layer-wise NL sensitivity analysis.
    """
    model = timm.create_model("tiny_vit_5m_224", pretrained=False, num_classes=num_classes)
    
    # Base config
    base_cfg = AnalogLinearConfig(
        n_states=exp_cfg.n_states,
        sigma_c2c=exp_cfg.sigma_c2c,
        sigma_d2d=exp_cfg.sigma_d2d,
        noise_enabled=exp_cfg.noise_enabled,
        NL_LTP=exp_cfg.nl_default,
        NL_LTD=-exp_cfg.nl_default,
        restore_weight_scale=True,
    )
    
    # Convert to hybrid with base config first
    model = convert_to_hybrid(model, config=base_cfg, verbose=False)
    
    # Now modify specific layers based on their type/position
    for name, module in model.named_modules():
        if isinstance(module, (AnalogLinear, AnalogConv2d)):
            # Determine layer type from name
            if 'patch_embed' in name or 'stem' in name:
                # Patch embedding
                module.config.NL_LTP = exp_cfg.nl_patches
                module.config.NL_LTD = -exp_cfg.nl_patches
            elif 'qkv' in name:
                # QKV projections
                module.config.NL_LTP = exp_cfg.nl_qkv
                module.config.NL_LTD = -exp_cfg.nl_qkv
            elif 'attn' in name and 'proj' in name:
                # Attention output projection
                module.config.NL_LTP = exp_cfg.nl_attn_out
                module.config.NL_LTD = -exp_cfg.nl_attn_out
            elif 'mlp' in name:
                # MLP layers
                module.config.NL_LTP = exp_cfg.nl_mlp
                module.config.NL_LTD = -exp_cfg.nl_mlp
    
    return model.to(device)


def get_layer_type_stats(model) -> dict:
    """Get statistics of layer types and their NL values."""
    stats = {
        'patch_embed': [],
        'qkv': [],
        'attn_out': [],
        'mlp': [],
        'other': []
    }
    
    for name, module in model.named_modules():
        if isinstance(module, (AnalogLinear, AnalogConv2d)):
            nl_val = module.config.NL_LTP
            if 'patch_embed' in name or 'stem' in name:
                stats['patch_embed'].append((name, nl_val))
            elif 'qkv' in name:
                stats['qkv'].append((name, nl_val))
            elif 'attn' in name and 'proj' in name:
                stats['attn_out'].append((name, nl_val))
            elif 'mlp' in name:
                stats['mlp'].append((name, nl_val))
            else:
                stats['other'].append((name, nl_val))
    
    return stats


def evaluate_model(model, loader, criterion, device, num_runs=10):
    """Evaluate with MC sampling."""
    model.eval()
    accuracies = []
    
    for run in range(num_runs):
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
        'max': float(np.max(accuracies))
    }


def run_baseline_linear(checkpoint_path, device='cuda'):
    """Baseline: All layers linear (NL=1.0)."""
    print("\n" + "="*70)
    print("Baseline: All Linear (NL=1.0 everywhere)")
    print("="*70)
    
    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    exp_cfg = ExperimentConfig(name="baseline_linear")
    
    model = build_model_with_layer_nl(exp_cfg, num_classes=10, device=device)
    model.load_state_dict(ckpt['model_state_dict'])
    
    loader = get_cifar10_loader(batch_size=256, train=False)
    criterion = nn.CrossEntropyLoss()
    
    results = evaluate_model(model, loader, criterion, device, num_runs=10)
    print(f"  Accuracy: {results['mean']:.2f}% ± {results['std']:.2f}%")
    
    return results


def run_global_nl2(checkpoint_path, device='cuda'):
    """Global NL=2.0: All layers nonlinear."""
    print("\n" + "="*70)
    print("Global NL=2.0: All layers")
    print("="*70)
    
    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    exp_cfg = ExperimentConfig(
        name="global_nl2",
        nl_patches=2.0,
        nl_qkv=2.0,
        nl_attn_out=2.0,
        nl_mlp=2.0,
        nl_default=2.0
    )
    
    model = build_model_with_layer_nl(exp_cfg, num_classes=10, device=device)
    model.load_state_dict(ckpt['model_state_dict'])
    
    loader = get_cifar10_loader(batch_size=256, train=False)
    criterion = nn.CrossEntropyLoss()
    
    results = evaluate_model(model, loader, criterion, device, num_runs=10)
    print(f"  Accuracy: {results['mean']:.2f}% ± {results['std']:.2f}%")
    
    return results


def run_layer_ablations(checkpoint_path, device='cuda'):
    """Ablate each layer type individually."""
    ablations = [
        ('patch_embed', 'Patch Embedding only NL=2.0'),
        ('qkv', 'QKV Projections only NL=2.0'),
        ('attn_out', 'Attention Output only NL=2.0'),
        ('mlp', 'MLP layers only NL=2.0'),
    ]
    
    results = {}
    
    for layer_type, description in ablations:
        print("\n" + "="*70)
        print(f"Ablation: {description}")
        print("="*70)
        
        ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
        
        # Create config with only this layer type at NL=2.0
        exp_cfg = ExperimentConfig(name=f"nl2_{layer_type}")
        
        if layer_type == 'patch_embed':
            exp_cfg.nl_patches = 2.0
        elif layer_type == 'qkv':
            exp_cfg.nl_qkv = 2.0
        elif layer_type == 'attn_out':
            exp_cfg.nl_attn_out = 2.0
        elif layer_type == 'mlp':
            exp_cfg.nl_mlp = 2.0
        
        model = build_model_with_layer_nl(exp_cfg, num_classes=10, device=device)
        model.load_state_dict(ckpt['model_state_dict'])
        
        # Verify layer configuration
        stats = get_layer_type_stats(model)
        for ltype, layers in stats.items():
            if layers:
                nl_vals = [nl for _, nl in layers]
                print(f"  {ltype}: {len(layers)} layers, NL={set(nl_vals)}")
        
        loader = get_cifar10_loader(batch_size=256, train=False)
        criterion = nn.CrossEntropyLoss()
        
        res = evaluate_model(model, loader, criterion, device, num_runs=10)
        print(f"  Accuracy: {res['mean']:.2f}% ± {res['std']:.2f}%")
        
        results[layer_type] = res
    
    return results


def main():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Device: {device}")
    
    checkpoint_path = 'checkpoints/V4_hybrid_standard_noise_hat_best.pt'
    
    if not os.path.exists(checkpoint_path):
        print(f"WARNING: {checkpoint_path} not found, trying ensemble checkpoint...")
        checkpoint_path = 'checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt'
    
    if not os.path.exists(checkpoint_path):
        print("ERROR: No suitable checkpoint found")
        sys.exit(1)
    
    print(f"Using checkpoint: {checkpoint_path}")
    
    final_results = {}
    
    # 1. Baseline (all linear)
    final_results['baseline_linear'] = run_baseline_linear(checkpoint_path, device)
    
    # 2. Global NL=2.0
    final_results['global_nl2'] = run_global_nl2(checkpoint_path, device)
    
    # 3. Layer-wise ablations
    final_results.update(run_layer_ablations(checkpoint_path, device))
    
    # Summary
    print("\n" + "="*70)
    print("LAYER-WISE NL SENSITIVITY SUMMARY")
    print("="*70)
    
    baseline = final_results['baseline_linear']['mean']
    
    print(f"\n{'Configuration':<30} {'Accuracy':<15} {'Degradation':<15}")
    print("-" * 60)
    
    for key, res in final_results.items():
        acc = res['mean']
        deg = baseline - acc
        print(f"{key:<30} {acc:>6.2f}%        {deg:>6.2f} pp")
    
    # Rank by sensitivity
    print("\nSensitivity Ranking (most to least sensitive):")
    sensitivities = []
    for key, res in final_results.items():
        if key != 'baseline_linear':
            deg = baseline - res['mean']
            sensitivities.append((key, deg))
    
    sensitivities.sort(key=lambda x: x[1], reverse=True)
    for i, (key, deg) in enumerate(sensitivities, 1):
        print(f"  {i}. {key}: {deg:.2f} pp degradation")
    
    # Save results
    output = {
        'experiment': 'Layer-Wise NL Sensitivity',
        'checkpoint': checkpoint_path,
        'results': final_results,
        'sensitivity_ranking': [{k: v} for k, v in sensitivities],
        'interpretation': {
            'key_finding': 'Identifies which ViT modules are most sensitive to write nonlinearity',
            'methodology': 'Layer-specific NL injection while keeping others linear'
        }
    }
    
    output_path = 'report_md/_gpt/layer_wise_nl_sensitivity_results.json'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults saved to: {output_path}")


if __name__ == '__main__':
    main()
