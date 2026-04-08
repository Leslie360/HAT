#!/usr/bin/env python3
"""Inference-only continuous noise and ADC sensitivity sweeps."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Sequence

import torch

from device_profile_utils import DeviceProfile, load_device_profiles_json, select_device_profile
from inference_analysis_utils import (
    ADCQuantHookManager,
    adc_bits_label,
    apply_device_profile,
    build_sparsity_rows,
    iter_analog_modules,
    calibrate_adc_ranges,
    export_rows,
    load_existing_results,
    load_model_bundle,
    merge_rows,
    run_mc_eval,
    set_uniform_noise,
    set_uniform_retention,
)
from paper.plot_paper_figures import configure_style, ensure_dir, plot_fig9_noise_sensitivity
from report_asset_paths import asset_path
from train_tinyvit import RunLogger


DEFAULT_SIGMA_C2C = [0.0, 0.02, 0.05, 0.08, 0.10, 0.15, 0.20]
DEFAULT_SIGMA_D2D = [0.0, 0.05, 0.10, 0.15, 0.20, 0.30]
DEFAULT_ADC_BITS = ["3", "4", "6", "8", "10", "ideal"]


def default_experiment_for(model_type: str) -> str:
    return "V4" if model_type == "tinyvit" else "C4"


def parse_adc_bits(values: Sequence[str]) -> List[Optional[int]]:
    parsed: List[Optional[int]] = []
    for raw in values:
        token = str(raw).strip().lower()
        if token == "ideal":
            parsed.append(None)
        else:
            parsed.append(int(token))
    return parsed


def resolve_device_profile(profile_json: Optional[str], profile_name: Optional[str]) -> Optional[DeviceProfile]:
    if not profile_json:
        return None
    return select_device_profile(load_device_profiles_json(profile_json), profile_name)


def row_base(bundle, sweep_type: str, device_profile: Optional[DeviceProfile] = None) -> dict:
    return {
        "model": bundle.model_type,
        "experiment": bundle.experiment,
        "experiment_name": bundle.experiment_name,
        "dataset": bundle.dataset,
        "checkpoint_path": bundle.checkpoint_path,
        "checkpoint_epoch": bundle.checkpoint_epoch,
        "checkpoint_best_acc": bundle.checkpoint_best_acc,
        "sweep_type": sweep_type,
        "amp_enabled": bundle.amp_enabled,
        "device_profile": device_profile.device_type if device_profile else None,
        "profile_kind": device_profile.profile_kind if device_profile else None,
        "profile_source": device_profile.source if device_profile else None,
        "dynamic_range": device_profile.dynamic_range if device_profile else None,
        "n_states": device_profile.n_states if device_profile else None,
    }


def apply_override_config(bundle, noise_mode: Optional[str] = None,
                          nl_ltp: Optional[float] = None,
                          nl_ltd: Optional[float] = None) -> int:
    touched = 0
    for _, module in iter_analog_modules(bundle.model):
        if noise_mode is not None:
            module.config.noise_mode = str(noise_mode)
        if nl_ltp is not None:
            module.config.NL_LTP = float(nl_ltp)
        if nl_ltd is not None:
            module.config.NL_LTD = float(nl_ltd)
        touched += 1
    if noise_mode is not None:
        bundle.exp_cfg.noise_mode = str(noise_mode)
    if nl_ltp is not None:
        bundle.exp_cfg.nl_ltp = float(nl_ltp)
    if nl_ltd is not None:
        bundle.exp_cfg.nl_ltd = float(nl_ltd)
    return touched


def run_noise_grid(bundle, sigma_c2c_values: Sequence[float],
                   sigma_d2d_values: Sequence[float], eval_runs: int,
                   logger: RunLogger, device_profile: Optional[DeviceProfile] = None,
                   resample_d2d_each_point: bool = True,
                   noise_mode_override: Optional[str] = None):
    rows: List[dict] = []
    sparsity_rows: List[dict] = []
    logger.log("Running continuous noise sweep.")
    set_uniform_retention(bundle.model, 0.0)

    for sigma_d2d in sigma_d2d_values:
        for sigma_c2c in sigma_c2c_values:
            noise_enabled = (sigma_c2c > 0) or (sigma_d2d > 0)
            set_uniform_noise(
                bundle.model,
                sigma_c2c=float(sigma_c2c),
                sigma_d2d=float(sigma_d2d),
                noise_enabled=noise_enabled,
                resample_d2d=resample_d2d_each_point,
                noise_mode=noise_mode_override,
            )
            label = f"sigma_c2c={sigma_c2c:.2f}, sigma_d2d={sigma_d2d:.2f}"
            summary, sparsity_report = run_mc_eval(
                bundle, eval_runs=eval_runs, logger=logger, label=label, collect_sparsity=True
            )
            row = row_base(bundle, "noise", device_profile=device_profile)
            row.update({
                "sigma_c2c": float(sigma_c2c),
                "sigma_d2d": float(sigma_d2d),
                "adc_bits": None,
                "adc_label": "native",
            })
            row.update(summary)
            rows.append(row)
            sparsity_rows.extend(build_sparsity_rows(bundle, sparsity_report, context={
                "analysis_type": "noise_sweep",
                "sweep_type": "noise",
                "sigma_c2c": float(sigma_c2c),
                "sigma_d2d": float(sigma_d2d),
                "adc_label": "native",
            }))
    return rows, sparsity_rows


def run_adc_sweep(bundle, adc_bits_values: Sequence[Optional[int]], eval_runs: int,
                  calibration_batches: int, logger: RunLogger,
                  base_sigma_c2c: Optional[float] = None,
                  base_sigma_d2d: Optional[float] = None,
                  device_profile: Optional[DeviceProfile] = None,
                  noise_mode_override: Optional[str] = None):
    rows: List[dict] = []
    sparsity_rows: List[dict] = []
    logger.log("Calibrating analog output ranges for ADC sweep.")
    output_ranges = calibrate_adc_ranges(bundle, max_batches=calibration_batches)
    logger.log(f"Captured ADC ranges for {len(output_ranges)} analog layers.")

    set_uniform_retention(bundle.model, 0.0)
    active_sigma_c2c = float(bundle.exp_cfg.sigma_c2c if base_sigma_c2c is None else base_sigma_c2c)
    active_sigma_d2d = float(bundle.exp_cfg.sigma_d2d if base_sigma_d2d is None else base_sigma_d2d)
    set_uniform_noise(
        bundle.model,
        sigma_c2c=active_sigma_c2c,
        sigma_d2d=active_sigma_d2d,
        noise_enabled=bool((active_sigma_c2c > 0.0) or (active_sigma_d2d > 0.0)),
        noise_mode=noise_mode_override,
    )

    for adc_bits in adc_bits_values:
        label = adc_bits_label(adc_bits)
        logger.log(f"Running ADC sweep point: {label}")
        with ADCQuantHookManager(bundle.model, output_ranges, adc_bits=adc_bits):
            summary, sparsity_report = run_mc_eval(
                bundle, eval_runs=eval_runs, logger=logger, label=label, collect_sparsity=True
            )
        row = row_base(bundle, "adc", device_profile=device_profile)
        row.update({
            "sigma_c2c": active_sigma_c2c,
            "sigma_d2d": active_sigma_d2d,
            "adc_bits": adc_bits,
            "adc_label": label,
            "adc_calibration_batches": calibration_batches,
        })
        row.update(summary)
        rows.append(row)
        sparsity_rows.extend(build_sparsity_rows(bundle, sparsity_report, context={
            "analysis_type": "noise_sweep",
            "sweep_type": "adc",
            "sigma_c2c": active_sigma_c2c,
            "sigma_d2d": active_sigma_d2d,
            "adc_label": label,
        }))
    return rows, sparsity_rows


def build_markdown(current_rows: List[dict], merged_rows: List[dict], args,
                   device_profile: Optional[DeviceProfile]) -> str:
    lines = [
        "# Noise Sweep Results (GPT)",
        "",
        f"- Generated: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`",
        f"- Model: `{args.model_type}`",
        f"- Experiment: `{args.experiment}`",
        f"- Sweep type: `{args.sweep_type}`",
        f"- Eval runs per point: `{args.eval_runs}`",
        f"- Checkpoint: `{args.checkpoint or 'auto'}`",
        f"- Device profile: `{device_profile.device_type if device_profile else 'checkpoint default / literature prior'}`",
        f"- Noise mode override: `{args.noise_mode or 'checkpoint/profile default'}`",
        f"- D2D handling: `{'preserve checkpoint instance' if args.preserve_checkpoint_d2d else 'resample per sweep point'}`",
        "",
        "## Current Invocation",
        "",
        "| Sweep | Sigma C2C | Sigma D2D | ADC | Accuracy |",
        "|:------|-----------:|-----------:|:----|:---------|",
    ]
    for row in current_rows:
        lines.append(
            f"| {row['sweep_type']} | {row.get('sigma_c2c', '')} | {row.get('sigma_d2d', '')} | "
            f"{row.get('adc_label', 'native')} | "
            f"{row['test_acc_mean']:.2f} +/- {row['test_acc_std']:.2f}% ({row['eval_runs']} runs) |"
        )

    lines.extend([
        "",
        "## Combined Artifact Summary",
        "",
        f"- Total rows in merged artifact: `{len(merged_rows)}`",
        f"- JSON: `{asset_path(args.output_dir, 'json', args.json_name)}`",
        f"- CSV: `{asset_path(args.output_dir, 'csv', args.csv_name)}`",
        f"- Figure refreshed: `{args.figure_output_dir}/fig9_noise_sensitivity.png`",
        "",
        "## Notes",
        "",
        "- `noise` sweep scans the continuous `(sigma_c2c, sigma_d2d)` grid with retention disabled.",
        "- `adc` sweep keeps the checkpoint's base noise regime and adds fixed per-layer ADC quantizers during inference.",
        "- When `--device-profile-json` is provided, array dynamic range, state count, and optional retention constants are loaded from the measured profile before the sweep-specific overrides are applied.",
        "- Results are GPT-scoped append-only scratch artifacts for the paper pipeline.",
        "",
    ])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Run inference-only noise or ADC sweeps.")
    parser.add_argument("--model-type", choices=["tinyvit", "convnext"], required=True)
    parser.add_argument("--experiment", type=str, default=None,
                        help="Tiny-ViT uses V4 by default; ConvNeXt uses C4 by default.")
    parser.add_argument("--checkpoint", type=str, default=None)
    parser.add_argument("--checkpoint-dir", type=str, default="checkpoints")
    parser.add_argument("--dataset", type=str, default="cifar10")
    parser.add_argument("--data-root", type=str, default="./data")
    parser.add_argument("--num-workers", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=None)
    parser.add_argument("--device", type=str, default=None)
    parser.add_argument("--eval-runs", type=int, default=10)
    parser.add_argument("--amp", action="store_true")
    parser.add_argument("--sweep-type", choices=["noise", "adc"], default="noise")
    parser.add_argument("--sigma-c2c-values", nargs="+", type=float, default=DEFAULT_SIGMA_C2C)
    parser.add_argument("--sigma-d2d-values", nargs="+", type=float, default=DEFAULT_SIGMA_D2D)
    parser.add_argument("--adc-bits", nargs="+", default=DEFAULT_ADC_BITS)
    parser.add_argument("--adc-calibration-batches", type=int, default=1)
    parser.add_argument("--output-dir", type=str, default="report_md/_gpt")
    parser.add_argument("--json-name", type=str, default="noise_sweep_results_gpt.json")
    parser.add_argument("--csv-name", type=str, default="noise_sweep_results_gpt.csv")
    parser.add_argument("--sparsity-json-name", type=str, default="activation_sparsity_gpt.json")
    parser.add_argument("--sparsity-csv-name", type=str, default="activation_sparsity_gpt.csv")
    parser.add_argument("--report-name", type=str, default="noise_sweep_report_gpt.md")
    parser.add_argument("--figure-output-dir", type=str, default="paper/figures")
    parser.add_argument("--log-path", type=str, default="logs/_gpt/noise_sweep_gpt.log")
    parser.add_argument("--device-profile-json", type=str, default=None,
                        help="Optional measured-device profile JSON. Use with a single profile or pass --profile-name.")
    parser.add_argument("--profile-name", type=str, default=None,
                        help="Profile name inside --device-profile-json when multiple entries are present.")
    parser.add_argument("--noise-mode", choices=["uniform", "proportional"], default=None,
                        help="Override noise mode for all analog layers without changing the checkpoint identity.")
    parser.add_argument("--nl-ltp", type=float, default=None,
                        help="Optional inference-side NL_LTP override for all analog layers.")
    parser.add_argument("--nl-ltd", type=float, default=None,
                        help="Optional inference-side NL_LTD override for all analog layers.")
    parser.add_argument("--preserve-checkpoint-d2d", action="store_true",
                        help="Keep checkpoint D2D buffers instead of resampling them at each noise sweep point.")
    args = parser.parse_args()

    args.experiment = args.experiment or default_experiment_for(args.model_type)
    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")
    logger = RunLogger(args.log_path)

    try:
        logger.log(f"Device: {device}")
        logger.log(f"Model type: {args.model_type}")
        logger.log(f"Experiment: {args.experiment}")
        logger.log(f"Sweep type: {args.sweep_type}")
        logger.log(f"Eval runs: {args.eval_runs}")
        device_profile = resolve_device_profile(args.device_profile_json, args.profile_name)
        if device_profile is not None:
            logger.log(
                f"Measured profile: {device_profile.device_type} "
                f"(G_range={device_profile.dynamic_range}x, n_states={device_profile.n_states}, "
                f"c2c={device_profile.sigma_c2c}, d2d={device_profile.sigma_d2d})"
            )
        bundle = load_model_bundle(
            model_type=args.model_type,
            experiment=args.experiment,
            device=device,
            checkpoint_path=args.checkpoint,
            checkpoint_dir=args.checkpoint_dir,
            dataset=args.dataset,
            data_root=args.data_root,
            num_workers=args.num_workers,
            batch_size=args.batch_size,
            amp_enabled=args.amp,
        )
        logger.log(f"Checkpoint: {bundle.checkpoint_path}")
        logger.log(f"Checkpoint epoch: {bundle.checkpoint_epoch}, best_acc={bundle.checkpoint_best_acc}")
        if device_profile is not None:
            analog_layers = apply_device_profile(bundle.model, device_profile, resample_d2d=True)
            logger.log(f"Applied measured profile to {analog_layers} analog layers.")
        if any(v is not None for v in (args.noise_mode, args.nl_ltp, args.nl_ltd)):
            overridden = apply_override_config(
                bundle,
                noise_mode=args.noise_mode,
                nl_ltp=args.nl_ltp,
                nl_ltd=args.nl_ltd,
            )
            logger.log(
                f"Applied direct overrides to {overridden} analog layers "
                f"(noise_mode={args.noise_mode}, NL_LTP={args.nl_ltp}, NL_LTD={args.nl_ltd})."
            )

        if args.sweep_type == "noise":
            current_rows, current_sparsity_rows = run_noise_grid(
                bundle,
                sigma_c2c_values=args.sigma_c2c_values,
                sigma_d2d_values=args.sigma_d2d_values,
                eval_runs=args.eval_runs,
                logger=logger,
                device_profile=device_profile,
                resample_d2d_each_point=not args.preserve_checkpoint_d2d,
                noise_mode_override=args.noise_mode,
            )
        else:
            current_rows, current_sparsity_rows = run_adc_sweep(
                bundle,
                adc_bits_values=parse_adc_bits(args.adc_bits),
                eval_runs=args.eval_runs,
                calibration_batches=args.adc_calibration_batches,
                logger=logger,
                base_sigma_c2c=device_profile.sigma_c2c if device_profile else None,
                base_sigma_d2d=device_profile.sigma_d2d if device_profile else None,
                device_profile=device_profile,
                noise_mode_override=args.noise_mode,
            )

        json_path = asset_path(args.output_dir, "json", args.json_name)
        csv_path = asset_path(args.output_dir, "csv", args.csv_name)
        existing_rows = load_existing_results(json_path)
        merged_rows = merge_rows(
            existing_rows,
            current_rows,
            key_fields=("model", "experiment", "sweep_type", "sigma_c2c", "sigma_d2d", "adc_label"),
        )
        metadata = {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "last_model": args.model_type,
            "last_experiment": args.experiment,
            "last_sweep_type": args.sweep_type,
            "eval_runs": args.eval_runs,
            "profile_source": args.device_profile_json or "checkpoint_default",
            "noise_mode_override": args.noise_mode,
            "preserve_checkpoint_d2d": bool(args.preserve_checkpoint_d2d),
        }
        export_rows(merged_rows, json_path=json_path, csv_path=csv_path, metadata=metadata)

        sparsity_json_path = asset_path(args.output_dir, "json", args.sparsity_json_name)
        sparsity_csv_path = asset_path(args.output_dir, "csv", args.sparsity_csv_name)
        existing_sparsity_rows = load_existing_results(sparsity_json_path)
        merged_sparsity_rows = merge_rows(
            existing_sparsity_rows,
            current_sparsity_rows,
            key_fields=("model", "experiment", "analysis_type", "sweep_type", "sigma_c2c", "sigma_d2d", "adc_label", "layer"),
        )
        export_rows(merged_sparsity_rows, json_path=sparsity_json_path, csv_path=sparsity_csv_path, metadata=metadata)

        report_path = os.path.join(args.output_dir, args.report_name)
        os.makedirs(args.output_dir, exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as fh:
            fh.write(build_markdown(current_rows, merged_rows, args, device_profile))

        configure_style()
        figure_dir = Path(args.figure_output_dir)
        ensure_dir(figure_dir)
        plot_fig9_noise_sensitivity(figure_dir)

        logger.log(f"Merged rows written: {len(merged_rows)}")
        logger.log(f"JSON: {json_path}")
        logger.log(f"CSV: {csv_path}")
        logger.log(f"Sparsity CSV: {sparsity_csv_path}")
        logger.log(f"Report: {report_path}")
        logger.log(f"Figure: {figure_dir / 'fig9_noise_sensitivity.png'}")
    finally:
        logger.close()


if __name__ == "__main__":
    main()
