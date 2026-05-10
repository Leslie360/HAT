#!/usr/bin/env python3
"""Generate the main Paper-1 multi-panel spine figure and source-data tables."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / "paper" / "latex_gpt" / "figures"
SRC_DIR = ROOT / "paper" / "latex_gpt" / "source_data"
CKPT = ROOT / "paper2_aihwkit_baseline" / "checkpoints"

FIG_DIR.mkdir(parents=True, exist_ok=True)
SRC_DIR.mkdir(parents=True, exist_ok=True)

# Top-tier Journal Palette (Okabe-Ito inspired / Nature style)
NATURE_TEAL = "#2A9D8F"
NATURE_CORAL = "#E76F51"
NATURE_GOLD = "#E9C46A"
NATURE_NAVY = "#264653"
GRAY_DARK = "#333333"
GRAY_LIGHT = "#AAAAAA"

def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)

def drift_acc(run_dir: Path, seconds: float) -> float:
    drift = load_json(run_dir / "drift_eval.json")
    for row in drift["results"]:
        if float(row["t_inference_seconds"]) == seconds:
            return float(row["accuracy"])
    raise KeyError(seconds)

def mean_std(values: list[float]) -> tuple[float, float]:
    arr = np.asarray(values, dtype=float)
    return float(arr.mean()), float(arr.std(ddof=1))

ideal_rows = [
    {
        "condition": "IdealDevice\n8-bit",
        "fresh_mean": load_json(CKPT / "fresh_eval.json")["mean"],
        "fresh_std": load_json(CKPT / "fresh_eval.json")["std"],
        "role": "stable baseline",
    },
    {
        "condition": "IdealDevice\n4-bit",
        "fresh_mean": load_json(CKPT / "r11d_1_4bit" / "fresh_eval.json")["mean"],
        "fresh_std": load_json(CKPT / "r11d_1_4bit" / "fresh_eval.json")["std"],
        "role": "collapse",
    },
    {
        "condition": "Ensemble HAT\n4-bit",
        "fresh_mean": 86.15873333333333,
        "fresh_std": 0.19,
        "role": "algorithmic rescue",
    },
]
ensemble_hat = load_json(ROOT / "report_md" / "_gpt" / "json_gpt" / "r10a_canonical_ensemble_hat_3seed_fresh_eval.json")
ideal_rows[2]["fresh_mean"] = ensemble_hat["cross_seed"]["mean_of_seed_means"]
ideal_rows[2]["fresh_std"] = ensemble_hat["cross_seed"]["std_of_seed_means_sample"]

pcm_groups = {
    "8-bit PCM": ["r11d_5a_pcm_seed123", "r11d_5a_pcm_seed456", "r11d_5a_pcm_seed789"],
    "6-bit PCM": ["r11d_6bit_pcm_seed123", "r11d_6bit_pcm_seed456", "r11d_6bit_pcm_seed457", "r11d_6bit_pcm_seed789"],
    "4-bit PCM": ["r11d_7_pcm_4bit_seed123", "r11d_7_pcm_4bit_seed456_clean", "r11d_7_pcm_4bit_seed789"],
}

pcm_rows = []
for label, runs in pcm_groups.items():
    best_vals = []
    fresh_vals = []
    drift0_vals = []
    drift1h_vals = []
    drift1d_vals = []
    for run in runs:
        run_dir = CKPT / run
        hist_path = run_dir / "training_history.json"
        fresh = load_json(run_dir / "fresh_eval.json")
        if hist_path.exists():
            hist = load_json(hist_path)
            best_vals.append(float(hist["best_acc"]))
        fresh_vals.append(float(fresh["mean"]))
        drift0_vals.append(drift_acc(run_dir, 0.0))
        drift1h_vals.append(drift_acc(run_dir, 3600.0))
        drift1d_vals.append(drift_acc(run_dir, 86400.0))
    best_mean, best_std = mean_std(best_vals)
    fresh_mean, fresh_std = mean_std(fresh_vals)
    drift_drop = float(np.mean(drift0_vals) - np.mean(drift1d_vals))
    pcm_rows.append(
        {
            "condition": label,
            "source_best_mean": best_mean,
            "source_best_std": best_std,
            "fresh_mean": fresh_mean,
            "fresh_std": fresh_std,
            "drift_1h_mean": float(np.mean(drift1h_vals)),
            "drift_1d_mean": float(np.mean(drift1d_vals)),
            "drift_drop_1d_pp": drift_drop,
            "n_fresh": len(fresh_vals),
            "n_drift": len(drift0_vals),
            "n_source_best": len(best_vals),
            "note": "new protocol; seed123 rerun complete 2026-05-09" if label == "6-bit PCM" else "original audited canonical",
        }
    )

with (SRC_DIR / "fig1_paper1_spine.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(ideal_rows[0].keys()), lineterminator="\n")
    writer.writeheader()
    writer.writerows(ideal_rows)

with (SRC_DIR / "tab_pcm_precision_ladder.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(pcm_rows[0].keys()), lineterminator="\n")
    writer.writeheader()
    writer.writerows(pcm_rows)

raw_sources = [
    CKPT / "fresh_eval.json",
    CKPT / "r11d_1_4bit" / "fresh_eval.json",
    ROOT / "report_md" / "_gpt" / "json_gpt" / "r10a_canonical_ensemble_hat_3seed_fresh_eval.json",
]
missing_optional_sources = []
for runs in pcm_groups.values():
    for run in runs:
        run_dir = CKPT / run
        hist_path = run_dir / "training_history.json"
        if hist_path.exists():
            raw_sources.append(hist_path)
        else:
            missing_optional_sources.append(hist_path)
        raw_sources.extend([run_dir / "fresh_eval.json", run_dir / "drift_eval.json"])

manifest = {
    "generated_by": "scripts/_gpt/plot_paper1_spine.py",
    "outputs": [
        "paper/latex_gpt/figures/fig1_paper1_spine.pdf",
        "paper/latex_gpt/figures/fig1_paper1_spine.png",
        "paper/latex_gpt/source_data/fig1_paper1_spine.csv",
        "paper/latex_gpt/source_data/tab_pcm_precision_ladder.csv",
    ],
    "raw_sources": [str(path.relative_to(ROOT)) for path in raw_sources],
    "missing_optional_sources": [str(path.relative_to(ROOT)) for path in missing_optional_sources],
}
with (SRC_DIR / "manifest_paper1_spine.json").open("w", encoding="utf-8") as handle:
    json.dump(manifest, handle, indent=2)
    handle.write("\n")

# Clean, Modern Typography (Nature Style)
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "font.size": 9.5,
    "axes.labelsize": 10,
    "axes.titlesize": 10.5,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "axes.linewidth": 0.8,
    "axes.edgecolor": GRAY_DARK,
    "xtick.color": GRAY_DARK,
    "ytick.color": GRAY_DARK,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.25), gridspec_kw={"width_ratios": [1.0, 1.15]})
fig.patch.set_facecolor("white")

# =========================================================
# Panel A: Algorithmic Failure and Rescue (Bar Chart)
# =========================================================
ax = axes[0]
labels_a = [row["condition"] for row in ideal_rows]
means_a = [row["fresh_mean"] for row in ideal_rows]
stds_a = [row["fresh_std"] for row in ideal_rows]

# Clean bars with softer edges and no caps on error bars
colors_a = [NATURE_NAVY, NATURE_CORAL, NATURE_TEAL]
bars = ax.bar(np.arange(len(labels_a)), means_a, yerr=stds_a, color=colors_a,
              edgecolor="none", width=0.65, alpha=0.9,
              error_kw=dict(ecolor=GRAY_DARK, lw=1.2, capsize=0))

ax.set_ylim(0, 100)
ax.set_ylabel("Fresh-Instance Accuracy (%)")
ax.set_xticks(np.arange(len(labels_a)))
ax.set_xticklabels(labels_a)
ax.set_title("A. Pure 4-bit failure and rescue", loc="left", fontweight="bold", pad=12)

# Subdued chance line
ax.axhline(10, color=GRAY_LIGHT, linestyle="--", linewidth=1.0, zorder=-1)
ax.text(2.4, 11.5, "chance", color=GRAY_LIGHT, fontsize=8, ha="right")

# Data labels above bars
for idx, value in enumerate(means_a):
    ax.text(idx, value + 4.0, f"{value:.1f}%", ha="center", va="bottom", fontsize=8.5, color=GRAY_DARK, fontweight="500")

ax.spines[["top", "right"]].set_visible(False)

# =========================================================
# Panel B: PCM Precision-Retention Regimes
# =========================================================
ax2 = axes[1]
labels_b = ["8-bit\nPCM", "6-bit\nPCM", "4-bit\nPCM"]
fresh_b = [row["fresh_mean"] for row in pcm_rows]
fresh_std_b = [row["fresh_std"] for row in pcm_rows]
drift_b = [row["drift_drop_1d_pp"] for row in pcm_rows]

# Scatter plot for the corrected precision-retention regimes.
ax2.plot(drift_b, fresh_b, color=GRAY_LIGHT, linewidth=1.5, linestyle="--", zorder=1)

# Plot points with distinct colors and sizes
colors_b = [NATURE_NAVY, NATURE_TEAL, NATURE_CORAL]
for i in range(3):
    ax2.errorbar(drift_b[i], fresh_b[i], yerr=fresh_std_b[i], fmt='o',
                 color=colors_b[i], markersize=9, markeredgecolor='white', markeredgewidth=1.5,
                 zorder=3, ecolor=colors_b[i], elinewidth=1.5, capsize=0, label=labels_b[i].replace('\n', ' '))

    if i == 1:
        ax2.annotate("transition\nzone", xy=(drift_b[i], fresh_b[i]), xytext=(35, -8),
                     textcoords="offset points", ha="left", va="center",
                     fontsize=8.5, color=NATURE_TEAL,
                     arrowprops=dict(arrowstyle="->", color=NATURE_TEAL, connectionstyle="arc3,rad=-0.2"))

ax2.legend(loc='upper right', frameon=False, fontsize=8.5, handletextpad=0.5)

ax2.set_xlim(-0.5, 5.5)
ax2.set_ylim(60.0, 80.5)
ax2.set_xlabel("1-Day Drift Drop (percentage points)")
ax2.set_ylabel("Fresh Accuracy (%)")
ax2.set_title("B. PCM precision-retention regimes", loc="left", fontweight="bold", pad=12)

# Subtle grid
ax2.grid(True, linestyle=":", alpha=0.4, zorder=0)

ax2.spines[["top", "right"]].set_visible(False)

fig.tight_layout(w_pad=3.0)
for ext in ["pdf", "png"]:
    fig.savefig(FIG_DIR / f"fig1_paper1_spine.{ext}", bbox_inches="tight", dpi=300)
print(FIG_DIR / "fig1_paper1_spine.pdf")
