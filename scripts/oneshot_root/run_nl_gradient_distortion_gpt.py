#!/usr/bin/env python3
"""Group-wise nonlinear-write gradient-distortion diagnostic for Tiny-ViT.

This script addresses the remaining mechanistic question around severe
nonlinear write (`NL=2.0`) without launching another slow end-to-end training
suite. Because the current analog layer implementation uses `NL` only in the
backward surrogate, the forward loss under matched settings is unchanged while
the gradient field is distorted. We therefore measure how much the gradient
direction and magnitude change when `NL=2.0` is activated only for selected
analog module groups.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Callable, Iterable, List, Sequence, Tuple

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F

from inference_analysis_utils import (
    iter_analog_modules,
    load_model_bundle,
    restore_analog_state,
    snapshot_analog_state,
)
from train_tinyvit import get_dataloaders, set_seed


DEFAULT_JSON_PATH = "report_md/_gpt/json_gpt/nl_gradient_distortion_gpt.json"
DEFAULT_MD_PATH = "report_md/_gpt/nl_gradient_distortion_gpt.md"
DEFAULT_FIG_PATH = "paper/figures/fig_nl_gradient_distortion.png"
DEFAULT_LOG_PATH = "logs/_gpt/nl_gradient_distortion_gpt.log"


LayerSelector = Callable[[str], bool]


def tinyvit_groups() -> List[Tuple[str, str, LayerSelector]]:
    return [
        ("P", "Patch Embed", lambda name: name.startswith("patch_embed.") and ".conv" in name),
        ("Q", "Attention QKV", lambda name: ".attn.qkv" in name),
        ("R", "Attention Proj", lambda name: ".attn.proj" in name),
        ("M", "MLP", lambda name: ".mlp.fc1" in name or ".mlp.fc2" in name),
        ("A", "All analog", lambda _name: True),
    ]


class FileLogger:
    def __init__(self, path: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = self.path.open("w", encoding="utf-8")

    def log(self, message: str = "") -> None:
        print(message, flush=True)
        self._fh.write(message + "\n")
        self._fh.flush()

    def close(self) -> None:
        self._fh.close()


def configure_matched_forward_path(model: torch.nn.Module, sigma_d2d: float, noise_mode: str) -> int:
    active = 0
    for _name, module in iter_analog_modules(model):
        module.config.noise_enabled = sigma_d2d > 0.0
        module.config.sigma_c2c = 0.0
        module.config.sigma_d2d = sigma_d2d
        module.config.noise_mode = noise_mode
        module.config.NL_LTP = 1.0
        module.config.NL_LTD = -1.0
        active += 1
    return active


def set_group_nl(model: torch.nn.Module, selector: LayerSelector, nl_value: float) -> Tuple[List[str], int]:
    selected: List[str] = []
    total = 0
    for name, module in iter_analog_modules(model):
        total += 1
        if selector(name):
            module.config.NL_LTP = nl_value
            module.config.NL_LTD = -nl_value
            selected.append(name)
        else:
            module.config.NL_LTP = 1.0
            module.config.NL_LTD = -1.0
    return selected, total


def param_names_for_modules(model: torch.nn.Module, module_names: Sequence[str]) -> List[str]:
    requested = set(module_names)
    names: List[str] = []
    for module_name, module in model.named_modules():
        if module_name not in requested:
            continue
        for param_name, _param in module.named_parameters(recurse=False):
            full_name = f"{module_name}.{param_name}" if module_name else param_name
            names.append(full_name)
    return names


def flatten_grads(named_parameters: Iterable[Tuple[str, torch.nn.Parameter]],
                  selected_names: Sequence[str] | None = None) -> torch.Tensor:
    selected = set(selected_names) if selected_names is not None else None
    chunks: List[torch.Tensor] = []
    for name, param in named_parameters:
        if selected is not None and name not in selected:
            continue
        if param.grad is None:
            continue
        chunks.append(param.grad.detach().float().reshape(-1).cpu())
    if not chunks:
        return torch.zeros(1, dtype=torch.float32)
    return torch.cat(chunks, dim=0)


def cosine_similarity(a: torch.Tensor, b: torch.Tensor) -> float:
    if a.numel() == 0 or b.numel() == 0:
        return float("nan")
    if float(a.norm().item()) == 0.0 or float(b.norm().item()) == 0.0:
        return float("nan")
    value = float(F.cosine_similarity(a, b, dim=0).item())
    return max(-1.0, min(1.0, value))


def norm_ratio(a: torch.Tensor, b: torch.Tensor) -> float:
    denom = float(a.norm().item())
    if denom == 0.0:
        return float("nan")
    return float(b.norm().item() / denom)


def sign_flip_rate(a: torch.Tensor, b: torch.Tensor, eps: float = 1e-10) -> float:
    mask = (a.abs() > eps) & (b.abs() > eps)
    active = int(mask.sum().item())
    if active == 0:
        return float("nan")
    flips = ((a[mask] > 0) != (b[mask] > 0)).float().mean().item()
    return float(flips)


def backward_pass(model: torch.nn.Module, inputs: torch.Tensor, targets: torch.Tensor,
                  criterion: torch.nn.Module) -> float:
    model.zero_grad(set_to_none=True)
    outputs = model(inputs)
    loss = criterion(outputs, targets)
    loss_value = float(loss.detach().item())
    loss.backward(retain_graph=True)
    del outputs
    del loss
    return loss_value


def build_markdown(rows: List[dict], meta: dict) -> str:
    lines = [
        "# NL Gradient Distortion Diagnostic",
        "",
        f"- Generated: `{meta['generated_at']}`",
        f"- Experiment: `{meta['experiment']}`",
        f"- Dataset: `{meta['dataset']}`",
        f"- Batches: `{meta['max_batches']}`",
        f"- Batch size: `{meta['batch_size']}`",
        f"- Matched forward path: `sigma_c2c=0`, preserved D2D, eval-mode deterministic backprop",
        "",
        "| Group | Affected Modules | Full-Grad Cosine | Affected-Grad Cosine | Full Norm Ratio | Affected Norm Ratio | Affected Sign-Flip | Mean Loss Delta |",
        "|:--|--:|--:|--:|--:|--:|--:|--:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['group_label']} | {row['affected_modules']}/{row['total_analog_modules']} | "
            f"{row['full_grad_cosine_mean']:.4f} | {row['affected_grad_cosine_mean']:.4f} | "
            f"{row['full_grad_norm_ratio_mean']:.4f} | {row['affected_grad_norm_ratio_mean']:.4f} | "
            f"{row['affected_sign_flip_rate_mean']:.4f} | {row['loss_delta_mean']:+.6f} |"
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        "- `Mean Loss Delta` staying near zero confirms that this diagnostic is measuring backward-surrogate distortion rather than a forward-path mismatch.",
        "- Lower cosine similarity indicates stronger gradient-direction distortion under `NL=2.0` for the selected module group.",
        "- Higher sign-flip rate indicates a larger fraction of affected parameters whose gradient direction reverses relative to the linear-surrogate baseline.",
        "",
    ])
    return "\n".join(lines) + "\n"


def plot_rows(rows: List[dict], figure_path: str) -> None:
    figure = Path(figure_path)
    figure.parent.mkdir(parents=True, exist_ok=True)

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
        "font.family": "serif",
        "font.serif": ["STIXGeneral", "DejaVu Serif"],
        "mathtext.fontset": "stix",
    })

    labels = [row["group_label"] for row in rows]
    full_cos = [row["full_grad_cosine_mean"] for row in rows]
    affected_cos = [row["affected_grad_cosine_mean"] for row in rows]
    sign_flip = [row["affected_sign_flip_rate_mean"] * 100.0 for row in rows]

    x = torch.arange(len(rows)).numpy()
    width = 0.36
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 4.2))

    axes[0].bar(x - width / 2, full_cos, width=width, color="#35618f", label="Full gradient")
    axes[0].bar(x + width / 2, affected_cos, width=width, color="#d57a3a", label="Affected params")
    axes[0].set_ylim(0.0, 1.02)
    axes[0].set_ylabel("Cosine similarity vs NL=1 baseline")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels, rotation=20, ha="right")
    axes[0].grid(axis="y", linestyle=":", linewidth=0.8, alpha=0.6)
    axes[0].legend(frameon=True)

    axes[1].bar(x, sign_flip, width=0.58, color="#8e4c6d")
    axes[1].set_ylabel("Sign-flip rate on affected params (%)")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels, rotation=20, ha="right")
    axes[1].grid(axis="y", linestyle=":", linewidth=0.8, alpha=0.6)

    fig.suptitle("Group-wise NL=2.0 gradient distortion on Tiny-ViT V4", y=1.02, fontsize=13)
    fig.tight_layout()
    fig.savefig(figure, bbox_inches="tight")
    fig.savefig(figure.with_suffix(".pdf"), bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment", default="V4")
    parser.add_argument("--dataset", default="cifar10")
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--checkpoint-path", default=None)
    parser.add_argument("--checkpoint-dir", default="checkpoints")
    parser.add_argument("--data-root", default="./data")
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--num-workers", type=int, default=2)
    parser.add_argument("--max-batches", type=int, default=8)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--json-path", default=DEFAULT_JSON_PATH)
    parser.add_argument("--md-path", default=DEFAULT_MD_PATH)
    parser.add_argument("--figure-path", default=DEFAULT_FIG_PATH)
    parser.add_argument("--log-path", default=DEFAULT_LOG_PATH)
    args = parser.parse_args()

    logger = FileLogger(args.log_path)
    set_seed(args.seed)
    logger.log("=" * 78)
    logger.log("NL gradient distortion diagnostic")
    logger.log("=" * 78)
    logger.log(f"Device: {args.device}")
    logger.log(f"Experiment: {args.experiment}")
    logger.log(f"Dataset: {args.dataset}")
    logger.log(f"Batch size: {args.batch_size}")
    logger.log(f"Max batches: {args.max_batches}")

    bundle = load_model_bundle(
        model_type="tinyvit",
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
    probe_bundle = load_model_bundle(
        model_type="tinyvit",
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
    trainloader, _ = get_dataloaders(
        dataset=args.dataset,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        data_root=args.data_root,
    )
    logger.log(f"Checkpoint: {bundle.checkpoint_path}")
    logger.log(f"Checkpoint epoch: {bundle.checkpoint_epoch}, best_acc={bundle.checkpoint_best_acc}")

    baseline_snapshot = snapshot_analog_state(bundle.model)
    probe_snapshot = snapshot_analog_state(probe_bundle.model)
    try:
        total_analog = configure_matched_forward_path(
            bundle.model,
            sigma_d2d=float(bundle.exp_cfg.sigma_d2d),
            noise_mode=str(bundle.exp_cfg.noise_mode),
        )
        configure_matched_forward_path(
            probe_bundle.model,
            sigma_d2d=float(probe_bundle.exp_cfg.sigma_d2d),
            noise_mode=str(probe_bundle.exp_cfg.noise_mode),
        )
        logger.log(
            "Matched forward path configured: "
            f"{total_analog} analog modules, sigma_c2c=0.0, sigma_d2d={bundle.exp_cfg.sigma_d2d}, "
            f"noise_mode={bundle.exp_cfg.noise_mode}"
        )
        bundle.model.eval()
        probe_bundle.model.eval()
        criterion = bundle.criterion

        metric_rows: List[dict] = []
        group_defs = tinyvit_groups()

        batches = []
        for batch_idx, (inputs, targets) in enumerate(trainloader):
            if batch_idx >= args.max_batches:
                break
            batches.append((inputs.to(args.device), targets.to(args.device)))
        logger.log(f"Captured {len(batches)} train batches for gradient diagnostics")

        baseline_named_params = list(bundle.model.named_parameters())
        probe_named_params = list(probe_bundle.model.named_parameters())

        for group_id, group_label, selector in group_defs:
            set_group_nl(bundle.model, selector=lambda _name: False, nl_value=1.0)
            set_group_nl(probe_bundle.model, selector=lambda _name: False, nl_value=1.0)
            selected_module_names, _ = set_group_nl(probe_bundle.model, selector=selector, nl_value=2.0)
            affected_param_names = param_names_for_modules(probe_bundle.model, selected_module_names)
            logger.log(
                f"Group {group_id} ({group_label}): affected_modules={len(selected_module_names)}/{total_analog}, "
                f"affected_params={len(affected_param_names)} tensors"
            )

            full_cosines: List[float] = []
            affected_cosines: List[float] = []
            full_ratios: List[float] = []
            affected_ratios: List[float] = []
            sign_flips: List[float] = []
            loss_deltas: List[float] = []

            for batch_idx, (inputs, targets) in enumerate(batches, start=1):
                base_loss = backward_pass(bundle.model, inputs, targets, criterion)
                base_full_grad = flatten_grads(baseline_named_params)
                base_group_grad = flatten_grads(baseline_named_params, selected_names=affected_param_names)

                perturbed_loss = backward_pass(probe_bundle.model, inputs, targets, criterion)
                perturbed_full_grad = flatten_grads(probe_named_params)
                perturbed_group_grad = flatten_grads(probe_named_params, selected_names=affected_param_names)

                full_cosines.append(cosine_similarity(base_full_grad, perturbed_full_grad))
                affected_cosines.append(cosine_similarity(base_group_grad, perturbed_group_grad))
                full_ratios.append(norm_ratio(base_full_grad, perturbed_full_grad))
                affected_ratios.append(norm_ratio(base_group_grad, perturbed_group_grad))
                sign_flips.append(sign_flip_rate(base_group_grad, perturbed_group_grad))
                loss_deltas.append(perturbed_loss - base_loss)

                logger.log(
                    f"  batch={batch_idx}/{len(batches)} "
                    f"full_cos={full_cosines[-1]:.4f} "
                    f"affected_cos={affected_cosines[-1]:.4f} "
                    f"sign_flip={sign_flips[-1]:.4f} "
                    f"loss_delta={loss_deltas[-1]:+.6f}"
                )

            metric_rows.append({
                "group_id": group_id,
                "group_label": group_label,
                "affected_module_names": selected_module_names,
                "affected_modules": len(selected_module_names),
                "total_analog_modules": total_analog,
                "affected_param_tensors": len(affected_param_names),
                "full_grad_cosine_mean": mean(full_cosines),
                "affected_grad_cosine_mean": mean(affected_cosines),
                "full_grad_norm_ratio_mean": mean(full_ratios),
                "affected_grad_norm_ratio_mean": mean(affected_ratios),
                "affected_sign_flip_rate_mean": mean(sign_flips),
                "loss_delta_mean": mean(loss_deltas),
            })

        metric_rows.sort(key=lambda row: row["affected_grad_cosine_mean"])
        meta = {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "experiment": args.experiment,
            "dataset": args.dataset,
            "batch_size": args.batch_size,
            "max_batches": len(batches),
            "checkpoint_path": bundle.checkpoint_path,
            "checkpoint_epoch": bundle.checkpoint_epoch,
            "checkpoint_best_acc": bundle.checkpoint_best_acc,
            "matched_forward_sigma_d2d": float(bundle.exp_cfg.sigma_d2d),
            "matched_forward_sigma_c2c": 0.0,
        }

        json_path = Path(args.json_path)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(
            json.dumps({"metadata": meta, "results": metric_rows}, indent=2),
            encoding="utf-8",
        )

        md_path = Path(args.md_path)
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_path.write_text(
            build_markdown(metric_rows, meta),
            encoding="utf-8",
        )

        plot_rows(metric_rows, args.figure_path)
        logger.log(f"JSON written: {json_path}")
        logger.log(f"Markdown written: {md_path}")
        logger.log(f"Figure written: {args.figure_path}")
    finally:
        restore_analog_state(bundle.model, baseline_snapshot)
        restore_analog_state(probe_bundle.model, probe_snapshot)
        logger.close()


if __name__ == "__main__":
    main()
