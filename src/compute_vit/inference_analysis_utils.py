#!/usr/bin/env python3
"""Inference harness for post-training Monte-Carlo evaluation and device-profile sweeps.

This module provides the glue between trained checkpoints and analog non-ideality
models: loading a ``ModelBundle``, applying a ``DeviceProfile``, running repeated
evaluations (``run_mc_eval``), and calibrating ADC ranges.  It is the primary
entry point for reproducing the Fig. 4 accuracy-versus-condition bars.
"""

from __future__ import annotations

import csv
import inspect
import json
import math
import os
from dataclasses import dataclass
from statistics import mean, stdev
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import torch
import torch.nn as nn

from analog_layers import (
    ADCConfig,
    ADCQuantizer,
    AnalogConv2d,
    AnalogLinear,
    disable_sparsity_tracking,
    enable_sparsity_tracking,
    get_sparsity_report,
    reset_sparsity_tracking,
    resample_d2d_buffers,
)
from device_profile_utils import DeviceProfile
from amp_utils import amp_enabled_for_device, autocast_context
try:
    from train_convnext import (
        DATASET_STATS as CONVNEXT_DATASET_STATS,
        build_model as build_convnext_model,
        evaluate as evaluate_convnext,
        get_dataloaders as get_convnext_dataloaders,
        get_experiment_configs,
    )
except ImportError:
    CONVNEXT_DATASET_STATS = {}
    build_convnext_model = None
    evaluate_convnext = None
    get_convnext_dataloaders = None
    get_experiment_configs = None
try:
    from train_tinyvit import (
        build_model as build_tinyvit_model,
        evaluate as evaluate_tinyvit,
        get_dataloaders as get_tinyvit_dataloaders,
        get_v_experiment_configs,
    )
except ImportError:
    build_tinyvit_model = None
    evaluate_tinyvit = None
    get_tinyvit_dataloaders = None
    get_v_experiment_configs = None

try:
    from train_tinyvit_ensemble import (
        TinyViTPhysicalFrontEnd,
        get_num_classes,
    )
except ImportError:
    try:
        from train_tinyvit import TinyViTPhysicalFrontEnd  # type: ignore
    except ImportError:
        TinyViTPhysicalFrontEnd = None  # type: ignore
    get_num_classes = None  # type: ignore


ANALOG_MODULE_TYPES = (AnalogLinear, AnalogConv2d)


@dataclass
class ModelBundle:
    """Container for a loaded checkpoint, config, dataloader and frontend."""
    model_type: str
    experiment: str
    experiment_name: str
    dataset: str
    device: str
    model: nn.Module
    exp_cfg: object
    testloader: object
    criterion: nn.Module
    frontend: Optional[nn.Module]
    checkpoint_path: str
    checkpoint_epoch: Optional[int]
    checkpoint_best_acc: Optional[float]
    amp_enabled: bool


def ensure_parent_dir(path: Optional[str]):
    """Create the parent directory of *path* if it does not exist."""
    if not path:
        return
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def iter_analog_modules(model: nn.Module):
    """Yield (name, module) tuples for every analog layer in *model*."""
    for name, module in model.named_modules():
        if isinstance(module, ANALOG_MODULE_TYPES):
            yield name, module


def snapshot_analog_state(model: nn.Module) -> Dict[str, dict]:
    """Capture a reversible snapshot of all analog-layer configurations."""
    state = {}
    for name, module in iter_analog_modules(model):
        inl = getattr(module.config, "inl_table", None)
        state[name] = {
            "n_states": int(module.config.n_states),
            "G_min": float(module.config.G_min),
            "G_max": float(module.config.G_max),
            "noise_enabled": bool(module.config.noise_enabled),
            "noise_mode": str(getattr(module.config, "noise_mode", "uniform")),
            "sigma_c2c": float(module.config.sigma_c2c),
            "sigma_d2d": float(module.config.sigma_d2d),
            "NL_LTP": float(getattr(module.config, "NL_LTP", 1.0)),
            "NL_LTD": float(getattr(module.config, "NL_LTD", -1.0)),
            "retention_enabled": bool(module.config.retention_enabled),
            "inference_time": float(module.config.inference_time),
            "retention_recalibrate_scale": bool(getattr(module.config, "retention_recalibrate_scale", False)),
            "retention_scales_d2d": bool(getattr(module.config, "retention_scales_d2d", False)),
            "inl_table": inl.detach().cpu().tolist() if isinstance(inl, torch.Tensor) else inl,
        }
    return state


def restore_analog_state(model: nn.Module, state: Dict[str, dict]):
    """Restore analog-layer configurations from a snapshot dict."""
    for name, module in iter_analog_modules(model):
        if name not in state:
            continue
        saved = state[name]
        module.config.n_states = saved["n_states"]
        module.config.G_min = saved["G_min"]
        module.config.G_max = saved["G_max"]
        module.config.noise_enabled = saved["noise_enabled"]
        module.config.noise_mode = saved.get("noise_mode", "uniform")
        module.config.sigma_c2c = saved["sigma_c2c"]
        module.config.sigma_d2d = saved["sigma_d2d"]
        module.config.NL_LTP = saved.get("NL_LTP", 1.0)
        module.config.NL_LTD = saved.get("NL_LTD", -1.0)
        module.config.retention_enabled = saved["retention_enabled"]
        module.config.inference_time = saved["inference_time"]
        module.config.retention_recalibrate_scale = saved.get("retention_recalibrate_scale", False)
        module.config.retention_scales_d2d = saved.get("retention_scales_d2d", False)
        saved_inl = saved.get("inl_table")
        if saved_inl is None:
            module.config.inl_table = None
        else:
            module.config.inl_table = torch.tensor(
                saved_inl,
                dtype=torch.float32,
                device=module.weight.device,
            )


def set_uniform_noise(model: nn.Module, sigma_c2c: float, sigma_d2d: float,
                      noise_enabled: bool, resample_d2d: bool = False,
                      noise_mode: Optional[str] = None):
    """Apply uniform C2C/D2D noise settings to every analog layer in *model*."""
    for _, module in iter_analog_modules(model):
        module.config.noise_enabled = noise_enabled
        module.config.sigma_c2c = sigma_c2c
        module.config.sigma_d2d = sigma_d2d
        if noise_mode is not None:
            module.config.noise_mode = noise_mode
    if resample_d2d:
        resample_d2d_buffers(model)


def set_uniform_retention(model: nn.Module, inference_time: float,
                          recalibrate_scale: bool = False,
                          scale_d2d: bool = False):
    """Configure retention decay parameters for all analog layers."""
    for _, module in iter_analog_modules(model):
        module.config.retention_enabled = inference_time > 0
        module.config.inference_time = inference_time
        module.config.retention_recalibrate_scale = recalibrate_scale
        module.config.retention_scales_d2d = scale_d2d


def apply_device_profile(model: nn.Module, profile: DeviceProfile,
                         resample_d2d: bool = True) -> int:
    """Push a literature or measured device profile into every analog layer."""
    active = 0
    for _, module in iter_analog_modules(model):
        module.config.G_min = float(profile.G_min)
        module.config.G_max = float(profile.G_max)
        module.config.n_states = int(profile.n_states)
        module.config.sigma_c2c = float(profile.sigma_c2c)
        module.config.sigma_d2d = float(profile.sigma_d2d)
        module.config.noise_mode = str(profile.noise_mode)
        if profile.NL_LTP is not None:
            module.config.NL_LTP = float(profile.NL_LTP)
        if profile.NL_LTD is not None:
            module.config.NL_LTD = float(profile.NL_LTD)
        module.config.noise_enabled = (profile.sigma_c2c > 0.0) or (profile.sigma_d2d > 0.0)
        if profile.tau_1 is not None:
            module.config.tau_1 = float(profile.tau_1)
        if profile.tau_2 is not None:
            module.config.tau_2 = float(profile.tau_2)
        if profile.A_0 is not None:
            module.config.A_0 = float(profile.A_0)
        if profile.inl_table is not None:
            module.config.inl_table = torch.tensor(
                profile.inl_table,
                dtype=torch.float32,
                device=module.weight.device,
            )
        else:
            module.config.inl_table = None
        active += 1
    if resample_d2d:
        resample_d2d_buffers(model)
    return active


def collect_analog_noise_diagnostics(model: nn.Module,
                                     layer_names: Optional[Sequence[str]] = None) -> List[dict]:
    """Return per-layer noise statistics for analog modules."""
    requested = set(layer_names) if layer_names else None
    rows: List[dict] = []

    for name, module in iter_analog_modules(model):
        if requested is not None and name not in requested:
            continue
        with torch.no_grad():
            weight = module.weight.float()
            G_pos, G_neg = module._weight_to_conductance(module.weight)
            conductance_weight = (G_pos - G_neg).float()
            G_range = float(module.config.G_max - module.config.G_min)
            noise_mode = str(getattr(module.config, "noise_mode", "uniform")).lower()
            if noise_mode == "proportional":
                reference = conductance_weight.abs().clamp_min(1e-8)
                d2d_noise = (module.d2d_noise.float() / max(G_range, 1e-8)) * reference
                c2c_noise = (
                    torch.randn_like(conductance_weight) * module.config.sigma_c2c * reference
                    if module.config.sigma_c2c > 0 else torch.zeros_like(conductance_weight)
                )
            else:
                d2d_noise = module.d2d_noise.float()
                c2c_noise = (
                    torch.randn_like(conductance_weight) * module.config.sigma_c2c * G_range
                    if module.config.sigma_c2c > 0 else torch.zeros_like(conductance_weight)
                )
            total_noise = d2d_noise + c2c_noise
            scale = float(module._conductance_to_weight_scale(module.weight).float().item())

            def safe_std(tensor: torch.Tensor) -> float:
                return float(tensor.float().std(unbiased=False).item())

            conductance_std = safe_std(conductance_weight)
            weight_std = safe_std(weight)
            effective_weight = conductance_weight * scale
            effective_noise = total_noise * scale
            effective_weight_std = safe_std(effective_weight)
            d2d_noise_std_conductance = safe_std(d2d_noise)
            c2c_noise_std_conductance = safe_std(c2c_noise)
            total_noise_std_conductance = math.sqrt(
                d2d_noise_std_conductance ** 2 + c2c_noise_std_conductance ** 2
            )
            d2d_noise_std_weight = safe_std(d2d_noise * scale)
            c2c_noise_std_weight = safe_std(c2c_noise * scale)
            total_noise_std_weight = math.sqrt(
                d2d_noise_std_weight ** 2 + c2c_noise_std_weight ** 2
            )

            rows.append({
                "layer": name,
                "kind": type(module).__name__,
                "shape": list(weight.shape),
                "n_states": int(module.config.n_states),
                "G_min": float(module.config.G_min),
                "G_max": float(module.config.G_max),
                "sigma_c2c": float(module.config.sigma_c2c),
                "sigma_d2d": float(module.config.sigma_d2d),
                "noise_mode": str(getattr(module.config, "noise_mode", "uniform")),
                "NL_LTP": float(getattr(module.config, "NL_LTP", 1.0)),
                "NL_LTD": float(getattr(module.config, "NL_LTD", -1.0)),
                "weight_std": weight_std,
                "conductance_weight_std": conductance_std,
                "effective_weight_std": effective_weight_std,
                "d2d_noise_std_conductance": d2d_noise_std_conductance,
                "c2c_noise_std_conductance": c2c_noise_std_conductance,
                "total_noise_std_conductance": total_noise_std_conductance,
                "d2d_noise_std_weight": d2d_noise_std_weight,
                "c2c_noise_std_weight": c2c_noise_std_weight,
                "total_noise_std_weight": total_noise_std_weight,
                "scale_recovery_factor": scale,
                "noise_to_conductance_weight_ratio": (
                    total_noise_std_conductance / conductance_std if conductance_std > 0 else 0.0
                ),
                "noise_to_weight_ratio": (
                    total_noise_std_weight / weight_std if weight_std > 0 else 0.0
                ),
                "noise_to_effective_weight_ratio": (
                    total_noise_std_weight / effective_weight_std if effective_weight_std > 0 else 0.0
                ),
            })

    return rows


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


def _resolve_tinyvit_bundle(experiment: str, dataset: str, device: str,
                            checkpoint_path: Optional[str], checkpoint_dir: str,
                            data_root: str, num_workers: int,
                            batch_size: Optional[int], amp_enabled: bool) -> ModelBundle:
    configs = get_v_experiment_configs()
    if experiment not in configs:
        raise ValueError(f"Unknown Tiny-ViT experiment: {experiment}")
    exp_cfg = configs[experiment]
    if batch_size is not None:
        exp_cfg.batch_size = batch_size
    num_classes = get_num_classes(dataset)
    ckpt_path = checkpoint_path or os.path.join(checkpoint_dir, f"{exp_cfg.name}_best.pt")
    if not os.path.exists(ckpt_path):
        raise FileNotFoundError(f"Checkpoint not found: {ckpt_path}")

    model = build_tinyvit_model(exp_cfg, num_classes=num_classes, device=device, pretrained=False)
    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    model.load_state_dict(ckpt["model_state_dict"])
    _, testloader = get_tinyvit_dataloaders(
        dataset=dataset,
        batch_size=exp_cfg.batch_size,
        num_workers=num_workers,
        data_root=data_root,
        pin_memory=False,
    )
    frontend = None
    if exp_cfg.use_physical_frontend:
        frontend = TinyViTPhysicalFrontEnd(
            dataset=dataset,
            gamma_phys=exp_cfg.physical_gamma,
            I_dark=exp_cfg.physical_I_dark,
        ).to(device)

    return ModelBundle(
        model_type="tinyvit",
        experiment=experiment,
        experiment_name=exp_cfg.name,
        dataset=dataset,
        device=device,
        model=model,
        exp_cfg=exp_cfg,
        testloader=testloader,
        criterion=nn.CrossEntropyLoss(),
        frontend=frontend,
        checkpoint_path=ckpt_path,
        checkpoint_epoch=ckpt.get("epoch"),
        checkpoint_best_acc=ckpt.get("best_acc"),
        amp_enabled=amp_enabled_for_device(amp_enabled, device),
    )


def _resolve_convnext_bundle(experiment: str, dataset: str, device: str,
                             checkpoint_path: Optional[str], checkpoint_dir: str,
                             data_root: str, num_workers: int,
                             batch_size: Optional[int], amp_enabled: bool) -> ModelBundle:
    if get_experiment_configs is None:
        raise ImportError("ConvNeXt evaluation requires train_convnext dependencies")
    configs = get_experiment_configs()
    if experiment not in configs:
        raise ValueError(f"Unknown ConvNeXt experiment: {experiment}")
    if dataset not in CONVNEXT_DATASET_STATS:
        raise ValueError(f"Unsupported ConvNeXt dataset: {dataset}")
    exp_cfg = configs[experiment]
    if batch_size is not None:
        exp_cfg.batch_size = batch_size
    dataset_stats = CONVNEXT_DATASET_STATS[dataset]
    ckpt_path = checkpoint_path or os.path.join(checkpoint_dir, f"{exp_cfg.name}_best.pt")
    if not os.path.exists(ckpt_path):
        raise FileNotFoundError(f"Checkpoint not found: {ckpt_path}")

    model = build_convnext_model(
        exp_cfg,
        num_classes=dataset_stats["num_classes"],
        image_size=dataset_stats["image_size"],
        device=device,
    )
    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    model.load_state_dict(ckpt["model_state_dict"])
    _, testloader = get_convnext_dataloaders(
        dataset=dataset,
        batch_size=exp_cfg.batch_size,
        num_workers=num_workers,
        data_root=data_root,
    )
    return ModelBundle(
        model_type="convnext",
        experiment=experiment,
        experiment_name=exp_cfg.name,
        dataset=dataset,
        device=device,
        model=model,
        exp_cfg=exp_cfg,
        testloader=testloader,
        criterion=nn.CrossEntropyLoss(),
        frontend=None,
        checkpoint_path=ckpt_path,
        checkpoint_epoch=ckpt.get("epoch"),
        checkpoint_best_acc=ckpt.get("best_acc"),
        amp_enabled=amp_enabled_for_device(amp_enabled, device),
    )


def load_model_bundle(model_type: str, experiment: str, device: str,
                      checkpoint_path: Optional[str] = None, checkpoint_dir: str = "checkpoints",
                      dataset: str = "cifar10", data_root: str = "./data",
                      num_workers: int = 4, batch_size: Optional[int] = None,
                      amp_enabled: bool = False) -> ModelBundle:
    """Load a trained checkpoint and wrap it with dataloaders and config for evaluation."""
    if model_type == "tinyvit":
        return _resolve_tinyvit_bundle(
            experiment=experiment,
            dataset=dataset,
            device=device,
            checkpoint_path=checkpoint_path,
            checkpoint_dir=checkpoint_dir,
            data_root=data_root,
            num_workers=num_workers,
            batch_size=batch_size,
            amp_enabled=amp_enabled,
        )
    if model_type == "convnext":
        return _resolve_convnext_bundle(
            experiment=experiment,
            dataset=dataset,
            device=device,
            checkpoint_path=checkpoint_path,
            checkpoint_dir=checkpoint_dir,
            data_root=data_root,
            num_workers=num_workers,
            batch_size=batch_size,
            amp_enabled=amp_enabled,
        )
    raise ValueError(f"Unsupported model type: {model_type}")


def evaluate_once(bundle: ModelBundle) -> Tuple[float, float]:
    """Run a single eval pass on the model contained in *bundle*."""
    if bundle.model_type == "tinyvit":
        params = inspect.signature(evaluate_tinyvit).parameters
        if "frontend" in params:
            return evaluate_tinyvit(
                bundle.model,
                bundle.testloader,
                bundle.criterion,
                bundle.device,
                bundle.exp_cfg,
                frontend=bundle.frontend,
                amp_enabled=bundle.amp_enabled,
            )
        return evaluate_tinyvit(
            bundle.model,
            bundle.testloader,
            bundle.criterion,
            bundle.device,
            bundle.exp_cfg,
            amp_enabled=bundle.amp_enabled,
        )
    return evaluate_convnext(
        bundle.model,
        bundle.testloader,
        bundle.criterion,
        bundle.device,
        bundle.exp_cfg,
        amp_enabled=bundle.amp_enabled,
    )


def run_mc_eval(bundle: ModelBundle, eval_runs: int, logger=None, label: Optional[str] = None,
                collect_sparsity: bool = False):
    """Monte-Carlo eval: repeat *eval_runs* times and return summary statistics."""
    losses: List[float] = []
    accuracies: List[float] = []
    if collect_sparsity:
        reset_sparsity_tracking(bundle.model)
        enable_sparsity_tracking(bundle.model)
    try:
        for run_idx in range(eval_runs):
            loss, acc = evaluate_once(bundle)
            losses.append(loss)
            accuracies.append(acc)
            if logger is not None and eval_runs > 1:
                prefix = f"{label}: " if label else ""
                logger.log(f"{prefix}mc_run={run_idx + 1}/{eval_runs}: test_acc={acc:.2f}%")
    finally:
        if collect_sparsity:
            disable_sparsity_tracking(bundle.model)
    summary = summarize_eval_runs(losses, accuracies)
    sparsity_report = get_sparsity_report(bundle.model) if collect_sparsity else None
    if logger is not None:
        prefix = f"{label}: " if label else ""
        logger.log(
            f"{prefix}acc={summary['test_acc_mean']:.2f}% ± {summary['test_acc_std']:.2f} "
            f"(min={summary['test_acc_min']:.2f}, max={summary['test_acc_max']:.2f})"
        )
        if sparsity_report is not None:
            logger.log(
                f"{prefix}sparsity_rel={sparsity_report['model_mean_relative_zero_frac'] * 100:.2f}% "
                f"(scale={sparsity_report['relative_scale']:.4f}), "
                f"sparsity_abs={sparsity_report['model_mean_absolute_zero_frac'] * 100:.2f}% "
                f"(th={sparsity_report['absolute_threshold']:.4f}) "
                f"across {sparsity_report['tracked_layers']} analog layers"
            )
    if collect_sparsity:
        return summary, sparsity_report
    return summary


def calibrate_adc_ranges(
    bundle: ModelBundle,
    max_batches: int = 1,
    use_current_noise: bool = False,
    disable_c2c: bool = False,
) -> Dict[str, dict]:
    """Record per-layer analog output min/max over a few batches for ADC range setup."""
    ranges: Dict[str, dict] = {}
    hooks = []
    snapshot = snapshot_analog_state(bundle.model)

    def make_hook(name: str):
        def hook(_module, _inputs, output):
            if not isinstance(output, torch.Tensor):
                return output
            entry = ranges.setdefault(name, {"min": float("inf"), "max": float("-inf")})
            entry["min"] = min(entry["min"], float(output.detach().min().item()))
            entry["max"] = max(entry["max"], float(output.detach().max().item()))
            return output
        return hook

    try:
        for name, module in iter_analog_modules(bundle.model):
            hooks.append(module.register_forward_hook(make_hook(name)))
        bundle.model.eval()
        if use_current_noise:
            if disable_c2c:
                for _, module in iter_analog_modules(bundle.model):
                    module.config.sigma_c2c = 0.0
        else:
            set_uniform_noise(bundle.model, sigma_c2c=0.0, sigma_d2d=0.0, noise_enabled=False)
            set_uniform_retention(bundle.model, inference_time=0.0)

        with torch.no_grad():
            for batch_idx, (inputs, _targets) in enumerate(bundle.testloader):
                if batch_idx >= max_batches:
                    break
                inputs = inputs.to(bundle.device)
                if bundle.frontend is not None:
                    inputs = bundle.frontend(inputs, mode="compensated")
                with autocast_context(bundle.device, bundle.amp_enabled):
                    bundle.model(inputs)
    finally:
        for hook in hooks:
            hook.remove()
        restore_analog_state(bundle.model, snapshot)

    for entry in ranges.values():
        if entry["min"] >= entry["max"]:
            center = entry["min"]
            entry["min"] = center - 1e-6
            entry["max"] = center + 1e-6
    return ranges


class ADCQuantHookManager:
    """Attach fixed ADC quantizers to analog layer outputs for inference-only sweeps.

    Note: The hook is registered on the module's forward output. For
    AnalogLinear this means the quantizer sees ``F.linear(..., bias)``,
    i.e. the analog MAC current *plus* the digital bias term. In a
    physically exact model the bias would be added after the ADC;
    the current implementation quantizes the combined signal for
    simplicity. This introduces a minor bias-discretization artifact
    that should be noted when citing these numbers.
    """

    def __init__(self, model: nn.Module, output_ranges: Dict[str, dict],
                 adc_bits: Optional[int], dnl_sigma: float = 0.5):
        """Install ADC quantizer hooks on analog layer outputs."""
        self.model = model
        self.output_ranges = output_ranges
        self.adc_bits = adc_bits
        self.dnl_sigma = dnl_sigma
        self._hooks = []
        self._quantizers: Dict[str, ADCQuantizer] = {}

    def _make_hook(self, quantizer: ADCQuantizer):
        def hook(_module, _inputs, output):
            if not isinstance(output, torch.Tensor):
                return output
            quantized = quantizer(output.float())
            return quantized.to(dtype=output.dtype)
        return hook

    def __enter__(self):
        if self.adc_bits is None:
            return self
        for name, module in iter_analog_modules(self.model):
            limits = self.output_ranges.get(name)
            if limits is None:
                continue
            quantizer = ADCQuantizer(
                ADCConfig(
                    adc_bits=self.adc_bits,
                    dnl_sigma=self.dnl_sigma,
                    I_min=limits["min"],
                    I_max=limits["max"],
                )
            ).to(next(module.parameters()).device)
            self._quantizers[name] = quantizer
            self._hooks.append(module.register_forward_hook(self._make_hook(quantizer)))
        return self

    def __exit__(self, exc_type, exc, tb):
        for hook in self._hooks:
            hook.remove()
        self._hooks.clear()
        self._quantizers.clear()
        return False


def load_existing_results(json_path: str) -> List[dict]:
    """Load a previous result JSON or return an empty list."""
    if not json_path or not os.path.exists(json_path):
        return []
    with open(json_path, "r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("results"), list):
        return payload["results"]
    return []


def merge_rows(existing_rows: Iterable[dict], new_rows: Iterable[dict],
               key_fields: Tuple[str, ...]) -> List[dict]:
    """Upsert *new_rows* into *existing_rows* keyed by *key_fields*."""
    merged: Dict[Tuple[object, ...], dict] = {}
    order: List[Tuple[object, ...]] = []
    for row in list(existing_rows) + list(new_rows):
        key = tuple(row.get(field) for field in key_fields)
        if key not in merged:
            order.append(key)
        merged[key] = row
    return [merged[key] for key in order]


def export_rows(rows: List[dict], json_path: str, csv_path: str,
                metadata: Optional[dict] = None):
    """Write result rows to JSON and CSV."""
    ensure_parent_dir(json_path)
    ensure_parent_dir(csv_path)

    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump({"results": rows, "metadata": metadata or {}}, fh, indent=2)

    fieldnames: List[str] = []
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)

    with open(csv_path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_sparsity_rows(bundle: ModelBundle, sparsity_report: dict,
                        context: Optional[dict] = None) -> List[dict]:
    """Flatten a sparsity report into per-layer rows for export."""
    context = context or {}
    rows = []
    for layer_row in sparsity_report.get("layers", []):
        row = {
            "model": bundle.model_type,
            "experiment": bundle.experiment,
            "experiment_name": bundle.experiment_name,
            "dataset": bundle.dataset,
            "checkpoint_path": bundle.checkpoint_path,
            "layer": layer_row["layer"],
            "kind": layer_row["kind"],
            "samples": layer_row["samples"],
            "relative_scale": layer_row["relative_scale"],
            "absolute_threshold": layer_row["absolute_threshold"],
            "mean_relative_zero_frac": layer_row["mean_relative_zero_frac"],
            "mean_relative_nonzero_frac": layer_row["mean_relative_nonzero_frac"],
            "last_relative_zero_frac": layer_row["last_relative_zero_frac"],
            "mean_absolute_zero_frac": layer_row["mean_absolute_zero_frac"],
            "mean_absolute_nonzero_frac": layer_row["mean_absolute_nonzero_frac"],
            "last_absolute_zero_frac": layer_row["last_absolute_zero_frac"],
            "model_mean_relative_zero_frac": sparsity_report.get("model_mean_relative_zero_frac", 0.0),
            "model_mean_absolute_zero_frac": sparsity_report.get("model_mean_absolute_zero_frac", 0.0),
        }
        row.update(context)
        rows.append(row)
    return rows


def adc_bits_label(adc_bits: Optional[int]) -> str:
    """Return a human-readable label for the given ADC bit width."""
    return "ideal" if adc_bits is None else f"{adc_bits}-bit"
