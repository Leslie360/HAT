#!/usr/bin/env python3
"""Diagnose Tiny-ViT retention behavior under scale recovery."""

from __future__ import annotations

import argparse
import json
import math
import os
from datetime import datetime
from typing import List

import torch

from inference_analysis_utils import (
    iter_analog_modules,
    load_model_bundle,
    run_mc_eval,
    set_uniform_retention,
)
from train_tinyvit import RunLogger


DEFAULT_JSON_PATH = "report_md/_gpt/json_gpt/tinyvit_retention_diagnostic_gpt.json"
DEFAULT_MD_PATH = "report_md/_gpt/tinyvit_retention_diagnostic_gpt.md"
DEFAULT_LOG_PATH = "logs/_gpt/tinyvit_retention_diagnostic_gpt.log"
DEFAULT_LAYER_NAMES = [
    "patch_embed.conv1.conv",
    "stages.1.blocks.0.attn.qkv",
    "stages.3.blocks.1.mlp.fc2",
]


def ensure_parent_dir(path: str):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def retention_decay_factor(cfg) -> float:
    if not cfg.retention_enabled or cfg.inference_time <= 0:
        return 1.0
    a0 = cfg.A_0
    a1 = (1.0 - a0) / 2.0
    a2 = a1
    t = cfg.inference_time
    return (
        a1 * math.exp(-t / cfg.tau_1)
        + a2 * math.exp(-t / cfg.tau_2)
        + a0
    )


def set_retention_mode(model, *, recalibrate_scale: bool, scale_d2d: bool):
    for _name, module in iter_analog_modules(model):
        module.config.retention_recalibrate_scale = recalibrate_scale
        module.config.retention_scales_d2d = scale_d2d


def collect_retention_layer_diagnostics(model, layer_names: List[str]) -> List[dict]:
    wanted = set(layer_names)
    rows = []
    for name, module in iter_analog_modules(model):
        if name not in wanted:
            continue
        with torch.no_grad():
            G_pos, G_neg = module._weight_to_conductance(module.weight)
            G_pos_d, G_neg_d = module._apply_retention(G_pos, G_neg)
            retained_diff = (G_pos_d - G_neg_d).float()

            w_abs_max = float(module.weight.float().abs().max().item())
            original_scale = float(w_abs_max / (module.config.G_max - module.config.G_min + 1e-8))
            recalibrated_scale = float(w_abs_max / (retained_diff.abs().max().item() + 1e-8))
            effective_scale = float(module._conductance_to_weight_scale(module.weight, retained_diff).item())
            decay = retention_decay_factor(module.config)
            d2d_scale = decay if module.config.retention_scales_d2d else 1.0
            d2d_std = float((module.d2d_noise.float() * d2d_scale).std(unbiased=False).item())
            rows.append({
                "layer": name,
                "kind": type(module).__name__,
                "decay_factor": decay,
                "retained_diff_max": float(retained_diff.abs().max().item()),
                "original_scale": original_scale,
                "recalibrated_scale": recalibrated_scale,
                "effective_scale": effective_scale,
                "d2d_std_conductance": d2d_std,
                "retention_recalibrate_scale": bool(module.config.retention_recalibrate_scale),
                "retention_scales_d2d": bool(module.config.retention_scales_d2d),
            })
    return rows


def build_markdown(payload: dict) -> str:
    lines = [
        "# Tiny-ViT Retention Diagnostic (GPT)",
        "",
        f"- Generated: `{payload['generated_at']}`",
        f"- Device: `{payload['device']}`",
        f"- Eval runs: `{payload['eval_runs']}`",
        f"- Time point: `{payload['time_s']}s`",
        "",
        "## Condition Summary",
        "",
        "| Condition | Recalibrate Scale | D2D Decays | Accuracy |",
        "|:----------|:------------------|:-----------|:---------|",
    ]
    for cond in payload["conditions"]:
        lines.append(
            f"| {cond['label']} | {cond['recalibrate_scale']} | {cond['scale_d2d']} | "
            f"{cond['summary']['test_acc_mean']:.2f} +/- {cond['summary']['test_acc_std']:.2f}% |"
        )
    lines.extend(["", "## Representative Layers", ""])
    for cond in payload["conditions"]:
        lines.extend([
            f"### {cond['label']}",
            "",
            "| Layer | Decay | Original Scale | Recal Scale | Effective Scale | retained |D| max | D2D std(G) |",
            "|:------|------:|---------------:|------------:|----------------:|----------------:|-----------:|",
        ])
        for row in cond["layer_diagnostics"]:
            lines.append(
                f"| {row['layer']} | {row['decay_factor']:.4f} | {row['original_scale']:.6f} | "
                f"{row['recalibrated_scale']:.6f} | {row['effective_scale']:.6f} | "
                f"{row['retained_diff_max']:.6f} | {row['d2d_std_conductance']:.6f} |"
            )
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Diagnose Tiny-ViT retention collapse.")
    parser.add_argument("--device", type=str, default=None)
    parser.add_argument("--checkpoint-dir", type=str, default="checkpoints")
    parser.add_argument("--data-root", type=str, default="./data")
    parser.add_argument("--num-workers", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=None)
    parser.add_argument("--eval-runs", type=int, default=10)
    parser.add_argument("--amp", action="store_true")
    parser.add_argument("--time-s", type=int, default=1)
    parser.add_argument("--layer-names", nargs="+", default=DEFAULT_LAYER_NAMES)
    parser.add_argument("--results-json-path", type=str, default=DEFAULT_JSON_PATH)
    parser.add_argument("--results-md-path", type=str, default=DEFAULT_MD_PATH)
    parser.add_argument("--log-path", type=str, default=DEFAULT_LOG_PATH)
    args = parser.parse_args()

    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")
    logger = RunLogger(args.log_path)

    conditions = [
        ("current", False, False),
        ("recalibrate_scale", True, False),
        ("recalibrate_scale_and_decay_d2d", True, True),
    ]
    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "device": device,
        "eval_runs": args.eval_runs,
        "time_s": args.time_s,
        "conditions": [],
    }

    try:
        for label, recalibrate_scale, scale_d2d in conditions:
            logger.log(
                f"Condition: {label} "
                f"(recalibrate_scale={recalibrate_scale}, scale_d2d={scale_d2d})"
            )
            bundle = load_model_bundle(
                model_type="tinyvit",
                experiment="V4",
                device=device,
                checkpoint_dir=args.checkpoint_dir,
                dataset="cifar10",
                data_root=args.data_root,
                num_workers=args.num_workers,
                batch_size=args.batch_size,
                amp_enabled=args.amp,
            )
            set_retention_mode(
                bundle.model,
                recalibrate_scale=recalibrate_scale,
                scale_d2d=scale_d2d,
            )
            set_uniform_retention(bundle.model, float(args.time_s))
            diagnostics = collect_retention_layer_diagnostics(bundle.model, list(args.layer_names))
            for row in diagnostics:
                logger.log(
                    f"{label}: {row['layer']}: decay={row['decay_factor']:.4f}, "
                    f"orig_scale={row['original_scale']:.6f}, "
                    f"recal_scale={row['recalibrated_scale']:.6f}, "
                    f"eff_scale={row['effective_scale']:.6f}, "
                    f"retained|max|={row['retained_diff_max']:.6f}, "
                    f"d2d_std_G={row['d2d_std_conductance']:.6f}"
                )
            summary = run_mc_eval(bundle, eval_runs=args.eval_runs, logger=logger, label=label)
            payload["conditions"].append({
                "label": label,
                "recalibrate_scale": recalibrate_scale,
                "scale_d2d": scale_d2d,
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
