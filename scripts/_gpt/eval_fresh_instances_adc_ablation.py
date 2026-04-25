#!/usr/bin/env python3
"""Fresh-instance evaluator with hook-based ADC quantization enabled.

This is an inference-only ablation for the M-series ADC-off/default-forward
caveat. It uses the existing ADCQuantHookManager path in
inference_analysis_utils.py and does not modify checkpoints.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import numpy as np
import torch

from eval_fresh_instances_postfix import (
    load_checkpoint_provenance,
    resolve_eval_overrides,
    runtime_metadata,
)
from inference_analysis_utils import (
    ADCQuantHookManager,
    calibrate_adc_ranges,
    load_model_bundle,
    run_mc_eval,
    set_uniform_noise,
)


def push_eval_config(bundle, nl_ltp, nl_ltd, noise_mode):
    cfg = bundle.exp_cfg
    if nl_ltp is not None:
        cfg.nl_ltp = nl_ltp
    if nl_ltd is not None:
        cfg.nl_ltd = nl_ltd
    if noise_mode is not None:
        cfg.noise_mode = noise_mode

    for module in bundle.model.modules():
        if not hasattr(module, "config"):
            continue
        if nl_ltp is not None:
            module.config.NL_LTP = nl_ltp
        if nl_ltd is not None:
            module.config.NL_LTD = nl_ltd
        if noise_mode is not None:
            module.config.noise_mode = noise_mode


def evaluate_with_adc(
    model_type,
    exp_id,
    checkpoint_path,
    device,
    num_instances,
    mc_runs_per_instance,
    nl_ltp,
    nl_ltd,
    noise_mode,
    allow_eval_nl_override,
    adc_bits,
    adc_dnl_sigma,
    adc_calibration_batches,
    num_workers,
    batch_size,
):
    provenance = load_checkpoint_provenance(checkpoint_path)
    nl_ltp, nl_ltd, noise_mode, mismatches = resolve_eval_overrides(
        provenance,
        nl_ltp=nl_ltp,
        nl_ltd=nl_ltd,
        noise_mode=noise_mode,
        allow_eval_nl_override=allow_eval_nl_override,
    )

    bundle = load_model_bundle(
        model_type,
        exp_id,
        device,
        checkpoint_path=checkpoint_path,
        num_workers=num_workers,
        batch_size=batch_size,
        amp_enabled=True,
    )
    push_eval_config(bundle, nl_ltp, nl_ltd, noise_mode)
    cfg = bundle.exp_cfg

    print(f"\n[ADC-ON] Evaluating {exp_id} from {checkpoint_path}")
    print(f"  Fresh protocol: {num_instances} instances x {mc_runs_per_instance} MC runs")
    print(f"  NL/noise: NL_LTP={cfg.nl_ltp}, NL_LTD={cfg.nl_ltd}, noise_mode={cfg.noise_mode}")
    print(f"  ADC: bits={adc_bits}, dnl_sigma={adc_dnl_sigma}, calibration_batches={adc_calibration_batches}")
    print(
        "  Checkpoint provenance: "
        f"NL_LTP={provenance.get('checkpoint_nl_ltp')}, "
        f"NL_LTD={provenance.get('checkpoint_nl_ltd')}, "
        f"noise_mode={provenance.get('checkpoint_noise_mode')}, "
        f"seed={provenance.get('checkpoint_seed')}"
    )

    instance_accs = []
    calibrated_module_counts = []
    for instance_idx in range(num_instances):
        seed = 42 + instance_idx * 100
        torch.manual_seed(seed)
        np.random.seed(seed)

        set_uniform_noise(
            bundle.model,
            sigma_c2c=cfg.sigma_c2c,
            sigma_d2d=cfg.sigma_d2d,
            noise_enabled=cfg.noise_enabled,
            resample_d2d=True,
            noise_mode=cfg.noise_mode,
        )
        output_ranges = calibrate_adc_ranges(
            bundle,
            max_batches=adc_calibration_batches,
            use_current_noise=True,
            disable_c2c=True,
        )
        calibrated_module_counts.append(len(output_ranges))
        print(
            f"  Instance {instance_idx + 1}: calibrated ADC ranges for "
            f"{len(output_ranges)} analog modules"
        )
        # New hook manager per instance: treats ADC DNL as part of the fresh device draw.
        with ADCQuantHookManager(bundle.model, output_ranges, adc_bits=adc_bits, dnl_sigma=adc_dnl_sigma):
            stats = run_mc_eval(
                bundle,
                eval_runs=mc_runs_per_instance,
                label=f"ADC Instance {instance_idx + 1}/{num_instances}",
            )
        instance_accs.append(stats["test_acc_mean"])
        print(f"  Instance {instance_idx + 1}: {stats['test_acc_mean']:.2f}%")

    mean_acc = float(np.mean(instance_accs))
    std_acc = float(np.std(instance_accs))
    print(
        f"Result ADC-ON: Mean={mean_acc:.4f}%, Std={std_acc:.4f}%, "
        f"Range={min(instance_accs):.2f}--{max(instance_accs):.2f}%\n"
    )

    return {
        "checkpoint_path": str(checkpoint_path),
        "exp_id": exp_id,
        "fresh_instances": num_instances,
        "mc_runs_per_instance": mc_runs_per_instance,
        "nl_ltp": cfg.nl_ltp,
        "nl_ltd": cfg.nl_ltd,
        "noise_mode": cfg.noise_mode,
        "allow_eval_nl_override": allow_eval_nl_override,
        "eval_provenance_mismatches": mismatches,
        "adc_enabled": True,
        "adc_bits": adc_bits,
        "adc_dnl_sigma": adc_dnl_sigma,
        "adc_calibration_batches": adc_calibration_batches,
        "adc_calibration_scope": "per_instance",
        "adc_calibration_noise": "current_d2d_with_c2c_disabled",
        "adc_calibrated_modules": calibrated_module_counts[0] if calibrated_module_counts else 0,
        "adc_calibrated_modules_per_instance": calibrated_module_counts,
        **provenance,
        **runtime_metadata(),
        "cross_instance_mean": mean_acc,
        "cross_instance_std": std_acc,
        "instance_means": instance_accs,
        "fresh_per_instance_mean": instance_accs,
        "fresh_aggregate": {
            "mean": mean_acc,
            "std": std_acc,
            "median": float(np.median(instance_accs)),
            "range": [float(min(instance_accs)), float(max(instance_accs))],
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--exp-id", default="V4")
    parser.add_argument("--model-type", default="tinyvit")
    parser.add_argument("--device", default=None)
    parser.add_argument("--num-instances", type=int, default=10)
    parser.add_argument("--mc-runs", type=int, default=5)
    parser.add_argument("--nl-ltp", type=float, default=None)
    parser.add_argument("--nl-ltd", type=float, default=None)
    parser.add_argument("--noise-mode", default=None)
    parser.add_argument("--allow-eval-nl-override", action="store_true")
    parser.add_argument("--adc-bits", type=int, default=8)
    parser.add_argument("--adc-dnl-sigma", type=float, default=0.5)
    parser.add_argument("--adc-calibration-batches", type=int, default=2)
    parser.add_argument("--num-workers", type=int, default=2)
    parser.add_argument("--batch-size", type=int, default=None)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")
    result = evaluate_with_adc(
        args.model_type,
        args.exp_id,
        args.checkpoint,
        device,
        args.num_instances,
        args.mc_runs,
        args.nl_ltp,
        args.nl_ltd,
        args.noise_mode,
        args.allow_eval_nl_override,
        args.adc_bits,
        args.adc_dnl_sigma,
        args.adc_calibration_batches,
        args.num_workers,
        args.batch_size,
    )

    output_path = args.output or f"report_md/_gpt/json_gpt/{Path(args.checkpoint).stem}_adc_fresh_eval.json"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)
    print(f"Saved to {output_path}")


if __name__ == "__main__":
    main()
