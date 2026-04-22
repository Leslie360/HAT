#!/usr/bin/env python3
"""
CrossSim comparison for the ConvNeXt-Tiny C4 checkpoint.

This evaluates:
1. Our framework under the checkpoint's canonical noise profile plus ADC hooks.
2. A CrossSim conversion of the corresponding effective digital model.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import numpy as np
import torch
import torch.nn as nn

from repo_bootstrap import configure_crosssim_paths, ensure_repo_root

sys.stdout.reconfigure(line_buffering=True)

REPO_ROOT = ensure_repo_root()
configure_crosssim_paths()

from calibration import calibrate_adc_limits  # noqa: E402
from simulator.algorithms.dnn.torch.convert import analog_modules, convertible_modules, from_torch  # noqa: E402
from simulator.algorithms.dnn.torch.profile import get_profiled_adc_inputs  # noqa: E402

try:
    from simulator.algorithms.dnn.torch.convert import reinitialize  # type: ignore  # noqa: E402
except ImportError:  # pragma: no cover - CrossSim version dependent
    reinitialize = None

from dnn_inference_params import dnn_inference_params  # noqa: E402

from analog_layers import AnalogConv2d, AnalogLinear
from inference_analysis_utils import (
    ADCQuantHookManager,
    ModelBundle,
    calibrate_adc_ranges,
    set_uniform_noise,
)
from train_convnext import (
    DATASET_STATS,
    ExperimentConfig,
    build_model,
    get_dataloaders,
)

DEFAULT_CHECKPOINT = "checkpoints/C4_4bit_noise_HAT_best.pt"
DEFAULT_OUTPUT = "report_md/_gpt/crosssim_comparison_results.json"
DEFAULT_LEGACY_OUTPUT = "report_md/_gpt/crosssim_convnext_results.json"
DEFAULT_LOG = "logs/_gpt/crosssim_convnext.log"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", default=DEFAULT_CHECKPOINT)
    parser.add_argument("--dataset", default="cifar10", choices=sorted(DATASET_STATS))
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--legacy-output", default=DEFAULT_LEGACY_OUTPUT)
    parser.add_argument("--log-file", default=DEFAULT_LOG)
    parser.add_argument("--adc-bits", type=int, default=8)
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--num-workers", type=int, default=2)
    parser.add_argument("--max-samples", type=int, default=0)
    parser.add_argument("--calibration-batches", type=int, default=5)
    parser.add_argument("--sigma-c2c", type=float, default=0.05)
    parser.add_argument("--sigma-d2d", type=float, default=0.10)
    parser.add_argument(
        "--crosssim-alpha-noise",
        type=float,
        default=None,
        help="Override CrossSim read-noise magnitude; defaults to --sigma-c2c",
    )
    parser.add_argument(
        "--crosssim-alpha-error",
        type=float,
        default=None,
        help="Override CrossSim programming-error magnitude; defaults to --sigma-d2d",
    )
    parser.add_argument("--weight-bits", type=int, default=4)
    parser.add_argument("--device", default=None)
    return parser.parse_args()


def log(message: str, log_file: Optional[Path]) -> None:
    stamped = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    print(stamped)
    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with log_file.open("a", encoding="utf-8") as fh:
            fh.write(stamped + "\n")


def load_config(ckpt: dict) -> ExperimentConfig:
    valid = {field.name for field in dataclasses.fields(ExperimentConfig)}
    filtered = {k: v for k, v in ckpt["exp_cfg"].items() if k in valid}
    if "name" not in filtered:
        filtered["name"] = "C4_alignment"
    return ExperimentConfig(**filtered)


def make_eval_loader(dataset: str, batch_size: int, num_workers: int, max_samples: int):
    _, test_loader = get_dataloaders(dataset, batch_size=batch_size, num_workers=num_workers)
    if max_samples <= 0:
        return test_loader
    subset = torch.utils.data.Subset(test_loader.dataset, list(range(min(max_samples, len(test_loader.dataset)))))
    return torch.utils.data.DataLoader(
        subset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
    )


def evaluate_accuracy(
    model: nn.Module,
    loader,
    device: str,
    progress_prefix: Optional[str] = None,
    log_file: Optional[Path] = None,
    progress_every: int = 0,
) -> float:
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        total_batches = len(loader)
        for batch_idx, (inputs, targets) in enumerate(loader, start=1):
            inputs = inputs.to(device)
            targets = targets.to(device)
            outputs = model(inputs)
            preds = outputs.argmax(1)
            correct += preds.eq(targets).sum().item()
            total += targets.size(0)
            if (
                progress_prefix
                and progress_every > 0
                and (batch_idx % progress_every == 0 or batch_idx == total_batches)
            ):
                running = 100.0 * correct / max(total, 1)
                log(
                    f"{progress_prefix}: batch {batch_idx}/{total_batches}, "
                    f"running_acc={running:.2f}%",
                    log_file,
                )
    return 100.0 * correct / total


def build_analog_model(
    ckpt: dict,
    exp_cfg: ExperimentConfig,
    dataset: str,
    device: str,
    noise_enabled: bool,
) -> nn.Module:
    num_classes = DATASET_STATS[dataset]["num_classes"]
    img_sz = DATASET_STATS[dataset]["image_size"]
    cfg = dataclasses.replace(exp_cfg)
    cfg.use_analog = True
    cfg.noise_enabled = noise_enabled
    model = build_model(cfg, num_classes=num_classes, image_size=img_sz, device=device)
    model.load_state_dict(ckpt["model_state_dict"], strict=True)
    return model


def build_effective_digital_model(
    ckpt: dict,
    exp_cfg: ExperimentConfig,
    dataset: str,
    device: str,
) -> nn.Module:
    analog_model = build_analog_model(ckpt, exp_cfg, dataset, device, noise_enabled=True)
    analog_model.eval()

    num_classes = DATASET_STATS[dataset]["num_classes"]
    img_sz = DATASET_STATS[dataset]["image_size"]
    digital_cfg = dataclasses.replace(exp_cfg, use_analog=False, noise_enabled=False)
    digital_model = build_model(digital_cfg, num_classes=num_classes, image_size=img_sz, device=device)

    mapped_state = {}
    analog_state = analog_model.state_dict()
    for name, module in analog_model.named_modules():
        if isinstance(module, (AnalogConv2d, AnalogLinear)):
            with torch.no_grad():
                module.config.noise_enabled = False 
                
                G_pos, G_neg = module._weight_to_conductance(module.weight)
                retained_diff = G_pos - G_neg
                
                mapped_state[f"{name}.weight"] = retained_diff * module._conductance_to_weight_scale(
                    module.weight, retained_diff
                )
                if module.bias is not None:
                    mapped_state[f"{name}.bias"] = module.bias.detach().clone()

    for key, value in analog_state.items():
        if "d2d_noise" in key or "w_abs_max" in key or "bias_abs_max" in key:
            continue
        if key not in mapped_state:
            mapped_state[key] = value

    digital_model.load_state_dict(mapped_state, strict=True)
    return digital_model


def calibrate_convnext_adc_ranges(
    ckpt: dict,
    exp_cfg: ExperimentConfig,
    dataset: str,
    device: str,
    loader,
    checkpoint_path: str,
    calibration_batches: int,
) -> dict:
    model = build_analog_model(ckpt, exp_cfg, dataset, device, noise_enabled=False)
    set_uniform_noise(
        model,
        sigma_c2c=0.0,
        sigma_d2d=0.0,
        noise_enabled=False,
        resample_d2d=False,
        noise_mode=exp_cfg.noise_mode,
    )
    bundle = ModelBundle(
        model_type="convnext",
        experiment=exp_cfg.name,
        experiment_name=exp_cfg.name,
        dataset=dataset,
        device=device,
        model=model,
        exp_cfg=exp_cfg,
        testloader=loader,
        criterion=nn.CrossEntropyLoss(),
        frontend=None,
        checkpoint_path=checkpoint_path,
        checkpoint_epoch=ckpt.get("epoch"),
        checkpoint_best_acc=ckpt.get("best_acc"),
        amp_enabled=False,
    )
    return calibrate_adc_ranges(bundle, max_batches=calibration_batches)


def calibrate_crosssim_input_ranges(model: nn.Module, loader, max_batches: int, device: str):
    input_ranges = {}
    profile_counts = {}
    hooks = []

    def make_hook(index: int, module: nn.Module):
        def hook(_module, inputs, _output):
            x = inputs[0].detach()
            input_ranges.setdefault(index, [float("inf"), float("-inf")])
            input_ranges[index][0] = min(input_ranges[index][0], float(x.min()))
            input_ranges[index][1] = max(input_ranges[index][1], float(x.max()))
            if isinstance(module, nn.Linear):
                count = 1 if x.ndim == 1 else int(np.prod(x.shape[:-1]))
            else:
                count = int(x.shape[0]) if x.ndim > 0 else 1
            profile_counts[index] = profile_counts.get(index, 0) + count
        return hook

    modules = convertible_modules(model)
    for idx, module in enumerate(modules):
        hooks.append(module.register_forward_hook(make_hook(idx, module)))

    try:
        with torch.no_grad():
            for batch_idx, (inputs, _targets) in enumerate(loader):
                if batch_idx >= max_batches:
                    break
                model(inputs.to(device))
    finally:
        for hook in hooks:
            hook.remove()

    return input_ranges, profile_counts


def build_crosssim_params(
    model: nn.Module,
    input_ranges,
    adc_ranges,
    adc_bits: int,
    weight_bits: int,
    alpha_noise: float,
    alpha_error: float,
    device: str,
    profile_adc_inputs: bool = False,
    profile_samples=None,
) -> List[object]:
    params_list = []
    analog_idx = 0
    for idx, module in enumerate(convertible_modules(model)):
        in_min, in_max = input_ranges[idx]
        in_min, in_max = in_min - 1e-4, in_max + 1e-4

        positive_only = in_min >= 0.0
        if positive_only:
            input_range = (0.0, in_max)
        else:
            abs_in = max(abs(in_min), abs(in_max))
            input_range = (-abs_in, abs_in)

        is_analog = True
        if isinstance(module, nn.Conv2d):
            if module.groups > 1 and module.groups == module.in_channels:
                is_analog = False
        
        # ConvNeXt also has LayerNorm and fully connected layers. 
        # In our framework convert_resnet_to_analog converts all nn.Conv2d (non-depthwise) and nn.Linear.
        
        if not is_analog:
            params_list.append(
                dnn_inference_params(
                    ideal=True,
                    useGPU=(device == "cuda"),
                )
            )
            continue

        adc_range = adc_ranges[analog_idx] if adc_ranges is not None else (-1.0, 1.0)
        analog_idx += 1

        params_list.append(
            dnn_inference_params(
                ideal=False,
                core_style="BALANCED",
                Nslices=1,
                weight_bits=weight_bits,
                weight_percentile=100,
                digital_bias=True,
                Rmin=1e4,
                Rmax=1e6,
                infinite_on_off_ratio=False,
                error_model="generic",
                alpha_error=alpha_error,
                proportional_error=False,
                noise_model="generic",
                alpha_noise=alpha_noise,
                proportional_noise=False,
                drift_model="none",
                t_drift=0,
                NrowsMax=512,
                NcolsMax=None,
                Rp_row=0,
                Rp_col=0,
                interleaved_posneg=False,
                subtract_current_in_xbar=True,
                current_from_input=True,
                input_bits=8,
                input_bitslicing=False,
                input_slice_size=1,
                adc_bits=adc_bits,
                adc_range_option="CALIBRATED",
                adc_type="generic",
                adc_per_ibit=False,
                useGPU=(device == "cuda"),
                positiveInputsOnly=positive_only,
                input_range=input_range,
                adc_range=adc_range,
                profile_adc_inputs=profile_adc_inputs,
                ntest=(
                    int(profile_samples.get(idx, 1))
                    if isinstance(profile_samples, dict)
                    else int(profile_samples)
                    if profile_samples
                    else 1
                ),
            )
        )
    return params_list


def calibrate_crosssim_adc_ranges(
    digital_model: nn.Module,
    loader,
    calibration_batches: int,
    adc_bits: int,
    weight_bits: int,
    device: str,
):
    profile_loader = torch.utils.data.DataLoader(
        loader.dataset,
        batch_size=1,
        shuffle=False,
        num_workers=0,
    )
    input_ranges, profile_counts = calibrate_crosssim_input_ranges(
        digital_model, profile_loader, calibration_batches, device
    )
    profile_params = build_crosssim_params(
        digital_model,
        input_ranges=input_ranges,
        adc_ranges=None,
        adc_bits=0,
        weight_bits=weight_bits,
        alpha_noise=0.0,
        alpha_error=0.0,
        device=device,
        profile_adc_inputs=True,
        profile_samples=profile_counts,
    )
    profile_model = from_torch(digital_model, profile_params, fuse_batchnorm=True, bias_rows=0).to(device)
    profile_model.eval()

    with torch.no_grad():
        for batch_idx, (inputs, _targets) in enumerate(profile_loader):
            if batch_idx >= calibration_batches:
                break
            profile_model(inputs.to(device))

    profiled_inputs = get_profiled_adc_inputs(profile_model)
    profiled_layers = []
    filtered_inputs = []
    for layer, adc_input in zip(analog_modules(profile_model), profiled_inputs):
        if adc_input is None:
            continue
        profiled_layers.append(layer)
        filtered_inputs.append(adc_input)

    if not filtered_inputs:
        raise RuntimeError("CrossSim ADC profiling produced no ADC-input statistics")

    adc_ranges = calibrate_adc_limits(profiled_layers, filtered_inputs, Nbits=adc_bits)
    return input_ranges, adc_ranges


def summarize_runs(accuracies: List[float], elapsed: float) -> dict:
    return {
        "accuracies": accuracies,
        "mean": float(np.mean(accuracies)),
        "std": float(np.std(accuracies)),
        "runtime_total_s": float(elapsed),
        "runtime_per_run_s": float(elapsed / max(len(accuracies), 1)),
    }


def run_our_framework(
    ckpt: dict,
    exp_cfg: ExperimentConfig,
    checkpoint_path: str,
    dataset: str,
    device: str,
    loader,
    adc_bits: int,
    sigma_c2c: float,
    sigma_d2d: float,
    runs: int,
    calibration_batches: int,
    log_file: Optional[Path],
) -> dict:
    log("Calibrating our-framework ADC ranges", log_file)
    output_ranges = calibrate_convnext_adc_ranges(
        ckpt=ckpt,
        exp_cfg=exp_cfg,
        dataset=dataset,
        device=device,
        loader=loader,
        checkpoint_path=checkpoint_path,
        calibration_batches=calibration_batches,
    )
    log(f"Our-framework calibrated {len(output_ranges)} analog layer range(s)", log_file)

    accuracies = []
    started = time.time()
    for run_idx in range(runs):
        model = build_analog_model(ckpt, exp_cfg, dataset, device, noise_enabled=True)
        set_uniform_noise(
            model,
            sigma_c2c=sigma_c2c,
            sigma_d2d=sigma_d2d,
            noise_enabled=True,
            resample_d2d=True,
            noise_mode=exp_cfg.noise_mode,
        )
        with ADCQuantHookManager(model, output_ranges, adc_bits=adc_bits):
            acc = evaluate_accuracy(model, loader, device)
        accuracies.append(float(acc))
        log(f"Our-framework run {run_idx + 1}/{runs}: {acc:.2f}%", log_file)
    return summarize_runs(accuracies, time.time() - started)


def run_crosssim(
    ckpt: dict,
    exp_cfg: ExperimentConfig,
    dataset: str,
    device: str,
    loader,
    adc_bits: int,
    weight_bits: int,
    crosssim_alpha_noise: float,
    crosssim_alpha_error: float,
    runs: int,
    calibration_batches: int,
    log_file: Optional[Path],
) -> dict:
    digital_model = build_effective_digital_model(ckpt, exp_cfg, dataset, device)
    digital_model.eval()
    input_ranges, adc_ranges = calibrate_crosssim_adc_ranges(
        digital_model,
        loader,
        calibration_batches=calibration_batches,
        adc_bits=adc_bits,
        weight_bits=weight_bits,
        device=device,
    )
    params_list = build_crosssim_params(
        digital_model,
        input_ranges=input_ranges,
        adc_ranges=adc_ranges,
        adc_bits=adc_bits,
        weight_bits=weight_bits,
        alpha_noise=crosssim_alpha_noise,
        alpha_error=crosssim_alpha_error,
        device=device,
    )
    log(f"Converting {len(params_list)} layers to CrossSim", log_file)
    analog_model = from_torch(digital_model, params_list, fuse_batchnorm=True, bias_rows=0)
    analog_model = analog_model.to(device)
    analog_model.eval()
    log("CrossSim conversion complete", log_file)

    accuracies = []
    started = time.time()
    for run_idx in range(runs):
        if run_idx > 0 and reinitialize is not None:
            reinitialize(analog_model)
        acc = evaluate_accuracy(
            analog_model,
            loader,
            device,
            progress_prefix=f"CrossSim run {run_idx + 1}/{runs}",
            log_file=log_file,
            progress_every=4,
        )
        accuracies.append(float(acc))
        log(f"CrossSim run {run_idx + 1}/{runs}: {acc:.2f}%", log_file)
    return summarize_runs(accuracies, time.time() - started)


def save_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)


def main() -> None:
    args = parse_args()
    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")
    checkpoint_path = args.checkpoint
    log_file = Path(args.log_file) if args.log_file else None

    if not os.path.exists(checkpoint_path):
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")

    log(f"Using device: {device}", log_file)
    log(f"Loading checkpoint: {checkpoint_path}", log_file)
    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    exp_cfg = load_config(ckpt)
    crosssim_alpha_noise = args.crosssim_alpha_noise if args.crosssim_alpha_noise is not None else args.sigma_c2c
    crosssim_alpha_error = args.crosssim_alpha_error if args.crosssim_alpha_error is not None else args.sigma_d2d
    loader = make_eval_loader(args.dataset, args.batch_size, args.num_workers, args.max_samples)
    log(
        f"Dataset={args.dataset} samples={len(loader.dataset)} runs={args.runs} "
        f"adc={args.adc_bits}bit",
        log_file,
    )
    log(
        f"CrossSim noise mapping: alpha_error={crosssim_alpha_error:.4f} "
        f"alpha_noise={crosssim_alpha_noise:.4f}",
        log_file,
    )

    our_framework = run_our_framework(
        ckpt=ckpt,
        exp_cfg=exp_cfg,
        checkpoint_path=checkpoint_path,
        dataset=args.dataset,
        device=device,
        loader=loader,
        adc_bits=args.adc_bits,
        sigma_c2c=args.sigma_c2c,
        sigma_d2d=args.sigma_d2d,
        runs=args.runs,
        calibration_batches=args.calibration_batches,
        log_file=log_file,
    )

    crosssim = run_crosssim(
        ckpt=ckpt,
        exp_cfg=exp_cfg,
        dataset=args.dataset,
        device=device,
        loader=loader,
        adc_bits=args.adc_bits,
        weight_bits=args.weight_bits,
        crosssim_alpha_noise=crosssim_alpha_noise,
        crosssim_alpha_error=crosssim_alpha_error,
        runs=args.runs,
        calibration_batches=args.calibration_batches,
        log_file=log_file,
    )

    payload = {
        "experiment": "ConvNeXt-Tiny CrossSim comparison",
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "checkpoint": checkpoint_path,
        "dataset": args.dataset,
        "adc_bits": args.adc_bits,
        "weight_bits": args.weight_bits,
        "sigma_c2c": args.sigma_c2c,
        "sigma_d2d": args.sigma_d2d,
        "crosssim_alpha_noise": crosssim_alpha_noise,
        "crosssim_alpha_error": crosssim_alpha_error,
        "max_samples": args.max_samples if args.max_samples > 0 else len(loader.dataset),
        "our_framework": our_framework,
        "crosssim": crosssim,
        "notes": {
            "checkpoint_eval_model": "our_framework uses fresh D2D resampling plus ADCQuantHookManager",
            "crosssim_noise_mapping": "CrossSim generic programming_error/read_noise magnitudes are not identical to the framework's fixed-D2D plus per-forward C2C implementation",
        },
    }

    save_json(Path(args.output), payload)
    save_json(Path(args.legacy_output), payload)
    log(f"Saved comparison results to {args.output}", log_file)


if __name__ == "__main__":
    main()
