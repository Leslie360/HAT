#!/usr/bin/env python3
"""R10B class-distribution diagnostics for Standard-vs-Ensemble HAT.

The first R10B proxy run accidentally evaluated the post-fix M-series
checkpoints only.  This script makes the checkpoint set explicit so the
canonical 10% fresh-instance collapse and the post-fix M-series diagnostic
cannot be conflated.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional

import matplotlib.pyplot as plt
import numpy as np
import torch

sys.path.insert(0, ".")

from amp_utils import autocast_context
from inference_analysis_utils import load_model_bundle, set_uniform_noise


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class ProbeSpec:
    key: str
    label: str
    exp_id: str
    checkpoint: str
    family: str
    expected: str


CANONICAL_PROBES = [
    ProbeSpec(
        key="canonical_standard_hat",
        label="Canonical Standard HAT",
        exp_id="V4",
        checkpoint="checkpoints/V4_hybrid_standard_noise_hat_best.pt",
        family="canonical",
        expected="fresh-instance collapse near 10%",
    ),
    ProbeSpec(
        key="canonical_ensemble_hat",
        label="Canonical Ensemble HAT",
        exp_id="V4",
        checkpoint="checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt",
        family="canonical",
        expected="fresh-instance robust near 86%",
    ),
]


POSTFIX_M_SERIES_PROBES = [
    ProbeSpec(
        key="postfix_mseries_standard_hat",
        label="Post-fix M-series Standard HAT",
        exp_id="V3",
        checkpoint=(
            "checkpoints/_gpt/postfix_m_series/cx_m1_standard_seed123/"
            "V3_hybrid_standard_noise_standard_train_best.pt"
        ),
        family="postfix_mseries",
        expected="diagnostic control, not canonical collapse evidence",
    ),
    ProbeSpec(
        key="postfix_mseries_ensemble_hat",
        label="Post-fix M-series Ensemble HAT",
        exp_id="V4",
        checkpoint=(
            "checkpoints/_gpt/postfix_m_series/cx_m2_ensemble_seed123/"
            "V4_hybrid_standard_noise_hat_best.pt"
        ),
        family="postfix_mseries",
        expected="diagnostic control, not canonical collapse evidence",
    ),
]


def iter_probe_specs(mode: str) -> Iterable[ProbeSpec]:
    if mode == "canonical":
        return CANONICAL_PROBES
    if mode == "postfix-mseries":
        return POSTFIX_M_SERIES_PROBES
    return [*CANONICAL_PROBES, *POSTFIX_M_SERIES_PROBES]


def checkpoint_meta(path: Path) -> dict:
    ckpt = torch.load(path, map_location="cpu", weights_only=False)
    exp_cfg = ckpt.get("exp_cfg") or {}
    return {
        "checkpoint_path": str(path),
        "checkpoint_epoch": ckpt.get("epoch"),
        "checkpoint_best_epoch": ckpt.get("best_epoch"),
        "checkpoint_best_acc": ckpt.get("best_acc"),
        "checkpoint_seed": ckpt.get("seed"),
        "checkpoint_exp_cfg": exp_cfg,
    }


def evaluate_predictions(
    spec: ProbeSpec,
    device: str,
    num_instances: int,
    batch_size: int,
    num_workers: int,
    max_batches: Optional[int],
    sigma_c2c: float,
    sigma_d2d: float,
) -> dict:
    ckpt_path = ROOT / spec.checkpoint
    if not ckpt_path.exists():
        raise FileNotFoundError(f"{spec.key} checkpoint not found: {ckpt_path}")

    print(f"\nLoading {spec.label}: {ckpt_path}")
    bundle = load_model_bundle(
        "tinyvit",
        spec.exp_id,
        device,
        str(ckpt_path),
        num_workers=num_workers,
        batch_size=batch_size,
        amp_enabled=(device == "cuda"),
    )

    meta = checkpoint_meta(ckpt_path)
    results = []

    for instance_idx in range(num_instances):
        seed = 42 + instance_idx * 100
        torch.manual_seed(seed)
        np.random.seed(seed)
        set_uniform_noise(
            bundle.model,
            sigma_c2c=sigma_c2c,
            sigma_d2d=sigma_d2d,
            noise_enabled=True,
            resample_d2d=True,
            noise_mode="uniform",
        )

        all_preds = []
        all_targets = []
        bundle.model.eval()
        with torch.no_grad():
            for batch_idx, (inputs, targets) in enumerate(bundle.testloader):
                if max_batches is not None and batch_idx >= max_batches:
                    break
                inputs = inputs.to(device)
                targets = targets.to(device)
                if bundle.frontend is not None:
                    inputs = bundle.frontend(inputs, mode="compensated")
                with autocast_context(device, bundle.amp_enabled):
                    outputs = bundle.model(inputs)
                preds = outputs.argmax(dim=1)
                all_preds.append(preds.detach().cpu().numpy())
                all_targets.append(targets.detach().cpu().numpy())

        preds_np = np.concatenate(all_preds)
        targets_np = np.concatenate(all_targets)
        pred_counts = np.bincount(preds_np, minlength=10)
        pred_freq = pred_counts / max(1, len(preds_np))
        entropy = float(-np.sum(pred_freq * np.log(pred_freq + 1e-12)))
        class_accs = []
        for cls in range(10):
            mask = targets_np == cls
            class_accs.append(float(np.mean(preds_np[mask] == cls)) if np.any(mask) else 0.0)
        overall_acc = float(np.mean(preds_np == targets_np))
        row = {
            "instance": instance_idx,
            "seed": seed,
            "num_examples": int(len(preds_np)),
            "overall_acc": overall_acc,
            "overall_acc_percent": overall_acc * 100.0,
            "pred_counts": pred_counts.tolist(),
            "pred_freq": pred_freq.tolist(),
            "max_class": int(np.argmax(pred_freq)),
            "max_freq": float(np.max(pred_freq)),
            "entropy": entropy,
            "entropy_fraction_of_uniform": entropy / math.log(10),
            "class_accs": class_accs,
        }
        results.append(row)
        print(
            f"{spec.key} instance {instance_idx}: "
            f"acc={row['overall_acc_percent']:.2f}%, "
            f"entropy={entropy:.4f}, max_freq={row['max_freq'] * 100:.2f}%"
        )

    return {
        "spec": asdict(spec),
        "checkpoint_meta": meta,
        "eval_protocol": {
            "device": device,
            "num_instances": num_instances,
            "batch_size": batch_size,
            "num_workers": num_workers,
            "max_batches": max_batches,
            "sigma_c2c": sigma_c2c,
            "sigma_d2d": sigma_d2d,
            "noise_mode": "uniform",
            "eval_nl_ltp": 1.0,
            "eval_nl_ltd": -1.0,
        },
        "instances": results,
        "summary": summarize_instances(results),
    }


def summarize_instances(rows: list[dict]) -> dict:
    summary = {}
    for key in ("overall_acc_percent", "entropy", "max_freq"):
        vals = np.asarray([row[key] for row in rows], dtype=float)
        summary[key] = {
            "mean": float(vals.mean()),
            "std": float(vals.std(ddof=0)),
            "min": float(vals.min()),
            "max": float(vals.max()),
        }
    return summary


def plot_results(results: dict, output_pdf: Path, output_png: Path) -> None:
    classes = np.arange(10)
    plot_keys = [key for key in results if key in {"canonical_standard_hat", "canonical_ensemble_hat"}]
    if len(plot_keys) < 2:
        plot_keys = list(results)[:2]

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
    palette = {
        "canonical_standard_hat": "#ba3b2f",
        "canonical_ensemble_hat": "#2b6c8a",
        "postfix_mseries_standard_hat": "#9b6a20",
        "postfix_mseries_ensemble_hat": "#4a7c39",
    }

    for ax, key in zip(axes[:2], plot_keys[:2]):
        payload = results[key]
        color = palette.get(key, "#444444")
        for row in payload["instances"]:
            ax.plot(classes, row["pred_freq"], marker="o", alpha=0.55, color=color)
        ax.set_title(payload["spec"]["label"])
        ax.set_xlabel("Predicted class")
        ax.set_ylabel("Frequency")
        ax.set_ylim(0, 1.05)
        ax.set_xticks(classes)
        ax.grid(alpha=0.2)

    labels = [results[key]["spec"]["label"].replace(" HAT", "") for key in results]
    means = [results[key]["summary"]["entropy"]["mean"] for key in results]
    stds = [results[key]["summary"]["entropy"]["std"] for key in results]
    colors = [palette.get(key, "#444444") for key in results]
    xpos = np.arange(len(labels))
    axes[2].bar(xpos, means, yerr=stds, capsize=4, color=colors)
    axes[2].axhline(y=math.log(10), color="#111111", linestyle="--", linewidth=1, label="uniform")
    axes[2].set_ylabel("Prediction entropy")
    axes[2].set_xticks(xpos)
    axes[2].set_xticklabels(labels, rotation=20, ha="right")
    axes[2].set_ylim(0, math.log(10) * 1.08)
    axes[2].legend(frameon=False)
    axes[2].grid(axis="y", alpha=0.2)

    fig.tight_layout()
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    output_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_pdf)
    fig.savefig(output_png, dpi=300)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["canonical", "postfix-mseries", "both"], default="canonical")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--num-instances", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--max-batches", type=int, default=None, help="Debug only; omit for full CIFAR-10.")
    parser.add_argument("--sigma-c2c", type=float, default=0.05)
    parser.add_argument("--sigma-d2d", type=float, default=0.10)
    parser.add_argument(
        "--output-json",
        default="report_md/_gpt/json_gpt/r10b_standard_hat_class_distribution.json",
    )
    parser.add_argument(
        "--output-figure-pdf",
        default="paper/latex_gpt/figures/figS_standard_hat_collapse_mechanism.pdf",
    )
    parser.add_argument(
        "--output-figure-png",
        default="paper/latex_gpt/figures/figS_standard_hat_collapse_mechanism.png",
    )
    args = parser.parse_args()

    output = {
        "generated_at": datetime.now().isoformat(),
        "script": str(Path(__file__).relative_to(ROOT)),
        "mode": args.mode,
        "warning": (
            "Use canonical_* entries for the paper's 10% fresh-instance collapse mechanism. "
            "postfix_mseries_* entries are diagnostic controls and must not be cited as "
            "canonical collapse evidence."
        ),
        "probes": {},
    }
    for spec in iter_probe_specs(args.mode):
        output["probes"][spec.key] = evaluate_predictions(
            spec=spec,
            device=args.device,
            num_instances=args.num_instances,
            batch_size=args.batch_size,
            num_workers=args.num_workers,
            max_batches=args.max_batches,
            sigma_c2c=args.sigma_c2c,
            sigma_d2d=args.sigma_d2d,
        )

    out_json = ROOT / args.output_json
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(output, indent=2), encoding="utf-8")

    plot_results(output["probes"], ROOT / args.output_figure_pdf, ROOT / args.output_figure_png)
    print(f"\nSaved JSON: {out_json}")
    print(f"Saved figure PDF: {ROOT / args.output_figure_pdf}")
    print(f"Saved figure PNG: {ROOT / args.output_figure_png}")


if __name__ == "__main__":
    main()
