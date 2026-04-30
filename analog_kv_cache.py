#!/usr/bin/env python3
"""
Analog KV Cache simulation for autoregressive inference on analog CIM.

Extends the HAT framework to model KV-cache storage non-idealities:
  - Quantization of KV activations to discrete conductance states
  - D2D noise (fixed per storage cell, manufacturing variation)
  - C2C noise (re-sampled on every read, read noise)
  - Retention drift (double-exponential decay, token-age-dependent)

The module is designed for two use cases:
  1. "Pseudo-decode" on ViT: feed image patches one-by-one, maintain KV cache,
     measure accuracy degradation vs. sequence length and retention params.
  2. Future extension to LLMs: the same AnalogKVCache can be plugged into
     autoregressive Transformer decode loops.
"""

import copy
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F

from analog_layers import (
    AnalogLinearConfig,
    EnergyProfiler,
    autocast_disabled_context,
    ste_quantize,
)


# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────

@dataclass
class AnalogKVCacheConfig:
    """Configuration for analog KV-cache storage simulation.

    Reuses the same device-physics parameters as AnalogLinearConfig
    (conductance range, quantization levels, noise, retention) so that
    weight and KV storage can be calibrated to the same fabrication process.
    """

    # Device physics (re-used from weight storage)
    analog_config: AnalogLinearConfig = field(default_factory=AnalogLinearConfig)

    # Batch and Cache capacity
    max_batch_size: int = 128        # Maximum batch size supported
    max_seq_len: int = 1024          # Maximum sequence length

    # K/V activation clamp range before conductance mapping.
    # Empirically, ViT attention outputs are within ~10× of weight magnitudes.
    kv_clamp_range: float = 10.0

    # Digital fallback: store KV in perfect FP32 (baseline)
    digital_mode: bool = False
    
    # Disable quantization for parity checking
    no_quantize: bool = False

    # Time per decode step (seconds). Each new token increments the age of
    # all previously cached tokens by this amount.
    decode_step_time: float = 1e-3   # 1 ms placeholder

    # Whether retention decay is state-dependent (high-conductance decays faster)
    state_dependent_retention: bool = False

    # Number of iterative write-verify cycles for programming KV to array
    write_verify_cycles: int = 1

    def __post_init__(self):
        if self.max_batch_size <= 0:
            raise ValueError(f"max_batch_size must be positive, got {self.max_batch_size}")
        if self.max_seq_len <= 0:
            raise ValueError(f"max_seq_len must be positive, got {self.max_seq_len}")
        if self.kv_clamp_range <= 0:
            raise ValueError(f"kv_clamp_range must be positive, got {self.kv_clamp_range}")


# ─────────────────────────────────────────────
# Core: Analog KV Cache
# ─────────────────────────────────────────────

class AnalogKVCache(nn.Module):
    """Analog KV-cache with non-ideal storage simulation.

    Stores Key and Value tensors in simulated analog crossbar arrays.
    Each token position has:
      - its own D2D noise pattern (fixed at cache creation, broadcast across batch)
      - a retention age that grows with decode steps
      - a write-scale factor to recover original float magnitude (per-sample)
    """

    def __init__(self, num_heads: int, head_dim: int, config: AnalogKVCacheConfig):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = head_dim
        self.config = config
        self.analog_cfg = config.analog_config

        max_batch = config.max_batch_size
        max_len = config.max_seq_len

        # Cached K/V effective weights: [max_batch, max_seq_len, num_heads, head_dim]
        # These are *conductance-domain* values (after quantization + D2D write).
        self.register_buffer("k_cache", torch.zeros(max_batch, max_len, num_heads, head_dim))
        self.register_buffer("v_cache", torch.zeros(max_batch, max_len, num_heads, head_dim))

        # D2D noise: fixed per cell, sampled once at cache creation.
        # Shared across batch (simulating the same physical array instance).
        if not config.digital_mode:
            G_range = self.analog_cfg.G_max - self.analog_cfg.G_min
            sigma = self.analog_cfg.sigma_d2d * G_range
            self.register_buffer("k_d2d_noise", torch.randn(max_len, num_heads, head_dim) * sigma)
            self.register_buffer("v_d2d_noise", torch.randn(max_len, num_heads, head_dim) * sigma)
        else:
            self.register_buffer("k_d2d_noise", torch.zeros(max_len, num_heads, head_dim))
            self.register_buffer("v_d2d_noise", torch.zeros(max_len, num_heads, head_dim))

        # Per-token age (seconds stored) and write-recovery scale
        self.register_buffer("token_ages", torch.zeros(max_batch, max_len))
        self.register_buffer("k_write_scale", torch.ones(max_batch, max_len))
        self.register_buffer("v_write_scale", torch.ones(max_batch, max_len))

        # Sequence length counter (not a buffer — pure Python state)
        self.cache_len: int = 0
        self.current_batch_size: int = 0

    # ── Public API ──

    def reset(self):
        """Clear cache and reset all state."""
        self.k_cache.zero_()
        self.v_cache.zero_()
        self.token_ages.zero_()
        self.k_write_scale.fill_(1.0)
        self.v_write_scale.fill_(1.0)
        self.cache_len = 0
        self.current_batch_size = 0

    @torch.no_grad()
    def write(self, k_new: torch.Tensor, v_new: torch.Tensor):
        """Write a new token's K and V for all batch elements into the analog cache.

        Args:
            k_new: [B, num_heads, 1, head_dim] or [B, num_heads, head_dim]
            v_new: [B, num_heads, 1, head_dim] or [B, num_heads, head_dim]

        Raises:
            RuntimeError: if cache is full or batch size exceeds capacity.
        """
        B = k_new.shape[0]
        if self.cache_len >= self.config.max_seq_len:
            raise RuntimeError(
                f"KV cache overflow: {self.cache_len} >= {self.config.max_seq_len}"
            )
        if B > self.config.max_batch_size:
            raise RuntimeError(
                f"Batch size overflow: {B} > {self.config.max_batch_size}"
            )
        
        # Track active batch size
        self.current_batch_size = B

        cfg = self.config
        k_new = _squeeze_token_dim(k_new)  # [B, num_heads, head_dim]
        v_new = _squeeze_token_dim(v_new)

        idx = self.cache_len

        if cfg.digital_mode:
            self.k_cache[:B, idx].copy_(k_new)
            self.v_cache[:B, idx].copy_(v_new)
            self.k_write_scale[:B, idx] = 1.0
            self.v_write_scale[:B, idx] = 1.0
        else:
            k_eff, k_scale = self._float_to_conductance(k_new) # k_eff: [B, H, D], k_scale: [B]
            v_eff, v_scale = self._float_to_conductance(v_new)

            # Add fixed D2D noise (broadcast across batch)
            k_eff = k_eff + self.k_d2d_noise[idx]
            v_eff = v_eff + self.v_d2d_noise[idx]

            self.k_cache[:B, idx].copy_(k_eff)
            self.v_cache[:B, idx].copy_(v_eff)
            self.k_write_scale[:B, idx].copy_(k_scale)
            self.v_write_scale[:B, idx].copy_(v_scale)

        # Age bookkeeping: existing tokens get older, new token starts at 0
        if idx > 0:
            self.token_ages[:B, :idx] += cfg.decode_step_time
        self.token_ages[:B, idx] = 0.0
        self.cache_len += 1

    @torch.no_grad()
    def read(self) -> Tuple[torch.Tensor, torch.Tensor]:
        """Read all cached K/V for the current batch with non-idealities.

        Returns:
            k, v: each [B, num_heads, cache_len, head_dim]
        """
        cfg = self.config
        B = self.current_batch_size
        L = self.cache_len

        if L == 0:
            device = self.k_cache.device
            empty = torch.zeros(B, self.num_heads, 0, self.head_dim, device=device)
            return empty, empty

        k = self.k_cache[:B, :L].clone()  # [B, L, H, D]
        v = self.v_cache[:B, :L].clone()

        if not cfg.digital_mode:
            with autocast_disabled_context(k.device.type):
                ages = self.token_ages[:B, :L]
                decay = self._retention_decay_vector(ages) # [B, L, 1, 1]
                k = k * decay
                v = v * decay

                # C2C read noise — inject in conductance domain BEFORE recovery
                if self.analog_cfg.sigma_c2c > 0:
                    G_range = self.analog_cfg.G_max - self.analog_cfg.G_min
                    sigma = self.analog_cfg.sigma_c2c * G_range
                    k = k + torch.randn_like(k) * sigma
                    v = v + torch.randn_like(v) * sigma

                # Recover float magnitude (per-sample scale)
                k_scale = self.k_write_scale[:B, :L].unsqueeze(-1).unsqueeze(-1) # [B, L, 1, 1]
                v_scale = self.v_write_scale[:B, :L].unsqueeze(-1).unsqueeze(-1)
                k = k * k_scale
                v = v * v_scale

        # [B, L, num_heads, head_dim] -> [B, num_heads, L, head_dim]
        k = k.transpose(1, 2)
        v = v.transpose(1, 2)
        return k, v

    # ── Internal helpers ──

    def _float_to_conductance(self, x: torch.Tensor):
        """Map batch of float KV values to quantized differential conductance.

        Args:
            x: [B, num_heads, head_dim]

        Returns:
            (W_eff, recover_scale) where:
              - W_eff: [B, num_heads, head_dim]
              - recover_scale: [B] (one scale per batch element)
        """
        cfg = self.analog_cfg
        clamp_r = self.config.kv_clamp_range
        B = x.shape[0]

        with autocast_disabled_context(x.device.type):
            x_fp32 = x.float().clamp(-clamp_r, clamp_r)
            # Per-sample scale calculation
            scale = x_fp32.reshape(B, -1).abs().amax(dim=-1).detach() + 1e-8 # [B]
            
            # Normalize to [-1, 1] using per-sample scale
            x_norm = x_fp32 / scale.view(B, 1, 1)
            x_pos = torch.clamp(x_norm, min=0.0)
            x_neg = torch.clamp(-x_norm, min=0.0)

            G_range = cfg.G_max - cfg.G_min
            G_pos = cfg.G_min + x_pos * G_range
            G_neg = cfg.G_min + x_neg * G_range

            if not self.config.no_quantize:
                G_pos = ste_quantize(
                    G_pos, cfg.n_states, cfg.G_min, cfg.G_max,
                    cfg.NL_LTP, cfg.NL_LTD, cfg.inl_table,
                    cfg.use_second_order_ste, cfg.delta_g_eff, cfg.second_order_alpha,
                )
                G_neg = ste_quantize(
                    G_neg, cfg.n_states, cfg.G_min, cfg.G_max,
                    cfg.NL_LTP, cfg.NL_LTD, cfg.inl_table,
                    cfg.use_second_order_ste, cfg.delta_g_eff, cfg.second_order_alpha,
                )

            W_eff = G_pos - G_neg
            recover_scale = scale / G_range # [B]
            return W_eff, recover_scale

    def _retention_decay_vector(self, ages: torch.Tensor) -> torch.Tensor:
        """Double-exponential decay factor for a tensor of ages.

        Args:
            ages: [B, L]

        Returns:
            decay: [B, L, 1, 1] broadcastable over [B, L, num_heads, head_dim]
        """
        cfg = self.analog_cfg
        if not cfg.retention_enabled or ages.max() <= 0:
            return torch.ones_like(ages).unsqueeze(-1).unsqueeze(-1)

        A_0 = cfg.A_0
        A_1 = (1.0 - A_0) / 2.0
        A_2 = A_1
        decay = A_1 * torch.exp(-ages / cfg.tau_1) + A_2 * torch.exp(-ages / cfg.tau_2) + A_0
        return decay.unsqueeze(-1).unsqueeze(-1)


# ─────────────────────────────────────────────
# Attention decode with analog KV cache
# ─────────────────────────────────────────────

def analog_attention_decode(
    q: torch.Tensor,
    kv_cache: AnalogKVCache,
    scale: Optional[float] = None,
) -> torch.Tensor:
    """Single decode-step scaled dot-product attention with vectorized analog KV cache.

    Args:
        q: [B, num_heads, 1, head_dim] — query for the current token only.
        kv_cache: AnalogKVCache instance holding previous tokens for the batch.
        scale: Attention temperature (default 1/sqrt(head_dim)).

    Returns:
        output: [B, num_heads, 1, head_dim]
    """
    if scale is None:
        scale = q.shape[-1] ** -0.5

    k, v = kv_cache.read()  # [B, num_heads, L, head_dim]

    # Empty cache: return zeros
    if k.shape[2] == 0:
        return torch.zeros_like(q)

    # q @ k^T  -> [B, num_heads, 1, L]
    scores = torch.matmul(q, k.transpose(-2, -1)) * scale
    attn = torch.softmax(scores, dim=-1)

    # attn @ v -> [B, num_heads, 1, head_dim]
    output = torch.matmul(attn, v)
    return output


# ─────────────────────────────────────────────
# ViT patch-by-patch "pseudo-decode" forward
# ─────────────────────────────────────────────

class ViTPatchByPatchDecoder(nn.Module):
    """Wrapper that runs a ViT model patch-by-patch with analog KV cache.

    Replaces the standard all-patches-at-once attention with a sequential
    decode loop where each patch is processed one at a time and KV states
    are maintained in an AnalogKVCache. This lets us measure how analog
    KV-storage non-idealities degrade classification accuracy as a function
    of image resolution (number of patches).

    Usage::

        model = timm.create_model("tiny_vit_5m_224", num_classes=10)
        model = convert_to_hybrid(model, config=AnalogLinearConfig())

        decoder = ViTPatchByPatchDecoder(model, kv_cache_config)
        logits = decoder(image)   # image: [B, 3, H, W]

    The wrapper intercepts the attention blocks inside the ViT and forces
    patch-by-patch decode while keeping all other layers (patch embed,
    MLP, LayerNorm, head) unchanged.
    """

    def __init__(
        self,
        vit_model: nn.Module,
        kv_config: AnalogKVCacheConfig,
        num_patches: Optional[int] = None,
    ):
        super().__init__()
        self.vit = vit_model
        self.kv_config = kv_config

        # Try to infer number of patches and heads from the model
        if num_patches is None:
            num_patches = self._infer_num_patches(vit_model)
        self.num_patches = num_patches

        # One KV cache per attention block (per-block head config discovered below)
        self.kv_caches: List[AnalogKVCache] = nn.ModuleList()
        self._block_indices: List[int] = []
        self._discover_attention_blocks()

        # Fallback head config (first block) — used only if a block does not expose num_heads
        if self.kv_caches:
            self.num_heads = self.kv_caches[0].num_heads
            self.head_dim = self.kv_caches[0].head_dim
        else:
            self.num_heads = 3
            self.head_dim = 64

    # ── Public forward ──

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Run ViT in patch-by-patch decode mode.

        Args:
            x: [B, 3, H, W] image tensor.

        Returns:
            logits: [B, num_classes]
        """
        # 1. Patch embedding (all patches at once — not autoregressive)
        x = self._extract_patch_embeddings(x)  # [B, N, D]

        # 2. Prepend CLS token if the model uses one
        if hasattr(self.vit, "cls_token"):
            B = x.shape[0]
            cls = self.vit.cls_token.expand(B, -1, -1)  # [B, 1, D]
            x = torch.cat([cls, x], dim=1)  # [B, 1+N, D]

        # 3. Add positional embedding if present (all-at-once, standard)
        if hasattr(self.vit, "pos_embed"):
            # pos_embed usually includes CLS position 0
            pe = self.vit.pos_embed
            if pe.shape[1] <= x.shape[1]:
                x = x + pe
            else:
                x = x + pe[:, : x.shape[1], :]

        # 4. Process through each block with patch-by-patch attention
        for block_idx, kv_cache in zip(self._block_indices, self.kv_caches):
            block = self._get_block(block_idx)
            x = self._decode_block(block, x, kv_cache)

        # 5. Final norm + classification head
        return self._head_forward(x)

    # ── Internal helpers ──

    def _infer_num_patches(self, model: nn.Module) -> int:
        """Infer number of spatial patches from a timm ViT."""
        # Common timm attribute
        if hasattr(model, "num_patches"):
            return int(model.num_patches)
        # Try patch_embed
        pe = getattr(model, "patch_embed", None)
        if pe is not None and hasattr(pe, "num_patches"):
            return int(pe.num_patches)
        # Fallback: assume 224x224 / 16 = 196 patches
        return 196

    def _flatten_blocks(self, model: nn.Module) -> List[nn.Module]:
        """Recursively find all transformer blocks in common timm architectures."""
        if hasattr(model, "blocks"):
            return list(model.blocks)
        if hasattr(model, "stages"):
            blocks = []
            for stage in model.stages:
                if hasattr(stage, "blocks"):
                    blocks.extend(list(stage.blocks))
            if blocks:
                return blocks
        for name in ("layers", "transformer", "encoder"):
            container = getattr(model, name, None)
            if container is not None:
                return list(container)
        raise RuntimeError(
            "Cannot find transformer blocks in model. "
            "Supported layouts: model.blocks (ViT/DeiT), model.stages[i].blocks (Tiny-ViT-like). "
            "Patch-by-patch decode currently only works with standard ViT/DeiT."
        )

    def _infer_block_head_shape(self, block: nn.Module) -> Tuple[int, int]:
        """Infer (num_heads, head_dim) from a single attention block."""
        attn = getattr(block, "attn", None)
        if attn is None:
            raise RuntimeError("Block has no 'attn' attribute")
        qkv = getattr(attn, "qkv", None)
        from analog_layers import AnalogLinear
        if not isinstance(qkv, (nn.Linear, AnalogLinear)):
            raise RuntimeError(
                f"Unsupported attention QKV: {type(qkv).__name__} (expected nn.Linear or AnalogLinear). "
                f"Windowed attention or grouped convolutions are not supported."
            )
        embed_dim = qkv.out_features // 3
        num_heads = getattr(attn, "num_heads", None)
        if num_heads is None:
            num_heads = 12 if embed_dim % 12 == 0 else 3
        head_dim = getattr(attn, "head_dim", None)
        if head_dim is None or head_dim == 0:
            head_dim = embed_dim // num_heads
        return num_heads, head_dim

    def _check_block_compatible(self, block: nn.Module) -> bool:
        """Check if a block can be used with patch-by-patch decode."""
        for attr in ("norm1", "norm2", "mlp", "attn"):
            if not hasattr(block, attr):
                return False
        attn = block.attn
        if not hasattr(attn, "qkv"):
            return False
        from analog_layers import AnalogLinear
        if not isinstance(attn.qkv, (nn.Linear, AnalogLinear)):
            return False
        return True

    def _get_block(self, idx: int):
        return self._flatten_blocks(self.vit)[idx]

    def _discover_attention_blocks(self):
        """Find all attention blocks and create matching KV caches."""
        blocks = self._flatten_blocks(self.vit)
        for idx, block in enumerate(blocks):
            if not self._check_block_compatible(block):
                raise RuntimeError(
                    f"Block {idx} ({type(block).__name__}) is not compatible with patch-by-patch decode. "
                    f"Required: norm1, attn.qkv (nn.Linear), norm2, mlp. "
                    f"Models with windowed attention, local_conv, or non-standard layouts "
                    f"(e.g. Tiny-ViT) are not yet supported."
                )
            num_heads, head_dim = self._infer_block_head_shape(block)
            kv = AnalogKVCache(
                num_heads=num_heads,
                head_dim=head_dim,
                config=copy.deepcopy(self.kv_config),
            )
            self.kv_caches.append(kv)
            self._block_indices.append(idx)

    def _extract_patch_embeddings(self, x: torch.Tensor) -> torch.Tensor:
        """Run patch_embed to get per-patch features."""
        pe = getattr(self.vit, "patch_embed", None)
        if pe is None:
            raise RuntimeError("Model has no patch_embed")
        # patch_embed usually returns [B, N, D]
        out = pe(x)
        if out.dim() == 4:
            # Some patch_embeds return [B, D, H', W']
            B, D, Hp, Wp = out.shape
            out = out.flatten(2).transpose(1, 2)  # [B, H'*W', D]
        return out


    def _decode_block(
        self,
        block: nn.Module,
        x: torch.Tensor,
        kv_cache: AnalogKVCache,
    ) -> torch.Tensor:
        """Run one transformer block in patch-by-patch decode mode.

        Standard block pattern (timm)::

            x = x + drop_path(attn(norm1(x)))
            x = x + drop_path(mlp(norm2(x)))

        We replace the attention with sequential decode over tokens while
        keeping the MLP, norms, and drop_path intact.
        """
        B, N, D = x.shape
        attn_module = block.attn
        norm1 = block.norm1
        norm2 = block.norm2
        mlp = block.mlp

        # Per-block head config (needed if blocks vary in head count)
        num_heads = getattr(attn_module, "num_heads", kv_cache.num_heads)
        head_dim = getattr(attn_module, "head_dim", None)
        if head_dim is None or head_dim == 0:
            head_dim = D // num_heads

        # --- Attention path (replaced with patch-by-patch decode) ---
        x_norm = norm1(x)  # [B, N, D]

        # Use the model's own QKV projection
        qkv = attn_module.qkv(x_norm)  # [B, N, 3*D]
        qkv = qkv.reshape(B, N, 3, num_heads, head_dim)
        qkv = qkv.permute(2, 0, 3, 1, 4)  # [3, B, heads, N, head_dim]
        q_all, k_all, v_all = qkv[0], qkv[1], qkv[2]

        kv_cache.reset()

        outputs = []
        for i in range(N):
            q_i = q_all[:, :, i:i + 1, :]  # [B, heads, 1, head_dim]
            # First token has no prior KV -> attend to empty cache (returns zero)
            # This is slightly different from standard ViT where all tokens
            # attend to all tokens simultaneously, but it is the correct
            # autoregressive semantics.
            out_i = analog_attention_decode(q_i, kv_cache, scale=attn_module.scale)
            outputs.append(out_i)

            # Cache this token's K/V for future tokens
            k_i = k_all[:, :, i:i + 1, :]
            v_i = v_all[:, :, i:i + 1, :]
            kv_cache.write(k_i, v_i)

        # Re-assemble attention output
        attn_out = torch.cat(outputs, dim=2)  # [B, heads, N, head_dim]
        attn_out = attn_out.transpose(1, 2).reshape(B, N, D)  # [B, N, D]
        attn_out = attn_module.proj(attn_out)
        if hasattr(attn_module, "proj_drop"):
            attn_out = attn_module.proj_drop(attn_out)

        ls1 = getattr(block, "ls1", None)
        if ls1 is not None:
            attn_out = ls1(attn_out)

        drop_path1 = getattr(block, "drop_path1", None) or getattr(block, "drop_path", None)
        if drop_path1 is not None:
            attn_out = drop_path1(attn_out)

        x = x + attn_out

        # --- MLP path (unchanged) ---
        mlp_out = mlp(norm2(x))

        ls2 = getattr(block, "ls2", None)
        if ls2 is not None:
            mlp_out = ls2(mlp_out)

        drop_path2 = getattr(block, "drop_path2", drop_path1)
        if drop_path2 is not None:
            mlp_out = drop_path2(mlp_out)
        x = x + mlp_out

        return x

    def _head_forward(self, x: torch.Tensor) -> torch.Tensor:
        """Run final norm and classification head.

        For ViT we typically use the CLS token (first position).
        If no CLS token is detected we fall back to mean pooling.
        """
        B = x.shape[0]

        # Detect CLS token: if the model has a cls_token buffer, x[0] is CLS
        if hasattr(self.vit, "cls_token"):
            x_head = x[:, 0]  # [B, D]
        else:
            x_head = x.mean(dim=1)  # [B, D]

        if hasattr(self.vit, "norm"):
            x_head = self.vit.norm(x_head)
        elif hasattr(self.vit, "norm_head"):
            x_head = self.vit.norm_head(x_head)

        if hasattr(self.vit, "head"):
            x_head = self.vit.head(x_head)
        elif hasattr(self.vit, "fc"):
            x_head = self.vit.fc(x_head)
        return x_head


# ─────────────────────────────────────────────
# Utilities
# ─────────────────────────────────────────────

def _squeeze_token_dim(t: torch.Tensor) -> torch.Tensor:
    """Remove singleton token dimension if present.

    Accepts [B, H, 1, D] -> [B, H, D]
              [B, H, D]   -> [B, H, D]
    """
    if t.dim() == 4 and t.shape[2] == 1:
        return t.squeeze(2)
    return t
