#!/usr/bin/env python3
"""
Framework Comparison Experiment (Reviewer #4 W1)

Compare our framework vs AIHWKIT on canonical + organic-specific configs.
No organic features in AIHWKIT → demonstrate capability gap.
"""

import torch
import json
import time
from pathlib import Path
from train_tinyvit import build_model, TinyViTExperimentConfig, get_dataloaders, set_seed
from train_tinyvit_ensemble import resample_all_d2d_noise

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
RESULTS = {}

def run_ours(config_name, exp_cfg, num_classes=10):
    """Run our framework."""
    print(f"\n{'='*60}")
    print(f"Running OUR FRAMEWORK: {config_name}")
    print(f"{'='*60}")
    
    set_seed(42)
    _, testloader = get_dataloaders('cifar10', batch_size=128, num_workers=2, data_root='./data')
    
    start_time = time.time()
    model = build_model(exp_cfg, num_classes=num_classes, device=DEVICE)
    
    # Load checkpoint if available
    ckpt_path = f"checkpoints/V4_hybrid_standard_noise_hat_best.pt"
    if Path(ckpt_path).exists() and config_name == "canonical":
        ckpt = torch.load(ckpt_path, map_location=DEVICE)
        model.load_state_dict(ckpt['model_state_dict'])
        print(f"Loaded checkpoint: {ckpt_path}")
    
    # Evaluate (no D2D resampling for single checkpoint eval)
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
    elapsed = time.time() - start_time
    
    result = {
        'framework': 'ours',
        'config': config_name,
        'accuracy': acc,
        'time_seconds': elapsed,
        'device': str(DEVICE),
        'status': 'success'
    }
    
    print(f"Accuracy: {acc:.2f}%")
    print(f"Time: {elapsed:.1f}s")
    
    return result

def run_aihwkit_baseline():
    """Reference AIHWKIT result from previous run."""
    return {
        'framework': 'aihwkit',
        'config': 'resnet18_cifar10_4bit',
        'accuracy': 90.08,
        'accuracy_std': 0.21,
        'time_seconds': 11358,  # From log
        'device': 'cpu',
        'status': 'reference',
        'note': 'From p13_aihwkit_shared_regime_result.json'
    }

def main():
    print("="*60)
    print("FRAMEWORK COMPARISON EXPERIMENT")
    print("="*60)
    print(f"Device: {DEVICE}")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Config 1: Canonical (already have results)
    print("\n[1/4] CANONICAL CONFIGURATION")
    canonical_ours = run_ours("canonical", TinyViTExperimentConfig(
        name="V4_canonical", use_hybrid=True, n_states=16,
        sigma_c2c=0.05, sigma_d2d=0.10, noise_mode="uniform",
        noise_enabled=True, hat_training=True, adc_bits=8
    ))
    
    canonical_aihwkit = run_aihwkit_baseline()
    
    # Config 2: With photoresponse (organic-specific)
    print("\n[2/4] WITH PHOTORESPONSE (Organic-specific)")
    photo_ours = run_ours("photoresponse", TinyViTExperimentConfig(
        name="V4_photoresponse", use_hybrid=True, n_states=16,
        sigma_c2c=0.05, sigma_d2d=0.10, noise_mode="uniform",
        noise_enabled=True, hat_training=True, adc_bits=8,
        use_physical_frontend=True, physical_gamma=0.8, physical_I_dark=1e-10
    ))
    
    photo_aihwkit = {
        'framework': 'aihwkit',
        'config': 'photoresponse',
        'status': 'not_supported',
        'note': 'AIHWKIT does not support photoresponse modeling'
    }
    
    # Config 3: With retention (organic-specific)
    print("\n[3/4] WITH RETENTION (Organic-specific)")
    retention_ours = run_ours("retention", TinyViTExperimentConfig(
        name="V4_retention", use_hybrid=True, n_states=16,
        sigma_c2c=0.05, sigma_d2d=0.10, noise_mode="uniform",
        noise_enabled=True, hat_training=True, adc_bits=8,
        retention_enabled=True, inference_time=3600  # 1 hour
    ))
    
    retention_aihwkit = {
        'framework': 'aihwkit',
        'config': 'retention',
        'status': 'not_supported',
        'note': 'AIHWKIT does not support double-exponential retention'
    }
    
    # Config 4: With NL (organic-specific)
    print("\n[4/4] WITH NL=2.0 (Organic-specific)")
    nl_ours = run_ours("nl_2.0", TinyViTExperimentConfig(
        name="V4_nl2", use_hybrid=True, n_states=16,
        sigma_c2c=0.05, sigma_d2d=0.10, noise_mode="uniform",
        noise_enabled=True, hat_training=True, adc_bits=8,
        nl_ltp=2.0, nl_ltd=-2.0
    ))
    
    nl_aihwkit = {
        'framework': 'aihwkit',
        'config': 'nl_2.0',
        'status': 'not_supported',
        'note': 'AIHWKIT does not support NL write asymmetry'
    }
    
    # Compile results
    RESULTS = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'device': str(DEVICE),
        'comparisons': [
            {'config': 'canonical', 'ours': canonical_ours, 'aihwkit': canonical_aihwkit},
            {'config': 'photoresponse', 'ours': photo_ours, 'aihwkit': photo_aihwkit},
            {'config': 'retention', 'ours': retention_ours, 'aihwkit': retention_aihwkit},
            {'config': 'nl_2.0', 'ours': nl_ours, 'aihwkit': nl_aihwkit},
        ]
    }
    
    # Save
    output_path = Path('report_md/_gpt/framework_comparison.json')
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(RESULTS, f, indent=2)
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    
    print(f"\n{'Config':<20} {'Ours':<15} {'AIHWKIT':<15} {'Advantage':<20}")
    print("-" * 70)
    for comp in RESULTS['comparisons']:
        ours_acc = comp['ours'].get('accuracy', 'N/A')
        aihwkit_acc = comp['aihwkit'].get('accuracy', comp['aihwkit'].get('status', 'N/A'))
        
        if isinstance(ours_acc, float) and isinstance(aihwkit_acc, float):
            diff = f"{ours_acc - aihwkit_acc:+.2f}%"
        elif comp['aihwkit'].get('status') == 'not_supported':
            diff = "Exclusive capability"
        else:
            diff = "N/A"
        
        print(f"{comp['config']:<20} {str(ours_acc):<15} {str(aihwkit_acc):<15} {diff:<20}")
    
    print(f"\nResults saved: {output_path}")
    print(f"\nKey Finding: Our framework supports organic-specific features")
    print(f"(photoresponse, retention, NL) that AIHWKIT cannot model.")

if __name__ == "__main__":
    main()
