#!/usr/bin/env python3
"""
Training loop and evaluation scaffold for Tiny-ViT hybrid analog/digital experiments.

This module builds the model, dataloaders, and training/evaluation pipeline used
to generate the Fig. 4 cross-dataset accuracy bars.  Public helpers such as
``build_model``, ``train_one_epoch``, and ``evaluate`` are imported by sweep
scripts to run HAT and fresh-instance experiments.
"""

import argparse
import csv
import json
import os
import random
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from statistics import mean, stdev
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms

try:
    import timm
except ImportError:
    print("ERROR: timm is required. Install it in the active environment.")
    sys.exit(1)

from analog_layers import (
    AnalogConv2d,
    AnalogLinear,
    AnalogLinearConfig,
    convert_to_hybrid,
)
from amp_utils import amp_enabled_for_device, autocast_context, create_grad_scaler
from report_asset_paths import asset_path
from tinyvit_hybrid_utils import ARRAY_SIZE, classify_tinyvit_layer, crossbar_array_count

sys.stdout.reconfigure(line_buffering=True)

MODEL_NAME = "tiny_vit_5m_224"
DEFAULT_REPORT_PATH = "report_md/_gpt/tinyvit_hybrid_dryrun_report_gpt.md"
DEFAULT_LOG_PATH = "logs/_gpt/tinyvit_hybrid_dryrun_gpt.log"
DEFAULT_RESULTS_JSON_PATH = asset_path("report_md/_gpt", "json", "tinyvit_results_gpt.json")
DEFAULT_RESULTS_CSV_PATH = asset_path("report_md/_gpt", "csv", "tinyvit_results_gpt.csv")
DEFAULT_RESULTS_MD_PATH = "report_md/_gpt/tinyvit_results_gpt.md"

DATASET_STATS = {
    "cifar10": {
        "num_classes": 10,
        "mean": (0.4914, 0.4822, 0.4465),
        "std": (0.2023, 0.1994, 0.2010),
        "dataset_cls": torchvision.datasets.CIFAR10,
        "split_style": "train_flag",
    },
    "cifar100": {
        "num_classes": 100,
        "mean": (0.5071, 0.4867, 0.4408),
        "std": (0.2675, 0.2565, 0.2761),
        "dataset_cls": torchvision.datasets.CIFAR100,
        "split_style": "train_flag",
    },
    "flowers102": {
        "num_classes": 102,
        "mean": (0.485, 0.456, 0.406),
        "std": (0.229, 0.224, 0.225),
        "dataset_cls": torchvision.datasets.Flowers102,
        "split_style": "flowers102",
        "train_splits": ("train", "val"),
        "test_split": "test",
    },
}

@dataclass
class TinyViTExperimentConfig:
    """Hyper-parameters and noise flags for a single Tiny-ViT experiment."""
    name: str
    use_hybrid: bool = False
    n_states: int = 16
    nl_ltp: float = 1.0
    nl_ltd: float = -1.0
    sigma_c2c: float = 0.0
    sigma_d2d: float = 0.0
    noise_mode: str = "uniform"
    noise_enabled: bool = False
    hat_training: bool = False
    use_physical_frontend: bool = False
    retention_enabled: bool = False
    inference_time: float = 0.0
    physical_gamma: float = 1.0
    physical_I_dark: float = 1e-10
    adc_bits: int = 8
    epochs: int = 100
    batch_size: int = 64
    lr: float = 5e-4
    weight_decay: float = 0.05
    asymmetry_factor: float = 0.0
    ir_drop_factor: float = 0.0
    sneak_factor: float = 0.0
    inl_table: Optional[List[float]] = None

def get_v_experiment_configs(epochs: int = 100, batch_size: int = 64) -> Dict[str, TinyViTExperimentConfig]:
    """Return the canonical V1-V8 experiment configuration dictionary."""
    base = dict(epochs=epochs, batch_size=batch_size)
    return {
        "V1": TinyViTExperimentConfig(name="V1_fp32_digital_baseline", use_hybrid=False, **base),
        "V2": TinyViTExperimentConfig(name="V2_hybrid_no_noise", use_hybrid=True, noise_enabled=False, **base),
        "V3": TinyViTExperimentConfig(name="V3_hybrid_standard_noise_standard_train", use_hybrid=True, noise_enabled=True, sigma_c2c=0.05, sigma_d2d=0.10, **base),
        "V4": TinyViTExperimentConfig(name="V4_hybrid_standard_noise_hat", use_hybrid=True, noise_enabled=True, sigma_c2c=0.05, sigma_d2d=0.10, hat_training=True, **base),
        "V5": TinyViTExperimentConfig(name="V5_hybrid_pessimistic_noise_hat", use_hybrid=True, noise_enabled=True, sigma_c2c=0.10, sigma_d2d=0.20, hat_training=True, **base),
        "V6": TinyViTExperimentConfig(name="V6_hybrid_hat_with_physical_frontend", use_hybrid=True, noise_enabled=True, sigma_c2c=0.05, sigma_d2d=0.10, hat_training=True, use_physical_frontend=True, physical_gamma=1.0, physical_I_dark=1e-10, **base),
        "V7": TinyViTExperimentConfig(name="V7_hybrid_hat_with_retention", use_hybrid=True, noise_enabled=True, sigma_c2c=0.05, sigma_d2d=0.10, hat_training=True, retention_enabled=True, inference_time=1000.0, **base),
        "V8": TinyViTExperimentConfig(name="V8_hybrid_hat_with_retention_aware_training", use_hybrid=True, noise_enabled=True, sigma_c2c=0.05, sigma_d2d=0.10, hat_training=True, retention_enabled=True, inference_time=1000.0, **base),
    }


def ensure_parent_dir(path: Optional[str]):
    """Create the parent directory of *path* if it does not exist."""
    if not path:
        return
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


class RunLogger:
    """Simple stdout + file logger shared by training and inference helpers."""

    def __init__(self, path: Optional[str] = None):
        self.path = path
        self._fh = None
        if path:
            ensure_parent_dir(path)
            self._fh = open(path, "w", encoding="utf-8")

    def log(self, message: str = ""):
        stamped = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}" if message else ""
        print(stamped)
        if self._fh is not None:
            self._fh.write(stamped + "\n")
            self._fh.flush()

    def close(self):
        if self._fh is not None:
            self._fh.close()
            self._fh = None


def set_seed(seed: int):
    """Fix random seeds for reproducible training and inference."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def get_num_classes(dataset: str, num_classes: Optional[int] = None) -> int:
    """Resolve the number of output classes for a dataset."""
    if num_classes is not None:
        return num_classes
    return DATASET_STATS[dataset]["num_classes"]


def resolve_experiment_ids(default_experiment: str,
                           requested_experiments: Optional[Sequence[str]],
                           configs: Dict[str, TinyViTExperimentConfig]) -> List[str]:
    """Parse a comma-separated experiment list and validate against known configs."""
    raw_ids = list(requested_experiments) if requested_experiments else [default_experiment]
    tokens: List[str] = []
    for raw in raw_ids:
        for token in str(raw).split(","):
            token = token.strip()
            if token:
                tokens.append(token)

    if any(token.upper() == "ALL" for token in tokens):
        return list(configs.keys())

    resolved: List[str] = []
    seen = set()
    for token in tokens:
        if token not in configs:
            raise ValueError(f"Unknown experiment '{token}'. Expected one of: {sorted(configs)}")
        if token not in seen:
            resolved.append(token)
            seen.add(token)
    return resolved

def set_retention(model: nn.Module, inference_time: float, recalibrate_scale: bool = False, scale_d2d: bool = False):
    """Configure retention decay on all analog layers in *model*."""
    for module in model.modules():
        if isinstance(module, (AnalogLinear, AnalogConv2d)):
            module.config.retention_enabled = inference_time > 0
            module.config.inference_time = inference_time
            module.config.retention_recalibrate_scale = recalibrate_scale
            module.config.retention_scales_d2d = scale_d2d


def set_noise_for_eval(model: nn.Module, exp_cfg: TinyViTExperimentConfig):
    """Push evaluation noise parameters from *exp_cfg* into analog layers."""
    for module in model.modules():
        if isinstance(module, (AnalogLinear, AnalogConv2d)):
            module.config.noise_enabled = exp_cfg.noise_enabled
            module.config.sigma_c2c = exp_cfg.sigma_c2c
            module.config.sigma_d2d = exp_cfg.sigma_d2d
            module.config.noise_mode = exp_cfg.noise_mode
            module.config.NL_LTP = exp_cfg.nl_ltp
            module.config.NL_LTD = exp_cfg.nl_ltd


def set_noise_for_train(model: nn.Module, exp_cfg: TinyViTExperimentConfig):
    """Push training noise parameters from *exp_cfg* into analog layers."""
    for module in model.modules():
        if isinstance(module, (AnalogLinear, AnalogConv2d)):
            if exp_cfg.hat_training:
                module.config.noise_enabled = exp_cfg.noise_enabled
                module.config.sigma_c2c = exp_cfg.sigma_c2c
            elif exp_cfg.noise_enabled:
                module.config.noise_enabled = True
                module.config.sigma_c2c = 0.0
            else:
                module.config.noise_enabled = False
                module.config.sigma_c2c = 0.0
            module.config.sigma_d2d = exp_cfg.sigma_d2d
            module.config.noise_mode = exp_cfg.noise_mode
            module.config.NL_LTP = exp_cfg.nl_ltp
            module.config.NL_LTD = exp_cfg.nl_ltd

def build_model(exp_cfg: TinyViTExperimentConfig, num_classes: int, device: str, pretrained: bool = False) -> nn.Module:
    """Instantiate a Tiny-ViT and optionally convert it to hybrid analog/digital."""
    model = timm.create_model(MODEL_NAME, pretrained=pretrained, num_classes=num_classes)
    if exp_cfg.use_hybrid:
        analog_cfg = AnalogLinearConfig(
            n_states=exp_cfg.n_states, NL_LTP=exp_cfg.nl_ltp, NL_LTD=exp_cfg.nl_ltd,
            sigma_c2c=exp_cfg.sigma_c2c if exp_cfg.hat_training else 0.0, sigma_d2d=exp_cfg.sigma_d2d,
            noise_mode=exp_cfg.noise_mode, noise_enabled=exp_cfg.hat_training and exp_cfg.noise_enabled,
            restore_weight_scale=True,
            asymmetry_factor=exp_cfg.asymmetry_factor,
            ir_drop_factor=exp_cfg.ir_drop_factor,
            sneak_factor=exp_cfg.sneak_factor,
            inl_table=torch.tensor(exp_cfg.inl_table, dtype=torch.float32) if exp_cfg.inl_table is not None else None,
        )
        model = convert_to_hybrid(model, config=analog_cfg, verbose=False)
        set_retention(model, exp_cfg.inference_time if exp_cfg.retention_enabled else 0.0, recalibrate_scale=exp_cfg.retention_enabled, scale_d2d=exp_cfg.retention_enabled)
    return model.to(device)

def maybe_fraction_subset(dataset, data_fraction: float, seed: Optional[int]):
    """Return a random subset of *dataset* when *data_fraction* < 1.0."""
    if data_fraction >= 1.0:
        return dataset
    total = len(dataset)
    subset_size = max(1, int(total * data_fraction))
    rng = np.random.default_rng(0 if seed is None else seed)
    indices = np.arange(total)
    rng.shuffle(indices)
    return torch.utils.data.Subset(dataset, indices[:subset_size].tolist())


def build_dataset_pair(dataset: str, data_root: str, transform_train, transform_test,
                       download: bool = True, dataset_cls=None):
    """Load train and test torchvision datasets with the requested transforms."""
    stats = DATASET_STATS[dataset]
    dataset_cls = dataset_cls or stats["dataset_cls"]
    split_style = stats.get("split_style", "train_flag")

    if split_style == "flowers102":
        train_splits = stats.get("train_splits", ("train",))
        train_parts = [
            dataset_cls(root=data_root, split=split, download=download, transform=transform_train)
            for split in train_splits
        ]
        trainset = torch.utils.data.ConcatDataset(train_parts)
        testset = dataset_cls(
            root=data_root,
            split=stats.get("test_split", "test"),
            download=download,
            transform=transform_test,
        )
        return trainset, testset

    trainset = dataset_cls(root=data_root, train=True, download=download, transform=transform_train)
    testset = dataset_cls(root=data_root, train=False, download=download, transform=transform_test)
    return trainset, testset


def get_dataloaders(dataset: str = "cifar10", batch_size: int = 64, num_workers: int = 4,
                    data_root: str = "./data", data_fraction: float = 1.0,
                    seed: Optional[int] = None, pin_memory: Optional[bool] = None):
    """Build train and test DataLoaders for the requested dataset."""
    stats = DATASET_STATS[dataset]
    transform_train = transforms.Compose([transforms.Resize((224, 224)), transforms.RandomHorizontalFlip(), transforms.ToTensor(), transforms.Normalize(stats["mean"], stats["std"])])
    transform_test = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor(), transforms.Normalize(stats["mean"], stats["std"])])
    trainset, testset = build_dataset_pair(
        dataset=dataset,
        data_root=data_root,
        transform_train=transform_train,
        transform_test=transform_test,
        download=True,
        dataset_cls=stats["dataset_cls"],
    )
    trainset = maybe_fraction_subset(trainset, data_fraction=data_fraction, seed=seed)
    loader_kwargs = {
        "batch_size": batch_size,
        "num_workers": num_workers,
        "pin_memory": torch.cuda.is_available() if pin_memory is None else pin_memory,
    }
    if num_workers > 0:
        loader_kwargs["persistent_workers"] = True
    return (
        torch.utils.data.DataLoader(trainset, shuffle=True, **loader_kwargs),
        torch.utils.data.DataLoader(testset, shuffle=False, **loader_kwargs),
    )

def train_one_epoch(model, loader, optimizer, criterion, device, exp_cfg, amp_enabled=False, scaler=None):
    """Run one training epoch and return (loss, accuracy)."""
    model.train()
    set_noise_for_train(model, exp_cfg)
    running_loss, correct, total = 0.0, 0, 0
    for inputs, targets in loader:
        inputs, targets = inputs.to(device), targets.to(device)
        optimizer.zero_grad(set_to_none=True)
        with autocast_context(device, amp_enabled):
            outputs = model(inputs)
            loss = criterion(outputs, targets)
        if scaler: scaler.scale(loss).backward(); scaler.step(optimizer); scaler.update()
        else: loss.backward(); optimizer.step()
        running_loss += loss.item() * inputs.size(0); _, predicted = outputs.max(1); correct += predicted.eq(targets).sum().item(); total += targets.size(0)
    return running_loss / total, 100.0 * correct / total

@torch.no_grad()
def evaluate(model, loader, criterion, device, exp_cfg, amp_enabled=False):
    """Run inference on the test set and return (loss, accuracy)."""
    model.eval()
    set_noise_for_eval(model, exp_cfg)
    running_loss, correct, total = 0.0, 0, 0
    for inputs, targets in loader:
        inputs, targets = inputs.to(device), targets.to(device)
        with autocast_context(device, amp_enabled):
            outputs = model(inputs)
            loss = criterion(outputs, targets)
        running_loss += loss.item() * inputs.size(0); _, predicted = outputs.max(1); correct += predicted.eq(targets).sum().item(); total += targets.size(0)
    return running_loss / total, 100.0 * correct / total


def init_training_history() -> dict:
    """Return a fresh history dict for tracking train/test metrics."""
    return {"train_loss": [], "train_acc": [], "test_loss": [], "test_acc": [], "lr": []}


def normalize_training_history(history: Optional[dict]) -> dict:
    """Coerce a history object to the canonical list-based format."""
    normalized = init_training_history()
    if not isinstance(history, dict):
        return normalized
    for key in normalized:
        value = history.get(key, [])
        normalized[key] = list(value) if isinstance(value, list) else []
    return normalized


def get_training_checkpoint_paths(exp_cfg: TinyViTExperimentConfig, save_dir: str) -> Tuple[str, str]:
    """Return (best_path, last_path) for a given experiment config."""
    best_checkpoint_path = os.path.join(save_dir, f"{exp_cfg.name}_best.pt")
    last_checkpoint_path = os.path.join(save_dir, f"{exp_cfg.name}_last.pt")
    return best_checkpoint_path, last_checkpoint_path


def build_training_checkpoint_payload(model: nn.Module, optimizer, scheduler, scaler,
                                      exp_cfg: TinyViTExperimentConfig,
                                      dataset: str, num_classes: int, epoch: int, best_acc: float,
                                      best_epoch: int, history: dict, amp_enabled: bool,
                                      data_fraction: float = 1.0,
                                      seed: Optional[int] = None) -> dict:
    """Assemble a checkpoint dict containing model, optimizer, and metadata."""
    payload = {
        "epoch": epoch,
        "best_epoch": best_epoch,
        "best_acc": best_acc,
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "exp_cfg": asdict(exp_cfg),
        "dataset": dataset,
        "data_fraction": data_fraction,
        "num_classes": num_classes,
        "history": normalize_training_history(history),
        "amp_enabled": amp_enabled,
        "seed": seed,
    }
    if scheduler is not None:
        payload["scheduler_state_dict"] = scheduler.state_dict()
    if scaler is not None and hasattr(scaler, "is_enabled") and scaler.is_enabled():
        payload["scaler_state_dict"] = scaler.state_dict()
    return payload


def checkpoint_is_compatible(ckpt: dict, dataset: str, num_classes: int,
                             data_fraction: float) -> Tuple[bool, str]:
    """Check whether a checkpoint matches the target dataset and class count."""
    ckpt_dataset = ckpt.get("dataset")
    if ckpt_dataset is not None and ckpt_dataset != dataset:
        return False, f"dataset mismatch (checkpoint={ckpt_dataset}, target={dataset})"
    ckpt_num_classes = ckpt.get("num_classes")
    if ckpt_num_classes is not None and int(ckpt_num_classes) != int(num_classes):
        return False, f"num_classes mismatch (checkpoint={ckpt_num_classes}, target={num_classes})"
    ckpt_data_fraction = float(ckpt.get("data_fraction", 1.0))
    if abs(ckpt_data_fraction - float(data_fraction)) > 1e-9:
        return False, (
            f"data_fraction mismatch (checkpoint={ckpt_data_fraction}, "
            f"target={data_fraction})"
        )
    return True, ""


def maybe_resume_experiment(model: nn.Module, optimizer, scheduler, scaler,
                            exp_cfg: TinyViTExperimentConfig,
                            save_dir: str, device: str, dataset: str, num_classes: int,
                            data_fraction: float = 1.0, resume_existing: bool = False,
                            logger: Optional[RunLogger] = None):
    """Resume from the latest checkpoint if it is compatible, otherwise start fresh."""
    best_checkpoint_path, last_checkpoint_path = get_training_checkpoint_paths(exp_cfg, save_dir)
    start_epoch = 0
    best_acc = 0.0
    best_epoch = -1
    history = init_training_history()
    resume_checkpoint_path = None

    if resume_existing:
        if os.path.exists(last_checkpoint_path):
            resume_checkpoint_path = last_checkpoint_path
        elif os.path.exists(best_checkpoint_path):
            resume_checkpoint_path = best_checkpoint_path

    if resume_checkpoint_path is None:
        return start_epoch, best_acc, best_epoch, best_checkpoint_path, last_checkpoint_path, history, None

    ckpt = torch.load(resume_checkpoint_path, map_location=device, weights_only=False)
    compatible, reason = checkpoint_is_compatible(
        ckpt, dataset=dataset, num_classes=num_classes, data_fraction=data_fraction
    )
    if not compatible:
        message = f"Skipping resume from {resume_checkpoint_path}: {reason}"
        if logger is not None:
            logger.log(message)
        else:
            print(message)
        return start_epoch, best_acc, best_epoch, best_checkpoint_path, last_checkpoint_path, history, None

    try:
        model.load_state_dict(ckpt["model_state_dict"])
    except RuntimeError as exc:
        message = f"Skipping resume from {resume_checkpoint_path}: incompatible state_dict ({exc})"
        if logger is not None:
            logger.log(message)
        else:
            print(message)
        return start_epoch, best_acc, best_epoch, best_checkpoint_path, last_checkpoint_path, history, None

    optimizer_state = ckpt.get("optimizer_state_dict")
    if optimizer_state is not None:
        optimizer.load_state_dict(optimizer_state)
    scheduler_state = ckpt.get("scheduler_state_dict")
    if scheduler_state is not None and scheduler is not None:
        scheduler.load_state_dict(scheduler_state)
    scaler_state = ckpt.get("scaler_state_dict")
    if scaler_state is not None and scaler is not None and hasattr(scaler, "is_enabled") and scaler.is_enabled():
        scaler.load_state_dict(scaler_state)

    start_epoch = int(ckpt.get("epoch", -1)) + 1
    best_acc = float(ckpt.get("best_acc", 0.0))
    best_epoch = int(ckpt.get("best_epoch", ckpt.get("epoch", -1)))
    history = normalize_training_history(ckpt.get("history"))
    return start_epoch, best_acc, best_epoch, best_checkpoint_path, last_checkpoint_path, history, resume_checkpoint_path


def build_retention_metadata(exp_id: str, exp_cfg: TinyViTExperimentConfig,
                             checkpoint_path: str, ckpt: dict, eval_runs: int) -> dict:
    """Create a metadata dict describing a retention sweep run."""
    return {
        "checkpoint_path": checkpoint_path,
        "source_experiment": exp_cfg.name,
        "experiment": exp_id,
        "epoch": ckpt.get("epoch"),
        "best_acc": ckpt.get("best_acc"),
        "trained_epochs": (ckpt.get("exp_cfg") or {}).get("epochs", exp_cfg.epochs),
        "dataset": ckpt.get("dataset"),
        "mc_runs": eval_runs,
    }


def summarize_eval_runs(losses: List[float], accuracies: List[float]) -> dict:
    """Compute mean, min, max and standard deviation over repeated eval runs."""
    if not losses or not accuracies:
        raise ValueError("losses and accuracies must be non-empty")
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


def build_results_markdown(result_rows: List[dict], retention_rows: Optional[List[dict]] = None,
                           retention_metadata: Optional[dict] = None) -> str:
    """Render experiment results as a Markdown table string."""
    lines = ["# Tiny-ViT Results (GPT)", ""]

    if result_rows:
        lines.extend([
            "| Mode | Exp | Name | Dataset | Primary Metric | Checkpoint |",
            "|:-----|:----|:-----|:--------|:---------------|:-----------|",
        ])
        for row in result_rows:
            if row["mode"] == "train":
                metric = f"best_acc={row['best_test_acc']:.2f}% @ epoch {row['best_epoch']}"
            else:
                metric = (
                    f"acc={row['test_acc_mean']:.2f}%"
                    f" +/- {row['test_acc_std']:.2f} ({row['eval_runs']} runs)"
                )
            lines.append(
                f"| {row['mode']} | {row['experiment']} | {row['experiment_name']} | "
                f"{row['dataset']} | {metric} | `{row['checkpoint_path']}` |"
            )

    if retention_rows:
        lines.extend(["", "## Retention Sweep", ""])
        if retention_metadata:
            lines.extend([
                f"- Source experiment: `{retention_metadata['source_experiment']}`",
                f"- Checkpoint: `{retention_metadata['checkpoint_path']}`",
                f"- Saved epoch: {retention_metadata['epoch']}",
                f"- Checkpoint best accuracy: {retention_metadata['best_acc']:.2f}%",
                f"- MC runs per time point: {retention_metadata['mc_runs']}",
                "",
            ])
        lines.extend([
            "| Exp | Dataset | Time (s) | Accuracy | Checkpoint |",
            "|:----|:--------|---------:|:---------|:-----------|",
        ])
        for row in retention_rows:
            lines.append(
                f"| {row['experiment']} | {row['dataset']} | {row['time_s']} | "
                f"{row['test_acc_mean']:.2f} +/- {row['test_acc_std']:.2f}%"
                f" ({row['mc_runs']} runs) | `{row['checkpoint_path']}` |"
            )

    lines.extend([
        "",
        "## Notes",
        "",
        "- `eval` mode reports repeated-run statistics for noisy experiments when `--eval-runs > 1`.",
        "- `retention-sweep` result files are optional summaries layered on top of canonical checkpoints.",
        "- These result files are scratch artifacts and do not replace the canonical experiment reports.",
    ])
    return "\n".join(lines) + "\n"


def export_result_rows(result_rows: List[dict], json_path: Optional[str],
                       csv_path: Optional[str], md_path: Optional[str],
                       retention_rows: Optional[List[dict]] = None,
                       retention_metadata: Optional[dict] = None):
    """Write result rows to JSON, CSV, and Markdown files."""
    if not result_rows and not retention_rows:
        return

    if json_path:
        ensure_parent_dir(json_path)
        with open(json_path, "w", encoding="utf-8") as fh:
            if retention_rows or retention_metadata:
                json.dump({
                    "results": result_rows,
                    "retention": retention_rows or [],
                    "retention_metadata": retention_metadata,
                }, fh, indent=2)
            else:
                json.dump(result_rows, fh, indent=2)

    if csv_path:
        ensure_parent_dir(csv_path)
        csv_rows = result_rows if result_rows else (retention_rows or [])
        fieldnames = list(csv_rows[0].keys())
        extra_fields = sorted(
            field
            for row in csv_rows
            for field in row.keys()
            if field not in fieldnames
        )
        fieldnames.extend(extra_fields)
        with open(csv_path, "w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            for row in csv_rows:
                writer.writerow(row)

    if md_path:
        ensure_parent_dir(md_path)
        with open(md_path, "w", encoding="utf-8") as fh:
            fh.write(build_results_markdown(result_rows, retention_rows, retention_metadata))


def resolve_checkpoint_path(exp_cfg: TinyViTExperimentConfig, explicit_checkpoint: Optional[str],
                            checkpoint_dir: str) -> str:
    """Return the explicit checkpoint path or the default best checkpoint."""
    if explicit_checkpoint:
        return explicit_checkpoint
    best_checkpoint_path, _ = get_training_checkpoint_paths(exp_cfg, checkpoint_dir)
    if not os.path.exists(best_checkpoint_path):
        raise FileNotFoundError(f"Checkpoint not found: {best_checkpoint_path}")
    return best_checkpoint_path

def main():
    """CLI entry point for train, eval, and dry-run modes."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["train", "eval", "dry-run"], default="dry-run")
    parser.add_argument("--experiment", type=str, default="V4")
    parser.add_argument("--dataset", default="cifar10")
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--amp", action="store_true")
    parser.add_argument("--checkpoint", type=str, default=None)
    parser.add_argument("--checkpoint-dir", type=str, default=None)
    parser.add_argument("--save-dir", type=str, default="checkpoints")
    parser.add_argument("--data-root", type=str, default="./data")
    parser.add_argument("--data-fraction", type=float, default=1.0)
    parser.add_argument("--num-workers", type=int, default=4)
    parser.add_argument("--eval-runs", type=int, default=1)
    parser.add_argument("--pretrained", action="store_true")
    parser.add_argument("--resume-existing", action="store_true")
    args = parser.parse_args()
    if not (0.0 < args.data_fraction <= 1.0):
        raise ValueError(f"--data-fraction must be in (0, 1], got {args.data_fraction}")
    if args.seed is not None:
        set_seed(args.seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    configs = get_v_experiment_configs(epochs=args.epochs, batch_size=args.batch_size)
    exp_cfg = configs[args.experiment]
    model = build_model(exp_cfg, DATASET_STATS[args.dataset]["num_classes"], device, pretrained=args.pretrained)
    criterion = nn.CrossEntropyLoss()

    if args.mode == "dry-run":
        print(
            f"Dry run for {args.experiment} on {args.dataset}: "
            f"hybrid={exp_cfg.use_hybrid}, pretrained={args.pretrained}, "
            f"noise={exp_cfg.noise_enabled}, retention={exp_cfg.retention_enabled}, "
            f"data_fraction={args.data_fraction}"
        )
        return

    trainloader, testloader = get_dataloaders(
        args.dataset, args.batch_size, num_workers=args.num_workers, data_root=args.data_root,
        data_fraction=args.data_fraction, seed=args.seed
    )

    if args.mode == "eval":
        checkpoint_dir = args.checkpoint_dir or args.save_dir
        checkpoint_path = resolve_checkpoint_path(exp_cfg, args.checkpoint, checkpoint_dir)
        checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)
        state_dict = checkpoint.get("model_state_dict", checkpoint)
        model.load_state_dict(state_dict)
        print(
            f"Starting eval for {args.experiment} on {args.dataset} "
            f"(Seed: {args.seed}, BS: {args.batch_size}, AMP: {args.amp}, "
            f"pretrained={args.pretrained}, checkpoint={checkpoint_path}, "
            f"data_fraction={args.data_fraction})"
        )
        losses: List[float] = []
        accuracies: List[float] = []
        for run_idx in range(args.eval_runs):
            t_loss, t_acc = evaluate(model, testloader, criterion, device, exp_cfg, args.amp)
            losses.append(t_loss)
            accuracies.append(t_acc)
            print(f"Eval run {run_idx + 1}/{args.eval_runs}: test_loss={t_loss:.4f}, test_acc={t_acc:.2f}%")
        acc_mean = mean(accuracies)
        acc_std = stdev(accuracies) if len(accuracies) > 1 else 0.0
        print(
            f"Eval summary: checkpoint_epoch={checkpoint.get('epoch')}, "
            f"checkpoint_best_acc={checkpoint.get('best_acc')}, "
            f"test_acc_mean={acc_mean:.2f}%, test_acc_std={acc_std:.2f}%"
        )
        return

    optimizer = optim.AdamW(model.parameters(), lr=exp_cfg.lr, weight_decay=exp_cfg.weight_decay)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)
    scaler = create_grad_scaler(device, args.amp)
    start_epoch, best_acc, best_epoch, checkpoint_path, last_checkpoint_path, history, resume_checkpoint_path = (
        maybe_resume_experiment(
            model, optimizer, scheduler, scaler, exp_cfg, args.save_dir, device,
            dataset=args.dataset, num_classes=DATASET_STATS[args.dataset]["num_classes"],
            data_fraction=args.data_fraction,
            resume_existing=args.resume_existing,
        )
    )
    print(
        f"Starting train for {args.experiment} on {args.dataset} "
        f"(Seed: {args.seed}, BS: {args.batch_size}, AMP: {args.amp}, "
        f"pretrained={args.pretrained}, data_fraction={args.data_fraction})"
    )
    if args.data_fraction < 1.0:
        print(f"Training subset size: {len(trainloader.dataset)} samples")
    if resume_checkpoint_path is not None:
        print(
            f"Resuming from {resume_checkpoint_path}: start_epoch={start_epoch}, "
            f"best_acc={best_acc:.2f}%, best_epoch={best_epoch}"
        )

    os.makedirs(args.save_dir, exist_ok=True)
    for epoch in range(start_epoch, args.epochs):
        current_lr = optimizer.param_groups[0]["lr"]
        loss, acc = train_one_epoch(model, trainloader, optimizer, criterion, device, exp_cfg, args.amp, scaler)
        t_loss, t_acc = evaluate(model, testloader, criterion, device, exp_cfg, args.amp)
        history["train_loss"].append(loss)
        history["train_acc"].append(acc)
        history["test_loss"].append(t_loss)
        history["test_acc"].append(t_acc)
        history["lr"].append(current_lr)

        improved = t_acc > best_acc
        if improved:
            best_acc = t_acc
            best_epoch = epoch

        checkpoint_payload = build_training_checkpoint_payload(
            model, optimizer, scheduler, scaler, exp_cfg, args.dataset, DATASET_STATS[args.dataset]["num_classes"],
            epoch, best_acc, best_epoch, history, args.amp, args.data_fraction, args.seed
        )
        torch.save(checkpoint_payload, last_checkpoint_path)
        if improved:
            torch.save(checkpoint_payload, checkpoint_path)
        scheduler.step()

        print(
            f"Epoch {epoch}: train_loss={loss:.4f}, train_acc={acc:.2f}%, "
            f"test_acc={t_acc:.2f}% (best={best_acc:.2f}%), lr={current_lr:.6f}"
        )

    print(f"Finished. Best accuracy: {best_acc:.2f}% at epoch {best_epoch}; checkpoint={checkpoint_path}")

if __name__ == "__main__":
    main()
