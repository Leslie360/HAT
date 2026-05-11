"""
Quantized KV Cache Baseline (INT4 / INT8 RTN)

Loads a clean model, monkey-patches attention to apply RTN quantization
on key/value states, and reports PPL on WikiText-2 test.

RTN (Round-To-Nearest) symmetric quantization:
  scale = max(|x|) / (2^(n-1) - 1)
  x_q   = round(x / scale)
  x_deq = x_q * scale
"""

import math
import os
import sys
import json
import argparse
import time

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset

sys.path.insert(0, '/home/lisq753/projects/HAT/HAT')

# Default HF mirror
if not os.environ.get("HF_ENDPOINT"):
    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"


def rtn_quantize_tensor(x: torch.Tensor, n_bits: int):
    """Symmetric per-head per-token RTN quantization."""
    if n_bits >= 16:
        return x
    qmax = 2 ** (n_bits - 1) - 1
    # Per-head, per-token dynamic range (same granularity as HAT)
    x_max = x.abs().amax(dim=-1, keepdim=True) + 1e-8
    scale = x_max / qmax
    x_q = torch.round(x / scale).clamp(-qmax, qmax)
    return x_q * scale


def patch_attention_for_rtn_quantization(model, n_bits: int, target_layers: set = None):
    """Monkey-patch GPTNeoXAttention to apply RTN quantization on KV states."""
    import types
    from transformers.models.gpt_neox.modeling_gpt_neox import apply_rotary_pos_emb

    num_layers = model.config.num_hidden_layers
    target = target_layers if target_layers is not None else set(range(num_layers))
    count = 0

    for name, module in model.named_modules():
        if 'attention' in name.lower() and type(module).__name__ == 'GPTNeoXAttention':
            layer_idx = None
            for p in name.split('.'):
                if p.isdigit():
                    layer_idx = int(p)
                    break
            if layer_idx is None or layer_idx not in target:
                continue

            original_forward = module.forward
            module._original_forward = original_forward

            def make_forward(attn_module, cfg_nbits):
                def forward(self, hidden_states, attention_mask, layer_past=None, position_embeddings=None, **kwargs):
                    input_shape = hidden_states.shape[:-1]
                    hidden_shape = (*input_shape, -1, 3 * attn_module.head_size)
                    qkv = attn_module.query_key_value(hidden_states).view(hidden_shape).transpose(1, 2)
                    query_states, key_states, value_states = qkv.chunk(3, dim=-1)

                    cos, sin = position_embeddings
                    query_states, key_states = apply_rotary_pos_emb(query_states, key_states, cos, sin)

                    if layer_past is not None:
                        key_states, value_states = layer_past.update(key_states, value_states, attn_module.layer_idx)

                    # === RTN quantization on KV ===
                    key_states = rtn_quantize_tensor(key_states, cfg_nbits)
                    value_states = rtn_quantize_tensor(value_states, cfg_nbits)
                    # ==============================

                    from transformers.models.gpt_neox.modeling_gpt_neox import ALL_ATTENTION_FUNCTIONS, eager_attention_forward
                    attn_interface = ALL_ATTENTION_FUNCTIONS.get_interface(
                        self.config._attn_implementation, eager_attention_forward
                    )
                    attn_output, attn_weights = attn_interface(
                        self, query_states, key_states, value_states,
                        attention_mask, scaling=self.scaling,
                        dropout=0.0 if not self.training else self.attention_dropout,
                        **kwargs,
                    )

                    attn_output = attn_output.reshape(*input_shape, -1).contiguous()
                    attn_output = attn_module.dense(attn_output)
                    return attn_output, attn_weights
                return forward

            module.forward = types.MethodType(make_forward(module, n_bits), module)
            count += 1

    print(f"Patched {count} attention layers for INT{n_bits} RTN KV quantization")
    return count


def evaluate_ppl(model, tokenizer, device="cuda", max_tokens=999999, max_length=512, fp16=False):
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
            with torch.amp.autocast("cuda", enabled=fp16):
                outputs = model(input_ids, use_cache=False)
                logits = outputs.logits
                shift_logits = logits[..., :-1, :].contiguous()
                shift_labels = input_ids[..., 1:].contiguous()
                loss = F.cross_entropy(shift_logits.view(-1, shift_logits.size(-1)), shift_labels.view(-1), reduction='sum')
            nlls.append(loss.item())
            total_predicted += shift_labels.numel()

    return math.exp(sum(nlls) / total_predicted)


def main():
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, required=True)
    parser.add_argument("--n_bits", type=int, required=True, choices=[4, 8],
                        help="Quantization bitwidth for KV cache")
    parser.add_argument("--analog_layers", type=str, default=None,
                        help="Layer indices to quantize (default: all)")
    parser.add_argument("--max_length", type=int, default=512)
    parser.add_argument("--output_dir", type=str, default="/home/lisq753/projects/HAT_kv107/paper2/results/remote107")
    parser.add_argument("--device", type=str, default="cuda")
    parser.add_argument("--fp16", action="store_true")
    args = parser.parse_args()

    dtype = torch.bfloat16 if args.fp16 else torch.float32
    print(f"Loading {args.model_name}...")
    model = AutoModelForCausalLM.from_pretrained(
        args.model_name, torch_dtype=dtype, use_safetensors=True, local_files_only=True
    )
    tokenizer = AutoTokenizer.from_pretrained(args.model_name, local_files_only=True)
    tokenizer.pad_token = tokenizer.eos_token
    model = model.to(args.device)

    target_layers = set(int(x) for x in args.analog_layers.split(",")) if args.analog_layers else None

    print(f"Patching attention for INT{args.n_bits} RTN KV quantization...")
    patch_attention_for_rtn_quantization(model, args.n_bits, target_layers)

    print(f"\nEvaluating PPL (INT{args.n_bits} RTN KV)...")
    ppl = evaluate_ppl(model, tokenizer, args.device, max_length=args.max_length, fp16=args.fp16)
    print(f"PPL: {ppl:.2f}")

    result = {
        "script": os.path.basename(__file__),
        "command": " ".join(sys.argv),
        "mode": "eval_quantized_baseline",
        "model": args.model_name,
        "dataset_eval": "wikitext-2-raw-v1 (test)",
        "n_bits": args.n_bits,
        "analog_layers": sorted(target_layers) if target_layers else list(range(model.config.num_hidden_layers)),
        "ctx_len": args.max_length,
        "stride": args.max_length,
        "batch_size": 1,
        "ppl": ppl,
        "wall_clock_time": time.time() - start_time,
    }

    out_file = os.path.join(
        args.output_dir,
        f"quant_baseline_{args.model_name.split('/')[-1]}_int{args.n_bits}_seed42.json"
    )
    os.makedirs(args.output_dir, exist_ok=True)
    with open(out_file, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"Saved: {out_file}")


if __name__ == "__main__":
    main()
