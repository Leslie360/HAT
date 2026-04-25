#!/usr/bin/env python3
"""Train a per-batch D2D-resampling control and compare fresh-instance transfer.

This runner closes the reviewer-facing mechanism gap around Ensemble HAT by
keeping the paper-locked checkpoints for:
  - fixed-mask HAT (`checkpoints/V4_hybrid_standard_noise_hat_best.pt`)
  - per-epoch Ensemble HAT (`checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt`)

and training only the missing per-batch resampling control under the same V4
recipe. All three checkpoints are then evaluated with the same fresh-instance
protocol: 10 freshly sampled D2D instances, 5 Monte Carlo evaluations per
instance.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
from datetime import datetime
from pathlib import Path
from statistics import mean, stdev
from typing import Dict, List, Tuple

import torch
import torch.nn as nn
import torch.optim as optim

from amp_utils import amp_enabled_for_device, autocast_context, create_grad_scaler
from repo_bootstrap import ensure_repo_root
from train_tinyvit import set_seed
from train_tinyvit_ensemble import (
    RunLogger,
    TinyViTExperimentConfig,
    build_model,
    build_training_checkpoint_payload,
    evaluate,
    get_dataloaders,
    get_v_experiment_configs,
    resample_all_d2d_noise,
    set_noise_for_train,
)

ensure_repo_root()


DEFAULT_BATCH_CKPT_DIR = "checkpoints/_cadence_control"
DEFAULT_JSON_PATH = "report_md/_gpt/json_gpt/fresh_instance_cadence_control.json"
DEFAULT_MD_PATH = "report_md/_gpt/fresh_instance_cadence_control.md"
DEFAULT_LOG_PATH = "logs/_gpt/fresh_instance_cadence_control.log"

FIXED_CKPT = "checkpoints/V4_hybrid_standard_noise_hat_best.pt"
ENSEMBLE_CKPT = "checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt"


def train_one_epoch_with_cadence(
    model: nn.Module,
    trainloader,
    optimizer,
    criterion,
    device: str,
    exp_cfg: TinyViTExperimentConfig,
    cadence: str,
    amp_enabled: bool = False,
    scaler=None,
) -> Tuple[float, float, int]:
    model.train()
    set_noise_for_train(model, exp_cfg)
    running_loss = 0.0
    correct = 0
    total = 0
    resample_count = 0

    for inputs, targets in trainloader:
        if cadence == "batch" and exp_cfg.hat_training:
            resample_count += resample_all_d2d_noise(model)

        inputs, targets = inputs.to(device), targets.to(device)
        optimizer.zero_grad(set_to_none=True)

        with autocast_context(device, amp_enabled):
            outputs = model(inputs)
            loss = criterion(outputs, targets)

        if scaler is not None and scaler.is_enabled():
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            loss.backward()
            optimizer.step()

        running_loss += loss.item() * inputs.size(0)
        _, predicted = outputs.max(1)
        correct += predicted.eq(targets).sum().item()
        total += targets.size(0)

    return running_loss / total, 100.0 * correct / total, resample_count


def cfg_from_checkpoint(checkpoint_path: str) -> TinyViTExperimentConfig:
    ckpt = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    exp_cfg_dict = ckpt.get("exp_cfg", {})
    valid_keys = {f.name for f in dataclasses.fields(TinyViTExperimentConfig)}
    filtered = {k: v for k, v in exp_cfg_dict.items() if k in valid_keys}
    return TinyViTExperimentConfig(**filtered)


def checkpoint_name_for_cadence(cadence: str) -> str:
    return f"V4_hybrid_standard_noise_hat_{cadence}_control"


def train_batch_control(args) -> str:
    device = args.device
    save_dir = Path(args.save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    base_cfg = get_v_experiment_configs(epochs=args.epochs, batch_size=args.batch_size)["V4"]
    base_cfg.name = checkpoint_name_for_cadence("batch")
    base_cfg.lr = args.lr
    base_cfg.weight_decay = args.weight_decay

    best_path = save_dir / f"{base_cfg.name}_best.pt"
    last_path = save_dir / f"{base_cfg.name}_last.pt"

    if args.resume and best_path.exists():
        return str(best_path)

    model = build_model(base_cfg, num_classes=10, device=device, pretrained=False)
    trainloader, testloader = get_dataloaders(
        dataset="cifar10",
        batch_size=base_cfg.batch_size,
        data_root=args.data_root,
        num_workers=args.num_workers,
    )
    optimizer = optim.AdamW(model.parameters(), lr=base_cfg.lr, weight_decay=base_cfg.weight_decay)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=base_cfg.epochs)
    criterion = nn.CrossEntropyLoss()
    scaler = create_grad_scaler(device, args.amp)
    active_amp = amp_enabled_for_device(args.amp, device)

    history = {"train_loss": [], "train_acc": [], "test_loss": [], "test_acc": [], "lr": []}
    best_acc = 0.0
    best_epoch = -1

    logger = RunLogger(args.log_path)
    logger.log("=" * 72)
    logger.log("Per-batch D2D resampling control training")
    logger.log(f"checkpoint_name={base_cfg.name}")
    logger.log(f"epochs={base_cfg.epochs}, batch_size={base_cfg.batch_size}, lr={base_cfg.lr}")
    logger.log(f"amp={'on' if active_amp else 'off'}, num_workers={args.num_workers}")
    logger.log("=" * 72)

    for epoch in range(base_cfg.epochs):
        train_loss, train_acc, resampled = train_one_epoch_with_cadence(
            model=model,
            trainloader=trainloader,
            optimizer=optimizer,
            criterion=criterion,
            device=device,
            exp_cfg=base_cfg,
            cadence="batch",
            amp_enabled=active_amp,
            scaler=scaler,
        )
        test_loss, test_acc = evaluate(
            model=model,
            testloader=testloader,
            criterion=criterion,
            device=device,
            exp_cfg=base_cfg,
            amp_enabled=active_amp,
        )

        current_lr = optimizer.param_groups[0]["lr"]
        history["train_loss"].append(train_loss)
        history["train_acc"].append(train_acc)
        history["test_loss"].append(test_loss)
        history["test_acc"].append(test_acc)
        history["lr"].append(current_lr)

        improved = test_acc > best_acc
        if improved:
            best_acc = test_acc
            best_epoch = epoch

        logger.log(
            f"epoch={epoch:03d} train_loss={train_loss:.4f} train_acc={train_acc:.2f}% "
            f"test_acc={test_acc:.2f}% best={best_acc:.2f}% lr={current_lr:.6f} "
            f"resampled_modules={resampled}"
        )

        payload = build_training_checkpoint_payload(
            model=model,
            optimizer=optimizer,
            scheduler=scheduler,
            scaler=scaler,
            exp_cfg=base_cfg,
            dataset="cifar10",
            num_classes=10,
            epoch=epoch,
            best_acc=best_acc,
            best_epoch=best_epoch,
            history=history,
            amp_enabled=active_amp,
        )
        torch.save(payload, last_path)
        if improved:
            torch.save(payload, best_path)
        scheduler.step()

    logger.log(f"finished best_acc={best_acc:.2f}% best_epoch={best_epoch} best_path={best_path}")
    logger.close()
    return str(best_path)


def evaluate_fresh_instances(
    checkpoint_path: str,
    device: str,
    fresh_instances: int,
    eval_runs: int,
    data_root: str,
    num_workers: int,
) -> Dict[str, object]:
    print(f"\nEvaluating fresh-instance transfer for: {checkpoint_path}", flush=True)
    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    exp_cfg_dict = ckpt.get("exp_cfg", {})
    valid_keys = {f.name for f in dataclasses.fields(TinyViTExperimentConfig)}
    filtered = {k: v for k, v in exp_cfg_dict.items() if k in valid_keys}
    cfg = TinyViTExperimentConfig(**filtered)

    _, testloader = get_dataloaders(
        dataset="cifar10",
        batch_size=256,
        data_root=data_root,
        num_workers=num_workers,
    )
    criterion = nn.CrossEntropyLoss()

    instance_means: List[float] = []
    instance_rows: List[dict] = []

    for instance_idx in range(fresh_instances):
        seed = 42 + instance_idx * 100
        set_seed(seed)
        model = build_model(cfg, num_classes=10, device=device, pretrained=False)
        model.load_state_dict(ckpt["model_state_dict"], strict=True)
        resampled = resample_all_d2d_noise(model)

        losses: List[float] = []
        accs: List[float] = []
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
        "cross_instance_mean": mean(instance_means),
        "cross_instance_std": stdev(instance_means) if len(instance_means) > 1 else 0.0,
        "instance_means": instance_means,
        "instances": instance_rows,
    }
    print(
        f"Completed {checkpoint_path}: "
        f"{result['cross_instance_mean']:.2f}% +/- {result['cross_instance_std']:.2f}% "
        f"across {fresh_instances} fresh instances",
        flush=True,
    )
    return result


def build_markdown(summary: Dict[str, object]) -> str:
    lines = [
        "# Fresh-Instance Cadence Control",
        "",
        f"- Generated: `{summary['generated_at']}`",
        f"- Protocol: `{summary['protocol']}`",
        "",
        "| Training mode | Train best acc (%) | Fresh-instance mean (%) | Cross-instance std (%) |",
        "|:--|--:|--:|--:|",
    ]
    for key in ["fixed", "epoch", "batch"]:
        row = summary["results"][key]
        lines.append(
            f"| {key} | {row['train_best_acc']:.2f} | {row['cross_instance_mean']:.2f} | {row['cross_instance_std']:.2f} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `fixed` measures the paper-locked standard HAT checkpoint under fresh D2D instances.",
            "- `epoch` measures the paper-locked Ensemble HAT checkpoint under the same protocol.",
            "- `batch` is the new per-batch resampling control trained under the same V4 recipe and evaluated under the same fresh-instance protocol.",
            "",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--data-root", default="./data")
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--lr", type=float, default=5e-4)
    parser.add_argument("--weight-decay", type=float, default=0.05)
    parser.add_argument("--fresh-instances", type=int, default=10)
    parser.add_argument("--eval-runs", type=int, default=5)
    parser.add_argument("--save-dir", default=DEFAULT_BATCH_CKPT_DIR)
    parser.add_argument("--json-path", default=DEFAULT_JSON_PATH)
    parser.add_argument("--md-path", default=DEFAULT_MD_PATH)
    parser.add_argument("--log-path", default=DEFAULT_LOG_PATH)
    parser.add_argument("--amp", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--skip-train", action="store_true")
    args = parser.parse_args()

    batch_ckpt = str(Path(args.save_dir) / f"{checkpoint_name_for_cadence('batch')}_best.pt")
    if not args.skip_train:
        batch_ckpt = train_batch_control(args)
    elif not Path(batch_ckpt).exists():
        raise FileNotFoundError(f"--skip-train set but checkpoint missing: {batch_ckpt}")

    results = {
        "fixed": evaluate_fresh_instances(
            checkpoint_path=FIXED_CKPT,
            device=args.device,
            fresh_instances=args.fresh_instances,
            eval_runs=args.eval_runs,
            data_root=args.data_root,
            num_workers=args.num_workers,
        ),
        "epoch": evaluate_fresh_instances(
            checkpoint_path=ENSEMBLE_CKPT,
            device=args.device,
            fresh_instances=args.fresh_instances,
            eval_runs=args.eval_runs,
            data_root=args.data_root,
            num_workers=args.num_workers,
        ),
        "batch": evaluate_fresh_instances(
            checkpoint_path=batch_ckpt,
            device=args.device,
            fresh_instances=args.fresh_instances,
            eval_runs=args.eval_runs,
            data_root=args.data_root,
            num_workers=args.num_workers,
        ),
    }

    summary = {
        "generated_at": datetime.now().isoformat(),
        "protocol": (
            f"{args.fresh_instances} fresh D2D instances x {args.eval_runs} MC evaluations "
            f"per instance on CIFAR-10 Tiny-ViT V4 checkpoints"
        ),
        "results": results,
    }

    json_path = Path(args.json_path)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    md_path = Path(args.md_path)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(build_markdown(summary), encoding="utf-8")

    print(json.dumps(
        {
            "fixed_mean": results["fixed"]["cross_instance_mean"],
            "epoch_mean": results["epoch"]["cross_instance_mean"],
            "batch_mean": results["batch"]["cross_instance_mean"],
            "batch_checkpoint": batch_ckpt,
            "json_path": str(json_path),
        },
        indent=2,
    ))


if __name__ == "__main__":
    main()
