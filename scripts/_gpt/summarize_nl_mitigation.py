#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt

ROOT = Path('/home/qiaosir/projects/compute_vit')
JSON_DIR = ROOT / 'report_md/_gpt/json_gpt'
CSV_DIR = ROOT / 'report_md/_gpt/csv_gpt'
OUT_MD = ROOT / 'report_md/_gpt/NL_MITIGATION_SUMMARY_20260418.md'
OUT_JSON = JSON_DIR / 'nl_mitigation_summary_20260418.json'
OUT_CSV = CSV_DIR / 'nl_mitigation_summary_20260418.csv'
OUT_PNG = ROOT / 'report_md/_gpt/nl_mitigation_summary_20260418.png'

SOURCES = [
    {
        'label': 'Severe NL baseline',
        'kind': 'baseline_eval',
        'path': JSON_DIR / 'v4_nl2_hat_eval_results_gpt.json',
    },
    {
        'label': 'MLP-only linear compensation',
        'kind': 'train_result',
        'path': JSON_DIR / 'v4_nl2_mlp_linear_comp_train_results_gpt.json',
    },
    {
        'label': 'QKV-only linear compensation',
        'kind': 'train_result',
        'path': JSON_DIR / 'v4_nl2_qkv_linear_comp_train_results_gpt.json',
    },
    {
        'label': 'All-analog linear compensation',
        'kind': 'train_result',
        'path': JSON_DIR / 'v4_nl2_all_linear_comp_train_results_gpt.json',
    },
]

GRAD_PATH = JSON_DIR / 'nl_gradient_distortion_gpt.json'


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))


def summarize_source(src: dict[str, Any]) -> dict[str, Any]:
    row = {
        'label': src['label'],
        'kind': src['kind'],
        'path': str(src['path']),
        'exists': src['path'].exists(),
        'best_test_acc': None,
        'best_epoch': None,
        'mean_eval_acc': None,
        'std_eval_acc': None,
        'experiment_name': None,
    }
    if not src['path'].exists():
        return row
    obj = load_json(src['path'])
    if src['kind'] == 'baseline_eval':
        if isinstance(obj, dict) and 'results' in obj:
            # defensive in case structure changes
            obj = obj['results']
        if isinstance(obj, list) and obj:
            item = obj[0]
        elif isinstance(obj, dict):
            item = obj
        else:
            return row
        row['experiment_name'] = item.get('experiment_name')
        row['mean_eval_acc'] = item.get('test_acc_mean')
        row['std_eval_acc'] = item.get('test_acc_std')
        row['best_test_acc'] = item.get('test_acc_mean')
    elif src['kind'] == 'train_result':
        if isinstance(obj, list) and obj:
            item = obj[0]
        elif isinstance(obj, dict):
            item = obj
        else:
            return row
        row['experiment_name'] = item.get('experiment_name')
        row['best_test_acc'] = item.get('best_test_acc')
        row['best_epoch'] = item.get('best_epoch')
    return row


def load_gradient_summary() -> dict[str, Any]:
    summary = {
        'mlp_affected_grad_cosine_mean': None,
        'mlp_affected_grad_norm_ratio_mean': None,
        'qkv_affected_grad_cosine_mean': None,
        'qkv_affected_grad_norm_ratio_mean': None,
        'all_affected_grad_cosine_mean': None,
        'all_affected_grad_norm_ratio_mean': None,
    }
    if not GRAD_PATH.exists():
        return summary
    obj = load_json(GRAD_PATH)
    results = obj.get('results', []) if isinstance(obj, dict) else []
    for item in results:
        gid = item.get('group_id')
        if gid == 'M':
            summary['mlp_affected_grad_cosine_mean'] = item.get('affected_grad_cosine_mean')
            summary['mlp_affected_grad_norm_ratio_mean'] = item.get('affected_grad_norm_ratio_mean')
        elif gid == 'QKV':
            summary['qkv_affected_grad_cosine_mean'] = item.get('affected_grad_cosine_mean')
            summary['qkv_affected_grad_norm_ratio_mean'] = item.get('affected_grad_norm_ratio_mean')
        elif gid == 'ALL':
            summary['all_affected_grad_cosine_mean'] = item.get('affected_grad_cosine_mean')
            summary['all_affected_grad_norm_ratio_mean'] = item.get('affected_grad_norm_ratio_mean')
    return summary


def write_csv(rows: list[dict[str, Any]]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_md(rows: list[dict[str, Any]], grad: dict[str, Any]) -> None:
    lines = [
        '# NL Mitigation Summary',
        '',
        '| Condition | Exists | Best / Mean acc (%) | Best epoch | Source |',
        '|:--|:--:|--:|--:|:--|',
    ]
    for row in rows:
        acc = row['best_test_acc'] if row['best_test_acc'] is not None else ''
        epoch = row['best_epoch'] if row['best_epoch'] is not None else ''
        lines.append(f"| {row['label']} | {'yes' if row['exists'] else 'no'} | {acc} | {epoch} | `{Path(row['path']).name}` |")
    lines += [
        '',
        '## Gradient diagnostic anchors',
        '',
        f"- MLP affected-grad cosine: `{grad['mlp_affected_grad_cosine_mean']}`",
        f"- MLP affected-grad norm ratio: `{grad['mlp_affected_grad_norm_ratio_mean']}`",
        f"- QKV affected-grad cosine: `{grad['qkv_affected_grad_cosine_mean']}`",
        f"- QKV affected-grad norm ratio: `{grad['qkv_affected_grad_norm_ratio_mean']}`",
        f"- All-analog affected-grad cosine: `{grad['all_affected_grad_cosine_mean']}`",
        f"- All-analog affected-grad norm ratio: `{grad['all_affected_grad_norm_ratio_mean']}`",
        '',
        'Interpretation: compare the finished mitigation runs against the severe NL baseline and the gradient-localization evidence before promoting any result into the manuscript.',
        '',
    ]
    OUT_MD.write_text('\n'.join(lines), encoding='utf-8')


def write_plot(rows: list[dict[str, Any]]) -> None:
    labels = []
    values = []
    colors = []
    for row in rows:
        if row['best_test_acc'] is None:
            continue
        labels.append(row['label'])
        values.append(float(row['best_test_acc']))
        colors.append('#c44e52' if 'baseline' in row['label'].lower() else '#4c72b0')
    if not values:
        return
    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    bars = ax.bar(labels, values, color=colors, edgecolor='#222222', linewidth=1.0)
    ax.set_ylabel('Accuracy (%)')
    ax.set_title('Severe-NL mitigation controls')
    ax.set_ylim(0, max(values) + 10)
    ax.grid(axis='y', linestyle=':', linewidth=0.8, color='#BBBBBB', alpha=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(axis='x', rotation=15)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2.0, val + 0.8, f'{val:.2f}', ha='center', va='bottom', fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=300, bbox_inches='tight')
    plt.close(fig)


def main() -> None:
    rows = [summarize_source(src) for src in SOURCES]
    grad = load_gradient_summary()
    payload = {'rows': rows, 'gradient_summary': grad}
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2), encoding='utf-8')
    write_csv(rows)
    write_md(rows, grad)
    write_plot(rows)
    print(json.dumps({'json': str(OUT_JSON), 'csv': str(OUT_CSV), 'md': str(OUT_MD), 'png': str(OUT_PNG)}, indent=2))


if __name__ == '__main__':
    main()
