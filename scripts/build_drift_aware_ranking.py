#!/usr/bin/env python3
"""Build a drift-aware protection ranking from drift-vector profiling output."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def load_tsv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def write_tsv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build drift-aware ranking TSV")
    parser.add_argument(
        "--drift_tsv",
        default="thesis/results/drift_aware_sam/drift_vectors_profile_20260512_004906.tsv",
    )
    parser.add_argument(
        "--reference_sensitivity_tsv",
        default="thesis/results/mixed_precision/layer_sensitivity_full42_summary_20260510.tsv",
    )
    parser.add_argument("--retention_time", type=float, default=1000.0)
    parser.add_argument(
        "--output_tsv",
        default="thesis/results/drift_aware_sam/drift_aware_ranking_1000s_20260513.tsv",
    )
    args = parser.parse_args()

    drift_rows = load_tsv(Path(args.drift_tsv))
    ref_rows = load_tsv(Path(args.reference_sensitivity_tsv))

    ref_by_module = {row["module_path"]: row for row in ref_rows}
    filtered = [row for row in drift_rows if float(row["retention_time_s"]) == args.retention_time]
    filtered.sort(key=lambda row: float(row["drift_effective_l2"]), reverse=True)

    out_rows = []
    for rank, row in enumerate(filtered, start=1):
        ref = ref_by_module.get(row["module_path"], {})
        out_rows.append(
            {
                "rank": rank,
                "layer_id": ref.get("layer_id", ""),
                "module_path": row["module_path"],
                "role": ref.get("role", ""),
                "stage": ref.get("stage", ""),
                "layer_type": row["layer_type"],
                "drift_effective_l2": f"{float(row['drift_effective_l2']):.6f}",
                "drift_effective_linf": f"{float(row['drift_effective_linf']):.6f}",
                "drift_abs_to_weight_abs_corr": f"{float(row['drift_abs_to_weight_abs_corr']):.6f}",
                "retention_time_s": f"{float(row['retention_time_s']):.1f}",
                "reference_mean_acc_drop": ref.get("mean_acc_drop", ""),
                "reference_std_acc_drop": ref.get("std_acc_drop", ""),
                "source": "drift_vectors_profile + layer_sensitivity_full42_summary",
                "evidence_grade": "pilot/provisional",
            }
        )

    write_tsv(Path(args.output_tsv), out_rows)
    print(f"wrote {args.output_tsv}")


if __name__ == "__main__":
    main()
