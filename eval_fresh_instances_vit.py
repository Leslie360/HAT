#!/usr/bin/env python3
"""Fresh-instance evaluator for ViT-Small / DeiT-Small TinyImageNet checkpoints."""
import argparse
import json
import subprocess
import torch
import numpy as np
from pathlib import Path

from train_vit_tinyimagenet import (
    ViTTinyImageNetConfig,
    build_model,
    get_dataloaders,
    evaluate,
    set_noise_for_eval,
)
from analog_layers import resample_d2d_buffers
from amp_utils import amp_enabled_for_device


def load_checkpoint_provenance(checkpoint_path):
    ckpt = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    exp_cfg = ckpt.get("exp_cfg") or {}
    return {
        "checkpoint_epoch": ckpt.get("epoch"),
        "checkpoint_best_epoch": ckpt.get("best_epoch"),
        "checkpoint_best_acc": ckpt.get("best_acc"),
        "checkpoint_seed": ckpt.get("seed"),
        "checkpoint_nl_ltp": exp_cfg.get("nl_ltp"),
        "checkpoint_nl_ltd": exp_cfg.get("nl_ltd"),
        "checkpoint_noise_mode": exp_cfg.get("noise_mode"),
        "checkpoint_experiment_name": exp_cfg.get("name"),
        "checkpoint_arch": exp_cfg.get("arch"),
        "checkpoint_hat_type": exp_cfg.get("hat_type"),
        "amp_enabled": ckpt.get("amp_enabled", False),
    }


def runtime_metadata():
    try:
        commit_hash = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        commit_hash = None
    try:
        dirty = bool(subprocess.check_output(
            ["git", "status", "--porcelain"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip())
    except Exception:
        dirty = None

    cuda_device_name = None
    if torch.cuda.is_available():
        try:
            cuda_device_name = torch.cuda.get_device_name(0)
        except Exception:
            cuda_device_name = None

    return {
        "commit_hash": commit_hash,
        "git_worktree_dirty": dirty,
        "cuda_device_name": cuda_device_name,
        "pytorch_version": torch.__version__,
    }


def _float_matches(left, right, tol=1e-9):
    return left is None or right is None or abs(float(left) - float(right)) <= tol


def resolve_eval_overrides(provenance, nl_ltp=None, nl_ltd=None, noise_mode=None,
                           allow_eval_nl_override=False):
    ckpt_ltp = provenance.get("checkpoint_nl_ltp")
    ckpt_ltd = provenance.get("checkpoint_nl_ltd")
    ckpt_noise = provenance.get("checkpoint_noise_mode")

    resolved_ltp = ckpt_ltp if nl_ltp is None else nl_ltp
    resolved_ltd = ckpt_ltd if nl_ltd is None else nl_ltd
    resolved_noise = ckpt_noise if noise_mode is None else noise_mode

    mismatches = []
    if nl_ltp is not None and not _float_matches(nl_ltp, ckpt_ltp):
        mismatches.append(f"NL_LTP checkpoint={ckpt_ltp} eval={nl_ltp}")
    if nl_ltd is not None and not _float_matches(nl_ltd, ckpt_ltd):
        mismatches.append(f"NL_LTD checkpoint={ckpt_ltd} eval={nl_ltd}")
    if noise_mode is not None and ckpt_noise is not None and noise_mode != ckpt_noise:
        mismatches.append(f"noise_mode checkpoint={ckpt_noise} eval={noise_mode}")

    if mismatches and not allow_eval_nl_override:
        raise ValueError(
            "Refusing train/eval provenance mismatch without --allow-eval-nl-override: "
            + "; ".join(mismatches)
        )

    return resolved_ltp, resolved_ltd, resolved_noise, mismatches


def evaluate_once(model, testloader, criterion, device, exp_cfg, amp_enabled=False):
    return evaluate(model, testloader, criterion, device, exp_cfg, amp_enabled)


def run_mc_eval(model, testloader, criterion, device, exp_cfg, amp_enabled, eval_runs, label=None):
    losses = []
    accuracies = []
    for run_idx in range(eval_runs):
        loss, acc = evaluate_once(model, testloader, criterion, device, exp_cfg, amp_enabled)
        losses.append(loss)
        accuracies.append(acc)
    mean_acc = float(np.mean(accuracies))
    std_acc = float(np.std(accuracies)) if len(accuracies) > 1 else 0.0
    return {
        "eval_runs": eval_runs,
        "test_loss_mean": float(np.mean(losses)),
        "test_acc_mean": mean_acc,
        "test_acc_min": float(min(accuracies)),
        "test_acc_max": float(max(accuracies)),
        "test_acc_std": std_acc,
    }


def evaluate_on_fresh_instances(checkpoint_path, device,
                                num_instances=10, mc_runs_per_instance=5,
                                nl_ltp=None, nl_ltd=None, noise_mode=None,
                                allow_eval_nl_override=False,
                                data_root="../data/tiny-imagenet-200",
                                batch_size=None):
    provenance = load_checkpoint_provenance(checkpoint_path)
    nl_ltp, nl_ltd, noise_mode, mismatches = resolve_eval_overrides(
        provenance,
        nl_ltp=nl_ltp,
        nl_ltd=nl_ltd,
        noise_mode=noise_mode,
        allow_eval_nl_override=allow_eval_nl_override,
    )

    ckpt = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    exp_cfg_dict = ckpt.get("exp_cfg", {})
    exp_cfg = ViTTinyImageNetConfig(**exp_cfg_dict)

    # Override NL if specified
    if nl_ltp is not None:
        exp_cfg.nl_ltp = nl_ltp
    if nl_ltd is not None:
        exp_cfg.nl_ltd = nl_ltd
    if noise_mode is not None:
        exp_cfg.noise_mode = noise_mode

    _batch_size = batch_size if batch_size is not None else exp_cfg.batch_size
    model = build_model(exp_cfg, device, pretrained=False)
    model.load_state_dict(ckpt["model_state_dict"], strict=False)

    # Push NL overrides into the actual analog layer configs
    for module in model.modules():
        if hasattr(module, 'config'):
            if nl_ltp is not None:
                module.config.NL_LTP = nl_ltp
            if nl_ltd is not None:
                module.config.NL_LTD = nl_ltd
            if noise_mode is not None:
                module.config.noise_mode = noise_mode

    _, testloader = get_dataloaders(
        data_root=data_root,
        batch_size=_batch_size,
        num_workers=4,
        seed=None,
    )

    amp_enabled = provenance.get("amp_enabled", False)
    criterion = torch.nn.CrossEntropyLoss()

    instance_accs = []
    print(f"\nEvaluating {exp_cfg.name} from {checkpoint_path} on {num_instances} fresh instances...")
    print(f"  Config: NL_LTP={exp_cfg.nl_ltp}, NL_LTD={exp_cfg.nl_ltd}, noise_mode={exp_cfg.noise_mode}")
    print(
        "  Checkpoint provenance: "
        f"NL_LTP={provenance.get('checkpoint_nl_ltp')}, "
        f"NL_LTD={provenance.get('checkpoint_nl_ltd')}, "
        f"noise_mode={provenance.get('checkpoint_noise_mode')}, "
        f"seed={provenance.get('checkpoint_seed')}"
    )

    for instance_idx in range(num_instances):
        seed = 42 + instance_idx * 100
        torch.manual_seed(seed)
        np.random.seed(seed)

        # Resample D2D noise for this fresh instance
        resample_d2d_buffers(model)

        stats = run_mc_eval(
            model, testloader, criterion, device, exp_cfg, amp_enabled,
            eval_runs=mc_runs_per_instance,
            label=f"Instance {instance_idx+1}/{num_instances}",
        )
        instance_accs.append(stats["test_acc_mean"])
        print(f"  Instance {instance_idx+1}: {stats['test_acc_mean']:.2f}%")

    mean_acc = float(np.mean(instance_accs))
    std_acc = float(np.std(instance_accs))
    print(f"Result: Mean={mean_acc:.4f}%, Std={std_acc:.4f}%, Range={min(instance_accs):.2f}--{max(instance_accs):.2f}%\n")

    return {
        "checkpoint_path": str(checkpoint_path),
        "exp_id": exp_cfg.name,
        "fresh_instances": num_instances,
        "mc_runs_per_instance": mc_runs_per_instance,
        "nl_ltp": exp_cfg.nl_ltp,
        "nl_ltd": exp_cfg.nl_ltd,
        "noise_mode": exp_cfg.noise_mode,
        "allow_eval_nl_override": allow_eval_nl_override,
        "eval_provenance_mismatches": mismatches,
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
    parser.add_argument("--device", default=None)
    parser.add_argument("--num-instances", type=int, default=10)
    parser.add_argument("--mc-runs", type=int, default=5)
    parser.add_argument("--nl-ltp", type=float, default=None)
    parser.add_argument("--nl-ltd", type=float, default=None)
    parser.add_argument("--noise-mode", default=None)
    parser.add_argument("--allow-eval-nl-override", action="store_true",
                        help="Allow eval NL/noise settings to differ from checkpoint metadata")
    parser.add_argument("--output", default=None)
    parser.add_argument("--data-root", default="../data/tiny-imagenet-200")
    parser.add_argument("--batch-size", type=int, default=None)
    args = parser.parse_args()

    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")
    result = evaluate_on_fresh_instances(
        args.checkpoint, device,
        args.num_instances, args.mc_runs,
        args.nl_ltp, args.nl_ltd, args.noise_mode,
        args.allow_eval_nl_override,
        data_root=args.data_root,
        batch_size=args.batch_size,
    )

    ckpt_path = Path(args.checkpoint)
    output_path = args.output or f"report_md/_gpt/json_gpt/{ckpt_path.parent.name}_{ckpt_path.stem}_fresh_eval.json"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Saved to {output_path}")


if __name__ == "__main__":
    main()
