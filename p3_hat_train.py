"""
HAT Training for LLM Analog KV Cache (Pythia-410m + WikiText-2)

Monkey-patches GPTNeoXAttention to inject analog KV noise during training.
All operations are differentiable (STE quantization + C2C noise).
"""

import math
import os
import sys
import json
import argparse
import types
from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import AdamW
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset
from tqdm import tqdm

sys.path.insert(0, '/home/lisq753/projects/HAT/HAT')
from analog_kv_cache import AnalogKVCacheConfig
from analog_layers import AnalogLinearConfig


def analogize_kv_tensor(x: torch.Tensor, analog_cfg: AnalogLinearConfig,
                          d2d_noise_pos: torch.Tensor = None,
                          d2d_noise_neg: torch.Tensor = None,
                          clamp_r: float = 1e6,
                          retention_step_time: float = 0.0) -> torch.Tensor:
    """Differentiable analog KV injection in conductance domain.

    Physical model:
      - KV values mapped to differential conductance pair (G_pos, G_neg)
      - STE quantization applied at write time
      - D2D noise: fixed per-cell offset in conductance domain (two independent
        crossbars for pos/neg, noise added before differential read)
      - C2C noise: random per-read noise in conductance domain (independent
        per-leg, re-sampled each forward pass)
      - Retention: double-exponential decay applied per token position.
        Token at position i has age = (L-1-i) * retention_step_time.
      - Differential read: W_eff = (G_pos + noise_pos) - (G_neg + noise_neg)
      - Recovery: x_analog = W_eff * (scale / G_range)

    Args:
        x: [B, H, L, D] key or value states
        analog_cfg: device physics config (respects noise_enabled, noise_mode,
                     retention_enabled, tau_1, tau_2, A_0)
        d2d_noise_pos: [1, H, L, D] fixed D2D noise for positive leg
        d2d_noise_neg: [1, H, L, D] fixed D2D noise for negative leg
        clamp_r: clamp range (matches kv_clamp_range)
        retention_step_time: seconds per token position for age computation.
                             0.0 = retention disabled.

    Returns:
        x_analog: [B, H, L, D] analogized tensor with gradients preserved
    """
    B = x.shape[0]
    x_fp32 = x.float().clamp(-clamp_r, clamp_r)

    # Per-head scale (each head has independent dynamic range)
    scale = x_fp32.abs().amax(dim=(-2, -1), keepdim=True) + 1e-8  # [B, H, 1, 1]
    x_norm = x_fp32 / scale
    x_pos = torch.clamp(x_norm, min=0.0)
    x_neg = torch.clamp(-x_norm, min=0.0)

    G_range = analog_cfg.G_max - analog_cfg.G_min
    G_pos = analog_cfg.G_min + x_pos * G_range
    G_neg = analog_cfg.G_min + x_neg * G_range

    # STE quantization (write process)
    n_states = analog_cfg.n_states
    if n_states >= 2:
        def _ste_q(g):
            g_q = torch.round((g - analog_cfg.G_min) / G_range * (n_states - 1))
            g_q = g_q / (n_states - 1) * G_range + analog_cfg.G_min
            return g + (g_q - g).detach()
        G_pos = _ste_q(G_pos)
        G_neg = _ste_q(G_neg)

    # Retention decay (double-exponential, per token position)
    # Older tokens (earlier in sequence) have been stored longer → more decay.
    if retention_step_time > 0 and analog_cfg.retention_enabled and analog_cfg.A_0 < 1.0:
        L = x.size(2)
        device = x.device
        # age[i] = (L - 1 - i) * retention_step_time  — last token is newest
        ages = torch.arange(L - 1, -1, -1, device=device, dtype=torch.float32) * retention_step_time
        age_shape = (1, 1, L, 1)  # broadcast over [B, H, L, D]
        ages = ages.view(*age_shape)
        A_1 = (1.0 - analog_cfg.A_0) / 2.0
        A_2 = A_1
        decay = A_1 * torch.exp(-ages / analog_cfg.tau_1) + A_2 * torch.exp(-ages / analog_cfg.tau_2) + analog_cfg.A_0
        # G decayed = G_min + (G - G_min) * decay
        G_pos = analog_cfg.G_min + (G_pos - analog_cfg.G_min) * decay
        G_neg = analog_cfg.G_min + (G_neg - analog_cfg.G_min) * decay

    # D2D noise in conductance domain (fixed per cell, different for pos/neg crossbars)
    if analog_cfg.noise_enabled and d2d_noise_pos is not None and d2d_noise_neg is not None:
        G_pos = G_pos + d2d_noise_pos
        G_neg = G_neg + d2d_noise_neg

    # Differential read
    W_eff = G_pos - G_neg

    # C2C noise (re-sampled per read) in conductance domain
    if analog_cfg.noise_enabled and analog_cfg.sigma_c2c > 0:
        if analog_cfg.noise_mode == "uniform":
            # Per-leg std = sigma_c2c * G_range / sqrt(2), so differential pair
            # gives total C2C std = sigma_c2c * G_range (matching the config spec)
            per_leg_std = analog_cfg.sigma_c2c * G_range / (2 ** 0.5)
            noise_c2c_pos = torch.randn_like(G_pos) * per_leg_std
            noise_c2c_neg = torch.randn_like(G_neg) * per_leg_std
        else:  # proportional: noise scales with |G_current|
            # NOTE: In proportional mode, sigma_c2c is a noise-to-signal ratio, NOT
            # an absolute standard deviation. The effective noise std varies with
            # signal: zero signal → zero noise, full-range signal → σ_c2c × |G| / √2.
            # This differs from uniform mode where σ_c2c is a fixed absolute std.
            per_leg_std = analog_cfg.sigma_c2c / (2 ** 0.5)
            noise_c2c_pos = torch.randn_like(G_pos) * G_pos.abs() * per_leg_std
            noise_c2c_neg = torch.randn_like(G_neg) * G_neg.abs() * per_leg_std
        W_eff = (G_pos + noise_c2c_pos) - (G_neg + noise_c2c_neg)

    # Recovery from conductance domain to output space
    recover_scale = scale / G_range  # [B, H, 1, 1]
    x_analog = W_eff * recover_scale

    return x_analog.to(x.dtype)


def patch_model_for_hat(model, analog_cfg: AnalogLinearConfig,
                         analog_layers: Optional[set] = None, max_length: int = 512,
                         retention_step_time: float = 0.0, d2d_seed: int = 0xD2D):
    """Monkey-patch model attention layers to inject analog KV noise.

    Args:
        model: causal LM model
        analog_cfg: device physics config
        analog_layers: set of layer indices to patch (None = all)
        max_length: max sequence length for D2D noise buffer sizing
        d2d_seed: base seed for D2D noise pattern (per-layer seed = d2d_seed + layer_idx)
    """
    num_layers = model.config.num_hidden_layers
    target_layers = analog_layers if analog_layers is not None else set(range(num_layers))

    G_range = analog_cfg.G_max - analog_cfg.G_min
    count = 0
    for name, module in model.named_modules():
        if 'attention' in name.lower() and hasattr(module, 'forward') and type(module).__name__ == 'GPTNeoXAttention':
            # Extract layer index from name (e.g., "layers.5.attention" -> 5)
            layer_idx = None
            parts = name.split('.')
            for i, p in enumerate(parts):
                if p.isdigit():
                    layer_idx = int(p)
                    break

            if layer_idx is not None and layer_idx in target_layers:
                original_forward = module.forward
                module._original_forward = original_forward
                module._analog_cfg = analog_cfg
                module._layer_idx = layer_idx
                module._retention_step_time = retention_step_time

                # Pre-generate fixed D2D noise buffers in conductance domain (pos + neg legs)
                # Per-leg std = sigma_d2d * G_range / sqrt(2), so differential pair
                # gives total D2D std = sigma_d2d * G_range (matching the config spec)
                num_heads = model.config.num_attention_heads
                head_size = module.head_size
                if analog_cfg.noise_enabled and analog_cfg.sigma_d2d > 0:
                    per_leg_std = analog_cfg.sigma_d2d * G_range / (2 ** 0.5)
                    # Deterministic D2D seed per layer: d2d_seed + layer_idx.
                    # D2D is a manufacturing offset (device-instance-specific), separate
                    # from the training seed. Same d2d_seed → identical pattern.
                    with torch.random.fork_rng():
                        torch.manual_seed(d2d_seed + layer_idx)
                        module.register_buffer(
                            '_d2d_noise_k_pos',
                            torch.randn(1, num_heads, max_length, head_size, device=model.device) * per_leg_std
                        )
                        module.register_buffer(
                            '_d2d_noise_k_neg',
                            torch.randn(1, num_heads, max_length, head_size, device=model.device) * per_leg_std
                        )
                        module.register_buffer(
                            '_d2d_noise_v_pos',
                            torch.randn(1, num_heads, max_length, head_size, device=model.device) * per_leg_std
                        )
                        module.register_buffer(
                            '_d2d_noise_v_neg',
                            torch.randn(1, num_heads, max_length, head_size, device=model.device) * per_leg_std
                        )
                else:
                    module.register_buffer('_d2d_noise_k_pos', None)
                    module.register_buffer('_d2d_noise_k_neg', None)
                    module.register_buffer('_d2d_noise_v_pos', None)
                    module.register_buffer('_d2d_noise_v_neg', None)

                def make_forward(attn_module, cfg):
                    def forward(self, hidden_states, attention_mask, layer_past=None, position_embeddings=None, **kwargs):
                        from transformers.models.gpt_neox.modeling_gpt_neox import apply_rotary_pos_emb

                        input_shape = hidden_states.shape[:-1]
                        hidden_shape = (*input_shape, -1, 3 * attn_module.head_size)
                        qkv = attn_module.query_key_value(hidden_states).view(hidden_shape).transpose(1, 2)
                        query_states, key_states, value_states = qkv.chunk(3, dim=-1)

                        cos, sin = position_embeddings
                        query_states, key_states = apply_rotary_pos_emb(query_states, key_states, cos, sin)

                        if layer_past is not None:
                            key_states, value_states = layer_past.update(key_states, value_states, attn_module.layer_idx)

                        # === Analog KV injection in conductance domain ===
                        L = key_states.size(2)
                        buf_kp = getattr(attn_module, '_d2d_noise_k_pos', None)
                        buf_kn = getattr(attn_module, '_d2d_noise_k_neg', None)
                        buf_vp = getattr(attn_module, '_d2d_noise_v_pos', None)
                        buf_vn = getattr(attn_module, '_d2d_noise_v_neg', None)
                        if buf_kp is not None and L > buf_kp.size(2):
                            raise ValueError(
                                f"Sequence length {L} exceeds D2D buffer size {buf_kp.size(2)}. "
                                f"Re-run with --max_length >= {L}."
                            )
                        d2d_kp = buf_kp[:, :, :L, :] if buf_kp is not None else None
                        d2d_kn = buf_kn[:, :, :L, :] if buf_kn is not None else None
                        d2d_vp = buf_vp[:, :, :L, :] if buf_vp is not None else None
                        d2d_vn = buf_vn[:, :, :L, :] if buf_vn is not None else None
                        key_states = analogize_kv_tensor(key_states, cfg,
                            d2d_noise_pos=d2d_kp, d2d_noise_neg=d2d_kn,
                            retention_step_time=attn_module._retention_step_time)
                        value_states = analogize_kv_tensor(value_states, cfg,
                            d2d_noise_pos=d2d_vp, d2d_noise_neg=d2d_vn,
                            retention_step_time=attn_module._retention_step_time)
                        # =====================================================

                        # Use the model's configured attention interface (SDPA/eager)
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

                module.forward = types.MethodType(make_forward(module, analog_cfg), module)
                count += 1

    print(f"Patched {count} attention layers for HAT training")
    return count


def train_hat(
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
):
    """Run HAT training on WikiText-2."""
    optimizer = AdamW(model.parameters(), lr=lr, weight_decay=0.01)

    dataset = load_dataset("wikitext", "wikitext-2-raw-v1", split="train")
    text = "\n\n".join(dataset["text"])
    encodings = tokenizer(text, return_tensors="pt")
    seq_len = encodings.input_ids.size(1)

    model.train()
    step = 0
    losses = []

    pbar = tqdm(total=max_steps, desc="HAT Training")
    for epoch in range(epochs):
        for begin_loc in range(0, seq_len - max_length, max_length // 2):
            end_loc = min(begin_loc + max_length, seq_len)
            input_ids = encodings.input_ids[:, begin_loc:end_loc].to(device)

            outputs = model(input_ids, use_cache=False)
            logits = outputs.logits

            # CLM loss
            shift_logits = logits[..., :-1, :].contiguous()
            shift_labels = input_ids[..., 1:].contiguous()
            loss = F.cross_entropy(shift_logits.view(-1, shift_logits.size(-1)), shift_labels.view(-1))
            loss = loss / grad_accum
            loss.backward()

            if (step + 1) % grad_accum == 0:
                optimizer.step()
                optimizer.zero_grad()

            losses.append(loss.item() * grad_accum)
            pbar.update(1)
            pbar.set_postfix({"loss": f"{losses[-1]:.3f}", "avg": f"{sum(losses[-10:])/len(losses[-10:]):.3f}"})

            step += 1
            if step >= max_steps:
                break
        if step >= max_steps:
            break

    pbar.close()
    return losses


def evaluate_ppl(model, tokenizer, device="cuda", max_tokens=999999, max_length=512):
    """Quick PPL eval on WikiText-2 test."""
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
            outputs = model(input_ids, use_cache=False)
            logits = outputs.logits
            shift_logits = logits[..., :-1, :].contiguous()
            shift_labels = input_ids[..., 1:].contiguous()
            loss = F.cross_entropy(shift_logits.view(-1, shift_logits.size(-1)), shift_labels.view(-1), reduction='sum')
            nlls.append(loss.item())
            total_predicted += shift_labels.numel()

    return math.exp(sum(nlls) / total_predicted)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, default="hat_warmup")
    parser.add_argument("--n_states", type=int, default=256)
    parser.add_argument("--sigma_c2c", type=float, default=0.01)
    parser.add_argument("--sigma_d2d", type=float, default=0.0)
    parser.add_argument("--epochs", type=int, default=1)
    parser.add_argument("--lr", type=float, default=1e-5)
    parser.add_argument("--max_length", type=int, default=512)
    parser.add_argument("--max_steps", type=int, default=100)
    parser.add_argument("--analog_layers", type=str, default=None)
    parser.add_argument("--seed", type=int, default=42, help="Training seed (model init, data order)")
    parser.add_argument("--d2d-seed", type=int, default=0xD2D, dest="d2d_seed",
                        help="D2D noise pattern seed (device-instance identifier, default 0xD2D=53714)")
    parser.add_argument("--retention_step_time", type=float, default=0.0,
                        help="Retention decay step time in seconds per token position. "
                             "0.0 = retention disabled. Requires analog_cfg.retention_enabled=True.")
    parser.add_argument("--output_dir", type=str, default="/home/lisq753/projects/HAT_kv107/paper2/results/remote107")
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

    print("Loading Pythia-410m...")
    model = AutoModelForCausalLM.from_pretrained("EleutherAI/pythia-410m-deduped", torch_dtype=torch.float32)
    tokenizer = AutoTokenizer.from_pretrained("EleutherAI/pythia-410m-deduped")
    tokenizer.pad_token = tokenizer.eos_token
    model = model.to(device)

    print("Patching attention layers for analog KV...")
    patch_model_for_hat(model, analog_cfg, analog_layers,
                        max_length=args.max_length,
                        retention_step_time=args.retention_step_time,
                        d2d_seed=args.d2d_seed)

    print("\nPre-HAT PPL eval...")
    ppl_before = evaluate_ppl(model, tokenizer, device, max_length=args.max_length)
    print(f"PPL before HAT: {ppl_before:.2f}")

    print("\nStarting HAT training...")
    losses = train_hat(
        model, tokenizer, analog_cfg,
        device=device, epochs=args.epochs, lr=args.lr,
        max_length=args.max_length, max_steps=args.max_steps,
    )

    print("\nPost-HAT PPL eval...")
    ppl_after = evaluate_ppl(model, tokenizer, device, max_length=args.max_length)
    print(f"PPL after HAT:  {ppl_after:.2f}")

    analog_layers_list = sorted(analog_layers) if analog_layers else list(range(model.config.num_hidden_layers))
    result = {
        "name": args.name,
        "train_seed": args.seed,
        "d2d_seed": args.d2d_seed,
        "n_states": args.n_states,
        "sigma_c2c": args.sigma_c2c,
        "sigma_d2d": args.sigma_d2d,
        "analog_layers": analog_layers_list,
        "lr": args.lr,
        "max_steps": args.max_steps,
        "retention_step_time": args.retention_step_time,
        "ppl_before": ppl_before,
        "ppl_after": ppl_after,
        "losses": losses,
    }

    # Save checkpoint for downstream noise-generalization eval
    ckpt_dir = os.path.join(args.output_dir, "checkpoints", f"{args.name}_seed{args.seed}")
    os.makedirs(ckpt_dir, exist_ok=True)
    model.save_pretrained(ckpt_dir)
    tokenizer.save_pretrained(ckpt_dir)

    # Persist hat_config.json alongside checkpoint so eval knows analog_layers + d2d_seed
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
        json.dump(result, f, indent=2)
    print(f"Result saved: {out_file}")


if __name__ == "__main__":
    main()
