#!/usr/bin/env python3
"""Generate the main Paper-1 spine figure and source-data tables."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / "paper" / "latex_gpt" / "figures"
SRC_DIR = ROOT / "paper" / "latex_gpt" / "source_data"
CKPT = ROOT / "paper2_aihwkit_baseline" / "checkpoints"

FIG_DIR.mkdir(parents=True, exist_ok=True)
SRC_DIR.mkdir(parents=True, exist_ok=True)


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
        "condition": "IdealDevice 8-bit",
        "fresh_mean": load_json(CKPT / "fresh_eval.json")["mean"],
        "fresh_std": load_json(CKPT / "fresh_eval.json")["std"],
        "role": "stable baseline",
    },
    {
        "condition": "IdealDevice 4-bit",
        "fresh_mean": load_json(CKPT / "r11d_1_4bit" / "fresh_eval.json")["mean"],
        "fresh_std": load_json(CKPT / "r11d_1_4bit" / "fresh_eval.json")["std"],
        "role": "collapse",
    },
    {
        "condition": "Ensemble HAT 4-bit",
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
    "6-bit PCM": ["r11d_6bit_pcm_seed123", "r11d_6bit_pcm_seed456_full100", "r11d_6bit_pcm_seed789"],
    "4-bit PCM": ["r11d_7_pcm_4bit_seed123", "r11d_7_pcm_4bit_seed456_clean", "r11d_7_pcm_4bit_seed789"],
}

pcm_rows = []
for label, runs in pcm_groups.items():
    best_vals = []
    fresh_vals = []
    drift0_vals = []
    drift1d_vals = []
    for run in runs:
        run_dir = CKPT / run
        hist = load_json(run_dir / "training_history.json")
        fresh = load_json(run_dir / "fresh_eval.json")
        best_vals.append(float(hist["best_acc"]))
        fresh_vals.append(float(fresh["mean"]))
        drift0_vals.append(drift_acc(run_dir, 0.0))
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
            "drift_drop_1d_pp": drift_drop,
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

manifest = {
    "generated_by": "scripts/_gpt/plot_paper1_spine.py",
    "outputs": [
        "paper/latex_gpt/figures/fig1_paper1_spine.pdf",
        "paper/latex_gpt/figures/fig1_paper1_spine.png",
        "paper/latex_gpt/source_data/fig1_paper1_spine.csv",
        "paper/latex_gpt/source_data/tab_pcm_precision_ladder.csv",
    ],
    "raw_sources": [
        "paper2_aihwkit_baseline/checkpoints/fresh_eval.json",
        "paper2_aihwkit_baseline/checkpoints/r11d_1_4bit/fresh_eval.json",
        "report_md/_gpt/json_gpt/r10a_canonical_ensemble_hat_3seed_fresh_eval.json",
        *[f"paper2_aihwkit_baseline/checkpoints/{run}/training_history.json" for runs in pcm_groups.values() for run in runs],
        *[f"paper2_aihwkit_baseline/checkpoints/{run}/fresh_eval.json" for runs in pcm_groups.values() for run in runs],
        *[f"paper2_aihwkit_baseline/checkpoints/{run}/drift_eval.json" for runs in pcm_groups.values() for run in runs],
    ],
}
with (SRC_DIR / "manifest_paper1_spine.json").open("w", encoding="utf-8") as handle:
    json.dump(manifest, handle, indent=2)

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 10.2,
        "axes.labelsize": 10.2,
        "axes.titlesize": 10.4,
        "xtick.labelsize": 9.2,
        "ytick.labelsize": 9.2,
        "axes.linewidth": 0.8,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)

fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.25), gridspec_kw={"width_ratios": [1.05, 1.12]})
fig.patch.set_facecolor("white")

# Panel A: algorithmic failure and rescue.
ax = axes[0]
labels_a = ["8-bit\nIdeal", "4-bit\nIdeal", "4-bit\nEnsemble HAT"]
means_a = [row["fresh_mean"] for row in ideal_rows]
stds_a = [row["fresh_std"] for row in ideal_rows]
colors_a = ["#2F5D8C", "#B94A48", "#2E7D5B"]
ax.bar(np.arange(len(labels_a)), means_a, yerr=stds_a, capsize=3, color=colors_a, edgecolor="#202020", linewidth=0.6)
ax.set_ylim(0, 95)
ax.set_ylabel("Fresh-instance accuracy (%)")
ax.set_xticks(np.arange(len(labels_a)))
ax.set_xticklabels(labels_a)
ax.set_title("A. Pure 4-bit failure and rescue", loc="left", fontweight="bold")
ax.axhline(10, color="#777777", linestyle=":", linewidth=0.8)
ax.text(1.02, 12.0, "chance", color="#555555", fontsize=8.6)
for idx, value in enumerate(means_a):
    ax.text(idx, value + 3.0, f"{value:.2f}", ha="center", va="bottom", fontsize=8.8)
ax.spines[["top", "right"]].set_visible(False)

# Panel B: PCM precision-retention ladder.
ax = axes[1]
labels_b = ["8-bit", "6-bit", "4-bit"]
fresh_b = [row["fresh_mean"] for row in pcm_rows]
fresh_std_b = [row["fresh_std"] for row in pcm_rows]
drift_b = [row["drift_drop_1d_pp"] for row in pcm_rows]
x = np.arange(len(labels_b))
bars = ax.bar(x, fresh_b, yerr=fresh_std_b, capsize=3, color=["#7FA8C9", "#4E9F74", "#D59A4A"], edgecolor="#202020", linewidth=0.6)
ax.set_ylim(70, 80.5)
ax.set_ylabel("Fresh accuracy (%)")
ax.set_xticks(x)
ax.set_xticklabels(labels_b)
ax.set_title("B. PCM precision-retention frontier", loc="left", fontweight="bold")
for idx, value in enumerate(fresh_b):
    ax.text(idx, value + 0.35, f"{value:.2f}", ha="center", va="bottom", fontsize=8.8)
ax.spines[["top"]].set_visible(False)

ax2 = ax.twinx()
ax2.plot(x, drift_b, color="#7A2E2E", marker="o", linewidth=1.8)
ax2.set_ylim(0, 4.6)
ax2.set_ylabel("1-day drift drop (pp)", color="#7A2E2E")
ax2.tick_params(axis="y", colors="#7A2E2E")
ax2.spines["top"].set_visible(False)
for idx, value in enumerate(drift_b):
    ax2.text(idx + 0.05, value + 0.12, f"{value:.2f} pp", color="#7A2E2E", fontsize=8.6)
ax2.annotate("best tested\nPareto midpoint", xy=(1, fresh_b[1]), xycoords=ax.transData, xytext=(0.64, 0.20), textcoords="axes fraction", arrowprops=dict(arrowstyle="->", color="#2D6A4F", lw=0.9), fontsize=8.6, color="#2D6A4F", ha="center")

fig.tight_layout(w_pad=2.0)
for ext in ["pdf", "png"]:
    fig.savefig(FIG_DIR / f"fig1_paper1_spine.{ext}", bbox_inches="tight", dpi=300)
print(FIG_DIR / "fig1_paper1_spine.pdf")
print(SRC_DIR / "fig1_paper1_spine.csv")
print(SRC_DIR / "tab_pcm_precision_ladder.csv")
