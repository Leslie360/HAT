#!/usr/bin/env python3
"""Analyze K4R fresh-instance evaluation results and generate a markdown report.

Usage:
    python analyze_k4r_fresh_eval.py \
        --json report_md/_gpt/json_gpt/cx_k4r_fresh_eval.json \
        --out report_md/_gpt/KIMI_K4R_FRESH_EVAL_REPORT.md
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from statistics import mean, stdev


def fmt(v: float) -> str:
    return f"{v:.2f}"


def analyze(json_path: str, out_path: str | None) -> dict:
    with open(json_path) as f:
        data = json.load(f)

    ckpt = data["checkpoint_path"]
    train_best = data["train_best_acc"]
    train_epoch = data["train_best_epoch"]
    n_inst = data["fresh_instances"]
    n_mc = data["mc_runs_per_instance"]
    cross_mean = data["cross_instance_mean"]
    cross_std = data["cross_instance_std"]
    inst_means = data["instance_means"]
    instances = data["instances"]

    lines = []
    lines.append("# K4R Fresh-Instance Evaluation Report")
    lines.append("")
    lines.append(f"**Generated:** {Path(json_path).stat().st_mtime}")
    lines.append(f"**Checkpoint:** `{ckpt}`")
    lines.append(f"**Train best:** {fmt(train_best)}% (epoch {train_epoch})")
    lines.append("")
    lines.append("## Configuration")
    lines.append("")
    lines.append("| Parameter | Value |")
    lines.append("|:----------|:------|")
    lines.append(f"| Fresh instances | {n_inst} |")
    lines.append(f"| MC runs / instance | {n_mc} |")
    lines.append(f"| Dataset | {data['dataset']} |")
    lines.append(f"| Branch | A canonical (`ab56c2d`) |")
    lines.append(f"| Group | `all` uniform-NL |")
    lines.append(f"| Second-order α | 0.25 |")
    lines.append("")
    lines.append("## Cross-Instance Summary")
    lines.append("")
    lines.append(
        f"**{fmt(cross_mean)} ± {fmt(cross_std)}%** across {n_inst} fresh instances × {n_mc} MC runs"
    )
    lines.append("")

    # Comparison with pre-Branch-A baseline
    lines.append("## Comparison with Pre-Branch-A Baseline")
    lines.append("")
    lines.append("| Metric | Pre-Branch-A `[INVALID]` | K4R (Branch A) |")
    lines.append("|:-------|:-------------------------|:---------------|")
    lines.append(f"| Fresh-instance mean | 86.37% [INVALID] | {fmt(cross_mean)}% |")
    lines.append(f"| Fresh-instance std  | 1.54% [INVALID]  | {fmt(cross_std)}% |")
    lines.append(f"| Same-instance (V4)  | ~91.3%           | {fmt(train_best)}% (train best) |")
    lines.append("")
    lines.append(
        "> **Note:** The pre-Branch-A 86.37% figure was produced with incorrect "
        "second-order Taylor signs (positive `+0.5` instead of negative `-0.5`) "
        "and is **invalid** under Branch A semantics. K4R is the first canonical "
        "experiment."
    )
    lines.append("")

    # Instance breakdown
    lines.append("## Instance-by-Instance Breakdown")
    lines.append("")
    lines.append("| Instance | Seed | Mean Acc (%) | Std (%) | Min | Max |")
    lines.append("|:---------|:-----|:-------------|:--------|:----|:----|")
    for inst in instances:
        idx = inst["instance_index"]
        seed = inst["seed"]
        acc_mean = inst["test_acc_mean"]
        acc_std = inst["test_acc_std"]
        raw = inst["test_acc_raw"]
        lines.append(
            f"| {idx + 1} | {seed} | {fmt(acc_mean)} | {fmt(acc_std)} | "
            f"{fmt(min(raw))} | {fmt(max(raw))} |"
        )
    lines.append("")

    # Distribution stats
    lines.append("## Distribution Statistics")
    lines.append("")
    lines.append(f"- **Mean of instance means:** {fmt(cross_mean)}%")
    lines.append(f"- **Std of instance means:** {fmt(cross_std)}%")
    lines.append(f"- **Min instance mean:** {fmt(min(inst_means))}%")
    lines.append(f"- **Max instance mean:** {fmt(max(inst_means))}%")
    lines.append(f"- **Range:** {max(inst_means) - min(inst_means):.2f} pp")
    lines.append("")

    # Interpretation
    lines.append("## Interpretation")
    lines.append("")
    if cross_mean >= 85.0:
        lines.append(
            "✅ **Result meets or exceeds the pre-Branch-A nominal threshold.** "
            "The sign-corrected second-order brake (`-0.5`) with `α=0.25` does not "
            "degrade fresh-instance transfer relative to the (invalid) baseline."
        )
    elif cross_mean >= 80.0:
        lines.append(
            "⚠️ **Result is within ~5 pp of the pre-Branch-A nominal threshold.** "
            "Further hyperparameter tuning (α sweep, δg_eff adjustment) may improve."
        )
    else:
        lines.append(
            "❌ **Result falls well below the pre-Branch-A nominal threshold.** "
            "The sign-corrected second-order brake may be too aggressive, or "
            "additional regularization (domain randomization, larger ensemble) "
            "may be needed."
        )
    lines.append("")

    # Next steps
    lines.append("## Recommended Next Steps")
    lines.append("")
    lines.append("1. Compare with `group=mlp` diagnostic run to isolate NL sensitivity.")
    lines.append("2. Sweep α ∈ {0.1, 0.25, 0.5, 1.0} to identify optimal brake strength.")
    lines.append("3. If result < 85%, consider joint MLP-linear + Ensemble HAT training.")
    lines.append("4. Archive this report and update `CODEX` with the canonical number.")
    lines.append("")

    md = "\n".join(lines)

    if out_path:
        Path(out_path).parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w") as f:
            f.write(md)
        print(f"Report written to: {out_path}")

    print(md)
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", required=True, help="Path to eval JSON output")
    parser.add_argument("--out", default=None, help="Path to write markdown report")
    args = parser.parse_args()
    analyze(args.json, args.out)


if __name__ == "__main__":
    main()
