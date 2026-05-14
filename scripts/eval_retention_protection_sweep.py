#!/usr/bin/env python3
"""Retention × D2D-protection pilot for CIFAR fresh-instance evaluations."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path
from statistics import mean, stdev

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "compute_vit"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from amp_utils import autocast_context
from inference_analysis_utils import iter_analog_modules, load_model_bundle, set_uniform_noise, set_uniform_retention


def load_layer_sensitivity(path: Path, k_values: list[int]) -> dict[int, set[str]]:
    rows = []
    with path.open("r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        for row in reader:
            if row.get("module_path"):
                rows.append(row)
    rows.sort(key=lambda row: int(row.get("rank", len(rows) + 1)))
    layer_names = [row["module_path"] for row in rows]
    return {k: set(layer_names[:k]) for k in k_values}


def snapshot_d2d_buffers(model):
    return {name: module.d2d_noise.detach().clone() for name, module in iter_analog_modules(model)}


def restore_protected_d2d_buffers(model, checkpoint_d2d_buffers, protected_set: set[str]):
    for name, module in iter_analog_modules(model):
        if name in protected_set:
            module.d2d_noise.copy_(checkpoint_d2d_buffers[name])


def evaluate_current(bundle):
    bundle.model.eval()
    loss_sum = 0.0
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, targets in bundle.testloader:
            inputs = inputs.to(bundle.device)
            targets = targets.to(bundle.device)
            if bundle.frontend is not None:
                inputs = bundle.frontend(inputs, mode="compensated")
            with autocast_context(bundle.device, bundle.amp_enabled):
                outputs = bundle.model(inputs)
                loss = bundle.criterion(outputs, targets)
            loss_sum += loss.item() * inputs.size(0)
            correct += outputs.argmax(dim=1).eq(targets).sum().item()
            total += targets.size(0)
    return loss_sum / total, 100.0 * correct / total


def write_tsv_row(path: Path, row: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    write_header = not path.exists() or path.stat().st_size == 0
    with path.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(row.keys()), delimiter="\t")
        if write_header:
            writer.writeheader()
        writer.writerow(row)


def summarize(rows: list[dict]) -> list[dict]:
    per_instance: dict[tuple[str, int, float, int], list[float]] = {}
    for row in rows:
        key = (
            row["strategy"],
            row["protected_k"],
            row["retention_time_s"],
            row["instance_index"],
        )
        per_instance.setdefault(key, []).append(row["accuracy"])

    grouped: dict[tuple[str, int, float], list[float]] = {}
    for (strategy, protected_k, retention_time, _instance_idx), values in per_instance.items():
        grouped.setdefault((strategy, protected_k, retention_time), []).append(mean(values))

    out = []
    for (strategy, protected_k, retention_time), values in sorted(grouped.items(), key=lambda item: (item[0][2], item[0][1])):
        out.append({
            "strategy": strategy,
            "protected_k": protected_k,
            "retention_time_s": retention_time,
            "accuracy_mean": round(mean(values), 4),
            "accuracy_std": round(stdev(values), 4) if len(values) > 1 else 0.0,
            "accuracy_min": round(min(values), 4),
            "accuracy_max": round(max(values), 4),
            "instance_count": len(values),
        })
    return out


def write_tsv(path: Path, rows: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def parse_int_list(text: str) -> list[int]:
    return [int(item.strip()) for item in text.split(",") if item.strip()]


def parse_float_list(text: str) -> list[float]:
    return [float(item.strip()) for item in text.split(",") if item.strip()]


def run(args):
    k_values = parse_int_list(args.k_values)
    retention_times = parse_float_list(args.retention_times)
    protected_layers = load_layer_sensitivity(Path(args.sensitivity_tsv), k_values)
    bundle = load_model_bundle(
        model_type=args.model_type,
        experiment=args.experiment,
        device=args.device,
        checkpoint_path=args.checkpoint_path,
        checkpoint_dir=args.checkpoint_dir,
        dataset=args.dataset,
        data_root=args.data_root,
        num_workers=args.num_workers,
        batch_size=args.batch_size,
        amp_enabled=args.amp,
    )
    checkpoint_d2d_buffers = snapshot_d2d_buffers(bundle.model)
    rows = []
    print(
        f"loaded model analog_layers {len(checkpoint_d2d_buffers)} test_size {len(bundle.testloader.dataset)} "
        f"k_values {k_values} retention_times {retention_times} "
        f"recalibrate_scale {args.recalibrate_scale} scale_d2d {args.scale_d2d}",
        flush=True,
    )

    for instance_idx in range(1, args.num_instances + 1):
        instance_seed = args.base_seed + (instance_idx - 1) * 100_000
        torch.manual_seed(instance_seed)
        np.random.seed(instance_seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(instance_seed)
        set_uniform_noise(
            bundle.model,
            sigma_c2c=bundle.exp_cfg.sigma_c2c,
            sigma_d2d=bundle.exp_cfg.sigma_d2d,
            noise_enabled=bundle.exp_cfg.noise_enabled,
            resample_d2d=True,
            noise_mode=getattr(bundle.exp_cfg, "noise_mode", "uniform"),
        )
        fresh_d2d_buffers = snapshot_d2d_buffers(bundle.model)

        for protected_k in k_values:
            protected_set = protected_layers[protected_k]
            strategy = "fresh_all_analog" if protected_k == 0 else f"freeze_top{protected_k}_d2d"
            for name, module in iter_analog_modules(bundle.model):
                module.d2d_noise.copy_(fresh_d2d_buffers[name])
            restore_protected_d2d_buffers(bundle.model, checkpoint_d2d_buffers, protected_set)

            for retention_time in retention_times:
                set_uniform_retention(
                    bundle.model,
                    inference_time=retention_time,
                    state_dependent=args.state_dependent_retention,
                    recalibrate_scale=args.recalibrate_scale,
                    scale_d2d=args.scale_d2d,
                )
                for mc_idx in range(1, args.mc_runs + 1):
                    mc_seed = instance_seed + int(retention_time) + mc_idx
                    torch.manual_seed(mc_seed)
                    np.random.seed(mc_seed)
                    if torch.cuda.is_available():
                        torch.cuda.manual_seed_all(mc_seed)
                    print(
                        f"strategy {strategy} retention {retention_time:g}s instance {instance_idx} mc {mc_idx}",
                        flush=True,
                    )
                    t0 = time.perf_counter()
                    loss, acc = evaluate_current(bundle)
                    elapsed = time.perf_counter() - t0
                    row = {
                        "dataset": args.dataset,
                        "experiment": args.experiment,
                        "checkpoint": bundle.checkpoint_path,
                        "strategy": strategy,
                        "protected_k": protected_k,
                        "retention_time_s": retention_time,
                        "retention_state_dependent": args.state_dependent_retention,
                        "retention_recalibrate_scale": args.recalibrate_scale,
                        "retention_scales_d2d": args.scale_d2d,
                        "instance_index": instance_idx,
                        "instance_seed": instance_seed,
                        "mc_index": mc_idx,
                        "mc_seed": mc_seed,
                        "accuracy": round(acc, 4),
                        "loss": round(loss, 6),
                        "elapsed_seconds": round(elapsed, 3),
                        "sigma_c2c": bundle.exp_cfg.sigma_c2c,
                        "sigma_d2d": bundle.exp_cfg.sigma_d2d,
                        "noise_mode": getattr(bundle.exp_cfg, "noise_mode", "uniform"),
                        "script": "scripts/eval_retention_protection_sweep.py",
                        "evidence_grade": f"retention-protection-pilot-n{args.num_instances}-mc{args.mc_runs}",
                    }
                    print(f"RESULT {json.dumps(row)}", flush=True)
                    rows.append(row)
                    write_tsv_row(Path(args.tsv_out), row)

    summary_rows = summarize(rows)
    write_tsv(Path(args.summary_out), summary_rows)
    print(f"Raw results: {args.tsv_out}", flush=True)
    print(f"Summary: {args.summary_out}", flush=True)


def main():
    stamp = time.strftime("%Y%m%d_%H%M%S")
    out_dir = ROOT / "thesis" / "results" / "retention_protection"
    parser = argparse.ArgumentParser(description="Retention × protection pilot")
    parser.add_argument("--model_type", default="tinyvit")
    parser.add_argument("--experiment", default="V4")
    parser.add_argument("--dataset", default="cifar100")
    parser.add_argument("--checkpoint_path", default=None)
    parser.add_argument("--checkpoint_dir", default=str(ROOT / "checkpoints"))
    parser.add_argument("--sensitivity_tsv", required=True)
    parser.add_argument("--k_values", default="0,30,42")
    parser.add_argument("--retention_times", default="0,1000,10000")
    parser.add_argument("--num_instances", type=int, default=3)
    parser.add_argument("--mc_runs", type=int, default=2)
    parser.add_argument("--batch_size", type=int, default=128)
    parser.add_argument("--num_workers", type=int, default=4)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--data_root", default=str(ROOT / "data"))
    parser.add_argument("--base_seed", type=int, default=20260515)
    parser.add_argument("--amp", action="store_true")
    parser.add_argument("--state-dependent-retention", action="store_true")
    parser.add_argument("--recalibrate_scale", action="store_true")
    parser.add_argument("--scale_d2d", action="store_true")
    parser.add_argument("--tsv_out", default=str(out_dir / f"retention_protection_pilot_{stamp}.tsv"))
    parser.add_argument("--summary_out", default=str(out_dir / f"retention_protection_pilot_summary_{stamp}.tsv"))
    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
