#!/usr/bin/env python3
"""Evaluate canonical Ensemble HAT under spatially correlated D2D mismatch.

This closes Round J / CX-CA by reusing the same fresh-instance protocol already
used for the standard-HAT no-AMP rerun and the severe-NL control sweeps:

- 10 fresh D2D instances
- 5 Monte Carlo evaluations per instance
- CIFAR-10 Tiny-ViT V4 Ensemble HAT checkpoint

The only change is the D2D sampling law. After sampling a fresh i.i.d. D2D map
for each analog layer, we optionally transform it into a separable 2D AR(1)
field with coefficient ``rho`` while preserving zero mean and the original
standard deviation. This gives a lightweight spatial-correlation stress test
without changing the paper-locked checkpoint or evaluation harness.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import math
from datetime import datetime
from pathlib import Path
from statistics import mean, stdev
from typing import Dict, Iterable, List, Tuple
import sys

import torch
import torch.nn as nn

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from repo_bootstrap import ensure_repo_root
from train_tinyvit import set_seed
from train_tinyvit_ensemble import (
    TinyViTExperimentConfig,
    build_model,
    evaluate,
    get_dataloaders,
    resample_all_d2d_noise,
)

ensure_repo_root()


DEFAULT_CKPT = "checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt"
DEFAULT_JSON = "report_md/_gpt/json_gpt/fresh_instance_eval_v4_ensemble_correlated_d2d.json"
DEFAULT_MD = "report_md/_gpt/CODEX_S1_CORRELATED_D2D_20260420.md"


def _ar1_1d(x: torch.Tensor, rho: float) -> torch.Tensor:
    if x.numel() <= 1 or rho <= 0:
        return x.clone()
    alpha = math.sqrt(max(1.0 - rho * rho, 1e-8))
    out = x.clone()
    for idx in range(1, out.numel()):
        out[idx] = rho * out[idx - 1] + alpha * out[idx]
    return out


def _ar1_2d(field: torch.Tensor, rho: float) -> torch.Tensor:
    if field.ndim != 2:
        raise ValueError(f"_ar1_2d expects a 2D tensor, got shape={tuple(field.shape)}")
    if rho <= 0:
        return field.clone()

    alpha = math.sqrt(max(1.0 - rho * rho, 1e-8))
    out = field.clone()

    for row in range(1, out.shape[0]):
        out[row, :] = rho * out[row - 1, :] + alpha * out[row, :]

    for col in range(1, out.shape[1]):
        out[:, col] = rho * out[:, col - 1] + alpha * out[:, col]

    return out


def correlate_d2d_tensor(noise: torch.Tensor, rho: float) -> torch.Tensor:
    """Apply a simple separable AR(1) correlation model and preserve variance."""
    if rho <= 0:
        return noise.clone()

    orig_shape = noise.shape
    flat = noise.reshape(orig_shape[0], -1) if noise.ndim >= 2 else noise.reshape(-1)
    orig_std = flat.float().std(unbiased=False)

    if flat.ndim == 1:
        corr = _ar1_1d(flat, rho)
    else:
        corr = _ar1_2d(flat, rho)

    corr = corr - corr.mean()
    corr_std = corr.float().std(unbiased=False)
    if corr_std > 1e-8 and orig_std > 0:
        corr = corr * (orig_std / corr_std)

    return corr.reshape(orig_shape).to(dtype=noise.dtype, device=noise.device)


def apply_correlated_d2d_buffers(model: nn.Module, rho: float) -> int:
    count = 0
    with torch.no_grad():
        for module in model.modules():
            if not hasattr(module, "d2d_noise"):
                continue
            d2d = getattr(module, "d2d_noise")
            if not isinstance(d2d, torch.Tensor):
                continue
            module.d2d_noise.copy_(correlate_d2d_tensor(module.d2d_noise, rho))
            count += 1
    return count


def cfg_from_checkpoint(checkpoint_path: str) -> TinyViTExperimentConfig:
    ckpt = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    exp_cfg_dict = ckpt.get("exp_cfg", {})
    valid_keys = {f.name for f in dataclasses.fields(TinyViTExperimentConfig)}
    filtered = {k: v for k, v in exp_cfg_dict.items() if k in valid_keys}
    return TinyViTExperimentConfig(**filtered)


def evaluate_fresh_instances_correlated(
    checkpoint_path: str,
    device: str,
    fresh_instances: int,
    eval_runs: int,
    data_root: str,
    num_workers: int,
    rho: float,
) -> Dict[str, object]:
    label = "iid" if rho <= 0 else f"rho={rho:.1f}"
    print(f"\nEvaluating {label} fresh-instance transfer for: {checkpoint_path}", flush=True)

    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    cfg = cfg_from_checkpoint(checkpoint_path)

    _, testloader = get_dataloaders(
        dataset="cifar10",
        batch_size=256,
        data_root=data_root,
        num_workers=num_workers,
    )
    criterion = nn.CrossEntropyLoss()

    instance_means: List[float] = []
    instance_rows: List[dict] = []

    for instance_idx in range(fresh_instances):
        seed = 42 + instance_idx * 100
        set_seed(seed)
        model = build_model(cfg, num_classes=10, device=device, pretrained=False)
        model.load_state_dict(ckpt["model_state_dict"], strict=True)
        resampled = resample_all_d2d_noise(model)
        correlated_modules = apply_correlated_d2d_buffers(model, rho) if rho > 0 else 0

        losses: List[float] = []
        accs: List[float] = []
        for _ in range(eval_runs):
            loss, acc = evaluate(model, testloader, criterion, device, cfg, amp_enabled=False)
            losses.append(float(loss))
            accs.append(float(acc))

        mean_acc = mean(accs)
        print(
            f"  {label} instance {instance_idx + 1:02d}/{fresh_instances}: "
            f"mean_acc={mean_acc:.2f}% eval_runs={eval_runs}",
            flush=True,
        )
        instance_means.append(mean_acc)
        instance_rows.append(
            {
                "instance_index": instance_idx,
                "seed": seed,
                "rho": rho,
                "resampled_modules": resampled,
                "correlated_modules": correlated_modules,
                "eval_runs": eval_runs,
                "test_loss_mean": mean(losses),
                "test_acc_mean": mean_acc,
                "test_acc_std": stdev(accs) if len(accs) > 1 else 0.0,
                "test_acc_raw": accs,
            }
        )

    result = {
        "checkpoint_path": checkpoint_path,
        "train_best_acc": float(ckpt.get("best_acc", float("nan"))),
        "train_best_epoch": int(ckpt.get("best_epoch", ckpt.get("epoch", -1))),
        "fresh_instances": fresh_instances,
        "mc_runs_per_instance": eval_runs,
        "rho": rho,
        "correlation_model": "separable_ar1_2d",
        "cross_instance_mean": mean(instance_means),
        "cross_instance_std": stdev(instance_means) if len(instance_means) > 1 else 0.0,
        "instance_means": instance_means,
        "instances": instance_rows,
    }

    print(
        f"Completed {label}: {result['cross_instance_mean']:.2f}% +/- "
        f"{result['cross_instance_std']:.2f}% across {fresh_instances} fresh instances",
        flush=True,
    )
    return result


def format_key(rho: float) -> str:
    if rho <= 0:
        return "iid"
    return f"rho_{str(rho).replace('.', '_')}"


def build_markdown(summary: Dict[str, object]) -> str:
    lines = [
        "# Correlated D2D Fresh-Instance Stress Test",
        "",
        f"- Generated: `{summary['generated_at']}`",
        f"- Checkpoint: `{summary['checkpoint_path']}`",
        f"- Protocol: `{summary['protocol']}`",
        f"- Correlation model: `{summary['correlation_model']}`",
        "",
        "| Condition | Train best acc (%) | Fresh-instance mean (%) | Cross-instance std (%) |",
        "|:--|--:|--:|--:|",
    ]

    ordered_keys = list(summary["results"].keys())
    for key in ordered_keys:
        row = summary["results"][key]
        label = "iid Gaussian" if key == "iid" else key.replace("_", "=").replace("rho=", "rho=").replace("rho", "rho")
        if key.startswith("rho_"):
            label = f"correlated {key.replace('rho_', 'rho=')}"
        lines.append(
            f"| {label} | {row['train_best_acc']:.2f} | {row['cross_instance_mean']:.2f} | {row['cross_instance_std']:.2f} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `iid Gaussian` is the paper-locked fresh-instance baseline for the canonical Ensemble HAT checkpoint.",
            "- `correlated rho=...` keeps the same checkpoint and evaluation protocol but replaces i.i.d. D2D with a spatially correlated AR(1)-style field across the effective crossbar grid.",
            "- The reviewer-facing question is whether Ensemble HAT remains clearly above the collapsed fixed-mask baseline when moderate spatial structure is introduced.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", default=DEFAULT_CKPT)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--data-root", default="./data")
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--fresh-instances", type=int, default=10)
    parser.add_argument("--eval-runs", type=int, default=5)
    parser.add_argument(
        "--correlations",
        nargs="+",
        type=float,
        default=[0.0, 0.3],
        help="List of D2D correlation coefficients to evaluate; use 0 for iid baseline.",
    )
    parser.add_argument("--json-path", default=DEFAULT_JSON)
    parser.add_argument("--md-path", default=DEFAULT_MD)
    args = parser.parse_args()

    results: Dict[str, Dict[str, object]] = {}
    for rho in args.correlations:
        key = format_key(rho)
        results[key] = evaluate_fresh_instances_correlated(
            checkpoint_path=args.checkpoint,
            device=args.device,
            fresh_instances=args.fresh_instances,
            eval_runs=args.eval_runs,
            data_root=args.data_root,
            num_workers=args.num_workers,
            rho=rho,
        )

    summary = {
        "generated_at": datetime.now().isoformat(),
        "checkpoint_path": args.checkpoint,
        "protocol": (
            f"{args.fresh_instances} fresh D2D instances x {args.eval_runs} MC evaluations "
            "per instance on the canonical Tiny-ViT V4 Ensemble HAT checkpoint"
        ),
        "correlation_model": "separable_ar1_2d",
        "results": results,
    }

    json_path = Path(args.json_path)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    md_path = Path(args.md_path)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(build_markdown(summary), encoding="utf-8")

    print(
        json.dumps(
            {
                "json_path": str(json_path),
                "md_path": str(md_path),
                **{f"{key}_mean": row["cross_instance_mean"] for key, row in results.items()},
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
