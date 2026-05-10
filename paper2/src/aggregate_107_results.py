#!/usr/bin/env python3
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path

PROJECTS_ROOT = Path(__file__).resolve().parents[3]
COMPUTE_VIT_ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = PROJECTS_ROOT / "remote_reviews" / "107" / "results" / "paper2"
REPORT_PATH = COMPUTE_VIT_ROOT / "coordination" / "remote_tasks" / "107" / "REMOTE_107_PHASE_P8_CORRECTED_NOISE_REPORT_20260510.md"
TSV_PATH = COMPUTE_VIT_ROOT / "paper2" / "results" / "FRESH_D2D_SUMMARY_107_20260510.tsv"
METADATA_TSV_PATH = COMPUTE_VIT_ROOT / "paper2" / "results" / "METADATA_COMPLETENESS_107_20260510.tsv"

REQUIRED_METADATA = [
    "commit",
    "command",
    "config",
    "dataset",
    "eval_protocol",
    "checkpoint_sha256",
]


def layer_label(analog_layers):
    layers = tuple(analog_layers or [])
    if layers == tuple(range(24)):
        return "all24"
    if layers == (23,):
        return "last1_24l"
    if layers == (22, 23):
        return "last2_24l"
    if layers == (20, 21, 22, 23):
        return "last4_24l"
    if not layers:
        return "none"
    return f"layers_{'-'.join(str(layer) for layer in layers)}"


def checkpoint_name(checkpoint_dir):
    return str(checkpoint_dir or "unknown").rstrip("/").rsplit("/", 1)[-1]


def seed_sort_key(seed):
    return (seed is None, str(seed) if seed is None else seed)


def load_rows():
    rows = []
    metadata_missing_totals = Counter()
    bad_json = []

    for path in sorted(SOURCE_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text())
        except Exception as exc:
            bad_json.append((path.name, str(exc)))
            continue

        missing = [key for key in REQUIRED_METADATA if not data.get(key)]
        metadata_missing_totals.update(missing)

        if data.get("ppl") is None or data.get("sigma_d2d") is None or data.get("sigma_c2c") is None:
            continue

        layers = tuple(data.get("analog_layers") or [])
        rows.append(
            {
                "source_json": path.relative_to(PROJECTS_ROOT).as_posix(),
                "file": path.name,
                "checkpoint": checkpoint_name(data.get("checkpoint_dir")),
                "checkpoint_dir": str(data.get("checkpoint_dir") or ""),
                "analog_layers": layers,
                "layer_label": layer_label(layers),
                "eval_c2c": float(data.get("sigma_c2c")),
                "eval_d2d": float(data.get("sigma_d2d")),
                "d2d_seed": data.get("d2d_seed"),
                "ppl": float(data.get("ppl")),
                "missing_metadata": tuple(missing),
            }
        )

    return rows, metadata_missing_totals, bad_json


def aggregate(rows):
    grouped = defaultdict(list)
    for row in rows:
        if row["eval_d2d"] <= 0:
            continue
        key = (
            row["checkpoint"],
            row["layer_label"],
            row["analog_layers"],
            row["eval_c2c"],
            row["eval_d2d"],
        )
        grouped[key].append(row)

    summaries = []
    for (checkpoint, label, layers, c2c, d2d), items in grouped.items():
        ppls = [item["ppl"] for item in items]
        seeds = sorted({item["d2d_seed"] for item in items}, key=seed_sort_key)
        best = min(items, key=lambda item: item["ppl"])
        worst = max(items, key=lambda item: item["ppl"])
        missing_metadata = sorted({key for item in items for key in item["missing_metadata"]})
        summaries.append(
            {
                "status": "candidate_index_not_claim_lock",
                "checkpoint": checkpoint,
                "layer_label": label,
                "analog_layers": ",".join(str(layer) for layer in layers),
                "eval_c2c": c2c,
                "eval_d2d": d2d,
                "n_json": len(items),
                "n_d2d_seeds": len(seeds),
                "d2d_seeds": ",".join("NA" if seed is None else str(seed) for seed in seeds),
                "mean_ppl": statistics.mean(ppls),
                "std_ppl": statistics.stdev(ppls) if len(ppls) > 1 else 0.0,
                "min_ppl": min(ppls),
                "max_ppl": max(ppls),
                "best_json": best["file"],
                "worst_json": worst["file"],
                "missing_required_metadata": ",".join(missing_metadata) if missing_metadata else "none",
            }
        )

    return sorted(
        summaries,
        key=lambda row: (
            row["layer_label"],
            row["checkpoint"],
            row["eval_c2c"],
            row["eval_d2d"],
        ),
    )


def write_tsv(summaries):
    columns = [
        "status",
        "checkpoint",
        "layer_label",
        "analog_layers",
        "eval_c2c",
        "eval_d2d",
        "n_json",
        "n_d2d_seeds",
        "d2d_seeds",
        "mean_ppl",
        "std_ppl",
        "min_ppl",
        "max_ppl",
        "best_json",
        "worst_json",
        "missing_required_metadata",
    ]
    lines = ["\t".join(columns)]
    for row in summaries:
        lines.append(
            "\t".join(
                f"{row[column]:.6g}" if isinstance(row[column], float) else str(row[column])
                for column in columns
            )
        )
    TSV_PATH.write_text("\n".join(lines) + "\n")


def write_metadata_tsv(rows):
    columns = [
        "status",
        "source_json",
        "checkpoint",
        "checkpoint_dir",
        "layer_label",
        "analog_layers",
        "eval_c2c",
        "eval_d2d",
        "d2d_seed",
        "ppl",
        "has_commit",
        "has_command",
        "has_config",
        "has_dataset",
        "has_eval_protocol",
        "has_checkpoint_sha256",
        "missing_required_metadata",
    ]
    lines = ["\t".join(columns)]
    for row in sorted(rows, key=lambda item: item["source_json"]):
        missing = set(row["missing_metadata"])
        values = {
            "status": "fail_missing_required_metadata" if missing else "pass",
            "source_json": row["source_json"],
            "checkpoint": row["checkpoint"],
            "checkpoint_dir": row["checkpoint_dir"],
            "layer_label": row["layer_label"],
            "analog_layers": ",".join(str(layer) for layer in row["analog_layers"]),
            "eval_c2c": row["eval_c2c"],
            "eval_d2d": row["eval_d2d"],
            "d2d_seed": "NA" if row["d2d_seed"] is None else row["d2d_seed"],
            "ppl": row["ppl"],
            "has_commit": int("commit" not in missing),
            "has_command": int("command" not in missing),
            "has_config": int("config" not in missing),
            "has_dataset": int("dataset" not in missing),
            "has_eval_protocol": int("eval_protocol" not in missing),
            "has_checkpoint_sha256": int("checkpoint_sha256" not in missing),
            "missing_required_metadata": ",".join(sorted(missing)) if missing else "none",
        }
        lines.append(
            "\t".join(
                f"{values[column]:.6g}" if isinstance(values[column], float) else str(values[column])
                for column in columns
            )
        )
    METADATA_TSV_PATH.write_text("\n".join(lines) + "\n")


def selected_markdown_rows(summaries):
    rows = [row for row in summaries if row["n_d2d_seeds"] >= 5]
    preferred = []
    for row in rows:
        checkpoint = row["checkpoint"]
        if (
            checkpoint.startswith("410m_")
            or checkpoint.startswith("combined_layer")
            or checkpoint.startswith("hat_d2d002_500_freshd2d")
        ):
            preferred.append(row)
    return (preferred or rows)[:24]


def write_report(rows, summaries, metadata_missing_totals, bad_json):
    d2d_seed_missing = sum(1 for row in rows if row["d2d_seed"] is None)
    markdown_rows = selected_markdown_rows(summaries)

    lines = [
        "# Remote 107 Phase P8 Corrected-Noise Report — Strict-Review Draft",
        "",
        "**Date:** 2026-05-10",
        "**Status:** DRAFT / candidate index only; not claim-bearing and not locked.",
        "",
        "## Strict-review verdict",
        "",
        "This file supersedes the earlier Gemini claim-lock text. The raw JSON results are useful, but the current local package does not satisfy the P8 evidence-lock requirements yet.",
        "",
        "Do not cite these tables as Paper2 claims until the metadata and comparison gates below are closed.",
        "",
        "## Why the prior claim-lock table was rejected",
        "",
        "- The prior aggregation grouped runs only by broad labels such as `last1`, `last2`, and `all24`, which mixed distinct checkpoints and experiment conditions.",
        "- Its own table contradicted its conclusion: several rows had standard deviations far above 0.1 PPL, yet the conclusion claimed `<0.1 PPL` variance.",
        f"- Raw JSON count inspected: {len(rows)} usable files; bad JSON files: {len(bad_json)}.",
        f"- Files missing `d2d_seed`: {d2d_seed_missing}.",
        "- Required metadata missing from every inspected JSON: " + ", ".join(f"`{key}` ({metadata_missing_totals[key]})" for key in REQUIRED_METADATA) + ".",
        "",
        "## Candidate Fresh-D2D index",
        "",
        f"The companion TSV `{TSV_PATH.relative_to(COMPUTE_VIT_ROOT)}` is now grouped by checkpoint, exact analog-layer list, eval C2C, and eval D2D. It is an audit index, not a claim-bearing table. The per-file metadata audit is `{METADATA_TSV_PATH.relative_to(COMPUTE_VIT_ROOT)}`.",
        "",
        "| checkpoint | layers | eval C2C | eval D2D | n seeds | mean PPL | std PPL | min PPL | max PPL |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for row in markdown_rows:
        lines.append(
            f"| `{row['checkpoint']}` | `{row['layer_label']}` | {row['eval_c2c']:.3g} | {row['eval_d2d']:.3g} | {row['n_d2d_seeds']} | {row['mean_ppl']:.3f} | {row['std_ppl']:.3f} | {row['min_ppl']:.3f} | {row['max_ppl']:.3f} |"
        )

    lines.extend(
        [
            "",
            "## Gates still required before Paper2 claim use",
            "",
            "1. Identify the exact corrected-noise code path and Git SHA used by the remote 107 run.",
            "2. Attach exact training/eval commands, dataset split, context length, stride, batch size, analog-layer list, and seed semantics for every result row.",
            "3. Add checkpoint paths plus hashes without copying checkpoints into Paper1 or GitHub payloads.",
            "4. Produce the old-vs-corrected comparison table and mark whether the qualitative trend is preserved.",
            "5. Re-run metadata completeness after the JSON sidecars are patched or a signed manifest is provided.",
            "",
            "## Safe current use",
            "",
            "Use this report only to plan the next Paper2/107 audit and drafting tasks. Do not promote it into Paper1 source-data paths, and do not describe the 107 evidence as locked.",
        ]
    )

    REPORT_PATH.write_text("\n".join(lines) + "\n")


def main():
    rows, metadata_missing_totals, bad_json = load_rows()
    summaries = aggregate(rows)
    write_tsv(summaries)
    write_metadata_tsv(rows)
    write_report(rows, summaries, metadata_missing_totals, bad_json)
    print(f"usable_json={len(rows)}")
    print(f"candidate_groups={len(summaries)}")
    print(f"report={REPORT_PATH}")
    print(f"tsv={TSV_PATH}")


if __name__ == "__main__":
    main()
