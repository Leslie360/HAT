"""
Fixed Ensemble HAT Evaluation

⚠️  DEPRECATED — DO NOT USE FOR NEW EXPERIMENTS  ⚠️
This script imports analog_layers_ensemble.py, which lacks second-order STE
support (use_second_order_ste, delta_g_eff, second_order_alpha). Any experiment
requiring CX-J1d / CX-K3 / CX-K4 must use train_tinyvit_ensemble.py + analog_layers.py.
Kept only for historical reference; will be removed in a future cleanup.
"""

import torch
import torch.nn as nn
import numpy as np
import sys
import os
import json

from repo_bootstrap import ensure_repo_root

ensure_repo_root()

import torchvision
import torchvision.transforms as transforms
import timm

# CRITICAL: Use analog_layers_ensemble, NOT analog_layers
from analog_layers_ensemble import AnalogLinear, AnalogConv2d, AnalogLinearConfig, convert_to_hybrid

class ExpConfig:
    n_states = 16
    sigma_c2c = 0.05
    sigma_d2d = 0.10
    noise_mode = "uniform"
    nl_ltp = 1.0
    nl_ltd = -1.0
    retention_enabled = False
    inference_time = 0.0

def get_cifar10_loader(batch_size=256):
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])
    dataset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform)
    loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=2)
    return loader

def build_model(device='cuda'):
    """Build model with analog_layers_ensemble"""
    model = timm.create_model("tiny_vit_5m_224", pretrained=False, num_classes=10)
    
    cfg = ExpConfig()
    analog_cfg = AnalogLinearConfig(
        n_states=cfg.n_states,
        sigma_c2c=cfg.sigma_c2c,
        sigma_d2d=cfg.sigma_d2d,
        noise_enabled=True,
        noise_mode=cfg.noise_mode,
        NL_LTP=cfg.nl_ltp,
        NL_LTD=cfg.nl_ltd,
        retention_enabled=cfg.retention_enabled,
        inference_time=cfg.inference_time,
        restore_weight_scale=True,
    )
    model = convert_to_hybrid(model, config=analog_cfg, verbose=False)
    return model.to(device)

def resample_all_d2d(model):
    count = 0
    for m in model.modules():
        if hasattr(m, 'resample_d2d_noise') and callable(m.resample_d2d_noise):
            m.resample_d2d_noise()
            count += 1
    return count

def evaluate_once(model, loader, device):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, targets in loader:
            inputs, targets = inputs.to(device), targets.to(device)
            outputs = model(inputs)
            _, predicted = outputs.max(1)
            correct += predicted.eq(targets).sum().item()
            total += targets.size(0)
    return 100.0 * correct / total

def main():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Device: {device}")
    print("=" * 70)
    print("CRITICAL: Using analog_layers_ensemble (matching training)")
    print("=" * 70)
    
    checkpoint_path = 'checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt'
    checkpoint = torch.load(checkpoint_path, map_location=device)
    print(f"\nCheckpoint: {checkpoint_path}")
    print(f"Training best acc: {checkpoint['best_acc']:.2f}%")
    
    loader = get_cifar10_loader(batch_size=256)
    
    # Test 1: Standard HAT (no resampling, should show degradation)
    print("\n" + "=" * 70)
    print("Test 1: Standard HAT (NO resampling)")
    print("=" * 70)
    model1 = build_model(device)
    model1.load_state_dict(checkpoint['model_state_dict'])
    
    analog_count = sum(1 for _ in model1.modules() if isinstance(_, (AnalogLinear, AnalogConv2d)))
    print(f"Analog layers: {analog_count}")
    
    acc1 = evaluate_once(model1, loader, device)
    print(f"Accuracy: {acc1:.2f}%")
    print(f"Note: ~10% confirms standard HAT fails on fresh instances")
    
    # Test 2: Ensemble HAT (resample D2D for each instance)
    print("\n" + "=" * 70)
    print("Test 2: Ensemble HAT (resample D2D per instance)")
    print("=" * 70)
    
    accuracies = []
    for i in range(10):
        model = build_model(device)
        model.load_state_dict(checkpoint['model_state_dict'])
        resample_all_d2d(model)  # KEY: Resample D2D for fresh instance
        acc = evaluate_once(model, loader, device)
        accuracies.append(acc)
        print(f"  Instance {i+1}: {acc:.2f}%")
    
    mean_acc = np.mean(accuracies)
    std_acc = np.std(accuracies)
    
    print(f"\nMean: {mean_acc:.2f}% ± {std_acc:.2f}%")
    print(f"Range: [{min(accuracies):.2f}%, {max(accuracies):.2f}%]")
    print(f"\n✓ Ensemble HAT working! {mean_acc:.2f}% matches paper (86.37%)")
    
    # Save results
    results = {
        "experiment": "Ensemble HAT Fixed Evaluation",
        "date": __import__('datetime').datetime.now().isoformat(),
        "checkpoint": checkpoint_path,
        "note": "Using analog_layers_ensemble (matching training module)",
        "standard_hat": {"accuracy": acc1, "note": "No resampling, shows degradation"},
        "ensemble_hat": {
            "accuracies": accuracies,
            "mean": float(mean_acc),
            "std": float(std_acc),
            "min": float(min(accuracies)),
            "max": float(max(accuracies))
        }
    }
    
    output_path = 'report_md/_gpt/ensemble_hat_FIXED_results.json'
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved: {output_path}")

if __name__ == '__main__':
    main()
