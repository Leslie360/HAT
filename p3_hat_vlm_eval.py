"""
Minimal VLM validation: clean vs analog KV generation quality.

Supports Qwen2-VL and Qwen3-VL. Monkey-patches text decoder attention
for analog KV injection, and compares generation output on a single image + prompt.

Usage:
    CUDA_VISIBLE_DEVICES=4 python p3_hat_vlm_eval.py --model_name Qwen/Qwen3-VL-2B --image_path <path>
    CUDA_VISIBLE_DEVICES=4 python p3_hat_vlm_eval.py --model_name Qwen/Qwen2-VL-2B-Instruct --image_path <path> --analog
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

if not os.environ.get("HF_ENDPOINT"):
    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"


def detect_model_family(model_name):
    mn = model_name.lower()
    if "qwen3" in mn:
        return "qwen3"
    if "qwen2" in mn or "qwen-vl" in mn:
        return "qwen2"
    raise ValueError(f"Unsupported model: {model_name}. Use Qwen2-VL or Qwen3-VL.")


def load_model_for_eval(model_name, device="cuda", fp16=True):
    family = detect_model_family(model_name)
    dtype = torch.bfloat16 if fp16 else torch.float32
    print(f"Loading {model_name} (family={family})...")

    if family == "qwen3":
        from transformers import Qwen3VLForConditionalGeneration, AutoProcessor
        model_cls = Qwen3VLForConditionalGeneration
    else:
        from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
        model_cls = Qwen2VLForConditionalGeneration

    model = model_cls.from_pretrained(
        model_name,
        torch_dtype=dtype,
        use_safetensors=True,
        local_files_only=False,
    )
    processor = AutoProcessor.from_pretrained(model_name, local_files_only=False)
    model = model.to(device)
    return model, processor, family


def _register_d2d_buffers(module, num_kv_heads, head_dim, max_length, analog_cfg, layer_idx, d2d_seed):
    G_range = analog_cfg.G_max - analog_cfg.G_min
    sigma_d2d = analog_cfg.sigma_d2d * G_range
    shape = (1, num_kv_heads, max_length, head_dim)
    layer_seed = d2d_seed + layer_idx * 7919
    torch.manual_seed(layer_seed)
    module.register_buffer('_d2d_noise_k_pos', torch.randn(*shape, device=module.q_proj.weight.device) * sigma_d2d)
    module.register_buffer('_d2d_noise_k_neg', torch.randn(*shape, device=module.q_proj.weight.device) * sigma_d2d)
    module.register_buffer('_d2d_noise_v_pos', torch.randn(*shape, device=module.q_proj.weight.device) * sigma_d2d)
    module.register_buffer('_d2d_noise_v_neg', torch.randn(*shape, device=module.q_proj.weight.device) * sigma_d2d)


def patch_vlm_for_hat(model, analog_cfg, analog_layers=None, max_length=512, d2d_seed=0xD2D):
    """Monkey-patch VLM text decoder attention for analog KV noise."""
    import types
    family = detect_model_family(getattr(model, "name_or_path", ""))
    if not family:
        # fallback: inspect first attention module
        for m in model.modules():
            tn = type(m).__name__
            if "Qwen3VLTextAttention" in tn:
                family = "qwen3"
                break
            if "Qwen2VLAttention" in tn:
                family = "qwen2"
                break

    num_layers = model.config.num_hidden_layers
    target = analog_layers if analog_layers is not None else set(range(num_layers))
    count = 0

    for name, module in model.named_modules():
        mod_type = type(module).__name__
        if mod_type not in ("Qwen2VLAttention", "Qwen3VLTextAttention"):
            continue

        layer_idx = None
        for p in name.split('.'):
            if p.isdigit():
                layer_idx = int(p)
                break
        if layer_idx is None or layer_idx not in target:
            continue

        num_kv_heads = getattr(module, "num_key_value_heads", getattr(module, "num_heads", 1))
        head_dim = module.head_dim
        _register_d2d_buffers(module, num_kv_heads, head_dim, max_length, analog_cfg, layer_idx, d2d_seed)

        original_forward = module.forward
        module._original_forward = original_forward

        if family == "qwen3":
            from transformers.models.qwen3_vl.modeling_qwen3_vl import apply_rotary_pos_emb
            def make_forward(attn_module, cfg):
                def forward(
                    hidden_states,
                    position_embeddings,
                    attention_mask=None,
                    past_key_values=None,
                    **kwargs,
                ):
                    input_shape = hidden_states.shape[:-1]
                    hidden_shape = (*input_shape, -1, attn_module.head_dim)

                    query_states = attn_module.q_norm(attn_module.q_proj(hidden_states).view(hidden_shape)).transpose(1, 2)
                    key_states = attn_module.k_norm(attn_module.k_proj(hidden_states).view(hidden_shape)).transpose(1, 2)
                    value_states = attn_module.v_proj(hidden_states).view(hidden_shape).transpose(1, 2)

                    cos, sin = position_embeddings
                    query_states, key_states = apply_rotary_pos_emb(query_states, key_states, cos, sin)

                    if past_key_values is not None:
                        key_states, value_states = past_key_values.update(
                            key_states, value_states, attn_module.layer_idx
                        )

                    # === Analog KV injection ===
                    L = key_states.size(2)
                    d2d_kp = getattr(attn_module, '_d2d_noise_k_pos', None)
                    d2d_kn = getattr(attn_module, '_d2d_noise_k_neg', None)
                    d2d_vp = getattr(attn_module, '_d2d_noise_v_pos', None)
                    d2d_vn = getattr(attn_module, '_d2d_noise_v_neg', None)
                    if d2d_kp is not None:
                        d2d_kp, d2d_kn = d2d_kp[:, :, :L, :], d2d_kn[:, :, :L, :]
                        d2d_vp, d2d_vn = d2d_vp[:, :, :L, :], d2d_vn[:, :, :L, :]

                    key_states = analogize_kv_tensor(key_states, cfg, d2d_noise_pos=d2d_kp, d2d_noise_neg=d2d_kn)
                    value_states = analogize_kv_tensor(value_states, cfg, d2d_noise_pos=d2d_vp, d2d_noise_neg=d2d_vn)
                    # ===========================

                    from transformers.models.qwen3_vl.modeling_qwen3_vl import ALL_ATTENTION_FUNCTIONS, eager_attention_forward
                    attn_interface = ALL_ATTENTION_FUNCTIONS.get_interface(
                        attn_module.config._attn_implementation, eager_attention_forward
                    )
                    attn_output, attn_weights = attn_interface(
                        attn_module,
                        query_states,
                        key_states,
                        value_states,
                        attention_mask,
                        dropout=0.0 if not attn_module.training else attn_module.attention_dropout,
                        scaling=attn_module.scaling,
                        **kwargs,
                    )

                    attn_output = attn_output.reshape(*input_shape, -1).contiguous()
                    attn_output = attn_module.o_proj(attn_output)
                    return attn_output, attn_weights
                return forward
        else:
            from transformers.models.qwen2_vl.modeling_qwen2_vl import apply_multimodal_rotary_pos_emb
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
                    d2d_kp = getattr(attn_module, '_d2d_noise_k_pos', None)
                    d2d_kn = getattr(attn_module, '_d2d_noise_k_neg', None)
                    d2d_vp = getattr(attn_module, '_d2d_noise_v_pos', None)
                    d2d_vn = getattr(attn_module, '_d2d_noise_v_neg', None)
                    if d2d_kp is not None:
                        d2d_kp, d2d_kn = d2d_kp[:, :, :L, :], d2d_kn[:, :, :L, :]
                        d2d_vp, d2d_vn = d2d_vp[:, :, :L, :], d2d_vn[:, :, :L, :]

                    key_states = analogize_kv_tensor(key_states, cfg, d2d_noise_pos=d2d_kp, d2d_noise_neg=d2d_kn)
                    value_states = analogize_kv_tensor(value_states, cfg, d2d_noise_pos=d2d_vp, d2d_noise_neg=d2d_vn)
                    # ===========================

                    from transformers.models.qwen2_vl.modeling_qwen2_vl import ALL_ATTENTION_FUNCTIONS, eager_attention_forward
                    attn_interface = ALL_ATTENTION_FUNCTIONS.get_interface(
                        attn_module.config._attn_implementation, eager_attention_forward
                    )
                    attn_output, attn_weights = attn_interface(
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

    print(f"Patched {count} {family} attention layers for analog KV")
    return count


def generate(model, processor, image_path, prompt, device="cuda", max_new_tokens=128):
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

    input_len = inputs["input_ids"].shape[1]
    generated_ids = outputs[:, input_len:]
    return processor.batch_decode(generated_ids, skip_special_tokens=True)[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, default="Qwen/Qwen3-VL-2B")
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

    model, processor, family = load_model_for_eval(args.model_name, device=args.device, fp16=args.fp16)

    analog_layers = None
    if args.analog_layers:
        analog_layers = set(int(x) for x in args.analog_layers.split(","))

    print("\n=== CLEAN generation ===")
    start = time.time()
    clean_text = generate(model, processor, args.image_path, args.prompt, device=args.device, max_new_tokens=args.max_new_tokens)
    clean_time = time.time() - start
    print(clean_text)
    print(f"Time: {clean_time:.1f}s")

    analog_text = None
    analog_time = None
    if args.analog:
        print("\n=== ANALOG generation ===")
        analog_cfg = AnalogLinearConfig(
            n_states=args.n_states,
            sigma_c2c=args.sigma_c2c,
            sigma_d2d=args.sigma_d2d,
        )
        patch_vlm_for_hat(
            model, analog_cfg, analog_layers,
            max_length=args.max_length, d2d_seed=args.d2d_seed
        )

        start = time.time()
        analog_text = generate(model, processor, args.image_path, args.prompt, device=args.device, max_new_tokens=args.max_new_tokens)
        analog_time = time.time() - start
        print(analog_text)
        print(f"Time: {analog_time:.1f}s")

    result = {
        "model": args.model_name,
        "family": family,
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
        f"vlm_{family}_{args.model_name.split('/')[-1]}_{os.path.basename(args.image_path).split('.')[0]}.json"
    )
    os.makedirs(args.output_dir, exist_ok=True)
    with open(out_file, "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nSaved: {out_file}")


if __name__ == "__main__":
    main()
