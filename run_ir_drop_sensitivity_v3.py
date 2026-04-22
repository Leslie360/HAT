#!/usr/bin/env python3
"""
IR Drop Sensitivity Analysis v3 (Address Reviewer Concern Q1)

Key fix: Do NOT resample D2D noise for single checkpoint evaluation.
The checkpoint contains the trained D2D noise instances.
"""

import torch
import numpy as np
import json
from pathlib import Path
from train_tinyvit import build_model, TinyViTExperimentConfig, get_dataloaders, set_seed

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
SEEDS = [42, 123, 456]

def set_ir_drop(model, ir_factor):
    """Set IR drop factor for all analog layers."""
    from analog_layers import AnalogLinear, AnalogConv2d
    count = 0
    for m in model.modules():
        if isinstance(m, (AnalogLinear, AnalogConv2d)):
            m.config.ir_drop_factor = ir_factor
            count += 1
    return count

def evaluate_model(model, testloader):
    """Evaluate model (no D2D resampling for single checkpoint)."""
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
    print("NOTE: Using fixed D2D noise from checkpoint (no resampling)")
    print()
    
    # Load checkpoint
    checkpoint_path = "checkpoints/V4_hybrid_standard_noise_hat_best.pt"
    ckpt = torch.load(checkpoint_path, map_location='cpu')
    original_cfg_dict = ckpt['exp_cfg']
    print(f"Loaded checkpoint: Epoch {ckpt['epoch']}, Best Acc: {ckpt['best_acc']:.2f}%")
    print()
    
    # Get CIFAR-10 test data
    _, testloader = get_dataloaders('cifar10', batch_size=128, num_workers=2, data_root='./data')
    
    # IR drop configurations to test
    ir_configs = [
        (0.00, "0% (No IR drop)"),
        (0.01, "1% (ReRAM lower bound)"),
        (0.02, "2% (ReRAM typical)"),
        (0.03, "3% (ReRAM upper bound)"),
        (0.05, "5% (Organic conservative)"),
        (0.10, "10% (Organic typical)"),
        (0.15, "15% (Organic high)"),
        (0.20, "20% (Organic extreme)"),
    ]
    
    results = {}
    
    for ir_factor, description in ir_configs:
        print(f"\n{'='*70}")
        print(f"IR Drop: {description} (factor={ir_factor})")
        print(f"{'='*70}")
        
        accs = []
        
        for seed in SEEDS:
            print(f"  Seed {seed}...", end=" ", flush=True)
            set_seed(seed)
            
            # Build model with original config
            config = TinyViTExperimentConfig(
                name=f"V4_ir_{ir_factor}",
                use_hybrid=original_cfg_dict['use_hybrid'],
                n_states=original_cfg_dict['n_states'],
                nl_ltp=0.1,
                nl_ltd=0.1,
                sigma_c2c=original_cfg_dict['sigma_c2c'],
                sigma_d2d=original_cfg_dict['sigma_d2d'],
                noise_mode="uniform",
                noise_enabled=original_cfg_dict['noise_enabled'],
                hat_training=original_cfg_dict['hat_training'],
                use_physical_frontend=original_cfg_dict.get('use_physical_frontend', False),
                retention_enabled=original_cfg_dict.get('retention_enabled', False),
                inference_time=original_cfg_dict.get('inference_time', 0.0),
                physical_gamma=original_cfg_dict.get('physical_gamma', 1.0),
                physical_I_dark=original_cfg_dict.get('physical_I_dark', 1e-10),
                adc_bits=original_cfg_dict.get('adc_bits', 8),
                asymmetry_factor=0.0,
                ir_drop_factor=ir_factor,
                sneak_factor=0.0,
                inl_table=None,
            )
            
            model = build_model(config, num_classes=10, device=DEVICE)
            
            # Load checkpoint weights (includes D2D noise)
            model.load_state_dict(ckpt['model_state_dict'])
            
            # Set IR drop
            count = set_ir_drop(model, ir_factor)
            
            # Evaluate (no D2D resampling!)
            acc = evaluate_model(model, testloader)
            accs.append(acc)
            print(f"{acc:.2f}% ({count} analog layers)")
        
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
    print(f"\n{'IR Drop':<25} {'Accuracy':<15} {'Degradation':<15}")
    print("-" * 55)
    
    baseline = results[0.00]['mean']
    
    for ir_factor, data in sorted(results.items()):
        degradation = data['mean'] - baseline
        print(f"{data['description']:<25} {data['mean']:>6.2f}±{data['std']:<4.2f}% {degradation:>+6.2f}%")
    
    # Save results
    output_path = Path('report_md/_gpt/ir_drop_sensitivity_final.json')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved: {output_path}")
    
    # Interpretation
    print(f"\n{'='*70}")
    print("INTERPRETATION FOR REVIEWER RESPONSE (Q1)")
    print(f"{'='*70}")
    
    baseline_acc = results[0.00]['mean']
    reram_typical = results.get(0.02, {}).get('mean', 0)
    organic_typical = results.get(0.10, {}).get('mean', 0)
    organic_extreme = results.get(0.20, {}).get('mean', 0)
    
    print(f"\n1. Baseline (0% IR drop): {baseline_acc:.2f}%")
    print(f"   This is the 'ideal' case reported in the paper.")
    
    print(f"\n2. ReRAM typical (2% IR drop): {reram_typical:.2f}%")
    print(f"   Degradation: {reram_typical - baseline_acc:+.2f}%")
    
    print(f"\n3. Organic typical (10% IR drop): {organic_typical:.2f}%")
    print(f"   Degradation: {organic_typical - baseline_acc:+.2f}%")
    
    print(f"\n4. Organic extreme (20% IR drop): {organic_extreme:.2f}%")
    print(f"   Degradation: {organic_extreme - baseline_acc:+.2f}%")
    
    degradation_10 = abs(organic_typical - baseline_acc)
    print(f"\n5. CONCLUSION:")
    if degradation_10 < 2:
        print(f"   ✅ Framework is ROBUST to IR drop up to 10%")
        print(f"      (Degradation only {degradation_10:.2f}%)")
    elif degradation_10 < 5:
        print(f"   ⚠️ Framework shows MODERATE sensitivity to IR drop")
        print(f"      (Degradation {degradation_10:.2f}% at 10% IR drop)")
    else:
        print(f"   ❌ Framework shows SIGNIFICANT sensitivity to IR drop")
        print(f"      (Degradation {degradation_10:.2f}% at 10% IR drop)")
    
    print(f"\n6. REVIEWER RESPONSE RECOMMENDATION:")
    print(f"   - Current paper uses 0% IR drop (idealized)")
    print(f"   - ReRAM literature: 1-3% (our 'conservative' estimate)")
    print(f"   - Organic arrays: May experience 5-15% due to higher sheet resistance")
    print(f"   - Impact: {'Negligible' if degradation_10 < 2 else 'Moderate' if degradation_10 < 5 else 'Significant'}")
    print(f"   - Action: Add sensitivity analysis to manuscript Section X")

if __name__ == "__main__":
    main()
