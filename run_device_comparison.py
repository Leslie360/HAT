#!/usr/bin/env python3
"""Zero-shot hardware transferability sweep for Tiny-ViT V4 and ConvNeXt C4."""

from __future__ import annotations

import argparse
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Sequence

import torch

from device_profile_utils import (
    DEFAULT_DEVICE_PROFILES,
    DeviceProfile,
    load_device_profiles_json,
)
from inference_analysis_utils import (
    apply_device_profile,
    build_sparsity_rows,
    export_rows,
    load_existing_results,
    load_model_bundle,
    merge_rows,
    restore_analog_state,
    run_mc_eval,
    set_uniform_retention,
    snapshot_analog_state,
)
from paper.plot_paper_figures import configure_style, ensure_dir, plot_fig10_zero_shot_transferability
from report_asset_paths import asset_path
from train_tinyvit import RunLogger


DEVICE_PROFILES: Sequence[DeviceProfile] = DEFAULT_DEVICE_PROFILES


def default_experiment_for(model_type: str) -> str:
    return "V4" if model_type == "tinyvit" else "C4"


def row_base(bundle, profile: DeviceProfile) -> dict:
    return {
        "model": bundle.model_type,
        "experiment": bundle.experiment,
        "experiment_name": bundle.experiment_name,
        "dataset": bundle.dataset,
        "checkpoint_path": bundle.checkpoint_path,
        "checkpoint_epoch": bundle.checkpoint_epoch,
        "checkpoint_best_acc": bundle.checkpoint_best_acc,
        "device_type": profile.device_type,
        "profile": profile.device_type,
        "dynamic_range": profile.dynamic_range,
        "G_min": profile.G_min,
        "G_max": profile.G_max,
        "n_states": profile.n_states,
        "sigma_c2c": profile.sigma_c2c,
        "sigma_d2d": profile.sigma_d2d,
        "noise_mode": profile.noise_mode,
        "source": profile.source,
        "profile_kind": profile.profile_kind,
        "tau_1": profile.tau_1,
        "tau_2": profile.tau_2,
        "A_0": profile.A_0,
        "NL_LTP": profile.NL_LTP,
        "NL_LTD": profile.NL_LTD,
        "analysis_type": "device_comparison",
        "amp_enabled": bundle.amp_enabled,
        "d2d_instance_policy": "fresh_resampled_per_profile",
        "transfer_definition": "zero_shot_device_and_instance_transfer",
    }


def run_profiles(bundle, profiles: Sequence[DeviceProfile], eval_runs: int, logger: RunLogger):
    rows: List[dict] = []
    sparsity_rows: List[dict] = []
    snapshot = snapshot_analog_state(bundle.model)
    try:
        set_uniform_retention(bundle.model, 0.0)
        for profile in profiles:
            analog_layers = apply_device_profile(bundle.model, profile)
            logger.log(
                f"{bundle.model_type}/{bundle.experiment}: profile={profile.device_type}, "
                f"analog_layers={analog_layers}, n_states={profile.n_states}, "
                f"G_range={profile.dynamic_range}x, c2c={profile.sigma_c2c}, d2d={profile.sigma_d2d}"
            )
            summary, sparsity_report = run_mc_eval(
                bundle,
                eval_runs=eval_runs,
                logger=logger,
                label=f"{bundle.model_type}:{profile.device_type}",
                collect_sparsity=True,
            )
            row = row_base(bundle, profile)
            row.update(summary)
            rows.append(row)
            sparsity_rows.extend(build_sparsity_rows(bundle, sparsity_report, context={
                "analysis_type": "device_comparison",
                "device_type": profile.device_type,
                "profile": profile.device_type,
            }))
    finally:
        restore_analog_state(bundle.model, snapshot)
    return rows, sparsity_rows


def build_markdown(current_rows: List[dict], merged_rows: List[dict], args, profiles: Sequence[DeviceProfile]) -> str:
    lines = [
        "# Device Comparison Results (GPT)",
        "",
        f"- Generated: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`",
        f"- Models: `{', '.join(args.model_types)}`",
        f"- Tiny-ViT experiment: `{args.tinyvit_experiment}`",
        f"- ConvNeXt experiment: `{args.convnext_experiment}`",
        f"- Eval runs per profile: `{args.eval_runs}`",
        f"- Profile source: `{args.device_profile_json or 'built-in literature priors'}`",
        "",
        "## Current Invocation",
        "",
        "| Model | Device Profile | Accuracy | Source |",
        "|:------|:---------------|:---------|:-------|",
    ]
    for row in current_rows:
        lines.append(
            f"| {row['model']} | {row['device_type']} | "
            f"{row['test_acc_mean']:.2f} +/- {row['test_acc_std']:.2f}% ({row['eval_runs']} runs) | "
            f"{row['source']} |"
        )
    lines.extend([
        "",
        "## Notes",
        "",
        "- This sweep measures zero-shot hardware transferability from organic-HAT checkpoints.",
        "- Each profile applies a freshly resampled D2D instance after updating device parameters; results therefore reflect transfer to a new hardware instance, not reuse of the checkpoint's stored mismatch map.",
        "- It does not claim device-specific optimal performance for RRAM or PCM because no device-specific HAT fine-tuning is performed.",
        f"- Loaded profiles: `{', '.join(profile.device_type for profile in profiles)}`",
        f"- Total merged rows: `{len(merged_rows)}`",
        "",
    ])
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Run zero-shot hardware transferability sweeps.")
    parser.add_argument("--model-types", nargs="+", choices=["tinyvit", "convnext"], default=["tinyvit", "convnext"])
    parser.add_argument("--tinyvit-experiment", type=str, default="V4")
    parser.add_argument("--convnext-experiment", type=str, default="C4")
    parser.add_argument("--checkpoint-dir", type=str, default="checkpoints")
    parser.add_argument("--data-root", type=str, default="./data")
    parser.add_argument("--num-workers", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=None)
    parser.add_argument("--device", type=str, default=None)
    parser.add_argument("--eval-runs", type=int, default=10)
    parser.add_argument("--amp", action="store_true")
    parser.add_argument("--output-dir", type=str, default="report_md/_gpt")
    parser.add_argument("--json-name", type=str, default="device_comparison_results_gpt.json")
    parser.add_argument("--csv-name", type=str, default="device_comparison_results_gpt.csv")
    parser.add_argument("--sparsity-json-name", type=str, default="activation_sparsity_gpt.json")
    parser.add_argument("--sparsity-csv-name", type=str, default="activation_sparsity_gpt.csv")
    parser.add_argument("--report-name", type=str, default="device_comparison_report_gpt.md")
    parser.add_argument("--figure-output-dir", type=str, default="paper/figures")
    parser.add_argument("--log-path", type=str, default="logs/_gpt/device_comparison_gpt.log")
    parser.add_argument("--device-profile-json", type=str, default=None,
                        help="Optional measured-device profile JSON. Overrides built-in literature profiles.")
    args = parser.parse_args()

    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")
    logger = RunLogger(args.log_path)

    try:
        logger.log(f"Device: {device}")
        logger.log(f"Model types: {args.model_types}")
        logger.log(f"Eval runs: {args.eval_runs}")
        profiles = load_device_profiles_json(args.device_profile_json) if args.device_profile_json else list(DEVICE_PROFILES)
        logger.log(f"Profiles: {[profile.device_type for profile in profiles]}")
        current_rows: List[dict] = []
        current_sparsity_rows: List[dict] = []

        for model_type in args.model_types:
            experiment = args.tinyvit_experiment if model_type == "tinyvit" else args.convnext_experiment
            bundle = load_model_bundle(
                model_type=model_type,
                experiment=experiment,
                device=device,
                checkpoint_dir=args.checkpoint_dir,
                dataset="cifar10",
                data_root=args.data_root,
                num_workers=args.num_workers,
                batch_size=args.batch_size,
                amp_enabled=args.amp,
            )
            logger.log(f"{model_type}: checkpoint={bundle.checkpoint_path}, epoch={bundle.checkpoint_epoch}, best_acc={bundle.checkpoint_best_acc}")
            rows, sparsity_rows = run_profiles(bundle, profiles, eval_runs=args.eval_runs, logger=logger)
            current_rows.extend(rows)
            current_sparsity_rows.extend(sparsity_rows)

        json_path = asset_path(args.output_dir, "json", args.json_name)
        csv_path = asset_path(args.output_dir, "csv", args.csv_name)
        existing_rows = load_existing_results(json_path)
        merged_rows = merge_rows(existing_rows, current_rows, key_fields=("model", "experiment", "device_type"))
        metadata = {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "models": list(args.model_types),
            "eval_runs": args.eval_runs,
            "d2d_instance_policy": "fresh_resampled_per_profile",
            "transfer_definition": "zero_shot_device_and_instance_transfer",
            "profile_source": args.device_profile_json or "built_in_literature",
        }
        export_rows(merged_rows, json_path=json_path, csv_path=csv_path, metadata=metadata)

        sparsity_json_path = asset_path(args.output_dir, "json", args.sparsity_json_name)
        sparsity_csv_path = asset_path(args.output_dir, "csv", args.sparsity_csv_name)
        existing_sparsity = load_existing_results(sparsity_json_path)
        merged_sparsity = merge_rows(
            existing_sparsity,
            current_sparsity_rows,
            key_fields=("model", "experiment", "analysis_type", "device_type", "layer"),
        )
        export_rows(merged_sparsity, json_path=sparsity_json_path, csv_path=sparsity_csv_path, metadata=metadata)

        os.makedirs(args.output_dir, exist_ok=True)
        report_path = os.path.join(args.output_dir, args.report_name)
        with open(report_path, "w", encoding="utf-8") as fh:
            fh.write(build_markdown(current_rows, merged_rows, args, profiles))

        configure_style()
        figure_dir = Path(args.figure_output_dir)
        ensure_dir(figure_dir)
        plot_fig10_zero_shot_transferability(figure_dir)

        logger.log(f"Merged rows written: {len(merged_rows)}")
        logger.log(f"JSON: {json_path}")
        logger.log(f"CSV: {csv_path}")
        logger.log(f"Sparsity CSV: {sparsity_csv_path}")
        logger.log(f"Report: {report_path}")
    finally:
        logger.close()


if __name__ == "__main__":
    main()
