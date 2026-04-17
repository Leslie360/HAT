#!/usr/bin/env python3
"""
Iso-accuracy contour sweep for the Tiny-ViT ensemble HAT checkpoint.

This script evaluates the V4 ensemble checkpoint over a sigma_D2D x ADC-bit
grid, with auto-save/resume after each completed point.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple

import numpy as np
import torch
import torch.nn as nn

from amp_utils import amp_enabled_for_device
from inference_analysis_utils import (
    ADCQuantHookManager,
    ModelBundle,
    calibrate_adc_ranges,
    set_uniform_noise,
)
from train_tinyvit_ensemble import (
    DATASET_STATS,
    TinyViTExperimentConfig,
    build_model,
    evaluate,
    get_dataloaders,
)

sys.stdout.reconfigure(line_buffering=True)

DEFAULT_CHECKPOINT = "checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt"
DEFAULT_OUTPUT = "report_md/_gpt/iso_accuracy_contour_data.json"
DEFAULT_ERROR_OUTPUT = "report_md/_gpt/iso_accuracy_contour_errors.json"
DEFAULT_LOG = "logs/_gpt/iso_accuracy_contour.log"
DEFAULT_D2D = (1, 3, 5, 8, 10, 15, 20)
DEFAULT_ADC = (2, 3, 4, 5, 6, 7, 8, 10, 12)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", default=DEFAULT_CHECKPOINT)
    parser.add_argument("--dataset", default="cifar10", choices=sorted(DATASET_STATS))
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--error-output", default=DEFAULT_ERROR_OUTPUT)
    parser.add_argument("--log-file", default=DEFAULT_LOG)
    parser.add_argument("--d2d", nargs="*", type=float, default=list(DEFAULT_D2D))
    parser.add_argument("--adc-bits", nargs="*", type=int, default=list(DEFAULT_ADC))
    parser.add_argument("--sigma-c2c", type=float, default=5.0, help="Percent")
    parser.add_argument("--nl", type=float, default=1.0)
    parser.add_argument("--mc-runs", type=int, default=10)
    parser.add_argument("--sanity-runs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=256)
    parser.add_argument("--num-workers", type=int, default=4)
    parser.add_argument("--calibration-batches", type=int, default=5)
    parser.add_argument("--max-points", type=int, default=0)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--device", default=None)
    return parser.parse_args()


def log(message: str, log_file: Optional[Path]) -> None:
    stamped = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    print(stamped)
    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with log_file.open("a", encoding="utf-8") as fh:
            fh.write(stamped + "\n")


def load_rows(path: Path, overwrite: bool) -> List[dict]:
    if overwrite or not path.exists():
        return []
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    if isinstance(payload, list):
        return payload
    raise ValueError(f"{path} is not a JSON list; refusing to resume from it")


def load_errors(path: Path, overwrite: bool) -> List[dict]:
    if overwrite or not path.exists():
        return []
    with path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)
    return payload if isinstance(payload, list) else []


def save_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)


def completed_keys(rows: Iterable[dict]) -> set[Tuple[float, int]]:
    return {(float(row["d2d_pct"]), int(row["adc_bits"])) for row in rows}


def load_checkpoint_config(ckpt: dict) -> TinyViTExperimentConfig:
    valid = {field.name for field in dataclasses.fields(TinyViTExperimentConfig)}
    filtered = {k: v for k, v in ckpt["exp_cfg"].items() if k in valid}
    cfg = TinyViTExperimentConfig(**filtered)
    cfg.use_hybrid = True
    cfg.hat_training = True
    cfg.use_physical_frontend = False
    cfg.retention_enabled = False
    return cfg


def make_loader(dataset: str, batch_size: int, num_workers: int):
    train_loader, test_loader = get_dataloaders(
        dataset,
        batch_size=batch_size,
        num_workers=num_workers,
        data_root="./data",
    )

    def rebuild(loader, shuffle: bool):
        kwargs = {
            "batch_size": batch_size,
            "shuffle": shuffle,
            "num_workers": num_workers,
            "pin_memory": False,
        }
        if num_workers > 0:
            kwargs["persistent_workers"] = True
        return torch.utils.data.DataLoader(loader.dataset, **kwargs)

    return rebuild(train_loader, True), rebuild(test_loader, False)


def build_calibration_ranges(
    ckpt: dict,
    base_cfg: TinyViTExperimentConfig,
    checkpoint_path: str,
    dataset: str,
    device: str,
    test_loader,
    criterion: nn.Module,
    calibration_batches: int,
) -> dict:
    num_classes = DATASET_STATS[dataset]["num_classes"]
    amp_enabled = amp_enabled_for_device(True, device)
    model = build_model(base_cfg, num_classes=num_classes, device=device, pretrained=False)
    model.load_state_dict(ckpt["model_state_dict"], strict=True)
    set_uniform_noise(
        model,
        sigma_c2c=0.0,
        sigma_d2d=0.0,
        noise_enabled=False,
        resample_d2d=False,
        noise_mode=base_cfg.noise_mode,
    )
    bundle = ModelBundle(
        model_type="tinyvit",
        experiment=base_cfg.name,
        experiment_name=base_cfg.name,
        dataset=dataset,
        device=device,
        model=model,
        exp_cfg=base_cfg,
        testloader=test_loader,
        criterion=criterion,
        frontend=None,
        checkpoint_path=checkpoint_path,
        checkpoint_epoch=ckpt.get("epoch"),
        checkpoint_best_acc=ckpt.get("best_acc"),
        amp_enabled=amp_enabled,
    )
    return calibrate_adc_ranges(bundle, max_batches=calibration_batches)


def evaluate_point(
    ckpt: dict,
    base_cfg: TinyViTExperimentConfig,
    dataset: str,
    device: str,
    test_loader,
    criterion: nn.Module,
    output_ranges: dict,
    d2d_pct: float,
    adc_bits: int,
    sigma_c2c_pct: float,
    nl_value: float,
    mc_runs: int,
) -> dict:
    num_classes = DATASET_STATS[dataset]["num_classes"]
    point_cfg = dataclasses.replace(
        base_cfg,
        sigma_c2c=sigma_c2c_pct / 100.0,
        sigma_d2d=d2d_pct / 100.0,
        nl_ltp=nl_value,
        nl_ltd=-nl_value,
        adc_bits=adc_bits,
        noise_enabled=True,
    )

    accuracies: List[float] = []
    for run_idx in range(mc_runs):
        model = build_model(point_cfg, num_classes=num_classes, device=device, pretrained=False)
        model.load_state_dict(ckpt["model_state_dict"], strict=True)
        set_uniform_noise(
            model,
            sigma_c2c=point_cfg.sigma_c2c,
            sigma_d2d=point_cfg.sigma_d2d,
            noise_enabled=True,
            resample_d2d=True,
            noise_mode=point_cfg.noise_mode,
        )
        with ADCQuantHookManager(model, output_ranges, adc_bits=adc_bits):
            _, acc = evaluate(model, test_loader, criterion, device, point_cfg)
        accuracies.append(float(acc))

    return {
        "d2d_pct": float(d2d_pct),
        "adc_bits": int(adc_bits),
        "c2c_pct": float(sigma_c2c_pct),
        "nl": float(nl_value),
        "mean": float(np.mean(accuracies)),
        "std": float(np.std(accuracies)),
        "raw": accuracies,
    }


def sanity_checks(
    ckpt: dict,
    base_cfg: TinyViTExperimentConfig,
    dataset: str,
    device: str,
    test_loader,
    criterion: nn.Module,
    output_ranges: dict,
    sigma_c2c_pct: float,
    nl_value: float,
    sanity_runs: int,
    log_file: Optional[Path],
) -> None:
    checks = [
        ((0.0, 12), "~91%"),
        ((10.0, 8), "~86-88%"),
    ]
    for (d2d_pct, adc_bits), expectation in checks:
        row = evaluate_point(
            ckpt=ckpt,
            base_cfg=base_cfg,
            dataset=dataset,
            device=device,
            test_loader=test_loader,
            criterion=criterion,
            output_ranges=output_ranges,
            d2d_pct=d2d_pct,
            adc_bits=adc_bits,
            sigma_c2c_pct=sigma_c2c_pct,
            nl_value=nl_value,
            mc_runs=sanity_runs,
        )
        log(
            f"Sanity sigma_D2D={d2d_pct:.0f}% adc={adc_bits}bit -> "
            f"{row['mean']:.2f}% ± {row['std']:.2f}% (expected {expectation})",
            log_file,
        )


def main() -> None:
    args = parse_args()
    output_path = Path(args.output)
    error_path = Path(args.error_output)
    log_file = Path(args.log_file) if args.log_file else None
    checkpoint_path = args.checkpoint
    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")

    if not os.path.exists(checkpoint_path):
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")

    log(f"Using device: {device}", log_file)
    log(f"Loading checkpoint: {checkpoint_path}", log_file)

    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    base_cfg = load_checkpoint_config(ckpt)
    log(f"Checkpoint best_acc={ckpt.get('best_acc')} epoch={ckpt.get('epoch')}", log_file)

    _, test_loader = make_loader(args.dataset, args.batch_size, args.num_workers)
    criterion = nn.CrossEntropyLoss()

    log(
        f"Calibrating ADC ranges with {args.calibration_batches} batch(es) on clean activations",
        log_file,
    )
    output_ranges = build_calibration_ranges(
        ckpt=ckpt,
        base_cfg=base_cfg,
        checkpoint_path=checkpoint_path,
        dataset=args.dataset,
        device=device,
        test_loader=test_loader,
        criterion=criterion,
        calibration_batches=args.calibration_batches,
    )
    log(f"Calibrated {len(output_ranges)} analog layer range(s)", log_file)

    sanity_checks(
        ckpt=ckpt,
        base_cfg=base_cfg,
        dataset=args.dataset,
        device=device,
        test_loader=test_loader,
        criterion=criterion,
        output_ranges=output_ranges,
        sigma_c2c_pct=args.sigma_c2c,
        nl_value=args.nl,
        sanity_runs=args.sanity_runs,
        log_file=log_file,
    )

    rows = load_rows(output_path, overwrite=args.overwrite)
    errors = load_errors(error_path, overwrite=args.overwrite)
    done = completed_keys(rows)
    if rows:
        log(f"Resuming from {len(rows)} completed grid point(s)", log_file)

    point_budget = args.max_points if args.max_points > 0 else None
    completed_this_run = 0

    for d2d_pct in args.d2d:
        for adc_bits in args.adc_bits:
            key = (float(d2d_pct), int(adc_bits))
            if key in done:
                continue
            if point_budget is not None and completed_this_run >= point_budget:
                log("Reached --max-points limit; stopping early", log_file)
                save_json(output_path, rows)
                save_json(error_path, errors)
                return

            log(
                f"Evaluating sigma_D2D={float(d2d_pct):.1f}% adc={int(adc_bits)}bit "
                f"({args.mc_runs} MC runs)",
                log_file,
            )
            try:
                row = evaluate_point(
                    ckpt=ckpt,
                    base_cfg=base_cfg,
                    dataset=args.dataset,
                    device=device,
                    test_loader=test_loader,
                    criterion=criterion,
                    output_ranges=output_ranges,
                    d2d_pct=float(d2d_pct),
                    adc_bits=int(adc_bits),
                    sigma_c2c_pct=args.sigma_c2c,
                    nl_value=args.nl,
                    mc_runs=args.mc_runs,
                )
            except Exception as exc:  # noqa: BLE001
                err = {
                    "d2d_pct": float(d2d_pct),
                    "adc_bits": int(adc_bits),
                    "error": repr(exc),
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                }
                errors.append(err)
                log(
                    f"ERROR sigma_D2D={float(d2d_pct):.1f}% adc={int(adc_bits)}bit -> {exc}",
                    log_file,
                )
                save_json(error_path, errors)
                continue

            rows.append(row)
            rows.sort(key=lambda item: (float(item["d2d_pct"]), int(item["adc_bits"])))
            done.add(key)
            completed_this_run += 1
            save_json(output_path, rows)
            log(
                f"Saved sigma_D2D={row['d2d_pct']:.1f}% adc={row['adc_bits']}bit -> "
                f"{row['mean']:.2f}% ± {row['std']:.2f}%",
                log_file,
            )

    save_json(output_path, rows)
    save_json(error_path, errors)
    log(f"Completed contour sweep with {len(rows)} successful point(s)", log_file)


if __name__ == "__main__":
    main()
