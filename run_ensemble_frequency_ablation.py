#!/usr/bin/env python3
"""
Ensemble HAT Frequency Ablation (Reviewer #4 W2)

Test: Standard (fixed) vs Per-batch vs Per-epoch vs Per-N-epochs
Question: Is per-epoch resampling optimal?
"""

import torch
import json
import time
from pathlib import Path
from train_tinyvit import build_model, TinyViTExperimentConfig, get_dataloaders, set_seed
import torch.nn as nn

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def train_with_frequency(freq_mode, N, epochs=50, lr=0.001):
    """
    Train with specified D2D resampling frequency.
    
    freq_mode: 'fixed', 'batch', 'epoch', 'N_epochs'
    N: resample every N batches/epochs
    """
    print(f"\nTraining: freq={freq_mode}, N={N}")
    set_seed(42)
    
    trainloader, testloader = get_dataloaders('cifar10', batch_size=64, num_workers=2, data_root='./data')
    
    config = TinyViTExperimentConfig(
        name=f"ensemble_freq_{freq_mode}_{N}",
        use_hybrid=True, n_states=16,
        sigma_c2c=0.05, sigma_d2d=0.10,
        noise_mode="uniform",
        noise_enabled=True,
        hat_training=True,  # Critical for HAT
        adc_bits=8
    )
    
    model = build_model(config, num_classes=10, device=DEVICE)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.05)
    criterion = nn.CrossEntropyLoss()
    
    best_acc = 0.0
    resample_count = 0
    
    for epoch in range(epochs):
        model.train()
        epoch_loss = 0.0
        
        for batch_idx, (inputs, targets) in enumerate(trainloader):
            # Determine if we should resample D2D
            should_resample = False
            if freq_mode == 'fixed' and epoch == 0 and batch_idx == 0:
                should_resample = True  # Once at start
            elif freq_mode == 'batch':
                should_resample = (batch_idx % N == 0)
            elif freq_mode == 'epoch':
                should_resample = (batch_idx == 0)  # Start of each epoch
            elif freq_mode == 'N_epochs':
                should_resample = (epoch % N == 0 and batch_idx == 0)
            
            if should_resample:
                from train_tinyvit_ensemble import resample_all_d2d_noise
                resample_all_d2d_noise(model)
                resample_count += 1
            
            inputs, targets = inputs.to(DEVICE), targets.to(DEVICE)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
        
        # Evaluate every 10 epochs
        if (epoch + 1) % 10 == 0:
            model.eval()
            correct = 0
            total = 0
            with torch.no_grad():
                for inputs, targets in testloader:
                    inputs, targets = inputs.to(DEVICE), targets.to(DEVICE)
                    outputs = model(inputs)
                    _, predicted = outputs.max(1)
                    correct += predicted.eq(targets).sum().item()
                    total += targets.size(0)
            acc = 100.0 * correct / total
            best_acc = max(best_acc, acc)
            print(f"  Epoch {epoch+1}: Loss={epoch_loss/len(trainloader):.4f}, Acc={acc:.2f}%, Best={best_acc:.2f}%")
    
    print(f"  Resampled {resample_count} times")
    return best_acc

def main():
    print("="*70)
    print("ENSEMBLE HAT FREQUENCY ABLATION")
    print("="*70)
    print(f"Device: {DEVICE}")
    print()
    
    # Test configurations
    configs = [
        ('fixed', 1, "Standard HAT (fixed D2D)"),
        ('batch', 1, "Per-batch resampling (extreme augmentation)"),
        ('epoch', 1, "Ensemble HAT (per-epoch)"),
        ('N_epochs', 5, "Per-5-epochs resampling"),
        ('N_epochs', 20, "Per-20-epochs resampling"),
    ]
    
    results = []
    
    for freq_mode, N, description in configs:
        print(f"\n{'='*70}")
        print(f"Testing: {description}")
        print(f"{'='*70}")
        
        start = time.time()
        acc = train_with_frequency(freq_mode, N, epochs=50)
        elapsed = time.time() - start
        
        results.append({
            'freq_mode': freq_mode,
            'N': N,
            'description': description,
            'accuracy': acc,
            'time_seconds': elapsed
        })
        
        print(f"\nResult: {acc:.2f}% accuracy in {elapsed/60:.1f} minutes")
    
    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"\n{'Method':<40} {'Accuracy':<15} {'Rank':<10}")
    print("-" * 70)
    
    sorted_results = sorted(results, key=lambda x: x['accuracy'], reverse=True)
    for i, r in enumerate(sorted_results, 1):
        marker = "⭐ OPTIMAL" if i == 1 else ""
        print(f"{r['description']:<40} {r['accuracy']:>6.2f}%       #{i} {marker}")
    
    # Save
    output = {
        'experiment': 'ensemble_hat_frequency_ablation',
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'device': str(DEVICE),
        'results': results
    }
    
    output_path = Path('report_md/_gpt/ensemble_frequency_ablation.json')
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults saved: {output_path}")

if __name__ == "__main__":
    main()
