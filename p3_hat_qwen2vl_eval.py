"""
Minimal Qwen2-VL validation: clean vs analog KV generation quality.

Loads Qwen2-VL-2B-Instruct, monkey-patches Qwen2VLAttention for analog KV,
and compares generation output on a single image + prompt.

Usage:
    CUDA_VISIBLE_DEVICES=4 python p3_hat_qwen2vl_eval.py --image_path <path> --prompt "Describe this image."
"""

import os
import sys
import argparse
import time
import json

import torch
from PIL import Image

sys.path.insert(0, '/home/lisq753/projects/HAT/HAT')
from analog_layers import AnalogLinearConfig
from p3_hat_train import analogize_kv_tensor

# Default HF mirror
if not os.environ.get("HF_ENDPOINT"):
    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"


def load_model_for_eval(model_name, device="cuda", fp16=True):
    from transformers import Qwen2VLForConditionalGeneration, AutoProcessor

    dtype = torch.bfloat16 if fp16 else torch.float32
    print(f"Loading {model_name}...")
    model = Qwen2VLForConditionalGeneration.from_pretrained(
        model_name,
        torch_dtype=dtype,
        use_safetensors=True,
        local_files_only=True,
    )
    processor = AutoProcessor.from_pretrained(model_name, local_files_only=True)
    model = model.to(device)
    return model, processor


def patch_qwen2vl_for_hat(model, analog_cfg, analog_layers=None, max_length=512, d2d_seed=0xD2D):
    """Monkey-patch Qwen2VLAttention to inject analog KV noise."""
    import types
    import torch
    from transformers.models.qwen2_vl.modeling_qwen2_vl import apply_multimodal_rotary_pos_emb

    num_layers = model.config.num_hidden_layers
    target = analog_layers if analog_layers is not None else set(range(num_layers))
    count = 0

    # Pre-generate D2D noise for all target layers
    G_range = analog_cfg.G_max - analog_cfg.G_min
    sigma_d2d = analog_cfg.sigma_d2d * G_range

    for name, module in model.named_modules():
        if type(module).__name__ == 'Qwen2VLAttention':
            layer_idx = None
            for p in name.split('.'):
                if p.isdigit():
                    layer_idx = int(p)
                    break
            if layer_idx is None or layer_idx not in target:
                continue

            num_kv_heads = module.num_key_value_heads
            head_dim = module.head_dim
            shape = (1, num_kv_heads, max_length, head_dim)

            # Use per-layer seed for deterministic D2D patterns
            layer_seed = d2d_seed + layer_idx * 7919
            torch.manual_seed(layer_seed)
            module.register_buffer('_d2d_noise_k_pos', torch.randn(*shape) * sigma_d2d)
            module.register_buffer('_d2d_noise_k_neg', torch.randn(*shape) * sigma_d2d)
            module.register_buffer('_d2d_noise_v_pos', torch.randn(*shape) * sigma_d2d)
            module.register_buffer('_d2d_noise_v_neg', torch.randn(*shape) * sigma_d2d)

            original_forward = module.forward
            module._original_forward = original_forward

            def make_forward(attn_module, cfg):
                def forward(
                    hidden_states,
                    attention_mask=None,
                    position_ids=None,
                    past_key_values=None,
                    output_attentions=False,
                    use_cache=False,
                    position_embeddings=None,
                    **kwargs,
                ):
                    bsz, q_len, _ = hidden_states.size()

                    query_states = attn_module.q_proj(hidden_states)
                    key_states = attn_module.k_proj(hidden_states)
                    value_states = attn_module.v_proj(hidden_states)

                    query_states = query_states.view(bsz, q_len, -1, attn_module.head_dim).transpose(1, 2)
                    key_states = key_states.view(bsz, q_len, -1, attn_module.head_dim).transpose(1, 2)
                    value_states = value_states.view(bsz, q_len, -1, attn_module.head_dim).transpose(1, 2)

                    cos, sin = position_embeddings
                    query_states, key_states = apply_multimodal_rotary_pos_emb(
                        query_states, key_states, cos, sin,
                        attn_module.config.rope_parameters["mrope_section"]
                    )

                    if past_key_values is not None:
                        key_states, value_states = past_key_values.update(
                            key_states, value_states, attn_module.layer_idx
                        )

                    # === Analog KV injection ===
                    L = key_states.size(2)
                    buf_kp = getattr(attn_module, '_d2d_noise_k_pos', None)
                    buf_kn = getattr(attn_module, '_d2d_noise_k_neg', None)
                    buf_vp = getattr(attn_module, '_d2d_noise_v_pos', None)
                    buf_vn = getattr(attn_module, '_d2d_noise_v_neg', None)
                    d2d_kp = buf_kp[:, :, :L, :] if buf_kp is not None else None
                    d2d_kn = buf_kn[:, :, :L, :] if buf_kn is not None else None
                    d2d_vp = buf_vp[:, :, :L, :] if buf_vp is not None else None
                    d2d_vn = buf_vn[:, :, :L, :] if buf_vn is not None else None

                    key_states = analogize_kv_tensor(
                        key_states, cfg,
                        d2d_noise_pos=d2d_kp, d2d_noise_neg=d2d_kn
                    )
                    value_states = analogize_kv_tensor(
                        value_states, cfg,
                        d2d_noise_pos=d2d_vp, d2d_noise_neg=d2d_vn
                    )
                    # ===========================

                    from transformers.models.qwen2_vl.modeling_qwen2_vl import ALL_ATTENTION_FUNCTIONS, eager_attention_forward
                    attention_interface = ALL_ATTENTION_FUNCTIONS.get_interface(
                        attn_module.config._attn_implementation, eager_attention_forward
                    )
                    attn_output, attn_weights = attention_interface(
                        attn_module,
                        query_states,
                        key_states,
                        value_states,
                        attention_mask,
                        dropout=0.0 if not attn_module.training else attn_module.attention_dropout,
                        scaling=attn_module.scaling,
                        sliding_window=attn_module.sliding_window,
                        position_ids=position_ids,
                        **kwargs,
                    )

                    attn_output = attn_output.reshape(bsz, q_len, -1).contiguous()
                    attn_output = attn_module.o_proj(attn_output)
                    return attn_output, attn_weights, past_key_values if use_cache else None
                return forward

            module.forward = types.MethodType(make_forward(module, analog_cfg), module)
            count += 1

    print(f"Patched {count} Qwen2VLAttention layers for analog KV")
    return count


def generate(model, processor, image_path, prompt, device="cuda", max_new_tokens=128):
    from transformers import Qwen2VLForConditionalGeneration

    image = Image.open(image_path).convert("RGB")
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image_path},
                {"type": "text", "text": prompt},
            ],
        }
    ]
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = processor(text=[text], images=[image], return_tensors="pt", padding=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            top_p=None,
            temperature=None,
        )

    # Remove input tokens
    input_len = inputs["input_ids"].shape[1]
    generated_ids = outputs[:, input_len:]
    return processor.batch_decode(generated_ids, skip_special_tokens=True)[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, default="Qwen/Qwen2-VL-2B-Instruct")
    parser.add_argument("--image_path", type=str, required=True)
    parser.add_argument("--prompt", type=str, default="Describe this image in detail.")
    parser.add_argument("--analog", action="store_true", help="Enable analog KV noise")
    parser.add_argument("--n_states", type=int, default=256)
    parser.add_argument("--sigma_c2c", type=float, default=0.01)
    parser.add_argument("--sigma_d2d", type=float, default=0.02)
    parser.add_argument("--analog_layers", type=str, default=None)
    parser.add_argument("--d2d-seed", type=int, default=0xD2D, dest="d2d_seed")
    parser.add_argument("--max_length", type=int, default=512)
    parser.add_argument("--max_new_tokens", type=int, default=128)
    parser.add_argument("--device", type=str, default="cuda")
    parser.add_argument("--fp16", action="store_true", default=True)
    parser.add_argument("--output_dir", type=str, default="/home/lisq753/projects/HAT_kv107/paper2/results/remote107")
    args = parser.parse_args()

    # Load model
    model, processor = load_model_for_eval(args.model_name, device=args.device, fp16=args.fp16)

    # Determine analog layers
    analog_layers = None
    if args.analog_layers:
        analog_layers = set(int(x) for x in args.analog_layers.split(","))

    # Clean generation
    print("\n=== CLEAN generation ===")
    start = time.time()
    clean_text = generate(model, processor, args.image_path, args.prompt, device=args.device, max_new_tokens=args.max_new_tokens)
    clean_time = time.time() - start
    print(clean_text)
    print(f"Time: {clean_time:.1f}s")

    # Analog generation (if requested)
    analog_text = None
    analog_time = None
    if args.analog:
        print("\n=== ANALOG generation ===")
        analog_cfg = AnalogLinearConfig(
            n_states=args.n_states,
            sigma_c2c=args.sigma_c2c,
            sigma_d2d=args.sigma_d2d,
        )
        patch_qwen2vl_for_hat(
            model, analog_cfg, analog_layers,
            max_length=args.max_length, d2d_seed=args.d2d_seed
        )

        start = time.time()
        analog_text = generate(model, processor, args.image_path, args.prompt, device=args.device, max_new_tokens=args.max_new_tokens)
        analog_time = time.time() - start
        print(analog_text)
        print(f"Time: {analog_time:.1f}s")

    # Save result
    result = {
        "model": args.model_name,
        "image": args.image_path,
        "prompt": args.prompt,
        "clean_output": clean_text,
        "clean_time": clean_time,
        "analog": args.analog,
        "analog_output": analog_text,
        "analog_time": analog_time,
        "sigma_c2c": args.sigma_c2c if args.analog else None,
        "sigma_d2d": args.sigma_d2d if args.analog else None,
        "n_states": args.n_states if args.analog else None,
        "analog_layers": sorted(analog_layers) if analog_layers else list(range(model.config.num_hidden_layers)),
        "d2d_seed": args.d2d_seed if args.analog else None,
    }
    out_file = os.path.join(
        args.output_dir,
        f"qwen2vl_{args.model_name.split('/')[-1]}_{os.path.basename(args.image_path).split('.')[0]}.json"
    )
    os.makedirs(args.output_dir, exist_ok=True)
    with open(out_file, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\nSaved: {out_file}")


if __name__ == "__main__":
    main()
