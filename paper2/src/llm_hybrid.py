"""Pythia/GPT-NeoX hybrid conversion helpers for Work 2.

This file intentionally avoids importing PyTorch at module import time. Functions
raise clear dependency errors when the W1 runtime dependencies are unavailable.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple


@dataclass(frozen=True)
class HybridMappingSummary:
    """Summary of selected modules for analog conversion."""

    qkv: Tuple[str, ...]
    attention_output: Tuple[str, ...]
    mlp: Tuple[str, ...]
    skipped: Tuple[str, ...]

    @property
    def analog_names(self) -> Tuple[str, ...]:
        return self.qkv + self.attention_output + self.mlp


def classify_pythia_linear(name: str) -> str:
    """Classify a GPT-NeoX/Pythia linear module by name.

    Returns one of: `qkv`, `attention_output`, `mlp`, or `digital`.
    """
    lowered = name.lower()
    if "query_key_value" in lowered or lowered.endswith(".qkv"):
        return "qkv"
    if ".attention.dense" in lowered or lowered.endswith("attention.dense"):
        return "attention_output"
    if "dense_h_to_4h" in lowered or "dense_4h_to_h" in lowered:
        return "mlp"
    return "digital"


def discover_pythia_linear_modules(model: object) -> HybridMappingSummary:
    """Return Pythia linear-module names selected for analog conversion."""
    torch_nn = _torch_nn()
    qkv: List[str] = []
    attention_output: List[str] = []
    mlp: List[str] = []
    skipped: List[str] = []

    for name, module in model.named_modules():
        if not isinstance(module, torch_nn.Linear):
            continue
        kind = classify_pythia_linear(name)
        if kind == "qkv":
            qkv.append(name)
        elif kind == "attention_output":
            attention_output.append(name)
        elif kind == "mlp":
            mlp.append(name)
        else:
            skipped.append(name)

    return HybridMappingSummary(
        qkv=tuple(qkv),
        attention_output=tuple(attention_output),
        mlp=tuple(mlp),
        skipped=tuple(skipped),
    )


def convert_pythia_to_hybrid(
    model: object,
    config: Optional[object] = None,
    include_qkv: bool = True,
    include_attention_output: bool = True,
    include_mlp: bool = True,
    verbose: bool = False,
) -> Tuple[object, HybridMappingSummary]:
    """Replace selected Pythia linear modules with Paper 1 `AnalogLinear`.

    The conversion is in-place and returns `(model, summary)`. Each replacement
    receives an independent shallow-copied config to avoid groupwise/config
    sharing artifacts.
    """
    torch_nn = _torch_nn()
    from analog_layers import AnalogLinear, AnalogLinearConfig

    analog_config = config if config is not None else AnalogLinearConfig()
    summary = discover_pythia_linear_modules(model)
    selected = set()
    if include_qkv:
        selected.update(summary.qkv)
    if include_attention_output:
        selected.update(summary.attention_output)
    if include_mlp:
        selected.update(summary.mlp)

    module_lookup = dict(model.named_modules())
    for name in sorted(selected, key=lambda item: item.count("."), reverse=True):
        module = module_lookup[name]
        if not isinstance(module, torch_nn.Linear):
            continue
        replacement = AnalogLinear(
            in_features=module.in_features,
            out_features=module.out_features,
            bias=module.bias is not None,
            config=copy.copy(analog_config),
        )
        replacement.to(device=module.weight.device, dtype=module.weight.dtype)
        replacement.weight.data.copy_(module.weight.data)
        if module.bias is not None and replacement.bias is not None:
            replacement.bias.data.copy_(module.bias.data)
        _set_module(model, name, replacement)
        if verbose:
            print(f"Replaced {name} -> AnalogLinear({module.in_features}, {module.out_features})")

    return model, summary


def _set_module(root: object, dotted_name: str, module: object) -> None:
    parent = root
    parts = dotted_name.split(".")
    for part in parts[:-1]:
        parent = getattr(parent, part)
    setattr(parent, parts[-1], module)


def _torch_nn():
    try:
        import torch.nn as nn
    except Exception as exc:  # pragma: no cover - dependency guard
        raise RuntimeError("PyTorch is required for Work 2 LLM hybrid conversion") from exc
    return nn
