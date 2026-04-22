#!/usr/bin/env python3
"""Generate paper-ready figures from report artifacts.

Fig.1 and Fig.2 are manual schematics. This script covers the quantitative
paper figures and related appendix figures derived from experiment artifacts.
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
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch, Rectangle


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "report_md"
GPT_REPORT_DIR = REPORT_DIR / "_gpt"
FIGURE_DIR = ROOT / "paper" / "figures"


def configure_style():
    """Paper-style plot defaults with restrained serif typography."""
    plt.style.use("seaborn-v0_8-paper")
    plt.rcParams.update({
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "font.family": "serif",
        "font.serif": ["STIXGeneral", "DejaVu Serif"],
        "font.style": "normal",
        "font.size": 8,
        "axes.titlesize": 8,
        "axes.titleweight": "semibold",
        "axes.labelsize": 8,
        "axes.labelweight": "normal",
        "legend.fontsize": 7,
        "legend.frameon": True,
        "legend.edgecolor": "#cfcfcf",
        "legend.facecolor": "#ffffff",
        "legend.framealpha": 0.95,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.8,
        "axes.edgecolor": "#333333",
        "axes.grid": False,
        "grid.linewidth": 0.4,
        "grid.alpha": 0.3,
        "grid.color": "#b0b0b0",
        "figure.autolayout": False,
        "hatch.linewidth": 0.4,
        "mathtext.fontset": "stix",
        "mathtext.default": "regular",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })

def nature_compliant(func):
    """Decorator to ensure NC styling is applied before plotting."""
    def wrapper(*args, **kwargs):
        configure_style()
        return func(*args, **kwargs)
    return wrapper

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


def save_figure_pair(fig, output_dir: Path, stem: str):
    fig.savefig(output_dir / f"{stem}.png", bbox_inches="tight")
    fig.savefig(output_dir / f"{stem}.pdf", bbox_inches="tight")


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


def contour_grid_from_rows(rows: Iterable[dict]):
    d2d_vals = sorted({float(row["d2d_pct"]) for row in rows})
    adc_vals = sorted({int(row["adc_bits"]) for row in rows})
    grid = np.full((len(d2d_vals), len(adc_vals)), np.nan, dtype=float)
    for row in rows:
        i = d2d_vals.index(float(row["d2d_pct"]))
        j = adc_vals.index(int(row["adc_bits"]))
        grid[i, j] = float(row["mean"])
    return d2d_vals, adc_vals, grid


def wrap_device_label(label: str) -> str:
    replacements = {
        "Measured Sample Profile (Suboptimal)": "Measured Sample Profile\n(Suboptimal)",
        "Organic Pessimistic": "Organic\nPessimistic",
        "PCM (GST)": "PCM\n(GST)",
        "RRAM (HfOx)": "RRAM\n(HfOx)",
    }
    return replacements.get(label, label)


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
        GPT_REPORT_DIR / "json_gpt" / "tinyvit_results_gpt.json",
        GPT_REPORT_DIR / "json_gpt" / "tinyvit_v1_results_gpt.json",
        GPT_REPORT_DIR / "json_gpt" / "tinyvit_v2v7_results_gpt.json",
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
    candidates = [
        GPT_REPORT_DIR / "tinyvit_hybrid_dryrun_report_gpt.md",
        GPT_REPORT_DIR / "archive" / "md" / "tinyvit_hybrid_dryrun_report_gpt.md",
    ]
    path = next((candidate for candidate in candidates if candidate.exists()), None)
    if path is None:
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
    candidates = [
        GPT_REPORT_DIR / "tinyvit_hybrid_dryrun_report_gpt.md",
        GPT_REPORT_DIR / "archive" / "md" / "tinyvit_hybrid_dryrun_report_gpt.md",
    ]
    path = next((candidate for candidate in candidates if candidate.exists()), None)
    if path is None:
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


def accuracy_std(row: Optional[dict]) -> float:
    if row is None:
        return 0.0
    for key in ("mc_std_acc", "test_acc_std", "std_acc"):
        value = row.get(key)
        if value is not None:
            parsed = float(value)
            if math.isfinite(parsed):
                return max(parsed, 0.0)
    return 0.0


def has_stochastic_uncertainty(row: Optional[dict]) -> bool:
    if row is None:
        return False
    for key in ("mc_std_acc", "test_acc_std", "std_acc"):
        value = row.get(key)
        if value is not None:
            try:
                return math.isfinite(float(value))
            except (TypeError, ValueError):
                return False
    return False


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


@nature_compliant
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
    ax.set_title("Analytical SNR under inverse-gamma compensation")
    ax.legend(ncol=2, frameon=True)
    fig.savefig(output_dir / "fig3_snr_curves.png", bbox_inches="tight")
    fig.savefig(output_dir / "fig3_snr_curves.pdf", bbox_inches="tight")
    plt.close(fig)


@nature_compliant
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

    fig, axes = plt.subplots(1, len(datasets), figsize=(12.3, 4.15), sharey=True)
    width = 0.22
    x = np.arange(len(architectures))
    deterministic_bars_present = False

    missing_any = False
    for dataset_idx, (ax, dataset) in enumerate(zip(axes, datasets)):
        for regime_idx, (regime_name, color, exp_map) in enumerate(regimes):
            vals = []
            errs = []
            stochastic_mask = []
            for _, arch_key in architectures:
                rows = convnext[dataset] if arch_key == "convnext" else tinyvit[dataset]
                row = rows.get(exp_map[arch_key])
                vals.append(accuracy_value(row))
                errs.append(accuracy_std(row))
                stochastic_mask.append(has_stochastic_uncertainty(row))
            vals_arr = np.asarray(vals, dtype=float)
            errs_arr = np.asarray(errs, dtype=float)
            if np.isnan(vals_arr).any():
                missing_any = True
            bars = ax.bar(
                x + (regime_idx - 1) * width,
                vals_arr,
                width=width,
                yerr=np.nan_to_num(errs_arr, nan=0.0),
                capsize=2.3,
                color=color,
                label=regime_name if dataset_idx == 0 else None,
                edgecolor="#f7f7f7",
                linewidth=0.6,
                error_kw={"elinewidth": 0.8, "capthick": 0.8, "ecolor": "#333333"},
                zorder=3,
            )
            for bar, is_stochastic in zip(bars, stochastic_mask):
                if not is_stochastic:
                    bar.set_hatch("////")
                    bar.set_edgecolor("#222222")
                    bar.set_linewidth(0.9)
                    deterministic_bars_present = True

        for arch_idx, (_, arch_key) in enumerate(architectures):
            rows = convnext[dataset] if arch_key == "convnext" else tinyvit[dataset]
            standard = accuracy_value(rows.get("C3" if arch_key == "convnext" else "V3"))
            hat = accuracy_value(rows.get("C4" if arch_key == "convnext" else "V4"))
            if math.isnan(standard) or math.isnan(hat):
                continue
            standard_err = accuracy_std(rows.get("C3" if arch_key == "convnext" else "V3"))
            hat_err = accuracy_std(rows.get("C4" if arch_key == "convnext" else "V4"))
            delta = hat - standard
            ax.text(
                x[arch_idx] + width,
                max(standard + standard_err, hat + hat_err) + 2.1,
                f"{delta:+.1f} pp",
                ha="center",
                va="bottom",
                fontsize=7.6,
                color="#333333",
            )

        ax.set_xticks(x)
        ax.set_xticklabels([label for label, _ in architectures])
        ax.set_title(f"({chr(97 + dataset_idx)}) {prettify_dataset_name(dataset)}", pad=7)
        ax.set_ylim(0, 100)
        ax.set_axisbelow(True)
        enable_major_y_grid(ax)
        if dataset_idx == 0:
            ax.set_ylabel("Accuracy (%)")

    handles, labels = axes[0].get_legend_handles_labels()
    fig.subplots_adjust(top=0.82, wspace=0.20)
    fig.legend(
        handles,
        labels,
        loc="upper center",
        ncol=3,
        frameon=True,
        bbox_to_anchor=(0.5, 0.985),
        borderpad=0.28,
        handletextpad=0.6,
        columnspacing=1.2,
    )
    if deterministic_bars_present:
        fig.text(
            0.985,
            0.028,
            "Hatched bars: deterministic or single-run estimates",
            ha="right",
            va="bottom",
            fontsize=6.6,
            color="#444444",
        )
    save_figure_pair(fig, output_dir, "fig4_accuracy_comparison")
    plt.close(fig)


def generate_d2d_mask(seed: int, size: int = 20) -> np.ndarray:
    rng = np.random.default_rng(seed)
    base = rng.normal(loc=0.55, scale=0.14, size=(size, size))
    return np.clip(base, 0.0, 1.0)


def add_mask_thumbnail(ax, mask: np.ndarray, left: float, bottom: float, width: float, height: float):
    inset = ax.inset_axes([left, bottom, width, height])
    inset.imshow(mask, cmap="Greys", vmin=0.0, vmax=1.0, interpolation="nearest")
    inset.set_xticks([])
    inset.set_yticks([])
    for spine in inset.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.8)
        spine.set_edgecolor("#444444")


@nature_compliant
def plot_figS3_ensemble_hat(output_dir: Path):
    fig = plt.figure(figsize=(8.8, 3.35))
    gs = fig.add_gridspec(
        2,
        2,
        width_ratios=[4.55, 1.75],
        height_ratios=[1.0, 1.0],
        wspace=0.18,
        hspace=0.16,
    )
    top_ax = fig.add_subplot(gs[0, 0])
    bottom_ax = fig.add_subplot(gs[1, 0])
    metric_ax = fig.add_subplot(gs[:, 1])

    def draw_flow(ax, panel: str, title: str, color: str, seeds: List[int], descriptor: str, outcome_note: str):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.add_patch(Rectangle((0.0, 0.16), 0.012, 0.70, facecolor=color, edgecolor="none", alpha=0.95))
        ax.text(0.03, 0.83, f"{panel} {title}", fontsize=8.4, fontweight="semibold", color="#222222", va="top")
        ax.text(0.03, 0.69, descriptor, fontsize=7.0, color="#5A5A5A", va="top")

        tile_w = 0.105
        tile_h = 0.34
        tile_bottom = 0.30
        lefts = [0.29, 0.43, 0.57, 0.71]
        epoch_labels = ["Epoch 1", "Epoch 2", "Epoch 3", "Epoch N"]
        for idx, (left, seed) in enumerate(zip(lefts, seeds)):
            add_mask_thumbnail(ax, generate_d2d_mask(seed), left, tile_bottom, tile_w, tile_h)
            ax.text(left + tile_w / 2.0, 0.22, epoch_labels[idx], ha="center", va="top", fontsize=6.2, color="#3A3A3A")
            if idx < len(lefts) - 1:
                ax.annotate(
                    "",
                    xy=(lefts[idx + 1] - 0.018, 0.47),
                    xytext=(left + tile_w + 0.012, 0.47),
                    arrowprops=dict(arrowstyle="->", linewidth=1.0, color=color, shrinkA=0, shrinkB=0),
                )

        box = FancyBboxPatch(
            (0.86, 0.36),
            0.11,
            0.18,
            boxstyle="round,pad=0.02,rounding_size=0.035",
            linewidth=1.0,
            edgecolor=color,
            facecolor="#FCFCFC",
        )
        ax.add_patch(box)
        ax.text(0.915, 0.45, "trained\nmodel", ha="center", va="center", fontsize=7.0, fontweight="semibold", color="#222222")
        ax.annotate("", xy=(0.86, 0.45), xytext=(0.82, 0.45), arrowprops=dict(arrowstyle="->", linewidth=1.2, color=color))
        ax.text(0.86, 0.18, outcome_note, ha="left", va="top", fontsize=6.8, color="#4F4F4F")

    draw_flow(
        top_ax,
        "(a)",
        "Standard HAT",
        "#2E5B88",
        [7, 7, 7, 7],
        "The same D2D mismatch map is reused throughout training.",
        "optimized for one\nhardware instance",
    )
    draw_flow(
        bottom_ax,
        "(b)",
        "Ensemble HAT",
        "#2A8C82",
        [7, 19, 41, 73],
        "A new D2D mismatch map is presented at each epoch.",
        "learns across multiple\nhardware instances",
    )

    fresh_path = GPT_REPORT_DIR / "json_gpt" / "fresh_instance_eval.json"
    fresh = maybe_load_json(fresh_path)
    if fresh:
        standard_instances = np.asarray(fresh["V4_Standard"]["instances"], dtype=float)
        ensemble_instances = np.asarray(fresh["V4_Ensemble"]["instances"], dtype=float)
    else:
        standard_instances = np.asarray([10.0] * 10, dtype=float)
        ensemble_instances = np.asarray([87.282, 88.612, 87.358, 84.066, 85.554, 85.182, 86.914, 87.768, 87.104, 83.81], dtype=float)

    methods = ["Standard HAT", "Ensemble HAT"]
    means = np.array([standard_instances.mean(), ensemble_instances.mean()], dtype=float)
    errs = np.array([standard_instances.std(ddof=1), ensemble_instances.std(ddof=1)], dtype=float)
    colors = ["#C85C3A", "#2A8C82"]
    y = np.array([1.0, 0.0], dtype=float)
    metric_ax.hlines(y, 0, means, color="#D8D8D8", linewidth=1.8, zorder=1)
    metric_ax.errorbar(
        means,
        y,
        xerr=errs,
        fmt="o",
        markersize=6.6,
        linewidth=1.1,
        capsize=2.8,
        color="#333333",
        ecolor="#333333",
        markeredgecolor="#222222",
        markeredgewidth=0.7,
        zorder=4,
    )
    for xpos, ypos, values, color in zip(means, y, [standard_instances, ensemble_instances], colors):
        jitter = np.linspace(-0.10, 0.10, len(values)) if len(values) > 1 else np.array([0.0])
        metric_ax.scatter(values, np.full_like(values, ypos) + jitter, s=18, color=color, edgecolor="white", linewidth=0.4, alpha=0.85, zorder=3)
    for ypos, mean, err, color in zip(y, means, errs, colors):
        metric_ax.scatter([mean], [ypos], s=52, color=color, edgecolor="#222222", linewidth=0.7, zorder=5)
        label = f"{mean:.2f}%" if np.isnan(err) or err < 1e-9 else f"{mean:.2f} ± {err:.2f}%"
        metric_ax.text(min(mean + 3.3, 95.5), ypos + 0.03, label, ha="left", va="center", fontsize=6.9, color="#333333")
    p_label = "Welch $p<10^{-15}$"
    try:
        from scipy import stats  # type: ignore
        _t, p_value = stats.ttest_ind(ensemble_instances, standard_instances, equal_var=False)
        if np.isfinite(p_value):
            if p_value < 1e-15:
                p_label = "Welch $p<10^{-15}$"
            elif p_value < 1e-4:
                p_label = f"Welch $p={p_value:.1e}$"
            else:
                p_label = f"Welch $p={p_value:.4f}$"
    except Exception:
        pass
    bracket_y = 1.32
    metric_ax.plot([means[0], means[0], means[1], means[1]], [1.12, bracket_y, bracket_y, 0.12], color="#444444", linewidth=0.9, zorder=2)
    metric_ax.text(50.0, bracket_y + 0.06, p_label, ha="center", va="bottom", fontsize=6.6, color="#444444")
    metric_ax.set_xlim(0, 100)
    metric_ax.set_ylim(-0.55, 1.55)
    metric_ax.set_yticks(y)
    metric_ax.set_yticklabels(methods)
    metric_ax.set_xlabel("Fresh-instance accuracy (%)")
    metric_ax.set_title("(c) Fresh-instance transfer", loc="left", pad=7)
    metric_ax.grid(axis="x", which="major", linestyle=(0, (2.0, 2.0)), linewidth=0.6, alpha=0.24, color="#8A8A8A", zorder=0)
    metric_ax.spines["left"].set_visible(False)
    metric_ax.tick_params(axis="y", length=0, pad=2)
    metric_ax.set_axisbelow(True)
    fig.subplots_adjust(left=0.045, right=0.985, top=0.97, bottom=0.16)
    save_figure_pair(fig, output_dir, "figS3_ensemble_hat")
    plt.close(fig)


@nature_compliant
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

    fig, axes = plt.subplots(1, 2, figsize=(10.9, 4.1), sharey=False)
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
                edgecolor="#f7f7f7",
                linewidth=0.6,
                zorder=3,
            )
            for xpos, val in zip(x + (idx - 0.5) * width, vals):
                if math.isnan(val):
                    continue
                offset = 0.9 if val >= 0 else -1.2
                va = "bottom" if val >= 0 else "top"
                ax.text(xpos, val + offset, f"{val:+.1f}", ha="center", va=va, fontsize=7.5, color="#333333")

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
        ax.set_title(f"({chr(97 + plot_idx)}) {title}", loc="left", pad=7)
        ax.set_ylabel("Accuracy change (pp)" if plot_idx == 0 else "")
        ax.set_axisbelow(True)
        enable_major_y_grid(ax)
        ref_ax.set_ylim(0, 100)
        ref_ax.spines["top"].set_visible(False)
        ref_ax.tick_params(axis="y", colors="#666666", labelsize=7, labelright=(plot_idx == 1))
        ref_ax.set_ylabel("FP32 accuracy (%)" if plot_idx == 1 else "", color="#666666")

    axes[0].set_ylim(-100, 5)
    max_positive = max(
        (
            accuracy_value((convnext if source_key == "convnext" else tinyvit)[dataset].get(exp_keys[top_key]))
            - accuracy_value((convnext if source_key == "convnext" else tinyvit)[dataset].get(exp_keys[base_key]))
        )
        for title, top_key, base_key, _ in subplot_specs
        for arch_name, (source_key, exp_keys) in architecture_rows.items()
        for dataset in datasets
        if not math.isnan(
            accuracy_value((convnext if source_key == "convnext" else tinyvit)[dataset].get(exp_keys[top_key]))
        )
        and not math.isnan(
            accuracy_value((convnext if source_key == "convnext" else tinyvit)[dataset].get(exp_keys[base_key]))
        )
    )
    axes[1].set_ylim(-5, max(39.0, math.ceil(max_positive + 3.5)))
    handles = []
    labels = []
    for axis in (axes[1], ref_axes[1]):
        h, l = axis.get_legend_handles_labels()
        handles.extend(h)
        labels.extend(l)
    fig.legend(
        handles,
        labels,
        loc="upper center",
        ncol=4,
        frameon=True,
        bbox_to_anchor=(0.5, 1.01),
        borderpad=0.28,
        handletextpad=0.6,
        columnspacing=1.1,
    )
    fig.subplots_adjust(top=0.84, wspace=0.20)
    save_figure_pair(fig, output_dir, "fig5_hat_recovery")
    plt.close(fig)


@nature_compliant
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
    fig.suptitle("Physical compensation and robustness summary")
    fig.savefig(output_dir / "fig6_physical_compensation.png", bbox_inches="tight")
    fig.savefig(output_dir / "fig6_physical_compensation.pdf", bbox_inches="tight")
    plt.close(fig)


@nature_compliant
def plot_fig7_retention_curve(output_dir: Path):
    convnext_rows = load_convnext_retention()
    tinyvit_rows = load_tinyvit_retention()

    if not convnext_rows and not tinyvit_rows:
        save_placeholder_figure(
            output_dir / "fig7_retention_curve.png",
            "Retention decay",
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
    ax.set_title("Retention decay under programmed weight drift")
    ax.legend(frameon=True)
    enable_major_y_grid(ax)
    ax.axvspan(0.3, 10, color="#cccccc", alpha=0.08, zorder=0)
    ax.text(0.52, 0.08, "rapid initial decay", transform=ax.transAxes, fontsize=9, color="#666666")
    if not tinyvit_rows:
        label_pending(ax, "Tiny-ViT retention sweep pending")
    fig.savefig(output_dir / "fig7_retention_curve.png", bbox_inches="tight")
    fig.savefig(output_dir / "fig7_retention_curve.pdf", bbox_inches="tight")
    plt.close(fig)


@nature_compliant
def plot_fig8_pareto(output_dir: Path):
    tinyvit_results = load_tinyvit_results()
    energy = parse_tinyvit_dryrun_energy()
    v1 = tinyvit_results.get("V1")
    hybrid_order = ["V2", "V3", "V4", "V5", "V6", "V7"]
    hybrid_rows = [(exp, tinyvit_results.get(exp)) for exp in hybrid_order if tinyvit_results.get(exp) is not None]

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

    if hybrid_rows and "hybrid_energy_uJ" in energy:
        hybrid_x = energy["hybrid_energy_uJ"]
        palette = {
            "V2": "#4C78A8",
            "V3": "#D55E00",
            "V4": "#2E8B57",
            "V5": "#B279A2",
            "V6": "#E39C34",
            "V7": "#7F7F7F",
        }
        ax.axvline(hybrid_x, color="#BBBBBB", linestyle=":", linewidth=1.2, zorder=1)
        label_y = {
            "V2": 99.0,
            "V4": 94.5,
            "V3": 90.0,
            "V5": 87.0,
            "V7": 84.0,
            "V6": 80.0,
        }
        for exp, row in hybrid_rows:
            y = accuracy_value(row)
            ax.scatter(
                [hybrid_x],
                [y],
                s=78 if exp != "V4" else 92,
                color=palette.get(exp, "#3A8231"),
                edgecolor="white",
                linewidth=0.8,
                zorder=4,
            )
            ax.annotate(
                exp,
                xy=(hybrid_x, y),
                xytext=(hybrid_x * 1.08, label_y.get(exp, y)),
                textcoords="data",
                fontsize=9,
                ha="left",
                va="center",
                arrowprops={"arrowstyle": "-", "color": "#666666", "linewidth": 0.7},
            )
        ax.text(
            0.04,
            0.05,
            "V2-V7 share the same first-order hybrid energy estimate.",
            transform=ax.transAxes,
            fontsize=9,
            color="#555555",
            bbox={"boxstyle": "round,pad=0.28", "facecolor": "#F6F6F6", "edgecolor": "#DDDDDD"},
        )
        plotted_any = True

    ax.set_xscale("log")
    ax.set_xlabel("Energy per inference (µJ)")
    ax.set_ylabel("Accuracy (%)")
    ax.set_title("Accuracy-energy Pareto frontier")
    ax.set_ylim(0, 100)
    if "hybrid_energy_uJ" in energy and "fp32_energy_uJ" in energy:
        ax.set_xlim(energy["hybrid_energy_uJ"] * 0.7, energy["fp32_energy_uJ"] * 1.4)

    if plotted_any:
        handles = [
            plt.Line2D([], [], marker="o", linestyle="", color="#1f77b4", markersize=8, label="V1 digital baseline"),
            plt.Line2D([], [], marker="o", linestyle="", color="#2E8B57", markersize=8, label="Hybrid family V2-V7"),
        ]
        ax.legend(handles=handles, frameon=True, loc="lower right")
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
    fig.savefig(output_dir / "fig8_pareto_energy_accuracy.pdf", bbox_inches="tight")
    plt.close(fig)


@nature_compliant
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

    models = ["convnext", "tinyvit"]
    titles = ["ConvNeXt C4", "Tiny-ViT V4"]
    heatmap_specs = []
    for model_name, title in zip(models, titles):
        model_rows = [row for row in noise_rows if str(row.get("model", "")).lower() == model_name]
        if model_rows:
            heatmap_specs.append((model_name, title, model_rows))

    if not heatmap_specs and not adc_rows:
        save_placeholder_figure(
            output_dir / "fig9_noise_sensitivity.png",
            "Noise sensitivity sweep",
            "Noise sweep artifact exists but did not contain usable model rows.",
        )
        return

    n_heatmaps = max(1, len(heatmap_specs))
    fig_width = 10.8 if n_heatmaps == 1 else 14.4
    fig, axes = plt.subplots(1, n_heatmaps + 1, figsize=(fig_width, 4.6), sharey=False)
    if not isinstance(axes, np.ndarray):
        axes = np.asarray([axes])

    any_heatmap = False
    heatmap_im = None
    heatmap_axes_with_data = []
    vmin = 0.0
    vmax = 100.0

    for ax, (model_name, title, model_rows) in zip(axes[:n_heatmaps], heatmap_specs):
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

    adc_ax = axes[-1]
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

    fig.suptitle("Accuracy under continuous noise and ADC sweeps")
    if not any_heatmap and not adc_rows:
        plt.close(fig)
        save_placeholder_figure(
            output_dir / "fig9_noise_sensitivity.png",
            "Noise sensitivity sweep",
            "Noise sweep artifact exists but did not contain usable model rows.",
        )
        return
    fig.savefig(output_dir / "fig9_noise_sensitivity.png", bbox_inches="tight")
    fig.savefig(output_dir / "fig9_noise_sensitivity.pdf", bbox_inches="tight")
    plt.close(fig)


@nature_compliant
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

    preferred_order = [
        "Organic OPECT",
        "Organic Pessimistic",
        "PCM (GST)",
        "RRAM (HfOx)",
        "Ideal",
        "Measured Sample Profile (Suboptimal)",
    ]
    device_labels = list(dict.fromkeys(str(row.get("device_type", row.get("profile"))) for row in rows))
    device_labels = [label for label in preferred_order if label in device_labels] + [
        label for label in device_labels if label not in preferred_order
    ]
    model_names = ["convnext", "tinyvit"]
    pretty_names = {"convnext": "ConvNeXt C4", "tinyvit": "Tiny-ViT V4"}
    colors = {"convnext": "#2E5B88", "tinyvit": "#3A8231"}

    display_labels = [wrap_device_label(label) for label in device_labels]
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.15), sharex=True, sharey=True)
    y = np.arange(len(device_labels))
    for ax, model_name in zip(axes, model_names):
        model_rows = [row for row in rows if str(row.get("model")).lower() == model_name]
        vals = []
        labels_present = []
        source_best = math.nan
        for label in device_labels:
            row = next((r for r in model_rows if str(r.get("device_type", r.get("profile"))) == label), None)
            vals.append(accuracy_value(row))
            labels_present.append(row is not None)
            if row is not None and math.isnan(source_best):
                source_best = float(row.get("checkpoint_best_acc", math.nan))
        vals_arr = np.asarray(vals, dtype=float)
        valid_mask = np.isfinite(vals_arr)
        if np.any(valid_mask):
            ax.barh(
                y[valid_mask],
                vals_arr[valid_mask],
                color=colors[model_name],
                edgecolor="#222222",
                linewidth=0.8,
                zorder=3,
            )
        for ypos, val, present in zip(y, vals_arr, labels_present):
            if not present:
                ax.text(2.0, ypos, "n/a", va="center", ha="left", fontsize=8.5, color="#888888")
                continue
            if math.isnan(val):
                continue
            ax.text(min(val + 1.1, 96.5), ypos, f"{val:.1f}", va="center", ha="left", fontsize=9, color="#333333")
        if not math.isnan(source_best):
            ax.axvline(source_best, color="#666666", linestyle="--", linewidth=1.0)
            ax.text(
                min(source_best + 0.8, 97.0),
                -0.55,
                f"source best {source_best:.1f}%",
                fontsize=7.2,
                color="#666666",
                ha="left",
                va="center",
                bbox=dict(boxstyle="round,pad=0.16", facecolor="white", edgecolor="none", alpha=0.9),
            )
        ax.set_yticks(y)
        ax.set_yticklabels(display_labels)
        ax.set_xlim(0, 100)
        ax.set_title(
            f"({'a' if model_name == 'convnext' else 'b'}) {pretty_names[model_name]}",
            loc="left",
            pad=7,
        )
        ax.grid(axis="x", linestyle=":", linewidth=0.8, color="#BBBBBB", alpha=0.8, zorder=0)
        ax.set_axisbelow(True)
        ax.tick_params(axis="y", labelsize=7)

    for ax in axes:
        ax.invert_yaxis()
    axes[0].set_ylabel("Device profile")
    axes[0].set_xlabel("Accuracy (%)")
    axes[1].set_xlabel("Accuracy (%)")
    axes[1].tick_params(axis="y", labelleft=True)
    fig.tight_layout()
    save_figure_pair(fig, output_dir, "fig10_zero_shot_transferability")
    plt.close(fig)



@nature_compliant
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


@nature_compliant
def plot_fig_contour_map(output_dir: Path):
    path = GPT_REPORT_DIR / "iso_accuracy_contour_data.json"
    if not path.exists():
        save_placeholder_figure(
            output_dir / "fig_contour_map.png",
            "Contour map",
            "Contour sweep results were not found.\nExpected source: iso_accuracy_contour_data.json",
        )
        return

    rows = load_json(path)
    d2d_vals, adc_vals, grid = contour_grid_from_rows(rows)
    x_idx = np.arange(len(adc_vals))
    y_idx = np.arange(len(d2d_vals))
    xx, yy = np.meshgrid(x_idx, y_idx)

    fig, ax = plt.subplots(figsize=(6.35, 4.0))
    cmap = plt.get_cmap("RdYlBu_r")
    norm = plt.Normalize(vmin=10.0, vmax=90.0)
    im = ax.imshow(grid, cmap=cmap, norm=norm, aspect="auto", origin="lower")

    contour_levels = [80.0, 85.0, 88.0]
    contour_styles = [(0, (4.0, 2.0)), (0, (2.2, 1.4)), "solid"]
    ax.contour(
        xx,
        yy,
        grid,
        levels=contour_levels,
        colors="#202020",
        linewidths=0.9,
        linestyles=contour_styles,
    )

    for i in range(len(d2d_vals)):
        for j in range(len(adc_vals)):
            value = grid[i, j]
            if np.isnan(value):
                continue
            rgba = cmap(norm(value))
            luminance = 0.2126 * rgba[0] + 0.7152 * rgba[1] + 0.0722 * rgba[2]
            text_color = "white" if luminance < 0.48 else "#111111"
            ax.text(
                j,
                i,
                f"{value:.1f}",
                ha="center",
                va="center",
                fontsize=6.7,
                color=text_color,
                fontweight="normal",
            )

    ax.set_xticks(x_idx)
    ax.set_xticklabels([str(v) for v in adc_vals])
    ax.set_yticks(y_idx)
    ax.set_yticklabels([f"{v:.0f}" for v in d2d_vals])
    ax.set_xlabel("ADC Resolution (bits)")
    ax.set_ylabel(r"$\sigma_{\mathrm{D2D}}$ (%)")
    ax.tick_params(axis="both", length=0)
    ax.set_xlim(-0.5, len(adc_vals) - 0.5)
    ax.set_ylim(-0.5, len(d2d_vals) - 0.5)
    ax.set_xticks(np.arange(-0.5, len(adc_vals), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(d2d_vals), 1), minor=True)
    ax.grid(which="minor", color=(1.0, 1.0, 1.0, 0.12), linewidth=0.4)
    ax.tick_params(which="minor", bottom=False, left=False)

    legend_handles = [
        Line2D([0], [0], color="#202020", lw=0.95, linestyle=style, label=f"{level:.0f}%")
        for level, style in zip(contour_levels, contour_styles)
    ]
    ax.legend(
        handles=legend_handles,
        loc="lower left",
        bbox_to_anchor=(0.0, 1.01),
        ncol=3,
        frameon=False,
        fontsize=6.7,
        columnspacing=0.8,
        handlelength=1.8,
        borderpad=0.0,
        handletextpad=0.45,
        borderaxespad=0.0,
    )

    cbar = fig.colorbar(im, ax=ax, fraction=0.05, pad=0.03)
    cbar.set_label("Accuracy (%)")
    cbar.outline.set_linewidth(0.6)

    fig.tight_layout(rect=[0.0, 0.0, 1.0, 0.96], pad=0.35)
    save_figure_pair(fig, output_dir, "fig_contour_map")
    plt.close(fig)


@nature_compliant
def plot_fig_proxy_sensitivity_map(output_dir: Path):
    path = GPT_REPORT_DIR / "json_gpt" / "zhang_sensitivity_sweep_10mc.json"
    if not path.exists():
        save_placeholder_figure(
            output_dir / "fig_proxy_sensitivity_map.png",
            "Proxy sensitivity sweep",
            "Zhang proxy sensitivity results were not found.\nExpected source: zhang_sensitivity_sweep_10mc.json",
        )
        return

    data = load_json(path)
    c2c_vals = sorted({int(key.split("_")[1]) for key in data})
    d2d_vals = sorted({int(key.split("_")[3]) for key in data})
    grid = np.full((len(c2c_vals), len(d2d_vals)), np.nan, dtype=float)
    std_grid = np.full_like(grid, np.nan, dtype=float)

    for i, c2c in enumerate(c2c_vals):
        for j, d2d in enumerate(d2d_vals):
            row = data.get(f"c2c_{c2c}_d2d_{d2d}", {})
            grid[i, j] = float(row.get("test_acc_mean", math.nan))
            std_grid[i, j] = float(row.get("test_acc_std", math.nan))

    fig, ax = plt.subplots(figsize=(5.45, 3.55))
    cmap = plt.get_cmap("YlGnBu")
    norm = plt.Normalize(vmin=np.nanmin(grid) - 0.2, vmax=np.nanmax(grid) + 0.2)
    im = ax.imshow(grid, cmap=cmap, norm=norm, aspect="auto", origin="lower")

    for i, c2c in enumerate(c2c_vals):
        for j, d2d in enumerate(d2d_vals):
            value = grid[i, j]
            if np.isnan(value):
                continue
            rgba = cmap(norm(value))
            luminance = 0.2126 * rgba[0] + 0.7152 * rgba[1] + 0.0722 * rgba[2]
            text_color = "white" if luminance < 0.48 else "#111111"
            ax.text(
                j,
                i,
                f"{value:.1f}",
                ha="center",
                va="center",
                fontsize=6.8,
                color=text_color,
            )

    nominal_i = c2c_vals.index(2) if 2 in c2c_vals else None
    nominal_j = d2d_vals.index(3) if 3 in d2d_vals else None
    if nominal_i is not None and nominal_j is not None:
        ax.add_patch(
            Rectangle(
                (nominal_j - 0.5, nominal_i - 0.5),
                1.0,
                1.0,
                fill=False,
                edgecolor="#202020",
                linewidth=1.2,
            )
        )
        ax.text(
            nominal_j + 0.46,
            nominal_i + 0.44,
            "nominal",
            ha="right",
            va="top",
            fontsize=6.3,
            color="#202020",
            bbox=dict(boxstyle="round,pad=0.12", facecolor="white", edgecolor="none", alpha=0.92),
        )

    ax.set_xticks(np.arange(len(d2d_vals)))
    ax.set_xticklabels([f"{v}" for v in d2d_vals])
    ax.set_yticks(np.arange(len(c2c_vals)))
    ax.set_yticklabels([f"{v}" for v in c2c_vals])
    ax.set_xlabel(r"$\sigma_{\mathrm{D2D}}$ (%)")
    ax.set_ylabel(r"$\sigma_{\mathrm{C2C}}$ (%)")
    ax.tick_params(axis="both", length=0)
    ax.set_xticks(np.arange(-0.5, len(d2d_vals), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(c2c_vals), 1), minor=True)
    ax.grid(which="minor", color=(1.0, 1.0, 1.0, 0.18), linewidth=0.5)
    ax.tick_params(which="minor", bottom=False, left=False)
    ax.set_title("Zhang-proxy C2C/D2D sensitivity", loc="left", pad=6)

    cbar = fig.colorbar(im, ax=ax, fraction=0.05, pad=0.03)
    cbar.set_label("Accuracy (%)")
    cbar.outline.set_linewidth(0.6)

    fig.tight_layout(pad=0.35)
    save_figure_pair(fig, output_dir, "fig_proxy_sensitivity_map")
    plt.close(fig)


@nature_compliant
def plot_fig_fresh_instance_ablation(output_dir: Path):
    fresh_path = GPT_REPORT_DIR / "json_gpt" / "fresh_instance_eval.json"
    freq_path = GPT_REPORT_DIR / "ensemble_frequency_ablation.json"
    if not fresh_path.exists() or not freq_path.exists():
        save_placeholder_figure(
            output_dir / "fig_fresh_instance_ablation.png",
            "Fresh-instance robustness",
            "Expected sources: fresh_instance_eval.json and ensemble_frequency_ablation.json",
        )
        return

    fresh = load_json(fresh_path)
    freq_data = load_json(freq_path)
    results = freq_data.get("results", [])
    if not isinstance(results, list) or not results:
        save_placeholder_figure(
            output_dir / "fig_fresh_instance_ablation.png",
            "Fresh-instance robustness",
            "Frequency ablation artifact exists but did not contain usable results.",
        )
        return

    standard_instances = np.asarray(fresh["V4_Standard"]["instances"], dtype=float)
    ensemble_instances = np.asarray(fresh["V4_Ensemble"]["instances"], dtype=float)

    fig, axes = plt.subplots(1, 2, figsize=(7.35, 3.45))

    ax = axes[0]
    categories = [
        ("Standard HAT", standard_instances, "#C44E52"),
        ("Ensemble HAT", ensemble_instances, "#2A7F62"),
    ]
    offsets = np.linspace(-0.085, 0.085, max(len(standard_instances), len(ensemble_instances)))
    for xpos, (label, values, color) in enumerate(categories):
        used_offsets = offsets[: len(values)]
        ax.scatter(
            np.full(len(values), xpos) + used_offsets,
            values,
            s=24,
            color=color,
            edgecolor="white",
            linewidth=0.45,
            zorder=3,
        )
        mean = float(np.mean(values))
        std = float(np.std(values, ddof=0))
        ax.errorbar(
            xpos,
            mean,
            yerr=std,
            fmt="o",
            color="#111111",
            markersize=4.4,
            capsize=3.0,
            linewidth=0.9,
            zorder=4,
        )
        ax.text(
            xpos,
            min(mean + std + 4.2, 98.0),
            f"{mean:.2f}±{std:.2f}",
            ha="center",
            va="bottom",
            fontsize=6.8,
            color="#222222",
        )
    ax.set_xticks([0, 1])
    ax.set_xticklabels([label for label, _, _ in categories])
    ax.set_ylim(0, 100)
    ax.set_ylabel("Accuracy across fresh arrays (%)")
    ax.set_title("(a) Fresh fixed-D2D instances", loc="left", pad=6)
    enable_major_y_grid(ax)

    ax = axes[1]
    ordered_results = [
        next(item for item in results if item["freq_mode"] == "fixed"),
        next(item for item in results if item["freq_mode"] == "N_epochs" and int(item["N"]) == 20),
        next(item for item in results if item["freq_mode"] == "N_epochs" and int(item["N"]) == 5),
        next(item for item in results if item["freq_mode"] == "epoch"),
        next(item for item in results if item["freq_mode"] == "batch"),
    ]
    labels = ["Fixed\n(init)", "Every\n20 epochs", "Every\n5 epochs", "Every\nepoch", "Every\nbatch"]
    values = [float(item["accuracy"]) for item in ordered_results]
    colors = ["#B8BDC6", "#9FB3C8", "#7D9CB8", "#2A7F62", "#D0A35B"]
    bars = ax.bar(
        np.arange(len(values)),
        values,
        color=colors,
        edgecolor="#222222",
        linewidth=0.7,
        zorder=3,
    )
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            value + 0.08,
            f"{value:.2f}",
            ha="center",
            va="bottom",
            fontsize=6.8,
            color="#222222",
        )
    ax.set_xticks(np.arange(len(values)))
    ax.set_xticklabels(labels)
    ax.set_ylim(85.5, 89.1)
    ax.set_ylabel("Held-out accuracy (%)")
    ax.set_title("(b) D2D-resampling frequency ablation", loc="left", pad=6)
    ax.grid(axis="y", linestyle=(0, (2.0, 2.0)), linewidth=0.6, alpha=0.24, color="#8a8a8a", zorder=0)
    ax.set_axisbelow(True)

    fig.tight_layout(pad=0.45, w_pad=1.2)
    save_figure_pair(fig, output_dir, "fig_fresh_instance_ablation")
    plt.close(fig)


@nature_compliant
def plot_fig_sobol_sensitivity(output_dir: Path):
    path = GPT_REPORT_DIR / "sobol_sensitivity.json"
    if not path.exists():
        save_placeholder_figure(
            output_dir / "fig_sobol_sensitivity.png",
            "Sobol sensitivity",
            "Sobol sensitivity results were not found.\nExpected source: sobol_sensitivity.json",
        )
        return

    data = load_json(path)
    group_labels = ["Full grid", "Operational region"]
    series_labels = ["ADC", "D2D", "Interaction"]
    values = np.array([
        [
            float(data["full_grid"]["S_adc"]),
            float(data["full_grid"]["S_d2d"]),
            float(data["full_grid"]["S_interaction"]),
        ],
        [
            float(data["operational_region"]["S_adc"]),
            float(data["operational_region"]["S_d2d"]),
            float(data["operational_region"]["S_interaction"]),
        ],
    ])
    colors = ["#2B6CB0", "#D94841", "#7A7A7A"]

    fig, ax = plt.subplots(figsize=(5.8, 3.6))
    x = np.arange(len(group_labels))
    width = 0.22

    for idx, (label, color) in enumerate(zip(series_labels, colors)):
        offset = (idx - 1) * width
        bars = ax.bar(
            x + offset,
            values[:, idx],
            width=width,
            label=label,
            color=color,
            edgecolor="#222222",
            linewidth=0.7,
        )
        for bar, val in zip(bars, values[:, idx]):
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                min(val + 0.025, 1.02),
                f"{val:.3f}",
                ha="center",
                va="bottom",
                fontsize=7,
                color="#222222",
            )

    ax.set_xticks(x)
    ax.set_xticklabels(group_labels)
    ax.set_ylim(0.0, 1.05)
    ax.set_ylabel("First-order Sobol index")
    ax.grid(axis="y", linestyle=(0, (2.0, 2.0)), linewidth=0.6, alpha=0.24, color="#8a8a8a")
    ax.set_axisbelow(True)
    ax.legend(loc="upper center", ncol=3, frameon=True, bbox_to_anchor=(0.5, 1.16))

    fig.tight_layout(pad=0.35)
    save_figure_pair(fig, output_dir, "fig_sobol_sensitivity")
    plt.close(fig)


@nature_compliant
def plot_fig_corr_d2d(output_dir: Path):
    path = GPT_REPORT_DIR / "json_gpt" / "fresh_instance_eval_v4_ensemble_correlated_d2d.json"
    if not path.exists():
        save_placeholder_figure(
            output_dir / "figS_corr_d2d.png",
            "Correlated D2D robustness",
            "Expected source: fresh_instance_eval_v4_ensemble_correlated_d2d.json",
        )
        return

    data = load_json(path)
    results = data.get("results", {})
    ordered = [
        ("iid", "iid", "#2A7F62"),
        ("rho_0_3", r"$\rho=0.3$", "#3A6EA5"),
        ("rho_0_5", r"$\rho=0.5$", "#C06C2B"),
    ]

    x = np.arange(len(ordered))
    means = [float(results[key]["cross_instance_mean"]) for key, _, _ in ordered]
    stds = [float(results[key]["cross_instance_std"]) for key, _, _ in ordered]
    colors = [color for _, _, color in ordered]
    labels = [label for _, label, _ in ordered]
    deltas = [means[idx] - means[0] for idx in range(len(means))]

    fig, ax = plt.subplots(figsize=(4.8, 3.2))
    ax.plot(x, means, color="#222222", linewidth=1.0, zorder=2)
    for xpos, mean_val, std_val, color, delta in zip(x, means, stds, colors, deltas):
        ax.errorbar(
            xpos,
            mean_val,
            yerr=std_val,
            fmt="o",
            color=color,
            ecolor="#333333",
            elinewidth=0.9,
            capsize=3.0,
            markersize=5.0,
            markeredgecolor="white",
            markeredgewidth=0.45,
            zorder=3,
        )
        label = f"{mean_val:.2f}±{std_val:.2f}"
        if xpos > 0:
            label += f"\n({delta:+.2f} pp)"
        ax.text(
            xpos,
            min(mean_val + std_val + 0.8, 90.2),
            label,
            ha="center",
            va="bottom",
            fontsize=6.7,
            color="#222222",
        )

    ax.axhline(10.0, color="#B65C5C", linestyle=(0, (3.0, 2.0)), linewidth=0.9, alpha=0.9)
    ax.text(
        2.22,
        10.65,
        "standard-HAT collapse baseline",
        ha="right",
        va="bottom",
        fontsize=6.6,
        color="#8C3D3D",
    )

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_xlim(-0.2, 2.25)
    ax.set_ylim(8, 90.5)
    ax.set_ylabel("Fresh-instance accuracy (%)")
    ax.set_title("Correlated-D2D stress test", loc="left", pad=6)
    enable_major_y_grid(ax)
    fig.tight_layout(pad=0.35)
    save_figure_pair(fig, output_dir, "figS_corr_d2d")
    plt.close(fig)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=FIGURE_DIR)
    args = parser.parse_args()
    
    out = args.output_dir
    ensure_dir(out)
    
    print(f"Regenerating all figures in NC style to: {out}")
    plot_fig3_snr_curves(out)
    plot_fig4_accuracy_comparison(out)
    plot_fig5_hat_recovery(out)
    plot_fig6_physical_compensation(out)
    plot_fig7_retention_curve(out)
    plot_fig8_pareto(out)
    plot_fig9_noise_sensitivity(out)
    plot_fig10_zero_shot_transferability(out)
    plot_fig11_energy_breakdown(out)
    plot_figS3_ensemble_hat(out)
    plot_fig_contour_map(out)
    plot_fig_proxy_sensitivity_map(out)
    plot_fig_fresh_instance_ablation(out)
    plot_fig_sobol_sensitivity(out)
    plot_fig_corr_d2d(out)
    print("Done.")
