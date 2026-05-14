#!/usr/bin/env python3
"""Compare two retention/protection summary TSV files."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def load_summary(path: Path) -> dict[tuple[str, float], dict]:
    with path.open("r", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    return {
        (row["strategy"], float(row["retention_time_s"])): row
        for row in rows
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare retention/protection summary TSVs")
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--baseline-label", default="baseline")
    parser.add_argument("--candidate-label", default="candidate")
    args = parser.parse_args()

    baseline = load_summary(Path(args.baseline))
    candidate = load_summary(Path(args.candidate))
    keys = sorted(set(baseline) & set(candidate), key=lambda x: (x[1], x[0]))

    print(
        "retention_time_s\tstrategy\t"
        f"{args.baseline_label}_mean\t{args.candidate_label}_mean\tdelta_pp"
    )
    for key in keys:
        b = float(baseline[key]["accuracy_mean"])
        c = float(candidate[key]["accuracy_mean"])
        print(f"{key[1]:.1f}\t{key[0]}\t{b:.4f}\t{c:.4f}\t{c - b:+.4f}")


if __name__ == "__main__":
    main()
