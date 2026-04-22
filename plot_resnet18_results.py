#!/usr/bin/env python3
"""
Generate plots for A2.1 ResNet-18 experiment results.

Deliverables:
  1. Bar chart: R1-R6 accuracy comparison
  2. R4 training curves (loss + accuracy vs epoch)
"""

import json
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from report_asset_paths import asset_path


def load_results(json_path='report_md/json/resnet18_results.json'):
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data['results'], data['histories']


def plot_accuracy_comparison(results, output_dir='report_md'):
    """Bar chart: R1-R6 best test accuracy comparison."""
    fig, ax = plt.subplots(figsize=(10, 6))

    labels = [r['experiment'] for r in results]
    accs = [r['best_test_acc'] for r in results]
    mc_means = [r['mc_mean_acc'] for r in results]
    mc_stds = [r['mc_std_acc'] for r in results]

    colors = ['#2196F3', '#4CAF50', '#F44336', '#FF9800', '#9C27B0', '#00BCD4']

    x = np.arange(len(labels))
    bars = ax.bar(x, mc_means, yerr=mc_stds, capsize=5, color=colors, alpha=0.85,
                  edgecolor='black', linewidth=0.5)

    # Add value labels on bars
    for bar, acc, mc, std in zip(bars, accs, mc_means, mc_stds):
        height = bar.get_height()
        if std > 0:
            label = f'{mc:.1f}±{std:.1f}%'
        else:
            label = f'{acc:.1f}%'
        ax.text(bar.get_x() + bar.get_width()/2., height + 1.5,
                label, ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Annotations for key comparisons
    ax.annotate('', xy=(0, accs[0]+0.5), xytext=(1, accs[1]+0.5),
                arrowprops=dict(arrowstyle='<->', color='gray', lw=1.5))
    ax.text(0.5, max(accs[0], accs[1])+2.5, f'Δ={accs[1]-accs[0]:.1f}%',
            ha='center', fontsize=8, color='gray')

    # R3→R4 arrow (core result)
    mid_y = (mc_means[2] + mc_means[3]) / 2
    ax.annotate(f'HAT: +{mc_means[3]-mc_means[2]:.1f}%',
                xy=(3, mc_means[3]-2), xytext=(2.5, 55),
                fontsize=10, fontweight='bold', color='#FF9800',
                arrowprops=dict(arrowstyle='->', color='#FF9800', lw=2))

    ax.set_xlabel('Experiment', fontsize=12)
    ax.set_ylabel('Test Accuracy (%)', fontsize=12)
    ax.set_title('ResNet-18 on CIFAR-10: Hardware Simulation Experiments', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels([
        'R1\nFP32\nBaseline',
        'R2\n4-bit\nNo Noise',
        'R3\n4-bit\nNoise+Std',
        'R4\n4-bit\nNoise+HAT',
        'R5\n4-bit\nPessimistic',
        'R6\n6-bit\nNoise+HAT',
    ], fontsize=9)
    ax.set_ylim(0, 105)
    ax.axhline(y=90, color='gray', linestyle='--', alpha=0.3, label='90% threshold')
    ax.legend(fontsize=9)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    path = asset_path(output_dir, 'image', 'resnet18_accuracy_comparison.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    print(f"Saved: {path}")
    plt.close(fig)


def plot_r4_training_curves(histories, output_dir='report_md'):
    """R4 training curves: loss and accuracy vs epoch."""
    if 'R4' not in histories:
        print("R4 history not found, skipping training curves plot.")
        return

    h = histories['R4']
    epochs = range(len(h['train_loss']))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Loss curves
    ax1.plot(epochs, h['train_loss'], label='Train Loss', color='#2196F3', linewidth=1.5)
    ax1.plot(epochs, h['test_loss'], label='Test Loss', color='#F44336', linewidth=1.5)
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.set_title('R4 (4-bit HAT): Training & Test Loss')
    ax1.legend()
    ax1.grid(alpha=0.3)
    ax1.set_yscale('log')

    # Accuracy curves
    ax2.plot(epochs, h['train_acc'], label='Train Accuracy', color='#2196F3', linewidth=1.5)
    ax2.plot(epochs, h['test_acc'], label='Test Accuracy', color='#F44336', linewidth=1.5)
    ax2.axhline(y=90, color='gray', linestyle='--', alpha=0.5, label='90% target')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy (%)')
    ax2.set_title('R4 (4-bit HAT): Training & Test Accuracy')
    ax2.legend()
    ax2.grid(alpha=0.3)
    ax2.set_ylim(0, 105)

    plt.tight_layout()
    path = asset_path(output_dir, 'image', 'resnet18_R4_training_curves.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    print(f"Saved: {path}")
    plt.close(fig)


def plot_all_training_curves(histories, output_dir='report_md'):
    """All experiments accuracy curves on one plot for comparison."""
    fig, ax = plt.subplots(figsize=(10, 6))

    colors = {
        'R1': '#2196F3', 'R2': '#4CAF50', 'R3': '#F44336',
        'R4': '#FF9800', 'R5': '#9C27B0', 'R6': '#00BCD4'
    }
    labels = {
        'R1': 'R1: FP32 Baseline',
        'R2': 'R2: 4-bit, No Noise',
        'R3': 'R3: 4-bit, Noise (Std Train)',
        'R4': 'R4: 4-bit, Noise (HAT)',
        'R5': 'R5: 4-bit, Pessimistic (HAT)',
        'R6': 'R6: 6-bit, Noise (HAT)',
    }

    for exp_id, h in histories.items():
        epochs = range(len(h['test_acc']))
        ax.plot(epochs, h['test_acc'], label=labels.get(exp_id, exp_id),
                color=colors.get(exp_id, 'gray'), linewidth=1.5, alpha=0.9)

    ax.set_xlabel('Epoch', fontsize=12)
    ax.set_ylabel('Test Accuracy (%)', fontsize=12)
    ax.set_title('ResNet-18 CIFAR-10: All Experiments Test Accuracy', fontsize=14)
    ax.legend(fontsize=9, loc='lower right')
    ax.grid(alpha=0.3)
    ax.set_ylim(0, 100)

    plt.tight_layout()
    path = asset_path(output_dir, 'image', 'resnet18_all_training_curves.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    print(f"Saved: {path}")
    plt.close(fig)


if __name__ == '__main__':
    results, histories = load_results()
    plot_accuracy_comparison(results)
    plot_r4_training_curves(histories)
    plot_all_training_curves(histories)
    print("\nAll plots generated.")
