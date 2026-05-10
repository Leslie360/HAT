#!/usr/bin/env python3
"""Shared AMP helpers for training and numerically sensitive ops."""

from contextlib import nullcontext

import torch


def get_device_type(device: str) -> str:
    return "cuda" if str(device).startswith("cuda") else "cpu"


def amp_enabled_for_device(enabled: bool, device: str) -> bool:
    return enabled and get_device_type(device) == "cuda" and torch.cuda.is_available()


def autocast_context(device: str, enabled: bool):
    if not amp_enabled_for_device(enabled, device):
        return nullcontext()
    return torch.amp.autocast(device_type=get_device_type(device), enabled=True)


def autocast_disabled_context(device_type: str):
    if device_type not in {"cuda", "cpu"}:
        return nullcontext()
    return torch.amp.autocast(device_type=device_type, enabled=False)


def create_grad_scaler(device: str, enabled: bool):
    device_type = get_device_type(device)
    return torch.amp.GradScaler(device=device_type, enabled=amp_enabled_for_device(enabled, device))
