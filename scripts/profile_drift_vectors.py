#!/usr/bin/env python3
"""Drift-vector profiling for current analog retention model."""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "compute_vit"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from inference_analysis_utils import iter_analog_modules, load_model_bundle
from analog_layers import _retention_decay_factor


def parse_float_list(text: str) -> list[float]:
    return [float(item.strip()) for item in text.split(",") if item.strip()]


def corrcoef(x: np.ndarray, y: np.ndarray) -> float:
    if x.size < 2 or y.size < 2:
        return float("nan")
    if float(np.std(x)) == 0.0 or float(np.std(y)) == 0.0:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def tensor_stats(t: torch.Tensor) -> dict[str, float]:
    flat = t.detach().float().reshape(-1)
    return {
        "mean": float(flat.mean().item()),
        "std": float(flat.std(unbiased=False).item()),
        "l2": float(torch.linalg.vector_norm(flat).item()),
        "linf": float(flat.abs().max().item()),
    }


def conductance_pair(module):
    with torch.no_grad():
        return module._weight_to_conductance(module.weight)


def run(args):
    times = parse_float_list(args.times)
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
        amp_enabled=False,
    )
    rows = []
    layer_summaries = []
    print(
        f"loaded {bundle.model_type} {bundle.experiment} {bundle.experiment_name} "
        f"checkpoint={bundle.checkpoint_path} dataset={bundle.dataset}",
        flush=True,
    )
    for layer_index, (name, module) in enumerate(iter_analog_modules(bundle.model), start=1):
        cfg = module.config
        cfg.retention_state_dependent = bool(args.state_dependent)
        base_pos, base_neg = conductance_pair(module)
        base_eff = (base_pos - base_neg).detach().float()
        weight_abs = module.weight.detach().float().abs().reshape(-1).cpu().numpy()
        base_eff_abs = base_eff.abs().reshape(-1).cpu().numpy()
        for retention_time in times:
            cfg.retention_enabled = retention_time > 0
            cfg.inference_time = retention_time
            if cfg.retention_state_dependent:
                decay_pos = _retention_decay_factor(cfg, base_pos)
                decay_neg = _retention_decay_factor(cfg, base_neg)
                drift_pos = base_pos * decay_pos - base_pos
                drift_neg = base_neg * decay_neg - base_neg
            else:
                decay = _retention_decay_factor(cfg)
                drift_pos = base_pos * decay - base_pos
                drift_neg = base_neg * decay - base_neg
            drift_eff = (drift_pos - drift_neg).detach().float()
            drift_abs = drift_eff.abs().reshape(-1).cpu().numpy()
            pos_stats = tensor_stats(drift_pos)
            neg_stats = tensor_stats(drift_neg)
            eff_stats = tensor_stats(drift_eff)
            row = {
                "dataset": bundle.dataset,
                "model_type": bundle.model_type,
                "experiment": bundle.experiment,
                "experiment_name": bundle.experiment_name,
                "checkpoint": bundle.checkpoint_path,
                "module_path": name,
                "layer_index": layer_index,
                "layer_type": module.__class__.__name__,
                "retention_time_s": retention_time,
                "tau_1": float(cfg.tau_1),
                "tau_2": float(cfg.tau_2),
                "A_0": float(cfg.A_0),
                "retention_state_dependent": bool(cfg.retention_state_dependent),
                "retention_decay_factor_scalar": float(_retention_decay_factor(cfg)) if not cfg.retention_state_dependent else "state_dependent",
                "weight_abs_mean": float(np.mean(weight_abs)),
                "base_effective_abs_mean": float(np.mean(base_eff_abs)),
                "drift_pos_mean": pos_stats["mean"],
                "drift_pos_l2": pos_stats["l2"],
                "drift_neg_mean": neg_stats["mean"],
                "drift_neg_l2": neg_stats["l2"],
                "drift_effective_mean": eff_stats["mean"],
                "drift_effective_std": eff_stats["std"],
                "drift_effective_l2": eff_stats["l2"],
                "drift_effective_linf": eff_stats["linf"],
                "drift_abs_to_weight_abs_corr": corrcoef(drift_abs, weight_abs),
                "drift_abs_to_base_effective_abs_corr": corrcoef(drift_abs, base_eff_abs),
                "script": "scripts/profile_drift_vectors.py",
                "evidence_grade": "drift-vector-profile/provisional-model-only",
            }
            rows.append(row)
            print("RESULT " + json.dumps(row), flush=True)
        layer_summaries.append({
            "module_path": name,
            "layer_index": layer_index,
            "layer_type": module.__class__.__name__,
            "num_parameters": int(module.weight.numel()),
            "weight_abs_mean": float(np.mean(weight_abs)),
            "base_effective_abs_mean": float(np.mean(base_eff_abs)),
        })

    Path(args.tsv_out).parent.mkdir(parents=True, exist_ok=True)
    with Path(args.tsv_out).open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)
    with Path(args.json_out).open("w", encoding="utf-8") as fh:
        json.dump({
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "times": times,
            "model_type": bundle.model_type,
            "experiment": bundle.experiment,
            "checkpoint": bundle.checkpoint_path,
            "layer_count": len(layer_summaries),
            "layers": layer_summaries,
            "note": "Current simulator retention model only; not measured device drift.",
        }, fh, indent=2)
    print(f"TSV: {args.tsv_out}", flush=True)
    print(f"JSON: {args.json_out}", flush=True)


def main():
    stamp = time.strftime("%Y%m%d_%H%M%S")
    out_dir = ROOT / "thesis" / "results" / "drift_aware_sam"
    parser = argparse.ArgumentParser(description="Profile analog retention drift vectors")
    parser.add_argument("--model_type", default="tinyvit")
    parser.add_argument("--experiment", default="V4")
    parser.add_argument("--dataset", default="cifar100")
    parser.add_argument("--checkpoint_path", default=str(ROOT / "checkpoints" / "_ensemble" / "cifar100_seed789" / "V4_hybrid_standard_noise_hat_best.pt"))
    parser.add_argument("--checkpoint_dir", default=str(ROOT / "checkpoints"))
    parser.add_argument("--data_root", default=str(ROOT / "data"))
    parser.add_argument("--batch_size", type=int, default=128)
    parser.add_argument("--num_workers", type=int, default=0)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--times", default="0,1000,10000,86400")
    parser.add_argument("--state-dependent", action="store_true")
    parser.add_argument("--tsv_out", default=str(out_dir / f"drift_vectors_profile_{stamp}.tsv"))
    parser.add_argument("--json_out", default=str(out_dir / f"drift_vectors_profile_{stamp}.json"))
    args = parser.parse_args()
    # Toggle retention law before profiling.
    # This affects every analog layer through the loaded checkpoint config.
    run(args)


if __name__ == "__main__":
    main()
