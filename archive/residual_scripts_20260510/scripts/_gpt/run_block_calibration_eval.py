#!/usr/bin/env python3
"""End-to-end evaluation of block-output affine calibration for fresh-instance robustness.

Fits per-block affine calibration on a small calibration set, then evaluates
on test set with fresh D2D resampling.

Experiment matrix (per Codex recommendation):
  E2: all_analog + block_affine_calib
  E3: mlp_digital + attention_block_affine_calib
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from statistics import mean, stdev

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import torch
import torch.nn as nn

from hybrid_calibration import (
    ActivationCapture,
    AffineCalibrator,
    disable_all_analog_noise,
    restore_analog_noise,
)
from run_tinyvit_groupwise_nl_comp import build_selector
import train_tinyvit_ensemble as base
from train_tinyvit_ensemble import (
    TinyViTExperimentConfig,
    build_model,
    evaluate,
    get_dataloaders,
    resample_all_d2d_noise,
)
from train_tinyvit import set_seed


def get_block_names(model: nn.Module) -> list:
    """Get all transformer block names in the model."""
    blocks = []
    for name, module in model.named_modules():
        # Match pattern: stages.{i}.blocks.{j} (but not sub-modules)
        parts = name.split('.')
        if len(parts) == 4 and parts[0] == 'stages' and parts[2] == 'blocks':
            blocks.append(name)
    return blocks


def apply_calibration_to_model(model: nn.Module, calibrator: AffineCalibrator):
    """Register forward hooks to apply calibration to block outputs."""
    handles = []
    for name, module in model.named_modules():
        if name in calibrator.gamma:
            def make_hook(n):
                def hook(m, inp, out):
                    return calibrator.apply(n, out)
                return hook
            handles.append(module.register_forward_hook(make_hook(name)))
    return handles


def evaluate_with_calibration(
    checkpoint_path: str,
    device: str,
    fresh_instances: int,
    eval_runs: int,
    data_root: str,
    num_workers: int,
    num_calib_samples: int,
    apply_mlp_digital: bool,
    calib_target: str,  # 'all_blocks', 'attention_only', 'mlp_only'
    resample_scope: str,
    dataset: str | None = None,
    eval_batch_size: int | None = None,
    num_classes: int | None = None,
    protected_group: str = "all",
    protected_nl_ltp: float = 1.0,
    protected_nl_ltd: float = -1.0,
) -> dict:
    print(f"\n{'='*60}")
    print(f"Block Calibration Eval")
    print(f"  checkpoint: {checkpoint_path}")
    print(f"  calib_samples: {num_calib_samples}")
    print(f"  mlp_digital: {apply_mlp_digital}")
    print(f"  calib_target: {calib_target}")
    print(f"  resample_scope: {resample_scope}")
    print(f"{'='*60}", flush=True)
    
    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    exp_cfg_dict = ckpt.get("exp_cfg", {})
    valid_keys = {f.name for f in __import__("dataclasses").fields(TinyViTExperimentConfig)}
    filtered = {k: v for k, v in exp_cfg_dict.items() if k in valid_keys}
    cfg = TinyViTExperimentConfig(**filtered)
    resolved_dataset = dataset or ckpt.get("dataset") or "cifar10"
    head_weight = (ckpt.get("model_state_dict") or {}).get("head.fc.weight")
    resolved_num_classes = num_classes
    if resolved_num_classes is None:
        if ckpt.get("num_classes") is not None:
            resolved_num_classes = int(ckpt["num_classes"])
        elif head_weight is not None:
            resolved_num_classes = int(head_weight.shape[0])
        else:
            resolved_num_classes = 10
    resolved_batch_size = eval_batch_size or 256
    
    trainloader, testloader = get_dataloaders(
        dataset=resolved_dataset,
        batch_size=resolved_batch_size,
        data_root=data_root,
        num_workers=num_workers,
    )
    criterion = nn.CrossEntropyLoss()
    
    instance_means = []
    instance_rows = []
    
    for instance_idx in range(fresh_instances):
        seed = 42 + instance_idx * 100
        set_seed(seed)
        model = build_model(cfg, num_classes=resolved_num_classes, device=device, pretrained=False)
        model.load_state_dict(ckpt["model_state_dict"], strict=True)
        
        # Apply MLP digital if requested
        if apply_mlp_digital:
            for name, module in model.named_modules():
                if ".mlp.fc" in name and hasattr(module, 'config'):
                    module.config.noise_enabled = False
                    module.config.sigma_c2c = 0.0
                    module.config.sigma_d2d = 0.0
        
        # Resample D2D
        if resample_scope == "all":
            resampled = resample_all_d2d_noise(model)
        elif resample_scope == "none":
            resampled = 0
        else:
            sel = build_selector(resample_scope)
            resampled = 0
            for name, m in model.named_modules():
                if hasattr(m, "resample_d2d_noise") and callable(m.resample_d2d_noise):
                    if sel(name):
                        m.resample_d2d_noise()
                        resampled += 1
        
        # Ensure eval noise config is set (evaluate() will call set_noise_for_eval internally)
        
        # Fit block calibration
        block_names = get_block_names(model)
        if calib_target == 'attention_only':
            # Only calibrate blocks with attention
            block_names = [b for b in block_names if any(
                b in name and 'attn' in name
                for name, _ in model.named_modules()
            )] or block_names
        elif calib_target == 'mlp_only':
            block_names = [b for b in block_names if any(
                b in name and 'mlp' in name
                for name, _ in model.named_modules()
            )] or block_names
        
        # Take calibration samples from trainloader
        calib_images = []
        calib_labels = []
        for images, labels in trainloader:
            calib_images.append(images)
            calib_labels.append(labels)
            if sum(len(im) for im in calib_images) >= num_calib_samples:
                break
        calib_images = torch.cat(calib_images, dim=0)[:num_calib_samples]
        calib_labels = torch.cat(calib_labels, dim=0)[:num_calib_samples]
        calib_dataset = torch.utils.data.TensorDataset(calib_images, calib_labels)
        calib_loader = torch.utils.data.DataLoader(calib_dataset, batch_size=32, shuffle=False)
        
        # Fit calibration
        if num_calib_samples > 0 and len(block_names) > 0:
            from hybrid_calibration import fit_block_affine_calibration
            calibrator = fit_block_affine_calibration(
                model, calib_loader, device, block_names, num_calib_batches=2
            )
            calib_handles = apply_calibration_to_model(model, calibrator)
        else:
            calibrator = None
            calib_handles = []
        
        # Evaluate
        losses = []
        accs = []
        for _ in range(eval_runs):
            loss, acc = evaluate(model, testloader, criterion, device, cfg, amp_enabled=False)
            losses.append(float(loss))
            accs.append(float(acc))
        
        # Remove calibration hooks
        for h in calib_handles:
            h.remove()
        
        mean_acc = mean(accs)
        print(
            f"  instance {instance_idx + 1:02d}/{fresh_instances}: "
            f"mean_acc={mean_acc:.2f}% eval_runs={eval_runs} resampled={resampled} "
            f"calib_blocks={len(block_names) if calibrator else 0}",
            flush=True,
        )
        instance_means.append(mean_acc)
        instance_rows.append(
            {
                "instance_index": instance_idx,
                "seed": seed,
                "resampled_modules": resampled,
                "resample_scope": resample_scope,
                "eval_runs": eval_runs,
                "calib_samples": num_calib_samples,
                "calib_blocks": len(block_names) if calibrator else 0,
                "test_loss_mean": mean(losses),
                "test_acc_mean": mean_acc,
                "test_acc_std": stdev(accs) if len(accs) > 1 else 0.0,
                "test_acc_raw": accs,
            }
        )
    
    result = {
        "checkpoint_path": checkpoint_path,
        "train_best_acc": float(ckpt.get("best_acc", float("nan"))),
        "fresh_instances": fresh_instances,
        "mc_runs_per_instance": eval_runs,
        "num_calib_samples": num_calib_samples,
        "apply_mlp_digital": apply_mlp_digital,
        "calib_target": calib_target,
        "resample_scope": resample_scope,
        "dataset": resolved_dataset,
        "num_classes": resolved_num_classes,
        "eval_batch_size": resolved_batch_size,
        "cross_instance_mean": mean(instance_means),
        "cross_instance_std": stdev(instance_means) if len(instance_means) > 1 else 0.0,
        "instance_means": instance_means,
        "instances": instance_rows,
    }
    print(
        f"\nCompleted: {result['cross_instance_mean']:.2f}% +/- "
        f"{result['cross_instance_std']:.2f}% across {fresh_instances} fresh instances",
        flush=True,
    )
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--fresh-instances", type=int, default=5)
    parser.add_argument("--eval-runs", type=int, default=3)
    parser.add_argument("--data-root", default="./data")
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--num-calib-samples", type=int, default=64)
    parser.add_argument("--apply-mlp-digital", action="store_true")
    parser.add_argument("--calib-target", choices=["all_blocks", "attention_only", "mlp_only"], default="all_blocks")
    parser.add_argument("--resample-scope", choices=["all", "none"], default="all")
    parser.add_argument("--dataset", default=None)
    parser.add_argument("--num-classes", type=int, default=None)
    parser.add_argument("--eval-batch-size", type=int, default=None)
    parser.add_argument("--protected-group", default="all")
    parser.add_argument("--protected-nl-ltp", type=float, default=1.0)
    parser.add_argument("--protected-nl-ltd", type=float, default=-1.0)
    parser.add_argument("--json-out", default="report_md/_gpt/json_gpt/block_calibration_eval.json")
    args = parser.parse_args()
    
    result = evaluate_with_calibration(
        checkpoint_path=args.checkpoint,
        device=args.device,
        fresh_instances=args.fresh_instances,
        eval_runs=args.eval_runs,
        data_root=args.data_root,
        num_workers=args.num_workers,
        num_calib_samples=args.num_calib_samples,
        apply_mlp_digital=args.apply_mlp_digital,
        calib_target=args.calib_target,
        resample_scope=args.resample_scope,
        dataset=args.dataset,
        eval_batch_size=args.eval_batch_size,
        num_classes=args.num_classes,
        protected_group=args.protected_group,
        protected_nl_ltp=args.protected_nl_ltp,
        protected_nl_ltd=args.protected_nl_ltd,
    )
    
    out_path = Path(args.json_out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"JSON saved to: {out_path}")


if __name__ == "__main__":
    main()
