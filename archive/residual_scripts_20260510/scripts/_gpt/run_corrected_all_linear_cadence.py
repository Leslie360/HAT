#!/usr/bin/env python3
"""Corrected local runner for uniform all-linear cadence experiments.

This is the local mainline runner after the parity re-anchor:
  - `group=all`
  - protected NL = (1.0, -1.0) for every analog layer
  - severe global NL still recorded in `exp_cfg` for parity/debug context
  - intra-epoch D2D resampling cadence is the main search axis
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import torch
import torch.nn as nn
import torch.optim as optim

from amp_utils import amp_enabled_for_device
import train_tinyvit_ensemble as base
from run_tinyvit_groupwise_nl_comp import build_selector, make_groupwise_setter
from scripts._gpt.eval_joint_fresh_instance import evaluate_fresh_instances_groupwise
from train_tinyvit_ensemble import (
    RunLogger,
    TinyViTExperimentConfig,
    build_training_checkpoint_payload,
    evaluate,
    get_dataloaders,
    get_v_experiment_configs,
    maybe_resume_experiment,
    resample_all_d2d_noise,
)


DEFAULT_SAVE_DIR = "checkpoints/_gpt/all_linear_cadence"
DEFAULT_JSON_DIR = "report_md/_gpt/json_gpt"
DEFAULT_MD_DIR = "report_md/_gpt"
DEFAULT_LOG_DIR = "logs/_gpt"


def build_run_name(resample_interval: int, epochs: int) -> str:
    return f"V4_hybrid_standard_noise_hat_all_linear_r{resample_interval}_{epochs}ep"


def build_output_paths(run_name: str, args) -> Tuple[str, str, str]:
    json_path = args.json_path or str(Path(DEFAULT_JSON_DIR) / f"{run_name}.json")
    md_path = args.md_path or str(Path(DEFAULT_MD_DIR) / f"{run_name}.md")
    log_path = args.log_path or str(Path(DEFAULT_LOG_DIR) / f"{run_name}.log")
    return json_path, md_path, log_path


def train_one_epoch_with_interval(
    model,
    trainloader,
    optimizer,
    criterion,
    device: str,
    exp_cfg: TinyViTExperimentConfig,
    resample_interval: int,
    amp_enabled: bool = False,
    scaler=None,
) -> Tuple[float, float, int]:
    model.train()
    base.set_noise_for_train(model, exp_cfg)
    running_loss = 0.0
    correct = 0
    total = 0
    resample_count = 0

    for batch_idx, (inputs, targets) in enumerate(trainloader):
        if exp_cfg.hat_training and resample_interval > 0 and batch_idx % resample_interval == 0:
            resample_count += resample_all_d2d_noise(model)

        inputs, targets = inputs.to(device), targets.to(device)
        optimizer.zero_grad(set_to_none=True)
        with base.autocast_context(device, amp_enabled):
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


def build_markdown(summary: Dict[str, object]) -> str:
    train = summary["train"]
    fresh = summary.get("fresh")
    lines = [
        f"# {summary['run_name']}",
        "",
        f"- Generated: `{summary['generated_at']}`",
        f"- Checkpoint: `{summary['checkpoint_path']}`",
        f"- Resample interval: `{summary['resample_interval']}` batches",
        f"- Epochs: `{summary['epochs']}`",
        "",
        "## Train",
        "",
        f"- best source acc: `{train['best_acc']:.2f}%`",
        f"- best epoch: `{train['best_epoch']}`",
        f"- final source acc: `{train['final_test_acc']:.2f}%`",
        "",
    ]
    if fresh is not None:
        lines.extend(
            [
                "## Fresh",
                "",
                f"- mean: `{fresh['cross_instance_mean']:.2f}%`",
                f"- std: `{fresh['cross_instance_std']:.2f}%`",
                f"- peak instance: `{max(fresh['instance_means']):.2f}%`",
                "",
            ]
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resample-interval", type=int, required=True)
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--data-root", default="./data")
    parser.add_argument("--save-dir", default=DEFAULT_SAVE_DIR)
    parser.add_argument("--json-path", default=None)
    parser.add_argument("--md-path", default=None)
    parser.add_argument("--log-path", default=None)
    parser.add_argument("--warm-start-from", default="checkpoints/V4_hybrid_standard_noise_hat_best.pt")
    parser.add_argument("--lr", type=float, default=5e-4)
    parser.add_argument("--weight-decay", type=float, default=0.05)
    parser.add_argument("--dataset", default="cifar10")
    parser.add_argument("--eval-batch-size", type=int, default=256)
    parser.add_argument("--fresh-instances", type=int, default=5)
    parser.add_argument("--eval-runs", type=int, default=3)
    parser.add_argument("--amp", action="store_true")
    parser.add_argument("--log-interval", type=int, default=10)
    parser.add_argument("--protected-group", default="all")
    parser.add_argument("--protected-nl-ltp", type=float, default=1.0)
    parser.add_argument("--protected-nl-ltd", type=float, default=-1.0)
    parser.add_argument("--nl-ltp", type=float, default=2.0)
    parser.add_argument("--nl-ltd", type=float, default=-2.0)
    so2_group = parser.add_mutually_exclusive_group()
    so2_group.add_argument("--use-second-order-ste", dest="use_second_order_ste", action="store_true")
    so2_group.add_argument("--no-use-second-order-ste", dest="use_second_order_ste", action="store_false")
    parser.set_defaults(use_second_order_ste=False)
    parser.add_argument("--delta-g-eff", type=float, default=-1.0)
    parser.add_argument("--second-order-alpha", type=float, default=1.0)
    parser.add_argument("--skip-fresh-eval", action="store_true")
    parser.add_argument("--resume-existing", action="store_true")
    args = parser.parse_args()

    run_name = build_run_name(args.resample_interval, args.epochs)
    json_path, md_path, log_path = build_output_paths(run_name, args)

    selector = build_selector(args.protected_group)
    base.set_noise_for_train = make_groupwise_setter(
        selector=selector,
        protected_nl_ltp=args.protected_nl_ltp,
        protected_nl_ltd=args.protected_nl_ltd,
        train_mode=True,
        use_second_order_ste=args.use_second_order_ste,
        delta_g_eff=args.delta_g_eff,
        second_order_alpha=args.second_order_alpha,
    )
    base.set_noise_for_eval = make_groupwise_setter(
        selector=selector,
        protected_nl_ltp=args.protected_nl_ltp,
        protected_nl_ltd=args.protected_nl_ltd,
        train_mode=False,
        use_second_order_ste=args.use_second_order_ste,
        delta_g_eff=args.delta_g_eff,
        second_order_alpha=args.second_order_alpha,
    )

    exp_cfg = get_v_experiment_configs(epochs=args.epochs, batch_size=args.batch_size)["V4"]
    exp_cfg.name = run_name
    exp_cfg.lr = args.lr
    exp_cfg.weight_decay = args.weight_decay
    exp_cfg.nl_ltp = args.nl_ltp
    exp_cfg.nl_ltd = args.nl_ltd

    logger = RunLogger(log_path)
    logger.log("=" * 72)
    logger.log("Corrected all-linear cadence runner")
    logger.log(
        f"run_name={run_name} interval={args.resample_interval} epochs={args.epochs} "
        f"batch_size={args.batch_size} warm_start={args.warm_start_from}"
    )
    logger.log(
        f"protected_group={args.protected_group} protected_nl=({args.protected_nl_ltp}, {args.protected_nl_ltd}) "
        f"global_nl=({args.nl_ltp}, {args.nl_ltd}) so2={args.use_second_order_ste} "
        f"delta_g_eff={args.delta_g_eff} alpha={args.second_order_alpha}"
    )
    logger.log("=" * 72)

    model = base.build_model(exp_cfg, num_classes=10, device=args.device, pretrained=False)
    trainloader, testloader = get_dataloaders(
        dataset=args.dataset,
        batch_size=exp_cfg.batch_size,
        data_root=args.data_root,
        num_workers=args.num_workers,
    )
    optimizer = optim.AdamW(model.parameters(), lr=exp_cfg.lr, weight_decay=exp_cfg.weight_decay)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=exp_cfg.epochs)
    criterion = nn.CrossEntropyLoss()
    scaler = base.create_grad_scaler(args.device, args.amp)
    active_amp = amp_enabled_for_device(args.amp, args.device)

    start_epoch, best_acc, best_epoch, best_path, last_path, history, resumed = maybe_resume_experiment(
        model=model,
        optimizer=optimizer,
        scheduler=scheduler,
        scaler=scaler,
        exp_cfg=exp_cfg,
        save_dir=args.save_dir,
        device=args.device,
        dataset=args.dataset,
        num_classes=10,
        resume_existing=args.resume_existing,
        warm_start_from=args.warm_start_from,
        logger=logger,
    )
    if resumed:
        logger.log(f"weights loaded from {resumed}")

    for epoch in range(start_epoch, exp_cfg.epochs):
        train_loss, train_acc, resampled = train_one_epoch_with_interval(
            model=model,
            trainloader=trainloader,
            optimizer=optimizer,
            criterion=criterion,
            device=args.device,
            exp_cfg=exp_cfg,
            resample_interval=args.resample_interval,
            amp_enabled=active_amp,
            scaler=scaler,
        )
        test_loss, test_acc = evaluate(
            model=model,
            testloader=testloader,
            criterion=criterion,
            device=args.device,
            exp_cfg=exp_cfg,
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

        if epoch == 0 or epoch == exp_cfg.epochs - 1 or (epoch + 1) % max(1, args.log_interval) == 0:
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
            exp_cfg=exp_cfg,
            dataset=args.dataset,
            num_classes=10,
            epoch=epoch,
            best_acc=best_acc,
            best_epoch=best_epoch,
            history=history,
            amp_enabled=active_amp,
        )
        os.makedirs(args.save_dir, exist_ok=True)
        torch.save(payload, last_path)
        if improved:
            torch.save(payload, best_path)
        scheduler.step()

    fresh = None
    if not args.skip_fresh_eval:
        fresh = evaluate_fresh_instances_groupwise(
            checkpoint_path=best_path,
            device=args.device,
            fresh_instances=args.fresh_instances,
            eval_runs=args.eval_runs,
            data_root=args.data_root,
            num_workers=args.num_workers,
            dataset=args.dataset,
            eval_batch_size=args.eval_batch_size,
            num_classes=10,
            protected_group=args.protected_group,
            protected_nl_ltp=args.protected_nl_ltp,
            protected_nl_ltd=args.protected_nl_ltd,
            use_second_order_ste=args.use_second_order_ste,
            delta_g_eff=args.delta_g_eff,
            second_order_alpha=args.second_order_alpha,
        )

    summary = {
        "generated_at": datetime.now().isoformat(),
        "run_name": run_name,
        "checkpoint_path": best_path,
        "resample_interval": args.resample_interval,
        "epochs": args.epochs,
        "train": {
            "best_acc": best_acc,
            "best_epoch": best_epoch,
            "final_test_acc": history["test_acc"][-1],
            "final_train_acc": history["train_acc"][-1],
        },
        "fresh": fresh,
        "config": {
            "batch_size": args.batch_size,
            "num_workers": args.num_workers,
            "warm_start_from": args.warm_start_from,
            "protected_group": args.protected_group,
            "protected_nl_ltp": args.protected_nl_ltp,
            "protected_nl_ltd": args.protected_nl_ltd,
            "nl_ltp": args.nl_ltp,
            "nl_ltd": args.nl_ltd,
            "use_second_order_ste": args.use_second_order_ste,
            "delta_g_eff": args.delta_g_eff,
            "second_order_alpha": args.second_order_alpha,
            "fresh_instances": args.fresh_instances,
            "eval_runs": args.eval_runs,
        },
    }

    Path(json_path).parent.mkdir(parents=True, exist_ok=True)
    Path(json_path).write_text(json.dumps(summary, indent=2), encoding="utf-8")
    Path(md_path).parent.mkdir(parents=True, exist_ok=True)
    Path(md_path).write_text(build_markdown(summary), encoding="utf-8")
    logger.log(f"summary_json={json_path}")
    logger.log(f"summary_md={md_path}")
    logger.close()


if __name__ == "__main__":
    main()
