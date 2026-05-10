#!/usr/bin/env python3
"""Shared Tiny-ViT hybrid-mapping utilities.

Keeps the Tiny-ViT analog/digital split consistent across:
  - model profiling
  - hybrid model conversion
  - dry-run / energy estimation
"""

import math
from typing import Tuple

import torch.nn as nn


ARRAY_SIZE = 128
DIFF_PAIR_MULTIPLIER = 2

TINYVIT_ANALOG_LINEAR_PATTERNS = (
    ".attn.qkv",
    ".attn.proj",
    ".mlp.fc1",
    ".mlp.fc2",
)

TINYVIT_ANALOG_CONV_NAMES = (
    "patch_embed.conv1.conv",
    "patch_embed.conv2.conv",
)


def is_depthwise_conv(module: nn.Module) -> bool:
    """Return True when a Conv2d is depthwise."""
    return (
        isinstance(module, nn.Conv2d)
        and module.groups == module.in_channels
        and module.groups > 1
    )


def is_tinyvit_analog_module(name: str, module: nn.Module) -> bool:
    """Return True when a Tiny-ViT module should map to analog crossbars."""
    if isinstance(module, nn.Linear):
        return any(pattern in name for pattern in TINYVIT_ANALOG_LINEAR_PATTERNS)

    if isinstance(module, nn.Conv2d):
        return name in TINYVIT_ANALOG_CONV_NAMES and not is_depthwise_conv(module)

    return False


def classify_tinyvit_layer(name: str, module: nn.Module) -> str:
    """Classify a Tiny-ViT layer into analog or digital domain."""
    return "analog" if is_tinyvit_analog_module(name, module) else "digital"


def crossbar_shape(module: nn.Module) -> Tuple[int, int]:
    """Return effective (M, N) crossbar shape for Linear/Conv2d modules."""
    if isinstance(module, nn.Linear):
        return module.out_features, module.in_features

    if isinstance(module, nn.Conv2d):
        k_h, k_w = module.kernel_size
        n = (module.in_channels // module.groups) * k_h * k_w
        return module.out_channels, n

    raise TypeError(f"Unsupported module type for crossbar shape: {type(module)!r}")


def crossbar_array_count(m: int, n: int, array_size: int = ARRAY_SIZE) -> Tuple[int, int, int]:
    """Return (row_tiles, col_tiles, diff-pair array count)."""
    row_tiles = math.ceil(m / array_size)
    col_tiles = math.ceil(n / array_size)
    arrays_single = row_tiles * col_tiles
    return row_tiles, col_tiles, arrays_single * DIFF_PAIR_MULTIPLIER
