"""
Flowers-102 Training for Framework Generality Validation

Flowers-102 = Oxford 102 Category Flower Dataset
- 102 flower categories
- Variable image sizes (typically ~500x500)
- Resized to 224x224 for Tiny-ViT
- Validates fine-grained classification with many classes
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import sys

from repo_bootstrap import ensure_repo_root

ensure_repo_root()
sys.stdout.reconfigure(line_buffering=True)

import torchvision
import torchvision.transforms as transforms

from train_tinyvit import (
    build_model, evaluate, set_seed, set_noise_for_train
)

# Define set_noise_for_eval if not available
def set_noise_for_eval(model, exp_cfg):
    """Set noise for evaluation (same as train for HAT)"""
    from analog_layers import AnalogLinear, AnalogConv2d
    for m in model.modules():
        if isinstance(m, (AnalogLinear, AnalogConv2d)):
            m.config.noise_enabled = exp_cfg.noise_enabled
            m.config.sigma_c2c = exp_cfg.sigma_c2c
            m.config.sigma_d2d = exp_cfg.sigma_d2d

def get_flowers102_loaders(batch_size=64, num_workers=4):
    """Get Flowers-102 train/test loaders"""
    # Flowers-102 uses 224x224 (same as ImageNet/Tiny-ViT default)
    transform_train = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ])
    transform_test = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    ])
    
    # Flowers-102: train+val for training, test for evaluation
    trainset = torchvision.datasets.Flowers102(
        root='./data', split='train', download=True, transform=transform_train)
    valset = torchvision.datasets.Flowers102(
        root='./data', split='val', download=True, transform=transform_train)
    
    # Combine train and val
    trainset = torch.utils.data.ConcatDataset([trainset, valset])
    trainloader = torch.utils.data.DataLoader(
        trainset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    
    testset = torchvision.datasets.Flowers102(
        root='./data', split='test', download=True, transform=transform_test)
    testloader = torch.utils.data.DataLoader(
        testset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    
    return trainloader, testloader

def train_flowers102(model, trainloader, testloader, device, epochs=50, lr=0.0001):
    """Train Flowers-102 with HAT"""
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
    print("Flowers-102 Training (Fine-grained Classification)")
    print("="*70)
    print(f"Device: {device}")
    print("\nFlowers-102: Oxford 102 Category Flower Dataset")
    print("  - 102 classes (fine-grained)")
    print("  - 224x224 images (ImageNet size)")
    print("  - Tests many-class classification capability")
    
    # Import after setup
    from train_tinyvit import TinyViTExperimentConfig
    
    # Config (lower LR for fine-grained)
    cfg = TinyViTExperimentConfig(
        name='Flowers102_HAT',
        use_hybrid=True,
        n_states=16,
        sigma_c2c=0.05,
        sigma_d2d=0.10,
        noise_enabled=True,
        hat_training=True,
        epochs=50,
        lr=0.0001,
    )
    
    # Build model
    print(f"\nBuilding Tiny-ViT for Flowers-102...")
    model = build_model(cfg, num_classes=102, device=device)
    
    # Get data
    print(f"\nLoading Flowers-102 dataset...")
    trainloader, testloader = get_flowers102_loaders(batch_size=64)
    print(f"  Train: {len(trainloader.dataset)} images")
    print(f"  Test: {len(testloader.dataset)} images")
    
    # Train
    print(f"\nTraining Flowers-102 with Ensemble HAT...")
    print(f"  Epochs: {cfg.epochs}, LR: {cfg.lr}")
    best_acc = train_flowers102(model, trainloader, testloader, device, epochs=cfg.epochs, lr=cfg.lr)
    
    # Final evaluation
    print(f"\nFinal evaluation on Flowers-102 test set...")
    criterion = nn.CrossEntropyLoss()
    
    # Eval with noise (use local set_noise_for_eval)
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
    print(f"Flowers-102 Best Accuracy: {best_acc:.2f}%")
    print(f"Flowers-102 Final Accuracy: {final_acc:.2f}%")
    print(f"CIFAR-10 V4 Reference: 86.37%")
    print(f"\nExpected Flowers-102: ~85-95% (fine-grained but simpler than CIFAR-100)")
    
    # Save results
    import json
    from datetime import datetime
    results = {
        'experiment': 'Flowers-102 Training (Fine-grained Classification)',
        'date': datetime.now().isoformat(),
        'best_accuracy': float(best_acc),
        'final_accuracy': float(final_acc),
        'training_epochs': cfg.epochs,
        'dataset': 'Flowers-102',
        'classes': 102,
        'note': 'Fine-grained classification with many classes'
    }
    
    with open('report_md/_gpt/flowers102_training_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved: report_md/_gpt/flowers102_training_results.json")

if __name__ == '__main__':
    main()
