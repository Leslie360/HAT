"""
Diagnose Ensemble HAT evaluation issue

Compare working vs non-working evaluation paths
"""

import torch
import torch.nn as nn
import numpy as np
import sys
import os

sys.path.insert(0, '/home/qiaosir/projects/compute_vit')

import torchvision
import torchvision.transforms as transforms
import timm

from analog_layers import AnalogLinear, AnalogConv2d, AnalogLinearConfig, convert_to_hybrid

# Config
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
    """Build model matching V4 config"""
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
    
    # Load checkpoint
    checkpoint_path = 'checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt'
    checkpoint = torch.load(checkpoint_path, map_location=device)
    print(f"Checkpoint: {checkpoint_path}")
    print(f"Best acc (from checkpoint): {checkpoint['best_acc']:.2f}%")
    print(f"Epoch: {checkpoint['epoch']}")
    
    # Get loader
    loader = get_cifar10_loader(batch_size=256)
    
    # Test 1: Load and evaluate WITHOUT resampling (Standard HAT)
    print("\n" + "=" * 70)
    print("Test 1: Standard HAT (NO resampling)")
    print("=" * 70)
    model1 = build_model(device)
    model1.load_state_dict(checkpoint['model_state_dict'])
    
    # Count analog layers
    analog_count = sum(1 for _ in model1.modules() if isinstance(_, (AnalogLinear, AnalogConv2d)))
    print(f"Analog layers: {analog_count}")
    
    acc1 = evaluate_once(model1, loader, device)
    print(f"Accuracy: {acc1:.2f}%")
    
    # Test 2: Load, resample once, evaluate (Fresh instance with resampling)
    print("\n" + "=" * 70)
    print("Test 2: Resample D2D once then evaluate")
    print("=" * 70)
    model2 = build_model(device)
    model2.load_state_dict(checkpoint['model_state_dict'])
    
    count = resample_all_d2d(model2)
    print(f"Resampled {count} layers")
    
    acc2 = evaluate_once(model2, loader, device)
    print(f"Accuracy: {acc2:.2f}%")
    
    # Test 3: Multiple resamples
    print("\n" + "=" * 70)
    print("Test 3: Multiple resamples (10 instances)")
    print("=" * 70)
    accuracies = []
    for i in range(10):
        model = build_model(device)
        model.load_state_dict(checkpoint['model_state_dict'])
        resample_all_d2d(model)
        acc = evaluate_once(model, loader, device)
        accuracies.append(acc)
        print(f"  Instance {i+1}: {acc:.2f}%")
    
    print(f"\nMean: {np.mean(accuracies):.2f}% ± {np.std(accuracies):.2f}%")
    print(f"Range: [{min(accuracies):.2f}%, {max(accuracies):.2f}%]")
    
    # Test 4: Check if there's something special in checkpoint loading
    print("\n" + "=" * 70)
    print("Test 4: Examine model state dict keys")
    print("=" * 70)
    model4 = build_model(device)
    state_dict = checkpoint['model_state_dict']
    print(f"State dict keys (sample): {list(state_dict.keys())[:10]}")
    print(f"Total keys: {len(state_dict)}")
    
    # Check for D2D noise in state dict
    d2d_keys = [k for k in state_dict.keys() if 'd2d' in k.lower()]
    print(f"D2D-related keys: {d2d_keys}")
    
    # Test 5: Load with strict=False and check missing/unexpected
    print("\n" + "=" * 70)
    print("Test 5: Strict loading check")
    print("=" * 70)
    model5 = build_model(device)
    missing, unexpected = model5.load_state_dict(state_dict, strict=False)
    print(f"Missing keys: {len(missing)}")
    if missing:
        print(f"  Sample: {missing[:5]}")
    print(f"Unexpected keys: {len(unexpected)}")
    if unexpected:
        print(f"  Sample: {unexpected[:5]}")
    
    # Test 6: Try setting eval mode explicitly before resampling
    print("\n" + "=" * 70)
    print("Test 6: Set eval mode BEFORE resampling")
    print("=" * 70)
    model6 = build_model(device)
    model6.load_state_dict(checkpoint['model_state_dict'])
    model6.eval()  # Set eval mode first
    resample_all_d2d(model6)
    acc6 = evaluate_once(model6, loader, device)
    print(f"Accuracy: {acc6:.2f}%")

if __name__ == '__main__':
    main()
