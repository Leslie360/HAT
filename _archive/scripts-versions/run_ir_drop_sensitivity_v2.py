#!/usr/bin/env python3
"""
IR Drop Sensitivity Analysis v2 (Address Reviewer Concern Q1)

Uses original checkpoint config to ensure correct model loading.
"""

import torch
import numpy as np
import json
from pathlib import Path
from train_tinyvit import build_model, get_dataloaders, set_seed
from train_tinyvit_ensemble import resample_all_d2d_noise

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

def evaluate_model(model, testloader, seed):
    """Evaluate model."""
    set_seed(seed)
    resample_all_d2d_noise(model)
    
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
            
            # Build model with original config - use build_model with correct approach
            from train_tinyvit import TinyViTExperimentConfig
            
            # Create config matching checkpoint
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
                ir_drop_factor=ir_factor,  # Set the IR drop factor
                sneak_factor=0.0,
                inl_table=None,
            )
            
            model = build_model(config, num_classes=10, device=DEVICE)
            
            # Load checkpoint weights
            model.load_state_dict(ckpt['model_state_dict'])
            
            # Verify IR drop is set
            count = set_ir_drop(model, ir_factor)
            
            # Evaluate
            acc = evaluate_model(model, testloader, seed)
            accs.append(acc)
            print(f"{acc:.2f}% (set {count} layers)")
        
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
    
    baseline = results[0.00]['mean']  # Use 0% as baseline
    
    for ir_factor, data in sorted(results.items()):
        degradation = data['mean'] - baseline
        print(f"{data['description']:<25} {data['mean']:>6.2f}±{data['std']:<4.2f}% {degradation:>+6.2f}%")
    
    # Save results
    output_path = Path('report_md/_gpt/ir_drop_sensitivity_v2.json')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved: {output_path}")
    
    # Interpretation for reviewer response
    print(f"\n{'='*70}")
    print("INTERPRETATION FOR REVIEWER RESPONSE")
    print(f"{'='*70}")
    
    baseline_acc = results[0.00]['mean']
    drop_10 = results.get(0.10, {}).get('mean', 0)
    drop_20 = results.get(0.20, {}).get('mean', 0)
    
    print(f"\n1. Baseline (0% IR drop): {baseline_acc:.2f}%")
    
    print(f"\n2. At 10% IR drop (organic typical): {drop_10:.2f}% accuracy")
    print(f"   Degradation: {drop_10 - baseline_acc:+.2f}%")
    
    print(f"\n3. At 20% IR drop (organic extreme): {drop_20:.2f}% accuracy")
    print(f"   Degradation: {drop_20 - baseline_acc:+.2f}%")
    
    degradation_20 = abs(drop_20 - baseline_acc)
    print(f"\n4. Framework shows {'graceful' if degradation_20 < 10 else 'significant'} degradation")
    print(f"   with increasing IR drop.")
    
    print(f"\n5. RECOMMENDATION:")
    print(f"   - 0-3% IR drop: Use as 'optimistic lower bound' (ReRAM-like)")
    print(f"   - 5-10% IR drop: Typical for organic arrays")
    print(f"   - >10% IR drop: High-resistance organic arrays")
    print(f"   - Add sensitivity discussion to manuscript Section X")

if __name__ == "__main__":
    main()
