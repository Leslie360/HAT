"""Training smoke entry point for Work 2.

This script is intentionally conservative. It supports a small overfit-style
training smoke on Pythia 410M to verify that the hybrid conversion still allows
loss/backprop/optimizer flow without claiming publication-quality numbers.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path
from typing import Iterable, List

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Work 2 Pythia training smoke")
    parser.add_argument("--model", default="EleutherAI/pythia-410m-deduped")
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    parser.add_argument("--dtype", default="float32", choices=["float32", "float16"])
    parser.add_argument("--local-files-only", action="store_true")
    parser.add_argument("--steps", type=int, default=20)
    parser.add_argument("--lr", type=float, default=1e-5)
    parser.add_argument("--seed", type=int, default=1234)
    parser.add_argument("--max-length", type=int, default=64)
    parser.add_argument("--hybrid", action="store_true")
    parser.add_argument(
        "--analog-scope",
        default="all",
        choices=["all", "qkv", "attention_output", "mlp", "qkv_attention"],
        help="Pythia module subset to convert when --hybrid is enabled",
    )
    parser.add_argument("--high-precision-analog", action="store_true")
    parser.add_argument("--noise-enabled", action="store_true", help="Enable analog noise during hybrid smoke")
    parser.add_argument("--sigma-d2d", type=float, default=0.10)
    parser.add_argument("--sigma-c2c", type=float, default=0.05)
    parser.add_argument("--train-scope", default="last_block", choices=["last_block", "analog_all", "lm_head"])
    parser.add_argument(
        "--eval-text-set",
        default="train",
        choices=["train", "heldout"],
        help="Use the train smoke texts or a disjoint held-out smoke text set for eval",
    )
    parser.add_argument("--resample-every", type=int, default=0, help="Resample analog D2D buffers every N steps; 0 disables")
    parser.add_argument("--eval-repeats", type=int, default=3, help="Independent eval repeats before and after training")
    parser.add_argument(
        "--fresh-d2d-instances",
        type=int,
        default=0,
        help="After training, evaluate this many fresh D2D instances; 0 disables",
    )
    parser.add_argument(
        "--fresh-d2d-repeats",
        type=int,
        default=3,
        help="C2C eval repeats per fresh D2D instance when --fresh-d2d-instances > 0",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.steps <= 0:
        raise SystemExit("--steps must be positive")

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    from analog_layers import AnalogLinear, AnalogLinearConfig
    from paper2.src.llm_hybrid import convert_pythia_to_hybrid, discover_pythia_linear_modules

    random.seed(args.seed)
    torch.manual_seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)

    device = "cuda" if args.device == "auto" and torch.cuda.is_available() else args.device
    if device == "auto":
        device = "cpu"
    dtype = torch.float32 if args.dtype == "float32" else torch.float16

    started = time.time()
    print(json.dumps({
        "event": "start",
        "argv": sys.argv[1:],
        "model": args.model,
        "device": device,
        "dtype": str(dtype),
        "hybrid": args.hybrid,
        "analog_scope": args.analog_scope if args.hybrid else "none",
        "high_precision_analog": args.high_precision_analog,
        "noise_enabled": args.noise_enabled,
        "sigma_d2d": args.sigma_d2d if args.noise_enabled else 0.0,
        "sigma_c2c": args.sigma_c2c if args.noise_enabled else 0.0,
        "train_scope": args.train_scope,
        "eval_text_set": args.eval_text_set,
        "steps": args.steps,
        "lr": args.lr,
        "seed": args.seed,
        "resample_every": args.resample_every,
        "eval_repeats": args.eval_repeats,
        "fresh_d2d_instances": args.fresh_d2d_instances,
        "fresh_d2d_repeats": args.fresh_d2d_repeats,
        "max_length": args.max_length,
        "local_files_only": args.local_files_only,
    }), flush=True)

    tokenizer = AutoTokenizer.from_pretrained(args.model, local_files_only=args.local_files_only)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(args.model, dtype=dtype, local_files_only=args.local_files_only)
    model.to(device)

    if args.hybrid:
        analog_cfg = AnalogLinearConfig(
            n_states=65536 if args.high_precision_analog else 16,
            noise_enabled=args.noise_enabled,
            restore_weight_scale=True,
            sigma_c2c=args.sigma_c2c if args.noise_enabled else 0.0,
            sigma_d2d=args.sigma_d2d if args.noise_enabled else 0.0,
        )
        include_qkv = args.analog_scope in {"all", "qkv", "qkv_attention"}
        include_attention_output = args.analog_scope in {"all", "attention_output", "qkv_attention"}
        include_mlp = args.analog_scope in {"all", "mlp"}
        model, mapping = convert_pythia_to_hybrid(
            model,
            config=analog_cfg,
            include_qkv=include_qkv,
            include_attention_output=include_attention_output,
            include_mlp=include_mlp,
            verbose=False,
        )
    else:
        mapping = discover_pythia_linear_modules(model)

    trainable_names = set(_select_trainable_names(model, args.train_scope, analog_only=args.hybrid))
    for name, param in model.named_parameters():
        param.requires_grad = name in trainable_names
    trainable_params = [param for param in model.parameters() if param.requires_grad]
    if not trainable_params:
        raise RuntimeError(f"no trainable parameters selected for scope {args.train_scope}")

    texts = [
        "Analog compute-in-memory accelerators must tolerate device variation during transformer decoding.",
        "The key value cache stores attention states and is repeatedly read during autoregressive inference.",
        "Hybrid-aware training should reduce sensitivity to persistent device mismatch and fresh read noise.",
        "This is a small smoke batch for infrastructure validation, not a benchmark dataset.",
    ]
    eval_texts = texts if args.eval_text_set == "train" else [
        "Autoregressive language models reuse cached keys and values to avoid recomputing prior tokens.",
        "Device noise in analog memory can accumulate across long context windows and repeated reads.",
        "A credible accelerator study needs held-out evaluation rather than only fitting a smoke batch.",
        "Scoped analog conversion helps identify which transformer submodules are robust under noise.",
    ]
    batch = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=args.max_length)
    batch = {key: value.to(device) for key, value in batch.items()}
    labels = batch["input_ids"].clone()
    labels[batch["attention_mask"] == 0] = -100
    eval_batch = tokenizer(eval_texts, return_tensors="pt", padding=True, truncation=True, max_length=args.max_length)
    eval_batch = {key: value.to(device) for key, value in eval_batch.items()}
    eval_labels = eval_batch["input_ids"].clone()
    eval_labels[eval_batch["attention_mask"] == 0] = -100

    optimizer = torch.optim.SGD(trainable_params, lr=args.lr)
    losses: List[float] = []
    eval_before = _eval_loss(model, eval_batch, eval_labels, repeats=args.eval_repeats)
    print(json.dumps({"event": "eval_before", **eval_before}), flush=True)
    model.train()
    for step in range(args.steps):
        optimizer.zero_grad(set_to_none=True)
        out = model(**batch, labels=labels)
        loss = out.loss
        if not torch.isfinite(loss):
            raise RuntimeError(f"non-finite loss at step {step}: {loss}")
        loss.backward()
        optimizer.step()
        if args.resample_every > 0 and args.hybrid and (step + 1) % args.resample_every == 0:
            resampled = _resample_analog_d2d(model)
        else:
            resampled = 0
        loss_value = float(loss.detach().cpu())
        losses.append(loss_value)
        print(json.dumps({"event": "step", "step": step, "pre_update_loss": loss_value, "resampled": resampled}), flush=True)

    peak_mem = torch.cuda.max_memory_allocated() / (1024 ** 3) if device == "cuda" else 0.0
    analog_counts = _count_analog_modules_by_kind(model) if args.hybrid else {"qkv": 0, "attention_output": 0, "mlp": 0}
    eval_after = _eval_loss(model, eval_batch, eval_labels, repeats=args.eval_repeats)
    print(json.dumps({"event": "eval_after", **eval_after}), flush=True)
    fresh_d2d_eval = None
    if args.hybrid and args.fresh_d2d_instances > 0:
        fresh_d2d_eval = _eval_fresh_d2d(
            model,
            eval_batch,
            eval_labels,
            instances=args.fresh_d2d_instances,
            repeats=args.fresh_d2d_repeats,
        )
        print(json.dumps({"event": "fresh_d2d_eval", **fresh_d2d_eval}), flush=True)
    print(json.dumps({
        "event": "complete",
        "analog_scope": args.analog_scope if args.hybrid else "none",
        "initial_pre_update_loss": losses[0],
        "final_pre_update_loss": losses[-1],
        "pre_update_loss_delta": losses[-1] - losses[0],
        "pre_update_loss_decreased": losses[-1] < losses[0],
        "min_pre_update_loss": min(losses),
        "eval_before_mean": eval_before["mean_loss"],
        "eval_after_mean": eval_after["mean_loss"],
        "eval_delta": eval_after["mean_loss"] - eval_before["mean_loss"],
        "eval_decreased": eval_after["mean_loss"] < eval_before["mean_loss"],
        "fresh_d2d_mean_loss": fresh_d2d_eval["mean_loss"] if fresh_d2d_eval else None,
        "fresh_d2d_std_loss": fresh_d2d_eval["std_loss"] if fresh_d2d_eval else None,
        "fresh_d2d_instances": fresh_d2d_eval["instances"] if fresh_d2d_eval else 0,
        "fresh_d2d_repeats": fresh_d2d_eval["repeats_per_instance"] if fresh_d2d_eval else 0,
        "trainable_params": sum(param.numel() for param in trainable_params),
        "qkv_modules": analog_counts["qkv"],
        "attention_output_modules": analog_counts["attention_output"],
        "mlp_modules": analog_counts["mlp"],
        "discovered_qkv_modules": len(mapping.qkv),
        "discovered_attention_output_modules": len(mapping.attention_output),
        "discovered_mlp_modules": len(mapping.mlp),
        "peak_cuda_mem_gb": peak_mem,
        "elapsed_s": time.time() - started,
    }, indent=2), flush=True)


def _select_trainable_names(model: object, scope: str, analog_only: bool) -> Iterable[str]:
    analog_prefixes = set()
    if analog_only:
        from analog_layers import AnalogLinear

        analog_prefixes = {name for name, module in model.named_modules() if isinstance(module, AnalogLinear)}

    if scope == "lm_head":
        tokens = ("embed_out", "lm_head")
        return [name for name, _ in model.named_parameters() if any(token in name for token in tokens)]

    names = []
    for name, param in model.named_parameters():
        if scope == "last_block" and "gpt_neox.layers.23" not in name:
            continue
        if analog_only and not any(name == f"{prefix}.weight" or name == f"{prefix}.bias" for prefix in analog_prefixes):
            continue
        names.append(name)
    return names


def _count_analog_modules_by_kind(model: object) -> dict:
    from analog_layers import AnalogLinear
    from paper2.src.llm_hybrid import classify_pythia_linear

    counts = {"qkv": 0, "attention_output": 0, "mlp": 0}
    for name, module in model.named_modules():
        if not isinstance(module, AnalogLinear):
            continue
        kind = classify_pythia_linear(name)
        if kind in counts:
            counts[kind] += 1
    return counts


def _eval_loss(model: object, batch: dict, labels: object, repeats: int) -> dict:
    import torch

    repeats = max(1, repeats)
    was_training = model.training
    model.eval()
    losses = []
    with torch.no_grad():
        for _ in range(repeats):
            out = model(**batch, labels=labels)
            loss = out.loss
            if not torch.isfinite(loss):
                raise RuntimeError(f"non-finite eval loss: {loss}")
            losses.append(float(loss.detach().cpu()))
    if was_training:
        model.train()
    mean = sum(losses) / len(losses)
    variance = sum((value - mean) ** 2 for value in losses) / len(losses)
    return {
        "losses": losses,
        "mean_loss": mean,
        "std_loss": variance ** 0.5,
        "repeats": len(losses),
    }


def _resample_analog_d2d(model: object) -> int:
    from analog_layers import AnalogLinear

    count = 0
    for module in model.modules():
        if isinstance(module, AnalogLinear):
            module.resample_d2d_noise()
            count += 1
    return count


def _eval_fresh_d2d(model: object, batch: dict, labels: object, instances: int, repeats: int) -> dict:
    losses = []
    instance_means = []
    for instance_idx in range(max(1, instances)):
        resampled = _resample_analog_d2d(model)
        result = _eval_loss(model, batch, labels, repeats=repeats)
        instance_means.append(
            {
                "instance": instance_idx,
                "mean_loss": result["mean_loss"],
                "std_loss": result["std_loss"],
                "resampled_modules": resampled,
            }
        )
        losses.append(result["mean_loss"])
    mean = sum(losses) / len(losses)
    variance = sum((value - mean) ** 2 for value in losses) / len(losses)
    return {
        "instance_means": instance_means,
        "mean_loss": mean,
        "std_loss": variance ** 0.5,
        "instances": len(losses),
        "repeats_per_instance": max(1, repeats),
    }


if __name__ == "__main__":
    main()
