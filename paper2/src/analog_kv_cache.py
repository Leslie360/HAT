"""Analog KV-cache primitive for Work 2.

This module models cached K/V tensors as analog storage: D2D mismatch is
persistent for a cache lifetime, while C2C noise is freshly sampled on each read.
It is deliberately standalone so behavior can be unit-tested before wiring into
Hugging Face attention internals.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

import torch
import torch.nn as nn


@dataclass
class AnalogKVCacheConfig:
    """Configuration for analog KV-cache reads and writes."""

    sigma_d2d: float = 0.10
    sigma_c2c: float = 0.05
    bit_width: int = 4
    quantize: bool = True
    noise_enabled: bool = True
    d2d_enabled: bool = True
    c2c_enabled: bool = True
    eps: float = 1e-8

    def __post_init__(self) -> None:
        if self.sigma_d2d < 0 or self.sigma_c2c < 0:
            raise ValueError("noise sigmas must be non-negative")
        if self.bit_width < 1:
            raise ValueError("bit_width must be >= 1")


class AnalogKVCache(nn.Module):
    """Per-layer analog KV-cache with persistent D2D and fresh C2C noise.

    Shape convention follows common decoder caches:
    `(batch, num_heads, seq_len, head_dim)`.

    `write()` accepts K/V for one token with shape `(batch, heads, head_dim)` or
    `(batch, heads, 1, head_dim)`. `read()` returns a prefix or range of cached
    values with analog noise applied at read time.
    """

    def __init__(
        self,
        layer_idx: int,
        num_heads: int,
        head_dim: int,
        max_seq_len: int,
        batch_size: int = 1,
        config: Optional[AnalogKVCacheConfig] = None,
        device: Optional[torch.device] = None,
        dtype: Optional[torch.dtype] = None,
    ) -> None:
        super().__init__()
        if layer_idx < 0:
            raise ValueError("layer_idx must be non-negative")
        if num_heads <= 0 or head_dim <= 0 or max_seq_len <= 0 or batch_size <= 0:
            raise ValueError("num_heads, head_dim, max_seq_len, and batch_size must be positive")

        self.layer_idx = int(layer_idx)
        self.num_heads = int(num_heads)
        self.head_dim = int(head_dim)
        self.max_seq_len = int(max_seq_len)
        self.config = config if config is not None else AnalogKVCacheConfig()
        self._batch_size = int(batch_size)

        factory = {"device": device, "dtype": dtype or torch.float32}
        shape = (batch_size, num_heads, max_seq_len, head_dim)
        self.register_buffer("k_cache", torch.zeros(shape, **factory), persistent=False)
        self.register_buffer("v_cache", torch.zeros(shape, **factory), persistent=False)
        self.register_buffer("d2d_k", torch.zeros(shape, **factory), persistent=False)
        self.register_buffer("d2d_v", torch.zeros(shape, **factory), persistent=False)
        self.register_buffer("valid_length", torch.zeros((), dtype=torch.long, device=device), persistent=False)
        self.resample_d2d()

    @property
    def batch_size(self) -> int:
        return self._batch_size

    def reset(
        self,
        batch_size: Optional[int] = None,
        device: Optional[torch.device] = None,
        dtype: Optional[torch.dtype] = None,
        resample_d2d: bool = True,
    ) -> None:
        """Clear cache storage, optionally resizing batch/device/dtype."""
        batch_size = int(batch_size or self._batch_size)
        if batch_size <= 0:
            raise ValueError("batch_size must be positive")
        device = device or self.k_cache.device
        dtype = dtype or self.k_cache.dtype
        shape = (batch_size, self.num_heads, self.max_seq_len, self.head_dim)

        self.k_cache = torch.zeros(shape, device=device, dtype=dtype)
        self.v_cache = torch.zeros(shape, device=device, dtype=dtype)
        self.d2d_k = torch.zeros(shape, device=device, dtype=dtype)
        self.d2d_v = torch.zeros(shape, device=device, dtype=dtype)
        self.valid_length = torch.zeros((), dtype=torch.long, device=device)
        self._batch_size = batch_size
        if resample_d2d:
            self.resample_d2d()

    def resample_d2d(self) -> None:
        """Draw a new persistent D2D mask for this cache lifetime."""
        cfg = self.config
        if not cfg.noise_enabled or not cfg.d2d_enabled or cfg.sigma_d2d == 0:
            self.d2d_k.zero_()
            self.d2d_v.zero_()
            return
        self.d2d_k.normal_(mean=0.0, std=cfg.sigma_d2d)
        self.d2d_v.normal_(mean=0.0, std=cfg.sigma_d2d)

    def write(self, token_idx: int, k_token: torch.Tensor, v_token: torch.Tensor) -> None:
        """Store one token's K/V vectors into the cache."""
        if token_idx < 0 or token_idx >= self.max_seq_len:
            raise IndexError(f"token_idx {token_idx} outside [0, {self.max_seq_len})")
        k_token = self._normalize_token_shape(k_token, "k_token")
        v_token = self._normalize_token_shape(v_token, "v_token")
        if k_token.shape != v_token.shape:
            raise ValueError(f"K/V token shapes differ: {tuple(k_token.shape)} vs {tuple(v_token.shape)}")
        if k_token.shape[1:] != (self.num_heads, self.head_dim):
            raise ValueError(
                f"expected token shape (*, {self.num_heads}, {self.head_dim}), got {tuple(k_token.shape)}"
            )
        if k_token.shape[0] != self.batch_size or k_token.device != self.k_cache.device or k_token.dtype != self.k_cache.dtype:
            self.reset(batch_size=k_token.shape[0], device=k_token.device, dtype=k_token.dtype, resample_d2d=True)

        self.k_cache[:, :, token_idx, :] = self._quantize(k_token)
        self.v_cache[:, :, token_idx, :] = self._quantize(v_token)
        self.valid_length.fill_(max(int(self.valid_length.item()), token_idx + 1))

    def read(
        self,
        end_pos: Optional[int] = None,
        start_pos: int = 0,
        generator: Optional[torch.Generator] = None,
    ) -> Tuple[torch.Tensor, torch.Tensor]:
        """Read a cache range with analog D2D/C2C effects applied."""
        valid = int(self.valid_length.item())
        end_pos = valid if end_pos is None else int(end_pos)
        start_pos = int(start_pos)
        if start_pos < 0 or end_pos < start_pos or end_pos > valid:
            raise IndexError(f"invalid read range [{start_pos}, {end_pos}) with valid_length={valid}")

        k = self.k_cache[:, :, start_pos:end_pos, :]
        v = self.v_cache[:, :, start_pos:end_pos, :]
        if not self.config.noise_enabled:
            return k.clone(), v.clone()

        d2d_k = self.d2d_k[:, :, start_pos:end_pos, :]
        d2d_v = self.d2d_v[:, :, start_pos:end_pos, :]
        k_read = k * (1.0 + d2d_k)
        v_read = v * (1.0 + d2d_v)
        if self.config.c2c_enabled and self.config.sigma_c2c > 0:
            k_read = k_read + self._sample_c2c(k, generator)
            v_read = v_read + self._sample_c2c(v, generator)
        return k_read, v_read

    def read_token(self, token_idx: int, generator: Optional[torch.Generator] = None) -> Tuple[torch.Tensor, torch.Tensor]:
        """Read one token position with analog noise."""
        return self.read(end_pos=token_idx + 1, start_pos=token_idx, generator=generator)

    def _normalize_token_shape(self, token: torch.Tensor, name: str) -> torch.Tensor:
        if token.ndim == 4 and token.shape[2] == 1:
            token = token[:, :, 0, :]
        if token.ndim != 3:
            raise ValueError(f"{name} must have shape (batch, heads, dim) or (batch, heads, 1, dim)")
        return token

    def _quantize(self, x: torch.Tensor) -> torch.Tensor:
        cfg = self.config
        if not cfg.quantize:
            return x
        qmax = (2 ** (cfg.bit_width - 1)) - 1
        if qmax <= 0:
            return torch.zeros_like(x)
        scale = x.detach().abs().amax(dim=(-2, -1), keepdim=True).clamp_min(cfg.eps) / qmax
        return torch.round(x / scale).clamp(-qmax, qmax) * scale

    def _sample_c2c(self, stored: torch.Tensor, generator: Optional[torch.Generator]) -> torch.Tensor:
        cfg = self.config
        # Per-token/head scale keeps zero-valued cache slots from receiving large additive noise.
        scale = stored.detach().abs().mean(dim=-1, keepdim=True).clamp_min(cfg.eps)
        noise = torch.randn(
            stored.shape,
            device=stored.device,
            dtype=stored.dtype,
            generator=generator,
        )
        return noise * (cfg.sigma_c2c * scale)
