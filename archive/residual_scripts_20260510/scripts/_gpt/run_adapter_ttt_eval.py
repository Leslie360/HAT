#!/usr/bin/env python3
"""Evaluate lightweight adapter + test-time training for fresh-instance robustness."""
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

from lightweight_adapter import inject_adapter_before_head, ttt_finetune_adapter, remove_adapter_from_head
from train_tinyvit_ensemble import (
    TinyViTExperimentConfig,
    build_model,
    evaluate,
    get_dataloaders,
    resample_all_d2d_noise,
)
from train_tinyvit import set_seed


def evaluate_with_adapter_ttt(
    checkpoint_path: str,
    device: str,
    fresh_instances: int,
    eval_runs: int,
    data_root: str,
    num_workers: int,
    num_calib_samples: int,
    num_ttt_steps: int,
    adapter_hidden_dim: int | None,
    adapter_dropout: float,
    ttt_lr: float,
    ttt_weight_decay: float,
    apply_mlp_digital: bool,
    dataset: str | None = None,
    eval_batch_size: int | None = None,
    num_classes: int | None = None,
) -> dict:
    print(f"\n{'='*60}")
    print(f"Adapter TTT Eval")
    print(f"  checkpoint: {checkpoint_path}")
    print(f"  calib_samples: {num_calib_samples}")
    print(f"  ttt_steps: {num_ttt_steps}")
    print(f"  adapter_hidden: {adapter_hidden_dim}")
    print(f"  mlp_digital: {apply_mlp_digital}")
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
        
        if apply_mlp_digital:
            for name, module in model.named_modules():
                if ".mlp.fc" in name and hasattr(module, 'config'):
                    module.config.noise_enabled = False
                    module.config.sigma_c2c = 0.0
                    module.config.sigma_d2d = 0.0
        
        resampled = resample_all_d2d_noise(model)
        
        adapter = inject_adapter_before_head(model, hidden_dim=adapter_hidden_dim, dropout=adapter_dropout)
        adapter = adapter.to(device)
        
        trainset = trainloader.dataset
        calib_subset = torch.utils.data.Subset(trainset, range(num_calib_samples))
        calib_loader = torch.utils.data.DataLoader(calib_subset, batch_size=32, shuffle=True)
        
        ttt_finetune_adapter(
            model, adapter, calib_loader, device,
            num_steps=num_ttt_steps, lr=ttt_lr, weight_decay=ttt_weight_decay,
        )
        
        losses = []
        accs = []
        for _ in range(eval_runs):
            loss, acc = evaluate(model, testloader, criterion, device, cfg, amp_enabled=False)
            losses.append(float(loss))
            accs.append(float(acc))
        
        remove_adapter_from_head(model)
        
        mean_acc = mean(accs)
        print(
            f"  instance {instance_idx + 1:02d}/{fresh_instances}: "
            f"mean_acc={mean_acc:.2f}% eval_runs={eval_runs} resampled={resampled}",
            flush=True,
        )
        instance_means.append(mean_acc)
        instance_rows.append(
            {
                "instance_index": instance_idx,
                "seed": seed,
                "resampled_modules": resampled,
                "eval_runs": eval_runs,
                "calib_samples": num_calib_samples,
                "ttt_steps": num_ttt_steps,
                "adapter_hidden_dim": adapter_hidden_dim,
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
        "num_ttt_steps": num_ttt_steps,
        "adapter_hidden_dim": adapter_hidden_dim,
        "ttt_lr": ttt_lr,
        "ttt_weight_decay": ttt_weight_decay,
        "apply_mlp_digital": apply_mlp_digital,
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
    parser.add_argument("--num-ttt-steps", type=int, default=50)
    parser.add_argument("--adapter-hidden-dim", type=int, default=None)
    parser.add_argument("--adapter-dropout", type=float, default=0.1)
    parser.add_argument("--ttt-lr", type=float, default=1e-3)
    parser.add_argument("--ttt-weight-decay", type=float, default=0.01)
    parser.add_argument("--apply-mlp-digital", action="store_true")
    parser.add_argument("--dataset", default=None)
    parser.add_argument("--num-classes", type=int, default=None)
    parser.add_argument("--eval-batch-size", type=int, default=None)
    parser.add_argument("--json-out", default="report_md/_gpt/json_gpt/adapter_ttt_eval.json")
    args = parser.parse_args()
    
    result = evaluate_with_adapter_ttt(
        checkpoint_path=args.checkpoint,
        device=args.device,
        fresh_instances=args.fresh_instances,
        eval_runs=args.eval_runs,
        data_root=args.data_root,
        num_workers=args.num_workers,
        num_calib_samples=args.num_calib_samples,
        num_ttt_steps=args.num_ttt_steps,
        adapter_hidden_dim=args.adapter_hidden_dim,
        adapter_dropout=args.adapter_dropout,
        ttt_lr=args.ttt_lr,
        ttt_weight_decay=args.ttt_weight_decay,
        apply_mlp_digital=args.apply_mlp_digital,
        dataset=args.dataset,
        eval_batch_size=args.eval_batch_size,
        num_classes=args.num_classes,
    )
    
    out_path = Path(args.json_out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"JSON saved to: {out_path}")


if __name__ == "__main__":
    main()
