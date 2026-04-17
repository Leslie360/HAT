"""
SVHN Training for Framework Generality Validation

SVHN = Street View House Numbers
- 10 classes (digits 0-9)
- 32x32 images (same as CIFAR-10)
- Different distribution (street view vs natural images)
- Validates cross-domain generalization
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import sys

sys.path.insert(0, '/home/qiaosir/projects/compute_vit')
sys.stdout.reconfigure(line_buffering=True)

import torchvision
import torchvision.transforms as transforms
import timm

from train_tinyvit import (
    build_model, get_dataloaders, evaluate, set_seed
)

# Add SVHN to DATASET_STATS temporarily
def add_svhn_support():
    """Add SVHN to train_tinyvit's DATASET_STATS"""
    from train_tinyvit import DATASET_STATS
    
    DATASET_STATS['svhn'] = {
        'num_classes': 10,
        'mean': (0.5, 0.5, 0.5),  # SVHN approx mean
        'std': (0.5, 0.5, 0.5),   # SVHN approx std
        'dataset_cls': torchvision.datasets.SVHN,
        'split_style': 'svhn',  # Special handling needed
    }
    return DATASET_STATS

def get_svhn_loaders(batch_size=256, num_workers=4):
    """Get SVHN train/test loaders"""
    transform_train = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
    ])
    transform_test = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
    ])
    
    trainset = torchvision.datasets.SVHN(
        root='./data', split='train', download=True, transform=transform_train)
    trainloader = torch.utils.data.DataLoader(
        trainset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    
    testset = torchvision.datasets.SVHN(
        root='./data', split='test', download=True, transform=transform_test)
    testloader = torch.utils.data.DataLoader(
        testset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    
    return trainloader, testloader

# Monkey patch get_dataloaders for SVHN
original_get_dataloaders = None

def patched_get_dataloaders(dataset='cifar10', batch_size=256):
    if dataset == 'svhn':
        return get_svhn_loaders(batch_size=batch_size)
    # Fall back to original for other datasets
    import train_tinyvit
    return original_get_dataloaders(dataset, batch_size)

def train_svhn(model, trainloader, testloader, device, epochs=50, lr=0.001):
    """Train SVHN with HAT"""
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=0.05)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    
    best_acc = 0.0
    
    for epoch in range(epochs):
        # Training
        model.train()
        # Resample D2D for Ensemble HAT
        for m in model.modules():
            if hasattr(m, 'resample_d2d_noise') and callable(m.resample_d2d_noise):
                m.resample_d2d_noise()
        
        train_loss = 0
        correct = 0
        total = 0
        
        for inputs, targets in trainloader:
            inputs, targets = inputs.to(device), targets.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()
        
        train_acc = 100.0 * correct / total
        
        # Evaluation
        model.eval()
        test_correct = 0
        test_total = 0
        
        with torch.no_grad():
            for inputs, targets in testloader:
                inputs, targets = inputs.to(device), targets.to(device)
                outputs = model(inputs)
                _, predicted = outputs.max(1)
                test_total += targets.size(0)
                test_correct += predicted.eq(targets).sum().item()
        
        test_acc = 100.0 * test_correct / test_total
        best_acc = max(best_acc, test_acc)
        
        scheduler.step()
        
        if (epoch + 1) % 5 == 0:
            print(f"  Epoch {epoch+1}/{epochs}: Train={train_acc:.2f}%, Test={test_acc:.2f}%, Best={best_acc:.2f}%")
    
    return best_acc

def main():
    set_seed(42)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    print("="*70)
    print("SVHN Training (Cross-Domain Validation)")
    print("="*70)
    print(f"Device: {device}")
    print("\nSVHN: Street View House Numbers")
    print("  - 10 classes (digits 0-9)")
    print("  - 32x32 images")
    print("  - Different from CIFAR-10 (street view vs natural)")
    
    # Setup SVHN support
    add_svhn_support()
    
    # Import after adding SVHN
    from train_tinyvit import TinyViTExperimentConfig
    from dataclasses import dataclass
    
    # V4 config for SVHN
    cfg = TinyViTExperimentConfig(
        name='SVHN_HAT',
        use_hybrid=True,
        n_states=16,
        sigma_c2c=0.05,
        sigma_d2d=0.10,
        noise_enabled=True,
        hat_training=True,
        epochs=50,
        lr=0.001,
    )
    
    # Build model
    print(f"\nBuilding Tiny-ViT for SVHN...")
    model = build_model(cfg, num_classes=10, device=device)
    
    # Get data
    print(f"\nLoading SVHN dataset...")
    trainloader, testloader = get_svhn_loaders(batch_size=256)
    print(f"  Train: {len(trainloader.dataset)} images")
    print(f"  Test: {len(testloader.dataset)} images")
    
    # Train
    print(f"\nTraining SVHN with Ensemble HAT...")
    print(f"  Epochs: {cfg.epochs}, LR: {cfg.lr}")
    best_acc = train_svhn(model, trainloader, testloader, device, epochs=cfg.epochs, lr=cfg.lr)
    
    # Final evaluation
    print(f"\nFinal evaluation on SVHN test set...")
    criterion = nn.CrossEntropyLoss()
    
    # Eval with noise
    from train_tinyvit import set_noise_for_eval
    set_noise_for_eval(model, cfg)
    
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, targets in testloader:
            inputs, targets = inputs.to(device), targets.to(device)
            outputs = model(inputs)
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()
    
    final_acc = 100.0 * correct / total
    
    print(f"\n" + "="*70)
    print("RESULTS")
    print("="*70)
    print(f"SVHN Best Accuracy: {best_acc:.2f}%")
    print(f"SVHN Final Accuracy: {final_acc:.2f}%")
    print(f"CIFAR-10 V4 Reference: 86.37%")
    print(f"\nExpected SVHN: ~90-95% (simpler task than CIFAR-10)")
    
    # Save results
    import json
    from datetime import datetime
    results = {
        'experiment': 'SVHN Training (Cross-Domain Validation)',
        'date': datetime.now().isoformat(),
        'best_accuracy': float(best_acc),
        'final_accuracy': float(final_acc),
        'training_epochs': cfg.epochs,
        'dataset': 'SVHN',
        'classes': 10,
        'note': 'Cross-domain validation (street view vs natural)'
    }
    
    with open('report_md/_gpt/svhn_training_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved: report_md/_gpt/svhn_training_results.json")

if __name__ == '__main__':
    main()
