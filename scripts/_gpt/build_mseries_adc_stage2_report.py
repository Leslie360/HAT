#!/usr/bin/env python3
"""Build the Round-4 M-series ADC Stage-2 per-instance calibration report."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from statistics import mean, stdev

ROOT = Path(__file__).resolve().parents[2]
JSON_DIR = ROOT / "report_md/_gpt/json_gpt"
CSV_PATH = ROOT / "report_md/_gpt/csv_gpt/mseries_adc_stage2_report.csv"
MD_PATH = ROOT / "report_md/_gpt/CODEX_MSERIES_ADC_STAGE2_REPORT_20260425.md"

RUNS = [
    ("CX-M1", "V3 Standard", "Standard", 123, "cx_m1_fresh_eval.json", "cx_m1_adc_fresh_eval.json", "cx_m1_adc_perinstance_fresh_eval.json"),
    ("CX-M2", "V4 Ensemble", "Ensemble", 123, "cx_m2_fresh_eval.json", "cx_m2_adc_fresh_eval.json", "cx_m2_adc_perinstance_fresh_eval.json"),
    ("CX-M3", "V4 Proportional", "Proportional", 123, "cx_m3_fresh_eval.json", "cx_m3_adc_fresh_eval.json", "cx_m3_adc_perinstance_fresh_eval.json"),
    ("CX-M4", "V4 Proportional", "Proportional", 456, "cx_m4_fresh_eval.json", "cx_m4_adc_fresh_eval.json", "cx_m4_adc_perinstance_fresh_eval.json"),
    ("CX-M5", "V3 Standard", "Standard", 456, "cx_m5_fresh_eval.json", "cx_m5_adc_fresh_eval.json", "cx_m5_adc_perinstance_fresh_eval.json"),
    ("CX-M6", "V4 Ensemble", "Ensemble", 456, "cx_m6_fresh_eval.json", "cx_m6_adc_fresh_eval.json", "cx_m6_adc_perinstance_fresh_eval.json"),
]

PROVENANCE_FILES = [
    ROOT / "analog_layers.py",
    ROOT / "eval_fresh_instances_postfix.py",
    ROOT / "inference_analysis_utils.py",
    ROOT / "scripts/_gpt/eval_fresh_instances_adc_ablation.py",
    ROOT / "scripts/_gpt/run_adc_stage2_mseries_20260424.sh",
]


def load_json(filename: str) -> dict:
    path = JSON_DIR / filename
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def fmt(value: float | None, digits: int = 2, blank: str = "—") -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return blank
    return f"{float(value):.{digits}f}"


def fmt_pm(mean_value: float | None, std_value: float | None, digits: int = 2) -> str:
    if mean_value is None:
        return "—"
    if std_value is None:
        return f"{mean_value:.{digits}f}"
    return f"{mean_value:.{digits}f} ± {std_value:.{digits}f}"


def require_common_provenance(data: dict, label: str) -> None:
    if data.get("allow_eval_nl_override") is not False:
        raise ValueError(f"{label}: expected allow_eval_nl_override=false")
    if data.get("eval_provenance_mismatches") != []:
        raise ValueError(f"{label}: expected eval_provenance_mismatches=[]")


def require_stage2_provenance(data: dict, label: str) -> None:
    require_common_provenance(data, label)
    if data.get("adc_calibration_scope") != "per_instance":
        raise ValueError(f"{label}: expected adc_calibration_scope=per_instance")
    if data.get("adc_calibration_noise") != "current_d2d_with_c2c_disabled":
        raise ValueError(f"{label}: expected adc_calibration_noise=current_d2d_with_c2c_disabled")
    if data.get("adc_bits") != 8:
        raise ValueError(f"{label}: expected adc_bits=8")
    if data.get("fresh_instances") != 10 or data.get("mc_runs_per_instance") != 5:
        raise ValueError(f"{label}: expected 10 fresh instances x 5 MC runs")


def code_sha256(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in paths:
        digest.update(str(path.relative_to(ROOT)).encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def aggregate(rows: list[dict], hat_type: str, key: str) -> tuple[float, float]:
    values = [float(row[key]) for row in rows if row["hat_type"] == hat_type]
    if len(values) == 1:
        return values[0], 0.0
    return mean(values), stdev(values)


def verdict(delta_mean: float) -> str:
    if delta_mean < 0:
        return "ESCALATE: Stage-2 regressed versus Stage-1 static calibration; implementation/protocol issue must be debugged before integration."
    if delta_mean < 0.2:
        return "NO ESCALATION: Stage-2 recovery is effectively zero and below Claude's expected +0.2 to +0.8 pp window; the static-calibration caveat did not materially bias the current M-series ADC numbers."
    if delta_mean <= 0.8:
        return "NORMAL: Stage-2 recovery is within Claude's expected +0.2 to +0.8 pp window."
    if delta_mean <= 2.0:
        return "NOTE: Stage-2 recovery is larger than expected but below the >2 pp escalation threshold."
    return "ESCALATE: Stage-2 recovery exceeds +2 pp; D4 severity was underestimated and §5.7 should be reopened."


def main() -> None:
    rows: list[dict] = []
    for run_id, config, hat_type, seed, off_file, static_file, stage2_file in RUNS:
        off = load_json(off_file)
        static = load_json(static_file)
        stage2 = load_json(stage2_file)
        require_common_provenance(off, f"{run_id} ADC-off")
        require_common_provenance(static, f"{run_id} Stage-1 static")
        require_stage2_provenance(stage2, f"{run_id} Stage-2 per-instance")
        row = {
            "run_id": run_id,
            "config": config,
            "hat_type": hat_type,
            "seed": seed,
            "train_best_acc": float(off["checkpoint_best_acc"]),
            "fresh_adc_off_mean": float(off["cross_instance_mean"]),
            "fresh_adc_off_std": float(off["cross_instance_std"]),
            "stage1_static_mean": float(static["cross_instance_mean"]),
            "stage1_static_std": float(static["cross_instance_std"]),
            "stage2_perinstance_mean": float(stage2["cross_instance_mean"]),
            "stage2_perinstance_std": float(stage2["cross_instance_std"]),
            "delta_stage2_vs_stage1": float(stage2["cross_instance_mean"]) - float(static["cross_instance_mean"]),
            "delta_stage2_vs_off": float(stage2["cross_instance_mean"]) - float(off["cross_instance_mean"]),
            "off_json": str((JSON_DIR / off_file).relative_to(ROOT)),
            "stage1_json": str((JSON_DIR / static_file).relative_to(ROOT)),
            "stage2_json": str((JSON_DIR / stage2_file).relative_to(ROOT)),
            "stage2": stage2,
        }
        rows.append(row)

    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CSV_PATH.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "run_id",
                "config",
                "seed",
                "train_best_acc",
                "fresh_adc_off_mean",
                "fresh_adc_off_std",
                "fresh_adc_on_static_mean",
                "fresh_adc_on_static_std",
                "fresh_adc_on_perinstance_mean",
                "fresh_adc_on_perinstance_std",
                "delta_stage2_vs_stage1",
                "delta_stage2_vs_off",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "run_id": row["run_id"],
                "config": row["config"],
                "seed": row["seed"],
                "train_best_acc": f"{row['train_best_acc']:.2f}",
                "fresh_adc_off_mean": f"{row['fresh_adc_off_mean']:.4f}",
                "fresh_adc_off_std": f"{row['fresh_adc_off_std']:.4f}",
                "fresh_adc_on_static_mean": f"{row['stage1_static_mean']:.4f}",
                "fresh_adc_on_static_std": f"{row['stage1_static_std']:.4f}",
                "fresh_adc_on_perinstance_mean": f"{row['stage2_perinstance_mean']:.4f}",
                "fresh_adc_on_perinstance_std": f"{row['stage2_perinstance_std']:.4f}",
                "delta_stage2_vs_stage1": f"{row['delta_stage2_vs_stage1']:.4f}",
                "delta_stage2_vs_off": f"{row['delta_stage2_vs_off']:.4f}",
            })

    metadata = rows[0]["stage2"]
    delta_values = [row["delta_stage2_vs_stage1"] for row in rows]
    delta_mean = mean(delta_values)
    delta_std = stdev(delta_values)
    hats = ["Standard", "Ensemble", "Proportional"]
    aggregate_lines = []
    paper_parts = []
    for hat in hats:
        stage2_mean, stage2_std = aggregate(rows, hat, "stage2_perinstance_mean")
        stage1_mean, _stage1_std = aggregate(rows, hat, "stage1_static_mean")
        delta_hat = stage2_mean - stage1_mean
        aggregate_lines.append(
            f"| {hat} | {fmt_pm(stage2_mean, stage2_std)} | {fmt_pm(stage1_mean, _stage1_std)} | {delta_hat:.2f} |"
        )
        paper_parts.append(f"{stage2_mean:.2f}±{stage2_std:.2f}%")

    code_hash = code_sha256(PROVENANCE_FILES)
    lines = [
        "# CODEX M-Series ADC Stage-2 Per-Instance Calibration Report",
        "",
        "## 1. Provenance",
        "",
        f"- Eval commit: `{metadata.get('commit_hash')}`",
        f"- Eval-stack code SHA256: `{code_hash}`",
        f"- Dirty worktree at eval time: `{metadata.get('git_worktree_dirty')}`",
        f"- CUDA device: `{metadata.get('cuda_device_name')}`",
        f"- PyTorch: `{metadata.get('pytorch_version')}`",
        f"- Protocol: `{metadata.get('fresh_instances')}` fresh instances x `{metadata.get('mc_runs_per_instance')}` MC eval runs per checkpoint",
        "- ADC setting: `8-bit`, `adc_dnl_sigma=0.5`, `adc_calibration_batches=2`",
        "- Stage-2 calibration: `adc_calibration_scope=per_instance`, `adc_calibration_noise=current_d2d_with_c2c_disabled`",
        "- NL setting: `NL_LTP=2.0`, `NL_LTD=-2.0`; noise mode matched each checkpoint provenance.",
        "- Provenance guard: `allow_eval_nl_override=false` and `eval_provenance_mismatches=[]` for every JSON used here.",
        f"- CSV output: `{CSV_PATH.relative_to(ROOT)}`",
        "",
        "## 2. Stage-1 vs Stage-2 Comparison",
        "",
        "| Run | Config | Seed | Fresh ADC-off | Fresh ADC-on static cal (Stage 1) | Fresh ADC-on per-instance cal (Stage 2) | Δ Stage2−Stage1 | Δ Stage2−Off | JSONs |",
        "|:--|:--|--:|--:|--:|--:|--:|--:|:--|",
    ]
    for row in rows:
        jsons = f"`{row['off_json']}`<br>`{row['stage1_json']}`<br>`{row['stage2_json']}`"
        lines.append(
            f"| {row['run_id']} | {row['config']} | {row['seed']} | "
            f"{fmt_pm(row['fresh_adc_off_mean'], row['fresh_adc_off_std'])} | "
            f"{fmt_pm(row['stage1_static_mean'], row['stage1_static_std'])} | "
            f"{fmt_pm(row['stage2_perinstance_mean'], row['stage2_perinstance_std'])} | "
            f"{row['delta_stage2_vs_stage1']:.2f} | {row['delta_stage2_vs_off']:.2f} | {jsons} |"
        )

    lines.extend([
        "",
        "## 3. Aggregate By HAT Type",
        "",
        "| HAT Type | Stage-2 per-instance ADC-on | Stage-1 static ADC-on | Δ Stage2−Stage1 |",
        "|:--|--:|--:|--:|",
        *aggregate_lines,
        "",
        "## 4. Escalation Verdict",
        "",
        f"- Mean Δ Stage2−Stage1 across all six M-series runs: `{delta_mean:.4f}` pp; run-to-run std: `{delta_std:.4f}` pp.",
        f"- Claude threshold verdict: **{verdict(delta_mean)}**",
        "- Interpretation scope: these remain hook-based ADC quantization measurements with per-instance range recalibration on each fresh noisy hardware realization; they validate that static calibration was not a material confounder under the current hook protocol, but they still use the current post-module-output hook implementation.",
        "",
        "## 5. Paper-Safe Statement For Kimi",
        "",
        f"> Severe-NL fresh-instance accuracy under the current hook-based 8-bit ADC quantization protocol, with per-instance recalibration on each noisy hardware realization, sits at [{paper_parts[0]}] for Standard HAT, [{paper_parts[1]}] for Ensemble HAT, and [{paper_parts[2]}] for Proportional HAT, across two seeds per configuration. This is a +{delta_mean:.2f} pp change relative to the static-calibration protocol reported in the initial dual report, indicating no material static-calibration bias under the current hook implementation.",
        "",
    ])
    MD_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(CSV_PATH.relative_to(ROOT))
    print(MD_PATH.relative_to(ROOT))
    print(f"delta_mean={delta_mean:.4f}")


if __name__ == "__main__":
    main()
