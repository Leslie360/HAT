"""
HAT Training for Qwen3-VL Analog KV Cache (pure text, WikiText-2)

Adapts p3_hat_train.py for Qwen3-VL:
  - Loads Qwen3VLForConditionalGeneration
  - Patches Qwen3VLTextAttention layers for analog KV
  - Trains on pure text (no images) for next-token prediction
  - Evaluates PPL on WikiText-2 test

Usage:
    CUDA_VISIBLE_DEVICES=4 python p3_hat_vlm_train.py \
        --model_name Qwen/Qwen3-VL-2B-Instruct \
        --analog_layers 27 --max_steps 500 --fp16
"""

import copy
import math
import os
if not os.environ.get("HF_ENDPOINT"):
    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
import sys
import json
import argparse
import types
import subprocess
import time
from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import AdamW
from transformers import Qwen3VLForConditionalGeneration, AutoTokenizer
from datasets import load_dataset
from tqdm import tqdm

sys.path.insert(0, '/home/lisq753/projects/HAT/HAT')
from analog_layers import AnalogLinearConfig
from p3_hat_train import analogize_kv_tensor
from p3_hat_vlm_eval import patch_vlm_for_hat, detect_model_family


def train_hat_vlm(
    model,
    tokenizer,
    analog_cfg: AnalogLinearConfig,
    device: str = "cuda",
    epochs: int = 1,
    lr: float = 1e-5,
    max_length: int = 512,
    batch_size: int = 1,
    grad_accum: int = 4,
    max_steps: int = 100,
    analog_layers: Optional[set] = None,
    freeze_non_target: bool = False,
    fp16: bool = False,
):
    """Run HAT training on WikiText-2 for Qwen3-VL (text-only)."""
    num_layers = getattr(model.config, "num_hidden_layers", None)
    if num_layers is None and hasattr(model.config, "text_config"):
        num_layers = model.config.text_config.num_hidden_layers
    target_layers = analog_layers if analog_layers is not None else set(range(num_layers))

    if freeze_non_target and len(target_layers) < num_layers:
        frozen_count = 0
        trainable_count = 0
        for name, p in model.named_parameters():
            layer_idx = None
            for part in name.split('.'):
                if part.isdigit():
                    layer_idx = int(part)
                    break
            if layer_idx is not None and layer_idx not in target_layers:
                p.requires_grad = False
                frozen_count += p.numel()
            else:
                trainable_count += p.numel()
        print(f"[freeze_non_target] Frozen {frozen_count:,} params, trainable {trainable_count:,} params")
        params_to_optimize = model.parameters()
    else:
        params_to_optimize = model.parameters()

    optimizer = AdamW(params_to_optimize, lr=lr, weight_decay=0.01)

    dataset = load_dataset("wikitext", "wikitext-2-raw-v1", split="train")
    text = "\n\n".join(dataset["text"])
    encodings = tokenizer(text, return_tensors="pt")
    seq_len = encodings.input_ids.size(1)

    use_amp = (not fp16) and torch.cuda.is_available()
    scaler = torch.amp.GradScaler("cuda") if use_amp else None

    model.train()
    step = 0
    losses = []

    pbar = tqdm(total=max_steps, desc="HAT-VLM Training")
    for epoch in range(epochs):
        for begin_loc in range(0, seq_len - max_length, max_length // 2):
            end_loc = min(begin_loc + max_length, seq_len)
            input_ids = encodings.input_ids[:, begin_loc:end_loc].to(device)
            attention_mask = encodings.attention_mask[:, begin_loc:end_loc].to(device) if hasattr(encodings, 'attention_mask') else None

            with torch.amp.autocast("cuda", enabled=use_amp):
                # Qwen3-VL accepts text-only inputs; pixel_values omitted
                outputs = model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    use_cache=False,
                )
                logits = outputs.logits

                shift_logits = logits[..., :-1, :].contiguous()
                shift_labels = input_ids[..., 1:].contiguous()
                loss = F.cross_entropy(
                    shift_logits.view(-1, shift_logits.size(-1)),
                    shift_labels.view(-1),
                )
            loss = loss / grad_accum

            if use_amp:
                scaler.scale(loss).backward()
            else:
                loss.backward()

            if (step + 1) % grad_accum == 0:
                if use_amp:
                    scaler.step(optimizer)
                    scaler.update()
                else:
                    optimizer.step()
                optimizer.zero_grad()

            losses.append(loss.item() * grad_accum)
            pbar.update(1)
            pbar.set_postfix({
                "loss": f"{losses[-1]:.3f}",
                "avg": f"{sum(losses[-10:]) / len(losses[-10:]):.3f}",
            })

            step += 1
            if step >= max_steps:
                break
        if step >= max_steps:
            break

    pbar.close()
    return losses


def evaluate_ppl_vlm(model, tokenizer, device="cuda", max_tokens=999999, max_length=512, fp16=False):
    """Quick PPL eval on WikiText-2 test for Qwen3-VL (text-only)."""
    model.eval()
    dataset = load_dataset("wikitext", "wikitext-2-raw-v1", split="test")
    text = "\n\n".join(dataset["text"])
    encodings = tokenizer(text, return_tensors="pt")
    seq_len = min(encodings.input_ids.size(1), max_tokens)

    nlls = []
    total_predicted = 0
    with torch.no_grad():
        for begin_loc in range(0, seq_len, max_length):
            end_loc = min(begin_loc + max_length, seq_len)
            input_ids = encodings.input_ids[:, begin_loc:end_loc].to(device)
            attention_mask = encodings.attention_mask[:, begin_loc:end_loc].to(device) if hasattr(encodings, 'attention_mask') else None
            with torch.amp.autocast("cuda", enabled=fp16):
                outputs = model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    use_cache=False,
                )
                logits = outputs.logits
                shift_logits = logits[..., :-1, :].contiguous()
                shift_labels = input_ids[..., 1:].contiguous()
                loss = F.cross_entropy(
                    shift_logits.view(-1, shift_logits.size(-1)),
                    shift_labels.view(-1),
                    reduction='sum',
                )
            nlls.append(loss.item())
            total_predicted += shift_labels.numel()

    return math.exp(sum(nlls) / total_predicted)


def _git_info():
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=os.path.dirname(__file__),
            stderr=subprocess.DEVNULL,
            timeout=5,
        ).decode().strip()
        status = subprocess.check_output(
            ["git", "status", "--short"],
            cwd=os.path.dirname(__file__),
            stderr=subprocess.DEVNULL,
            timeout=5,
        ).decode().strip()
    except Exception:
        commit, status = None, None
    return commit, status


def main():
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, default="hat_vlm_warmup")
    parser.add_argument("--n_states", type=int, default=256)
    parser.add_argument("--sigma_c2c", type=float, default=0.01)
    parser.add_argument("--sigma_d2d", type=float, default=0.0)
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--lr", type=float, default=1e-5)
    parser.add_argument("--max_length", type=int, default=512)
    parser.add_argument("--max_steps", type=int, default=100)
    parser.add_argument("--analog_layers", type=str, default=None)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--d2d-seed", type=int, default=0xD2D, dest="d2d_seed")
    parser.add_argument("--model_name", type=str, default="Qwen/Qwen3-VL-2B-Instruct")
    parser.add_argument(
        "--output_dir",
        type=str,
        default="/home/lisq753/projects/HAT_kv107/paper2/results/remote107",
    )
    parser.add_argument("--freeze-non-target-params", action="store_true")
    parser.add_argument("--fp16", action="store_true")
    args = parser.parse_args()

    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"

    analog_cfg = AnalogLinearConfig(
        n_states=args.n_states,
        sigma_c2c=args.sigma_c2c,
        sigma_d2d=args.sigma_d2d,
    )

    analog_layers = set(int(x) for x in args.analog_layers.split(",")) if args.analog_layers else None

    print(f"Loading {args.model_name}...")
    dtype = torch.bfloat16 if args.fp16 else torch.float32
    model = Qwen3VLForConditionalGeneration.from_pretrained(
        args.model_name,
        torch_dtype=dtype,
        use_safetensors=True,
        local_files_only=False,
    )
    tokenizer = AutoTokenizer.from_pretrained(args.model_name, local_files_only=False, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    model = model.to(device)

    print("Patching text decoder attention for analog KV...")
    patch_vlm_for_hat(
        model,
        analog_cfg,
        analog_layers,
        max_length=args.max_length,
        d2d_seed=args.d2d_seed,
    )

    print("\nPre-HAT PPL eval...")
    ppl_before = evaluate_ppl_vlm(model, tokenizer, device, max_length=args.max_length, fp16=args.fp16)
    print(f"PPL before HAT: {ppl_before:.2f}")

    print("\nStarting HAT training...")
    losses = train_hat_vlm(
        model,
        tokenizer,
        analog_cfg,
        device=device,
        epochs=args.epochs,
        lr=args.lr,
        max_length=args.max_length,
        max_steps=args.max_steps,
        analog_layers=analog_layers,
        freeze_non_target=args.freeze_non_target_params,
        fp16=args.fp16,
    )

    print("\nPost-HAT PPL eval...")
    ppl_after = evaluate_ppl_vlm(model, tokenizer, device, max_length=args.max_length, fp16=args.fp16)
    print(f"PPL after HAT:  {ppl_after:.2f}")

    num_layers = getattr(model.config, "num_hidden_layers", None)
    if num_layers is None and hasattr(model.config, "text_config"):
        num_layers = model.config.text_config.num_hidden_layers
    analog_layers_list = sorted(analog_layers) if analog_layers else list(range(num_layers))
    git_commit, git_status_short = _git_info()
    gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu"
    gpu_id = os.environ.get("CUDA_VISIBLE_DEVICES", "unknown")
    result = {
        "git_commit": git_commit,
        "git_status_short": git_status_short,
        "script": os.path.basename(__file__),
        "command": " ".join(sys.argv),
        "mode": "train",
        "model": args.model_name,
        "dataset_train": "wikitext-2-raw-v1 (train)",
        "dataset_eval": "wikitext-2-raw-v1 (test)",
        "train_seed": args.seed,
        "train_d2d_seed": args.d2d_seed,
        "eval_d2d_seed": None,
        "n_states": args.n_states,
        "sigma_c2c": args.sigma_c2c,
        "sigma_d2d": args.sigma_d2d,
        "analog_layers": analog_layers_list,
        "ctx_len": args.max_length,
        "stride": args.max_length // 2,
        "max_steps": args.max_steps,
        "batch_size": 1,
        "epochs": args.epochs,
        "lr": args.lr,
        "ppl_before": ppl_before,
        "ppl_after": ppl_after,
        "losses": losses,
        "wall_clock_time": time.time() - start_time,
        "gpu_id": gpu_id,
        "gpu_name": gpu_name,
    }

    ckpt_dir = os.path.join(args.output_dir, "checkpoints", f"{args.name}_seed{args.seed}")
    os.makedirs(ckpt_dir, exist_ok=True)
    model.save_pretrained(ckpt_dir)
    tokenizer.save_pretrained(ckpt_dir)

    hat_config = {
        "analog_layers": analog_layers_list,
        "d2d_seed": args.d2d_seed,
        "n_states": args.n_states,
    }
    with open(os.path.join(ckpt_dir, "hat_config.json"), "w") as f:
        json.dump(hat_config, f)
    print(f"\nCheckpoint saved: {ckpt_dir}")

    out_file = os.path.join(args.output_dir, f"{args.name}_seed{args.seed}.json")
    os.makedirs(args.output_dir, exist_ok=True)
    with open(out_file, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"Result saved: {out_file}")


if __name__ == "__main__":
    main()
