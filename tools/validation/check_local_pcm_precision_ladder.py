#!/usr/bin/env python3
"""Verify local R11D PCM precision-ladder aggregates from raw artifacts."""

from __future__ import annotations

import json
import statistics as stats
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CKPT_ROOT = REPO_ROOT / "paper2_aihwkit_baseline" / "checkpoints"

GROUPS = {
    "8bit": {
        "runs": [
            "r11d_5a_pcm_seed123",
            "r11d_5a_pcm_seed456",
            "r11d_5a_pcm_seed789",
        ],
        "inp_res": 0.00390625,
        "expected": {
            "best_mean": 77.64,
            "best_std": 0.68,
            "fresh_mean": 77.60,
            "fresh_std": 0.64,
            "drift_drop": 0.04,
        },
    },
    "6bit": {
        "runs": [
            "r11d_6bit_pcm_seed123",
            "r11d_6bit_pcm_seed456",
            "r11d_6bit_pcm_seed457",
            "r11d_6bit_pcm_seed789",
        ],
        "inp_res": 0.015625,
        "expected": {
            "best_mean": 68.40,
            "best_std": 6.00,
            "fresh_mean": 68.44,
            "fresh_std": 6.03,
            "drift_drop": 0.04,
        },
    },
    "4bit": {
        "runs": [
            "r11d_7_pcm_4bit_seed123",
            "r11d_7_pcm_4bit_seed456_clean",
            "r11d_7_pcm_4bit_seed789",
        ],
        "inp_res": 0.0625,
        "expected": {
            "best_mean": 76.71,
            "best_std": 0.46,
            "fresh_mean": 76.68,
            "fresh_std": 0.37,
            "drift_drop": 4.01,
        },
    },
}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def drift_accuracy(drift: dict, seconds: float) -> float:
    for row in drift["results"]:
        if float(row["t_inference_seconds"]) == seconds:
            return float(row["accuracy"])
    raise KeyError(f"missing drift time {seconds}")


def assert_close(label: str, actual: float, expected: float, tol: float = 0.01) -> bool:
    ok = abs(actual - expected) <= tol
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {label}: expected {expected:.4f}, actual {actual:.4f}, tol ±{tol}")
    return ok


def main() -> int:
    failures = 0
    print("=" * 72)
    print("Local R11D PCM Precision-Ladder Guard")
    print("=" * 72)

    for group_name, spec in GROUPS.items():
        best_values: list[float] = []
        fresh_values: list[float] = []
        drift0_values: list[float] = []
        drift1d_values: list[float] = []

        print(f"\n## {group_name}")
        for run_id in spec["runs"]:
            run_dir = CKPT_ROOT / run_id
            history_path = run_dir / "training_history.json"
            history = load_json(history_path) if history_path.exists() else None
            fresh = load_json(run_dir / "fresh_eval.json")
            drift = load_json(run_dir / "drift_eval.json")

            if history is not None:
                args = history["args"]
                rpu = history["rpu_config_spec"]
                run_failures = [
                    (history.get("pcm_preset_used") == "PCMPresetUnitCell", "pcm_preset_used"),
                    (abs(float(args["inp_res"]) - spec["inp_res"]) < 1e-12, "arg_inp_res"),
                    (abs(float(args["out_res"]) - spec["inp_res"]) < 1e-12, "arg_out_res"),
                    (abs(float(rpu["forward_inp_res"]) - spec["inp_res"]) < 1e-12, "rpu_inp_res"),
                    (abs(float(rpu["forward_out_res"]) - spec["inp_res"]) < 1e-12, "rpu_out_res"),
                ]
                bad = [name for ok, name in run_failures if not ok]
                if bad:
                    print(f"[FAIL] {run_id}: provenance failed {bad}")
                    failures += len(bad)
                else:
                    print(f"[PASS] {run_id}: provenance ok")
                best_values.append(float(history["best_acc"]))
            else:
                print(f"[WARN] {run_id}: training_history missing; best_acc excluded")

            fresh_values.append(float(fresh["mean"]))
            drift0_values.append(drift_accuracy(drift, 0.0))
            drift1d_values.append(drift_accuracy(drift, 86400.0))

        actuals = {
            "best_mean": stats.mean(best_values),
            "best_std": stats.stdev(best_values),
            "fresh_mean": stats.mean(fresh_values),
            "fresh_std": stats.stdev(fresh_values),
            "drift_drop": stats.mean(drift0_values) - stats.mean(drift1d_values),
        }

        for key, expected in spec["expected"].items():
            if not assert_close(f"{group_name}.{key}", actuals[key], expected):
                failures += 1

    pure4 = load_json(CKPT_ROOT / "r11d_1_4bit" / "fresh_eval.json")["mean"]
    ideal8 = load_json(CKPT_ROOT / "fresh_eval.json")["mean"]
    if not assert_close("pure_4bit_collapse.fresh_mean", float(pure4), 14.64):
        failures += 1
    if not assert_close("ideal_8bit_baseline.fresh_mean", float(ideal8), 87.28):
        failures += 1

    print("\n" + "=" * 72)
    if failures:
        print(f"Result: FAIL ({failures} checks failed)")
        return 1
    print("Result: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
