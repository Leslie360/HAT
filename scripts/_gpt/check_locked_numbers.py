# ⚠️ WARNING: H6 (expected=27.72) is BUG-CONTAMINATED — pre-fix NL=2.0 result invalid after commit 33bed9c.
# Do not use this script to verify severe-NL numbers. Bug-immune numbers (H3-H5, H7-H8) remain valid.
# See report_md/_gpt/BROADCAST_REBUILD_3WEEK_20260424.md

#!/usr/bin/env python3
"""Guard script: verify locked numbers in manuscript match canonical JSON sources.

Usage:
    cd /home/qiaosir/projects/compute_vit
    python scripts/_gpt/check_locked_numbers.py

Exit codes:
    0 = all locked numbers match
    1 = mismatch found (prints details to stderr)
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Optional

REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass
class LockedNumber:
    id: str
    description: str
    json_path: Path
    accessor: Callable[[Any], Any]
    expected: float
    tolerance: Optional[float] = None


def load_json(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    locked_numbers: list[LockedNumber] = [
        # §1 Headline numbers
        LockedNumber(
            id="H3",
            description="A2.3 inverse-gamma compensated at gamma=2.0, I_dark=10pA",
            json_path=REPO_ROOT / "report_md" / "json" / "a23_experiment_results.json",
            accessor=lambda d: d["group1"]["2.0_1e-11"]["acc_compensated"],
            expected=89.85,
            tolerance=0.01,
        ),
        LockedNumber(
            id="H3_raw",
            description="A2.3 raw baseline at gamma=2.0, I_dark=10pA",
            json_path=REPO_ROOT / "report_md" / "json" / "a23_experiment_results.json",
            accessor=lambda d: d["group1"]["2.0_1e-11"]["acc_raw"],
            expected=84.04,
            tolerance=0.01,
        ),
        LockedNumber(
            id="H4",
            description="Ensemble HAT fresh-instance mean",
            json_path=REPO_ROOT / "report_md" / "_gpt" / "json_gpt" / "fresh_instance_eval.json",
            accessor=lambda d: d["V4_Ensemble"]["mean"],
            expected=86.37,
            tolerance=0.01,
        ),
        LockedNumber(
            id="H5",
            description="Standard HAT fresh-instance collapse",
            json_path=REPO_ROOT / "report_md" / "_gpt" / "json_gpt" / "fresh_instance_eval.json",
            accessor=lambda d: d["V4_Standard"]["mean"],
            expected=10.0,
            tolerance=0.001,
        ),
        LockedNumber(
            id="H6",
            description="NL=2.0 global HAT eval",
            json_path=REPO_ROOT / "report_md" / "_gpt" / "json_gpt" / "v4_nl2_hat_eval_results_gpt.json",
            accessor=lambda d: d[0]["test_acc_mean"],
            expected=27.72,
            tolerance=0.01,
        ),
        LockedNumber(
            id="H7",
            description="OPECT zero-shot transfer",
            json_path=REPO_ROOT / "report_md" / "_gpt" / "json_gpt" / "literature_profile_eval.json",
            accessor=lambda d: d["V4_Ensemble"]["test_acc_mean"],
            expected=88.53,
            tolerance=0.01,
        ),
        LockedNumber(
            id="H8",
            description="Tiny-ViT FP32 baseline (single-seed train best)",
            json_path=REPO_ROOT / "report_md" / "_gpt" / "json_gpt" / "tinyvit_v1_results_gpt.json",
            accessor=lambda d: d[0]["best_test_acc"],
            expected=97.48,
            tolerance=0.01,
        ),
        # In-flight numbers
        LockedNumber(
            id="L1",
            description="MLP-only NL mitigation",
            json_path=REPO_ROOT / "report_md" / "_gpt" / "json_gpt" / "v4_nl2_mlp_linear_comp_train_results_gpt.json",
            accessor=lambda d: d[0]["best_test_acc"],
            expected=87.79,
            tolerance=0.01,
        ),
        LockedNumber(
            id="L4",
            description="QKV-only NL mitigation",
            json_path=REPO_ROOT / "report_md" / "_gpt" / "json_gpt" / "v4_nl2_qkv_linear_comp_train_results_gpt.json",
            accessor=lambda d: d[0]["best_test_acc"],
            expected=18.72,
            tolerance=0.01,
        ),
        LockedNumber(
            id="L3",
            description="E3 learnable gamma best val acc",
            json_path=REPO_ROOT / "report_md" / "json" / "learnable_gamma_20260418_110011_g2.0_s42.json",
            accessor=lambda d: d["results"]["learnable"]["best_val_acc"],
            expected=51.9,
            tolerance=0.01,
        ),
        LockedNumber(
            id="L3_gamma",
            description="E3 learned gamma_comp",
            json_path=REPO_ROOT / "report_md" / "json" / "learnable_gamma_20260418_110011_g2.0_s42.json",
            accessor=lambda d: d["results"]["learnable"]["learned_gamma_history"][-1],
            expected=0.7398,
            tolerance=0.0001,
        ),
        # Cross-framework
        LockedNumber(
            id="F5_ours",
            description="CrossSim standard noise ours",
            json_path=REPO_ROOT / "report_md" / "_gpt" / "crosssim_standard_noise.json",
            accessor=lambda d: d["our_framework"]["mean"],
            expected=81.63,
            tolerance=0.01,
        ),
        LockedNumber(
            id="F5_crosssim",
            description="CrossSim standard noise CrossSim",
            json_path=REPO_ROOT / "report_md" / "_gpt" / "crosssim_standard_noise.json",
            accessor=lambda d: d["crosssim"]["mean"],
            expected=67.20,
            tolerance=0.01,
        ),
        # ADC nonideality
        LockedNumber(
            id="A1",
            description="ADC ideal hook-based",
            json_path=REPO_ROOT / "report_md" / "_gpt" / "json_gpt" / "adc_layerwise_nonideality_full_gpt.json",
            accessor=lambda d: next(r["mean"] for r in d["results"] if r["name"] == "Ideal"),
            expected=82.04,
            tolerance=0.02,
        ),
        # Retention
        LockedNumber(
            id="R0s",
            description="Retention 0s",
            json_path=REPO_ROOT / "report_md" / "_gpt" / "json_gpt" / "tinyvit_v4_retention_results_gpt.json",
            accessor=lambda d: next(r["test_acc_mean"] for r in d["retention"] if r["time_s"] == 0),
            expected=91.63,
            tolerance=0.02,
        ),
        LockedNumber(
            id="R10s",
            description="Retention 10s plateau",
            json_path=REPO_ROOT / "report_md" / "_gpt" / "json_gpt" / "tinyvit_v4_retention_results_gpt.json",
            accessor=lambda d: next(r["test_acc_mean"] for r in d["retention"] if r["time_s"] == 10),
            expected=79.13,
            tolerance=0.02,
        ),
    ]

    failures = 0
    warnings = 0
    print("=" * 70)
    print("Locked Numbers Guard Check")
    print("=" * 70)

    for ln in locked_numbers:
        try:
            data = load_json(ln.json_path)
            actual = ln.accessor(data)
        except Exception as e:
            print(f"\n[{ln.id}] ❌ ERROR loading {ln.json_path}: {e}")
            failures += 1
            continue

        if ln.tolerance is not None:
            match = abs(actual - ln.expected) <= ln.tolerance
        else:
            match = actual == ln.expected

        status = "✅ PASS" if match else "❌ FAIL"
        print(f"\n[{ln.id}] {status} — {ln.description}")
        print(f"       Expected: {ln.expected}")
        print(f"       Actual:   {actual}")
        if ln.tolerance:
            print(f"       Tolerance: ±{ln.tolerance}")
        print(f"       Source:   {ln.json_path}")

        if not match:
            failures += 1

    # Warn about H8 discrepancy
    print("\n" + "-" * 70)
    print("NOTE: H8 (Tiny-ViT FP32) single-seed train best = 97.48%,")
    print("      manuscript claims 98.06% which is the 3-seed mean (98.18/97.87/98.14).")
    print("      Guard script verifies the single-seed canonical file;")
    print("      3-seed aggregate must be verified manually or via separate aggregate JSON.")
    print("-" * 70)

    print("\n" + "=" * 70)
    total = len(locked_numbers)
    passed = total - failures
    print(f"Result: {passed}/{total} passed")
    if failures == 0:
        print("All locked numbers match. Manuscript is consistent with JSON sources.")
    else:
        print(f"WARNING: {failures} mismatch(es) found. Do NOT submit before resolving.")
    print("=" * 70)

    return 1 if failures > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
