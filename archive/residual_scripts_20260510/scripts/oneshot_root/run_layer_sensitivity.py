#!/usr/bin/env python3
"""Inference-only layer-wise noise sensitivity analysis."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Callable, Dict, List, Sequence, Tuple

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import torch

from analog_layers import resample_d2d_buffers
from inference_analysis_utils import (
    build_sparsity_rows,
    export_rows,
    iter_analog_modules,
    load_existing_results,
    load_model_bundle,
    merge_rows,
    run_mc_eval,
    snapshot_analog_state,
    restore_analog_state,
    set_uniform_retention,
)
from report_asset_paths import asset_path
from train_tinyvit import RunLogger


LayerSelector = Callable[[str], bool]


def default_experiment_for(model_type: str) -> str:
    return "V4" if model_type == "tinyvit" else "C4"


def tinyvit_groups() -> List[Tuple[str, str, LayerSelector]]:
    return [
        ("A", "Attention QKV", lambda name: ".attn.qkv" in name),
        ("B", "Attention Proj", lambda name: ".attn.proj" in name),
        ("C", "FFN fc1+fc2", lambda name: ".mlp.fc1" in name or ".mlp.fc2" in name),
        ("D", "Patch Embed", lambda name: name.startswith("patch_embed.") and ".conv" in name),
        ("E", "All analog", lambda _name: True),
        ("F", "All layers C2C off", lambda _name: False),
    ]


def convnext_groups() -> List[Tuple[str, str, LayerSelector]]:
    return [
        ("A", "Pointwise fc1", lambda name: name.endswith(".block.3")),
        ("B", "Pointwise fc2", lambda name: name.endswith(".block.5")),
        ("C", "Stem/Downsample", lambda name: name in {"features.0.0", "features.2.1", "features.4.1", "features.6.1"}),
        ("D", "Classifier", lambda name: name == "classifier.2"),
        ("E", "All analog", lambda _name: True),
        ("F", "All layers C2C off", lambda _name: False),
    ]


def group_specs_for(model_type: str) -> List[Tuple[str, str, LayerSelector]]:
    if model_type == "tinyvit":
        return tinyvit_groups()
    if model_type == "convnext":
        return convnext_groups()
    raise ValueError(f"Unsupported model type: {model_type}")


def apply_group_noise(model, sigma_c2c: float, sigma_d2d: float, selector: LayerSelector,
                      resample_d2d: bool = False) -> Tuple[int, int]:
    total = 0
    active = 0
    for name, module in iter_analog_modules(model):
        total += 1
        enabled = bool(selector(name))
        # Canonical Task 15 isolates C2C sensitivity while preserving the
        # checkpoint's trained D2D instance across every analog layer.
        module.config.noise_enabled = True
        module.config.sigma_c2c = sigma_c2c if enabled else 0.0
        module.config.sigma_d2d = sigma_d2d
        if enabled:
            active += 1
    if resample_d2d:
        resample_d2d_buffers(model, selector=lambda name, _module: bool(selector(name)))
    return active, total


def row_base(bundle, d2d_instance_policy: str, layer_sensitivity_mode: str) -> dict:
    return {
        "model": bundle.model_type,
        "experiment": bundle.experiment,
        "experiment_name": bundle.experiment_name,
        "dataset": bundle.dataset,
        "checkpoint_path": bundle.checkpoint_path,
        "checkpoint_epoch": bundle.checkpoint_epoch,
        "checkpoint_best_acc": bundle.checkpoint_best_acc,
        "sigma_c2c": float(bundle.exp_cfg.sigma_c2c),
        "sigma_d2d": float(bundle.exp_cfg.sigma_d2d),
        "amp_enabled": bundle.amp_enabled,
        "d2d_instance_policy": d2d_instance_policy,
        "layer_sensitivity_mode": layer_sensitivity_mode,
    }


def run_groups(bundle, eval_runs: int, groups: Sequence[Tuple[str, str, LayerSelector]],
               logger: RunLogger, resample_d2d: bool):
    rows: List[dict] = []
    sparsity_rows: List[dict] = []
    set_uniform_retention(bundle.model, 0.0)
    d2d_instance_policy = (
        "fresh_resampled_for_noisy_layers" if resample_d2d else "checkpoint_preserved"
    )
    layer_sensitivity_mode = (
        "fresh_instance_group_ablation" if resample_d2d else "c2c_isolation_on_checkpoint_d2d"
    )
    for group_id, group_label, selector in groups:
        active, total = apply_group_noise(
            bundle.model,
            sigma_c2c=float(bundle.exp_cfg.sigma_c2c),
            sigma_d2d=float(bundle.exp_cfg.sigma_d2d),
            selector=selector,
            resample_d2d=resample_d2d,
        )
        logger.log(f"Group {group_id} ({group_label}): noisy_layers={active}/{total}")
        summary, sparsity_report = run_mc_eval(
            bundle, eval_runs=eval_runs, logger=logger, label=f"group={group_id}", collect_sparsity=True
        )
        row = row_base(
            bundle,
            d2d_instance_policy=d2d_instance_policy,
            layer_sensitivity_mode=layer_sensitivity_mode,
        )
        row.update({
            "phase": "isolated",
            "group_id": group_id,
            "group_label": group_label,
            "noisy_layers": active,
            "total_analog_layers": total,
        })
        row.update(summary)
        rows.append(row)
        sparsity_rows.extend(build_sparsity_rows(bundle, sparsity_report, context={
            "analysis_type": "layer_sensitivity",
            "phase": "isolated",
            "group_id": group_id,
            "group_label": group_label,
        }))
    return rows, sparsity_rows


def phase1_rows_for_ranking(rows: Sequence[dict], model_type: str, experiment: str) -> List[dict]:
    return [
        row for row in rows
        if row.get("model") == model_type
        and row.get("experiment") == experiment
        and row.get("phase", "isolated") == "isolated"
    ]


def rank_group_drops(phase1_rows: Sequence[dict]) -> List[dict]:
    clean_row = next((row for row in phase1_rows if row.get("group_id") == "F"), None)
    if clean_row is None:
        raise ValueError("Phase 2 requires the clean control group F in Phase 1 results.")
    clean_acc = float(clean_row["test_acc_mean"])
    ranked = []
    for row in phase1_rows:
        group_id = row.get("group_id")
        if group_id in {"E", "F"}:
            continue
        ranked.append({
            "group_id": group_id,
            "group_label": row.get("group_label", group_id),
            "test_acc_mean": float(row["test_acc_mean"]),
            "accuracy_drop": clean_acc - float(row["test_acc_mean"]),
        })
    ranked.sort(key=lambda item: item["accuracy_drop"])
    return ranked


def select_robust_groups_for_phase2(phase1_rows: Sequence[dict], top_k: int) -> List[str]:
    ranked = rank_group_drops(phase1_rows)
    return [item["group_id"] for item in ranked[:max(0, top_k)]]


def run_phase2_mixed(bundle, eval_runs: int, phase1_rows: Sequence[dict],
                     group_specs: Sequence[Tuple[str, str, LayerSelector]],
                     top_k_robust: int, pessimistic_n_states: int,
                     pessimistic_sigma_c2c: float, pessimistic_sigma_d2d: float,
                     logger: RunLogger):
    selected_group_ids = select_robust_groups_for_phase2(phase1_rows, top_k=top_k_robust)
    if not selected_group_ids:
        return None, []

    selector_by_group = {group_id: selector for group_id, _label, selector in group_specs}
    label_by_group = {group_id: label for group_id, label, _selector in group_specs}
    snapshot = snapshot_analog_state(bundle.model)
    selected_labels = [label_by_group[group_id] for group_id in selected_group_ids]
    selected_set = set(selected_group_ids)

    pessimistic_layers = 0
    total_layers = 0
    try:
        set_uniform_retention(bundle.model, 0.0)
        for name, module in iter_analog_modules(bundle.model):
            total_layers += 1
            module.config.n_states = int(bundle.exp_cfg.n_states)
            module.config.noise_enabled = bool(bundle.exp_cfg.noise_enabled)
            module.config.sigma_c2c = float(bundle.exp_cfg.sigma_c2c)
            module.config.sigma_d2d = float(bundle.exp_cfg.sigma_d2d)
            if any(selector_by_group[group_id](name) for group_id in selected_set):
                module.config.n_states = pessimistic_n_states
                module.config.sigma_c2c = pessimistic_sigma_c2c
                module.config.sigma_d2d = pessimistic_sigma_d2d
                pessimistic_layers += 1

        resample_d2d_buffers(
            bundle.model,
            selector=lambda name, _module: any(selector_by_group[group_id](name) for group_id in selected_set),
        )

        logger.log(
            "Phase 2 mixed projection: "
            f"robust_groups={selected_group_ids}, pessimistic_layers={pessimistic_layers}/{total_layers}"
        )
        summary, sparsity_report = run_mc_eval(
            bundle, eval_runs=eval_runs, logger=logger, label="phase2_mixed", collect_sparsity=True
        )
        row = row_base(
            bundle,
            d2d_instance_policy="fresh_resampled_for_selected_groups",
            layer_sensitivity_mode="mixed_projection",
        )
        row.update({
            "phase": "mixed",
            "group_id": "MIXED",
            "group_label": f"Mixed robust groups: {', '.join(selected_group_ids)}",
            "selected_group_ids": ",".join(selected_group_ids),
            "selected_group_labels": " | ".join(selected_labels),
            "pessimistic_layers": pessimistic_layers,
            "total_analog_layers": total_layers,
            "pessimistic_n_states": pessimistic_n_states,
            "pessimistic_sigma_c2c": pessimistic_sigma_c2c,
            "pessimistic_sigma_d2d": pessimistic_sigma_d2d,
        })
        row.update(summary)
        sparsity_rows = build_sparsity_rows(bundle, sparsity_report, context={
            "analysis_type": "layer_sensitivity",
            "phase": "mixed",
            "group_id": "MIXED",
            "group_label": row["group_label"],
            "selected_group_ids": row["selected_group_ids"],
        })
        return row, sparsity_rows
    finally:
        restore_analog_state(bundle.model, snapshot)


def build_markdown(current_rows: List[dict], merged_rows: List[dict], args) -> str:
    lines = [
        "# Layer Sensitivity Results (GPT)",
        "",
        f"- Generated: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`",
        f"- Model: `{args.model_type}`",
        f"- Experiment: `{args.experiment}`",
        f"- Eval runs per group: `{args.eval_runs}`",
        "",
        "## Current Invocation",
        "",
        "| Phase | Group | Label | Noisy/Pessimistic layers | Accuracy |",
        "|:------|:------|:------|------------------------:|:---------|",
    ]
    for row in current_rows:
        layer_field = row.get("noisy_layers", row.get("pessimistic_layers", 0))
        lines.append(
            f"| {row.get('phase', 'isolated')} | {row['group_id']} | {row['group_label']} | "
            f"{layer_field}/{row['total_analog_layers']} | "
            f"{row['test_acc_mean']:.2f} +/- {row['test_acc_std']:.2f}% ({row['eval_runs']} runs) |"
        )

    lines.extend([
        "",
        "## Combined Artifact Summary",
        "",
        f"- Total rows in merged artifact: `{len(merged_rows)}`",
        f"- JSON: `{asset_path(args.output_dir, 'json', args.json_name)}`",
        f"- CSV: `{asset_path(args.output_dir, 'csv', args.csv_name)}`",
        f"- Figure refreshed: `{args.figure_path}`",
        "",
        "## Notes",
        "",
        "- Canonical Phase 1 keeps the checkpoint's original D2D buffers for every analog layer and isolates the impact of C2C variability by turning C2C on only for the selected group.",
        "- Optional `--resample-d2d` switches Phase 1 into a stricter fresh-instance ablation mode; this is useful for diagnostics but is not the default paper-facing Task 15 setting.",
        "- Group `E` is the all-analog control and group `F` is the clean control.",
        "- Optional `phase2-mixed` reads the merged Phase 1 rows, ranks groups by accuracy drop from clean control `F`, and assigns pessimistic settings only to the top-K most robust groups.",
        "- Results are GPT-scoped append-only scratch artifacts for the paper pipeline.",
        "",
    ])
    return "\n".join(lines)


def plot_layer_sensitivity(rows: List[dict], figure_path: str):
    if not rows:
        return
    os.makedirs(os.path.dirname(figure_path), exist_ok=True)
    plt.style.use("seaborn-v0_8-paper")
    plt.rcParams.update({
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "font.size": 12,
        "axes.titlesize": 12,
        "axes.labelsize": 12,
        "legend.fontsize": 10,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
    })

    model_names = list(dict.fromkeys(row["model"] for row in rows))
    group_order = list(dict.fromkeys(row["group_id"] for row in rows))
    group_labels = {
        row["group_id"]: row["group_label"]
        for row in rows
    }

    x = np.arange(len(group_order))
    width = 0.8 / max(1, len(model_names))
    fig, ax = plt.subplots(figsize=(10.4, 4.8))

    for idx, model_name in enumerate(model_names):
        means = []
        stds = []
        for group_id in group_order:
            row = next(
                (
                    item for item in rows
                    if item["model"] == model_name and item["group_id"] == group_id
                ),
                None,
            )
            means.append(row["test_acc_mean"] if row else float("nan"))
            stds.append(row["test_acc_std"] if row else 0.0)
        ax.bar(
            x + (idx - (len(model_names) - 1) / 2) * width,
            means,
            width=width,
            yerr=stds,
            capsize=3,
            label=model_name,
        )

    ax.set_xticks(x)
    ax.set_xticklabels([group_labels[group_id] for group_id in group_order], rotation=20, ha="right")
    ax.set_ylabel("Accuracy (%)")
    ax.set_ylim(0, 100)
    ax.set_title("Layer-wise noise sensitivity")
    ax.grid(True, axis="y", alpha=0.25)
    ax.legend(frameon=True)
    fig.savefig(figure_path, bbox_inches="tight")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Run layer-wise noise sensitivity ablations.")
    parser.add_argument("--model-type", choices=["tinyvit", "convnext"], required=True)
    parser.add_argument("--experiment", type=str, default=None)
    parser.add_argument("--checkpoint", type=str, default=None)
    parser.add_argument("--checkpoint-dir", type=str, default="checkpoints")
    parser.add_argument("--dataset", type=str, default="cifar10")
    parser.add_argument("--data-root", type=str, default="./data")
    parser.add_argument("--num-workers", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=None)
    parser.add_argument("--device", type=str, default=None)
    parser.add_argument("--eval-runs", type=int, default=10)
    parser.add_argument("--amp", action="store_true")
    parser.add_argument("--groups", nargs="+", default=None,
                        help="Subset of group ids to run, e.g. --groups A C E F")
    parser.add_argument("--output-dir", type=str, default="report_md/_gpt")
    parser.add_argument("--json-name", type=str, default="layer_sensitivity_results_gpt.json")
    parser.add_argument("--csv-name", type=str, default="layer_sensitivity_results_gpt.csv")
    parser.add_argument("--sparsity-json-name", type=str, default="activation_sparsity_gpt.json")
    parser.add_argument("--sparsity-csv-name", type=str, default="activation_sparsity_gpt.csv")
    parser.add_argument("--report-name", type=str, default="layer_sensitivity_report_gpt.md")
    parser.add_argument("--figure-path", type=str, default="paper/figures/fig_layer_sensitivity.png")
    parser.add_argument("--log-path", type=str, default="logs/_gpt/layer_sensitivity_gpt.log")
    parser.add_argument("--phase2-mixed", action="store_true",
                        help="Run data-driven mixed projection after Phase 1 rows are available.")
    parser.add_argument("--resample-d2d", action="store_true",
                        help="Diagnostic mode: resample fresh D2D buffers for noisy layers in Phase 1.")
    parser.add_argument("--top-k-robust", type=int, default=2)
    parser.add_argument("--pessimistic-n-states", type=int, default=8)
    parser.add_argument("--pessimistic-sigma-c2c", type=float, default=0.10)
    parser.add_argument("--pessimistic-sigma-d2d", type=float, default=0.20)
    args = parser.parse_args()

    args.experiment = args.experiment or default_experiment_for(args.model_type)
    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")
    logger = RunLogger(args.log_path)

    try:
        logger.log(f"Device: {device}")
        logger.log(f"Model type: {args.model_type}")
        logger.log(f"Experiment: {args.experiment}")
        logger.log(f"Eval runs: {args.eval_runs}")
        logger.log(
            "Phase 1 mode: "
            + ("fresh-instance D2D resampling" if args.resample_d2d else "checkpoint D2D preserved, C2C isolated")
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

        groups = group_specs_for(args.model_type)
        if args.groups:
            selected = {token.strip().upper() for token in args.groups}
            groups = [group for group in groups if group[0] in selected]
        current_rows, current_sparsity_rows = run_groups(
            bundle, eval_runs=args.eval_runs, groups=groups, logger=logger, resample_d2d=args.resample_d2d
        )

        json_path = asset_path(args.output_dir, "json", args.json_name)
        csv_path = asset_path(args.output_dir, "csv", args.csv_name)
        existing_rows = load_existing_results(json_path)
        merged_rows = merge_rows(
            existing_rows,
            current_rows,
            key_fields=("model", "experiment", "phase", "group_id"),
        )
        if args.phase2_mixed:
            phase1_rows = phase1_rows_for_ranking(merged_rows, args.model_type, args.experiment)
            mixed_row, mixed_sparsity_rows = run_phase2_mixed(
                bundle,
                eval_runs=args.eval_runs,
                phase1_rows=phase1_rows,
                group_specs=group_specs_for(args.model_type),
                top_k_robust=args.top_k_robust,
                pessimistic_n_states=args.pessimistic_n_states,
                pessimistic_sigma_c2c=args.pessimistic_sigma_c2c,
                pessimistic_sigma_d2d=args.pessimistic_sigma_d2d,
                logger=logger,
            )
            if mixed_row is not None:
                current_rows.append(mixed_row)
                current_sparsity_rows.extend(mixed_sparsity_rows)
                merged_rows = merge_rows(
                    merged_rows,
                    [mixed_row],
                    key_fields=("model", "experiment", "phase", "group_id"),
                )
        metadata = {
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "last_model": args.model_type,
            "last_experiment": args.experiment,
            "eval_runs": args.eval_runs,
            "phase2_mixed": args.phase2_mixed,
            "resample_d2d": args.resample_d2d,
        }
        export_rows(merged_rows, json_path=json_path, csv_path=csv_path, metadata=metadata)

        sparsity_json_path = asset_path(args.output_dir, "json", args.sparsity_json_name)
        sparsity_csv_path = asset_path(args.output_dir, "csv", args.sparsity_csv_name)
        existing_sparsity_rows = load_existing_results(sparsity_json_path)
        merged_sparsity_rows = merge_rows(
            existing_sparsity_rows,
            current_sparsity_rows,
            key_fields=("model", "experiment", "analysis_type", "phase", "group_id", "layer"),
        )
        export_rows(
            merged_sparsity_rows,
            json_path=sparsity_json_path,
            csv_path=sparsity_csv_path,
            metadata=metadata,
        )

        report_path = os.path.join(args.output_dir, args.report_name)
        os.makedirs(args.output_dir, exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as fh:
            fh.write(build_markdown(current_rows, merged_rows, args))

        plot_layer_sensitivity(merged_rows, args.figure_path)

        logger.log(f"Merged rows written: {len(merged_rows)}")
        logger.log(f"JSON: {json_path}")
        logger.log(f"CSV: {csv_path}")
        logger.log(f"Sparsity CSV: {sparsity_csv_path}")
        logger.log(f"Report: {report_path}")
        logger.log(f"Figure: {args.figure_path}")
    finally:
        logger.close()


if __name__ == "__main__":
    main()
