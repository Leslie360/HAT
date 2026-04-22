#!/usr/bin/env python3
"""Zero-shot ImageNet analog deployment evaluation for Tiny-ViT."""

from __future__ import annotations

import argparse
import csv
import json
import os
from dataclasses import replace
from pathlib import Path
from statistics import mean, stdev
from typing import List, Optional

import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms

from device_profile_utils import DeviceProfile, load_device_profiles_json, select_device_profile
from inference_analysis_utils import apply_device_profile
from report_asset_paths import asset_path
from train_tinyvit import (
    TinyViTExperimentConfig,
    build_model,
    evaluate,
)
from datetime import datetime

class RunLogger:
    """Simple stdout + file logger for evaluation outputs."""
    def __init__(self, path: Optional[str] = None):
        self.path = path
        self._fh = None
        if path:
            parent = os.path.dirname(path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            self._fh = open(path, "w", encoding="utf-8")

    def log(self, message: str = ""):
        if message:
            stamped = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}"
        else:
            stamped = ""
        print(stamped)
        if self._fh is not None:
            self._fh.write(stamped + "\n")
            self._fh.flush()

    def close(self):
        if self._fh is not None:
            self._fh.close()
            self._fh = None


IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)
DEFAULT_JSON_PATH = asset_path("report_md/_gpt", "json", "imagenet_eval_results_gpt.json")
DEFAULT_CSV_PATH = asset_path("report_md/_gpt", "csv", "imagenet_eval_results_gpt.csv")
DEFAULT_MD_PATH = "report_md/_gpt/imagenet_eval_results_gpt.md"
DEFAULT_LOG_PATH = "logs/_gpt/imagenet_eval_gpt.log"


def ensure_parent_dir(path: Optional[str]):
    if not path:
        return
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def resolve_imagenet_val_dir(data_root: str, explicit_val_dir: Optional[str] = None) -> str:
    candidates: List[Path] = []
    if explicit_val_dir:
        candidates.append(Path(explicit_val_dir))

    data_root_path = Path(data_root)
    candidates.extend([
        data_root_path / "val",
        data_root_path / "validation",
        data_root_path / "imagenet" / "val",
        data_root_path / "imagenet" / "validation",
        data_root_path / "tiny-imagenet-200" / "val", # Local extraction path
    ])

    for candidate in candidates:
        if candidate.is_dir():
            return str(candidate)

    raise FileNotFoundError(
        "Could not find an ImageNet validation directory. "
        "Pass --val-dir explicitly or create one of: "
        f"{', '.join(str(path) for path in candidates)}"
    )


def get_imagenet_val_loader(val_dir: str, batch_size: int, num_workers: int,
                            max_samples: Optional[int] = None):
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(IMAGENET_MEAN, IMAGENET_STD),
    ])
    dataset = torchvision.datasets.ImageFolder(root=val_dir, transform=transform)
    if max_samples is not None:
        max_samples = max(1, min(len(dataset), max_samples))
        dataset = torch.utils.data.Subset(dataset, list(range(max_samples)))
    loader_kwargs = {
        "batch_size": batch_size,
        "num_workers": num_workers,
        "shuffle": False,
        "pin_memory": torch.cuda.is_available(),
    }
    if num_workers > 0:
        loader_kwargs["persistent_workers"] = True
    return torch.utils.data.DataLoader(dataset, **loader_kwargs), len(dataset)


def summarize_eval_runs(losses: List[float], accuracies: List[float]) -> dict:
    summary = {
        "eval_runs": len(accuracies),
        "test_loss_mean": mean(losses),
        "test_acc_mean": mean(accuracies),
        "test_acc_min": min(accuracies),
        "test_acc_max": max(accuracies),
        "test_acc_std": 0.0,
    }
    if len(accuracies) > 1:
        summary["test_acc_std"] = stdev(accuracies)
    return summary


def resolve_device_profile(profile_json: Optional[str], profile_name: Optional[str]) -> Optional[DeviceProfile]:
    if not profile_json:
        return None
    return select_device_profile(load_device_profiles_json(profile_json), profile_name)


def run_condition(label: str, exp_cfg: TinyViTExperimentConfig, device: str, val_loader,
                  checkpoint_path: Optional[str], eval_runs: int, logger: RunLogger,
                  device_profile: Optional[DeviceProfile] = None, num_classes: int = 1000):
    eval_cfg = replace(exp_cfg)
    if device_profile is not None and eval_cfg.use_hybrid:
        eval_cfg.n_states = device_profile.n_states
        if eval_cfg.noise_enabled:
            eval_cfg.sigma_c2c = device_profile.sigma_c2c
            eval_cfg.sigma_d2d = device_profile.sigma_d2d

    model = build_model(eval_cfg, num_classes=num_classes, device=device, pretrained=(num_classes == 1000))
    if checkpoint_path:
        checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
        try:
            model.load_state_dict(checkpoint["model_state_dict"])
        except RuntimeError as exc:
            raise RuntimeError(
                f"Failed to load checkpoint '{checkpoint_path}' into a 1000-class Tiny-ViT model. "
                "This usually means the checkpoint was trained for another dataset/head."
            ) from exc
        ckpt_epoch = checkpoint.get("epoch")
        ckpt_best_acc = checkpoint.get("best_acc")
    else:
        ckpt_epoch = None
        ckpt_best_acc = None

    if device_profile is not None and eval_cfg.use_hybrid:
        active_layers = apply_device_profile(model, device_profile, resample_d2d=True)
        logger.log(
            f"  measured_profile={device_profile.device_type}, analog_layers={active_layers}, "
            f"G_range={device_profile.dynamic_range}x, n_states={device_profile.n_states}"
        )

    criterion = nn.CrossEntropyLoss()
    actual_runs = eval_runs if eval_cfg.noise_enabled else 1
    losses: List[float] = []
    accuracies: List[float] = []

    logger.log("")
    logger.log("=" * 70)
    logger.log(f"Condition: {label}")
    logger.log(
        f"  hybrid={eval_cfg.use_hybrid}, noise={eval_cfg.noise_enabled}, "
        f"C2C={eval_cfg.sigma_c2c}, D2D={eval_cfg.sigma_d2d}, HAT={eval_cfg.hat_training}"
    )
    logger.log(f"  checkpoint={checkpoint_path or 'timm pretrained only'}")

    for run_idx in range(actual_runs):
        test_loss, test_acc = evaluate(
            model,
            val_loader,
            criterion,
            device,
            eval_cfg,
            amp_enabled=torch.cuda.is_available() and device.startswith("cuda"),
        )
        losses.append(test_loss)
        accuracies.append(test_acc)
        if actual_runs > 1:
            logger.log(f"  eval_run={run_idx + 1}/{actual_runs}: test_acc={test_acc:.2f}%")

    summary = summarize_eval_runs(losses, accuracies)
    logger.log(
        f"  Summary: acc={summary['test_acc_mean']:.2f}% ± {summary['test_acc_std']:.2f}"
        f" (min={summary['test_acc_min']:.2f}, max={summary['test_acc_max']:.2f})"
    )

    row = {
        "dataset": "imagenet1k",
        "condition": label,
        "use_hybrid": eval_cfg.use_hybrid,
        "noise_enabled": eval_cfg.noise_enabled,
        "sigma_c2c": eval_cfg.sigma_c2c,
        "sigma_d2d": eval_cfg.sigma_d2d,
        "hat_training": eval_cfg.hat_training,
        "device_profile": device_profile.device_type if device_profile else None,
        "profile_source": device_profile.source if device_profile else None,
        "dynamic_range": device_profile.dynamic_range if device_profile else None,
        "n_states": device_profile.n_states if device_profile else None,
        "checkpoint_path": checkpoint_path,
        "checkpoint_epoch": ckpt_epoch,
        "checkpoint_best_acc": ckpt_best_acc,
    }
    row.update(summary)
    return row


def build_markdown(rows: List[dict], val_dir: str, num_samples: int) -> str:
    lines = [
        "# ImageNet Zero-Shot Analog Deployment Results (GPT)",
        "",
        f"- Validation directory: `{val_dir}`",
        f"- Evaluated samples: `{num_samples}`",
        "",
        "| Condition | Hybrid | Noise | Accuracy | Checkpoint |",
        "|:----------|:------:|:-----:|:---------|:-----------|",
    ]
    for row in rows:
        lines.append(
            f"| {row['condition']} | {'yes' if row['use_hybrid'] else 'no'} | "
            f"{'on' if row['noise_enabled'] else 'off'} | "
            f"{row['test_acc_mean']:.2f} +/- {row['test_acc_std']:.2f}% ({row['eval_runs']} runs) | "
            f"`{row['checkpoint_path'] or 'timm pretrained'}` |"
        )
    lines.extend([
        "",
        "## Notes",
        "",
        "- `digital_fp32_pretrained` is the reference timm-pretrained Tiny-ViT baseline on ImageNet-1k.",
        "- `hybrid_quant_only` measures zero-shot analog deployment with quantization and scale recovery but no device noise.",
        "- `hybrid_standard_noise` adds standard organic noise (5% C2C, 10% D2D) without ImageNet HAT training.",
        "- `hybrid_hat_checkpoint` is included only when a compatible 1000-class HAT checkpoint is provided.",
        "- Optional `--device-profile-json` lets the same ImageNet path reuse in-house measured device parameters.",
        "",
    ])
    return "\n".join(lines) + "\n"


def export_rows(rows: List[dict], json_path: str, csv_path: str, md_path: str,
                val_dir: str, num_samples: int):
    ensure_parent_dir(json_path)
    ensure_parent_dir(csv_path)
    ensure_parent_dir(md_path)

    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump({"results": rows, "val_dir": val_dir, "num_samples": num_samples}, fh, indent=2)

    fieldnames: List[str] = []
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    with open(csv_path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    with open(md_path, "w", encoding="utf-8") as fh:
        fh.write(build_markdown(rows, val_dir, num_samples))


def main():
    parser = argparse.ArgumentParser(description="Evaluate pretrained Tiny-ViT under zero-shot analog deployment on ImageNet-1k.")
    parser.add_argument("--data-root", type=str, default="./data")
    parser.add_argument("--val-dir", type=str, default=None)
    parser.add_argument("--hat-checkpoint", type=str, default=None,
                        help="Optional 1000-class Tiny-ViT HAT checkpoint. Skipped if omitted.")
    parser.add_argument("--device", type=str, default=None)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--num-workers", type=int, default=4)
    parser.add_argument("--eval-runs", type=int, default=10,
                        help="Monte Carlo runs for noisy conditions.")
    parser.add_argument("--max-samples", type=int, default=None,
                        help="Optional subset size for smoke checks.")
    parser.add_argument("--device-profile-json", type=str, default=None,
                        help="Optional measured-device profile JSON.")
    parser.add_argument("--profile-name", type=str, default=None,
                        help="Profile name inside --device-profile-json when multiple entries are present.")
    parser.add_argument("--num-classes", type=int, default=1000,
                        help="Number of output classes (1000 for ImageNet-1K, 200 for Tiny-ImageNet).")
    parser.add_argument("--results-json-path", type=str, default=DEFAULT_JSON_PATH)
    parser.add_argument("--results-csv-path", type=str, default=DEFAULT_CSV_PATH)
    parser.add_argument("--results-md-path", type=str, default=DEFAULT_MD_PATH)
    parser.add_argument("--log-path", type=str, default=DEFAULT_LOG_PATH)
    args = parser.parse_args()

    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")
    logger = RunLogger(args.log_path)

    try:
        val_dir = resolve_imagenet_val_dir(args.data_root, args.val_dir)
        val_loader, num_samples = get_imagenet_val_loader(
            val_dir,
            batch_size=args.batch_size,
            num_workers=args.num_workers,
            max_samples=args.max_samples,
        )

        logger.log(f"Device: {device}")
        logger.log(f"ImageNet val dir: {val_dir}")
        logger.log(f"Evaluated samples: {num_samples}")
        device_profile = resolve_device_profile(args.device_profile_json, args.profile_name)
        if device_profile is not None:
            logger.log(
                f"Measured profile: {device_profile.device_type} "
                f"(G_range={device_profile.dynamic_range}x, n_states={device_profile.n_states}, "
                f"c2c={device_profile.sigma_c2c}, d2d={device_profile.sigma_d2d})"
            )

        rows: List[dict] = []

        rows.append(run_condition(
            label="digital_fp32_pretrained",
            exp_cfg=TinyViTExperimentConfig(name="imagenet_digital_fp32", use_hybrid=False, noise_enabled=False),
            device=device,
            val_loader=val_loader,
            checkpoint_path=None,
            eval_runs=1,
            logger=logger,
            device_profile=device_profile,
            num_classes=args.num_classes,
        ))

        rows.append(run_condition(
            label="hybrid_quant_only",
            exp_cfg=TinyViTExperimentConfig(
                name="imagenet_hybrid_quant_only",
                use_hybrid=True,
                noise_enabled=False,
                sigma_c2c=0.0,
                sigma_d2d=0.0,
                hat_training=False,
            ),
            device=device,
            val_loader=val_loader,
            checkpoint_path=None,
            eval_runs=1,
            logger=logger,
            device_profile=device_profile,
            num_classes=args.num_classes,
        ))

        rows.append(run_condition(
            label="hybrid_standard_noise",
            exp_cfg=TinyViTExperimentConfig(
                name="imagenet_hybrid_standard_noise",
                use_hybrid=True,
                noise_enabled=True,
                sigma_c2c=0.05,
                sigma_d2d=0.10,
                hat_training=False,
            ),
            device=device,
            val_loader=val_loader,
            checkpoint_path=None,
            eval_runs=args.eval_runs,
            logger=logger,
            device_profile=device_profile,
            num_classes=args.num_classes,
        ))

        if args.hat_checkpoint:
            rows.append(run_condition(
                label="hybrid_hat_checkpoint",
                exp_cfg=TinyViTExperimentConfig(
                    name="imagenet_hybrid_hat_checkpoint",
                    use_hybrid=True,
                    noise_enabled=True,
                    sigma_c2c=0.05,
                    sigma_d2d=0.10,
                    hat_training=True,
                ),
                device=device,
                val_loader=val_loader,
                checkpoint_path=args.hat_checkpoint,
                eval_runs=args.eval_runs,
                logger=logger,
                device_profile=device_profile,
                num_classes=args.num_classes,
            ))
        else:
            logger.log("No --hat-checkpoint provided; skipping hybrid_hat_checkpoint condition.")

        export_rows(
            rows,
            json_path=args.results_json_path,
            csv_path=args.results_csv_path,
            md_path=args.results_md_path,
            val_dir=val_dir,
            num_samples=num_samples,
        )
        logger.log(f"JSON: {args.results_json_path}")
        logger.log(f"CSV: {args.results_csv_path}")
        logger.log(f"Markdown: {args.results_md_path}")
    finally:
        logger.close()


if __name__ == "__main__":
    main()
