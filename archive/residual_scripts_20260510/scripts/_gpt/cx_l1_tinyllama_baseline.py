#!/usr/bin/env python3
"""CX-L1: HuggingFace causal-LM perplexity baseline for Work 2.

This establishes the digital FP16/BF16 baseline before KV-cache analog noise hooks
are introduced. It is written to be conservative: use --dry-run for a no-download
configuration check, or --local-files-only to require an existing HF cache.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_JSON = ROOT / "report_md" / "_gpt" / "json_gpt" / "cx_l1_tinyllama_baseline.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def parse_dtype(name: str, torch_mod):
    if name == "auto":
        return "auto"
    if name == "fp16":
        return torch_mod.float16
    if name == "bf16":
        return torch_mod.bfloat16
    if name == "fp32":
        return torch_mod.float32
    raise ValueError(f"Unsupported dtype: {name}")


def load_texts(dataset_name: str, dataset_config: str, split: str, max_texts: int | None, local_files_only: bool) -> list[str]:
    from datasets import load_dataset

    # datasets uses download_mode/cache controls but does not expose local_files_only
    # as directly as transformers. Offline users can set HF_DATASETS_OFFLINE=1.
    ds = load_dataset(dataset_name, dataset_config, split=split)
    texts = []
    for item in ds:
        text = item.get("text", "")
        if text and not text.isspace():
            texts.append(text)
        if max_texts is not None and len(texts) >= max_texts:
            break
    return texts


def iter_windows(input_ids, block_size: int, stride: int, max_tokens: int | None):
    total_len = input_ids.size(1)
    if max_tokens is not None:
        total_len = min(total_len, max_tokens)
    for begin in range(0, total_len, stride):
        end = min(begin + block_size, total_len)
        trg_len = end - begin
        if trg_len <= 1:
            break
        yield begin, end, trg_len
        if end >= total_len:
            break


def evaluate_ppl(args: argparse.Namespace) -> dict:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    started = time.time()
    device = args.device
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"

    dtype = parse_dtype(args.dtype, torch)
    tokenizer = AutoTokenizer.from_pretrained(args.model_id, local_files_only=args.local_files_only)
    model = AutoModelForCausalLM.from_pretrained(
        args.model_id,
        torch_dtype=dtype,
        device_map=None,
        local_files_only=args.local_files_only,
    )
    model.to(device)
    model.eval()

    texts = load_texts(args.dataset, args.dataset_config, args.split, args.max_texts, args.local_files_only)
    if not texts:
        raise RuntimeError("No non-empty texts loaded from dataset.")
    joined = "\n\n".join(texts)
    encoded = tokenizer(joined, return_tensors="pt")
    input_ids = encoded.input_ids.to(device)

    nll_sum = 0.0
    token_count = 0
    window_count = 0
    with torch.no_grad():
        for begin, end, trg_len in iter_windows(input_ids, args.block_size, args.stride, args.max_tokens):
            input_slice = input_ids[:, begin:end]
            target_ids = input_slice.clone()
            if begin > 0:
                target_ids[:, :-trg_len] = -100
            with torch.autocast(device_type="cuda", dtype=torch.float16, enabled=(device == "cuda" and args.amp)):
                out = model(input_slice, labels=target_ids)
            valid_tokens = int((target_ids[:, 1:] != -100).sum().item())
            if valid_tokens <= 0:
                continue
            nll_sum += float(out.loss.item()) * valid_tokens
            token_count += valid_tokens
            window_count += 1

    if token_count <= 0:
        raise RuntimeError("No valid tokens evaluated.")
    mean_nll = nll_sum / token_count
    return {
        "experiment": "cx_l1_tinyllama_baseline",
        "generated_at": now_iso(),
        "model_id": args.model_id,
        "dataset": args.dataset,
        "dataset_config": args.dataset_config,
        "split": args.split,
        "device": device,
        "dtype": args.dtype,
        "amp": bool(args.amp),
        "block_size": args.block_size,
        "stride": args.stride,
        "max_texts": args.max_texts,
        "max_tokens": args.max_tokens,
        "tokens_evaluated": token_count,
        "windows": window_count,
        "mean_nll": mean_nll,
        "perplexity": math.exp(mean_nll),
        "wall_clock_s": time.time() - started,
        "local_files_only": bool(args.local_files_only),
    }


def dry_run_result(args: argparse.Namespace) -> dict:
    import torch
    import transformers
    import datasets

    return {
        "experiment": "cx_l1_tinyllama_baseline",
        "generated_at": now_iso(),
        "dry_run": True,
        "ready_to_run": True,
        "model_id": args.model_id,
        "dataset": args.dataset,
        "dataset_config": args.dataset_config,
        "split": args.split,
        "device_requested": args.device,
        "cuda_available": torch.cuda.is_available(),
        "torch_version": torch.__version__,
        "transformers_version": transformers.__version__,
        "datasets_version": datasets.__version__,
        "json_out": str(args.json_out),
        "note": "Dry run only: no model or dataset loaded/downloaded.",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-id", default="TinyLlama/TinyLlama-1.1B-intermediate")
    parser.add_argument("--dataset", default="wikitext")
    parser.add_argument("--dataset-config", default="wikitext-103-raw-v1")
    parser.add_argument("--split", default="validation")
    parser.add_argument("--device", default="auto", choices=["auto", "cuda", "cpu"])
    parser.add_argument("--dtype", default="fp16", choices=["auto", "fp16", "bf16", "fp32"])
    parser.add_argument("--amp", action="store_true")
    parser.add_argument("--block-size", type=int, default=1024)
    parser.add_argument("--stride", type=int, default=512)
    parser.add_argument("--max-texts", type=int, default=256)
    parser.add_argument("--max-tokens", type=int, default=10000)
    parser.add_argument("--local-files-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json-out", type=Path, default=DEFAULT_JSON)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = dry_run_result(args) if args.dry_run else evaluate_ppl(args)
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
