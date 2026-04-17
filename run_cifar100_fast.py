"""
Fast CIFAR-100 Training using V4 Ensemble HAT backbone

Strategy: Load V4 backbone (frozen), only train classifier (100 classes)
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import sys
import dataclasses

sys.path.insert(0, '/home/qiaosir/projects/compute_vit')
sys.stdout.reconfigure(line_buffering=True)

import torchvision
import torchvision.transforms as transforms
import timm

from train_tinyvit import (
    build_model, get_dataloaders, evaluate,
    TinyViTExperimentConfig, DATASET_STATS, set_seed
)
from analog_layers import AnalogLinear, AnalogConv2d

def freeze_backbone(model):
    """Freeze all layers except classifier"""
    # Freeze all parameters
    for param in model.parameters():
        param.requires_grad = False
    
    # Unfreeze classifier
    if hasattr(model, 'head') and hasattr(model.head, 'fc'):
        for param in model.head.fc.parameters():
            param.requires_grad = True
        print("  Classifier unfrozen (backbone frozen)")
    
    return model

def train_classifier(model, trainloader, testloader, device, epochs=30, lr=0.01):
    """Train only the classifier"""
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(filter(lambda p: p.requires_grad, model.parameters()), 
                         lr=lr, momentum=0.9, weight_decay=5e-4)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    
    best_acc = 0.0
    
    for epoch in range(epochs):
        # Training
        model.train()
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
    print("CIFAR-100 Fast Training (V4 Backbone + New Classifier)")
    print("="*70)
    print(f"Device: {device}")
    
    # Load V4 checkpoint
    v4_path = 'checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt'
    print(f"\nLoading V4 backbone from: {v4_path}")
    
    ckpt = torch.load(v4_path, map_location=device, weights_only=False)
    print(f"  V4 CIFAR-10 accuracy: {ckpt.get('best_acc', 'N/A')}%")
    
    # Build model for CIFAR-100
    exp_cfg_dict = ckpt.get('exp_cfg', {})
    valid_keys = {f.name for f in dataclasses.fields(TinyViTExperimentConfig)}
    filtered = {k: v for k, v in exp_cfg_dict.items() if k in valid_keys}
    cfg = TinyViTExperimentConfig(**filtered)
    cfg.noise_enabled = True
    cfg.hat_training = True
    
    print(f"\nBuilding model for CIFAR-100...")
    model = build_model(cfg, num_classes=100, device=device)
    
    # Load backbone weights (skip classifier)
    state_dict = ckpt['model_state_dict']
    
    # Filter out classifier keys
    backbone_state = {k: v for k, v in state_dict.items() 
                     if not ('head.fc' in k or 'classifier' in k)}
    
    missing, unexpected = model.load_state_dict(backbone_state, strict=False)
    classifier_missing = [k for k in missing if 'head.fc' in k]
    print(f"  Loaded backbone: {len(backbone_state)} tensors")
    print(f"  Skipped classifier: {len(classifier_missing)} tensors")
    
    # Initialize new classifier
    if hasattr(model, 'head') and hasattr(model.head, 'fc'):
        nn.init.xavier_uniform_(model.head.fc.weight)
        nn.init.zeros_(model.head.fc.bias)
        print("  Classifier initialized")
    
    # Freeze backbone
    model = freeze_backbone(model)
    
    # Get data loaders
    print("\nLoading CIFAR-100...")
    trainloader, testloader = get_dataloaders('cifar100', batch_size=256)
    
    # Train classifier
    print(f"\nTraining classifier (backbone frozen)...")
    best_acc = train_classifier(model, trainloader, testloader, device, epochs=30, lr=0.01)
    
    # Final evaluation with analog noise
    print(f"\nFinal evaluation with analog noise...")
    criterion = nn.CrossEntropyLoss()
    _, final_acc = evaluate(model, testloader, criterion, device, cfg)
    
    print(f"\n" + "="*70)
    print("RESULTS")
    print("="*70)
    print(f"Best accuracy during training: {best_acc:.2f}%")
    print(f"Final accuracy (with noise): {final_acc:.2f}%")
    print(f"V4 CIFAR-10 reference: 86.37%")
    print(f"\nExpected CIFAR-100: ~65-75% (vs 86% on CIFAR-10)")
    
    # Save results
    import json
    from datetime import datetime
    results = {
        'experiment': 'CIFAR-100 Fast Training (V4 Backbone)',
        'date': datetime.now().isoformat(),
        'backbone': v4_path,
        'best_accuracy': float(best_acc),
        'final_accuracy': float(final_acc),
        'training_epochs': 30,
        'strategy': 'Frozen V4 backbone + trained classifier'
    }
    
    with open('report_md/_gpt/cifar100_fast_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved: report_md/_gpt/cifar100_fast_results.json")

if __name__ == '__main__':
    main()
