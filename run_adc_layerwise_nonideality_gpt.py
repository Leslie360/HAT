#!/usr/bin/env python3
"""Layer-wise ADC non-ideality sweep using analog-layer output hooks.

This script is a stricter follow-up to earlier reviewer-response analyses that
perturbed only the final logits. Here we calibrate output ranges for every
analog layer and inject ADC offset / gain / INL errors directly at those layer
outputs during inference.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from statistics import mean, stdev
from typing import Dict, List, Optional

import torch

from amp_utils import autocast_context
from inference_analysis_utils import (
    calibrate_adc_ranges,
    iter_analog_modules,
    load_model_bundle,
)
from train_tinyvit import set_seed


DEFAULT_OUTPUT_JSON = "report_md/_gpt/json_gpt/adc_layerwise_nonideality_results_gpt.json"
DEFAULT_OUTPUT_MD = "report_md/_gpt/adc_layerwise_nonideality_results_gpt.md"


ADC_CONFIGS = [
    {
        "name": "Ideal",
        "adc_bits": 8,
        "offset_lsb": 0.0,
        "gain_error": 0.0,
        "inl_lsb": 0.0,
    },
    {
        "name": "Offset +/-0.5 LSB",
        "adc_bits": 8,
        "offset_lsb": 0.5,
        "gain_error": 0.0,
        "inl_lsb": 0.0,
    },
    {
        "name": "Gain +/-5%",
        "adc_bits": 8,
        "offset_lsb": 0.0,
        "gain_error": 0.05,
        "inl_lsb": 0.0,
    },
    {
        "name": "INL 0.5 LSB",
        "adc_bits": 8,
        "offset_lsb": 0.0,
        "gain_error": 0.0,
        "inl_lsb": 0.5,
    },
    {
        "name": "Combined realistic",
        "adc_bits": 8,
        "offset_lsb": 0.5,
        "gain_error": 0.05,
        "inl_lsb": 0.5,
    },
    {
        "name": "Combined pessimistic",
        "adc_bits": 8,
        "offset_lsb": 1.0,
        "gain_error": 0.10,
        "inl_lsb": 1.0,
    },
]


class LayerwiseADCNonIdealHookManager:
    """Attach deterministic ADC non-idealities to analog-layer outputs."""

    def __init__(
        self,
        model: torch.nn.Module,
        output_ranges: Dict[str, dict],
        adc_bits: int,
        offset_lsb: float = 0.0,
        gain_error: float = 0.0,
        inl_lsb: float = 0.0,
    ):
        self.model = model
        self.output_ranges = output_ranges
        self.adc_bits = adc_bits
        self.offset_lsb = offset_lsb
        self.gain_error = gain_error
        self.inl_lsb = inl_lsb
        self._hooks = []

    def _apply_nonideality(self, output: torch.Tensor, limits: dict) -> torch.Tensor:
        x = output.float()
        i_min = float(limits["min"])
        i_max = float(limits["max"])
        n_levels = 2 ** int(self.adc_bits)
        full_scale = max(i_max - i_min, 1e-8)
        q_step = full_scale / max(n_levels - 1, 1)

        if self.gain_error:
            x = x * (1.0 + self.gain_error)
        if self.offset_lsb:
            x = x + self.offset_lsb * q_step

        x = torch.clamp(x, i_min, i_max)
        code = torch.round((x - i_min) / q_step).clamp(0, n_levels - 1)
        quantized = code * q_step + i_min

        if self.inl_lsb:
            inl = self.inl_lsb * q_step * torch.sin(code * (2.0 * math.pi / n_levels))
            quantized = quantized + inl

        quantized = torch.clamp(quantized, i_min, i_max)
        return quantized.to(dtype=output.dtype)

    def _make_hook(self, limits: dict):
        def hook(_module, _inputs, output):
            if not isinstance(output, torch.Tensor):
                return output
            return self._apply_nonideality(output, limits)

        return hook

    def __enter__(self):
        for name, module in iter_analog_modules(self.model):
            limits = self.output_ranges.get(name)
            if limits is None:
                continue
            self._hooks.append(module.register_forward_hook(self._make_hook(limits)))
        return self

    def __exit__(self, exc_type, exc, tb):
        for hook in self._hooks:
            hook.remove()
        self._hooks.clear()
        return False


def evaluate_accuracy(bundle, output_ranges: Dict[str, dict], config: dict,
                      max_batches: Optional[int] = None) -> float:
    bundle.model.eval()
    correct = 0
    total = 0

    with LayerwiseADCNonIdealHookManager(
        bundle.model,
        output_ranges=output_ranges,
        adc_bits=config["adc_bits"],
        offset_lsb=config["offset_lsb"],
        gain_error=config["gain_error"],
        inl_lsb=config["inl_lsb"],
    ):
        with torch.no_grad():
            for batch_idx, (inputs, targets) in enumerate(bundle.testloader):
                if max_batches is not None and batch_idx >= max_batches:
                    break
                inputs = inputs.to(bundle.device)
                targets = targets.to(bundle.device)
                if bundle.frontend is not None:
                    inputs = bundle.frontend(inputs, mode="compensated")
                with autocast_context(bundle.device, bundle.amp_enabled):
                    outputs = bundle.model(inputs)
                predictions = outputs.argmax(dim=1)
                correct += predictions.eq(targets).sum().item()
                total += targets.size(0)

    return 100.0 * correct / max(total, 1)


def summarise_rows(rows: List[dict]) -> str:
    baseline = next((row for row in rows if row["name"] == "Ideal"), None)
    baseline_acc = baseline["mean"] if baseline else rows[0]["mean"]
    lines = [
        "# Layer-wise ADC Non-Ideality Sweep",
        "",
        "| Configuration | Mean Acc. (%) | Std. (%) | Delta vs Ideal (pp) |",
        "|:--|--:|--:|--:|",
    ]
    for row in rows:
        delta = row["mean"] - baseline_acc
        lines.append(
            f"| {row['name']} | {row['mean']:.2f} | {row['std']:.2f} | {delta:+.2f} |"
        )
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--experiment", default="V4")
    parser.add_argument("--dataset", default="cifar10")
    parser.add_argument("--checkpoint-path", default=None)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--num-workers", type=int, default=2)
    parser.add_argument("--max-batches", type=int, default=None)
    parser.add_argument("--max-configs", type=int, default=None)
    parser.add_argument("--max-seeds", type=int, default=None)
    parser.add_argument("--output-json", default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", default=DEFAULT_OUTPUT_MD)
    args = parser.parse_args()

    seeds = [42, 123, 456]
    if args.max_seeds is not None:
        seeds = seeds[: args.max_seeds]

    configs = ADC_CONFIGS
    if args.max_configs is not None:
        configs = configs[: args.max_configs]

    print("=" * 78)
    print("Layer-wise ADC non-ideality sweep")
    print("=" * 78)
    print(f"Device: {args.device}")
    print(f"Experiment: {args.experiment}")
    print(f"Dataset: {args.dataset}")
    print(f"Seeds: {seeds}")
    print(f"Configs: {[cfg['name'] for cfg in configs]}")
    print()

    calibration_bundle = load_model_bundle(
        model_type="tinyvit",
        experiment=args.experiment,
        dataset=args.dataset,
        device=args.device,
        checkpoint_path=args.checkpoint_path,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        amp_enabled=True,
    )
    output_ranges = calibrate_adc_ranges(calibration_bundle, max_batches=5)
    print(f"Calibrated ADC ranges for {len(output_ranges)} analog layers.")

    rows: List[dict] = []
    for config in configs:
        print()
        print("-" * 78)
        print(
            f"{config['name']}: bits={config['adc_bits']}, "
            f"offset={config['offset_lsb']} LSB, "
            f"gain={config['gain_error'] * 100:.1f}%, "
            f"inl={config['inl_lsb']} LSB"
        )
        print("-" * 78)

        accuracies: List[float] = []
        for seed in seeds:
            set_seed(seed)
            bundle = load_model_bundle(
                model_type="tinyvit",
                experiment=args.experiment,
                dataset=args.dataset,
                device=args.device,
                checkpoint_path=args.checkpoint_path,
                batch_size=args.batch_size,
                num_workers=args.num_workers,
                amp_enabled=True,
            )
            acc = evaluate_accuracy(bundle, output_ranges, config, max_batches=args.max_batches)
            accuracies.append(acc)
            print(f"seed {seed}: {acc:.2f}%")

        row = {
            "name": config["name"],
            "adc_bits": config["adc_bits"],
            "offset_lsb": config["offset_lsb"],
            "gain_error": config["gain_error"],
            "inl_lsb": config["inl_lsb"],
            "accuracies": accuracies,
            "mean": mean(accuracies),
            "std": stdev(accuracies) if len(accuracies) > 1 else 0.0,
        }
        rows.append(row)
        print(f"mean: {row['mean']:.2f}% ± {row['std']:.2f}%")

    payload = {
        "metadata": {
            "experiment": args.experiment,
            "dataset": args.dataset,
            "device": args.device,
            "seeds": seeds,
            "notes": (
                "ADC offset/gain/INL injected at analog-layer outputs via forward hooks "
                "using per-layer calibrated output ranges."
            ),
        },
        "results": rows,
    }

    output_json = Path(args.output_json)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    output_md = Path(args.output_md)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(summarise_rows(rows), encoding="utf-8")

    print()
    print("=" * 78)
    print(summarise_rows(rows).strip())
    print("=" * 78)
    print(f"Wrote {output_json}")
    print(f"Wrote {output_md}")


if __name__ == "__main__":
    main()
