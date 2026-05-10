#!/usr/bin/env python3
"""Regenerate post-fix M-series figures from audited fresh-eval JSON files."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from statistics import mean, stdev

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
JSON_DIR = ROOT / "report_md/_gpt/json_gpt"
FIG_DIR = ROOT / "paper/figures"
REPORT = ROOT / "report_md/_gpt/CODEX_PLOT_REFRESH_REPORT_20260424.md"
DEPRECATED = FIG_DIR / "deprecated_20260424"

LOCAL_RUNS = [
    ("CX-M1", "Standard", 123, "cx_m1_fresh_eval.json"),
    ("CX-M2", "Ensemble", 123, "cx_m2_fresh_eval.json"),
    ("CX-M3", "Proportional", 123, "cx_m3_fresh_eval.json"),
    ("CX-M4", "Proportional", 456, "cx_m4_fresh_eval.json"),
    ("CX-M5", "Standard", 456, "cx_m5_fresh_eval.json"),
    ("CX-M6", "Ensemble", 456, "cx_m6_fresh_eval.json"),
]

ADC_8BIT_FILES = {
    "CX-M1": "cx_m1_adc_fresh_eval.json",
    "CX-M2": "cx_m2_adc_fresh_eval.json",
    "CX-M3": "cx_m3_adc_fresh_eval.json",
    "CX-M4": "cx_m4_adc_fresh_eval.json",
    "CX-M5": "cx_m5_adc_fresh_eval.json",
    "CX-M6": "cx_m6_adc_fresh_eval.json",
}

ADC_6BIT_FILES = {
    "CX-M1": "cx_m1_adc6_fresh_eval.json",
    "CX-M3": "cx_m3_adc6_fresh_eval.json",
}

REMOTE_FRESH = {
    "Standard": [83.64],
    "Proportional": [84.80, 84.79],
}

REMOTE_STD = {
    "Standard": [0.10],
    "Proportional": [0.08, 0.07],
}


def load_runs():
    rows = []
    for run_id, hat_type, seed, filename in LOCAL_RUNS:
        path = JSON_DIR / filename
        data = json.loads(path.read_text(encoding="utf-8"))
        adc8 = json.loads((JSON_DIR / ADC_8BIT_FILES[run_id]).read_text(encoding="utf-8"))
        adc6_path = JSON_DIR / ADC_6BIT_FILES[run_id] if run_id in ADC_6BIT_FILES else None
        adc6 = json.loads(adc6_path.read_text(encoding="utf-8")) if adc6_path and adc6_path.exists() else None
        rows.append({
            "run_id": run_id,
            "hat_type": hat_type,
            "seed": seed,
            "train_best": float(data["checkpoint_best_acc"]),
            "fresh_mean": float(data["cross_instance_mean"]),
            "fresh_std": float(data["cross_instance_std"]),
            "adc8_mean": float(adc8["cross_instance_mean"]),
            "adc8_std": float(adc8["cross_instance_std"]),
            "adc6_mean": float(adc6["cross_instance_mean"]) if adc6 else np.nan,
            "adc6_std": float(adc6["cross_instance_std"]) if adc6 else np.nan,
            "json": str(path.relative_to(ROOT)),
        })
    return rows


def group(rows, hat_type, key):
    vals = [
        row[key]
        for row in rows
        if row["hat_type"] == hat_type and not (isinstance(row[key], float) and np.isnan(row[key]))
    ]
    if not vals:
        return np.nan, np.nan, 0
    if len(vals) == 1:
        return vals[0], 0.0, 1
    return mean(vals), stdev(vals), len(vals)


def backup_existing(stem):
    DEPRECATED.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "pdf"):
        src = FIG_DIR / f"{stem}.{ext}"
        dst = DEPRECATED / f"{stem}_pre_plotrefresh_20260424.{ext}"
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)


def save_figure(fig, stem):
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_DIR / f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(FIG_DIR / f"{stem}.png", bbox_inches="tight", dpi=300)
    plt.close(fig)


def plot_postfix_summary(rows):
    backup_existing("fig_postfix_severe_nl")
    hats = ["Standard", "Ensemble", "Proportional"]
    x = np.arange(len(hats))
    width = 0.24

    local_train = [group(rows, h, "train_best")[0] for h in hats]
    local_train_err = [group(rows, h, "train_best")[1] for h in hats]
    local_fresh = [group(rows, h, "fresh_mean")[0] for h in hats]
    local_fresh_err = [group(rows, h, "fresh_mean")[1] for h in hats]
    adc8_fresh = [group(rows, h, "adc8_mean")[0] for h in hats]
    adc8_fresh_err = [group(rows, h, "adc8_mean")[1] for h in hats]
    adc6_fresh = [group(rows, h, "adc6_mean")[0] for h in hats]
    adc6_fresh_err = [group(rows, h, "adc6_mean")[1] for h in hats]
    remote_fresh = [mean(REMOTE_FRESH[h]) if h in REMOTE_FRESH else np.nan for h in hats]
    remote_fresh_err = [
        stdev(REMOTE_FRESH[h]) if h in REMOTE_FRESH and len(REMOTE_FRESH[h]) > 1 else
        (REMOTE_STD[h][0] if h in REMOTE_STD else np.nan)
        for h in hats
    ]

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.0), gridspec_kw={"width_ratios": [1.15, 1.0]})
    ax = axes[0]
    ax.bar(x - width, local_train, width, yerr=local_train_err, label="Local train best", color="tab:blue", capsize=3)
    ax.bar(x, local_fresh, width, yerr=local_fresh_err, label="Local fresh", color="tab:orange", capsize=3)
    ax.bar(x + width, remote_fresh, width, yerr=remote_fresh_err, label="Remote fresh", color="tab:green", capsize=3)
    ax.set_ylabel("Accuracy (%)")
    ax.set_xticks(x)
    ax.set_xticklabels(hats)
    ax.set_ylim(75, 91)
    ax.set_title("Post-fix severe-NL summary (NL=2.0)")
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    ax.grid(axis="y", alpha=0.25)
    ax.text(0.99, 0.02, "Local batch=64; remote batch=512", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=8)

    ax2 = axes[1]
    adc_width = 0.22
    ax2.bar(x - adc_width, local_fresh, adc_width, yerr=local_fresh_err, label="ADC-off", color="#4C78A8", capsize=3)
    ax2.bar(x, adc8_fresh, adc_width, yerr=adc8_fresh_err, label="ADC-on 8-bit", color="#F58518", capsize=3)
    for idx, (value, err) in enumerate(zip(adc6_fresh, adc6_fresh_err)):
        if not np.isnan(value):
            ax2.bar(x[idx] + adc_width, value, adc_width, yerr=err, color="#54A24B", capsize=3)
    ax2.set_xticks(x)
    ax2.set_xticklabels(hats)
    ax2.set_ylim(75, 83)
    ax2.set_title("Deployment ADC impact")
    ax2.grid(axis="y", alpha=0.25)
    ax2.legend(
        handles=[
            plt.Rectangle((0, 0), 1, 1, color="#4C78A8"),
            plt.Rectangle((0, 0), 1, 1, color="#F58518"),
            plt.Rectangle((0, 0), 1, 1, color="#54A24B"),
        ],
        labels=["ADC-off", "ADC-on 8-bit", "ADC-on 6-bit"],
        frameon=False,
        fontsize=9,
        loc="lower left",
    )
    ax2.text(
        0.99,
        0.02,
        "6-bit spot-check available for Standard/Proportional only",
        transform=ax2.transAxes,
        ha="right",
        va="bottom",
        fontsize=8,
    )
    fig.suptitle("Severe-NL post-fix summary and deployment ablation", y=1.02, fontsize=12)
    save_figure(fig, "fig_postfix_severe_nl")


def plot_cross_host(rows):
    by_run = {row["run_id"]: row for row in rows}
    points = [
        ("Standard s123", by_run["CX-M1"]["fresh_mean"], by_run["CX-M1"]["fresh_std"], 83.64, 0.10),
        ("Proportional s123", by_run["CX-M3"]["fresh_mean"], by_run["CX-M3"]["fresh_std"], 84.80, 0.08),
    ]

    fig, ax = plt.subplots(figsize=(4.2, 4.0))
    for label, x, xerr, y, yerr in points:
        ax.errorbar(x, y, xerr=xerr, yerr=yerr, fmt="o", capsize=3, label=label)
        ax.annotate(label, (x, y), xytext=(5, 5), textcoords="offset points", fontsize=8)
    lo, hi = 79, 85.5
    ax.plot([lo, hi], [lo, hi], "--", color="0.35", linewidth=1)
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.set_xlabel("Local fresh accuracy (%)")
    ax.set_ylabel("Remote fresh accuracy (%)")
    ax.set_title("Cross-host parity")
    ax.grid(alpha=0.25)
    save_figure(fig, "figS_cross_host_parity")


def plot_fig5_refresh(rows):
    backup_existing("fig5_hat_recovery")
    hats = ["Standard", "Ensemble", "Proportional"]
    x = np.arange(len(hats))
    fresh = [group(rows, h, "fresh_mean")[0] for h in hats]
    fresh_err = [group(rows, h, "fresh_mean")[1] for h in hats]

    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.5), gridspec_kw={"width_ratios": [0.8, 1.4]})
    axes[0].bar([0], [86.37], yerr=[1.54], color="tab:green", capsize=3)
    axes[0].set_xticks([0])
    axes[0].set_xticklabels(["Canonical\nEnsemble HAT"])
    axes[0].set_ylim(75, 90)
    axes[0].set_ylabel("Accuracy (%)")
    axes[0].set_title("Bug-immune NL=1")
    axes[0].grid(axis="y", alpha=0.25)

    axes[1].bar(x, fresh, yerr=fresh_err, color=["tab:blue", "tab:orange", "tab:green"], capsize=3)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(hats)
    axes[1].set_ylim(75, 84)
    axes[1].set_title("Post-fix severe NL=2")
    axes[1].grid(axis="y", alpha=0.25)
    fig.suptitle("HAT recovery after post-fix M-series")
    save_figure(fig, "fig5_hat_recovery")


def plot_figs3_refresh(rows):
    backup_existing("figS3_ensemble_hat")
    ensemble_mean, ensemble_std, _ = group(rows, "Ensemble", "fresh_mean")
    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.5), gridspec_kw={"width_ratios": [1.1, 1.2]})

    ax = axes[0]
    ax.axis("off")
    ax.text(0.5, 0.78, "Ensemble HAT", ha="center", va="center", fontsize=13, weight="bold")
    ax.text(0.5, 0.55, "Resample hardware\ninstances during training", ha="center", va="center", fontsize=10)
    ax.annotate("", xy=(0.5, 0.33), xytext=(0.5, 0.47), arrowprops={"arrowstyle": "->", "lw": 1.5})
    ax.text(0.5, 0.22, "Fresh-instance\nrobustness", ha="center", va="center", fontsize=10)

    labels = ["Standard\nNL=1", "Ensemble\nNL=1", "Ensemble\nNL=2"]
    vals = [10.00, 86.37, ensemble_mean]
    errs = [0.0, 1.54, ensemble_std]
    axes[1].bar(np.arange(3), vals, yerr=errs, color=["tab:red", "tab:green", "tab:orange"], capsize=3)
    axes[1].set_xticks(np.arange(3))
    axes[1].set_xticklabels(labels)
    axes[1].set_ylabel("Fresh accuracy (%)")
    axes[1].set_ylim(0, 92)
    axes[1].set_title("Fresh-instance transfer")
    axes[1].grid(axis="y", alpha=0.25)
    save_figure(fig, "figS3_ensemble_hat")


def write_report(rows):
    local_sources = "\n".join(f"- `{row['json']}`" for row in rows)
    REPORT.write_text(
        "\n".join([
            "# CODEX Plot Refresh Report",
            "",
            "- Date: 2026-04-24",
            "- Scope: post-fix severe-NL figure refresh from CX-M1..M6 JSON files.",
            "- No experiments were run by this plotting script.",
            "",
            "## Outputs",
            "",
            "- `paper/figures/fig5_hat_recovery.png` and `.pdf`",
            "- `paper/figures/figS3_ensemble_hat.png` and `.pdf`",
            "- `paper/figures/fig_postfix_severe_nl.png` and `.pdf`",
            "- `paper/figures/figS_cross_host_parity.png` and `.pdf`",
            "",
            "## Source Data",
            "",
            local_sources,
            "",
            "Remote rows used only where dispatch supplied fresh values:",
            "- R-M1 Standard seed 123: 83.64 +/- 0.10",
            "- R-M2 Proportional seed 123: 84.80 +/- 0.08",
            "- R-M2 Proportional seed 222: 84.79 +/- 0.07",
            "",
            "## Notes",
            "",
            "- Existing `fig5_hat_recovery` and `figS3_ensemble_hat` were backed up under `paper/figures/deprecated_20260424/` before overwrite.",
            "- `fig_postfix_severe_nl` now includes an ADC-off vs ADC-on subplot; 6-bit bars are spot-checks for Standard and Proportional only.",
            "- Bug-immune canonical Ensemble HAT value `86.37 +/- 1.54` is retained as a reference bar.",
            "- The severe-NL structural-limit figure remains quarantined.",
            "- Captions should state that error bars are 1 standard deviation across seeds unless otherwise noted.",
            "",
        ]),
        encoding="utf-8",
    )


def main():
    rows = load_runs()
    plot_postfix_summary(rows)
    plot_cross_host(rows)
    plot_fig5_refresh(rows)
    plot_figs3_refresh(rows)
    write_report(rows)
    print(REPORT)


if __name__ == "__main__":
    main()
