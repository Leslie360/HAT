#!/usr/bin/env python3
"""Evaluate one or more measured device profiles against a checkpoint."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
import re
from typing import List, Sequence

import torch
from torch.utils.data import DataLoader, Subset

from device_profile_utils import load_device_profiles_json, profile_to_payload, select_device_profile
from inference_analysis_utils import (
    apply_device_profile,
    load_model_bundle,
    restore_analog_state,
    run_mc_eval,
    snapshot_analog_state,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate measured-device profiles on a checkpoint.")
    parser.add_argument("--profile-json", type=str, default="report_md/_gpt/json_gpt/measured_device_profiles.json")
    parser.add_argument("--profile-audit-json", type=str, default=None)
    parser.add_argument("--profile-name", type=str, default=None)
    parser.add_argument("--model-type", type=str, choices=["tinyvit", "convnext"], default="tinyvit")
    parser.add_argument("--experiment", type=str, default="V4")
    parser.add_argument("--dataset", type=str, default="cifar10")
    parser.add_argument("--data-root", type=str, default="./data")
    parser.add_argument("--checkpoint-dir", type=str, default="checkpoints")
    parser.add_argument("--checkpoint-path", type=str, default=None)
    parser.add_argument("--device", type=str, default=None)
    parser.add_argument("--num-workers", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=None)
    parser.add_argument("--eval-runs", type=int, default=1)
    parser.add_argument("--amp", action="store_true")
    parser.add_argument("--max-samples", type=int, default=None)
    parser.add_argument("--output", type=str, default="report_md/_gpt/measured_profile_eval.json")
    parser.add_argument("--bundle-dir", type=str, default=None)
    return parser.parse_args()


def subset_testloader(bundle, max_samples: int | None, num_workers: int):
    if not max_samples:
        return bundle.testloader
    dataset = bundle.testloader.dataset
    max_samples = min(int(max_samples), len(dataset))
    subset = Subset(dataset, list(range(max_samples)))
    return DataLoader(
        subset,
        batch_size=bundle.testloader.batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=getattr(bundle.testloader, "pin_memory", False),
    )


def evaluate_profiles(bundle, profiles: Sequence, eval_runs: int) -> List[dict]:
    rows: List[dict] = []
    snapshot = snapshot_analog_state(bundle.model)
    try:
        for profile in profiles:
            apply_device_profile(bundle.model, profile, resample_d2d=True)
            summary = run_mc_eval(bundle, eval_runs=eval_runs)
            row = {
                "model": bundle.model_type,
                "experiment": bundle.experiment,
                "dataset": bundle.dataset,
                "checkpoint_path": bundle.checkpoint_path,
                "checkpoint_best_acc": bundle.checkpoint_best_acc,
                "device_type": profile.device_type,
                "profile_kind": profile.profile_kind,
                "source": profile.source,
                "dynamic_range": profile.dynamic_range,
                "G_min": profile.G_min,
                "G_max": profile.G_max,
                "n_states": profile.n_states,
                "sigma_c2c": profile.sigma_c2c,
                "sigma_d2d": profile.sigma_d2d,
                "tau_1": profile.tau_1,
                "tau_2": profile.tau_2,
                "A_0": profile.A_0,
                "gamma_phys": profile.gamma_phys,
                "I_dark": profile.I_dark,
                "responsivity_alpha": profile.responsivity_alpha,
                "NL_LTP": profile.NL_LTP,
                "NL_LTD": profile.NL_LTD,
                "pulse_count_max": profile.pulse_count_max,
                "max_samples": len(bundle.testloader.dataset),
            }
            row.update(summary)
            rows.append(row)
    finally:
        restore_analog_state(bundle.model, snapshot)
    return rows


def infer_profile_audit_json(profile_json_path: Path) -> Path | None:
    candidates = []
    name = profile_json_path.name
    if name.endswith("_profiles.json"):
        candidates.append(profile_json_path.with_name(name.replace("_profiles.json", "_profile_summary.json")))
    if "profiles.json" in name:
        candidates.append(profile_json_path.with_name(name.replace("profiles.json", "profile_summary.json")))
    candidates.append(profile_json_path.with_name(f"{profile_json_path.stem}_summary.json"))
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def load_optional_json(path: Path | None) -> dict | None:
    if path is None or not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def sanitize_token(text: str) -> str:
    token = re.sub(r"[^A-Za-z0-9._-]+", "_", str(text).strip())
    token = token.strip("._")
    return token or "run"


def infer_bundle_dir(args: argparse.Namespace, out_path: Path, checkpoint_path: str | None) -> Path:
    if args.bundle_dir:
        return Path(args.bundle_dir)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    checkpoint_token = sanitize_token(Path(checkpoint_path).stem if checkpoint_path else out_path.stem)
    run_name = "_".join(
        [
            ts,
            sanitize_token(args.model_type),
            sanitize_token(args.experiment),
            sanitize_token(args.dataset),
            checkpoint_token,
        ]
    )
    return Path("outputs") / "measured_profile_runs" / run_name


def write_metrics_csv(path: Path, rows: Sequence[dict]) -> None:
    fields = [
        "device_type",
        "profile_kind",
        "checkpoint_path",
        "checkpoint_best_acc",
        "test_acc_mean",
        "test_acc_std",
        "test_loss_mean",
        "dynamic_range",
        "n_states",
        "sigma_c2c",
        "sigma_d2d",
        "tau_1",
        "tau_2",
        "A_0",
        "gamma_phys",
        "I_dark",
        "responsivity_alpha",
        "NL_LTP",
        "NL_LTD",
        "pulse_count_max",
        "max_samples",
        "eval_runs",
    ]
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fields})


def render_manifest_section(audit_payload: dict | None) -> List[str]:
    if not audit_payload:
        return [
            "## Input Coverage",
            "",
            "No profile audit JSON was available, so this bundle cannot classify inputs into used / archived-only / unresolved.",
            "",
        ]

    diagnostics = audit_payload.get("diagnostics", {})
    manifest = diagnostics.get("input_manifest")
    if not isinstance(manifest, list) or not manifest:
        return [
            "## Input Coverage",
            "",
            "Profile audit JSON was present, but it did not expose a structured `input_manifest`.",
            "",
        ]

    lines = ["## Input Coverage", ""]
    for status, title in (
        ("used", "Used Inputs"),
        ("archived_only", "Archived-Only Inputs"),
        ("unresolved", "Unresolved Inputs"),
    ):
        items = [item for item in manifest if item.get("status") == status]
        if not items:
            continue
        lines.extend([
            f"### {title}",
            "",
            "| Path | Role | Note |",
            "|:--|:--|:--|",
        ])
        for item in items:
            lines.append(
                f"| `{item.get('path', '')}` | {item.get('role', '')} | {item.get('note', '')} |"
            )
        lines.append("")
    return lines


def write_run_summary(
    path: Path,
    payload: dict,
    rows: Sequence[dict],
    profiles: Sequence,
    audit_payload: dict | None,
    bundle_dir: Path,
    out_path: Path,
    metrics_csv_path: Path,
    used_profiles_path: Path,
    audit_copy_path: Path | None,
) -> None:
    best = max(rows, key=lambda row: row.get("test_acc_mean", float("-inf")))
    worst = min(rows, key=lambda row: row.get("test_acc_mean", float("inf")))
    show_gap = payload.get("requested_max_samples") in (None, 0)
    lines = [
        "# Measured Profile Run Summary",
        "",
        "## Bottom Line",
        "",
        f"- Profiles evaluated: `{len(rows)}`",
        f"- Best result: `{best['device_type']}` -> `{best['test_acc_mean']:.2f}%`",
        f"- Worst result: `{worst['device_type']}` -> `{worst['test_acc_mean']:.2f}%`",
        f"- Checkpoint: `{rows[0]['checkpoint_path']}`",
        f"- Bundle directory: `{bundle_dir.resolve()}`",
        "",
        "## Run Context",
        "",
        f"- Generated at: `{payload['generated_at']}`",
        f"- Device: `{payload['device']}`",
        f"- Model: `{rows[0]['model']}`",
        f"- Experiment: `{rows[0]['experiment']}`",
        f"- Dataset: `{rows[0]['dataset']}`",
        f"- Evaluation samples: `{payload.get('eval_dataset_size')}`",
        f"- Requested max samples: `{payload.get('requested_max_samples')}`",
        f"- Profile JSON: `{payload['profile_json']}`",
        f"- Results JSON: `{out_path.resolve()}`",
        "",
        "## Evaluation Table",
        "",
        f"| Profile | Kind | Acc mean (%) | Acc std (%) | Loss | {'Gap vs ckpt best (pp)' if show_gap else 'Checkpoint comparison'} | Range | States | sigma_c2c | sigma_d2d |",
        "|:--|:--|--:|--:|--:|--:|--:|--:|--:|--:|",
    ]
    for row in rows:
        gap = None
        if row.get("checkpoint_best_acc") is not None and row.get("test_acc_mean") is not None:
            gap = float(row["checkpoint_best_acc"]) - float(row["test_acc_mean"])
        gap_text = "subset run; compare cautiously"
        if show_gap:
            gap_text = "n/a" if gap is None else f"{gap:.2f}"
        lines.append(
            f"| {row['device_type']} | {row['profile_kind']} | {row['test_acc_mean']:.2f} | "
            f"{row['test_acc_std']:.2f} | {row['test_loss_mean']:.4f} | "
            f"{gap_text} | {row['dynamic_range']:.2f}x | "
            f"{row['n_states']} | {row['sigma_c2c']:.4f} | {row['sigma_d2d']:.4f} |"
        )
    lines.extend([
        "",
        "## Profile Parameters",
        "",
        "| Profile | tau_1 | tau_2 | A_0 | gamma_phys | I_dark | responsivity_alpha | NL_LTP | NL_LTD | pulse_count_max |",
        "|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|",
    ])
    for row in rows:
        def fmt(value, spec=".4g"):
            return "n/a" if value is None else format(value, spec)
        lines.append(
            f"| {row['device_type']} | {fmt(row.get('tau_1'))} | {fmt(row.get('tau_2'))} | "
            f"{fmt(row.get('A_0'))} | {fmt(row.get('gamma_phys'))} | {fmt(row.get('I_dark'))} | "
            f"{fmt(row.get('responsivity_alpha'))} | {fmt(row.get('NL_LTP'))} | "
            f"{fmt(row.get('NL_LTD'))} | {fmt(row.get('pulse_count_max'), '.0f')} |"
        )
    lines.extend([""])
    lines.extend(render_manifest_section(audit_payload))
    lines.extend([
        "## Artifacts",
        "",
        f"- Results JSON: `{out_path.resolve()}`",
        f"- Bundle-local results JSON: `{(bundle_dir / 'results.json').resolve()}`",
        f"- Metrics CSV: `{metrics_csv_path.resolve()}`",
        f"- Profiles used JSON: `{used_profiles_path.resolve()}`",
    ])
    if audit_copy_path is not None:
        lines.append(f"- Profile audit snapshot: `{audit_copy_path.resolve()}`")
    lines.extend([
        "",
        "## User Read Path",
        "",
        "- Start with this `run_summary.md`.",
        "- Use `metrics.csv` for quick comparison across runs.",
        "- Use `profiles_used.json` as the exact machine-readable profile payload applied during this run.",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_bundle(
    args: argparse.Namespace,
    payload: dict,
    rows: Sequence[dict],
    profiles: Sequence,
    out_path: Path,
    checkpoint_path: str | None,
) -> Path:
    profile_json_path = Path(args.profile_json)
    audit_json_path = Path(args.profile_audit_json) if args.profile_audit_json else infer_profile_audit_json(profile_json_path)
    audit_payload = load_optional_json(audit_json_path)

    bundle_dir = infer_bundle_dir(args, out_path, checkpoint_path)
    bundle_dir.mkdir(parents=True, exist_ok=True)

    bundle_results_path = bundle_dir / "results.json"
    bundle_results_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    metrics_csv_path = bundle_dir / "metrics.csv"
    write_metrics_csv(metrics_csv_path, rows)

    used_profiles_path = bundle_dir / "profiles_used.json"
    used_profiles_path.write_text(
        json.dumps(
            {
                "source": str(profile_json_path),
                "profiles": [profile_to_payload(profile) for profile in profiles],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    audit_copy_path = None
    if audit_payload is not None and audit_json_path is not None:
        audit_copy_path = bundle_dir / "profile_audit.json"
        audit_copy_path.write_text(json.dumps(audit_payload, indent=2) + "\n", encoding="utf-8")

    write_run_summary(
        path=bundle_dir / "run_summary.md",
        payload=payload,
        rows=rows,
        profiles=profiles,
        audit_payload=audit_payload,
        bundle_dir=bundle_dir,
        out_path=out_path,
        metrics_csv_path=metrics_csv_path,
        used_profiles_path=used_profiles_path,
        audit_copy_path=audit_copy_path,
    )
    return bundle_dir


def main() -> None:
    args = parse_args()
    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")
    profiles = load_device_profiles_json(args.profile_json)
    if args.profile_name is not None:
        profiles = [select_device_profile(profiles, args.profile_name)]

    bundle = load_model_bundle(
        model_type=args.model_type,
        experiment=args.experiment,
        device=device,
        dataset=args.dataset,
        data_root=args.data_root,
        checkpoint_path=args.checkpoint_path,
        checkpoint_dir=args.checkpoint_dir,
        num_workers=args.num_workers,
        batch_size=args.batch_size,
        amp_enabled=args.amp,
    )
    bundle.testloader = subset_testloader(bundle, args.max_samples, args.num_workers)
    rows = evaluate_profiles(bundle, profiles, args.eval_runs)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "device": device,
        "profile_json": args.profile_json,
        "profile_audit_json": args.profile_audit_json,
        "requested_max_samples": args.max_samples,
        "eval_dataset_size": len(bundle.testloader.dataset),
        "results": rows,
    }
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    bundle_dir = write_bundle(args, payload, rows, profiles, out_path, bundle.checkpoint_path)
    for row in rows:
        print(
            f"{row['device_type']}: acc={row['test_acc_mean']:.2f}% ± {row['test_acc_std']:.2f} "
            f"(n_states={row['n_states']}, G_range={row['dynamic_range']:.2f}x, "
            f"sigma_c2c={row['sigma_c2c']:.4f}, sigma_d2d={row['sigma_d2d']:.4f})"
        )
    print(f"Saved evaluation payload to {out_path}")
    print(f"Saved user-facing result bundle to {bundle_dir}")


if __name__ == "__main__":
    main()
