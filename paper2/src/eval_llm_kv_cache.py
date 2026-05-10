"""Offline analog KV-cache evaluation for Work 2.

This evaluator does not patch Hugging Face attention internals. Instead it loads
Pythia, captures real `past_key_values`, stores them in `AnalogKVCache`, and
measures reconstruction error after quantization plus persistent D2D and fresh
C2C reads. It is a required intermediate step before claiming end-to-end
perplexity with an analog KV cache.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Iterable, Sequence

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC = PROJECT_ROOT / "src" / "compute_vit"
for path in (str(SRC), str(PROJECT_ROOT)):
    if path not in sys.path:
        sys.path.insert(0, path)

from paper2.src.analog_kv_cache import AnalogKVCache, AnalogKVCacheConfig


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Offline Work 2 analog KV-cache read-noise evaluator")
    parser.add_argument("--model", default="EleutherAI/pythia-410m-deduped")
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda"])
    parser.add_argument("--dtype", default="float32", choices=["float32", "float16"])
    parser.add_argument("--local-files-only", action="store_true")
    parser.add_argument("--max-length", type=int, default=64)
    parser.add_argument("--layers", default="last", help="Layer selector: last, all, or comma-separated indices")
    parser.add_argument("--instances", type=int, default=10, help="Fresh D2D cache instances")
    parser.add_argument("--read-repeats", type=int, default=5, help="Fresh C2C reads per D2D instance")
    parser.add_argument("--sigma-d2d", type=float, default=0.005)
    parser.add_argument("--sigma-c2c", type=float, default=0.002)
    parser.add_argument("--bit-width", type=int, default=16)
    parser.add_argument("--no-quantize", action="store_true")
    parser.add_argument("--noise-disabled", action="store_true")
    parser.add_argument("--output-json", default="")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.instances <= 0 or args.read_repeats <= 0:
        raise SystemExit("--instances and --read-repeats must be positive")

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

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
        "layers": args.layers,
        "instances": args.instances,
        "read_repeats": args.read_repeats,
        "sigma_d2d": args.sigma_d2d,
        "sigma_c2c": args.sigma_c2c,
        "bit_width": args.bit_width,
        "quantize": not args.no_quantize,
        "noise_enabled": not args.noise_disabled,
        "local_files_only": args.local_files_only,
    }), flush=True)

    tokenizer = AutoTokenizer.from_pretrained(args.model, local_files_only=args.local_files_only)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(args.model, dtype=dtype, local_files_only=args.local_files_only)
    model.to(device)
    model.eval()

    texts = [
        "Autoregressive transformers reuse cached key and value states during long-context decoding.",
        "Analog memory read noise may perturb attention scores even when projection weights are accurate.",
        "Persistent device mismatch and cycle-to-cycle variation should be measured separately for cache tensors.",
        "This offline diagnostic captures real Pythia KV tensors but does not alter model attention outputs.",
    ]
    batch = tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=args.max_length)
    batch = {key: value.to(device) for key, value in batch.items()}

    with torch.no_grad():
        outputs = model(**batch, use_cache=True)
    cache_layers = _legacy_cache(outputs.past_key_values)
    selected = _select_layers(args.layers, len(cache_layers))
    cfg = AnalogKVCacheConfig(
        sigma_d2d=args.sigma_d2d,
        sigma_c2c=args.sigma_c2c,
        bit_width=args.bit_width,
        quantize=not args.no_quantize,
        noise_enabled=not args.noise_disabled,
    )

    layer_results = []
    for layer_idx in selected:
        k_ref, v_ref = cache_layers[layer_idx]
        result = _evaluate_layer(layer_idx, k_ref.detach(), v_ref.detach(), cfg, args.instances, args.read_repeats)
        layer_results.append(result)
        print(json.dumps({"event": "layer", **result}), flush=True)

    summary = _summarize(layer_results)
    output = {
        "event": "complete",
        "summary": summary,
        "layers": layer_results,
        "elapsed_s": time.time() - started,
    }
    print(json.dumps(output, indent=2), flush=True)
    if args.output_json:
        path = Path(args.output_json)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(output, indent=2), encoding="utf-8")


def _legacy_cache(past_key_values: object) -> Sequence[tuple]:
    if hasattr(past_key_values, "to_legacy_cache"):
        past_key_values = past_key_values.to_legacy_cache()
    elif hasattr(past_key_values, "layers"):
        layers = []
        for idx, layer in enumerate(past_key_values.layers):
            keys = getattr(layer, "keys", None)
            values = getattr(layer, "values", None)
            if keys is None or values is None or getattr(keys, "numel", lambda: 0)() == 0:
                raise RuntimeError(f"empty DynamicCache layer {idx}")
            layers.append((keys, values))
        return layers
    if not isinstance(past_key_values, (list, tuple)):
        raise RuntimeError(f"unsupported past_key_values type: {type(past_key_values)!r}")
    layers = []
    for idx, item in enumerate(past_key_values):
        if not isinstance(item, (list, tuple)) or len(item) < 2:
            raise RuntimeError(f"unsupported cache layer {idx}: {type(item)!r}")
        layers.append((item[0], item[1]))
    return layers


def _select_layers(selector: str, n_layers: int) -> list[int]:
    if n_layers <= 0:
        raise RuntimeError("model returned no cache layers")
    selector = selector.strip().lower()
    if selector == "last":
        return [n_layers - 1]
    if selector == "all":
        return list(range(n_layers))
    selected = []
    for token in selector.split(","):
        idx = int(token.strip())
        if idx < 0:
            idx = n_layers + idx
        if idx < 0 or idx >= n_layers:
            raise ValueError(f"layer index {idx} outside [0, {n_layers})")
        selected.append(idx)
    return selected


def _evaluate_layer(layer_idx: int, k_ref, v_ref, cfg: AnalogKVCacheConfig, instances: int, repeats: int) -> dict:
    import torch

    if k_ref.shape != v_ref.shape or k_ref.ndim != 4:
        raise RuntimeError(f"expected K/V shape (batch, heads, seq, dim), got {tuple(k_ref.shape)} and {tuple(v_ref.shape)}")
    batch_size, heads, seq_len, head_dim = k_ref.shape
    instance_rows = []
    for instance_idx in range(instances):
        cache = AnalogKVCache(
            layer_idx=layer_idx,
            num_heads=heads,
            head_dim=head_dim,
            max_seq_len=seq_len,
            batch_size=batch_size,
            config=cfg,
            device=k_ref.device,
            dtype=k_ref.dtype,
        )
        for pos in range(seq_len):
            cache.write(pos, k_ref[:, :, pos, :], v_ref[:, :, pos, :])
        read_rows = []
        for _ in range(repeats):
            k_read, v_read = cache.read()
            read_rows.append(_error_metrics(k_ref, v_ref, k_read, v_read))
        instance_rows.append(_mean_metrics(read_rows, extra={"instance": instance_idx}))
    return {
        "layer_idx": layer_idx,
        "shape": list(k_ref.shape),
        "instances": instances,
        "read_repeats": repeats,
        "instance_metrics": instance_rows,
        **_mean_metrics(instance_rows),
    }


def _error_metrics(k_ref, v_ref, k_read, v_read) -> dict:
    import torch

    k_err = (k_read - k_ref).float()
    v_err = (v_read - v_ref).float()
    k_ref_f = k_ref.float()
    v_ref_f = v_ref.float()
    k_mse = torch.mean(k_err.square()).item()
    v_mse = torch.mean(v_err.square()).item()
    k_power = torch.mean(k_ref_f.square()).clamp_min(1e-12).item()
    v_power = torch.mean(v_ref_f.square()).clamp_min(1e-12).item()
    return {
        "k_mse": k_mse,
        "v_mse": v_mse,
        "kv_mse": 0.5 * (k_mse + v_mse),
        "k_relative_mse": k_mse / k_power,
        "v_relative_mse": v_mse / v_power,
        "kv_relative_mse": 0.5 * ((k_mse / k_power) + (v_mse / v_power)),
    }


def _mean_metrics(rows: Iterable[dict], extra: dict | None = None) -> dict:
    rows = list(rows)
    keys = [
        "k_mse",
        "v_mse",
        "kv_mse",
        "k_relative_mse",
        "v_relative_mse",
        "kv_relative_mse",
    ]
    out = dict(extra or {})
    for key in keys:
        values = [float(row[key]) for row in rows]
        out[key] = sum(values) / len(values)
    return out


def _summarize(layer_results: Sequence[dict]) -> dict:
    return _mean_metrics(layer_results, extra={"n_layers": len(layer_results)})


if __name__ == "__main__":
    main()
