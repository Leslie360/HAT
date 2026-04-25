#!/usr/bin/env python3
"""
ADC 6-bit Cliff Disambiguation Analysis (Reviewer Priority 3)

Goal: Determine whether 6-bit ADC performance degradation is due to:
  (a) Insufficient quantization levels for activation representation, OR
  (b) Scale mismatch between trained weights and ADC dynamic range

Method: Multi-seed evaluation with scale recovery ablation
"""

import torch
import torch.nn as nn
import numpy as np
import json
from pathlib import Path
from train_tinyvit import build_model, TinyViTExperimentConfig, get_dataloaders, DATASET_STATS, set_seed
from train_tinyvit_ensemble import resample_all_d2d_noise

# Configuration
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
SEEDS = [42, 123, 456, 789, 1024]

def create_config(name, n_states, adc_bits, sigma_c2c, sigma_d2d):
    """Create experiment config."""
    return TinyViTExperimentConfig(
        name=name,
        n_states=n_states,
        nl_ltp=0.1,
        nl_ltd=0.1,
        sigma_c2c=sigma_c2c,
        sigma_d2d=sigma_d2d,
        noise_mode="uniform",
        noise_enabled=True,
        hat_training=True,
        use_hybrid=True,
        adc_bits=adc_bits,
        retention_enabled=False,
        inference_time=0.0,
        asymmetry_factor=0.0,
        ir_drop_factor=0.0,
        sneak_factor=0.0,
        inl_table=None,
    )

def evaluate_with_scale(model, testloader, scale_factor=1.0):
    """Evaluate with optional output scale adjustment."""
    model.eval()
    correct = 0
    total = 0
    
    with torch.no_grad():
        for inputs, targets in testloader:
            inputs, targets = inputs.to(DEVICE), targets.to(DEVICE)
            outputs = model(inputs) * scale_factor
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()
    
    return 100.0 * correct / total

def test_scale_recovery(model, testloader, seed, scales=[0.5, 0.75, 1.0, 1.25, 1.5, 2.0]):
    """Test multiple scale factors to find optimal."""
    results = {}
    for scale in scales:
        set_seed(seed)  # Reset seed for fair comparison
        resample_all_d2d_noise(model)
        acc = evaluate_with_scale(model, testloader, scale)
        results[float(scale)] = acc
    return results

def evaluate_config(name, n_states, adc_bits, checkpoint_path, testloader):
    """Evaluate a specific configuration across multiple seeds."""
    print(f"\n{'='*70}")
    print(f"Config: {name} (ADC={adc_bits}, n_states={n_states})")
    print(f"Checkpoint: {checkpoint_path}")
    print(f"{'='*70}")
    
    config = create_config(name, n_states, adc_bits, sigma_c2c=0.05, sigma_d2d=0.10)
    
    results = {'seeds': {}, 'adc_bits': adc_bits, 'n_states': n_states}
    
    for seed in SEEDS:
        print(f"\n  Seed {seed}:")
        set_seed(seed)
        
        # Build model
        model = build_model(config, num_classes=10, device=DEVICE)
        
        # Load checkpoint
        ckpt = torch.load(checkpoint_path, map_location=DEVICE)
        if isinstance(ckpt, dict) and 'model_state_dict' in ckpt:
            model.load_state_dict(ckpt['model_state_dict'])
        else:
            model.load_state_dict(ckpt)
        
        # Standard evaluation
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
        standard_acc = 100.0 * correct / total
        print(f"    Standard: {standard_acc:.2f}%")
        
        # Scale recovery ablation
        scale_results = test_scale_recovery(model, testloader, seed)
        best_scale = max(scale_results, key=scale_results.get)
        best_acc = scale_results[best_scale]
        print(f"    Scale recovery: {scale_results}")
        print(f"    Best (scale={best_scale}): {best_acc:.2f}%")
        
        results['seeds'][seed] = {
            'standard': standard_acc,
            'scale_recovery': scale_results,
            'best_scale': best_scale,
            'best_acc': best_acc
        }
    
    # Aggregate
    standard_accs = [r['standard'] for r in results['seeds'].values()]
    best_accs = [r['best_acc'] for r in results['seeds'].values()]
    
    results['stats'] = {
        'standard_mean': float(np.mean(standard_accs)),
        'standard_std': float(np.std(standard_accs)),
        'best_mean': float(np.mean(best_accs)),
        'best_std': float(np.std(best_accs)),
        'recovery_gain': float(np.mean(best_accs) - np.mean(standard_accs))
    }
    
    print(f"\n  Summary:")
    print(f"    Standard: {results['stats']['standard_mean']:.2f} ± {results['stats']['standard_std']:.2f}%")
    print(f"    With recovery: {results['stats']['best_mean']:.2f} ± {results['stats']['best_std']:.2f}%")
    print(f"    Recovery gain: {results['stats']['recovery_gain']:+.2f}%")
    
    return results

def main():
    print("=" * 70)
    print("ADC 6-bit Cliff Disambiguation Analysis")
    print("=" * 70)
    print(f"Device: {DEVICE}")
    print(f"Seeds: {SEEDS}")
    print()
    
    # Get CIFAR-10 test data
    _, testloader = get_dataloaders('cifar10', batch_size=128, num_workers=2, data_root='./data')
    
    # Test configurations
    configs = [
        ("ADC8_n16", 16, 8, "checkpoints/V4_hybrid_standard_noise_hat_best.pt"),
        ("ADC6_n16", 16, 6, "checkpoints/V4_hybrid_standard_noise_hat_best.pt"),
        ("ADC4_n16", 16, 4, "checkpoints/V7_4bit_HAT_ADC4_best.pt"),
    ]
    
    all_results = {}
    
    for name, n_states, adc_bits, ckpt_path in configs:
        if not Path(ckpt_path).exists():
            print(f"WARNING: Checkpoint not found: {ckpt_path}")
            continue
        all_results[name] = evaluate_config(name, n_states, adc_bits, ckpt_path, testloader)
    
    # Cross-config comparison
    print(f"\n{'='*70}")
    print("CROSS-CONFIG COMPARISON")
    print(f"{'='*70}")
    
    for name, res in all_results.items():
        stats = res['stats']
        print(f"\n{name}:")
        print(f"  Standard:      {stats['standard_mean']:.2f} ± {stats['standard_std']:.2f}%")
        print(f"  w/ Recovery:   {stats['best_mean']:.2f} ± {stats['best_std']:.2f}%")
        print(f"  Gain:          {stats['recovery_gain']:+.2f}%")
    
    # Save results
    output_path = Path('report_md/_gpt/adc_cliff_analysis.json')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(all_results, f, indent=2)
    print(f"\n\nResults saved: {output_path}")
    
    # Interpretation
    print(f"\n{'='*70}")
    print("INTERPRETATION GUIDE")
    print(f"{'='*70}")
    
    adc6 = all_results.get('ADC6_n16', {}).get('stats', {})
    adc6_gain = adc6.get('recovery_gain', 0)
    
    if adc6_gain > 2.0:
        print("FINDING: 6-bit ADC cliff is PRIMARILY DUE TO SCALE MISMATCH")
        print(f"  - Scale recovery improves accuracy by {adc6_gain:+.2f}%")
        print("  - Recommendation: ADC-aware HAT with dynamic range calibration")
    elif adc6_gain < 0.5:
        print("FINDING: 6-bit ADC cliff is PRIMARILY DUE TO QUANTIZATION LIMIT")
        print(f"  - Scale recovery only improves by {adc6_gain:+.2f}%")
        print("  - Recommendation: Increase ADC precision or non-uniform quantization")
    else:
        print("FINDING: MIXED contribution (both scale and quantization)")
        print(f"  - Scale recovery improves by {adc6_gain:+.2f}%")
        print("  - Recommendation: Both calibration and precision improvements needed")
    
    # Compare to other ADC configs
    for name in ['ADC8_n16', 'ADC4_n16']:
        if name in all_results:
            gain = all_results[name]['stats']['recovery_gain']
            print(f"  vs {name}: {gain:+.2f}% recovery gain")

if __name__ == "__main__":
    main()
