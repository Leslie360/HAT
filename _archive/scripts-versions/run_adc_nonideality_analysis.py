#!/usr/bin/env python3
"""
ADC Non-Ideality Analysis (Address Reviewer Concern Q2 - Scale-Masking)

Goal: Quantify impact of ADC offset/gain errors and INL/DNL on scale-masking

The reviewer notes that "ideal calibrated digital rescaling" creates artificial
scale-masking where C2C noise is absorbed below quantization step.

This analysis tests robustness when calibration is non-ideal.
"""

import torch
import numpy as np
import json
from pathlib import Path
from train_tinyvit import build_model, TinyViTExperimentConfig, get_dataloaders, set_seed
from train_tinyvit_ensemble import resample_all_d2d_noise

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
SEEDS = [42, 123, 456]

def apply_adc_nonideality(outputs, adc_bits=8, offset_lsb=0.0, gain_error=0.0, inl_lsb=0.0):
    """
    Apply ADC non-ideality to outputs.
    
    Args:
        outputs: Analog output values (before ADC)
        adc_bits: ADC resolution
        offset_lsb: Offset error in LSBs
        gain_error: Gain error (fraction, e.g., 0.05 = 5%)
        inl_lsb: INL (integral non-linearity) in LSBs
    """
    # Quantization step
    q_step = 1.0 / (2**adc_bits - 1)
    
    # 1. Apply gain error
    if gain_error != 0:
        outputs = outputs * (1 + gain_error)
    
    # 2. Apply offset error
    if offset_lsb != 0:
        outputs = outputs + offset_lsb * q_step
    
    # 3. Quantize
    quantized = torch.round(outputs / q_step) * q_step
    
    # 4. Apply INL (simplified: sinusoidal deviation)
    if inl_lsb != 0:
        # INL creates code-dependent errors
        code = torch.round(outputs / q_step).clamp(0, 2**adc_bits - 1)
        inl_error = inl_lsb * q_step * torch.sin(code * 2 * np.pi / (2**adc_bits))
        quantized = quantized + inl_error
    
    # Clip to valid range
    quantized = quantized.clamp(0, 1.0)
    
    return quantized

def evaluate_with_adc_errors(model, testloader, adc_config, seed):
    """Evaluate with ADC non-idealities."""
    set_seed(seed)
    resample_all_d2d_noise(model)
    
    model.eval()
    correct = 0
    total = 0
    
    with torch.no_grad():
        for inputs, targets in testloader:
            inputs, targets = inputs.to(DEVICE), targets.to(DEVICE)
            
            # Forward through model (analog layers)
            outputs = model(inputs)
            
            # Apply ADC non-ideality to simulate non-ideal calibration
            outputs = apply_adc_nonideality(
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
    
    checkpoint_path = "checkpoints/V4_hybrid_standard_noise_hat_best.pt"
    
    # Build base model
    config = TinyViTExperimentConfig(
        name="V4_baseline",
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
    )
    
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
            print(f"  Seed {seed}...", end=" ")
            
            # Build and load model
            model = build_model(config, num_classes=10, device=DEVICE)
            ckpt = torch.load(checkpoint_path, map_location=DEVICE)
            if isinstance(ckpt, dict) and 'model_state_dict' in ckpt:
                model.load_state_dict(ckpt['model_state_dict'])
            else:
                model.load_state_dict(ckpt)
            
            # Evaluate with ADC errors
            acc = evaluate_with_adc_errors(model, testloader, cfg, seed)
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
    output_path = Path('report_md/_gpt/adc_nonideality_analysis.json')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved: {output_path}")
    
    # Interpretation for reviewer response
    print(f"\n{'='*70}")
    print("INTERPRETATION FOR REVIEWER RESPONSE (Q2)")
    print(f"{'='*70}")
    
    realistic = results.get('Combined (realistic)', {}).get('mean', 0)
    pessimistic = results.get('Combined (pessimistic)', {}).get('mean', 0)
    offset_2lsb = results.get('±2 LSB offset', {}).get('mean', 0)
    
    print(f"\n1. Baseline (ideal calibration): {baseline:.2f}%")
    print(f"\n2. With realistic ADC errors (±0.5 LSB, ±5%, 0.5 LSB INL):")
    print(f"   Accuracy: {realistic:.2f}% (degradation: {realistic - baseline:+.2f}%)")
    
    print(f"\n3. With pessimistic ADC errors (±1 LSB, ±10%, 1.0 LSB INL):")
    print(f"   Accuracy: {pessimistic:.2f}% (degradation: {pessimistic - baseline:+.2f}%)")
    
    print(f"\n4. Scale-masking is {'ROBUST' if abs(realistic - baseline) < 2 else 'SENSITIVE'}")
    print(f"   to calibration non-idealities.")
    
    if abs(pessimistic - baseline) > 5:
        print(f"\n5. CONCLUSION: Reviewer's concern is VALID.")
        print(f"   Scale-masking relies heavily on ideal calibration.")
        print(f"   Non-ideal calibration can cause {abs(pessimistic - baseline):.1f}% degradation.")
        print(f"   ")
        print(f"   RECOMMENDATION: Add explicit caveat about calibration quality")
        print(f"   and discuss robust calibration strategies for organic arrays.")
    else:
        print(f"\n5. CONCLUSION: Scale-masking is robust to moderate ADC non-idealities.")

if __name__ == "__main__":
    main()
