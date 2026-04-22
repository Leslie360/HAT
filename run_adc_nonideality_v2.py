#!/usr/bin/env python3
"""
ADC Non-Ideality Analysis v2 (Address Reviewer Q2 - Scale-Masking)

Key fix: Use checkpoint config to build model correctly.
"""

import torch
import numpy as np
import json
from pathlib import Path
from train_tinyvit import build_model, TinyViTExperimentConfig, get_dataloaders, set_seed

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
SEEDS = [42, 123, 456]

def apply_adc_errors(outputs, adc_bits=8, offset_lsb=0.0, gain_error=0.0, inl_lsb=0.0):
    """Apply ADC non-ideality to outputs."""
    q_step = 1.0 / (2**adc_bits - 1)
    
    if gain_error != 0:
        outputs = outputs * (1 + gain_error)
    
    if offset_lsb != 0:
        outputs = outputs + offset_lsb * q_step
    
    quantized = torch.round(outputs / q_step) * q_step
    
    if inl_lsb != 0:
        code = torch.round(outputs / q_step).clamp(0, 2**adc_bits - 1)
        inl_error = inl_lsb * q_step * torch.sin(code * 2 * np.pi / (2**adc_bits))
        quantized = quantized + inl_error
    
    quantized = quantized.clamp(0, 1.0)
    return quantized

def evaluate_with_adc_errors(model, testloader, adc_config):
    """Evaluate with ADC non-idealities applied to outputs."""
    model.eval()
    correct = 0
    total = 0
    
    with torch.no_grad():
        for inputs, targets in testloader:
            inputs, targets = inputs.to(DEVICE), targets.to(DEVICE)
            outputs = model(inputs)
            
            # Apply ADC non-ideality to simulate non-ideal calibration
            outputs = apply_adc_errors(
                outputs,
                adc_bits=adc_config['bits'],
                offset_lsb=adc_config['offset_lsb'],
                gain_error=adc_config['gain_error'],
                inl_lsb=adc_config['inl_lsb']
            )
            
            _, predicted = outputs.max(1)
            correct += predicted.eq(targets).sum().item()
            total += targets.size(0)
    
    return 100.0 * correct / total

def main():
    print("=" * 70)
    print("ADC Non-Ideality Analysis (Reviewer Q2 - Scale-Masking)")
    print("=" * 70)
    print(f"Device: {DEVICE}")
    print()
    print("Testing robustness of 'ideal calibrated digital rescaling'")
    print("when calibration has offset/gain/INL errors.")
    print()
    
    # Load checkpoint
    checkpoint_path = "checkpoints/V4_hybrid_standard_noise_hat_best.pt"
    ckpt = torch.load(checkpoint_path, map_location='cpu')
    original_cfg_dict = ckpt['exp_cfg']
    print(f"Loaded checkpoint: Epoch {ckpt['epoch']}, Best Acc: {ckpt['best_acc']:.2f}%")
    print()
    
    # Get CIFAR-10 test data
    _, testloader = get_dataloaders('cifar10', batch_size=128, num_workers=2, data_root='./data')
    
    # ADC configurations
    adc_configs = [
        {'name': 'Ideal', 'bits': 8, 'offset_lsb': 0.0, 'gain_error': 0.0, 'inl_lsb': 0.0},
        {'name': '±0.5 LSB offset', 'bits': 8, 'offset_lsb': 0.5, 'gain_error': 0.0, 'inl_lsb': 0.0},
        {'name': '±1 LSB offset', 'bits': 8, 'offset_lsb': 1.0, 'gain_error': 0.0, 'inl_lsb': 0.0},
        {'name': '±2 LSB offset', 'bits': 8, 'offset_lsb': 2.0, 'gain_error': 0.0, 'inl_lsb': 0.0},
        {'name': '±5% gain error', 'bits': 8, 'offset_lsb': 0.0, 'gain_error': 0.05, 'inl_lsb': 0.0},
        {'name': '±10% gain error', 'bits': 8, 'offset_lsb': 0.0, 'gain_error': 0.10, 'inl_lsb': 0.0},
        {'name': '0.5 LSB INL', 'bits': 8, 'offset_lsb': 0.0, 'gain_error': 0.0, 'inl_lsb': 0.5},
        {'name': '1.0 LSB INL', 'bits': 8, 'offset_lsb': 0.0, 'gain_error': 0.0, 'inl_lsb': 1.0},
        {'name': 'Combined (realistic)', 'bits': 8, 'offset_lsb': 0.5, 'gain_error': 0.05, 'inl_lsb': 0.5},
        {'name': 'Combined (pessimistic)', 'bits': 8, 'offset_lsb': 1.0, 'gain_error': 0.10, 'inl_lsb': 1.0},
    ]
    
    results = {}
    
    for cfg in adc_configs:
        print(f"\n{'='*70}")
        print(f"ADC Config: {cfg['name']}")
        print(f"  Offset: ±{cfg['offset_lsb']} LSB")
        print(f"  Gain error: ±{cfg['gain_error']*100:.1f}%")
        print(f"  INL: ±{cfg['inl_lsb']} LSB")
        print(f"{'='*70}")
        
        accs = []
        
        for seed in SEEDS:
            print(f"  Seed {seed}...", end=" ", flush=True)
            set_seed(seed)
            
            # Build model with checkpoint config
            config = TinyViTExperimentConfig(
                name=f"V4_adc_test",
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
            )
            
            model = build_model(config, num_classes=10, device=DEVICE)
            model.load_state_dict(ckpt['model_state_dict'])
            
            # Evaluate with ADC errors
            acc = evaluate_with_adc_errors(model, testloader, cfg)
            accs.append(acc)
            print(f"{acc:.2f}%")
        
        mean_acc = np.mean(accs)
        std_acc = np.std(accs)
        
        results[cfg['name']] = {
            'config': {k: v for k, v in cfg.items() if k != 'name'},
            'mean': float(mean_acc),
            'std': float(std_acc),
            'seeds': {seed: acc for seed, acc in zip(SEEDS, accs)}
        }
        
        print(f"  Mean: {mean_acc:.2f} ± {std_acc:.2f}%")
    
    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY: ADC Non-Ideality Impact on Scale-Masking")
    print(f"{'='*70}")
    print(f"\n{'Configuration':<30} {'Accuracy':<15} {'Degradation':<15}")
    print("-" * 60)
    
    baseline = results['Ideal']['mean']
    
    for name, data in results.items():
        degradation = data['mean'] - baseline
        print(f"{name:<30} {data['mean']:>6.2f}±{data['std']:<4.2f}% {degradation:>+6.2f}%")
    
    # Save results
    output_path = Path('report_md/_gpt/adc_nonideality_final.json')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved: {output_path}")
    
    # Interpretation
    print(f"\n{'='*70}")
    print("INTERPRETATION FOR REVIEWER RESPONSE (Q2)")
    print(f"{'='*70}")
    
    realistic = results.get('Combined (realistic)', {}).get('mean', 0)
    pessimistic = results.get('Combined (pessimistic)', {}).get('mean', 0)
    
    print(f"\n1. Baseline (ideal calibration): {baseline:.2f}%")
    
    print(f"\n2. With realistic ADC errors (±0.5 LSB, ±5%, 0.5 LSB INL):")
    print(f"   Accuracy: {realistic:.2f}% (degradation: {realistic - baseline:+.2f}%)")
    
    print(f"\n3. With pessimistic ADC errors (±1 LSB, ±10%, 1.0 LSB INL):")
    print(f"   Accuracy: {pessimistic:.2f}% (degradation: {pessimistic - baseline:+.2f}%)")
    
    degradation_realistic = abs(realistic - baseline)
    print(f"\n4. Scale-masking is {'ROBUST' if degradation_realistic < 2 else 'SENSITIVE'}")
    print(f"   to calibration non-idealities.")
    
    if degradation_realistic > 2:
        print(f"\n5. CONCLUSION: Reviewer's concern is VALID.")
        print(f"   Scale-masking relies heavily on ideal calibration.")
        print(f"   Non-ideal calibration can cause {degradation_realistic:.1f}% degradation.")
    else:
        print(f"\n5. CONCLUSION: Scale-masking is robust to moderate ADC non-idealities.")
        print(f"   The 'ideal calibrated digital rescaling' assumption is reasonable")
        print(f"   for typical ADC errors (±0.5 LSB, ±5% gain).")

if __name__ == "__main__":
    main()
