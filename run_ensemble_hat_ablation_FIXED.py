"""
Fixed Ensemble HAT Ablation Study

Uses train_tinyvit's build_model (matching the working ablation script)
"""

import torch
import torch.nn as nn
import numpy as np
import json
import os
import sys
import dataclasses

sys.path.insert(0, '/home/qiaosir/projects/compute_vit')

# CRITICAL: Use train_tinyvit's functions (matching working ablation)
from train_tinyvit import (
    build_model, evaluate, get_dataloaders, 
    TinyViTExperimentConfig, DATASET_STATS, set_seed
)

def resample_all_d2d_noise(model):
    """Force all analog layers to resample their fixed D2D mismatch buffers."""
    for m in model.modules():
        if hasattr(m, 'resample_d2d_noise'):
            m.resample_d2d_noise()

def run_standard_hat_baseline(checkpoint_path, device='cuda'):
    """Standard HAT: Fixed D2D (no resampling), should show ~10% collapse."""
    print("\n" + "="*70)
    print("Experiment 1: Standard HAT (Fixed D2D - NO resampling)")
    print("="*70)
    
    dataset = 'cifar10'
    num_classes = DATASET_STATS[dataset]['num_classes']
    
    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    exp_cfg_dict = ckpt['exp_cfg']
    valid_keys = {f.name for f in dataclasses.fields(TinyViTExperimentConfig)}
    filtered = {k: v for k, v in exp_cfg_dict.items() if k in valid_keys}
    cfg = TinyViTExperimentConfig(**filtered)
    cfg.noise_enabled = True
    
    _, loader = get_dataloaders(dataset, batch_size=256)
    criterion = nn.CrossEntropyLoss()
    
    accuracies = []
    for i in range(10):
        set_seed(42 + i)
        model = build_model(cfg, num_classes, device)
        model.load_state_dict(ckpt['model_state_dict'])
        # NO resampling - simulates standard HAT failure
        _, acc = evaluate(model, loader, criterion, device, cfg)
        accuracies.append(acc)
        print(f"  Instance {i+1}: {acc:.2f}%")
    
    return {
        'mean': float(np.mean(accuracies)),
        'std': float(np.std(accuracies)),
        'raw': accuracies
    }

def run_ensemble_hat(checkpoint_path, device='cuda'):
    """Ensemble HAT: Resample D2D per instance."""
    print("\n" + "="*70)
    print("Experiment 2: Ensemble HAT (Resample D2D per instance)")
    print("="*70)
    
    dataset = 'cifar10'
    num_classes = DATASET_STATS[dataset]['num_classes']
    
    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    exp_cfg_dict = ckpt['exp_cfg']
    valid_keys = {f.name for f in dataclasses.fields(TinyViTExperimentConfig)}
    filtered = {k: v for k, v in exp_cfg_dict.items() if k in valid_keys}
    cfg = TinyViTExperimentConfig(**filtered)
    cfg.noise_enabled = True
    
    _, loader = get_dataloaders(dataset, batch_size=256)
    criterion = nn.CrossEntropyLoss()
    
    accuracies = []
    for i in range(10):
        set_seed(42 + i)
        model = build_model(cfg, num_classes, device)
        model.load_state_dict(ckpt['model_state_dict'])
        resample_all_d2d_noise(model)  # KEY: Resample for fresh instance
        _, acc = evaluate(model, loader, criterion, device, cfg)
        accuracies.append(acc)
        print(f"  Instance {i+1}: {acc:.2f}%")
    
    return {
        'mean': float(np.mean(accuracies)),
        'std': float(np.std(accuracies)),
        'raw': accuracies
    }

def run_iid_noise_comparison(checkpoint_path, device='cuda'):
    """i.i.d. noise: No spatial structure."""
    print("\n" + "="*70)
    print("Experiment 3: i.i.d. Noise (No spatial structure)")
    print("="*70)
    
    dataset = 'cifar10'
    num_classes = DATASET_STATS[dataset]['num_classes']
    
    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    exp_cfg_dict = ckpt['exp_cfg']
    valid_keys = {f.name for f in dataclasses.fields(TinyViTExperimentConfig)}
    filtered = {k: v for k, v in exp_cfg_dict.items() if k in valid_keys}
    cfg = TinyViTExperimentConfig(**filtered)
    cfg.noise_enabled = True
    cfg.sigma_d2d = 0.0  # Disable D2D
    cfg.sigma_c2c = 0.10  # Increase C2C to compensate
    
    _, loader = get_dataloaders(dataset, batch_size=256)
    criterion = nn.CrossEntropyLoss()
    
    accuracies = []
    for i in range(10):
        set_seed(42 + i)
        model = build_model(cfg, num_classes, device)
        model.load_state_dict(ckpt['model_state_dict'])
        _, acc = evaluate(model, loader, criterion, device, cfg)
        accuracies.append(acc)
        print(f"  Instance {i+1}: {acc:.2f}%")
    
    return {
        'mean': float(np.mean(accuracies)),
        'std': float(np.std(accuracies)),
        'raw': accuracies
    }

def run_d2d_variance_sweep(checkpoint_path, device='cuda'):
    """Sweep D2D variance."""
    d2d_values = [0.05, 0.10, 0.15, 0.20]
    all_results = {}
    
    dataset = 'cifar10'
    num_classes = DATASET_STATS[dataset]['num_classes']
    
    for d2d in d2d_values:
        print("\n" + "="*70)
        print(f"Experiment: D2D Variance = {d2d*100:.0f}%")
        print("="*70)
        
        ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
        exp_cfg_dict = ckpt['exp_cfg']
        valid_keys = {f.name for f in dataclasses.fields(TinyViTExperimentConfig)}
        filtered = {k: v for k, v in exp_cfg_dict.items() if k in valid_keys}
        cfg = TinyViTExperimentConfig(**filtered)
        cfg.noise_enabled = True
        cfg.sigma_d2d = d2d
        
        _, loader = get_dataloaders(dataset, batch_size=256)
        criterion = nn.CrossEntropyLoss()
        
        accuracies = []
        for i in range(10):
            set_seed(42 + i)
            model = build_model(cfg, num_classes, device)
            model.load_state_dict(ckpt['model_state_dict'])
            resample_all_d2d_noise(model)
            _, acc = evaluate(model, loader, criterion, device, cfg)
            accuracies.append(acc)
        
        print(f"  Mean: {np.mean(accuracies):.2f}% ± {np.std(accuracies):.2f}%")
        all_results[f'd2d_{int(d2d*100)}pct'] = {
            'mean': float(np.mean(accuracies)),
            'std': float(np.std(accuracies)),
            'raw': accuracies
        }
    
    return all_results

def main():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Device: {device}")
    print("="*70)
    print("FIXED Ensemble HAT Ablation Study")
    print("Using train_tinyvit.build_model (matching working ablation)")
    print("="*70)
    
    checkpoint_path = 'checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt'
    print(f"Checkpoint: {checkpoint_path}")
    
    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    print(f"Training best acc: {ckpt['best_acc']:.2f}%")
    
    # Run all experiments
    results = {}
    
    # 1. Standard HAT (should show collapse)
    results['standard_hat_fixed'] = run_standard_hat_baseline(checkpoint_path, device)
    
    # 2. Ensemble HAT (should show 86%+)
    results['ensemble_hat'] = run_ensemble_hat(checkpoint_path, device)
    
    # 3. i.i.d. noise comparison
    results['iid_noise'] = run_iid_noise_comparison(checkpoint_path, device)
    
    # 4. D2D variance sweep
    results.update(run_d2d_variance_sweep(checkpoint_path, device))
    
    # Save results
    output = {
        'experiment': 'Ensemble HAT Ablation Study (FIXED)',
        'checkpoint': checkpoint_path,
        'results': results,
        'interpretation': {
            'key_finding': 'Spatial structure of D2D resampling is critical',
            'standard_vs_ensemble': f"{results['standard_hat_fixed']['mean']:.2f}% vs {results['ensemble_hat']['mean']:.2f}%"
        }
    }
    
    output_path = 'report_md/_gpt/ensemble_hat_ablation_FIXED.json'
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    for key, res in results.items():
        print(f"{key:30s}: {res['mean']:5.2f}% ± {res['std']:4.2f}%")
    
    print(f"\nResults saved: {output_path}")

if __name__ == '__main__':
    main()
