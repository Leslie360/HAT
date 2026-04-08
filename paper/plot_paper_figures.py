#!/usr/bin/env python3
"""Generate paper-ready figures from report artifacts.

Fig.1 and Fig.2 are manual schematics. This script covers Fig.3-Fig.11 and
gracefully falls back to placeholder panels when pending Tiny-ViT or sweep
artifacts are not available yet.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "report_md"
GPT_REPORT_DIR = REPORT_DIR / "_gpt"
FIGURE_DIR = ROOT / "paper" / "figures"


def configure_style():
    plt.style.use("seaborn-v0_8-paper")
    plt.rcParams.update({
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.labelsize": 12,
        "axes.labelweight": "medium",
        "legend.fontsize": 10,
        "legend.frameon": True,
        "legend.edgecolor": "#cccccc",
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 1.0,
        "axes.edgecolor": "#333333",
        "axes.grid": False,
        "grid.linewidth": 0.5,
        "grid.alpha": 0.3,
        "grid.color": "#b0b0b0",
        "figure.autolayout": False,
        "hatch.linewidth": 0.5,
    })

def enable_major_y_grid(ax):
    ax.grid(
        axis="y",
        which="major",
        linestyle=(0, (2.0, 2.0)),
        linewidth=0.6,
        alpha=0.24,
        color="#8a8a8a",
        zorder=0,
    )


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def maybe_load_json(path: Path):
    if not path.exists():
        return None
    return load_json(path)


def save_placeholder_figure(path: Path, title: str, message: str):
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    ax.axis("off")
    ax.text(
        0.5,
        0.5,
        message,
        ha="center",
        va="center",
        wrap=True,
        fontsize=12,
        bbox={"boxstyle": "round,pad=0.5", "facecolor": "#f4f4f4", "edgecolor": "#999999"},
    )
    ax.set_title(title)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def result_dict(rows: Iterable[dict]) -> Dict[str, dict]:
    out = {}
    for row in rows:
        exp = row.get("experiment")
        if exp:
            out[exp] = row
    return out


def load_rows_from_json(path: Path) -> List[dict]:
    data = load_json(path)
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("results"), list):
        return data["results"]
    if isinstance(data, dict) and data.get("experiment"):
        return [data]
    return []


def load_resnet_results() -> Dict[str, dict]:
    data = load_json(REPORT_DIR / "json" / "resnet18_results.json")
    return result_dict(data["results"])


def load_convnext_results() -> Dict[str, dict]:
    data = load_json(GPT_REPORT_DIR / "json_gpt" / "convnext_full_results_gpt.json")
    return result_dict(data["results"])


def load_convnext_retention() -> List[dict]:
    data = load_json(GPT_REPORT_DIR / "json_gpt" / "convnext_full_results_gpt.json")
    return data.get("retention", [])


def load_tinyvit_results() -> Dict[str, dict]:
    rows: List[dict] = []
    candidates = [
        GPT_REPORT_DIR / "json_gpt" / "tinyvit_v1_results_gpt.json",
        GPT_REPORT_DIR / "json_gpt" / "tinyvit_v2v7_results_gpt.json",
        GPT_REPORT_DIR / "json_gpt" / "tinyvit_results_gpt.json",
    ]
    for path in candidates:
        if not path.exists():
            continue
        data = load_json(path)
        if isinstance(data, list):
            rows.extend(data)
        elif isinstance(data, dict) and isinstance(data.get("results"), list):
            rows.extend(data["results"])
        elif isinstance(data, dict) and data.get("experiment"):
            rows.append(data)
    return result_dict(rows)


def load_tinyvit_multidataset_results() -> Dict[str, Dict[str, dict]]:
    dataset_rows: Dict[str, Dict[str, dict]] = {
        "cifar10": load_tinyvit_results(),
    }
    dataset_files = {
        "cifar100": GPT_REPORT_DIR / "json_gpt" / "tinyvit_cifar100_v134_results_gpt.json",
        "flowers102": GPT_REPORT_DIR / "json_gpt" / "tinyvit_flowers102_v134_results_gpt.json",
    }
    for dataset, path in dataset_files.items():
        dataset_rows[dataset] = result_dict(load_rows_from_json(path)) if path.exists() else {}
    return dataset_rows


def parse_convnext_completed_results_from_log(path: Path) -> Dict[str, dict]:
    if not path.exists():
        return {}

    rows: List[dict] = []
    current: Optional[dict] = None
    text = path.read_text(encoding="utf-8")
    for raw_line in text.splitlines():
        line = raw_line.strip()
        header = re.match(r"Experiment\s+(C\d+):\s+(.+)", line)
        if header:
            if current and current.get("best_test_acc") is not None:
                if current.get("mc_mean_acc") is None:
                    current["mc_mean_acc"] = current["best_test_acc"]
                    current["mc_std_acc"] = 0.0
                rows.append(current)
            current = {
                "experiment": header.group(1),
                "name": header.group(2),
                "best_test_acc": None,
                "mc_mean_acc": None,
                "mc_std_acc": None,
            }
            continue
        if current is None:
            continue
        finished = re.search(r"Finished in\s+([0-9.]+)s\.\s+Best test accuracy:\s+([0-9.]+)%", line)
        if finished:
            current["total_time_s"] = float(finished.group(1))
            current["best_test_acc"] = float(finished.group(2))
            continue
        mc = re.search(r"Monte Carlo:\s+([0-9.]+)%\s+±\s+([0-9.]+)%", line)
        if mc:
            current["mc_mean_acc"] = float(mc.group(1))
            current["mc_std_acc"] = float(mc.group(2))
            continue

    if current and current.get("best_test_acc") is not None:
        if current.get("mc_mean_acc") is None:
            current["mc_mean_acc"] = current["best_test_acc"]
            current["mc_std_acc"] = 0.0
        rows.append(current)
    return result_dict(rows)


def latest_matching_path(pattern: str) -> Optional[Path]:
    matches = sorted(ROOT.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
    return matches[0] if matches else None


def load_convnext_multidataset_results() -> Dict[str, Dict[str, dict]]:
    dataset_rows: Dict[str, Dict[str, dict]] = {
        "cifar10": load_convnext_results(),
        "cifar100": {},
        "flowers102": {},
    }

    dataset_jsons = {
        "cifar100": GPT_REPORT_DIR / "json_gpt" / "convnext_cifar100_c134_results_gpt.json",
        "flowers102": GPT_REPORT_DIR / "json_gpt" / "convnext_flowers102_c134_results_gpt.json",
    }
    for dataset, path in dataset_jsons.items():
        if path.exists():
            dataset_rows[dataset] = result_dict(load_rows_from_json(path))

    if not dataset_rows["cifar100"]:
        live_log = latest_matching_path("logs/_gpt/train_convnext_cifar100_c134_fix_*_gpt.log")
        if live_log is not None:
            dataset_rows["cifar100"] = parse_convnext_completed_results_from_log(live_log)

    if not dataset_rows["flowers102"]:
        flowers_log = latest_matching_path("logs/_gpt/train_convnext_flowers102_c134_fix_*_gpt.log")
        if flowers_log is not None:
            dataset_rows["flowers102"] = parse_convnext_completed_results_from_log(flowers_log)

    return dataset_rows


def load_tinyvit_retention() -> List[dict]:
    candidates = [
        GPT_REPORT_DIR / "json_gpt" / "tinyvit_v4_retention_results_gpt.json",
        GPT_REPORT_DIR / "json_gpt" / "tinyvit_retention_results_gpt.json",
    ]
    for path in candidates:
        if not path.exists():
            continue
        data = load_json(path)
        if isinstance(data, dict) and isinstance(data.get("retention"), list):
            return data["retention"]
        if isinstance(data, list) and data and "time_s" in data[0]:
            return data
    return []


def parse_tinyvit_dryrun_energy() -> Dict[str, float]:
    path = GPT_REPORT_DIR / "tinyvit_hybrid_dryrun_report_gpt.md"
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    patterns = {
        "hybrid_energy_uJ": r"Estimated hybrid energy: ([0-9.]+) µJ / inference",
        "fp32_energy_uJ": r"Estimated FP32 GPU energy: ([0-9.]+) µJ / inference",
        "energy_reduction_ratio": r"Estimated energy reduction ratio: ([0-9.]+)×",
    }
    values: Dict[str, float] = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            values[key] = float(match.group(1))
    return values


def parse_tinyvit_dryrun_breakdown() -> Dict[str, float]:
    path = GPT_REPORT_DIR / "tinyvit_hybrid_dryrun_report_gpt.md"
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    keys = ["analog_MAC", "ADC", "DAC", "digital_MAC", "special_ops", "buffer"]
    values: Dict[str, float] = {}
    for key in keys:
        match = re.search(rf"- {re.escape(key)}: ([0-9.]+) µJ", text)
        if match:
            values[key] = float(match.group(1))
    return values


def maybe_load_noise_sweep_rows() -> List[dict]:
    candidates = [
        GPT_REPORT_DIR / "json_gpt" / "noise_sweep_results_gpt.json",
        GPT_REPORT_DIR / "json_gpt" / "noise_sweep_results.json",
    ]
    for path in candidates:
        if not path.exists():
            continue
        data = load_json(path)
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and isinstance(data.get("results"), list):
            return data["results"]
    return []


def maybe_load_device_comparison_rows() -> List[dict]:
    candidates = [
        GPT_REPORT_DIR / "json_gpt" / "device_comparison_results_gpt.json",
        GPT_REPORT_DIR / "json_gpt" / "device_comparison_results.json",
    ]
    for path in candidates:
        if not path.exists():
            continue
        data = load_json(path)
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and isinstance(data.get("results"), list):
            return data["results"]
    return []


def accuracy_value(row: Optional[dict]) -> float:
    if row is None:
        return math.nan
    for key in ("mc_mean_acc", "best_test_acc", "best_acc", "test_acc_mean", "final_test_acc", "test_acc"):
        value = row.get(key)
        if value is not None:
            parsed = float(value)
            if not math.isfinite(parsed):
                exp = row.get("experiment", row.get("name", "unknown"))
                raise ValueError(f"Non-finite accuracy value found for {exp}: {value}")
            return parsed
    return math.nan


def prettify_dataset_name(dataset: str) -> str:
    mapping = {
        "cifar10": "CIFAR-10",
        "cifar100": "CIFAR-100",
        "flowers102": "Flowers-102",
    }
    return mapping.get(dataset, dataset)


def label_pending(ax, message: str):
    ax.text(
        0.98,
        0.02,
        message,
        ha="right",
        va="bottom",
        transform=ax.transAxes,
        fontsize=9,
        color="#555555",
        bbox={"boxstyle": "round,pad=0.25", "facecolor": "white", "edgecolor": "#cccccc"},
    )


def plot_band_curve(ax, x_vals, y_vals, y_errs, *, color: str, marker: str, label: str):
    x = np.asarray(x_vals, dtype=float)
    y = np.asarray(y_vals, dtype=float)
    err = np.maximum(np.asarray(y_errs, dtype=float), 0.0)
    mask = np.isfinite(x) & np.isfinite(y) & np.isfinite(err)
    if not np.any(mask):
        return
    x = x[mask]
    y = y[mask]
    err = err[mask]
    ax.plot(x, y, marker=marker, linewidth=2.2, markersize=6.5, color=color, label=label, zorder=4)
    ax.fill_between(x, y - err, y + err, color=color, alpha=0.16, linewidth=0, zorder=2)


def plot_fig3_snr_curves(output_dir: Path):
    data = load_json(REPORT_DIR / "json" / "a23_experiment_results.json")
    gamma_values = data["group2"]["gamma_values"]
    x_min, x_max = data["group2"]["x_range"]
    x = np.logspace(np.log10(max(x_min, 1e-3)), np.log10(x_max), 400)

    fig, ax = plt.subplots(figsize=(6.6, 4.6))
    for gamma in gamma_values:
        p_in = np.power(x, 1.0 / gamma)
        snr = x / np.sqrt(np.maximum(p_in, 1e-12))
        ax.plot(x, snr, linewidth=2, label=rf"$\gamma={gamma}$")

    ax.set_xscale("log")
    ax.set_xlabel("Normalized pixel intensity")
    ax.set_ylabel("Normalized SNR (a.u.)")
    ax.set_title("Fig. 3. Analytical SNR under inverse-gamma compensation")
    ax.legend(ncol=2, frameon=True)
    label_pending(ax, "Analytical reconstruction based on the A2.3 front-end model")
    fig.savefig(output_dir / "fig3_snr_curves.png", bbox_inches="tight")
    plt.close(fig)


def plot_fig4_accuracy_comparison(output_dir: Path):
    convnext = load_convnext_multidataset_results()
    tinyvit = load_tinyvit_multidataset_results()

    datasets = ["cifar10", "cifar100", "flowers102"]
    architectures = [
        ("ConvNeXt-\nTiny", "convnext"),
        ("Tiny-ViT-\n5M", "tinyvit"),
    ]
    regimes = [
        ("FP32", "#2E5B88", {"convnext": "C1", "tinyvit": "V1"}),
        ("Standard-noise", "#E45756", {"convnext": "C3", "tinyvit": "V3"}),
        ("HAT", "#3A8231", {"convnext": "C4", "tinyvit": "V4"}),
    ]

    fig, axes = plt.subplots(1, len(datasets), figsize=(13.6, 4.7), sharey=True)
    width = 0.22
    x = np.arange(len(architectures))

    missing_any = False
    for dataset_idx, (ax, dataset) in enumerate(zip(axes, datasets)):
        for regime_idx, (regime_name, color, exp_map) in enumerate(regimes):
            vals = []
            for _, arch_key in architectures:
                rows = convnext[dataset] if arch_key == "convnext" else tinyvit[dataset]
                vals.append(accuracy_value(rows.get(exp_map[arch_key])))
            vals_arr = np.asarray(vals, dtype=float)
            if np.isnan(vals_arr).any():
                missing_any = True
            ax.bar(
                x + (regime_idx - 1) * width,
                vals_arr,
                width=width,
                color=color,
                label=regime_name if dataset_idx == 0 else None,
                edgecolor="white",
                linewidth=0.8,
                zorder=3,
            )

        for arch_idx, (_, arch_key) in enumerate(architectures):
            rows = convnext[dataset] if arch_key == "convnext" else tinyvit[dataset]
            standard = accuracy_value(rows.get("C3" if arch_key == "convnext" else "V3"))
            hat = accuracy_value(rows.get("C4" if arch_key == "convnext" else "V4"))
            if math.isnan(standard) or math.isnan(hat):
                continue
            delta = hat - standard
            ax.text(
                x[arch_idx] + width,
                max(standard, hat) + 2.1,
                f"{delta:+.1f} pp",
                ha="center",
                va="bottom",
                fontsize=9,
                color="#333333",
            )

        ax.set_xticks(x)
        ax.set_xticklabels([label for label, _ in architectures])
        ax.set_title(prettify_dataset_name(dataset))
        ax.set_ylim(0, 100)
        ax.set_axisbelow(True)
        enable_major_y_grid(ax)
        if dataset_idx == 0:
            ax.set_ylabel("Accuracy (%)")

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=3, frameon=True, bbox_to_anchor=(0.5, 1.05))
    fig.suptitle("Fig. 4. Cross-dataset noise fragility and HAT recovery", y=1.09, fontsize=13)
    fig.text(
        0.5,
        -0.02,
        "Tiny-ViT V3 denotes the fixed-D2D standard-noise baseline; ConvNeXt C3 denotes standard noisy training.",
        ha="center",
        va="top",
        fontsize=9,
        color="#555555",
    )
    if missing_any:
        fig.text(
            0.5,
            -0.08,
            "This figure is designed to be live-updated: missing ConvNeXt multi-dataset bars are intentionally left blank until Task 21 completes.",
            ha="center",
            va="top",
            fontsize=8.5,
            color="#666666",
        )
    fig.savefig(output_dir / "fig4_accuracy_comparison.png", bbox_inches="tight")
    plt.close(fig)


def plot_fig5_hat_recovery(output_dir: Path):
    convnext = load_convnext_multidataset_results()
    tinyvit = load_tinyvit_multidataset_results()

    datasets = ["cifar10", "cifar100", "flowers102"]
    architecture_rows = {
        "ConvNeXt-Tiny": ("convnext", {"fp32": "C1", "standard": "C3", "hat": "C4"}),
        "Tiny-ViT-5M": ("tinyvit", {"fp32": "V1", "standard": "V3", "hat": "V4"}),
    }
    colors = {
        "ConvNeXt-Tiny": "#2E5B88",
        "Tiny-ViT-5M": "#3A8231",
    }

    fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.8), sharey=False)
    x = np.arange(len(datasets))
    width = 0.34
    ref_axes = [ax.twinx() for ax in axes]
    ref_styles = {
        "ConvNeXt-Tiny": {"color": "#4a4a4a", "marker": "o"},
        "Tiny-ViT-5M": {"color": "#8c8c8c", "marker": "s"},
    }

    subplot_specs = [
        ("Noise-induced degradation", "standard", "fp32", axes[0]),
        ("HAT recovery", "hat", "standard", axes[1]),
    ]
    missing_any = False

    for plot_idx, (title, top_key, base_key, ax) in enumerate(subplot_specs):
        ref_ax = ref_axes[plot_idx]
        for idx, (arch_name, (source_key, exp_keys)) in enumerate(architecture_rows.items()):
            values = []
            fp32_refs = []
            for dataset in datasets:
                rows = convnext[dataset] if source_key == "convnext" else tinyvit[dataset]
                top = accuracy_value(rows.get(exp_keys[top_key]))
                base = accuracy_value(rows.get(exp_keys[base_key]))
                fp32_refs.append(accuracy_value(rows.get(exp_keys["fp32"])))
                if math.isnan(top) or math.isnan(base):
                    values.append(math.nan)
                    missing_any = True
                else:
                    values.append(top - base)
            vals = np.asarray(values, dtype=float)
            ax.bar(
                x + (idx - 0.5) * width,
                vals,
                width=width,
                color=colors[arch_name],
                label=arch_name,
                edgecolor="white",
                linewidth=0.8,
                zorder=3,
            )
            for xpos, val in zip(x + (idx - 0.5) * width, vals):
                if math.isnan(val):
                    continue
                offset = 0.9 if val >= 0 else -1.2
                va = "bottom" if val >= 0 else "top"
                ax.text(xpos, val + offset, f"{val:+.1f}", ha="center", va=va, fontsize=9, color="#333333")

            fp32_refs = np.asarray(fp32_refs, dtype=float)
            finite = np.isfinite(fp32_refs)
            if np.any(finite):
                ref_ax.plot(
                    x[finite],
                    fp32_refs[finite],
                    linestyle=(0, (3.0, 2.0)),
                    linewidth=1.4,
                    marker=ref_styles[arch_name]["marker"],
                    markersize=5.0,
                    color=ref_styles[arch_name]["color"],
                    label=f"{arch_name} FP32 reference",
                    zorder=5,
                )

        ax.axhline(0.0, color="#666666", linewidth=0.9)
        ax.set_xticks(x)
        ax.set_xticklabels([prettify_dataset_name(d) for d in datasets], rotation=10)
        ax.set_title(title)
        ax.set_ylabel("Accuracy change (pp)")
        ax.set_axisbelow(True)
        enable_major_y_grid(ax)
        ref_ax.set_ylim(0, 100)
        ref_ax.spines["top"].set_visible(False)
        ref_ax.tick_params(axis="y", colors="#666666", labelsize=9)
        ref_ax.set_ylabel("FP32 accuracy (%)", color="#666666")

    axes[0].set_ylim(-100, 5)
    axes[1].set_ylim(-5, 35)
    handles = []
    labels = []
    for axis in (axes[1], ref_axes[1]):
        h, l = axis.get_legend_handles_labels()
        handles.extend(h)
        labels.extend(l)
    fig.legend(handles, labels, loc="upper center", ncol=2, frameon=True, bbox_to_anchor=(0.5, 1.06))
    fig.suptitle("Fig. 5. Cross-dataset degradation and HAT recovery with FP32 references", y=1.12, fontsize=13)
    fig.text(
        0.5,
        -0.02,
        "Bars show absolute percentage-point changes. Dashed marker lines on the right axis show the corresponding FP32 reference accuracies.",
        ha="center",
        va="top",
        fontsize=9,
        color="#555555",
    )
    if missing_any:
        fig.text(
            0.5,
            -0.08,
            "Missing ConvNeXt multi-dataset deltas will auto-populate once Task 21 finishes; Tiny-ViT V3 uses the fixed-D2D standard-noise protocol.",
            ha="center",
            va="top",
            fontsize=8.5,
            color="#666666",
        )
    fig.savefig(output_dir / "fig5_hat_recovery.png", bbox_inches="tight")
    plt.close(fig)


def plot_fig6_physical_compensation(output_dir: Path):
    data = load_json(REPORT_DIR / "json" / "a23_experiment_results.json")
    group1 = data["group1"]
    group3 = data["group3"]

    gammas = sorted({float(row["gamma"]) for row in group1.values()})
    i_dark_rows = sorted({(float(row["I_dark"]), row["I_dark_label"]) for row in group1.values()})
    heatmap = np.full((len(gammas), len(i_dark_rows)), np.nan, dtype=float)
    for row in group1.values():
        g_idx = gammas.index(float(row["gamma"]))
        d_idx = [v[0] for v in i_dark_rows].index(float(row["I_dark"]))
        heatmap[g_idx, d_idx] = float(row["delta"])

    corruptions = list(group3["hat_corrupted"].keys())
    hat_mean = float(group3["mce_hat"])
    std_mean = float(group3["mce_std"])

    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.4))

    im = axes[0].imshow(heatmap, cmap="RdYlGn", aspect="auto")
    axes[0].set_xticks(np.arange(len(i_dark_rows)))
    axes[0].set_xticklabels([label for _, label in i_dark_rows])
    axes[0].set_yticks(np.arange(len(gammas)))
    axes[0].set_yticklabels([f"{g:.1f}" for g in gammas])
    axes[0].set_xlabel(r"$I_{\mathrm{dark}}$")
    axes[0].set_ylabel(r"$\gamma_{\mathrm{phys}}$")
    axes[0].set_title("Group 1: compensation gain (%)")
    for i in range(heatmap.shape[0]):
        for j in range(heatmap.shape[1]):
            axes[0].text(j, i, f"{heatmap[i, j]:.2f}", ha="center", va="center", fontsize=9)
    fig.colorbar(im, ax=axes[0], fraction=0.046, pad=0.04)

    axes[1].bar(["Standard clean", "HAT clean"], [group3["std_clean"], group3["hat_clean"]], color=["#9ecae1", "#3182bd"], edgecolor='#222222', linewidth=0.8)
    axes[1].bar(["Standard mCE", "HAT mCE"], [std_mean, hat_mean], color=["#fdd0a2", "#e6550d"], edgecolor='#222222', linewidth=0.8)
    axes[1].set_ylim(0, 100)
    axes[1].set_ylabel("Accuracy / mCE (%)")
    axes[1].set_title("Group 3: clean accuracy and CIFAR-10-C mCE")
    label_pending(axes[1], f"{len(corruptions)} corruption types aggregated")

    fig.suptitle("Fig. 6. Physical compensation and robustness summary")
    fig.savefig(output_dir / "fig6_physical_compensation.png", bbox_inches="tight")
    plt.close(fig)


def plot_fig7_retention_curve(output_dir: Path):
    convnext_rows = load_convnext_retention()
    tinyvit_rows = load_tinyvit_retention()

    if not convnext_rows and not tinyvit_rows:
        save_placeholder_figure(
            output_dir / "fig7_retention_curve.png",
            "Fig. 7. Retention decay",
            "No retention artifacts were found for ConvNeXt or Tiny-ViT.",
        )
        return

    fig, ax = plt.subplots(figsize=(7.4, 4.8))
    palette = {
        "ConvNeXt C9": "#2E5B88",
        "Tiny-ViT V4": "#3A8231",
    }
    tick_positions = [0.3, 1, 10, 100, 1000, 10000]
    tick_labels = ["0", "1", "10", "100", "1000", "10000"]

    if convnext_rows:
        convnext_rows = sorted(convnext_rows, key=lambda row: row["time_s"])
        x_vals = [0.3 if row["time_s"] == 0 else row["time_s"] for row in convnext_rows]
        y_vals = [row.get("mean_acc", row.get("test_acc_mean")) for row in convnext_rows]
        y_errs = [row.get("std_acc", row.get("test_acc_std", 0.0)) for row in convnext_rows]
        plot_band_curve(
            ax,
            x_vals,
            y_vals,
            y_errs,
            color=palette["ConvNeXt C9"],
            marker="o",
            label="ConvNeXt C9",
        )
        ax.annotate(f"{y_vals[-1]:.1f}%", (x_vals[-1], y_vals[-1]), xytext=(8, 0), textcoords="offset points",
                    ha="left", va="center", fontsize=9, color=palette["ConvNeXt C9"])
    if tinyvit_rows:
        tinyvit_rows = sorted(tinyvit_rows, key=lambda row: row["time_s"])
        x_vals = [0.3 if row["time_s"] == 0 else row["time_s"] for row in tinyvit_rows]
        y_vals = [row.get("mean_acc", row.get("test_acc_mean")) for row in tinyvit_rows]
        y_errs = [row.get("std_acc", row.get("test_acc_std", 0.0)) for row in tinyvit_rows]
        plot_band_curve(
            ax,
            x_vals,
            y_vals,
            y_errs,
            color=palette["Tiny-ViT V4"],
            marker="s",
            label="Tiny-ViT V4",
        )
        ax.annotate(f"{y_vals[-1]:.1f}%", (x_vals[-1], y_vals[-1]), xytext=(8, 0), textcoords="offset points",
                    ha="left", va="center", fontsize=9, color=palette["Tiny-ViT V4"])

    ax.set_xscale("log")
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels)
    ax.set_xlabel("Time since programming (s)")
    ax.set_ylabel("Accuracy (%)")
    ax.set_ylim(0, 100)
    ax.set_title("Fig. 7. Retention decay under programmed weight drift")
    ax.legend(frameon=True)
    enable_major_y_grid(ax)
    ax.axvspan(0.3, 10, color="#cccccc", alpha=0.08, zorder=0)
    ax.text(0.52, 0.08, "rapid initial decay", transform=ax.transAxes, fontsize=9, color="#666666")
    if not tinyvit_rows:
        label_pending(ax, "Tiny-ViT retention sweep pending")
    fig.text(
        0.5,
        -0.02,
        "Shaded bands denote ±1 standard deviation across Monte Carlo runs at each retention time.",
        ha="center",
        va="top",
        fontsize=9,
        color="#555555",
    )
    fig.savefig(output_dir / "fig7_retention_curve.png", bbox_inches="tight")
    plt.close(fig)


def plot_fig8_pareto(output_dir: Path):
    tinyvit_results = load_tinyvit_results()
    energy = parse_tinyvit_dryrun_energy()
    v1 = tinyvit_results.get("V1")

    fig, ax = plt.subplots(figsize=(7.0, 4.6))
    plotted_any = False

    if v1 is not None and "fp32_energy_uJ" in energy:
        ax.scatter(
            [energy["fp32_energy_uJ"]],
            [accuracy_value(v1)],
            s=120,
            color="#1f77b4",
            label="Tiny-ViT V1 digital baseline",
            zorder=3,
        )
        ax.annotate("V1", (energy["fp32_energy_uJ"], accuracy_value(v1)), textcoords="offset points", xytext=(6, 6))
        plotted_any = True

    ax.set_xscale("log")
    ax.set_xlabel("Energy per inference (µJ)")
    ax.set_ylabel("Accuracy (%)")
    ax.set_title("Fig. 8. Accuracy-energy Pareto frontier")
    ax.set_ylim(0, 100)

    if plotted_any:
        label_pending(
            ax,
            "Hybrid Tiny-ViT canonical points (V2-V6) will appear after finalized export; current dry-run ratio "
            f"is {energy.get('energy_reduction_ratio', float('nan')):.2f}x",
        )
        ax.legend(frameon=True)
    else:
        ax.text(
            0.5,
            0.5,
            "Awaiting finalized Tiny-ViT energy/accuracy points.\n"
            "The script will auto-populate this panel once the canonical V1-V6 results are exported.",
            ha="center",
            va="center",
            transform=ax.transAxes,
            bbox={"boxstyle": "round,pad=0.5", "facecolor": "#f4f4f4", "edgecolor": "#999999"},
        )

    fig.savefig(output_dir / "fig8_pareto_energy_accuracy.png", bbox_inches="tight")
    plt.close(fig)


def plot_fig9_noise_sensitivity(output_dir: Path):
    rows = maybe_load_noise_sweep_rows()
    if not rows:
        save_placeholder_figure(
            output_dir / "fig9_noise_sensitivity.png",
            "Fig. 9. Noise sensitivity sweep",
            "Pending Task 11 artifacts.\nExpected inputs: noise_sweep_results_gpt.json/csv\nfrom ConvNeXt C4 and Tiny-ViT V4 Monte Carlo inference sweeps.",
        )
        return

    noise_rows = [
        row for row in rows
        if row.get("sweep_type", "noise") == "noise"
    ]
    adc_rows = [
        row for row in rows
        if row.get("sweep_type") == "adc"
    ]

    required = {"model", "sigma_c2c", "sigma_d2d"}
    if noise_rows and not all(required.issubset(set(row.keys())) for row in noise_rows):
        save_placeholder_figure(
            output_dir / "fig9_noise_sensitivity.png",
            "Fig. 9. Noise sensitivity sweep",
            "Noise sweep artifact found, but its schema is not yet compatible with the paper plotting contract.",
        )
        return

    fig, axes = plt.subplots(1, 3, figsize=(14.4, 4.6), sharey=False)
    models = ["convnext", "tinyvit"]
    titles = ["ConvNeXt C4", "Tiny-ViT V4"]
    any_heatmap = False
    heatmap_im = None
    heatmap_axes_with_data = []
    vmin = 0.0
    vmax = 100.0

    for ax, model_name, title in zip(axes[:2], models, titles):
        model_rows = [row for row in noise_rows if str(row.get("model", "")).lower() == model_name]
        if not model_rows:
            ax.axis("off")
            ax.text(
                0.5,
                0.56,
                f"{title}\nData pending",
                ha="center",
                va="center",
                fontsize=12.5,
                color="#444444",
            )
            ax.text(
                0.5,
                0.42,
                "Task 21 noise sweep has not been completed\nfor this architecture/profile pair.",
                ha="center",
                va="center",
                fontsize=9.5,
                color="#666666",
            )
            continue
        any_heatmap = True
        c2c_vals = sorted({float(row["sigma_c2c"]) for row in model_rows})
        d2d_vals = sorted({float(row["sigma_d2d"]) for row in model_rows})
        grid = np.full((len(d2d_vals), len(c2c_vals)), np.nan, dtype=float)
        for row in model_rows:
            i = d2d_vals.index(float(row["sigma_d2d"]))
            j = c2c_vals.index(float(row["sigma_c2c"]))
            acc = row.get("mean_acc", row.get("test_acc_mean", row.get("acc_mean")))
            if acc is not None:
                grid[i, j] = float(acc)
        im = ax.imshow(grid, cmap="viridis", aspect="auto", origin="lower", vmin=vmin, vmax=vmax)
        heatmap_im = im
        heatmap_axes_with_data.append(ax)
        ax.set_xticks(np.arange(len(c2c_vals)))
        ax.set_xticklabels([f"{v:.2f}" for v in c2c_vals], rotation=45, ha="right")
        ax.set_yticks(np.arange(len(d2d_vals)))
        ax.set_yticklabels([f"{v:.2f}" for v in d2d_vals])
        ax.set_xlabel(r"$\sigma_{C2C}$")
        ax.set_title(title)
        if ax is axes[0]:
            ax.set_ylabel(r"$\sigma_{D2D}$")
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                if math.isnan(grid[i, j]):
                    continue
                txt_color = "white" if grid[i, j] < 55 else "#1b1b1b"
                ax.text(j, i, f"{grid[i, j]:.1f}", ha="center", va="center", fontsize=7.5, color=txt_color)

    if heatmap_im is not None and heatmap_axes_with_data:
        fig.colorbar(heatmap_im, ax=heatmap_axes_with_data, fraction=0.025, pad=0.02, label="Accuracy (%)")

    adc_ax = axes[2]
    if adc_rows:
        order = ["3-bit", "4-bit", "6-bit", "8-bit", "10-bit", "ideal"]
        x = np.arange(len(order))
        palette = {"convnext": "#2E5B88", "tinyvit": "#3A8231"}
        pretty_labels = {"convnext": "ConvNeXt C4", "tinyvit": "Tiny-ViT V4"}
        for model_name, marker in zip(models, ["o", "s"]):
            model_rows = [row for row in adc_rows if str(row.get("model", "")).lower() == model_name]
            if not model_rows:
                continue
            points = {}
            for row in model_rows:
                label = str(row.get("adc_label", row.get("adc_bits")))
                points[label] = row
            means = []
            stds = []
            for label in order:
                row = points.get(label)
                if row is None:
                    means.append(math.nan)
                    stds.append(0.0)
                else:
                    means.append(row.get("mean_acc", row.get("test_acc_mean", row.get("acc_mean"))))
                    stds.append(row.get("std_acc", row.get("test_acc_std", 0.0)))
            means = np.asarray(means, dtype=float)
            stds = np.asarray(stds, dtype=float)
            adc_ax.plot(
                x,
                means,
                marker=marker,
                linewidth=2.2,
                markersize=6.5,
                color=palette[model_name],
                label=pretty_labels[model_name],
            )
            adc_ax.fill_between(x, means - stds, means + stds, color=palette[model_name], alpha=0.14, linewidth=0)
        adc_ax.set_xticks(x)
        adc_ax.set_xticklabels(order, rotation=20, ha="right")
        adc_ax.set_ylabel("Accuracy (%)")
        adc_ax.set_ylim(0, 100)
        adc_ax.set_title("ADC sensitivity")
        adc_ax.axvline(order.index("6-bit"), color="#666666", linestyle="--", linewidth=1.0)
        adc_ax.text(order.index("6-bit") + 0.08, 8, "6-bit knee", rotation=90, va="bottom", ha="left", fontsize=8.5, color="#666666")
        adc_ax.legend(frameon=True)
    else:
        adc_ax.axis("off")
        adc_ax.text(
            0.5,
            0.5,
            "ADC sweep pending\n(expected after Task 11 extension)",
            ha="center",
            va="center",
        )

    fig.suptitle("Fig. 9. Accuracy under continuous noise and ADC sweeps")
    if not any_heatmap and not adc_rows:
        plt.close(fig)
        save_placeholder_figure(
            output_dir / "fig9_noise_sensitivity.png",
            "Fig. 9. Noise sensitivity sweep",
            "Noise sweep artifact exists but did not contain usable model rows.",
        )
        return
    fig.savefig(output_dir / "fig9_noise_sensitivity.png", bbox_inches="tight")
    plt.close(fig)


def plot_fig10_zero_shot_transferability(output_dir: Path):
    rows = maybe_load_device_comparison_rows()
    if not rows:
        save_placeholder_figure(
            output_dir / "fig10_zero_shot_transferability.png",
            "Fig. 10. Zero-shot hardware transferability",
            "Pending Task 12 artifacts.\nExpected inputs: device_comparison_results_gpt.json/csv\nfrom organic-HAT checkpoints evaluated under alternative device profiles.",
        )
        return

    if not all(("model" in row and ("device_type" in row or "profile" in row)) for row in rows):
        save_placeholder_figure(
            output_dir / "fig10_zero_shot_transferability.png",
            "Fig. 10. Zero-shot hardware transferability",
            "Device comparison artifact found, but its schema is not yet compatible with the paper plotting contract.",
        )
        return

    preferred_order = ["Organic OPECT", "Organic Pessimistic", "PCM (GST)", "RRAM (HfOx)", "Ideal"]
    device_labels = list(dict.fromkeys(str(row.get("device_type", row.get("profile"))) for row in rows))
    device_labels = [label for label in preferred_order if label in device_labels] + [
        label for label in device_labels if label not in preferred_order
    ]
    model_names = ["convnext", "tinyvit"]
    pretty_names = {"convnext": "ConvNeXt C4", "tinyvit": "Tiny-ViT V4"}
    colors = {"convnext": "#2E5B88", "tinyvit": "#3A8231"}

    fig, axes = plt.subplots(1, 2, figsize=(11.4, 4.8), sharex=True)
    y = np.arange(len(device_labels))
    for ax, model_name in zip(axes, model_names):
        model_rows = [row for row in rows if str(row.get("model")).lower() == model_name]
        vals = []
        source_best = math.nan
        for label in device_labels:
            row = next((r for r in model_rows if str(r.get("device_type", r.get("profile"))) == label), None)
            vals.append(accuracy_value(row))
            if row is not None and not math.isnan(source_best):
                pass
            if row is not None and math.isnan(source_best):
                source_best = float(row.get("checkpoint_best_acc", math.nan))
        vals_arr = np.asarray(vals, dtype=float)
        ax.barh(y, vals_arr, color=colors[model_name], edgecolor="#222222", linewidth=1.0, zorder=3)
        for ypos, val in zip(y, vals_arr):
            if math.isnan(val):
                continue
            ax.text(val + 1.0, ypos, f"{val:.1f}", va="center", ha="left", fontsize=9, color="#333333")
        if not math.isnan(source_best):
            ax.axvline(source_best, color="#666666", linestyle="--", linewidth=1.0)
            ax.text(source_best + 0.6, len(device_labels) - 0.55, f"source best {source_best:.1f}%", fontsize=8.5, color="#666666")
        ax.set_yticks(y)
        ax.set_yticklabels(device_labels if ax is axes[0] else [])
        ax.set_xlim(0, 100)
        ax.set_title(pretty_names[model_name])
        ax.set_axisbelow(True)

    axes[0].invert_yaxis()
    axes[0].set_ylabel("Device profile")
    axes[0].set_xlabel("Accuracy (%)")
    axes[1].set_xlabel("Accuracy (%)")
    fig.suptitle("Fig. 10. Zero-shot hardware transferability across device profiles", y=1.04, fontsize=13)
    fig.text(
        0.5,
        -0.02,
        "Dashed vertical line marks the source checkpoint best accuracy under the nominal training profile.",
        ha="center",
        va="top",
        fontsize=9,
        color="#555555",
    )
    fig.text(
        0.5,
        -0.08,
        "Interpret this as transferability across unseen device profiles, not as a comparison of device-specific optimal performance.",
        ha="center",
        va="top",
        fontsize=8.5,
        color="#666666",
    )
    fig.savefig(output_dir / "fig10_zero_shot_transferability.png", bbox_inches="tight")
    plt.close(fig)


def plot_fig11_energy_breakdown(output_dir):
    from pathlib import Path
    import matplotlib.pyplot as plt
    import math
    energy = parse_tinyvit_dryrun_energy()
    breakdown = parse_tinyvit_dryrun_breakdown()
    if not energy or not breakdown:
        save_placeholder_figure(
            output_dir / "fig11_energy_breakdown.png",
            "Fig. 11. Energy breakdown",
            "Tiny-ViT dry-run breakdown was not found.\nExpected source: tinyvit_hybrid_dryrun_report_gpt.md",
        )
        return

    labels = list(breakdown.keys())
    values = [breakdown[key] for key in labels]
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]
    fp32_total = energy.get("fp32_energy_uJ", math.nan)

    fig, ax = plt.subplots(figsize=(8.0, 4.0))

    left = 0.0
    for label, value, color in zip(labels, values, colors):
        ax.barh(["Hybrid Architecture"], [value], left=left, label=label, color=color, edgecolor='#222222', linewidth=0.8)
        left += value
    if not math.isnan(fp32_total):
        ax.barh(["Digital Baseline (GPU)"], [fp32_total], color="#bbbbbb", label="FP32 total reference", edgecolor='#222222', linewidth=0.8)

    ax.set_xlabel("Energy per inference (µJ)")
    ax.set_title("Energy Breakdown: Hybrid Architecture vs Digital Baseline")

    handles, legend_labels = ax.get_legend_handles_labels()
    by_label = dict(zip(legend_labels, handles))
    ax.legend(by_label.values(), by_label.keys(), frameon=True, loc="lower right", fontsize=9)

    fig.suptitle("Fig. 11. Energy Comparison")
    fig.savefig(output_dir / "fig11_energy_breakdown.png", bbox_inches="tight")
    plt.close(fig)


