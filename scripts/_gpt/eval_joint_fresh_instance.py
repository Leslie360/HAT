#!/usr/bin/env python3
"""Fresh-instance evaluation for joint MLP-linear + Ensemble HAT checkpoint.

Loads the groupwise NL setter so MLP blocks are protected during eval,
matching the training regime.
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

from run_tinyvit_groupwise_nl_comp import build_selector, make_groupwise_setter
import train_tinyvit_ensemble as base
from train_tinyvit_ensemble import (
    RunLogger,
    TinyViTExperimentConfig,
    build_model,
    evaluate,
    get_dataloaders,
    resample_all_d2d_noise,
)
from train_tinyvit import set_seed


def evaluate_fresh_instances_groupwise(
    checkpoint_path: str,
    device: str,
    fresh_instances: int,
    eval_runs: int,
    data_root: str,
    num_workers: int,
    dataset: str | None = None,
    eval_batch_size: int | None = None,
    num_classes: int | None = None,
    protected_group: str = "mlp",
    protected_nl_ltp: float = 1.0,
    protected_nl_ltd: float = -1.0,
    use_second_order_ste: bool = False,
    delta_g_eff: float = 0.0,
    second_order_alpha: float = 1.0,
) -> dict:
    print(f"\nEvaluating fresh-instance transfer for: {checkpoint_path}", flush=True)

    # Load groupwise setter
    selector = build_selector(protected_group)
    base.set_noise_for_eval = make_groupwise_setter(
        selector=selector,
        protected_nl_ltp=protected_nl_ltp,
        protected_nl_ltd=protected_nl_ltd,
        train_mode=False,
        use_second_order_ste=use_second_order_ste,
        delta_g_eff=delta_g_eff,
        second_order_alpha=second_order_alpha,
    )

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

    _, testloader = get_dataloaders(
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
        resampled = resample_all_d2d_noise(model)
        base.set_noise_for_eval(model, cfg)

        losses = []
        accs = []
        for _ in range(eval_runs):
            loss, acc = evaluate(model, testloader, criterion, device, cfg, amp_enabled=False)
            losses.append(float(loss))
            accs.append(float(acc))

        mean_acc = mean(accs)
        print(
            f"  instance {instance_idx + 1:02d}/{fresh_instances}: "
            f"mean_acc={mean_acc:.2f}% eval_runs={eval_runs}",
            flush=True,
        )
        instance_means.append(mean_acc)
        instance_rows.append(
            {
                "instance_index": instance_idx,
                "seed": seed,
                "resampled_modules": resampled,
                "eval_runs": eval_runs,
                "test_loss_mean": mean(losses),
                "test_acc_mean": mean_acc,
                "test_acc_std": stdev(accs) if len(accs) > 1 else 0.0,
                "test_acc_raw": accs,
            }
        )

    result = {
        "checkpoint_path": checkpoint_path,
        "train_best_acc": float(ckpt.get("best_acc", float("nan"))),
        "train_best_epoch": int(ckpt.get("best_epoch", ckpt.get("epoch", -1))),
        "fresh_instances": fresh_instances,
        "mc_runs_per_instance": eval_runs,
        "dataset": resolved_dataset,
        "num_classes": resolved_num_classes,
        "eval_batch_size": resolved_batch_size,
        "cross_instance_mean": mean(instance_means),
        "cross_instance_std": stdev(instance_means) if len(instance_means) > 1 else 0.0,
        "instance_means": instance_means,
        "instances": instance_rows,
    }
    print(
        f"Completed: {result['cross_instance_mean']:.2f}% +/- {result['cross_instance_std']:.2f}% "
        f"across {fresh_instances} fresh instances",
        flush=True,
    )
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--fresh-instances", type=int, default=10)
    parser.add_argument("--eval-runs", type=int, default=5)
    parser.add_argument("--data-root", default="./data")
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--dataset", default=None, help="Override dataset name; default: read from checkpoint")
    parser.add_argument("--num-classes", type=int, default=None, help="Override class count; default: read from checkpoint/head shape")
    parser.add_argument("--eval-batch-size", type=int, default=None, help="Override eval batch size; default: 256")
    parser.add_argument("--protected-group", default="mlp")
    parser.add_argument("--protected-nl-ltp", type=float, default=1.0)
    parser.add_argument("--protected-nl-ltd", type=float, default=-1.0)
    parser.add_argument("--use-second-order-ste", action="store_true")
    parser.add_argument("--delta-g-eff", type=float, default=-1.0,
                        help="Effective perturbation scale for curvature correction (negative=auto, 0=literal zero)")
    parser.add_argument("--second-order-alpha", type=float, default=1.0)
    parser.add_argument("--json-out", default="report_md/_gpt/json_gpt/joint_fresh_eval.json")
    args = parser.parse_args()

    result = evaluate_fresh_instances_groupwise(
        checkpoint_path=args.checkpoint,
        device=args.device,
        fresh_instances=args.fresh_instances,
        eval_runs=args.eval_runs,
        data_root=args.data_root,
        num_workers=args.num_workers,
        dataset=args.dataset,
        eval_batch_size=args.eval_batch_size,
        num_classes=args.num_classes,
        protected_group=args.protected_group,
        protected_nl_ltp=args.protected_nl_ltp,
        protected_nl_ltd=args.protected_nl_ltd,
        use_second_order_ste=args.use_second_order_ste,
        delta_g_eff=args.delta_g_eff,
        second_order_alpha=args.second_order_alpha,
    )

    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.json_out, "w") as f:
        json.dump(result, f, indent=2)
    print(f"JSON saved to: {args.json_out}")


if __name__ == "__main__":
    main()
