#!/usr/bin/env python3
"""
Ensemble HAT training loop, D2D resampler, and dry-run scaffold for Tiny-ViT.

This module extends the base training pipeline with per-epoch D2D mismatch
resampling (``resample_all_d2d_noise``) to simulate Hardware-Aware Training
across fresh device instances.  It also provides energy estimation helpers
and the full experiment runner used to produce the Fig. 4 accuracy bars.
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
import torch.nn.functional as F
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
    EnergyProfiler,
    InverseGammaPreprocessor,
    PhotocurrentSimulator,
    convert_to_hybrid,
)
from amp_utils import amp_enabled_for_device, autocast_context, create_grad_scaler
from report_asset_paths import asset_path
from tinyvit_hybrid_utils import ARRAY_SIZE, classify_tinyvit_layer, crossbar_array_count

sys.stdout.reconfigure(line_buffering=True)

MODEL_NAME = "tiny_vit_5m_224"
DEFAULT_REPORT_PATH = "report_md/_gpt/tinyvit_hybrid_dryrun_report_gpt.md"
DEFAULT_LOG_PATH = None  # No default file log; use --log-path to specify
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
    drift_regularizer_enabled: bool = False
    drift_regularizer_weight: float = 0.0
    drift_regularizer_time_s: float = 1000.0
    drift_regularizer_state_dependent: bool = False
    epochs: int = 100
    batch_size: int = 64
    lr: float = 5e-4
    weight_decay: float = 0.05


def get_v_experiment_configs(epochs: int = 100, batch_size: int = 64) -> Dict[str, TinyViTExperimentConfig]:
    """Return the planned V1-V7 experiment matrix."""
    base = dict(epochs=epochs, batch_size=batch_size)
    return {
        "V1": TinyViTExperimentConfig(name="V1_fp32_digital_baseline", use_hybrid=False, **base),
        "V2": TinyViTExperimentConfig(
            name="V2_hybrid_no_noise", use_hybrid=True, noise_enabled=False, **base
        ),
        "V3": TinyViTExperimentConfig(
            name="V3_hybrid_standard_noise_standard_train",
            use_hybrid=True, noise_enabled=True, sigma_c2c=0.05, sigma_d2d=0.10, **base
        ),
        "V4": TinyViTExperimentConfig(
            name="V4_hybrid_standard_noise_hat",
            use_hybrid=True, noise_enabled=True, sigma_c2c=0.05, sigma_d2d=0.10,
            hat_training=True, **base
        ),
        "V5": TinyViTExperimentConfig(
            name="V5_hybrid_pessimistic_noise_hat",
            use_hybrid=True, noise_enabled=True, sigma_c2c=0.10, sigma_d2d=0.20,
            hat_training=True, **base
        ),
        "V6": TinyViTExperimentConfig(
            name="V6_hybrid_hat_with_physical_frontend",
            use_hybrid=True, noise_enabled=True, sigma_c2c=0.05, sigma_d2d=0.10,
            hat_training=True, use_physical_frontend=True, physical_gamma=1.0,
            physical_I_dark=1e-10, **base
        ),
        "V7": TinyViTExperimentConfig(
            name="V7_hybrid_hat_with_retention",
            use_hybrid=True, noise_enabled=True, sigma_c2c=0.05, sigma_d2d=0.10,
            hat_training=True, retention_enabled=True, inference_time=1000.0, **base
        ),
    }


class RunLogger:
    """Simple stdout + file logger for dry-run outputs."""

    def __init__(self, path: Optional[str] = None):
        self.path = path
        self._fh = None
        if path:
            ensure_parent_dir(path)
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


def ensure_parent_dir(path: Optional[str]):
    if not path:
        return
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def set_seed(seed: int):
    """Seed Python, NumPy, and Torch without changing CuDNN algorithm policy."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


class TinyViTPhysicalFrontEnd(nn.Module):
    """Optional physical front-end used by V6."""

    def __init__(self, dataset: str, gamma_phys: float = 1.0,
                 alpha: float = 1.0, I_dark: float = 1e-10, shot_noise: bool = True):
        super().__init__()
        stats = DATASET_STATS[dataset]
        self.inverse_gamma = InverseGammaPreprocessor(gamma_phys=gamma_phys, alpha=alpha)
        self.photo_sim = PhotocurrentSimulator(
            alpha=alpha,
            I_dark=I_dark,
            gamma_phys=gamma_phys,
            shot_noise=shot_noise,
        )
        self.register_buffer("mean", torch.tensor(stats["mean"]).view(1, 3, 1, 1))
        self.register_buffer("std", torch.tensor(stats["std"]).view(1, 3, 1, 1))

    def forward(self, x: torch.Tensor, mode: str = "compensated") -> torch.Tensor:
        if mode == "compensated":
            p_in, _ = self.inverse_gamma(x)
            i_out = self.photo_sim(p_in, mode="compensated")
        elif mode == "raw":
            i_out = self.photo_sim(x, mode="raw")
        else:
            raise ValueError(f"Unknown front-end mode: {mode}")

        batch = i_out.shape[0]
        flat = i_out.view(batch, -1)
        i_min = flat.min(dim=1, keepdim=True).values.view(batch, 1, 1, 1)
        i_max = flat.max(dim=1, keepdim=True).values.view(batch, 1, 1, 1)
        i_range = (i_max - i_min).clamp(min=1e-8)
        x_norm = (i_out - i_min) / i_range
        return (x_norm - self.mean.to(x.device)) / self.std.to(x.device)


def get_num_classes(dataset: str, num_classes: Optional[int] = None) -> int:
    """Resolve the number of output classes for a dataset."""
    if num_classes is not None:
        return num_classes
    return DATASET_STATS[dataset]["num_classes"]


def create_tinyvit_model(num_classes: int, pretrained: bool = False):
    """Create a raw Tiny-ViT model via timm."""
    return timm.create_model(MODEL_NAME, pretrained=pretrained, num_classes=num_classes)


def resolve_experiment_ids(default_experiment: str,
                           requested_experiments: Optional[Sequence[str]],
                           configs: Dict[str, TinyViTExperimentConfig]) -> List[str]:
    """Parse a comma-separated experiment list and validate against known configs."""
    raw_ids = list(requested_experiments) if requested_experiments else [default_experiment]
    tokens: List[str] = []

    for raw in raw_ids:
        for token in raw.split(","):
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


def build_model(exp_cfg: TinyViTExperimentConfig, num_classes: int, device: str,
                pretrained: bool = False) -> nn.Module:
    """Instantiate a Tiny-ViT and optionally convert it to hybrid analog/digital."""
    model = create_tinyvit_model(num_classes=num_classes, pretrained=pretrained)

    if exp_cfg.use_hybrid:
        analog_cfg = AnalogLinearConfig(
            n_states=exp_cfg.n_states,
            NL_LTP=exp_cfg.nl_ltp,
            NL_LTD=exp_cfg.nl_ltd,
            sigma_c2c=exp_cfg.sigma_c2c if exp_cfg.hat_training else 0.0,
            sigma_d2d=exp_cfg.sigma_d2d,
            noise_mode=exp_cfg.noise_mode,
            noise_enabled=exp_cfg.hat_training and exp_cfg.noise_enabled,
            restore_weight_scale=True,
        )
        model = convert_to_hybrid(model, config=analog_cfg, verbose=False)
        set_retention(
            model,
            exp_cfg.inference_time if exp_cfg.retention_enabled else 0.0,
            recalibrate_scale=exp_cfg.retention_enabled,
            scale_d2d=exp_cfg.retention_enabled,
        )

    return model.to(device)


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
                # Standard noisy training keeps fixed D2D mismatch active but
                # disables per-forward C2C resampling. This avoids an overly
                # optimistic train/eval gap for Tiny-ViT while preserving the
                # HAT vs. non-HAT distinction.
                module.config.noise_enabled = True
                module.config.sigma_c2c = 0.0
            else:
                module.config.noise_enabled = False
                module.config.sigma_c2c = 0.0
            module.config.sigma_d2d = exp_cfg.sigma_d2d
            module.config.noise_mode = exp_cfg.noise_mode
            module.config.NL_LTP = exp_cfg.nl_ltp
            module.config.NL_LTD = exp_cfg.nl_ltd


def set_retention(model: nn.Module, inference_time: float,
                  recalibrate_scale: bool = False,
                  scale_d2d: bool = False):
    """Configure retention decay on all analog layers in *model*."""
    for module in model.modules():
        if isinstance(module, (AnalogLinear, AnalogConv2d)):
            module.config.retention_enabled = inference_time > 0
            module.config.inference_time = inference_time
            module.config.retention_recalibrate_scale = recalibrate_scale
            module.config.retention_scales_d2d = scale_d2d


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


def resolve_pin_memory(pin_memory_mode: Optional[str]) -> bool:
    """Resolve DataLoader pin-memory behavior from a tri-state runtime setting."""
    if pin_memory_mode in (None, "auto"):
        return torch.cuda.is_available()
    if pin_memory_mode == "on":
        return True
    if pin_memory_mode == "off":
        return False
    raise ValueError(f"Unsupported pin_memory_mode: {pin_memory_mode}")


def get_dataloaders(dataset: str = "cifar10", batch_size: int = 64,
                    num_workers: int = 4, data_root: str = "./data",
                    image_size: int = 224, pin_memory_mode: Optional[str] = "auto",
                    resize_on_gpu: bool = False):
    """Build train and test DataLoaders for the requested dataset."""
    stats = DATASET_STATS[dataset]
    mean, std = stats["mean"], stats["std"]
    dataset_cls = stats["dataset_cls"]

    if resize_on_gpu and dataset not in {"cifar10", "cifar100"}:
        raise ValueError("--gpu-resize currently supports fixed-size CIFAR datasets only")

    train_transforms = []
    test_transforms = []
    if not resize_on_gpu:
        resize = transforms.Resize((image_size, image_size))
        train_transforms.append(resize)
        test_transforms.append(resize)
    train_transforms.extend([
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean, std),
    ])
    test_transforms.extend([
        transforms.ToTensor(),
        transforms.Normalize(mean, std),
    ])
    transform_train = transforms.Compose(train_transforms)
    transform_test = transforms.Compose(test_transforms)

    trainset, testset = build_dataset_pair(
        dataset=dataset,
        data_root=data_root,
        transform_train=transform_train,
        transform_test=transform_test,
        download=True,
        dataset_cls=dataset_cls,
    )
    loader_kwargs = {
        "batch_size": batch_size,
        "num_workers": num_workers,
        "pin_memory": resolve_pin_memory(pin_memory_mode),
    }
    if num_workers > 0:
        loader_kwargs["persistent_workers"] = True
        loader_kwargs["multiprocessing_context"] = "spawn"
    trainloader = torch.utils.data.DataLoader(
        trainset, shuffle=True, **loader_kwargs
    )
    testloader = torch.utils.data.DataLoader(
        testset, shuffle=False, **loader_kwargs
    )
    return trainloader, testloader


def maybe_resize_on_gpu(inputs: torch.Tensor, image_size: Optional[int]) -> torch.Tensor:
    """Resize CIFAR tensors on GPU to avoid PIL resize becoming the training bottleneck."""
    if image_size is None:
        return inputs
    target_size = (image_size, image_size)
    if tuple(inputs.shape[-2:]) == target_size:
        return inputs
    return F.interpolate(inputs, size=target_size, mode="bilinear", align_corners=False)


def compute_drift_regularizer(model: nn.Module, exp_cfg: TinyViTExperimentConfig) -> torch.Tensor:
    """Compute a differentiable retention-drift penalty over analog layers.

    The penalty is the mean absolute effective-weight drift across analog layers
    at a target inference time. It is evaluated in conductance space before
    D2D/C2C noise injection, so it regularizes the learned mapping itself rather
    than a particular sampled hardware instance.
    """
    if not exp_cfg.drift_regularizer_enabled or exp_cfg.drift_regularizer_weight <= 0.0:
        device = next(model.parameters()).device
        return torch.zeros((), device=device)

    penalties = []
    eps = 1e-8
    for module in model.modules():
        if not isinstance(module, (AnalogLinear, AnalogConv2d)):
            continue

        saved = (
            module.config.retention_enabled,
            module.config.inference_time,
            module.config.retention_state_dependent,
        )
        module.config.retention_enabled = True
        module.config.inference_time = float(exp_cfg.drift_regularizer_time_s)
        module.config.retention_state_dependent = bool(exp_cfg.drift_regularizer_state_dependent)
        try:
            g_pos, g_neg = module._weight_to_conductance(module.weight)
            g_pos_d, g_neg_d = module._apply_retention(g_pos, g_neg)
        finally:
            (
                module.config.retention_enabled,
                module.config.inference_time,
                module.config.retention_state_dependent,
            ) = saved

        base_eff = g_pos - g_neg
        drift_eff = (g_pos_d - g_neg_d) - base_eff
        penalties.append(drift_eff.pow(2).mean().clamp_min(eps))

    if not penalties:
        device = next(model.parameters()).device
        return torch.zeros((), device=device)

    return torch.stack(penalties).mean()


def train_one_epoch(model: nn.Module, trainloader, optimizer, criterion, device: str,
                    exp_cfg: TinyViTExperimentConfig, frontend: Optional[nn.Module] = None,
                    amp_enabled: bool = False, scaler=None,
                    gpu_resize_size: Optional[int] = None):
    """Run one training epoch and return (loss, accuracy, drift_penalty_mean)."""
    model.train()
    set_noise_for_train(model, exp_cfg)
    running_loss = 0.0
    correct = 0
    total = 0
    drift_penalty_running = 0.0

    for inputs, targets in trainloader:
        inputs, targets = inputs.to(device), targets.to(device)
        inputs = maybe_resize_on_gpu(inputs, gpu_resize_size)
        optimizer.zero_grad(set_to_none=True)

        if frontend is not None:
            inputs = frontend(inputs, mode="compensated")

        with autocast_context(device, amp_enabled):
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            drift_penalty = compute_drift_regularizer(model, exp_cfg)
            if exp_cfg.drift_regularizer_enabled and exp_cfg.drift_regularizer_weight > 0.0:
                loss = loss + exp_cfg.drift_regularizer_weight * drift_penalty

        if scaler is not None and scaler.is_enabled():
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            loss.backward()
            optimizer.step()

        running_loss += loss.item() * inputs.size(0)
        drift_penalty_running += float(drift_penalty.detach().item()) * inputs.size(0)
        _, predicted = outputs.max(1)
        correct += predicted.eq(targets).sum().item()
        total += targets.size(0)

    return running_loss / total, 100.0 * correct / total, drift_penalty_running / total


@torch.no_grad()
def evaluate(model: nn.Module, testloader, criterion, device: str,
             exp_cfg: TinyViTExperimentConfig, frontend: Optional[nn.Module] = None,
             amp_enabled: bool = False, gpu_resize_size: Optional[int] = None):
    """Run inference on the test set and return (loss, accuracy)."""
    model.eval()
    set_noise_for_eval(model, exp_cfg)
    running_loss = 0.0
    correct = 0
    total = 0

    for inputs, targets in testloader:
        inputs, targets = inputs.to(device), targets.to(device)
        inputs = maybe_resize_on_gpu(inputs, gpu_resize_size)

        if frontend is not None:
            inputs = frontend(inputs, mode="compensated")

        with autocast_context(device, amp_enabled):
            outputs = model(inputs)
            loss = criterion(outputs, targets)
        running_loss += loss.item() * inputs.size(0)
        _, predicted = outputs.max(1)
        correct += predicted.eq(targets).sum().item()
        total += targets.size(0)

    return running_loss / total, 100.0 * correct / total


def init_training_history() -> dict:
    """Return a fresh history dict for tracking train/test metrics."""
    return {"train_loss": [], "train_acc": [], "test_loss": [], "test_acc": [], "lr": []}


def get_training_checkpoint_paths(exp_cfg: TinyViTExperimentConfig, save_dir: str) -> Tuple[str, str]:
    """Return (best_path, last_path) for a given experiment config."""
    best_checkpoint_path = os.path.join(save_dir, f"{exp_cfg.name}_best.pt")
    last_checkpoint_path = os.path.join(save_dir, f"{exp_cfg.name}_last.pt")
    return best_checkpoint_path, last_checkpoint_path


def normalize_training_history(history: Optional[dict]) -> dict:
    """Coerce a history object to the canonical list-based format."""
    normalized = init_training_history()
    if not isinstance(history, dict):
        return normalized

    for key in normalized:
        value = history.get(key, [])
        normalized[key] = list(value) if isinstance(value, list) else []
    return normalized


def build_training_checkpoint_payload(model: nn.Module, optimizer, scheduler, scaler,
                                      exp_cfg: TinyViTExperimentConfig, dataset: str,
                                      num_classes: int,
                                      epoch: int, best_acc: float, best_epoch: int,
                                      history: dict, amp_enabled: bool,
                                      seed: Optional[int] = None) -> dict:
    """Assemble a checkpoint dict containing model, optimizer, and metadata."""
    payload = {
        "epoch": epoch,
        "best_epoch": best_epoch,
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "scheduler_state_dict": scheduler.state_dict(),
        "best_acc": best_acc,
        "exp_cfg": asdict(exp_cfg),
        "dataset": dataset,
        "num_classes": num_classes,
        "history": normalize_training_history(history),
        "amp_enabled": amp_enabled,
        "seed": seed,
    }
    if scaler is not None and scaler.is_enabled():
        payload["scaler_state_dict"] = scaler.state_dict()
    return payload


def checkpoint_is_compatible(ckpt: dict, dataset: str, num_classes: int) -> tuple[bool, str]:
    """Check whether a checkpoint matches the target dataset and class count."""
    ckpt_dataset = ckpt.get("dataset")
    if ckpt_dataset is not None and ckpt_dataset != dataset:
        return False, f"dataset mismatch (checkpoint={ckpt_dataset}, target={dataset})"

    ckpt_num_classes = ckpt.get("num_classes")
    if ckpt_num_classes is not None and int(ckpt_num_classes) != int(num_classes):
        return False, f"num_classes mismatch (checkpoint={ckpt_num_classes}, target={num_classes})"

    head_weight = (ckpt.get("model_state_dict") or {}).get("head.fc.weight")
    if head_weight is not None and int(head_weight.shape[0]) != int(num_classes):
        return False, f"classifier shape mismatch (checkpoint={head_weight.shape[0]}, target={num_classes})"

    return True, ""


def maybe_resume_experiment(model: nn.Module, optimizer, scheduler, scaler,
                            exp_cfg: TinyViTExperimentConfig, save_dir: str,
                            device: str, dataset: str, num_classes: int,
                            resume_existing: bool = False,
                            warm_start_from: Optional[str] = None,
                            logger: Optional[RunLogger] = None):
    """Resume from the latest checkpoint if it is compatible, otherwise start fresh."""
    best_checkpoint_path, last_checkpoint_path = get_training_checkpoint_paths(exp_cfg, save_dir)
    start_epoch = 0
    best_acc = 0.0
    best_epoch = -1
    history = init_training_history()
    resume_checkpoint_path = None

    if warm_start_from is not None:
        resume_checkpoint_path = warm_start_from
        if not os.path.exists(resume_checkpoint_path):
            if logger is not None:
                logger.log(f"Warm-start path not found: {resume_checkpoint_path}; starting fresh.")
            resume_checkpoint_path = None

    if resume_checkpoint_path is None and resume_existing:
        if os.path.exists(last_checkpoint_path):
            resume_checkpoint_path = last_checkpoint_path
        elif os.path.exists(best_checkpoint_path):
            resume_checkpoint_path = best_checkpoint_path

    if resume_checkpoint_path is None:
        return start_epoch, best_acc, best_epoch, best_checkpoint_path, last_checkpoint_path, history, None

    ckpt = torch.load(resume_checkpoint_path, map_location=device, weights_only=False)
    compatible, reason = checkpoint_is_compatible(ckpt, dataset=dataset, num_classes=num_classes)
    if not compatible:
        if logger is not None:
            logger.log(f"Skipping resume from {resume_checkpoint_path}: {reason}")
        return start_epoch, best_acc, best_epoch, best_checkpoint_path, last_checkpoint_path, history, None

    try:
        model.load_state_dict(ckpt["model_state_dict"])
    except RuntimeError as exc:
        if logger is not None:
            logger.log(f"Skipping resume from {resume_checkpoint_path}: incompatible state_dict ({exc})")
        return start_epoch, best_acc, best_epoch, best_checkpoint_path, last_checkpoint_path, history, None

    if warm_start_from is not None:
        if logger is not None:
            logger.log(f"Warm-start mode: weights only from {resume_checkpoint_path}; epoch/best/optimizer/scheduler state reset.")
        return start_epoch, best_acc, best_epoch, best_checkpoint_path, last_checkpoint_path, history, resume_checkpoint_path

    best_acc = float(ckpt.get("best_acc", 0.0))
    best_epoch = int(ckpt.get("best_epoch", ckpt.get("epoch", -1)))
    start_epoch = int(ckpt.get("epoch", -1)) + 1
    history = normalize_training_history(ckpt.get("history"))

    optimizer_state = ckpt.get("optimizer_state_dict")
    if optimizer_state is not None:
        optimizer.load_state_dict(optimizer_state)

    scheduler_state = ckpt.get("scheduler_state_dict")
    if scheduler_state is not None:
        scheduler.load_state_dict(scheduler_state)

    scaler_state = ckpt.get("scaler_state_dict")
    if scaler_state is not None and scaler is not None and scaler.is_enabled():
        scaler.load_state_dict(scaler_state)

    return start_epoch, best_acc, best_epoch, best_checkpoint_path, last_checkpoint_path, history, resume_checkpoint_path


def history_last(history: dict, key: str, default: float = float("nan")) -> float:
    """Return the last value for a key in a history dict."""
    values = history.get(key, [])
    return values[-1] if values else default


def build_retention_metadata(exp_id: str, exp_cfg: TinyViTExperimentConfig,
                             checkpoint_path: str, ckpt: dict, eval_runs: int) -> dict:
    """Create a metadata dict describing a retention sweep run."""
    ckpt_cfg = ckpt.get("exp_cfg") or {}
    return {
        "checkpoint_path": checkpoint_path,
        "source_experiment": exp_cfg.name,
        "experiment": exp_id,
        "epoch": ckpt.get("epoch"),
        "best_acc": ckpt.get("best_acc"),
        "trained_epochs": (ckpt.get("exp_cfg") or {}).get("epochs", exp_cfg.epochs),
        "dataset": ckpt.get("dataset"),
        "mc_runs": eval_runs,
        "drift_regularizer_enabled": ckpt_cfg.get("drift_regularizer_enabled", getattr(exp_cfg, "drift_regularizer_enabled", False)),
        "drift_regularizer_weight": ckpt_cfg.get("drift_regularizer_weight", getattr(exp_cfg, "drift_regularizer_weight", 0.0)),
        "drift_regularizer_time_s": ckpt_cfg.get("drift_regularizer_time_s", getattr(exp_cfg, "drift_regularizer_time_s", 1000.0)),
        "drift_regularizer_state_dependent": ckpt_cfg.get("drift_regularizer_state_dependent", getattr(exp_cfg, "drift_regularizer_state_dependent", False)),
    }


def resample_all_d2d_noise(model: nn.Module):
    """Force all analog layers to resample their fixed D2D mismatch buffers."""
    count = 0
    for m in model.modules():
        if hasattr(m, "resample_d2d_noise") and callable(m.resample_d2d_noise):
            m.resample_d2d_noise()
            count += 1
    return count


def run_experiment(exp_id: str, exp_cfg: TinyViTExperimentConfig, dataset: str,
                   device: str, num_classes: int, data_root: str,
                   save_dir: str, pretrained: bool = False, num_workers: int = 4,
                   logger: Optional[RunLogger] = None, log_interval: int = 20,
                   resume_existing: bool = False, warm_start_from: Optional[str] = None,
                   amp_enabled: bool = False, compile_model: bool = False,
                   pin_memory_mode: Optional[str] = "auto", gpu_resize: bool = False,
                   early_stop_patience: Optional[int] = None):
    """Train a single experiment from scratch or resume, logging progress."""
    model = build_model(exp_cfg, num_classes=num_classes, device=device, pretrained=pretrained)
    if compile_model and hasattr(torch, "compile"):
        try:
            model = torch.compile(model, mode="reduce-overhead")
            if logger is not None:
                logger.log("  torch.compile enabled (reduce-overhead)")
        except Exception as e:
            if logger is not None:
                logger.log(f"  torch.compile failed: {e}, falling back to uncompiled")
    frontend = None
    if exp_cfg.use_physical_frontend:
        frontend = TinyViTPhysicalFrontEnd(
            dataset=dataset,
            gamma_phys=exp_cfg.physical_gamma,
            I_dark=exp_cfg.physical_I_dark,
            shot_noise=True,
        ).to(device)

    trainloader, testloader = get_dataloaders(
        dataset=dataset,
        batch_size=exp_cfg.batch_size,
        data_root=data_root,
        num_workers=num_workers,
        pin_memory_mode=pin_memory_mode,
        resize_on_gpu=gpu_resize,
    )
    optimizer = optim.AdamW(model.parameters(), lr=exp_cfg.lr, weight_decay=exp_cfg.weight_decay)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=exp_cfg.epochs)
    criterion = nn.CrossEntropyLoss()
    scaler = create_grad_scaler(device, amp_enabled)
    active_amp = amp_enabled_for_device(amp_enabled, device)
    start_epoch, best_acc, best_epoch, checkpoint_path, last_checkpoint_path, history, resume_checkpoint_path = maybe_resume_experiment(
        model, optimizer, scheduler, scaler, exp_cfg, save_dir, device,
        dataset=dataset, num_classes=num_classes,
        resume_existing=resume_existing, warm_start_from=warm_start_from, logger=logger
    )

    if logger is not None:
        logger.log("")
        logger.log("=" * 70)
        logger.log(f"Experiment {exp_id}: {exp_cfg.name}")
        logger.log(
            f"  hybrid={exp_cfg.use_hybrid}, noise={exp_cfg.noise_enabled}, "
            f"C2C={exp_cfg.sigma_c2c}, D2D={exp_cfg.sigma_d2d}, HAT={exp_cfg.hat_training}"
        )
        if exp_cfg.drift_regularizer_enabled and exp_cfg.drift_regularizer_weight > 0.0:
            logger.log(
                f"  drift_regularizer=on, weight={exp_cfg.drift_regularizer_weight}, "
                f"time={exp_cfg.drift_regularizer_time_s}s, "
                f"state_dependent={exp_cfg.drift_regularizer_state_dependent}"
            )
        if exp_cfg.noise_enabled and not exp_cfg.hat_training:
            logger.log("  standard-noise policy: fixed D2D on during train, C2C off during train")
        logger.log(f"  amp={'on' if active_amp else 'off'}")
        logger.log(f"  gpu_resize={'on' if gpu_resize else 'off'}")
        logger.log(f"  early_stop_patience={early_stop_patience if early_stop_patience is not None else 'off'}")
        logger.log("=" * 70)
        if start_epoch > 0:
            source_kind = "last" if resume_checkpoint_path == last_checkpoint_path else "best fallback"
            logger.log(f"  Resuming from: {resume_checkpoint_path} ({source_kind})")
            logger.log(
                f"  Resume epoch: {start_epoch}/{exp_cfg.epochs}, best_acc={best_acc:.2f}%, "
                f"best_epoch={best_epoch}, lr={optimizer.param_groups[0]['lr']:.6f}"
            )
        if start_epoch >= exp_cfg.epochs:
            logger.log("  Checkpoint already reached target epochs; skipping training loop.")

    for epoch in range(start_epoch, exp_cfg.epochs):
        # Ensemble HAT: Resample hardware instance (D2D mismatch) at the start of each epoch
        if exp_cfg.hat_training:
            resampled_count = resample_all_d2d_noise(model)
            if logger is not None and epoch == start_epoch:
                logger.log(f"  Ensemble HAT active: Resampled D2D mismatch for {resampled_count} analog modules.")

        current_lr = optimizer.param_groups[0]["lr"]
        train_loss, train_acc, drift_penalty_mean = train_one_epoch(
            model, trainloader, optimizer, criterion, device, exp_cfg, frontend,
            amp_enabled=active_amp, scaler=scaler, gpu_resize_size=224 if gpu_resize else None,
        )
        test_loss, test_acc = evaluate(
            model, testloader, criterion, device, exp_cfg, frontend, amp_enabled=active_amp,
            gpu_resize_size=224 if gpu_resize else None,
        )

        history["train_loss"].append(train_loss)
        history["train_acc"].append(train_acc)
        history["test_loss"].append(test_loss)
        history["test_acc"].append(test_acc)
        history["lr"].append(current_lr)

        improved = test_acc > best_acc
        if improved:
            best_acc = test_acc
            best_epoch = epoch

        if logger is not None and (
            epoch == 0
            or epoch == exp_cfg.epochs - 1
            or (epoch + 1) % max(1, log_interval) == 0
        ):
            logger.log(
                f"  Epoch {epoch:3d}/{exp_cfg.epochs}: "
                f"train_loss={train_loss:.4f}, train_acc={train_acc:.2f}%, "
                f"test_acc={test_acc:.2f}% (best={best_acc:.2f}%), "
                f"drift_penalty={drift_penalty_mean:.6f}, lr={current_lr:.6f}"
            )

        scheduler.step()
        os.makedirs(save_dir, exist_ok=True)
        checkpoint_payload = build_training_checkpoint_payload(
            model, optimizer, scheduler, scaler, exp_cfg, dataset, num_classes,
            epoch, best_acc, best_epoch, history, active_amp, seed=getattr(exp_cfg, "seed", None)
        )
        torch.save(checkpoint_payload, last_checkpoint_path)
        if improved:
            torch.save(checkpoint_payload, checkpoint_path)

        if early_stop_patience is not None and early_stop_patience > 0 and best_epoch >= 0:
            epochs_without_improvement = epoch - best_epoch
            if epochs_without_improvement >= early_stop_patience:
                if logger is not None:
                    logger.log(
                        f"  Early stop: no test_acc improvement for {epochs_without_improvement} "
                        f"epochs (best={best_acc:.2f}% at epoch {best_epoch})."
                    )
                break

    if not history["test_acc"]:
        _, test_acc = evaluate(
            model, testloader, criterion, device, exp_cfg, frontend, amp_enabled=active_amp,
            gpu_resize_size=224 if gpu_resize else None,
        )
        history["train_loss"].append(float("nan"))
        history["train_acc"].append(float("nan"))
        history["test_loss"].append(float("nan"))
        history["test_acc"].append(test_acc)
        history["lr"].append(optimizer.param_groups[0]["lr"])

    if logger is not None:
        logger.log(
            f"  Finished. Best accuracy: {best_acc:.2f}% at epoch {best_epoch}; "
            f"checkpoint={checkpoint_path}"
        )

    return {
        "experiment": exp_id,
        "experiment_name": exp_cfg.name,
        "best_test_acc": best_acc,
        "best_epoch": best_epoch,
        "checkpoint_path": checkpoint_path,
    }, history


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


def resolve_checkpoint_path(exp_cfg: TinyViTExperimentConfig,
                            explicit_checkpoint: Optional[str],
                            checkpoint_dir: str) -> str:
    """Return the explicit checkpoint path or the default best checkpoint."""
    if explicit_checkpoint:
        return explicit_checkpoint
    return os.path.join(checkpoint_dir, f"{exp_cfg.name}_best.pt")


def run_eval(exp_id: str, exp_cfg: TinyViTExperimentConfig, dataset: str,
             device: str, num_classes: int, data_root: str, checkpoint_path: str,
             pretrained: bool = False, num_workers: int = 4, eval_runs: int = 1,
             logger: Optional[RunLogger] = None, amp_enabled: bool = False,
             pin_memory_mode: Optional[str] = "auto", gpu_resize: bool = False):
    """Evaluate a trained checkpoint with optional Monte-Carlo repetitions."""
    model = build_model(exp_cfg, num_classes=num_classes, device=device, pretrained=pretrained)
    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    model.load_state_dict(ckpt["model_state_dict"])
    active_amp = amp_enabled_for_device(amp_enabled, device)

    frontend = None
    if exp_cfg.use_physical_frontend:
        frontend = TinyViTPhysicalFrontEnd(
            dataset=dataset,
            gamma_phys=exp_cfg.physical_gamma,
            I_dark=exp_cfg.physical_I_dark,
        ).to(device)

    _, testloader = get_dataloaders(
        dataset=dataset,
        batch_size=exp_cfg.batch_size,
        data_root=data_root,
        num_workers=num_workers,
        pin_memory_mode=pin_memory_mode,
        resize_on_gpu=gpu_resize,
    )
    criterion = nn.CrossEntropyLoss()
    losses: List[float] = []
    accuracies: List[float] = []

    if logger is not None:
        logger.log("")
        logger.log("=" * 70)
        logger.log(f"Eval {exp_id}: {exp_cfg.name}")
        logger.log(f"  checkpoint={checkpoint_path}")
        logger.log(f"  checkpoint_epoch={ckpt.get('epoch')}, checkpoint_best_acc={ckpt.get('best_acc')}")
        logger.log(f"  amp={'on' if active_amp else 'off'}")
        logger.log(f"  gpu_resize={'on' if gpu_resize else 'off'}")
        if eval_runs > 1 and not exp_cfg.noise_enabled:
            logger.log("  note: repeated evals are expected to be identical because noise is disabled")

    for run_idx in range(eval_runs):
        test_loss, test_acc = evaluate(
            model, testloader, criterion, device, exp_cfg, frontend, amp_enabled=active_amp,
            gpu_resize_size=224 if gpu_resize else None,
        )
        losses.append(test_loss)
        accuracies.append(test_acc)
        if logger is not None and eval_runs > 1:
            logger.log(f"  eval_run={run_idx + 1}/{eval_runs}: test_loss={test_loss:.4f}, test_acc={test_acc:.2f}%")

    summary = summarize_eval_runs(losses, accuracies)
    ckpt_cfg = ckpt.get("exp_cfg") or {}
    summary.update({
        "experiment": exp_id,
        "experiment_name": exp_cfg.name,
        "checkpoint_path": checkpoint_path,
        "checkpoint_epoch": ckpt.get("epoch"),
        "checkpoint_best_acc": ckpt.get("best_acc"),
        "drift_regularizer_enabled": ckpt_cfg.get("drift_regularizer_enabled", getattr(exp_cfg, "drift_regularizer_enabled", False)),
        "drift_regularizer_weight": ckpt_cfg.get("drift_regularizer_weight", getattr(exp_cfg, "drift_regularizer_weight", 0.0)),
        "drift_regularizer_time_s": ckpt_cfg.get("drift_regularizer_time_s", getattr(exp_cfg, "drift_regularizer_time_s", 1000.0)),
        "drift_regularizer_state_dependent": ckpt_cfg.get("drift_regularizer_state_dependent", getattr(exp_cfg, "drift_regularizer_state_dependent", False)),
    })

    if logger is not None:
        logger.log(
            f"  Eval summary: acc={summary['test_acc_mean']:.2f}%"
            f" ± {summary['test_acc_std']:.2f} (min={summary['test_acc_min']:.2f}, "
            f"max={summary['test_acc_max']:.2f})"
        )

    return summary


def run_retention_sweep(exp_id: str, exp_cfg: TinyViTExperimentConfig, dataset: str,
                        device: str, num_classes: int, data_root: str, checkpoint_path: str,
                        pretrained: bool = False, num_workers: int = 4, eval_runs: int = 10,
                        retention_times: Optional[Sequence[int]] = None,
                        logger: Optional[RunLogger] = None, amp_enabled: bool = False,
                        pin_memory_mode: Optional[str] = "auto", gpu_resize: bool = False):
    """Sweep inference-time retention decay and report accuracy vs. time."""
    model = build_model(exp_cfg, num_classes=num_classes, device=device, pretrained=pretrained)
    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    model.load_state_dict(ckpt["model_state_dict"])
    active_amp = amp_enabled_for_device(amp_enabled, device)

    frontend = None
    if exp_cfg.use_physical_frontend:
        frontend = TinyViTPhysicalFrontEnd(
            dataset=dataset,
            gamma_phys=exp_cfg.physical_gamma,
            I_dark=exp_cfg.physical_I_dark,
        ).to(device)

    _, testloader = get_dataloaders(
        dataset=dataset,
        batch_size=exp_cfg.batch_size,
        data_root=data_root,
        num_workers=num_workers,
        pin_memory_mode=pin_memory_mode,
        resize_on_gpu=gpu_resize,
    )
    criterion = nn.CrossEntropyLoss()
    times = list(retention_times) if retention_times is not None else [0, 1, 10, 100, 1000, 10000]
    base_inference_time = exp_cfg.inference_time if exp_cfg.retention_enabled else 0.0
    metadata = build_retention_metadata(exp_id, exp_cfg, checkpoint_path, ckpt, eval_runs)
    rows = []

    if logger is not None:
        logger.log("")
        logger.log("=" * 70)
        logger.log(f"Retention Sweep {exp_id}: {exp_cfg.name}")
        logger.log(f"  checkpoint={checkpoint_path}")
        logger.log(f"  checkpoint_epoch={ckpt.get('epoch')}, checkpoint_best_acc={ckpt.get('best_acc')}")
        logger.log(f"  amp={'on' if active_amp else 'off'}")
        logger.log(f"  gpu_resize={'on' if gpu_resize else 'off'}")
        logger.log(f"  times={times}, mc_runs={eval_runs}")

    for time_s in times:
        set_retention(
            model,
            float(time_s),
            recalibrate_scale=True,
            scale_d2d=True,
        )
        losses: List[float] = []
        accuracies: List[float] = []
        for _ in range(eval_runs):
            test_loss, test_acc = evaluate(
                model, testloader, criterion, device, exp_cfg, frontend, amp_enabled=active_amp,
                gpu_resize_size=224 if gpu_resize else None,
            )
            losses.append(test_loss)
            accuracies.append(test_acc)

        summary = summarize_eval_runs(losses, accuracies)
        row = {
            "experiment": exp_id,
            "experiment_name": exp_cfg.name,
            "dataset": dataset,
            "time_s": time_s,
            "test_loss_mean": summary["test_loss_mean"],
            "test_acc_mean": summary["test_acc_mean"],
            "test_acc_std": summary["test_acc_std"],
            "test_acc_min": summary["test_acc_min"],
            "test_acc_max": summary["test_acc_max"],
            "mc_runs": summary["eval_runs"],
            "checkpoint_path": checkpoint_path,
            "checkpoint_epoch": ckpt.get("epoch"),
            "checkpoint_best_acc": ckpt.get("best_acc"),
        }
        rows.append(row)
        if logger is not None:
            logger.log(
                f"  t={time_s:6d}s: acc={row['test_acc_mean']:.2f}% ± {row['test_acc_std']:.2f}"
                f" (min={row['test_acc_min']:.2f}, max={row['test_acc_max']:.2f})"
            )

    set_retention(
        model,
        base_inference_time,
        recalibrate_scale=base_inference_time > 0,
        scale_d2d=base_inference_time > 0,
    )
    return rows, metadata


def _product(shape: Tuple[int, ...]) -> int:
    result = 1
    for dim in shape:
        result *= dim
    return result


def _conv_macs(module: nn.Conv2d, out_shape: Tuple[int, ...]) -> int:
    batch, out_channels, out_h, out_w = out_shape
    kernel_h, kernel_w = module.kernel_size
    return (
        batch
        * out_channels
        * out_h
        * out_w
        * (module.in_channels // module.groups)
        * kernel_h
        * kernel_w
    )


def _linear_macs(module: nn.Linear, in_shape: Tuple[int, ...]) -> int:
    batch_tokens = _product(in_shape[:-1])
    return batch_tokens * module.in_features * module.out_features


def collect_module_shapes(model: nn.Module, example_input: torch.Tensor) -> Dict[str, dict]:
    """Run a dummy forward pass and capture input/output shapes."""
    shapes = {}
    hooks = []

    def make_hook(name: str):
        def hook(module, inputs, output):
            in_tensor = inputs[0] if inputs else None
            if not isinstance(in_tensor, torch.Tensor):
                return
            out_tensor = output[0] if isinstance(output, (tuple, list)) else output
            if not isinstance(out_tensor, torch.Tensor):
                return
            shapes[name] = {
                "type": type(module).__name__,
                "in": tuple(in_tensor.shape),
                "out": tuple(out_tensor.shape),
            }
        return hook

    for name, module in model.named_modules():
        if (
            isinstance(module, (nn.Conv2d, AnalogConv2d, nn.Linear, AnalogLinear, nn.LayerNorm))
            or name.endswith(".attn")
        ):
            hooks.append(module.register_forward_hook(make_hook(name)))

    with torch.no_grad():
        model(example_input)

    for hook in hooks:
        hook.remove()

    return shapes


def build_energy_plan(model: nn.Module, shapes: Dict[str, dict]) -> Tuple[List[dict], EnergyProfiler, dict]:
    """Estimate per-layer energy and crossbar array counts."""
    profiler = EnergyProfiler()
    records: List[dict] = []

    for name, module in model.named_modules():
        shape_info = shapes.get(name)
        if shape_info is None:
            continue

        input_shape = shape_info["in"]
        output_shape = shape_info["out"]

        if isinstance(module, AnalogLinear):
            batch_tokens = _product(input_shape[:-1])
            m, n = module.out_features, module.in_features
            row_tiles, col_tiles, arrays = crossbar_array_count(m, n, array_size=ARRAY_SIZE)
            profiler.add_analog_layer(
                M=m,
                N=n,
                batch_tokens=batch_tokens,
                col_tiles=col_tiles,
                adc_bits=8,
                array_size=ARRAY_SIZE,
            )
            records.append({
                "name": name,
                "kind": "linear",
                "domain": "analog",
                "input_shape": input_shape,
                "output_shape": output_shape,
                "M": m,
                "N": n,
                "batch_tokens": batch_tokens,
                "row_tiles": row_tiles,
                "col_tiles": col_tiles,
                "arrays_diff_pair": arrays,
                "energy_desc": f"analog MACs={batch_tokens * m * n}, ADC={batch_tokens * m}, DAC={batch_tokens * n}",
            })
            continue

        if isinstance(module, AnalogConv2d):
            batch_tokens = output_shape[0] * output_shape[2] * output_shape[3]
            kernel_h, kernel_w = module.kernel_size
            m = module.out_channels
            n = (module.in_channels // module.groups) * kernel_h * kernel_w
            row_tiles, col_tiles, arrays = crossbar_array_count(m, n, array_size=ARRAY_SIZE)
            profiler.add_analog_layer(
                M=m,
                N=n,
                batch_tokens=batch_tokens,
                col_tiles=col_tiles,
                adc_bits=8,
                array_size=ARRAY_SIZE,
            )
            records.append({
                "name": name,
                "kind": "conv2d",
                "domain": "analog",
                "input_shape": input_shape,
                "output_shape": output_shape,
                "M": m,
                "N": n,
                "batch_tokens": batch_tokens,
                "row_tiles": row_tiles,
                "col_tiles": col_tiles,
                "arrays_diff_pair": arrays,
                "energy_desc": f"analog MACs={batch_tokens * m * n}, ADC={batch_tokens * m}, DAC={batch_tokens * n}",
            })
            continue

        if isinstance(module, nn.Conv2d):
            n_macs = _conv_macs(module, output_shape)
            profiler.add_digital_layer(n_MACs=n_macs, precision="INT8")
            records.append({
                "name": name,
                "kind": "conv2d",
                "domain": classify_tinyvit_layer(name, module),
                "input_shape": input_shape,
                "output_shape": output_shape,
                "M": module.out_channels,
                "N": (module.in_channels // module.groups) * module.kernel_size[0] * module.kernel_size[1],
                "batch_tokens": output_shape[0] * output_shape[2] * output_shape[3],
                "row_tiles": 0,
                "col_tiles": 0,
                "arrays_diff_pair": 0,
                "energy_desc": f"digital MACs={n_macs}",
            })
            continue

        if isinstance(module, nn.Linear):
            n_macs = _linear_macs(module, input_shape)
            profiler.add_digital_layer(n_MACs=n_macs, precision="INT8")
            records.append({
                "name": name,
                "kind": "linear",
                "domain": classify_tinyvit_layer(name, module),
                "input_shape": input_shape,
                "output_shape": output_shape,
                "M": module.out_features,
                "N": module.in_features,
                "batch_tokens": _product(input_shape[:-1]),
                "row_tiles": 0,
                "col_tiles": 0,
                "arrays_diff_pair": 0,
                "energy_desc": f"digital MACs={n_macs}",
            })
            continue

        if isinstance(module, nn.LayerNorm):
            n_elements = _product(input_shape)
            profiler.add_layernorm(n_elements=n_elements)
            records.append({
                "name": name,
                "kind": "layernorm",
                "domain": "digital",
                "input_shape": input_shape,
                "output_shape": output_shape,
                "M": 0,
                "N": 0,
                "batch_tokens": 0,
                "row_tiles": 0,
                "col_tiles": 0,
                "arrays_diff_pair": 0,
                "energy_desc": f"layernorm elements={n_elements}",
            })
            continue

        if name.endswith(".attn"):
            batch_windows, tokens, _ = input_shape
            n_qk = batch_windows * module.num_heads * tokens * tokens * module.key_dim
            n_av = batch_windows * module.num_heads * tokens * tokens * module.val_dim
            n_softmax = batch_windows * module.num_heads * tokens * tokens
            profiler.add_digital_layer(n_MACs=n_qk + n_av, precision="INT8")
            profiler.add_softmax(n_elements=n_softmax)
            records.append({
                "name": name,
                "kind": "attention_special",
                "domain": "digital",
                "input_shape": input_shape,
                "output_shape": output_shape,
                "M": 0,
                "N": 0,
                "batch_tokens": batch_windows,
                "row_tiles": 0,
                "col_tiles": 0,
                "arrays_diff_pair": 0,
                "energy_desc": (
                    f"QK digital MACs={n_qk}, AV digital MACs={n_av}, "
                    f"softmax elements={n_softmax}"
                ),
            })

    total_arrays = sum(record["arrays_diff_pair"] for record in records)
    total_devices = total_arrays * ARRAY_SIZE * ARRAY_SIZE
    total_macs = profiler.op_counts["analog_MACs"] + profiler.op_counts["digital_MACs"]
    comparison = profiler.compare_with_fp32_gpu(total_macs)
    totals = {
        "total_arrays_diff_pair": total_arrays,
        "total_devices": total_devices,
        "total_macs": total_macs,
        "fp32_comparison": comparison,
    }
    return records, profiler, totals


def format_experiment_matrix(configs: Dict[str, TinyViTExperimentConfig]) -> List[str]:
    """Render the V1-V7 experiment matrix as Markdown table rows."""
    lines = []
    lines.append("| Exp | Hybrid | Noise | C2C | D2D | HAT | Physical FE | Retention |")
    lines.append("|:---:|:------:|:-----:|:---:|:---:|:---:|:-----------:|:---------:|")
    for exp_id, cfg in configs.items():
        retention = f"{cfg.inference_time:.0f}s" if cfg.retention_enabled else "off"
        lines.append(
            f"| {exp_id} | {'yes' if cfg.use_hybrid else 'no'} | "
            f"{'on' if cfg.noise_enabled else 'off'} | {cfg.sigma_c2c} | {cfg.sigma_d2d} | "
            f"{'yes' if cfg.hat_training else 'no'} | "
            f"{'yes' if cfg.use_physical_frontend else 'no'} | "
            f"{retention} |"
        )
    return lines


def build_result_row_base(mode: str, exp_id: str, exp_cfg: TinyViTExperimentConfig,
                          dataset: str, num_classes: int) -> dict:
    """Create a base result row dict populated with experiment metadata."""
    return {
        "mode": mode,
        "experiment": exp_id,
        "experiment_name": exp_cfg.name,
        "dataset": dataset,
        "num_classes": num_classes,
        "use_hybrid": exp_cfg.use_hybrid,
        "noise_enabled": exp_cfg.noise_enabled,
        "sigma_c2c": exp_cfg.sigma_c2c,
        "sigma_d2d": exp_cfg.sigma_d2d,
        "hat_training": exp_cfg.hat_training,
        "use_physical_frontend": exp_cfg.use_physical_frontend,
        "retention_enabled": exp_cfg.retention_enabled,
        "inference_time": exp_cfg.inference_time,
        "drift_regularizer_enabled": exp_cfg.drift_regularizer_enabled,
        "drift_regularizer_weight": exp_cfg.drift_regularizer_weight,
        "drift_regularizer_time_s": exp_cfg.drift_regularizer_time_s,
        "drift_regularizer_state_dependent": exp_cfg.drift_regularizer_state_dependent,
        "epochs": exp_cfg.epochs,
        "batch_size": exp_cfg.batch_size,
        "lr": exp_cfg.lr,
        "weight_decay": exp_cfg.weight_decay,
    }


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
        "- `retention-sweep` reuses the ConvNeXt-style time grid and Monte Carlo summary format.",
        "- These result files are GPT-scoped scratch artifacts and do not replace the canonical experiment reports.",
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


def export_dry_run_report(report_path: str, exp_id: str, exp_cfg: TinyViTExperimentConfig,
                          records: List[dict], profiler: EnergyProfiler, totals: dict,
                          configs: Dict[str, TinyViTExperimentConfig], dataset: str):
    """Write a dry-run report with energy and array counts."""
    ensure_parent_dir(report_path)
    summary = profiler.summary()
    fp32 = totals["fp32_comparison"]
    latency = profiler.estimate_latency()

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Tiny-ViT Hybrid Dry-Run Report (GPT)\n\n")
        f.write(f"- Model: `{MODEL_NAME}`\n")
        f.write(f"- Dataset target: `{dataset}`\n")
        f.write(f"- Reference experiment for dry-run: `{exp_id}` / `{exp_cfg.name}`\n")
        f.write("- Scope: static dry-run only, no training launched\n\n")

        f.write("## Summary\n\n")
        analog_layers = [r for r in records if r["domain"] == "analog"]
        digital_layers = [r for r in records if r["domain"] == "digital"]
        f.write(f"- Analog layers tracked: {len(analog_layers)}\n")
        f.write(f"- Digital layers tracked: {len(digital_layers)}\n")
        f.write(f"- Total 128×128 crossbar arrays (diff pair): {totals['total_arrays_diff_pair']}\n")
        f.write(f"- Total crossbar devices: {totals['total_devices']:,}\n")
        f.write(f"- Estimated hybrid energy: {summary['total_energy_uJ']:.4f} µJ / inference\n")
        f.write(f"- Estimated FP32 GPU energy: {fp32['gpu_FP32_energy_uJ']:.4f} µJ / inference\n")
        f.write(f"- Estimated energy reduction ratio: {fp32['energy_reduction_ratio']:.2f}×\n\n")

        f.write("## Layer Allocation\n\n")
        f.write("| Layer | Kind | Domain | Input | Output | Arrays | Energy Config |\n")
        f.write("|:------|:-----|:------:|:------|:-------|-------:|:--------------|\n")
        for record in records:
            f.write(
                f"| {record['name']} | {record['kind']} | {record['domain']} | "
                f"`{record['input_shape']}` | `{record['output_shape']}` | "
                f"{record['arrays_diff_pair']} | {record['energy_desc']} |\n"
            )

        f.write("\n## Energy Breakdown\n\n")

        def format_share(key: str, value_uJ: float, pct: float) -> str:
            if key == "buffer" and value_uJ == 0.0:
                return "not separately modeled"
            if value_uJ > 0.0 and pct < 0.1:
                return "<0.1%"
            return f"{pct:.1f}%"

        for key, value in summary["energy_breakdown_J"].items():
            value_uJ = value * 1e6
            pct = summary.get("percentage", {}).get(key, 0.0)
            f.write(f"- {key}: {value_uJ:.4f} µJ ({format_share(key, value_uJ, pct)})\n")

        f.write("\n## Latency Estimate\n\n")
        f.write(f"- Estimated total latency: {latency['total_latency_us']:.4f} µs / inference\n")
        f.write("| Component | Latency |\n")
        f.write("|:----------|--------:|\n")
        for key, value in latency["latency_breakdown_ns"].items():
            f.write(f"| {key} | {value / 1000.0:.4f} µs |\n")

        f.write("\n## Experiment Matrix V1-V7\n\n")
        for line in format_experiment_matrix(configs):
            f.write(line + "\n")

        f.write("\n## Notes / TODO\n\n")
        f.write("- Attention energy uses a hook-based estimate for QK^T, softmax, and A·V.\n")
        f.write("- Buffer/SRAM/DRAM terms are not yet separately itemized in this dry-run and should not be interpreted as physically zero.\n")
        f.write("- Physical front-end min-max normalization remains a Claude-review item.\n")


def run_dry_run(exp_id: str, exp_cfg: TinyViTExperimentConfig, dataset: str,
                device: str, num_classes: int, pretrained: bool,
                report_path: str, logger: RunLogger):
    """Execute a non-mutating dry run and log energy estimates."""
    model = build_model(exp_cfg, num_classes=num_classes, device=device, pretrained=pretrained)
    example_input = torch.randn(1, 3, 224, 224, device=device)
    shapes = collect_module_shapes(model, example_input)
    records, profiler, totals = build_energy_plan(model, shapes)
    configs = get_v_experiment_configs(epochs=exp_cfg.epochs, batch_size=exp_cfg.batch_size)
    export_dry_run_report(report_path, exp_id, exp_cfg, records, profiler, totals, configs, dataset)

    logger.log("=" * 70)
    logger.log("Tiny-ViT Hybrid Dry-Run")
    logger.log("=" * 70)
    logger.log(f"Model: {MODEL_NAME}")
    logger.log(f"Reference experiment: {exp_id} / {exp_cfg.name}")
    logger.log(f"Tracked layers: {len(records)}")
    logger.log(f"Total arrays (diff pair): {totals['total_arrays_diff_pair']}")
    logger.log(f"Total devices: {totals['total_devices']:,}")
    logger.log(f"Estimated hybrid energy: {profiler.summary()['total_energy_uJ']:.4f} µJ")
    logger.log(f"Dry-run report: {report_path}")
    logger.log("")
    logger.log("Experiment matrix V1-V7:")
    for line in format_experiment_matrix(configs):
        logger.log(line)
    logger.log("")
    logger.log("Top analog layers:")
    for record in [r for r in records if r["domain"] == "analog"][:8]:
        logger.log(
            f"  {record['name']}: M={record['M']}, N={record['N']}, "
            f"arrays={record['arrays_diff_pair']}, batch_tokens={record['batch_tokens']}"
        )


def main():
    """CLI entry point for dry-run, train, eval, and retention-sweep modes."""
    parser = argparse.ArgumentParser(description="A3.1 Tiny-ViT hybrid scaffold")
    parser.add_argument("--mode", choices=["dry-run", "train", "eval"], default="dry-run")
    parser.add_argument("--experiment", type=str, default="V4", help="V1-V7 experiment id")
    parser.add_argument("--experiments", nargs="+", default=None,
                        help="one or more V1-V7 ids, comma-separated entries supported, or ALL")
    parser.add_argument("--dataset", choices=sorted(DATASET_STATS.keys()), default="cifar10")
    parser.add_argument("--num-classes", type=int, default=None)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--device", type=str, default=None)
    parser.add_argument("--data-root", type=str, default="./data")
    parser.add_argument("--num-workers", type=int, default=4)
    parser.add_argument("--seed", type=int, default=None,
                        help="Seed Python/NumPy/Torch for auditable replication runs")
    parser.add_argument("--save-dir", type=str, default="checkpoints")
    parser.add_argument("--checkpoint", type=str, default=None)
    parser.add_argument("--checkpoint-dir", type=str, default=None)
    parser.add_argument("--eval-runs", type=int, default=1)
    parser.add_argument("--retention-sweep", action="store_true",
                        help="In eval mode, sweep retention times instead of a single evaluation summary")
    parser.add_argument("--retention-times", nargs="+", type=int, default=None,
                        help="Retention evaluation times in seconds, e.g. --retention-times 0 1 10 100 1000 10000")
    parser.add_argument("--log-interval", type=int, default=20)
    parser.add_argument("--pretrained", action="store_true")
    parser.add_argument("--nl-ltp", type=float, default=None,
                        help="Override NL_LTP for all selected experiments")
    parser.add_argument("--nl-ltd", type=float, default=None,
                        help="Override NL_LTD for all selected experiments")
    parser.add_argument("--lr-override", type=float, default=None,
                        help="Override learning rate for all selected experiments")
    parser.add_argument("--noise-mode", choices=["uniform", "proportional"], default=None,
                        help="Override analog noise mode for all selected experiments")
    parser.add_argument("--amp", action="store_true",
                        help="Enable AMP mixed precision on CUDA. Omit to preserve previous full-precision behavior.")
    parser.add_argument("--pin-memory", choices=["auto", "on", "off"], default="auto",
                        help="DataLoader pin-memory mode. Use 'off' when CUDA pinning causes OOM in high-throughput runs.")
    parser.add_argument("--gpu-resize", action="store_true",
                        help="Load native CIFAR tensors and resize to 224x224 on GPU instead of PIL/CPU.")
    parser.add_argument("--early-stop-patience", type=int, default=None,
                        help="Stop training after this many epochs without test_acc improvement.")
    parser.add_argument("--resume-existing", action="store_true",
                        help="Resume training from *_last.pt if present, otherwise fall back to *_best.pt")
    parser.add_argument("--warm-start-from", type=str, default=None,
                        help="Load only model weights from the given checkpoint path; reset epoch/optimizer/scheduler/history")
    parser.add_argument("--compile", action="store_true",
                        help="Enable torch.compile(model) for ~15-30%% training speedup (PyTorch 2.x+)")
    parser.add_argument("--drift-reg-weight", type=float, default=0.0,
                        help="Enable drift-aware training with this relative-drift penalty weight.")
    parser.add_argument("--drift-reg-time", type=float, default=1000.0,
                        help="Target inference time in seconds for the drift-aware regularizer.")
    parser.add_argument("--drift-reg-state-dependent", action="store_true",
                        help="Use state-dependent retention acceleration inside the drift-aware regularizer.")
    parser.add_argument("--report-path", type=str, default=DEFAULT_REPORT_PATH)
    parser.add_argument("--log-path", type=str, default=DEFAULT_LOG_PATH)
    parser.add_argument("--results-json-path", type=str, default=DEFAULT_RESULTS_JSON_PATH)
    parser.add_argument("--results-csv-path", type=str, default=DEFAULT_RESULTS_CSV_PATH)
    parser.add_argument("--results-md-path", type=str, default=DEFAULT_RESULTS_MD_PATH)
    args = parser.parse_args()

    # Default-enable TF32 on Ampere/Ada GPUs for ~2× matmul speedup with negligible accuracy loss
    if torch.cuda.is_available() and torch.cuda.get_device_capability()[0] >= 8:
        torch.set_float32_matmul_precision('high')

    if args.seed is not None:
        set_seed(args.seed)

    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")
    num_classes = get_num_classes(args.dataset, args.num_classes)
    configs = get_v_experiment_configs(epochs=args.epochs, batch_size=args.batch_size)
    for cfg in configs.values():
        if args.nl_ltp is not None:
            cfg.nl_ltp = args.nl_ltp
        if args.nl_ltd is not None:
            cfg.nl_ltd = args.nl_ltd
        if args.lr_override is not None:
            cfg.lr = args.lr_override
        if args.noise_mode is not None:
            cfg.noise_mode = args.noise_mode
        if args.drift_reg_weight > 0.0:
            cfg.drift_regularizer_enabled = True
            cfg.drift_regularizer_weight = args.drift_reg_weight
            cfg.drift_regularizer_time_s = args.drift_reg_time
            cfg.drift_regularizer_state_dependent = args.drift_reg_state_dependent
        cfg.seed = args.seed
    experiment_ids = resolve_experiment_ids(args.experiment, args.experiments, configs)
    if args.mode == "dry-run" and len(experiment_ids) != 1:
        raise ValueError("dry-run mode supports a single experiment id; use --experiment or pass one value to --experiments")
    logger = RunLogger(args.log_path)

    try:
        logger.log(f"Device: {device}")
        logger.log(f"Mode: {args.mode}")
        logger.log(f"Experiments: {experiment_ids}")
        logger.log(f"Seed: {args.seed}")
        logger.log(f"AMP requested: {args.amp}, active: {amp_enabled_for_device(args.amp, device)}")
        logger.log(f"GPU resize: {args.gpu_resize}")
        logger.log(f"Early-stop patience: {args.early_stop_patience if args.early_stop_patience is not None else 'off'}")

        if args.mode == "dry-run":
            exp_id = experiment_ids[0]
            exp_cfg = configs[exp_id]
            run_dry_run(
                exp_id,
                exp_cfg,
                dataset=args.dataset,
                device=device,
                num_classes=num_classes,
                pretrained=args.pretrained,
                report_path=args.report_path,
                logger=logger,
            )
            return

        result_rows: List[dict] = []
        if args.mode == "train":
            for exp_id in experiment_ids:
                exp_cfg = configs[exp_id]
                result, history = run_experiment(
                    exp_id,
                    exp_cfg,
                    dataset=args.dataset,
                    device=device,
                    num_classes=num_classes,
                    data_root=args.data_root,
                    save_dir=args.save_dir,
                    pretrained=args.pretrained,
                    num_workers=args.num_workers,
                    logger=logger,
                    log_interval=args.log_interval,
                    resume_existing=args.resume_existing,
                    warm_start_from=args.warm_start_from,
                    amp_enabled=args.amp,
                    compile_model=args.compile,
                    pin_memory_mode=args.pin_memory,
                    gpu_resize=args.gpu_resize,
                    early_stop_patience=args.early_stop_patience,
                )
                row = build_result_row_base("train", exp_id, exp_cfg, args.dataset, num_classes)
                row.update({
                    "seed": args.seed,
                    "best_test_acc": result["best_test_acc"],
                    "best_epoch": result["best_epoch"],
                    "final_train_loss": history_last(history, "train_loss"),
                    "final_train_acc": history_last(history, "train_acc"),
                    "final_test_loss": history_last(history, "test_loss"),
                    "final_test_acc": history_last(history, "test_acc"),
                    "checkpoint_path": result["checkpoint_path"],
                })
                result_rows.append(row)

            export_result_rows(
                result_rows,
                args.results_json_path,
                args.results_csv_path,
                args.results_md_path,
            )
            logger.log(f"Training finished for {len(result_rows)} experiment(s).")
            logger.log(f"Result markdown: {args.results_md_path}")
            return

        if args.eval_runs < 1:
            raise ValueError("--eval-runs must be >= 1")

        checkpoint_dir = args.checkpoint_dir or args.save_dir
        if args.checkpoint and len(experiment_ids) > 1:
            raise ValueError("Use --checkpoint only with a single experiment, or use --checkpoint-dir for multi-experiment eval")

        if args.retention_sweep:
            retention_rows: List[dict] = []
            retention_metadata = None
            for exp_id in experiment_ids:
                exp_cfg = configs[exp_id]
                checkpoint_path = resolve_checkpoint_path(exp_cfg, args.checkpoint, checkpoint_dir)
                rows, metadata = run_retention_sweep(
                    exp_id,
                    exp_cfg,
                    dataset=args.dataset,
                    device=device,
                    num_classes=num_classes,
                    data_root=args.data_root,
                    checkpoint_path=checkpoint_path,
                    pretrained=args.pretrained,
                    num_workers=args.num_workers,
                    eval_runs=args.eval_runs,
                    retention_times=args.retention_times,
                    logger=logger,
                    amp_enabled=args.amp,
                    pin_memory_mode=args.pin_memory,
                    gpu_resize=args.gpu_resize,
                )
                retention_rows.extend(rows)
                if retention_metadata is None:
                    retention_metadata = metadata

            export_result_rows(
                result_rows,
                args.results_json_path,
                args.results_csv_path,
                args.results_md_path,
                retention_rows=retention_rows,
                retention_metadata=retention_metadata,
            )
            logger.log(f"Retention sweep finished for {len(experiment_ids)} experiment(s).")
            logger.log(f"Result markdown: {args.results_md_path}")
            return

        for exp_id in experiment_ids:
            exp_cfg = configs[exp_id]
            checkpoint_path = resolve_checkpoint_path(exp_cfg, args.checkpoint, checkpoint_dir)
            summary = run_eval(
                exp_id,
                exp_cfg,
                dataset=args.dataset,
                device=device,
                num_classes=num_classes,
                data_root=args.data_root,
                checkpoint_path=checkpoint_path,
                pretrained=args.pretrained,
                num_workers=args.num_workers,
                eval_runs=args.eval_runs,
                logger=logger,
                amp_enabled=args.amp,
                pin_memory_mode=args.pin_memory,
                gpu_resize=args.gpu_resize,
            )
            row = build_result_row_base("eval", exp_id, exp_cfg, args.dataset, num_classes)
            row.update(summary)
            result_rows.append(row)

        export_result_rows(
            result_rows,
            args.results_json_path,
            args.results_csv_path,
            args.results_md_path,
        )
        logger.log(f"Eval finished for {len(result_rows)} experiment(s).")
        logger.log(f"Result markdown: {args.results_md_path}")
    finally:
        logger.close()


if __name__ == "__main__":
    main()
