#!/usr/bin/env python3
"""Fresh-instance evaluation with SELECTIVE resampling scope.

Validates which layer groups are most responsible for fresh-instance collapse.
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
)
from train_tinyvit import set_seed


def resample_d2d_selective(model: nn.Module, scope: str) -> int:
    """Resample D2D noise only for modules matching scope.

    scope options:
      - 'all': all analog modules (same as resample_all_d2d_noise)
      - 'mlp': modules with '.mlp.fc1' or '.mlp.fc2' in name
      - 'qkv': modules with '.attn.qkv' in name
      - 'attn_proj': modules with '.attn.proj' in name
      - 'patch_embed': modules starting with 'patch_embed.' and containing '.conv'
      - 'none': no resampling (baseline)
    """
    if scope == "all":
        count = 0
        for m in model.modules():
            if hasattr(m, "resample_d2d_noise") and callable(m.resample_d2d_noise):
                m.resample_d2d_noise()
                count += 1
        return count

    if scope == "none":
        return 0

    selector = build_selector(scope)
    count = 0
    for name, m in model.named_modules():
        if hasattr(m, "resample_d2d_noise") and callable(m.resample_d2d_noise):
            if selector(name):
                m.resample_d2d_noise()
                count += 1
    return count


def evaluate_fresh_instances_selective(
    checkpoint_path: str,
    device: str,
    fresh_instances: int,
    eval_runs: int,
    data_root: str,
    num_workers: int,
    resample_scope: str = "all",
    dataset: str | None = None,
    eval_batch_size: int | None = None,
    num_classes: int | None = None,
    protected_group: str = "all",
    protected_nl_ltp: float = 1.0,
    protected_nl_ltd: float = -1.0,
) -> dict:
    print(f"\nFresh eval: selective resample_scope='{resample_scope}'")
    print(f"Checkpoint: {checkpoint_path}", flush=True)

    selector = build_selector(protected_group)
    base.set_noise_for_eval = make_groupwise_setter(
        selector=selector,
        protected_nl_ltp=protected_nl_ltp,
        protected_nl_ltd=protected_nl_ltd,
        train_mode=False,
        use_second_order_ste=False,
        delta_g_eff=0.0,
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
        resampled = resample_d2d_selective(model, resample_scope)
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
            f"mean_acc={mean_acc:.2f}% eval_runs={eval_runs} resampled_modules={resampled}",
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
        f"Completed scope='{resample_scope}': {result['cross_instance_mean']:.2f}% +/- "
        f"{result['cross_instance_std']:.2f}% across {fresh_instances} fresh instances",
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
    parser.add_argument(
        "--resample-scope",
        choices=["all", "none", "mlp", "qkv", "attn_proj", "patch_embed"],
        default="all",
        help="Which layer group to resample D2D noise for",
    )
    parser.add_argument("--dataset", default=None)
    parser.add_argument("--num-classes", type=int, default=None)
    parser.add_argument("--eval-batch-size", type=int, default=None)
    parser.add_argument("--protected-group", default="all")
    parser.add_argument("--protected-nl-ltp", type=float, default=1.0)
    parser.add_argument("--protected-nl-ltd", type=float, default=-1.0)
    parser.add_argument("--json-out", default="report_md/_gpt/json_gpt/selective_fresh_eval.json")
    args = parser.parse_args()

    result = evaluate_fresh_instances_selective(
        checkpoint_path=args.checkpoint,
        device=args.device,
        fresh_instances=args.fresh_instances,
        eval_runs=args.eval_runs,
        data_root=args.data_root,
        num_workers=args.num_workers,
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
