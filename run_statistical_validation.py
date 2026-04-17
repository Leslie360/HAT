"""
Statistical Significance Validation

Runs 10 independent trials for key configurations
Reports mean ± std with 95% confidence intervals
"""

import torch
import torch.nn as nn
import numpy as np
import sys
import dataclasses
import json
from datetime import datetime
from scipy import stats

sys.path.insert(0, '/home/qiaosir/projects/compute_vit')
sys.stdout.reconfigure(line_buffering=True)

from train_tinyvit import (
    build_model, evaluate, get_dataloaders, set_seed,
    TinyViTExperimentConfig, DATASET_STATS
)

def run_multiple_seeds(config, dataset='cifar10', num_runs=10, device='cuda'):
    """Run experiment with multiple random seeds"""
    
    accuracies = []
    _, loader = get_dataloaders(dataset, batch_size=256)
    criterion = nn.CrossEntropyLoss()
    
    checkpoint_path = 'checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt'
    
    print(f"\nRunning {num_runs} independent trials...")
    print("-" * 50)
    
    for run in range(num_runs):
        seed = 42 + run * 10
        set_seed(seed)
        
        # Load model
        ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
        exp_cfg_dict = ckpt.get('exp_cfg', {})
        valid_keys = {f.name for f in dataclasses.fields(TinyViTExperimentConfig)}
        filtered = {k: v for k, v in exp_cfg_dict.items() if k in valid_keys}
        cfg = TinyViTExperimentConfig(**filtered)
        
        # Apply config overrides
        for k, v in config.items():
            setattr(cfg, k, v)
        
        model = build_model(cfg, num_classes=10, device=device)
        model.load_state_dict(ckpt['model_state_dict'])
        
        # Resample D2D for fresh instance
        for m in model.modules():
            if hasattr(m, 'resample_d2d_noise') and callable(m.resample_d2d_noise):
                m.resample_d2d_noise()
        
        # Evaluate
        _, acc = evaluate(model, loader, criterion, device, cfg)
        accuracies.append(acc)
        
        print(f"  Run {run+1}/{num_runs}: {acc:.2f}%")
    
    # Statistics
    mean_acc = np.mean(accuracies)
    std_acc = np.std(accuracies, ddof=1)
    sem = std_acc / np.sqrt(num_runs)
    ci_95 = 1.96 * sem
    
    # 95% confidence interval
    ci_lower = mean_acc - ci_95
    ci_upper = mean_acc + ci_95
    
    print(f"\n{'='*50}")
    print(f"Statistics (n={num_runs}):")
    print(f"  Mean: {mean_acc:.2f}%")
    print(f"  Std: {std_acc:.2f}%")
    print(f"  95% CI: [{ci_lower:.2f}%, {ci_upper:.2f}%]")
    print(f"  Raw: {[f'{a:.2f}' for a in accuracies]}")
    
    return {
        'mean': float(mean_acc),
        'std': float(std_acc),
        'ci_95_lower': float(ci_lower),
        'ci_95_upper': float(ci_upper),
        'sem': float(sem),
        'raw': [float(a) for a in accuracies]
    }

def main():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    print("="*70)
    print("Statistical Significance Validation")
    print("="*70)
    print(f"Device: {device}")
    
    results = {}
    
    # Test 1: Ensemble HAT (standard)
    print("\n" + "="*70)
    print("Test 1: Ensemble HAT (10 fresh instances)")
    print("="*70)
    
    config1 = {
        'noise_enabled': True,
        'hat_training': True,
        'sigma_c2c': 0.05,
        'sigma_d2d': 0.10,
    }
    results['ensemble_hat_10runs'] = run_multiple_seeds(config1, num_runs=10, device=device)
    
    # Test 2: i.i.d. noise (comparison)
    print("\n" + "="*70)
    print("Test 2: i.i.d. Noise (10 runs)")
    print("="*70)
    
    config2 = {
        'noise_enabled': True,
        'hat_training': False,  # No spatial structure
        'sigma_c2c': 0.10,
        'sigma_d2d': 0.0,
    }
    results['iid_noise_10runs'] = run_multiple_seeds(config2, num_runs=10, device=device)
    
    # Statistical test
    print("\n" + "="*70)
    print("Statistical Comparison")
    print("="*70)
    
    ensemble_acc = results['ensemble_hat_10runs']['raw']
    iid_acc = results['iid_noise_10runs']['raw']
    
    # T-test
    t_stat, p_value = stats.ttest_ind(ensemble_acc, iid_acc)
    
    print(f"\nEnsemble HAT vs i.i.d. Noise:")
    print(f"  Ensemble: {np.mean(ensemble_acc):.2f}% ± {np.std(ensemble_acc):.2f}%")
    print(f"  i.i.d.: {np.mean(iid_acc):.2f}% ± {np.std(iid_acc):.2f}%")
    print(f"  T-statistic: {t_stat:.3f}")
    print(f"  P-value: {p_value:.4f}")
    
    if p_value < 0.05:
        print(f"  ✓ Significant difference (p < 0.05)")
    else:
        print(f"  ✗ No significant difference (p >= 0.05)")
    
    # Effect size (Cohen's d)
    pooled_std = np.sqrt((np.var(ensemble_acc, ddof=1) + np.var(iid_acc, ddof=1)) / 2)
    cohens_d = (np.mean(ensemble_acc) - np.mean(iid_acc)) / pooled_std
    print(f"  Cohen's d: {cohens_d:.3f}")
    
    # Save results
    output = {
        'experiment': 'Statistical Significance Validation',
        'date': datetime.now().isoformat(),
        'results': results,
        'statistical_test': {
            'comparison': 'Ensemble HAT vs i.i.d. Noise',
            't_statistic': float(t_stat),
            'p_value': float(p_value),
            'cohens_d': float(cohens_d),
            'significant': bool(p_value < 0.05)
        }
    }
    
    with open('report_md/_gpt/statistical_validation_results.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults saved: report_md/_gpt/statistical_validation_results.json")
    print("="*70)

if __name__ == '__main__':
    main()
