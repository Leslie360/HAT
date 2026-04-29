"""Pythia 410M smoke checks for Work 2 W1.

The script is intentionally explicit: it can load Hugging Face weights only when
run by the user/agent, and it writes no benchmark claims. Use it to verify model
loading, module discovery, FP forward, and later hybrid forward drift.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from dataclasses import asdict, dataclass
from typing import Dict, Optional

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Work 2 Pythia smoke checks")
    parser.add_argument("--model", default="EleutherAI/pythia-410m-deduped")
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    parser.add_argument("--dtype", default="auto", choices=["auto", "float16", "float32"], help="Model dtype; float32 is safest for hybrid drift checks")
    parser.add_argument("--max-length", type=int, default=64)
    parser.add_argument("--local-files-only", action="store_true")
    parser.add_argument("--hybrid", action="store_true", help="Also run no-noise hybrid conversion forward")
    parser.add_argument("--high-precision-analog", action="store_true", help="Use high n_states for drift smoke")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    import torch
    from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer

    from analog_layers import AnalogLinearConfig
    from paper2.src.llm_hybrid import convert_pythia_to_hybrid, discover_pythia_linear_modules

    if args.device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        device = args.device
    if args.dtype == "float16":
        dtype = torch.float16
    elif args.dtype == "float32":
        dtype = torch.float32
    else:
        dtype = torch.float16 if device == "cuda" else torch.float32

    started = time.time()
    print(json.dumps({"event": "start", "model": args.model, "device": device, "dtype": str(dtype)}), flush=True)

    config = AutoConfig.from_pretrained(args.model, local_files_only=args.local_files_only)
    tokenizer = AutoTokenizer.from_pretrained(args.model, local_files_only=args.local_files_only)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        dtype=dtype,
        local_files_only=args.local_files_only,
    )
    model.to(device)
    model.eval()

    summary = discover_pythia_linear_modules(model)
    texts = [
        "Analog compute-in-memory accelerators must tolerate device variation.",
        "The key-value cache stores transformer attention states during decoding.",
    ]
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=args.max_length)
    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.no_grad():
        fp_out = model(**inputs, labels=inputs["input_ids"])
    fp_loss = float(fp_out.loss.detach().cpu())
    fp_ppl = float(torch.exp(fp_out.loss.detach()).cpu())

    result = {
        "event": "fp_complete",
        "model": args.model,
        "model_type": getattr(config, "model_type", None),
        "hidden_size": getattr(config, "hidden_size", None),
        "num_hidden_layers": getattr(config, "num_hidden_layers", None),
        "num_attention_heads": getattr(config, "num_attention_heads", None),
        "intermediate_size": getattr(config, "intermediate_size", None),
        "max_position_embeddings": getattr(config, "max_position_embeddings", None),
        "input_shape": list(inputs["input_ids"].shape),
        "num_params": sum(param.numel() for param in model.parameters()),
        "qkv_modules": len(summary.qkv),
        "attention_output_modules": len(summary.attention_output),
        "mlp_modules": len(summary.mlp),
        "skipped_linear_modules": len(summary.skipped),
        "fp_loss": fp_loss,
        "fp_ppl": fp_ppl,
        "peak_cuda_mem_gb": torch.cuda.max_memory_allocated() / (1024 ** 3) if device == "cuda" else 0.0,
        "elapsed_s": time.time() - started,
    }
    print(json.dumps(result, indent=2), flush=True)

    if not args.hybrid:
        return

    analog_cfg = AnalogLinearConfig(
        n_states=65536 if args.high_precision_analog else 16,
        noise_enabled=False,
        restore_weight_scale=True,
        sigma_c2c=0.0,
        sigma_d2d=0.0,
    )
    convert_pythia_to_hybrid(model, config=analog_cfg, verbose=False)
    model.eval()
    with torch.no_grad():
        hybrid_out = model(**inputs, labels=inputs["input_ids"])
    hybrid_loss = float(hybrid_out.loss.detach().cpu())
    hybrid_ppl = float(torch.exp(hybrid_out.loss.detach()).cpu())
    print(json.dumps({
        "event": "hybrid_complete",
        "hybrid_loss": hybrid_loss,
        "hybrid_ppl": hybrid_ppl,
        "loss_delta": hybrid_loss - fp_loss,
        "ppl_delta": hybrid_ppl - fp_ppl,
        "high_precision_analog": args.high_precision_analog,
        "peak_cuda_mem_gb": torch.cuda.max_memory_allocated() / (1024 ** 3) if device == "cuda" else 0.0,
        "elapsed_s": time.time() - started,
    }, indent=2), flush=True)


if __name__ == "__main__":
    main()
