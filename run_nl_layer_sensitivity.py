#!/usr/bin/env python3
"""
NL=2.0 Layer-wise Sensitivity (Reviewer #4 W3)

Test: Which ViT layers are most affected by NL=2.0?
Method: Freeze all layers except one, train with NL=2.0
"""

import torch
import json
from pathlib import Path
from train_tinyvit import build_model, TinyViTExperimentConfig, get_dataloaders, set_seed
import torch.nn as nn

def freeze_all_except(model, target_layer):
    """Freeze all parameters except target layer."""
    for name, param in model.named_parameters():
        if target_layer in name:
            param.requires_grad = True
        else:
            param.requires_grad = False

def train_layer_isolated(layer_name, epochs=30, lr=0.001):
    """Train with only one layer unfrozen."""
    print(f"\n{'='*60}")
    print(f"Isolating layer: {layer_name}")
    print(f"{'='*60}")
    
    set_seed(42)
    trainloader, testloader = get_dataloaders('cifar10', batch_size=64, num_workers=2, data_root='./data')
    
    config = TinyViTExperimentConfig(
        name=f"nl_layer_{layer_name}",
        use_hybrid=True, n_states=16,
        sigma_c2c=0.05, sigma_d2d=0.10,
        noise_mode="uniform",
        noise_enabled=True, hat_training=True,
        adc_bits=8,
        nl_ltp=2.0, nl_ltd=-2.0  # High NL
    )
    
    model = build_model(config, num_classes=10, device='cuda')
    freeze_all_except(model, layer_name)
    
    # Count trainable parameters
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())
    print(f"Trainable: {trainable:,} / {total:,} parameters ({100*trainable/total:.1f}%)")
    
    optimizer = torch.optim.AdamW(
        [p for p in model.parameters() if p.requires_grad],
        lr=lr, weight_decay=0.05
    )
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
    
    return best_acc, trainable

def main():
    print("="*70)
    print("NL=2.0 LAYER-WISE SENSITIVITY ANALYSIS")
    print("="*70)
    print("Testing which layers are most affected by severe NL")
    print()
    
    # Key layers to test
    layers = [
        ('patch_embed', 'Patch Embedding'),
        ('blocks.0', 'Transformer Block 0 (early)'),
        ('blocks.2', 'Transformer Block 2 (mid)'),
        ('blocks.5', 'Transformer Block 5 (deep)'),
        ('head', 'Classification Head'),
    ]
    
    results = []
    
    for layer_name, description in layers:
        acc, params = train_layer_isolated(layer_name, epochs=30)
        results.append({
            'layer': layer_name,
            'description': description,
            'accuracy': acc,
            'trainable_params': params
        })
    
    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY: Layer Sensitivity to NL=2.0")
    print(f"{'='*70}")
    print(f"\n{'Layer':<30} {'Accuracy':<12} {'Trainable %':<15} {'Sensitivity':<15}")
    print("-" * 75)
    
    baseline = 27.72  # Full model NL=2.0 accuracy
    
    for r in sorted(results, key=lambda x: x['accuracy']):
        total_params = 2361348  # Tiny-ViT total
        percent = 100 * r['trainable_params'] / total_params
        
        if r['accuracy'] < 15:
            sensitivity = "🔴 HIGH"
        elif r['accuracy'] < 25:
            sensitivity = "🟡 MEDIUM"
        else:
            sensitivity = "🟢 LOW"
        
        print(f"{r['description']:<30} {r['accuracy']:>6.2f}%     {percent:>5.1f}%          {sensitivity}")
    
    # Save
    output = {
        'experiment': 'nl_layer_sensitivity',
        'baseline_full_model': baseline,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'results': results
    }
    
    output_path = Path('report_md/_gpt/nl_layer_sensitivity.json')
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults saved: {output_path}")
    print(f"\nKey Finding: Layers with 🔴 HIGH sensitivity are")
    print(f"most affected by NL=2.0 and should be prioritized")
    print(f"for mitigation strategies.")

if __name__ == "__main__":
    import time
    main()
