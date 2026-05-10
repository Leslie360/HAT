#!/usr/bin/env python3
"""Fresh-instance evaluator for post-fix rerun checkpoints."""
import argparse
import json
import subprocess
import torch
import numpy as np
from pathlib import Path

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
    }


def runtime_metadata():
    """Return audit metadata required by the M-series parity dispatch."""
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
    """Default eval settings to checkpoint metadata and reject silent mismatches."""
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


def evaluate_on_fresh_instances(model_type, exp_id, checkpoint_path, device, 
                                num_instances=10, mc_runs_per_instance=5,
                                nl_ltp=None, nl_ltd=None, noise_mode=None,
                                allow_eval_nl_override=False):
    from inference_analysis_utils import load_model_bundle, run_mc_eval, set_uniform_noise

    provenance = load_checkpoint_provenance(checkpoint_path)
    nl_ltp, nl_ltd, noise_mode, mismatches = resolve_eval_overrides(
        provenance,
        nl_ltp=nl_ltp,
        nl_ltd=nl_ltd,
        noise_mode=noise_mode,
        allow_eval_nl_override=allow_eval_nl_override,
    )
    bundle = load_model_bundle(model_type, exp_id, device, checkpoint_path)
    cfg = bundle.exp_cfg
    
    # Override NL if specified (for post-fix evaluation of checkpoints trained with specific NL)
    if nl_ltp is not None:
        cfg.nl_ltp = nl_ltp
    if nl_ltd is not None:
        cfg.nl_ltd = nl_ltd
    if noise_mode is not None:
        cfg.noise_mode = noise_mode
    
    # CRITICAL FIX: Push NL overrides into the actual model config
    for module in bundle.model.modules():
        if hasattr(module, 'config'):
            if nl_ltp is not None:
                module.config.NL_LTP = nl_ltp
            if nl_ltd is not None:
                module.config.NL_LTD = nl_ltd
            if noise_mode is not None:
                module.config.noise_mode = noise_mode
    
    instance_accs = []
    print(f"\nEvaluating {exp_id} from {checkpoint_path} on {num_instances} fresh instances...")
    print(f"  Config: NL_LTP={cfg.nl_ltp}, NL_LTD={cfg.nl_ltd}, noise_mode={cfg.noise_mode}")
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
        
        set_uniform_noise(bundle.model, sigma_c2c=cfg.sigma_c2c, sigma_d2d=cfg.sigma_d2d, 
                          noise_enabled=cfg.noise_enabled, resample_d2d=True, noise_mode=cfg.noise_mode)
        
        stats = run_mc_eval(bundle, eval_runs=mc_runs_per_instance, label=f"Instance {instance_idx+1}/{num_instances}")
        instance_accs.append(stats["test_acc_mean"])
        print(f"  Instance {instance_idx+1}: {stats['test_acc_mean']:.2f}%")
        
    mean_acc = float(np.mean(instance_accs))
    std_acc = float(np.std(instance_accs))
    print(f"Result: Mean={mean_acc:.4f}%, Std={std_acc:.4f}%, Range={min(instance_accs):.2f}--{max(instance_accs):.2f}%\n")
    
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
    parser.add_argument("--allow-eval-nl-override", action="store_true",
                        help="Allow eval NL/noise settings to differ from checkpoint metadata")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    
    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")
    result = evaluate_on_fresh_instances(
        args.model_type, args.exp_id, args.checkpoint, device,
        args.num_instances, args.mc_runs,
        args.nl_ltp, args.nl_ltd, args.noise_mode,
        args.allow_eval_nl_override
    )
    
    output_path = args.output or f"report_md/_gpt/json_gpt/{Path(args.checkpoint).stem}_fresh_eval.json"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()
