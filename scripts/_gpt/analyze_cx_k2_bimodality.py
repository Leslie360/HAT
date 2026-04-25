#!/usr/bin/env python3
"""CX-K2 bimodality analysis for the J1d N=30 fresh-instance distribution.

Inputs the existing cx_k2_fresh_eval.json and writes a compact JSON + markdown
with Hartigan dip, Silverman-style bootstrap, and Gaussian-mixture diagnostics.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from statistics import mean, median, stdev

import numpy as np
from scipy.signal import find_peaks
from sklearn.mixture import GaussianMixture

try:
    import diptest
except ImportError:  # pragma: no cover
    diptest = None


def kde_density(x: np.ndarray, grid: np.ndarray, h: float) -> np.ndarray:
    z = (grid[:, None] - x[None, :]) / h
    dens = np.exp(-0.5 * z * z).sum(axis=1) / (len(x) * h * math.sqrt(2.0 * math.pi))
    return dens


def count_modes(x: np.ndarray, h: float, grid: np.ndarray) -> int:
    dens = kde_density(x, grid, h)
    # Small prominence avoids counting numerical ripples as modes.
    prom = max(float(dens.max()) * 1e-3, 1e-12)
    peaks, _ = find_peaks(dens, prominence=prom)
    return int(len(peaks))


def critical_bandwidth(x: np.ndarray, max_modes: int = 1) -> float:
    x = np.asarray(x, dtype=float)
    if len(x) < 3:
        return 0.0
    sd = float(np.std(x, ddof=1))
    lo = max(sd * 1e-4, 1e-6)
    hi = max(sd * 2.5, 1.0)
    pad = max(sd, 1.0) * 1.5
    grid = np.linspace(float(x.min() - pad), float(x.max() + pad), 1024)
    while count_modes(x, hi, grid) > max_modes:
        hi *= 2.0
    for _ in range(36):
        mid = (lo + hi) / 2.0
        if count_modes(x, mid, grid) <= max_modes:
            hi = mid
        else:
            lo = mid
    return float(hi)


def silverman_bootstrap_pvalue(x: np.ndarray, h_obs: float, n_boot: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    x = np.asarray(x, dtype=float)
    n = len(x)
    sd = float(np.std(x, ddof=1))
    boot_h = []
    # Silverman-style null sampling from the critical KDE, variance corrected.
    # This approximates the H0 density with at most one mode.
    denom = math.sqrt(1.0 + (h_obs * h_obs) / (sd * sd)) if sd > 0 else 1.0
    centered = x - float(np.mean(x))
    for _ in range(n_boot):
        base = rng.choice(centered, size=n, replace=True)
        noise = rng.normal(0.0, h_obs, size=n)
        sample = (base + noise) / denom + float(np.mean(x))
        boot_h.append(critical_bandwidth(sample, max_modes=1))
    boot_h_arr = np.asarray(boot_h, dtype=float)
    p = float(np.mean(boot_h_arr >= h_obs))
    return {
        "p_value_ge_observed": p,
        "n_boot": int(n_boot),
        "bootstrap_hcrit_mean": float(np.mean(boot_h_arr)),
        "bootstrap_hcrit_std": float(np.std(boot_h_arr, ddof=1)),
        "bootstrap_hcrit_q05": float(np.quantile(boot_h_arr, 0.05)),
        "bootstrap_hcrit_q50": float(np.quantile(boot_h_arr, 0.50)),
        "bootstrap_hcrit_q95": float(np.quantile(boot_h_arr, 0.95)),
    }


def gmm_diagnostics(x: np.ndarray, seed: int) -> list[dict]:
    rows = []
    X = x.reshape(-1, 1)
    for k in [1, 2, 3]:
        gmm = GaussianMixture(n_components=k, covariance_type="full", random_state=seed, n_init=20)
        gmm.fit(X)
        rows.append({
            "components": k,
            "bic": float(gmm.bic(X)),
            "aic": float(gmm.aic(X)),
            "weights": [float(v) for v in gmm.weights_],
            "means": [float(v) for v in gmm.means_.ravel()],
            "stds": [float(math.sqrt(v)) for v in gmm.covariances_.reshape(-1)],
        })
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="report_md/_gpt/json_gpt/cx_k2_fresh_eval.json")
    ap.add_argument("--json-out", default="report_md/_gpt/json_gpt/cx_k2_bimodality_test.json")
    ap.add_argument("--md-out", default="report_md/_gpt/CODEX_CX_K2_BIMODALITY_TEST_20260423.md")
    ap.add_argument("--silverman-boot", type=int, default=500)
    ap.add_argument("--seed", type=int, default=20260423)
    args = ap.parse_args()

    payload = json.loads(Path(args.input).read_text())
    x = np.asarray(payload["instance_means"], dtype=float)
    zones = {
        "lt_35": int(np.sum(x < 35.0)),
        "between_35_50_inclusive": int(np.sum((x >= 35.0) & (x <= 50.0))),
        "gt_50": int(np.sum(x > 50.0)),
    }

    dip_result = None
    if diptest is not None:
        dip_stat, dip_p = diptest.diptest(x, boot_pval=True, n_boot=10000, seed=args.seed)
        dip_result = {
            "package": "diptest",
            "package_version": getattr(diptest, "__version__", "unknown"),
            "statistic": float(dip_stat),
            "p_value": float(dip_p),
            "n_boot": 10000,
            "null": "unimodal distribution",
            "alternative": "multimodal distribution",
        }

    h_obs = critical_bandwidth(x, max_modes=1)
    silver = silverman_bootstrap_pvalue(x, h_obs=h_obs, n_boot=args.silverman_boot, seed=args.seed)
    silver["observed_hcrit_unimodal"] = float(h_obs)
    silver["null"] = "at most one mode, approximated by critical-bandwidth KDE bootstrap"

    gmm = gmm_diagnostics(x, seed=args.seed)
    best_bic = min(gmm, key=lambda r: r["bic"])
    best_aic = min(gmm, key=lambda r: r["aic"])

    decision_parts = []
    if dip_result is None:
        decision_parts.append("Hartigan unavailable")
    elif dip_result["p_value"] < 0.05:
        decision_parts.append("Hartigan rejects unimodality")
    else:
        decision_parts.append("Hartigan does not reject unimodality")
    if silver["p_value_ge_observed"] < 0.05:
        decision_parts.append("Silverman-style bootstrap rejects unimodality")
    else:
        decision_parts.append("Silverman-style bootstrap does not reject unimodality")

    result = {
        "input": args.input,
        "n": int(len(x)),
        "mean": float(mean(x)),
        "std": float(stdev(x)),
        "median": float(median(x)),
        "min": float(np.min(x)),
        "max": float(np.max(x)),
        "zones": zones,
        "sorted_instance_means": [float(v) for v in sorted(x)],
        "hartigan_dip": dip_result,
        "silverman_unimodality": silver,
        "gmm": {
            "rows": gmm,
            "best_bic_components": int(best_bic["components"]),
            "best_aic_components": int(best_aic["components"]),
            "bic_delta_1_minus_2": float(gmm[0]["bic"] - gmm[1]["bic"]),
            "aic_delta_1_minus_2": float(gmm[0]["aic"] - gmm[1]["aic"]),
        },
        "decision_summary": "; ".join(decision_parts),
        "slim_decision": "confirmed" if (dip_result and dip_result["p_value"] < 0.05) or silver["p_value_ge_observed"] < 0.05 else "not_confirmed_by_tests",
    }

    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(result, indent=2), encoding="utf-8")

    dip_line = "Hartigan dip unavailable"
    if dip_result:
        dip_line = f"Hartigan dip statistic `{dip_result['statistic']:.6f}`, bootstrap p `{dip_result['p_value']:.4f}`"
    md = f"""# CODEX CX-K2 — Bimodality Test on J1d N=30
**Date:** 2026-04-23  
**Executor:** Codex  
**Input:** `{args.input}`  
**Status:** {'BIMODALITY CONFIRMED BY p<0.05 TEST' if result['slim_decision'] == 'confirmed' else 'BIMODALITY NOT CONFIRMED BY p<0.05 TESTS'}

## Distribution

| Metric | Value |
|:--|--:|
| N | `{result['n']}` |
| Mean | `{result['mean']:.4f}%` |
| Std | `{result['std']:.4f}%` |
| Median | `{result['median']:.4f}%` |
| Range | `{result['min']:.3f}% - {result['max']:.3f}%` |
| `<35%` | `{zones['lt_35']}` |
| `35-50%` | `{zones['between_35_50_inclusive']}` |
| `>50%` | `{zones['gt_50']}` |

Sorted instance means:

```text
{', '.join(f'{v:.3f}' for v in result['sorted_instance_means'])}
```

## Hartigan Dip Test

- {dip_line}
- Null: unimodal distribution.
- Alternative: multimodal distribution.

## Silverman-Style Unimodality Bootstrap

- Observed critical bandwidth for <=1 mode: `{h_obs:.6f}`.
- Bootstrap p (`hcrit_boot >= hcrit_observed`): `{silver['p_value_ge_observed']:.4f}` with `{silver['n_boot']}` bootstrap samples.
- Bootstrap hcrit mean/std: `{silver['bootstrap_hcrit_mean']:.6f} / {silver['bootstrap_hcrit_std']:.6f}`.
- Bootstrap hcrit q05/q50/q95: `{silver['bootstrap_hcrit_q05']:.6f} / {silver['bootstrap_hcrit_q50']:.6f} / {silver['bootstrap_hcrit_q95']:.6f}`.

This is a reproducible Silverman-style approximation, not a package-certified implementation. It is used as the sanity check requested by SLIM.

## Gaussian Mixture Diagnostic

| Components | BIC | AIC | Means | Weights | Stds |
|:--:|--:|--:|:--|:--|:--|
"""
    for row in gmm:
        md += (
            f"| {row['components']} | {row['bic']:.3f} | {row['aic']:.3f} | "
            f"{[round(v, 3) for v in row['means']]} | "
            f"{[round(v, 3) for v in row['weights']]} | "
            f"{[round(v, 3) for v in row['stds']]} |\n"
        )
    md += f"""

- Best BIC component count: `{result['gmm']['best_bic_components']}`.
- Best AIC component count: `{result['gmm']['best_aic_components']}`.
- BIC delta `(1-comp - 2-comp)`: `{result['gmm']['bic_delta_1_minus_2']:.3f}`. Positive favors 2 components.
- AIC delta `(1-comp - 2-comp)`: `{result['gmm']['aic_delta_1_minus_2']:.3f}`. Positive favors 2 components.

## SLIM Decision

`{result['decision_summary']}`.

**Decision:** `{result['slim_decision']}`.

Operationally, this means the existing N=30 distribution still supports a broad / basin-sensitive severe-NL story, but the formal p<0.05 bimodality gate should be interpreted exactly as shown above rather than rhetorically assumed.

## Output Files

- JSON: `{args.json_out}`
- Markdown: `{args.md_out}`
"""
    Path(args.md_out).write_text(md, encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
