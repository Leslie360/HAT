"""
ConvNeXt-Tiny ADC Bit-width Sweep

Validates that ResNet-18 CIFAR-100 issue is architecture-specific
by running full ADC scan on ConvNeXt-Tiny
"""

import torch
import torch.nn as nn
import numpy as np
import json
import os
import sys
import dataclasses

sys.path.insert(0, '/home/qiaosir/projects/compute_vit')

from train_convnext import (
    build_model, get_dataloaders,
    ExperimentConfig, DATASET_STATS, set_seed
)
from inference_analysis_utils import (
    ADCQuantHookManager,
    ModelBundle,
    calibrate_adc_ranges,
)

def evaluate(model, loader, device):
    """Simple evaluation function"""
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, targets in loader:
            inputs, targets = inputs.to(device), targets.to(device)
            outputs = model(inputs)
            _, predicted = outputs.max(1)
            correct += predicted.eq(targets).sum().item()
            total += targets.size(0)
    return 100.0 * correct / total

def run_adc_sweep(checkpoint_path, dataset='cifar10', device='cuda'):
    """Run ADC bit-width sweep on ConvNeXt"""
    
    adc_configs = [4, 6, 8, 10, 12]
    results = {}
    
    # Get image size from dataset stats
    img_sz = DATASET_STATS[dataset]["image_size"]
    
    print(f"\nDataset: {dataset} (image_size={img_sz})")
    print(f"Checkpoint: {checkpoint_path}")
    
    for adc_bits in adc_configs:
        print("\n" + "="*70)
        print(f"ADC Bits: {adc_bits}")
        print("="*70)
        
        # Load checkpoint
        ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
        exp_cfg_dict = ckpt.get('exp_cfg', {})
        
        # Build config
        valid_keys = {f.name for f in dataclasses.fields(ExperimentConfig)}
        filtered = {k: v for k, v in exp_cfg_dict.items() if k in valid_keys}
        cfg = ExperimentConfig(**filtered)
        
        cfg.noise_enabled = True
        
        num_classes = DATASET_STATS[dataset]['num_classes']
        _, loader = get_dataloaders(dataset, batch_size=256)

        # ADC is implemented as inference-only hooks on analog layer outputs.
        # Setting cfg.adc_bits alone has no effect on ConvNeXt/AnalogConv2d.
        set_seed(1234)
        calibration_model = build_model(cfg, num_classes, img_sz, device)
        calibration_model.load_state_dict(ckpt['model_state_dict'])
        calibration_bundle = ModelBundle(
            model_type="convnext",
            experiment=cfg.name,
            experiment_name=cfg.name,
            dataset=dataset,
            device=device,
            model=calibration_model,
            exp_cfg=cfg,
            testloader=loader,
            criterion=nn.CrossEntropyLoss(),
            frontend=None,
            checkpoint_path=checkpoint_path,
            checkpoint_epoch=ckpt.get('epoch'),
            checkpoint_best_acc=ckpt.get('best_acc'),
            amp_enabled=False,
        )
        output_ranges = calibrate_adc_ranges(calibration_bundle, max_batches=5)
        print(f"  Calibrated ADC ranges for {len(output_ranges)} analog layers")
        
        # Evaluate multiple runs
        accuracies = []
        n_runs = 10  # Supplement to 10 runs for all bits
        
        for run in range(n_runs):
            set_seed(42 + run)
            model = build_model(cfg, num_classes, img_sz, device)
            model.load_state_dict(ckpt['model_state_dict'])
            
            with ADCQuantHookManager(model, output_ranges, adc_bits=adc_bits):
                acc = evaluate(model, loader, device)
            accuracies.append(acc)
            print(f"  Run {run+1}: {acc:.2f}%")
        
        mean_acc = np.mean(accuracies)
        std_acc = np.std(accuracies) if len(accuracies) > 1 else 0.0
        
        print(f"  Mean: {mean_acc:.2f}% ± {std_acc:.2f}%")
        
        results[f'adc_{adc_bits}bit'] = {
            'mean': float(mean_acc),
            'std': float(std_acc),
            'raw': accuracies
        }
    
    return results

def main():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print("="*70)
    print("ConvNeXt-Tiny ADC Bit-width Sweep")
    print("="*70)
    print(f"Device: {device}")
    
    # Find ConvNeXt checkpoint
    checkpoint_candidates = [
        'checkpoints/C4_4bit_noise_HAT_best.pt',
        'checkpoints/C6_6bit_noise_HAT_best.pt',
    ]
    
    checkpoint_path = None
    for path in checkpoint_candidates:
        if os.path.exists(path):
            checkpoint_path = path
            break
    
    if not checkpoint_path:
        print("ERROR: No ConvNeXt checkpoint found!")
        print("Searched:", checkpoint_candidates)
        sys.exit(1)
    
    print(f"Using checkpoint: {checkpoint_path}")
    
    # Load and show checkpoint info
    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    print(f"Checkpoint best_acc: {ckpt.get('best_acc', 'N/A')}")
    print(f"Checkpoint epoch: {ckpt.get('epoch', 'N/A')}")
    
    # Run on CIFAR-10
    results_cifar10 = run_adc_sweep(checkpoint_path, dataset='cifar10', device=device)
    
    # Run on CIFAR-100 (if available)
    results_cifar100 = {}
    try:
        print("\n" + "="*70)
        print("Testing CIFAR-100...")
        print("="*70)
        results_cifar100 = run_adc_sweep(checkpoint_path, dataset='cifar100', device=device)
    except Exception as e:
        print(f"CIFAR-100 test failed: {e}")
    
    # Save results
    output = {
        'experiment': 'ConvNeXt-Tiny ADC Bit-width Sweep',
        'date': __import__('datetime').datetime.now().isoformat(),
        'checkpoint': checkpoint_path,
        'results': {
            'cifar10': results_cifar10,
            'cifar100': results_cifar100
        },
        'interpretation': {
            'purpose': 'Validate ResNet-18 issue is architecture-specific',
            'key_comparison': 'ConvNeXt should show normal ADC sweep behavior'
        }
    }
    
    output_path = 'report_md/_gpt/convnext_adc_sweep_results.json'
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY - CIFAR-10")
    print("="*70)
    for key, res in results_cifar10.items():
        print(f"{key:15s}: {res['mean']:5.2f}% ± {res['std']:4.2f}%")
    
    if results_cifar100:
        print("\n" + "="*70)
        print("SUMMARY - CIFAR-100")
        print("="*70)
        for key, res in results_cifar100.items():
            print(f"{key:15s}: {res['mean']:5.2f}% ± {res['std']:4.2f}%")
    
    print(f"\nResults saved: {output_path}")
    print("="*70)

if __name__ == '__main__':
    main()
