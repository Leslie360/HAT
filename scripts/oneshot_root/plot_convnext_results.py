#!/usr/bin/env python3
"""Generate ConvNeXt summary plots from GPT-scoped full results."""

import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from report_asset_paths import asset_path, asset_ref


def load_results(json_path='report_md/_gpt/json_gpt/convnext_full_results_gpt.json'):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def plot_accuracy_comparison(results, output_dir='report_md/_gpt'):
    labels = [r['experiment'] for r in results]
    mc_means = [r['mc_mean_acc'] for r in results]
    mc_stds = [r['mc_std_acc'] for r in results]
    best_accs = [r['best_test_acc'] for r in results]

    colors = ['#1f77b4', '#2ca02c', '#d62728', '#ff7f0e',
              '#9467bd', '#17becf', '#8c564b', '#7f7f7f']

    fig, ax = plt.subplots(figsize=(12, 6.5))
    x = np.arange(len(labels))
    bars = ax.bar(x, mc_means, yerr=mc_stds, capsize=5,
                  color=colors[:len(labels)], alpha=0.88,
                  edgecolor='black', linewidth=0.5)

    for bar, best, mc, std in zip(bars, best_accs, mc_means, mc_stds):
        if std > 0:
            text = f'{mc:.2f}±{std:.2f}%'
        else:
            text = f'{best:.2f}%'
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                text, ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax.annotate(f'Noise drop: {mc_means[2] - mc_means[0]:.2f}%',
                xy=(2, mc_means[2]), xytext=(1.2, 73),
                arrowprops=dict(arrowstyle='->', color='#d62728', lw=2),
                color='#d62728', fontsize=10, fontweight='bold')
    ax.annotate(f'HAT recovery: +{mc_means[3] - mc_means[2]:.2f}%',
                xy=(3, mc_means[3]), xytext=(3.8, 92),
                arrowprops=dict(arrowstyle='->', color='#ff7f0e', lw=2),
                color='#ff7f0e', fontsize=10, fontweight='bold')

    ax.set_xlabel('Experiment', fontsize=12)
    ax.set_ylabel('Accuracy (%)', fontsize=12)
    ax.set_title('ConvNeXt-Tiny on CIFAR-10: C1-C8 Hardware Simulation Results', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels([
        'C1\nFP32',
        'C2\n4-bit\nNo Noise',
        'C3\n4-bit\nNoise+Std',
        'C4\n4-bit\nNoise+HAT',
        'C5\n4-bit\nPessimistic',
        'C6\n6-bit\nNoise+HAT',
        'C7\nADC4',
        'C8\nADC6',
    ], fontsize=9)
    ax.set_ylim(60, 93)
    ax.axhline(y=90, color='gray', linestyle='--', alpha=0.35, label='90% reference')
    ax.legend(fontsize=9)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    path = asset_path(output_dir, 'image', 'convnext_accuracy_comparison_gpt.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return path


def plot_retention_curve(retention, output_dir='report_md/_gpt'):
    times = [r['time_s'] for r in retention]
    means = [r['mean_acc'] for r in retention]
    stds = [r['std_acc'] for r in retention]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.errorbar(times, means, yerr=stds, fmt='o-', capsize=4,
                color='#1f77b4', linewidth=2, markersize=6)
    ax.set_xscale('symlog', linthresh=1)
    ax.set_xlabel('Retention Time (s)', fontsize=12)
    ax.set_ylabel('Accuracy (%)', fontsize=12)
    ax.set_title('ConvNeXt C9: Retention Decay from C4 Checkpoint', fontsize=14)
    ax.grid(alpha=0.3, which='both')
    ax.set_ylim(min(means) - 2, max(means) + 2)

    for t, m in zip(times, means):
        ax.text(t, m + 0.35, f'{m:.2f}', fontsize=9, ha='center')

    plt.tight_layout()
    path = asset_path(output_dir, 'image', 'convnext_retention_curve_gpt.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return path


def main():
    data = load_results()
    results = data['results']
    retention = data.get('retention') or []
    output_dir = 'report_md/_gpt'

    acc_path = plot_accuracy_comparison(results, output_dir=output_dir)
    print(f'Saved: {acc_path}')

    if retention:
        retention_path = plot_retention_curve(retention, output_dir=output_dir)
        print(f'Saved: {retention_path}')
        print(f'Markdown ref: {asset_ref(output_dir, "image", "convnext_retention_curve_gpt.png")}')
    print(f'Markdown ref: {asset_ref(output_dir, "image", "convnext_accuracy_comparison_gpt.png")}')


if __name__ == '__main__':
    main()
