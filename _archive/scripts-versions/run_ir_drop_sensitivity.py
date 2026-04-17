#!/usr/bin/env python3
"""
IR Drop Sensitivity Analysis (Address Reviewer Concern Q1)

Goal: Quantify framework behavior under higher IR drop scenarios
      (organic arrays have higher sheet resistance than ReRAM)

Range: 1-3% (current, ReRAM proxy) → 5%, 10%, 15%, 20% (organic estimates)
"""

import torch
import numpy as np
import json
from pathlib import Path
from train_tinyvit import build_model, TinyViTExperimentConfig, get_dataloaders, set_seed
from train_tinyvit_ensemble import resample_all_d2d_noise

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
SEEDS = [42, 123, 456]

def create_config(ir_drop_factor):
    """Create config with specified IR drop."""
    return TinyViTExperimentConfig(
        name=f"V4_ir_{ir_drop_factor}",
        n_states=16,
        nl_ltp=0.1,
        nl_ltd=0.1,
        sigma_c2c=0.05,
        sigma_d2d=0.10,
        noise_mode="uniform",
        noise_enabled=True,
        hat_training=True,
        use_hybrid=True,
        adc_bits=8,
        retention_enabled=False,
        inference_time=0.0,
        asymmetry_factor=0.0,
        ir_drop_factor=ir_drop_factor,  # Key parameter
        sneak_factor=0.0,
        inl_table=None,
    )

def evaluate_with_ir_drop(model, testloader, ir_drop_factor, seed):
    """Evaluate with specified IR drop."""
    set_seed(seed)
    resample_all_d2d_noise(model)
    
    # Temporarily set IR drop
    from analog_layers import AnalogLinear, AnalogConv2d
    for m in model.modules():
        if isinstance(m, (AnalogLinear, AnalogConv2d)):
            m.config.ir_drop_factor = ir_drop_factor
    
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
    
    return 100.0 * correct / total

def main():
    print("=" * 70)
    print("IR Drop Sensitivity Analysis (Reviewer Q1)")
    print("=" * 70)
    print(f"Device: {DEVICE}")
    print()
    
    # Load checkpoint to get original config
    checkpoint_path = "checkpoints/V4_hybrid_standard_noise_hat_best.pt"
    ckpt = torch.load(checkpoint_path, map_location='cpu')
    original_cfg_dict = ckpt['exp_cfg']
    print(f"Loaded checkpoint: Epoch {ckpt['epoch']}, Best Acc: {ckpt['best_acc']:.2f}%")
    print()
    
    # Get CIFAR-10 test data
    _, testloader = get_dataloaders('cifar10', batch_size=128, num_workers=2, data_root='./data')
    
    # IR drop configurations to test
    ir_configs = [
        (0.01, "1% (ReRAM lower bound)"),
        (0.02, "2% (ReRAM typical)"),
        (0.03, "3% (ReRAM upper bound)"),
        (0.05, "5% (Organic conservative)"),
        (0.07, "7% (Organic moderate)"),
        (0.10, "10% (Organic typical)"),
        (0.15, "15% (Organic high)"),
        (0.20, "20% (Organic extreme)"),
    ]
    
    checkpoint_path = "checkpoints/V4_hybrid_standard_noise_hat_best.pt"
    
    results = {}
    
    for ir_factor, description in ir_configs:
        print(f"\n{'='*70}")
        print(f"IR Drop: {description}")
        print(f"{'='*70}")
        
        config = create_config(ir_factor)
        accs = []
        
        for seed in SEEDS:
            print(f"  Seed {seed}...", end=" ")
            
            # Build and load model
            model = build_model(config, num_classes=10, device=DEVICE)
            ckpt = torch.load(checkpoint_path, map_location=DEVICE)
            if isinstance(ckpt, dict) and 'model_state_dict' in ckpt:
                model.load_state_dict(ckpt['model_state_dict'])
            else:
                model.load_state_dict(ckpt)
            
            # Evaluate
            acc = evaluate_with_ir_drop(model, testloader, ir_factor, seed)
            accs.append(acc)
            print(f"{acc:.2f}%")
        
        mean_acc = np.mean(accs)
        std_acc = np.std(accs)
        
        results[ir_factor] = {
            'description': description,
            'mean': float(mean_acc),
            'std': float(std_acc),
            'seeds': {seed: acc for seed, acc in zip(SEEDS, accs)}
        }
        
        print(f"  Mean: {mean_acc:.2f} ± {std_acc:.2f}%")
    
    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY: IR Drop Impact")
    print(f"{'='*70}")
    print(f"\n{'IR Drop':<12} {'Accuracy':<15} {'Degradation':<15}")
    print("-" * 45)
    
    baseline = results[0.01]['mean']  # Use 1% as baseline
    
    for ir_factor, data in sorted(results.items()):
        degradation = data['mean'] - baseline
        print(f"{data['description']:<12} {data['mean']:>6.2f}±{data['std']:<4.2f}% {degradation:>+6.2f}%")
    
    # Save results
    output_path = Path('report_md/_gpt/ir_drop_sensitivity.json')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved: {output_path}")
    
    # Interpretation for reviewer response
    print(f"\n{'='*70}")
    print("INTERPRETATION FOR REVIEWER RESPONSE")
    print(f"{'='*70}")
    
    drop_10 = results.get(0.10, {}).get('mean', 0)
    drop_20 = results.get(0.20, {}).get('mean', 0)
    
    print(f"\n1. At 10% IR drop (organic typical): {drop_10:.2f}% accuracy")
    print(f"   Degradation from 1%: {drop_10 - baseline:+.2f}%")
    
    print(f"\n2. At 20% IR drop (organic extreme): {drop_20:.2f}% accuracy")
    print(f"   Degradation from 1%: {drop_20 - baseline:+.2f}%")
    
    print(f"\n3. Framework shows {'graceful' if abs(drop_20 - baseline) < 20 else 'steep'} degradation")
    print(f"   with increasing IR drop.")
    
    print(f"\n4. Recommendation: Use 1-3% as 'optimistic lower bound'")
    print(f"   and note actual organic arrays may experience 5-15% IR drop.")

if __name__ == "__main__":
    main()
