#!/usr/bin/env python3
"""
Spatial Correlation Ablation (Reviewer #4 W2)

Test: Spatially-correlated D2D vs i.i.d. noise
Question: Is spatial correlation necessary?
"""

import torch
import json
import time
from pathlib import Path
from train_tinyvit import build_model, TinyViTExperimentConfig, get_dataloaders, set_seed
import torch.nn as nn

def set_d2d_mode(model, mode='spatial'):
    """Set D2D noise mode."""
    from analog_layers import AnalogLinear, AnalogConv2d
    for m in model.modules():
        if isinstance(m, (AnalogLinear, AnalogConv2d)):
            m.config.spatial_d2d = (mode == 'spatial')

def train_with_spatial_mode(mode, epochs=50, lr=0.001):
    """Train with specified spatial mode."""
    print(f"\nTraining with D2D mode: {mode}")
    set_seed(42)
    
    trainloader, testloader = get_dataloaders('cifar10', batch_size=64, num_workers=2, data_root='./data')
    
    config = TinyViTExperimentConfig(
        name=f"spatial_{mode}",
        use_hybrid=True, n_states=16,
        sigma_c2c=0.05, sigma_d2d=0.10,
        noise_mode="uniform",
        noise_enabled=True,
        hat_training=True,
        adc_bits=8
    )
    
    model = build_model(config, num_classes=10, device='cuda')
    set_d2d_mode(model, mode)
    
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.05)
    criterion = nn.CrossEntropyLoss()
    
    best_acc = 0.0
    
    for epoch in range(epochs):
        model.train()
        epoch_loss = 0.0
        
        for inputs, targets in trainloader:
            inputs, targets = inputs.cuda(), targets.cuda()
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
        
        if (epoch + 1) % 10 == 0:
            model.eval()
            correct = 0
            total = 0
            with torch.no_grad():
                for inputs, targets in testloader:
                    inputs, targets = inputs.cuda(), targets.cuda()
                    outputs = model(inputs)
                    _, predicted = outputs.max(1)
                    correct += predicted.eq(targets).sum().item()
                    total += targets.size(0)
            acc = 100.0 * correct / total
            best_acc = max(best_acc, acc)
            print(f"  Epoch {epoch+1}: Loss={epoch_loss/len(trainloader):.4f}, Acc={acc:.2f}%, Best={best_acc:.2f}%")
    
    return best_acc

def main():
    print("="*70)
    print("SPATIAL CORRELATION ABLATION")
    print("="*70)
    print("Testing: Spatially-correlated D2D vs i.i.d. noise")
    print()
    
    configs = [
        ('spatial_fixed', "Standard HAT (spatial, fixed)"),
        ('spatial_resample', "Ensemble HAT (spatial, resample)"),
        ('iid_epoch', "Ensemble HAT (i.i.d., per-epoch)"),
        ('iid_batch', "Extreme (i.i.d., per-batch)"),
    ]
    
    results = []
    
    for mode, description in configs:
        print(f"\n{'='*70}")
        print(f"Testing: {description}")
        print(f"{'='*70}")
        
        start = time.time()
        acc = train_with_spatial_mode(mode, epochs=50)
        elapsed = time.time() - start
        
        results.append({
            'mode': mode,
            'description': description,
            'accuracy': acc,
            'time_seconds': elapsed
        })
        
        print(f"\nResult: {acc:.2f}% in {elapsed/60:.1f} minutes")
    
    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"\n{'Method':<45} {'Accuracy':<15}")
    print("-" * 60)
    
    for r in sorted(results, key=lambda x: x['accuracy'], reverse=True):
        marker = "⭐" if r['accuracy'] == max([x['accuracy'] for x in results]) else ""
        print(f"{r['description']:<45} {r['accuracy']:>6.2f}% {marker}")
    
    # Save
    output = {
        'experiment': 'spatial_correlation_ablation',
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'results': results
    }
    
    output_path = Path('report_md/_gpt/spatial_ablation.json')
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults saved: {output_path}")

if __name__ == "__main__":
    main()
