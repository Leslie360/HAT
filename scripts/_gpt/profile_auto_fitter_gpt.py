#!/usr/bin/env python3
"""Fit measured device profiles from the doctoral raw TXT exports."""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np
from scipy.optimize import curve_fit

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from device_profile_utils import DeviceProfile, dump_device_profiles_json, profile_to_payload


def nl_model(n: np.ndarray, g_min: float, g_max: float, beta: float, n_max: int) -> np.ndarray:
    """Behavioral nonlinearity model shared with the appendix description."""
    if abs(beta) < 1e-6:
        return g_min + (g_max - g_min) * n / max(n_max, 1)
    if beta > 0:
        return g_min + (g_max - g_min) * (1.0 - np.exp(-beta * n / max(n_max, 1))) / (1.0 - np.exp(-beta))
    return g_max - (g_max - g_min) * (1.0 - np.exp(beta * n / max(n_max, 1))) / (1.0 - np.exp(beta))


def retention_ratio_model(t: np.ndarray, a0: float, tau_1: float, tau_2: float) -> np.ndarray:
    a1 = (1.0 - a0) / 2.0
    a2 = a1
    return a1 * np.exp(-t / tau_1) + a2 * np.exp(-t / tau_2) + a0


def power_law_current(x: np.ndarray, i_dark: float, alpha: float, gamma: float) -> np.ndarray:
    return i_dark + alpha * np.power(x, gamma)


def parse_numeric_rows(path: Path) -> np.ndarray:
    rows: List[List[float]] = []
    with path.open("r", encoding="utf-8") as fh:
        for raw in fh:
            line = raw.strip()
            if not line:
                continue
            try:
                rows.append([float(token) for token in line.split("\t")])
            except ValueError:
                continue
    if not rows:
        raise ValueError(f"No numeric rows found in {path}")
    return np.asarray(rows, dtype=float)


def load_xy_pairs(path: Path) -> List[Tuple[np.ndarray, np.ndarray]]:
    arr = parse_numeric_rows(path)
    if arr.ndim != 2 or arr.shape[1] % 2 != 0:
        raise ValueError(f"Expected even number of columns in {path}, got shape {arr.shape}")
    pairs: List[Tuple[np.ndarray, np.ndarray]] = []
    for idx in range(0, arr.shape[1], 2):
        x = arr[:, idx]
        y = arr[:, idx + 1]
        mask = np.isfinite(x) & np.isfinite(y)
        pairs.append((x[mask], y[mask]))
    return pairs


def load_sparse_columns(path: Path) -> List[List[float]]:
    rows = [line.rstrip("\n").split("\t") for line in path.read_text(encoding="utf-8").splitlines()]
    max_cols = max(len(row) for row in rows)
    columns: List[List[float]] = [[] for _ in range(max_cols)]
    for row in rows:
        for idx in range(max_cols):
            token = row[idx].strip() if idx < len(row) else ""
            if not token:
                continue
            try:
                columns[idx].append(float(token))
            except ValueError:
                continue
    return columns


def moving_average(values: np.ndarray, window: int) -> np.ndarray:
    window = max(3, int(window))
    if window % 2 == 0:
        window += 1
    pad = window // 2
    padded = np.pad(values, pad_width=pad, mode="edge")
    kernel = np.ones(window, dtype=float) / float(window)
    return np.convolve(padded, kernel, mode="valid")


def robust_sigma(values: np.ndarray) -> float:
    centered = values - np.median(values)
    return float(1.4826 * np.median(np.abs(centered)))


def make_strictly_increasing(values: Sequence[float]) -> List[float]:
    fixed: List[float] = []
    eps = 1e-15
    for value in values:
        current = float(value)
        if fixed and current <= fixed[-1]:
            current = fixed[-1] + eps
        fixed.append(current)
    return fixed


def extract_state_ladder(trace_path: Path, n_states: int) -> Tuple[List[float], Dict[str, float]]:
    trace = parse_numeric_rows(trace_path)
    y = trace[:, 1]
    dy = np.abs(np.diff(y, prepend=y[0]))
    med = float(np.median(dy[1:])) if len(dy) > 1 else float(np.median(dy))
    threshold = max(med * 10.0, 1e-18)
    stable = y[dy <= threshold]
    if stable.size < n_states * 4:
        stable = y[np.isfinite(y)]
    stable = np.sort(stable)
    chunks = np.array_split(stable, n_states)
    ladder = make_strictly_increasing(float(np.median(chunk)) for chunk in chunks if chunk.size)
    if len(ladder) != n_states:
        raise ValueError(f"Expected {n_states} states from {trace_path}, got {len(ladder)}")
    diagnostics = {
        "stable_points": int(stable.size),
        "stable_threshold": threshold,
        "raw_points": int(y.size),
        "raw_min": float(np.min(y)),
        "raw_max": float(np.max(y)),
        "ladder_min": float(ladder[0]),
        "ladder_max": float(ladder[-1]),
    }
    return ladder, diagnostics


def fit_beta_from_ladder(ladder: Sequence[float]) -> float:
    ladder_arr = np.asarray(ladder, dtype=float)
    pulses = np.arange(ladder_arr.size, dtype=float)
    g_min = float(ladder_arr[0])
    g_max = float(ladder_arr[-1])
    n_max = max(int(ladder_arr.size) - 1, 1)
    try:
        popt, _ = curve_fit(
            lambda n, beta: nl_model(n, g_min, g_max, beta, n_max),
            pulses,
            ladder_arr,
            p0=[1.0],
            bounds=([-20.0], [20.0]),
            maxfev=20000,
        )
        return float(popt[0])
    except Exception:
        return 1.0


def estimate_programming_noise(program_trace_path: Path, g_range: float) -> float:
    trace = parse_numeric_rows(program_trace_path)
    y = trace[:, 1]
    smooth = moving_average(y, window=max(9, len(y) // 25))
    residual = y - smooth
    return robust_sigma(residual) / max(g_range, 1e-30)


def fit_retention_and_repeatability(retention_path: Path, g_range: float) -> Tuple[float, float, float, float, Dict[str, float]]:
    pairs = load_xy_pairs(retention_path)
    if len(pairs) < 2:
        raise ValueError(f"Expected duplicated retention traces in {retention_path}")
    half = len(pairs) // 2
    times: List[np.ndarray] = []
    ratios: List[np.ndarray] = []
    sigma_repeats: List[float] = []
    decay_pairs = 0

    for idx in range(half):
        x1, y1 = pairs[idx]
        x2, y2 = pairs[idx + half]
        left = max(float(np.min(x1)), float(np.min(x2)))
        right = min(float(np.max(x1)), float(np.max(x2)))
        if right <= left:
            continue
        samples = int(min(len(x1), len(x2), 512))
        grid = np.linspace(left, right, num=max(samples, 64), dtype=float)
        y1i = np.interp(grid, x1, y1)
        y2i = np.interp(grid, x2, y2)
        mean_curve = 0.5 * (y1i + y2i)
        sigma_repeats.append(float(np.std(y1i - y2i) / math.sqrt(2.0)))
        if mean_curve[-1] <= mean_curve[0] * 1.01:
            ratio = np.clip(mean_curve / max(float(mean_curve[0]), 1e-30), 0.0, 1.2)
            times.append(grid)
            ratios.append(ratio)
            decay_pairs += 1

    if decay_pairs >= 1:
        t_all = np.concatenate(times)
        r_all = np.concatenate(ratios)
        tau_short_init = max(float(np.quantile(t_all, 0.1)), 1.0)
        tau_long_init = max(float(np.quantile(t_all, 0.8)), tau_short_init * 10.0)
        try:
            popt, _ = curve_fit(
                retention_ratio_model,
                t_all,
                r_all,
                p0=[0.97, tau_short_init, tau_long_init],
                bounds=([0.85, 1e-3, 1e-2], [1.0, max(t_all) * 100.0, max(t_all) * 1e6]),
                maxfev=200000,
            )
            a0, tau_1, tau_2 = map(float, popt)
        except Exception:
            a0, tau_1, tau_2 = 0.97, tau_short_init, tau_long_init
    else:
        a0, tau_1, tau_2 = 0.99, 10.0, 1e6
        t_all = np.asarray([0.0, 1.0], dtype=float)

    if tau_1 > tau_2:
        tau_1, tau_2 = tau_2, tau_1

    sigma_c2c_repeat = float(np.mean(sigma_repeats)) / max(g_range, 1e-30)
    diagnostics = {
        "duplicate_pairs": int(half),
        "retention_points": int(t_all.size),
        "decay_pairs_used": int(decay_pairs),
        "sigma_c2c_repeat_only": sigma_c2c_repeat,
        "retention_time_min": float(np.min(t_all)),
        "retention_time_max": float(np.max(t_all)),
    }
    return a0, tau_1, tau_2, sigma_c2c_repeat, diagnostics


def fit_photoresponse(photo_path: Path) -> Tuple[float, float, float, Dict[str, float]]:
    arr = parse_numeric_rows(photo_path)
    x = arr[:, 0]
    y = arr[:, 1]
    best = None
    for frac in np.linspace(0.0, 0.7, 15):
        i_dark = float(np.min(y) * frac)
        shifted = y - i_dark
        if np.any(shifted <= 0.0):
            continue
        slope, intercept = np.polyfit(np.log(x), np.log(shifted), deg=1)
        alpha = float(np.exp(intercept))
        gamma = float(slope)
        pred = power_law_current(x, i_dark, alpha, gamma)
        ss_res = float(np.sum((y - pred) ** 2))
        ss_tot = float(np.sum((y - np.mean(y)) ** 2))
        r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
        candidate = (r2, i_dark, alpha, gamma)
        if best is None or candidate[0] > best[0]:
            best = candidate
    if best is None:
        slope, intercept = np.polyfit(np.log(x), np.log(y), deg=1)
        i_dark, alpha, gamma = 0.0, float(np.exp(intercept)), float(slope)
    else:
        _, i_dark, alpha, gamma = best
    pred = power_law_current(x, i_dark, alpha, gamma)
    ss_res = float(np.sum((y - pred) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    diagnostics = {
        "photo_points": int(len(x)),
        "photo_x_min": float(np.min(x)),
        "photo_x_max": float(np.max(x)),
        "photo_r2": r2,
    }
    return i_dark, alpha, gamma, diagnostics


def summarize_auxiliary_inputs(data_root: Path) -> Dict[str, dict]:
    third_g = load_xy_pairs(data_root / "第三页/g/图.txt")
    third_h = parse_numeric_rows(data_root / "第三页/h/100sID.txt")
    third_b = load_xy_pairs(data_root / "第三页/b/5-20paule.txt")
    third_c = load_xy_pairs(data_root / "第三页/c/300-800.txt")
    ppf_path = data_root / "第三页/a/小图.txt"
    ppf_raw_path = data_root / "第三页/a/小图_raw_ppf_points.txt"
    ppf_override_path = ROOT / "report_md/_gpt/json_gpt/doctor_ppf_inset_points.json"
    ppf_summary = {
        "available": False,
        "source": str(ppf_path),
    }
    if ppf_raw_path.exists():
        raw_rows = parse_numeric_rows(ppf_raw_path)
        ppf_summary = {
            "available": True,
            "source": str(ppf_raw_path),
            "format": "manual_raw_file",
            "delta_t_raw": [float(v) for v in raw_rows[:, 0]],
            "ppf_percent": [float(v) for v in raw_rows[:, 1]],
            "ppf_ratio": [float(v / 100.0) for v in raw_rows[:, 1]],
            "note": "Direct raw PPF points written alongside the original panel-a exports.",
        }
    elif ppf_override_path.exists():
        payload = json.loads(ppf_override_path.read_text(encoding="utf-8"))
        delta_t = [float(v) for v in payload["delta_t_raw"]]
        ppf_percent = [float(v) for v in payload["ppf_percent"]]
        ppf_summary = {
            "available": True,
            "source": str(ppf_override_path),
            "format": "manual_raw_override",
            "delta_t_raw": delta_t,
            "ppf_percent": ppf_percent,
            "ppf_ratio": [float(v / 100.0) for v in ppf_percent],
            "note": "Direct raw PPF points supplied manually after inspecting the inset source.",
        }
    if ppf_path.exists():
        cols = load_sparse_columns(ppf_path)
        # The supplied file is an Origin nonlinear-fit report sheet (`ExpDec1 fit of G`),
        # not the original PPF raw-point table. Preserve the fitted/diagnostic columns as
        # auxiliary evidence without overclaiming them as source measurements.
        if len(cols) >= 11:
            fit_report = {
                "available": True,
                "source": str(ppf_path),
                "format": "origin_fit_report",
                "fit_model": "ExpDec1 fit of G",
                "note": "Fit-report export, not the original raw PPF scatter table.",
                "fit_curve_x": cols[0],
                "fit_curve_y": cols[1],
                "residual_vs_x_x": cols[2],
                "residual_vs_x_residual": cols[3],
                "residual_hist_axis": cols[4],
                "fitted_y": cols[5],
                "residual_vs_fitted_residual": cols[6],
                "normal_prob_residual": cols[7],
                "normal_prob_percentile": cols[8],
                "normal_prob_reference_x": cols[9],
                "normal_prob_reference_line": cols[10],
                "reported_residual_mu": 0.0,
                "reported_residual_sigma": 0.011664,
            }
            if ppf_summary.get("available"):
                ppf_summary["fit_report"] = fit_report
            else:
                ppf_summary = fit_report
    return {
        "ppf_inset": ppf_summary,
        "volatile_rc_sequences": {
            "curve_count": len(third_g),
            "time_span": [float(min(np.min(x) for x, _ in third_g)), float(max(np.max(x) for x, _ in third_g))],
            "current_span": [float(min(np.min(y) for _, y in third_g)), float(max(np.max(y) for _, y in third_g))],
        },
        "volatile_rc_states_at_100s": {
            "n_states": int(third_h.shape[0]),
            "current_min": float(np.min(third_h[:, 1])),
            "current_max": float(np.max(third_h[:, 1])),
        },
        "volatile_epsc_pulse_count": {
            "curve_count": len(third_b),
        },
        "volatile_epsc_pulse_width": {
            "curve_count": len(third_c),
        },
    }


def build_profiles(data_root: Path) -> Tuple[List[DeviceProfile], Dict[str, dict]]:
    fourth_d = data_root / "第四页/d/256次线性作图.txt"
    fourth_e = data_root / "第四页/e/s0-s5.txt"
    fourth_i = data_root / "第四页/i/pot.txt"
    page20_16 = data_root / "第20页/16.txt"
    page20_64 = data_root / "第20页/64.txt"

    i_dark, alpha, gamma, photo_diag = fit_photoresponse(fourth_i)
    aux_diag = summarize_auxiliary_inputs(data_root)
    source_note = "Doctoral PPT raw TXT export (pages 3, 4, 20)"
    profiles: List[DeviceProfile] = []
    diagnostics: Dict[str, dict] = {
        "source_note": source_note,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "photoresponse": photo_diag,
        "auxiliary_inputs": aux_diag,
        "input_manifest": [
            {
                "path": "第20页/16.txt",
                "status": "used",
                "role": "Extracted stable conductance ladder for RC-16 and emitted as inl_table.",
            },
            {
                "path": "第20页/64.txt",
                "status": "used",
                "role": "Extracted stable conductance ladder for RC-64 and emitted as inl_table.",
            },
            {
                "path": "第四页/d/256次线性作图.txt",
                "status": "used",
                "role": "Used for programming residual noise estimation and pulse_count_max prior.",
            },
            {
                "path": "第四页/e/s0-s5.txt",
                "status": "used",
                "role": "Used for retention fitting and duplicate-trace repeatability estimation.",
            },
            {
                "path": "第四页/i/pot.txt",
                "status": "used",
                "role": "Used for photoresponse fitting: gamma_phys, I_dark, responsivity_alpha.",
            },
            {
                "path": "第三页/a/小图_raw_ppf_points.txt",
                "status": "archived_only",
                "role": "Raw PPF inset points archived as evidence.",
                "note": "Not injected into the nonvolatile DeviceProfile schema because no short-term facilitation field exists yet.",
            },
            {
                "path": "第三页/a/小图.txt",
                "status": "archived_only",
                "role": "Origin ExpDec1 fit report retained as diagnostics for the same PPF inset.",
            },
            {
                "path": "第三页/a/大图.txt",
                "status": "archived_only",
                "role": "Context-only panel export retained for traceability.",
            },
            {
                "path": "第三页/b/5-20paule.txt",
                "status": "archived_only",
                "role": "Pulse-count EPSC curves summarized as auxiliary volatile evidence.",
            },
            {
                "path": "第三页/c/300-800.txt",
                "status": "archived_only",
                "role": "Pulse-width EPSC curves summarized as auxiliary volatile evidence.",
            },
            {
                "path": "第三页/g/图.txt",
                "status": "archived_only",
                "role": "Volatile RC sequences summarized as auxiliary evidence.",
            },
            {
                "path": "第三页/h/100sID.txt",
                "status": "archived_only",
                "role": "100 s volatile RC state readout summarized as auxiliary evidence.",
            },
            {
                "path": "第四页/l/pot.txt",
                "status": "unresolved",
                "role": "Panel (l)/(m) support data retained but not mapped into the JSON fit.",
                "note": "The semantic mapping to the current nonvolatile profile schema is still ambiguous.",
            },
        ],
        "profiles": {},
        "limitations": {
            "ppf_inset_usage": "Third-page panel (a) inset now has direct raw PPF points plus the Origin fit-report export; neither is injected into the current nonvolatile weight-storage JSON because the schema has no short-term facilitation field.",
            "d2d_missing": "No explicit multi-device conductance distribution was present in the PPT export, so sigma_d2d is left at 0.0 rather than fabricated.",
            "static_condition_panel_m_uncertain": "Fourth-page panel (m) was image-only; panel (l) data were not injected into the JSON fit.",
        },
    }

    for state_count, ladder_path in ((16, page20_16), (64, page20_64)):
        ladder, ladder_diag = extract_state_ladder(ladder_path, state_count)
        g_min = float(ladder[0])
        g_max = float(ladder[-1])
        g_range = g_max - g_min
        beta = fit_beta_from_ladder(ladder)
        prog_sigma = estimate_programming_noise(fourth_d, g_range)
        a0, tau_1, tau_2, sigma_repeat, retention_diag = fit_retention_and_repeatability(fourth_e, g_range)
        sigma_c2c = max(prog_sigma, sigma_repeat)

        profile = DeviceProfile(
            device_type=f"Doctor OECT Nonvolatile RC-{state_count}",
            dynamic_range=g_max / g_min,
            n_states=state_count,
            sigma_c2c=float(sigma_c2c),
            sigma_d2d=0.0,
            source=source_note,
            noise_mode="uniform",
            G_min=g_min,
            tau_1=float(tau_1),
            tau_2=float(tau_2),
            A_0=float(a0),
            gamma_phys=float(gamma),
            I_dark=float(i_dark),
            responsivity_alpha=float(alpha),
            NL_LTP=float(beta),
            NL_LTD=-float(beta),
            pulse_count_max=262,
            inl_table=[float(v) for v in ladder],
            profile_kind="measured",
            notes=(
                f"State ladder extracted from 第20页/{state_count}.txt; photoresponse from 第四页/i/pot.txt; "
                f"retention and repeatability from 第四页/e/s0-s5.txt; programming residuals from 第四页/d/256次线性作图.txt. "
                "sigma_d2d left at 0.0 because no explicit multi-device mismatch trace was present in the provided raw export."
            ),
        )
        profiles.append(profile)
        diagnostics["profiles"][profile.device_type] = {
            "g_min": g_min,
            "g_max": g_max,
            "dynamic_range": g_max / g_min,
            "sigma_c2c_programming_residual": prog_sigma,
            "sigma_c2c_repeat_only": sigma_repeat,
            "sigma_c2c_selected": sigma_c2c,
            "sigma_d2d_selected": 0.0,
            "beta_from_ladder": beta,
            "pulse_count_max": 262,
            "ladder_preview": ladder[:6] + ladder[-6:],
            "ladder_diagnostics": ladder_diag,
            "retention_diagnostics": retention_diag,
        }

    return profiles, diagnostics


def write_audit_markdown(path: Path, profiles: Sequence[DeviceProfile], diagnostics: Dict[str, dict], output_json: str) -> None:
    lines = [
        "# Doctor Measured Profile Audit",
        "",
        f"- Generated: `{diagnostics['generated_at']}`",
        f"- Source root: `{diagnostics['source_note']}`",
        f"- Output JSON: `{output_json}`",
        "",
        "## Fitted Profiles",
        "",
        "| Profile | G_min | G_max | Range | n_states | sigma_c2c | sigma_d2d | tau_1 | tau_2 | A_0 | gamma |",
        "|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|",
    ]
    for profile in profiles:
        lines.append(
            f"| {profile.device_type} | {profile.G_min:.3e} | {profile.G_max:.3e} | "
            f"{profile.dynamic_range:.2f} | {profile.n_states} | {profile.sigma_c2c:.4f} | "
            f"{profile.sigma_d2d:.4f} | {profile.tau_1:.3f} | {profile.tau_2:.3f} | "
            f"{profile.A_0:.3f} | {profile.gamma_phys:.3f} |"
        )
    lines.extend([
        "",
        "## Raw-data Mapping",
        "",
        "- `第20页/16.txt`, `第20页/64.txt`: extracted stable readout ladders and emitted as `inl_table`.",
        "- `第四页/d/256次线性作图.txt`: used for programming residual noise and `pulse_count_max=262`.",
        "- `第四页/e/s0-s5.txt`: used for duplicate-trace repeatability and retention fitting.",
        "- `第四页/i/pot.txt`: used to fit `I_dark`, `responsivity_alpha`, and `gamma_phys`.",
        "- `第三页/a/小图.txt`: retained as the auxiliary `Origin ExpDec1 fit of G` diagnostic sheet for panel `(a)`.",
        "- `第三页/a/小图_raw_ppf_points.txt`: direct raw `PPF index vs ΔT` points supplied manually after inspecting the inset source.",
        "- `第三页/g/图.txt`, `第三页/h/100sID.txt`, `第三页/b/5-20paule.txt`, `第三页/c/300-800.txt`: parsed and summarized as auxiliary volatile/RC evidence, but not injected into the nonvolatile weight-storage profile.",
        "",
        "## Limitations",
        "",
        "- `sigma_d2d` is set to `0.0` because no explicit multi-device mismatch distribution was present in the supplied PPT raw export.",
        "- Third-page panel `(a)` inset now has both raw points and fit diagnostics archived, but the current nonvolatile profile schema still has no direct short-term facilitation / PPF field.",
        "- Fourth-page panel `(m)` was image-only; the available `(l)` raw file was not forced into the JSON profile without a clean mapping.",
        "",
        "## Photoresponse Fit",
        "",
        f"- points: `{diagnostics['photoresponse']['photo_points']}`",
        f"- R^2: `{diagnostics['photoresponse']['photo_r2']:.4f}`",
        "",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_demo() -> Tuple[List[DeviceProfile], Dict[str, dict]]:
    np.random.seed(42)
    g_min_gt = 1.0
    g_max_gt = 47.3
    n_states_gt = 34
    sigma_c2c_gt = 0.02
    tau_1_gt = 0.14
    tau_2_gt = 0.61
    a0_gt = 0.6
    beta_gt = 1.5
    pulses = np.arange(n_states_gt, dtype=float)
    ladder = nl_model(pulses, g_min_gt, g_max_gt, beta_gt, n_states_gt - 1)
    ladder += np.random.normal(0.0, 0.05 * sigma_c2c_gt * (g_max_gt - g_min_gt), size=ladder.shape)
    ladder = make_strictly_increasing(np.sort(ladder))
    profile = DeviceProfile(
        device_type="Demo_AutoFitted",
        dynamic_range=ladder[-1] / ladder[0],
        n_states=n_states_gt,
        sigma_c2c=sigma_c2c_gt,
        sigma_d2d=0.0,
        source="Auto-fitted Demo",
        G_min=ladder[0],
        tau_1=tau_1_gt,
        tau_2=tau_2_gt,
        A_0=a0_gt,
        NL_LTP=fit_beta_from_ladder(ladder),
        NL_LTD=-fit_beta_from_ladder(ladder),
        pulse_count_max=n_states_gt - 1,
        inl_table=ladder,
        profile_kind="measured",
        notes="Synthetic round-trip demo profile.",
    )
    diagnostics = {"generated_at": datetime.now().isoformat(timespec="seconds"), "profiles": {profile.device_type: asdict(profile)}}
    return [profile], diagnostics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Measured-device profile auto-fitter.")
    parser.add_argument("--demo", action="store_true", help="Run the synthetic demo instead of fitting the doctoral raw export.")
    parser.add_argument("--doctor-data-root", type=str, default=str(ROOT / "数据_博士"))
    parser.add_argument("--output", type=str, default=str(ROOT / "report_md/_gpt/json_gpt/doctor_measured_profiles.json"))
    parser.add_argument("--audit-json", type=str, default=str(ROOT / "report_md/_gpt/json_gpt/doctor_measured_profile_summary.json"))
    parser.add_argument("--audit-md", type=str, default=str(ROOT / "report_md/_gpt/DOCTOR_MEASURED_PROFILE_AUDIT_20260416.md"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.demo:
        profiles, diagnostics = run_demo()
    else:
        profiles, diagnostics = build_profiles(Path(args.doctor_data_root))

    output_path = dump_device_profiles_json(args.output, profiles, diagnostics.get("source_note", "demo"))
    audit_json_path = Path(args.audit_json)
    audit_json_path.parent.mkdir(parents=True, exist_ok=True)
    audit_json_path.write_text(
        json.dumps(
            {
                "generated_at": diagnostics.get("generated_at"),
                "source": diagnostics.get("source_note", "demo"),
                "profiles": [profile_to_payload(profile) for profile in profiles],
                "diagnostics": diagnostics,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    write_audit_markdown(Path(args.audit_md), profiles, diagnostics, output_path)
    print(f"Wrote {len(profiles)} profiles -> {output_path}")
    print(f"Wrote audit JSON -> {args.audit_json}")
    print(f"Wrote audit markdown -> {args.audit_md}")


if __name__ == "__main__":
    main()
