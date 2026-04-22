#!/usr/bin/env python3
"""Monitor Kimi ablation outputs and write non-GPU follow-up reports.

This script does not launch training or touch CUDA. It only polls expected JSON
outputs from already running experiments.
"""

from __future__ import annotations

import json
import time
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "report_md" / "_gpt"
SYNC_DIR = ROOT / "AGENT_SYNC"
LOG_PATH = SYNC_DIR / "kimi_training_monitor_20260415.log"
KP_FIX_2_PATH = SYNC_DIR / "kp_fix_2_ensemble_data_unification_codex.md"
SPATIAL_NOTE_PATH = SYNC_DIR / "spatial_ablation_quarantine_20260415.md"

ENSEMBLE_JSON = REPORT_DIR / "ensemble_frequency_ablation.json"
SPATIAL_JSON = REPORT_DIR / "spatial_ablation.json"
FIXED_JSON = REPORT_DIR / "ensemble_hat_ablation_FIXED.json"
STAT_VALIDATION = REPORT_DIR / "STATISTICAL_VALIDATION_SUMMARY.md"


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def append_log(message: str) -> None:
    SYNC_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(f"[{now()}] {message}\n")


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def fmt_acc(value) -> str:
    try:
        return f"{float(value):.2f}%"
    except (TypeError, ValueError):
        return "N/A"


def build_frequency_table(payload: dict) -> str:
    rows = payload.get("results", [])
    if not isinstance(rows, list):
        return "| status | value |\n|:--|:--|\n| parse_error | results is not a list |\n"
    lines = [
        "| Configuration | Accuracy | Time (min) | Notes |",
        "|:--|--:|--:|:--|",
    ]
    for row in rows:
        desc = row.get("description", row.get("freq_mode", "unknown"))
        acc = fmt_acc(row.get("accuracy"))
        seconds = row.get("time_seconds")
        mins = float(seconds) / 60.0 if isinstance(seconds, (int, float)) else 0.0
        notes = f"freq={row.get('freq_mode')}, N={row.get('N')}"
        lines.append(f"| {desc} | {acc} | {mins:.1f} | {notes} |")
    return "\n".join(lines) + "\n"


def build_kp_fix_2_report() -> None:
    ensemble_payload = load_json(ENSEMBLE_JSON)
    fixed_payload = load_json(FIXED_JSON) if FIXED_JSON.exists() else {}

    fixed_results = fixed_payload.get("results", {}) if isinstance(fixed_payload, dict) else {}
    fixed_ensemble = fixed_results.get("ensemble_hat", {})
    fixed_d2d_10 = fixed_results.get("d2d_10pct", {})

    raw_same = (
        fixed_ensemble.get("raw") == fixed_d2d_10.get("raw")
        and fixed_ensemble.get("raw") is not None
    )

    stat_validation_state = "present" if STAT_VALIDATION.exists() else "missing"
    spatial_state = "present but quarantined" if SPATIAL_JSON.exists() else "pending/quarantined if produced"

    content = f"""# KP-FIX-2 Ensemble HAT Data Unification — Codex Draft

Generated: {now()}

## Decision State

This is a data-unification draft, not a final paper table. The frequency ablation JSON is now available, but the final truth value still needs Claude approval because earlier Ensemble HAT files disagree.

## Newly Available Frequency Ablation

Source: `report_md/_gpt/ensemble_frequency_ablation.json`

{build_frequency_table(ensemble_payload)}

## Existing Conflicting Ensemble HAT Sources

| Source | Value | Raw/status | Current treatment |
|:--|:--|:--|:--|
| Historical locked value | 86.37 ± 1.54% | Correction Broadcast locked | Preferred paper baseline until Claude changes it |
| `ensemble_hat_ablation_FIXED.json` ensemble_hat | {fmt_acc(fixed_ensemble.get("mean"))} ± {fmt_acc(fixed_ensemble.get("std")).replace('%', '')} | raw present | Needs explanation |
| `ensemble_hat_ablation_FIXED.json` d2d_10pct | {fmt_acc(fixed_d2d_10.get("mean"))} ± {fmt_acc(fixed_d2d_10.get("std")).replace('%', '')} | raw same as ensemble_hat: {raw_same} | Same experiment label, not independent |
| `STATISTICAL_VALIDATION_SUMMARY.md` | present: {stat_validation_state} | raw differs from FIXED.json | Needs final source selection |
| `spatial_ablation.json` | {spatial_state} | implementation bug in mode switch | Do not merge into KP-FIX-2 final numbers |

## Codex Recommendation

1. Keep `86.37 ± 1.54%` as the paper-facing Ensemble HAT baseline for now.
2. Use `ensemble_frequency_ablation.json` only for frequency-design comparison, not for replacing the locked baseline.
3. Treat `ensemble_hat_ablation_FIXED.json` `ensemble_hat` and `d2d_10pct` as the same run because their raw arrays are identical.
4. Do not use `spatial_ablation.json` for spatial-vs-i.i.d. claims until `spatial_d2d` is actually implemented in the analog noise path.
5. Claude should choose one final raw-data source before any table update.

## Next Required Evidence

- Checkpoint path and exact command for each accepted run.
- Seed list for each raw array.
- Confirmation that no source mixes train-time best accuracy with fresh-instance evaluation accuracy.

"""
    KP_FIX_2_PATH.write_text(content, encoding="utf-8")
    append_log(f"Generated {KP_FIX_2_PATH.relative_to(ROOT)}")


def main() -> int:
    append_log("Monitor started")
    wrote_kp_fix_2 = KP_FIX_2_PATH.exists()
    noted_spatial = False

    max_seconds = 8 * 60 * 60
    poll_seconds = 60
    start = time.time()

    while time.time() - start < max_seconds:
        if ENSEMBLE_JSON.exists() and not wrote_kp_fix_2:
            try:
                build_kp_fix_2_report()
                wrote_kp_fix_2 = True
            except Exception as exc:  # noqa: BLE001
                append_log(f"Failed to generate KP-FIX-2 report: {exc}")

        if SPATIAL_JSON.exists() and not noted_spatial:
            append_log(
                "spatial_ablation.json appeared; keep quarantined per "
                f"{SPATIAL_NOTE_PATH.relative_to(ROOT)}"
            )
            noted_spatial = True

        if wrote_kp_fix_2 and (not SPATIAL_JSON.exists() or noted_spatial):
            append_log("Monitor completed")
            return 0

        time.sleep(poll_seconds)

    append_log("Monitor timed out")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

