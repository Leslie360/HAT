#!/usr/bin/env python3
"""Analyze EPSC CSV exports for the 2026-05-03 doctoral-data packet."""

from __future__ import annotations

import math
import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parent
FIG_DIR = ROOT / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)
TINOS_DIR = Path("/usr/share/fonts/truetype/croscore")
for font_file in TINOS_DIR.glob("Tinos-*.ttf"):
    font_manager.fontManager.addfont(str(font_file))

COL = {
    "ink": "#1E252B",
    "muted": "#66717A",
    "grid": "#E1E6EB",
    "blue": "#0072B2",
    "orange": "#D55E00",
    "green": "#009E73",
    "gold": "#E69F00",
    "gray": "#7A7F85",
    "red": "#B94A48",
}

plt.rcParams.update({
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "font.family": "Tinos",
    "font.serif": ["Tinos", "Times New Roman", "Nimbus Roman", "Liberation Serif", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 11.0,
    "axes.titlesize": 12.5,
    "axes.titleweight": "bold",
    "axes.labelsize": 11.5,
    "xtick.labelsize": 10.2,
    "ytick.labelsize": 10.2,
    "legend.fontsize": 9.8,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": COL["ink"],
    "axes.linewidth": 0.8,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

REP_MEASUREMENTS = [1, 6, 12, 18, 24]


def save_pair(fig: plt.Figure, stem: str) -> None:
    fig.savefig(FIG_DIR / f"{stem}.pdf", bbox_inches="tight", pad_inches=0.04)
    fig.savefig(FIG_DIR / f"{stem}.png", bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)


def style_axis(ax, grid_axis: str = "y") -> None:
    ax.grid(axis=grid_axis, color=COL["grid"], linewidth=0.55, alpha=0.95, linestyle=(0, (2, 2)))
    ax.set_axisbelow(True)
    ax.tick_params(length=3, width=0.7, color=COL["ink"], labelcolor=COL["ink"])


def parse_file_name(name: str) -> tuple[int | None, int | None, str]:
    if name.startswith("1-4-EPSC"):
        m = re.search(r"64ci-(\d+)\.csv$", name)
        return 9, int(m.group(1)) if m else None, "repeat"
    m = re.search(r"3-(\d+)-EPSC.*64ci-(\d+)\.csv$", name)
    if m:
        return int(m.group(1)), int(m.group(2)), "wafer"
    return None, None, "excluded"


def load_c1_trace(path: Path) -> tuple[np.ndarray, np.ndarray]:
    df = pd.read_csv(path, usecols=["CH1 Time 1", "CH1 Current 1"])
    t = pd.to_numeric(df["CH1 Time 1"], errors="coerce").to_numpy(dtype=float)
    i = pd.to_numeric(df["CH1 Current 1"], errors="coerce").to_numpy(dtype=float) * 1e9
    mask = np.isfinite(t) & np.isfinite(i)
    t = t[mask]
    i = i[mask]
    order = np.argsort(t)
    return t[order], i[order]


def resolve_csv(name: str) -> Path:
    path = ROOT / name
    if path.exists():
        return path
    if path.suffix != ".csv":
        csv_path = ROOT / f"{name}.csv"
        if csv_path.exists():
            return csv_path
    raise FileNotFoundError(path)


def first_crossing_time(t: np.ndarray, y: np.ndarray, threshold: float) -> float:
    idx = np.flatnonzero(y >= threshold)
    if idx.size == 0:
        return math.nan
    k = int(idx[0])
    if k == 0:
        return float(t[0])
    y0, y1 = float(y[k - 1]), float(y[k])
    t0, t1 = float(t[k - 1]), float(t[k])
    if y1 == y0:
        return t1
    return t0 + (threshold - y0) * (t1 - t0) / (y1 - y0)


def extract_c1_features(path: Path) -> dict[str, float | int | str]:
    t, current = load_c1_trace(path)
    if t.size < 20:
        raise ValueError(f"Too few C1 points: {path}")

    baseline = float(np.mean(current[: min(100, current.size)]))
    signal = baseline - current  # inward EPSC is positive after baseline correction.
    peak_idx = int(np.nanargmax(signal))
    amp = float(signal[peak_idx])
    peak_nA = float(current[peak_idx])
    t_peak = float(t[peak_idx])

    pre_t = t[: peak_idx + 1]
    pre_sig = signal[: peak_idx + 1]
    t10 = first_crossing_time(pre_t, pre_sig, 0.10 * amp)
    t50_rise = first_crossing_time(pre_t, pre_sig, 0.50 * amp)
    t90 = first_crossing_time(pre_t, pre_sig, 0.90 * amp)
    rise_10_90 = float(t90 - t10) if np.isfinite(t10) and np.isfinite(t90) else math.nan

    post_t = t[peak_idx:]
    post_sig = signal[peak_idx:]
    below_1e = np.flatnonzero(post_sig <= amp / math.e)
    tau_1e = float(post_t[int(below_1e[0])] - t_peak) if below_1e.size else math.nan
    below_half = np.flatnonzero(post_sig <= 0.50 * amp)
    t50_decay = float(post_t[int(below_half[0])]) if below_half.size else math.nan
    half_width = float(t50_decay - t50_rise) if np.isfinite(t50_rise) and np.isfinite(t50_decay) else math.nan

    above_10_post = np.flatnonzero(post_sig <= 0.10 * amp)
    end_idx = peak_idx + int(above_10_post[0]) if above_10_post.size else current.size - 1
    start_idx_candidates = np.flatnonzero(signal[: peak_idx + 1] >= 0.10 * amp)
    start_idx = int(start_idx_candidates[0]) if start_idx_candidates.size else 0
    seg_signal = np.clip(signal[start_idx : end_idx + 1], 0.0, None)
    seg_t = t[start_idx : end_idx + 1]
    charge_nC = float(np.trapezoid(seg_signal, seg_t)) if seg_t.size >= 2 else math.nan

    device, measurement, kind = parse_file_name(path.name)
    return {
        "file": path.name,
        "device": device,
        "measurement": measurement,
        "type": kind,
        "C1_baseline_nA_codex": baseline,
        "C1_peak_nA_codex": peak_nA,
        "C1_amp_nA_codex": amp,
        "C1_t_peak_s_codex": t_peak,
        "C1_rise_10_90_s": rise_10_90,
        "C1_tau_1e_decay_s": tau_1e,
        "C1_decay_1e_resolved": bool(np.isfinite(tau_1e)),
        "C1_half_width_s_codex": half_width,
        "C1_charge_nC": charge_nC,
    }


def linear_fit_summary(x: np.ndarray, y: np.ndarray) -> tuple[float, float, float]:
    coeff = np.polyfit(x, y, deg=1)
    slope, intercept = float(coeff[0]), float(coeff[1])
    pred = slope * x + intercept
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else math.nan
    return slope, intercept, r2


def plot_device_consistency(stats: pd.DataFrame) -> None:
    wafer = stats[stats["type"] == "wafer"].copy()
    devices = sorted(wafer["device"].dropna().astype(int).unique())
    data = [wafer.loc[wafer["device"] == d, "C1_amp_nA_codex"].to_numpy() for d in devices]

    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    parts = ax.violinplot(data, positions=np.arange(len(devices)), widths=0.72, showmeans=False, showextrema=False)
    for body in parts["bodies"]:
        body.set_facecolor("#DCEBF7")
        body.set_edgecolor(COL["blue"])
        body.set_alpha(0.70)
        body.set_linewidth(0.8)
    bp = ax.boxplot(data, positions=np.arange(len(devices)), widths=0.34, patch_artist=True, showfliers=False)
    for patch in bp["boxes"]:
        patch.set_facecolor("white")
        patch.set_edgecolor(COL["ink"])
        patch.set_linewidth(0.9)
    for key in ["whiskers", "caps", "medians"]:
        for line in bp[key]:
            line.set_color(COL["ink"])
            line.set_linewidth(0.9)
    rng = np.random.default_rng(7)
    for xpos, values in enumerate(data):
        ax.scatter(xpos + rng.uniform(-0.10, 0.10, len(values)), values, s=34, color=COL["blue"], edgecolor="white", linewidth=0.5, zorder=3)
    ax.set_xticks(np.arange(len(devices)))
    ax.set_xticklabels([f"D{d}" for d in devices])
    ax.set_ylabel("C1 inward peak amplitude (nA)")
    ax.set_title("Wafer-level EPSC device consistency", loc="left")
    style_axis(ax)
    summary = wafer.groupby("device")["C1_amp_nA_codex"].agg(["mean", "std"])
    for xpos, d in enumerate(devices):
        mean = summary.loc[d, "mean"]
        std = summary.loc[d, "std"]
        cv = std / mean * 100 if mean else math.nan
        ax.text(xpos, mean + std + 1.2, f"CV {cv:.1f}%", ha="center", va="bottom", fontsize=8.6, color=COL["muted"], rotation=0)
    save_pair(fig, "epsc_device_consistency")


def plot_repeat_trend(stats: pd.DataFrame) -> tuple[float, float, float]:
    repeat = stats[stats["type"] == "repeat"].sort_values("measurement").copy()
    x = repeat["measurement"].to_numpy(dtype=float)
    y = repeat["C1_amp_nA_codex"].to_numpy(dtype=float)
    slope, intercept, r2 = linear_fit_summary(x, y)

    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.plot(x, y, color=COL["gray"], linewidth=1.15, zorder=1)
    ax.scatter(x, y, s=38, color=COL["blue"], edgecolor="white", linewidth=0.5, zorder=2, label="D9 repeat")
    fit_x = np.array([x.min(), x.max()])
    ax.plot(fit_x, slope * fit_x + intercept, color=COL["orange"], linewidth=1.7, label="linear fit", zorder=3)
    rep = repeat[repeat["measurement"].isin(REP_MEASUREMENTS)]
    ax.scatter(rep["measurement"], rep["C1_amp_nA_codex"], s=92, color=COL["gold"], edgecolor=COL["ink"], linewidth=0.7, zorder=4, label="selected traces")
    for _, row in rep.iterrows():
        ax.text(row["measurement"], row["C1_amp_nA_codex"] + 1.0, f"M{int(row['measurement'])}", ha="center", va="bottom", fontsize=9.2, fontweight="bold")
    mean = float(np.mean(y))
    std = float(np.std(y, ddof=1))
    cv = std / mean * 100
    ax.text(0.02, 0.96, f"mean {mean:.2f} nA\nCV {cv:.1f}%\nslope {slope:+.2f} nA/run\n$R^2$ {r2:.2f}", transform=ax.transAxes, ha="left", va="top", fontsize=10.0, bbox={"boxstyle": "round,pad=0.32", "facecolor": "white", "edgecolor": COL["grid"]})
    ax.set_xlabel("Repeat measurement index")
    ax.set_ylabel("C1 inward peak amplitude (nA)")
    ax.set_title("D9 repeat EPSC stability across 24 measurements", loc="left")
    ax.set_xlim(0.5, 24.5)
    style_axis(ax)
    ax.legend(loc="lower right", frameon=True)
    save_pair(fig, "epsc_d9_repeat_trend")
    return slope, intercept, r2


def plot_representative_waveforms(stats: pd.DataFrame) -> None:
    repeat = stats[(stats["type"] == "repeat") & (stats["measurement"].isin(REP_MEASUREMENTS))].sort_values("measurement")
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    colors = [COL["blue"], COL["green"], COL["orange"], COL["gold"], "#8A63B8"]
    for color, (_, row) in zip(colors, repeat.iterrows()):
        t, current = load_c1_trace(resolve_csv(row["file"]))
        ax.plot(t, current, linewidth=1.25, color=color, label=f"M{int(row['measurement'])}: peak {row['C1_peak_nA_codex']:.1f} nA")
        ax.scatter([row["C1_t_peak_s_codex"]], [row["C1_peak_nA_codex"]], s=32, color=color, edgecolor="white", linewidth=0.5, zorder=3)
    ax.axhline(0, color=COL["grid"], linewidth=0.8)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("C1 current (nA; inward negative)")
    ax.set_title("Representative D9 EPSC waveforms", loc="left")
    style_axis(ax)
    ax.legend(loc="lower right", frameon=True, ncol=1)
    save_pair(fig, "epsc_representative_waveforms")


def plot_feature_and_auxiliary(stats: pd.DataFrame) -> None:
    wafer = stats[stats["type"] == "wafer"].copy()
    devices = sorted(wafer["device"].dropna().astype(int).unique())
    fig, axes = plt.subplots(2, 2, figsize=(9.6, 7.2))
    ax = axes[0, 0]
    charge_data = [wafer.loc[wafer["device"] == d, "C1_charge_nC"].to_numpy() for d in devices]
    ax.boxplot(charge_data, positions=np.arange(len(devices)), widths=0.46, patch_artist=True, showfliers=False, boxprops={"facecolor": "#E7F4EF", "edgecolor": COL["green"]}, medianprops={"color": COL["ink"]})
    ax.set_xticks(np.arange(len(devices)))
    ax.set_xticklabels([f"D{d}" for d in devices])
    ax.set_ylabel("Integrated EPSC charge (nC)")
    ax.set_title("(a) Charge by wafer device", loc="left")
    style_axis(ax)

    ax = axes[0, 1]
    rise_data = [wafer.loc[wafer["device"] == d, "C1_rise_10_90_s"].dropna().to_numpy() for d in devices]
    ax.boxplot(rise_data, positions=np.arange(len(devices)), widths=0.46, patch_artist=True, showfliers=False, boxprops={"facecolor": "#FBEADE", "edgecolor": COL["orange"]}, medianprops={"color": COL["ink"]})
    ax.set_xticks(np.arange(len(devices)))
    ax.set_xticklabels([f"D{d}" for d in devices])
    ax.set_ylabel("10–90% rise time (s)")
    ax.set_title("(b) Rise time by wafer device", loc="left")
    style_axis(ax)

    ax = axes[1, 0]
    for kind, color, marker in [("wafer", COL["blue"], "o"), ("repeat", COL["orange"], "s")]:
        sub = stats[stats["type"] == kind]
        ax.scatter(sub["C1_amp_nA_codex"], -sub["C2_mean_nA"], s=42, color=color, marker=marker, edgecolor="white", linewidth=0.5, label=kind)
    ax.set_xlabel("C1 inward peak amplitude (nA)")
    ax.set_ylabel("-C2 mean current (nA)")
    ax.set_title("(c) C2 holding/reference relation", loc="left")
    style_axis(ax)
    ax.legend(frameon=True)

    ax = axes[1, 1]
    valid_counts = stats.groupby(["type", "C3_valid"]).size().unstack(fill_value=0)
    types = [t for t in ["wafer", "repeat"] if t in valid_counts.index]
    valid = [int(valid_counts.loc[t].get(True, 0)) for t in types]
    invalid = [int(valid_counts.loc[t].get(False, 0)) for t in types]
    x = np.arange(len(types))
    ax.bar(x, valid, color=COL["green"], edgecolor="white", linewidth=0.7, label="C3 valid")
    ax.bar(x, invalid, bottom=valid, color=COL["red"], edgecolor="white", linewidth=0.7, label="C3 short")
    for xpos, v, inv in zip(x, valid, invalid):
        ax.text(xpos, v + inv + 0.7, f"{v}/{v+inv}", ha="center", va="bottom", fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(types)
    ax.set_ylabel("File count")
    ax.set_title("(d) C3 usable segment count", loc="left")
    style_axis(ax)
    ax.legend(frameon=True)

    fig.tight_layout(pad=0.8, w_pad=1.0, h_pad=1.1)
    save_pair(fig, "epsc_feature_auxiliary_summary")


def write_summaries(stats: pd.DataFrame, slope: float, intercept: float, r2: float) -> None:
    stats.to_csv(ROOT / "EPSC_STATS_CODEX.csv", index=False)
    wafer = stats[stats["type"] == "wafer"].copy()
    summary = wafer.groupby("device").agg(
        n=("file", "count"),
        peak_amp_mean_nA=("C1_amp_nA_codex", "mean"),
        peak_amp_std_nA=("C1_amp_nA_codex", "std"),
        charge_mean_nC=("C1_charge_nC", "mean"),
        charge_std_nC=("C1_charge_nC", "std"),
        tau_1e_mean_s=("C1_tau_1e_decay_s", "mean"),
        tau_1e_std_s=("C1_tau_1e_decay_s", "std"),
        decay_1e_resolved_count=("C1_decay_1e_resolved", "sum"),
        rise_10_90_mean_s=("C1_rise_10_90_s", "mean"),
        c2_mean_nA=("C2_mean_nA", "mean"),
        c3_valid_count=("C3_valid", "sum"),
    ).reset_index()
    summary["peak_amp_cv_pct"] = summary["peak_amp_std_nA"] / summary["peak_amp_mean_nA"] * 100
    summary.to_csv(ROOT / "EPSC_DEVICE_SUMMARY_CODEX.csv", index=False)

    repeat = stats[stats["type"] == "repeat"].copy()
    repeat_summary = pd.DataFrame([{
        "n": len(repeat),
        "peak_amp_mean_nA": repeat["C1_amp_nA_codex"].mean(),
        "peak_amp_std_nA": repeat["C1_amp_nA_codex"].std(ddof=1),
        "peak_amp_cv_pct": repeat["C1_amp_nA_codex"].std(ddof=1) / repeat["C1_amp_nA_codex"].mean() * 100,
        "peak_amp_min_nA": repeat["C1_amp_nA_codex"].min(),
        "peak_amp_max_nA": repeat["C1_amp_nA_codex"].max(),
        "trend_slope_nA_per_run": slope,
        "trend_intercept_nA": intercept,
        "trend_r2": r2,
        "c3_valid_count": int(repeat["C3_valid"].sum()),
    }])
    repeat_summary.to_csv(ROOT / "EPSC_D9_REPEAT_SUMMARY_CODEX.csv", index=False)

    best_cv = summary.sort_values("peak_amp_cv_pct").iloc[0]
    worst_cv = summary.sort_values("peak_amp_cv_pct", ascending=False).iloc[0]
    report = f"""# Codex EPSC Analysis Report — 2026-05-03

## Inputs

- Source directory: `compute_vit/数据_博士/`
- Valid EPSC CSV files analyzed: {len(stats)}
- Excluded by brief: `1-4.csv` (non-EPSC IV-like format)
- Main channel: `CH1 Current 1`, converted from A to nA

## Outputs

- `EPSC_STATS_CODEX.csv`: per-file C1/C2/C3 feature table
- `EPSC_DEVICE_SUMMARY_CODEX.csv`: wafer-device aggregate statistics
- `EPSC_D9_REPEAT_SUMMARY_CODEX.csv`: D9 24-repeat trend summary
- `figures/epsc_device_consistency.(pdf|png)`
- `figures/epsc_d9_repeat_trend.(pdf|png)`
- `figures/epsc_representative_waveforms.(pdf|png)`
- `figures/epsc_feature_auxiliary_summary.(pdf|png)`

## Key Findings

1. Wafer-level device consistency is heterogeneous. The most stable wafer device by C1 inward peak amplitude is D{int(best_cv['device'])} with CV={best_cv['peak_amp_cv_pct']:.1f}%; the least stable is D{int(worst_cv['device'])} with CV={worst_cv['peak_amp_cv_pct']:.1f}%.
2. D9 24-repeat stability shows mean inward peak amplitude {repeat_summary.loc[0, 'peak_amp_mean_nA']:.2f} ± {repeat_summary.loc[0, 'peak_amp_std_nA']:.2f} nA, CV={repeat_summary.loc[0, 'peak_amp_cv_pct']:.1f}%.
3. The D9 repeat linear trend slope is {slope:+.3f} nA per repeat with R²={r2:.3f}. This is a weak monotonic descriptor only; the visible run-to-run scatter is larger than the fitted drift trend.
4. C1 does not contain a resolved 1/e decay endpoint for these traces ({int(stats['C1_decay_1e_resolved'].sum())}/{len(stats)} resolved by threshold), so decay constants should not be reported from C1 alone.
5. C3 is useful as an auxiliary segment but not a universal endpoint: {int(stats['C3_valid'].sum())}/{len(stats)} files pass the ≥500-point criterion.

## Feature Definitions

- `C1_amp_nA_codex = baseline - peak`, positive for inward EPSC.
- `C1_rise_10_90_s`: first 10% to first 90% crossing before the C1 peak.
- `C1_tau_1e_decay_s`: time from peak until baseline-corrected signal falls below 1/e of peak amplitude; unresolved traces are left blank.
- `C1_charge_nC`: trapezoidal integral of positive baseline-corrected EPSC signal from 10% rise to post-peak 10% return. Since nA·s = nC, the unit is nC.

## Caveats

- Tau is not claimed as a robust result here because the C1 acquisition window generally ends before a 1/e recovery is reached.
- C3 truncation is preserved as a data-quality flag and is not treated as a parser error.
- The figures use positive inward amplitude for statistical comparisons, while waveform plots retain the physical negative-current convention.
"""
    (ROOT / "CODEX_EPSC_ANALYSIS_REPORT_20260503.md").write_text(report, encoding="utf-8")


def main() -> None:
    ready = pd.read_csv(ROOT / "EPSC_ANALYSIS_READY.csv")
    rows = []
    for _, row in ready.iterrows():
        features = extract_c1_features(resolve_csv(row["file"]))
        merged = {**row.to_dict(), **features}
        rows.append(merged)
    stats = pd.DataFrame(rows).sort_values(["type", "device", "measurement", "file"]).reset_index(drop=True)
    plot_device_consistency(stats)
    slope, intercept, r2 = plot_repeat_trend(stats)
    plot_representative_waveforms(stats)
    plot_feature_and_auxiliary(stats)
    write_summaries(stats, slope, intercept, r2)
    print(ROOT / "EPSC_STATS_CODEX.csv")
    print(ROOT / "CODEX_EPSC_ANALYSIS_REPORT_20260503.md")
    print(FIG_DIR)


if __name__ == "__main__":
    main()
