#!/usr/bin/env python3
"""Diagnose Tiny-ViT noise application and scale-recovery effects."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from typing import List

import torch

from inference_analysis_utils import (
    collect_analog_noise_diagnostics,
    iter_analog_modules,
    load_model_bundle,
    run_mc_eval,
    set_uniform_noise,
    set_uniform_retention,
)
from train_tinyvit import RunLogger


DEFAULT_JSON_PATH = "report_md/_gpt/json_gpt/tinyvit_noise_diagnostic_gpt.json"
DEFAULT_MD_PATH = "report_md/_gpt/tinyvit_noise_diagnostic_gpt.md"
DEFAULT_LOG_PATH = "logs/_gpt/tinyvit_noise_diagnostic_gpt.log"
DEFAULT_LAYER_NAMES = [
    "patch_embed.conv1.conv",
    "stages.1.blocks.0.attn.qkv",
    "stages.3.blocks.1.mlp.fc2",
]


def ensure_parent_dir(path: str):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def summarize_d2d_buffers(model) -> dict:
    layer_means: List[float] = []
    layer_stds: List[float] = []
    for _name, module in iter_analog_modules(model):
        d2d = module.d2d_noise.float()
        layer_means.append(float(d2d.abs().mean().item()))
        layer_stds.append(float(d2d.std(unbiased=False).item()))
    return {
        "analog_layers": len(layer_means),
        "mean_abs_d2d": sum(layer_means) / len(layer_means) if layer_means else 0.0,
        "mean_std_d2d": sum(layer_stds) / len(layer_stds) if layer_stds else 0.0,
    }


def build_markdown(payload: dict) -> str:
    lines = [
        "# Tiny-ViT Noise Diagnostic (GPT)",
        "",
        f"- Generated: `{payload['generated_at']}`",
        f"- Device: `{payload['device']}`",
        f"- Eval runs: `{payload['eval_runs']}`",
        f"- Target noise: `sigma_c2c={payload['sigma_c2c']}`, `sigma_d2d={payload['sigma_d2d']}`",
        "",
        "## Condition Summary",
        "",
        "| Condition | Experiment | Resample D2D | Accuracy | mean|D2D| | mean std(D2D) |",
        "|:----------|:-----------|:-------------|:---------|------:|--------------:|",
    ]
    for condition in payload["conditions"]:
        lines.append(
            f"| {condition['label']} | {condition['experiment']} | {condition['resample_d2d']} | "
            f"{condition['summary']['test_acc_mean']:.2f} +/- {condition['summary']['test_acc_std']:.2f}% | "
            f"{condition['d2d_buffer_summary']['mean_abs_d2d']:.6f} | "
            f"{condition['d2d_buffer_summary']['mean_std_d2d']:.6f} |"
        )

    lines.extend([
        "",
        "## Representative Layer Diagnostics",
        "",
    ])
    for condition in payload["conditions"]:
        lines.extend([
            f"### {condition['label']}",
            "",
            "| Layer | Noise/weight | Noise/effective-weight | D2D std (G) | C2C std (G) | Scale factor |",
            "|:------|-------------:|-----------------------:|------------:|------------:|------------:|",
        ])
        for row in condition["layer_diagnostics"]:
            lines.append(
                f"| {row['layer']} | {row['noise_to_weight_ratio']:.4f} | "
                f"{row['noise_to_effective_weight_ratio']:.4f} | "
                f"{row['d2d_noise_std_conductance']:.6f} | "
                f"{row['c2c_noise_std_conductance']:.6f} | "
                f"{row['scale_recovery_factor']:.6f} |"
            )
        lines.append("")

    lines.extend([
        "## Notes",
        "",
        "- `V2_current_path` mimics the pre-fix `run_noise_sweep.py` behavior: config sigmas are updated but D2D buffers are not re-sampled.",
        "- `V2_resampled_d2d` forces D2D re-sampling after changing `sigma_d2d` and is the correctness check requested by Claude.",
        "- `V4_reference` uses the HAT checkpoint under the same target noise setting as a reference point.",
        "",
    ])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Diagnose Tiny-ViT V2/V4 noise application.")
    parser.add_argument("--device", type=str, default=None)
    parser.add_argument("--checkpoint-dir", type=str, default="checkpoints")
    parser.add_argument("--data-root", type=str, default="./data")
    parser.add_argument("--num-workers", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=None)
    parser.add_argument("--eval-runs", type=int, default=10)
    parser.add_argument("--amp", action="store_true")
    parser.add_argument("--sigma-c2c", type=float, default=0.05)
    parser.add_argument("--sigma-d2d", type=float, default=0.10)
    parser.add_argument("--layer-names", nargs="+", default=DEFAULT_LAYER_NAMES)
    parser.add_argument("--results-json-path", type=str, default=DEFAULT_JSON_PATH)
    parser.add_argument("--results-md-path", type=str, default=DEFAULT_MD_PATH)
    parser.add_argument("--log-path", type=str, default=DEFAULT_LOG_PATH)
    args = parser.parse_args()

    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")
    logger = RunLogger(args.log_path)

    conditions = [
        ("V2_current_path", "V2", False),
        ("V2_resampled_d2d", "V2", True),
        ("V4_reference", "V4", False),
    ]

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "device": device,
        "eval_runs": args.eval_runs,
        "sigma_c2c": args.sigma_c2c,
        "sigma_d2d": args.sigma_d2d,
        "layer_names": list(args.layer_names),
        "conditions": [],
    }

    try:
        for label, experiment, resample_d2d in conditions:
            logger.log(f"Condition: {label} (experiment={experiment}, resample_d2d={resample_d2d})")
            bundle = load_model_bundle(
                model_type="tinyvit",
                experiment=experiment,
                device=device,
                checkpoint_dir=args.checkpoint_dir,
                dataset="cifar10",
                data_root=args.data_root,
                num_workers=args.num_workers,
                batch_size=args.batch_size,
                amp_enabled=args.amp,
            )
            set_uniform_retention(bundle.model, 0.0)
            set_uniform_noise(
                bundle.model,
                sigma_c2c=args.sigma_c2c,
                sigma_d2d=args.sigma_d2d,
                noise_enabled=True,
                resample_d2d=resample_d2d,
            )
            d2d_summary = summarize_d2d_buffers(bundle.model)
            logger.log(
                f"{label}: mean|d2d|={d2d_summary['mean_abs_d2d']:.6f}, "
                f"mean_std(d2d)={d2d_summary['mean_std_d2d']:.6f}"
            )
            diagnostics = collect_analog_noise_diagnostics(bundle.model, layer_names=args.layer_names)
            for row in diagnostics:
                logger.log(
                    f"{label}: {row['layer']}: noise/weight={row['noise_to_weight_ratio']:.4f}, "
                    f"noise/effective={row['noise_to_effective_weight_ratio']:.4f}, "
                    f"d2d_std_G={row['d2d_noise_std_conductance']:.6f}, "
                    f"c2c_std_G={row['c2c_noise_std_conductance']:.6f}, "
                    f"scale={row['scale_recovery_factor']:.6f}"
                )
            summary = run_mc_eval(bundle, eval_runs=args.eval_runs, logger=logger, label=label)
            payload["conditions"].append({
                "label": label,
                "experiment": experiment,
                "checkpoint_path": bundle.checkpoint_path,
                "checkpoint_epoch": bundle.checkpoint_epoch,
                "checkpoint_best_acc": bundle.checkpoint_best_acc,
                "resample_d2d": resample_d2d,
                "d2d_buffer_summary": d2d_summary,
                "summary": summary,
                "layer_diagnostics": diagnostics,
            })

        ensure_parent_dir(args.results_json_path)
        ensure_parent_dir(args.results_md_path)
        with open(args.results_json_path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
        with open(args.results_md_path, "w", encoding="utf-8") as fh:
            fh.write(build_markdown(payload))
        logger.log(f"JSON: {args.results_json_path}")
        logger.log(f"Markdown: {args.results_md_path}")
    finally:
        logger.close()


if __name__ == "__main__":
    main()
