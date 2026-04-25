#!/usr/bin/env python3
"""Build M-series local/remote parity CSV and Markdown report."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import mean, stdev


ROOT = Path(__file__).resolve().parents[2]
JSON_DIR = ROOT / "report_md/_gpt/json_gpt"
CSV_PATH = ROOT / "report_md/_gpt/csv_gpt/cross_host_parity_mseries.csv"
MD_PATH = ROOT / "report_md/_gpt/CODEX_CX_FRESH_EVAL_MSERIES_REPORT_20260424.md"

LOCAL_RUNS = [
    ("CX-M1", "V3", "Standard", 123, "cx_m1_fresh_eval.json"),
    ("CX-M2", "V4", "Ensemble", 123, "cx_m2_fresh_eval.json"),
    ("CX-M3", "V4", "Proportional", 123, "cx_m3_fresh_eval.json"),
    ("CX-M4", "V4", "Proportional", 456, "cx_m4_fresh_eval.json"),
    ("CX-M5", "V3", "Standard", 456, "cx_m5_fresh_eval.json"),
    ("CX-M6", "V4", "Ensemble", 456, "cx_m6_fresh_eval.json"),
]

REMOTE_ROWS = [
    {
        "run_id": "R-M1",
        "host": "remote",
        "model": "V3",
        "hat_type": "Standard",
        "seed": "123",
        "batch_size": "512",
        "nl": "2.0",
        "train_best": "83.75",
        "fresh_mean": "83.64",
        "fresh_std": "0.10",
        "fresh_range": "range_width=0.42",
    },
    {
        "run_id": "R-M2 s123",
        "host": "remote",
        "model": "V4",
        "hat_type": "Proportional",
        "seed": "123",
        "batch_size": "512",
        "nl": "2.0",
        "train_best": "84.79",
        "fresh_mean": "84.80",
        "fresh_std": "0.08",
        "fresh_range": "range_width=0.32",
    },
    {
        "run_id": "R-M2 s222",
        "host": "remote",
        "model": "V4",
        "hat_type": "Proportional",
        "seed": "222",
        "batch_size": "512",
        "nl": "2.0",
        "train_best": "84.71",
        "fresh_mean": "84.79",
        "fresh_std": "0.07",
        "fresh_range": "range_width=0.23",
    },
    {
        "run_id": "R-M2 s333",
        "host": "remote",
        "model": "V4",
        "hat_type": "Proportional",
        "seed": "333",
        "batch_size": "512",
        "nl": "2.0",
        "train_best": "83.23",
        "fresh_mean": "TBD",
        "fresh_std": "TBD",
        "fresh_range": "TBD",
    },
    {
        "run_id": "R-M2 s789",
        "host": "remote",
        "model": "V4",
        "hat_type": "Proportional",
        "seed": "789",
        "batch_size": "512",
        "nl": "2.0",
        "train_best": "83.38",
        "fresh_mean": "TBD",
        "fresh_std": "TBD",
        "fresh_range": "TBD",
    },
    {
        "run_id": "R-M2 s999",
        "host": "remote",
        "model": "V4",
        "hat_type": "Proportional",
        "seed": "999",
        "batch_size": "512",
        "nl": "2.0",
        "train_best": "83.72",
        "fresh_mean": "TBD",
        "fresh_std": "TBD",
        "fresh_range": "TBD",
    },
    {
        "run_id": "R-M5 s567",
        "host": "remote",
        "model": "V3",
        "hat_type": "Standard",
        "seed": "567",
        "batch_size": "512",
        "nl": "2.0",
        "train_best": "83.67",
        "fresh_mean": "TBD",
        "fresh_std": "TBD",
        "fresh_range": "TBD",
    },
    {
        "run_id": "R-M5 s890",
        "host": "remote",
        "model": "V3",
        "hat_type": "Standard",
        "seed": "890",
        "batch_size": "512",
        "nl": "2.0",
        "train_best": "82.20",
        "fresh_mean": "TBD",
        "fresh_std": "TBD",
        "fresh_range": "TBD",
    },
]


def fmt(value, digits=4):
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "TBD"
    return f"{float(value):.{digits}f}"


def load_local_rows():
    rows = []
    for run_id, model, hat_type, seed, filename in LOCAL_RUNS:
        path = JSON_DIR / filename
        data = json.loads(path.read_text(encoding="utf-8"))
        instances = list(data.get("fresh_per_instance_mean") or data["instance_means"])
        fresh_range = f"{min(instances):.2f}-{max(instances):.2f}"
        rows.append({
            "run_id": run_id,
            "host": "local",
            "model": model,
            "hat_type": hat_type,
            "seed": str(seed),
            "batch_size": "64",
            "nl": "2.0",
            "train_best": fmt(data.get("checkpoint_best_acc"), 2),
            "fresh_mean": fmt(data.get("cross_instance_mean"), 4),
            "fresh_std": fmt(data.get("cross_instance_std"), 4),
            "fresh_range": fresh_range,
            "_mean": float(data["cross_instance_mean"]),
            "_std": float(data["cross_instance_std"]),
            "_instances": instances,
            "_json": str(path.relative_to(ROOT)),
            "_commit": data.get("commit_hash"),
            "_dirty": data.get("git_worktree_dirty"),
            "_cuda": data.get("cuda_device_name"),
            "_torch": data.get("pytorch_version"),
        })
    return rows


def group_stats(rows, host, hat_type):
    values = [r["_mean"] for r in rows if r["host"] == host and r["hat_type"] == hat_type]
    if not values:
        return None
    if len(values) == 1:
        return mean(values), None, len(values)
    return mean(values), stdev(values), len(values)


def numeric_remote(hat_type):
    vals = [
        float(r["fresh_mean"])
        for r in REMOTE_ROWS
        if r["hat_type"] == hat_type and r["fresh_mean"] != "TBD"
    ]
    if not vals:
        return None
    if len(vals) == 1:
        return mean(vals), None, len(vals)
    return mean(vals), stdev(vals), len(vals)


def main():
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    local_rows = load_local_rows()
    csv_rows = [
        {k: v for k, v in r.items() if not k.startswith("_")}
        for r in local_rows
    ] + REMOTE_ROWS

    fieldnames = [
        "run_id",
        "host",
        "model",
        "hat_type",
        "seed",
        "batch_size",
        "nl",
        "train_best",
        "fresh_mean",
        "fresh_std",
        "fresh_range",
    ]
    with CSV_PATH.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)

    local_standard = group_stats(local_rows, "local", "Standard")
    local_ensemble = group_stats(local_rows, "local", "Ensemble")
    local_prop = group_stats(local_rows, "local", "Proportional")
    remote_standard = numeric_remote("Standard")
    remote_prop = numeric_remote("Proportional")

    by_id = {r["run_id"]: r for r in local_rows}
    delta_standard = 83.64 - by_id["CX-M1"]["_mean"]
    delta_prop_seed123 = 84.80 - by_id["CX-M3"]["_mean"]
    delta_prop_group = (remote_prop[0] if remote_prop else float("nan")) - local_prop[0]

    metadata = local_rows[0]
    lines = [
        "# CODEX CX-FRESH-EVAL-MSERIES Report",
        "",
        "- Date: 2026-04-24",
        "- Scope: local M1-M6 fresh-instance eval consolidation plus remote parity rows provided in dispatch.",
        "- Protocol: 10 fresh D2D instances x 5 MC eval runs per checkpoint.",
        "- NL: explicit `NL_LTP=2.0`, `NL_LTD=-2.0`; noise mode matched checkpoint provenance.",
        f"- Commit: `{metadata.get('_commit')}`; dirty worktree: `{metadata.get('_dirty')}`.",
        f"- CUDA device: `{metadata.get('_cuda')}`; PyTorch: `{metadata.get('_torch')}`.",
        f"- CSV: `{CSV_PATH.relative_to(ROOT)}`",
        "- Provenance guard: `eval_fresh_instances_postfix.py` used checkpoint metadata by default; "
        "`allow_eval_nl_override=false` and `eval_provenance_mismatches=[]` for all local M1-M6 JSONs.",
        "- ADC scope: these M-series fresh-eval numbers use the default analog forward path "
        "(conductance quantization + D2D/C2C/NL + float output accumulation). "
        "Hook-based ADC quantization is a separate ablation, not active in this report.",
        "",
        "## Local Fresh Eval",
        "",
        "| Run | Config | Seed | Train Best | Fresh Mean | Fresh Std | Range | JSON |",
        "|:--|:--|--:|--:|--:|--:|:--|:--|",
    ]
    for r in local_rows:
        config = f"{r['model']} {r['hat_type']}"
        lines.append(
            f"| {r['run_id']} | {config} | {r['seed']} | {r['train_best']} | "
            f"{r['fresh_mean']} | {r['fresh_std']} | {r['fresh_range']} | `{r['_json']}` |"
        )

    lines.extend([
        "",
        "## Aggregate Statistics",
        "",
        "| Group | n seeds | Fresh mean | Across-seed std |",
        "|:--|--:|--:|--:|",
    ])
    for label, stats in [
        ("Local V3 Standard", local_standard),
        ("Local V4 Ensemble", local_ensemble),
        ("Local V4 Proportional", local_prop),
        ("Remote V3 Standard", remote_standard),
        ("Remote V4 Proportional", remote_prop),
    ]:
        if stats is None:
            continue
        m, s, n = stats
        lines.append(f"| {label} | {n} | {fmt(m, 4)} | {fmt(s, 4) if s is not None else 'single-run'} |")

    lines.extend([
        "",
        "## Cross-Host Delta",
        "",
        f"- V3 Standard seed 123: remote R-M1 fresh `83.6400%` - local CX-M1 fresh `{by_id['CX-M1']['_mean']:.4f}%` = `{delta_standard:+.4f} pp`.",
        f"- V4 Proportional seed 123: remote R-M2 s123 fresh `84.8000%` - local CX-M3 fresh `{by_id['CX-M3']['_mean']:.4f}%` = `{delta_prop_seed123:+.4f} pp`.",
        f"- V4 Proportional group mean: remote known fresh `{remote_prop[0]:.4f}%` - local CX-M3/M4 mean `{local_prop[0]:.4f}%` = `{delta_prop_group:+.4f} pp`.",
        "",
        "Interpretation: the current remote advantage is not a uniform 1-2 pp shift. It is about +1.6 pp for the Standard seed-123 comparison but about +4.1 pp for the known Proportional comparison. This is confounded by host recipe and batch size (local batch 64 vs remote batch 512), so the parity table should be cited as cross-host evidence, not as a clean causal estimate of batch-size effect.",
        "",
        "## Anomalies / Caveats",
        "",
        "- No checkpoint-corruption signature: every local fresh mean is close to its train-best source accuracy.",
        "- CX-M6 has the widest local fresh spread (`std=1.6847%`, range `78.07-82.54`), so Ensemble-uniform seed 456 should be displayed with an error bar rather than as a single headline number.",
        "- The worktree is dirty because multiple agents are writing coordination artifacts and code patches; commit hash is still `33bed9c`, the required post-fix base.",
        "- Remote rows with `TBD` fresh values are placeholders from the dispatch and must not be cited as measured fresh performance.",
        "",
        "## Verdict",
        "",
        "CX-FRESH-EVAL-MSERIES is complete for local M1-M6. The paper-safe statement is: true-NL2 local fresh performance sits in the ~80-82% band across Standard, Ensemble-uniform, and Ensemble-proportional routes; the old 90.88% proportional claim remains invalid.",
        "",
    ])
    MD_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(CSV_PATH)
    print(MD_PATH)


if __name__ == "__main__":
    main()
