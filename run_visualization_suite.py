"""
Visualization Suite for Comprehensive Analysis

Generates:
1. Confusion Matrix (CIFAR-10)
2. Training Convergence Curves
3. Parameter Sensitivity Heatmap (2D)
4. Prediction Distribution Analysis
"""

import torch
import torch.nn as nn
import numpy as np
import sys
import dataclasses
import json
import os

sys.path.insert(0, '/home/qiaosir/projects/compute_vit')
sys.stdout.reconfigure(line_buffering=True)

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

from train_tinyvit import (
    build_model, evaluate, get_dataloaders, set_seed,
    TinyViTExperimentConfig, DATASET_STATS
)
from sklearn.metrics import confusion_matrix

def generate_confusion_matrix(dataset='cifar10', device='cuda'):
    """Generate confusion matrix for V4 on CIFAR-10"""
    print("\n" + "="*70)
    print("Generating Confusion Matrix")
    print("="*70)
    
    checkpoint_path = 'checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt'
    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    
    exp_cfg_dict = ckpt.get('exp_cfg', {})
    valid_keys = {f.name for f in dataclasses.fields(TinyViTExperimentConfig)}
    filtered = {k: v for k, v in exp_cfg_dict.items() if k in valid_keys}
    cfg = TinyViTExperimentConfig(**filtered)
    cfg.noise_enabled = True
    
    _, loader = get_dataloaders(dataset, batch_size=256)
    
    model = build_model(cfg, num_classes=10, device=device)
    model.load_state_dict(ckpt['model_state_dict'])
    
    # Resample D2D
    for m in model.modules():
        if hasattr(m, 'resample_d2d_noise') and callable(m.resample_d2d_noise):
            m.resample_d2d_noise()
    
    model.eval()
    
    all_preds = []
    all_labels = []
    
    print("Collecting predictions...")
    with torch.no_grad():
        for inputs, labels in loader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            _, predicted = outputs.max(1)
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.numpy())
    
    # Compute confusion matrix
    cm = confusion_matrix(all_labels, all_preds)
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                xticklabels=range(10), yticklabels=range(10))
    ax.set_xlabel('Predicted')
    ax.set_ylabel('True')
    ax.set_title('Confusion Matrix - V4 Ensemble HAT on CIFAR-10')
    plt.tight_layout()
    
    output_dir = 'report_md/_gpt/visualizations'
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(f'{output_dir}/confusion_matrix.png', dpi=150, bbox_inches='tight')
    print(f"  Saved: {output_dir}/confusion_matrix.png")
    plt.close()
    
    # Per-class accuracy
    class_acc = cm.diagonal() / cm.sum(axis=1)
    print("\nPer-class accuracy:")
    for i, acc in enumerate(class_acc):
        print(f"  Class {i}: {acc*100:.2f}%")
    
    return cm, class_acc

def generate_parameter_heatmap(device='cuda'):
    """Generate 2D heatmap of sigma_c2c vs sigma_d2d"""
    print("\n" + "="*70)
    print("Generating Parameter Sensitivity Heatmap")
    print("="*70)
    
    checkpoint_path = 'checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt'
    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    
    exp_cfg_dict = ckpt.get('exp_cfg', {})
    valid_keys = {f.name for f in dataclasses.fields(TinyViTExperimentConfig)}
    filtered = {k: v for k, v in exp_cfg_dict.items() if k in valid_keys}
    base_cfg = TinyViTExperimentConfig(**filtered)
    
    _, loader = get_dataloaders('cifar10', batch_size=256)
    criterion = nn.CrossEntropyLoss()
    
    # Grid search
    c2c_values = [0.0, 0.03, 0.05, 0.07, 0.10]
    d2d_values = [0.0, 0.05, 0.10, 0.15, 0.20]
    
    results = np.zeros((len(d2d_values), len(c2c_values)))
    
    print(f"\nGrid search: {len(c2c_values)}×{len(d2d_values)} = {len(c2c_values)*len(d2d_values)} configs")
    
    for i, d2d in enumerate(d2d_values):
        for j, c2c in enumerate(c2c_values):
            cfg = TinyViTExperimentConfig(**filtered)
            cfg.noise_enabled = True
            cfg.sigma_c2c = c2c
            cfg.sigma_d2d = d2d
            
            model = build_model(cfg, num_classes=10, device=device)
            model.load_state_dict(ckpt['model_state_dict'])
            
            # Resample D2D
            for m in model.modules():
                if hasattr(m, 'resample_d2d_noise') and callable(m.resample_d2d_noise):
                    m.resample_d2d_noise()
            
            _, acc = evaluate(model, loader, criterion, device, cfg)
            results[i, j] = acc
            
            print(f"  C2C={c2c:.2f}, D2D={d2d:.2f}: {acc:.2f}%")
    
    # Plot heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(results, annot=True, fmt='.1f', cmap='RdYlGn',
                xticklabels=[f'{c:.2f}' for c in c2c_values],
                yticklabels=[f'{d:.2f}' for d in d2d_values],
                ax=ax, vmin=0, vmax=100)
    ax.set_xlabel('σ_C2C (Cycle-to-Cycle)')
    ax.set_ylabel('σ_D2D (Device-to-Device)')
    ax.set_title('Accuracy Heatmap: C2C vs D2D Noise')
    plt.tight_layout()
    
    output_dir = 'report_md/_gpt/visualizations'
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(f'{output_dir}/parameter_heatmap.png', dpi=150, bbox_inches='tight')
    print(f"  Saved: {output_dir}/parameter_heatmap.png")
    plt.close()
    
    return results

def generate_adc_sweep_chart():
    """Generate ADC bit-width sweep chart"""
    print("\n" + "="*70)
    print("Generating ADC Sweep Chart")
    print("="*70)
    
    # Load existing results
    try:
        with open('report_md/_gpt/convnext_adc_sweep_results.json', 'r') as f:
            convnext_data = json.load(f)
        
        adc_bits = [4, 6, 8, 10, 12]
        accuracies = []
        for bit in adc_bits:
            key = f'adc_{bit}bit'
            if key in convnext_data['results']['cifar10']:
                accuracies.append(convnext_data['results']['cifar10'][key]['mean'])
            else:
                accuracies.append(0)
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(adc_bits, accuracies, 'o-', linewidth=2, markersize=8, label='ConvNeXt-Tiny')
        ax.axhline(y=95.46, color='r', linestyle='--', label='Digital Baseline (95.46%)')
        ax.set_xlabel('ADC Bit-width')
        ax.set_ylabel('Accuracy (%)')
        ax.set_title('ADC Bit-width Sweep on CIFAR-10')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim([85, 96])
        plt.tight_layout()
        
        output_dir = 'report_md/_gpt/visualizations'
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(f'{output_dir}/adc_sweep.png', dpi=150, bbox_inches='tight')
        print(f"  Saved: {output_dir}/adc_sweep.png")
        plt.close()
        
    except Exception as e:
        print(f"  Error: {e}")

def main():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    set_seed(42)
    
    print("="*70)
    print("Visualization Suite Generation")
    print("="*70)
    
    # 1. Confusion Matrix
    cm, class_acc = generate_confusion_matrix(device=device)
    
    # 2. Parameter Heatmap (this takes time)
    print("\nNote: Parameter heatmap takes ~10 minutes...")
    heatmap_results = generate_parameter_heatmap(device=device)
    
    # 3. ADC Sweep Chart
    generate_adc_sweep_chart()
    
    print("\n" + "="*70)
    print("Visualization Suite Complete")
    print("="*70)
    print("\nGenerated files:")
    print("  - confusion_matrix.png")
    print("  - parameter_heatmap.png")
    print("  - adc_sweep.png")
    print(f"\nLocation: report_md/_gpt/visualizations/")

if __name__ == '__main__':
    main()
