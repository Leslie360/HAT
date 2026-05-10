"""Hybrid calibration for organic CIM: block-output affine correction.

Given fresh-instance analog drift, collects reference (noise-off) and raw
analog activations on a small calibration set, then fits per-channel affine:
    y_cal = gamma * y_raw + beta

Usage:
    calibrator = BlockOutputCalibrator(calibration_samples=64)
    ref, raw = calibrator.collect_references(model, loader, device)
    calibrator.fit(ref, raw)
    # Then wrap model forward to apply calibration
"""
from __future__ import annotations

import json
from typing import Dict, List, Optional

import torch
import torch.nn as nn


class ActivationCapture:
    """Forward hook that captures layer outputs."""
    
    def __init__(self):
        self.outputs: List[torch.Tensor] = []
    
    def __call__(self, module, input, output):
        self.outputs.append(output.detach().cpu())
    
    def clear(self):
        self.outputs.clear()
    
    def get_concatenated(self) -> torch.Tensor:
        return torch.cat(self.outputs, dim=0)


class AffineCalibrator:
    """Fits per-channel affine transform: y_ref = gamma * y_raw + beta."""
    
    def __init__(self):
        self.gamma: Dict[str, torch.Tensor] = {}
        self.beta: Dict[str, torch.Tensor] = {}
        self._channel_dim: Dict[str, int] = {}
        self.fitted = False
    
    def fit(self, ref_outputs: Dict[str, torch.Tensor], raw_outputs: Dict[str, torch.Tensor]):
        """Fit affine transform for each target layer/block.
        
        Args:
            ref_outputs: {name: [N, ...] tensor} noise-off reference
            raw_outputs: {name: [N, ...] tensor} fresh analog
        """
        for name in ref_outputs.keys():
            if name not in raw_outputs:
                continue
            
            y_ref = ref_outputs[name]
            y_raw = raw_outputs[name]
            
            # Determine tensor layout and flatten to [N*spatial, C]
            if y_ref.dim() == 4:  # conv feature map
                # Heuristic: if last dim > dim1, likely [N, H, W, C] (channel-last)
                # otherwise [N, C, H, W] (channel-first)
                if y_ref.shape[-1] > y_ref.shape[1]:
                    # [N, H, W, C] -> [N*H*W, C]
                    y_ref = y_ref.reshape(-1, y_ref.shape[-1])
                    y_raw = y_raw.reshape(-1, y_raw.shape[-1])
                    self._channel_dim[name] = -1
                else:
                    # [N, C, H, W] -> [N*H*W, C]
                    y_ref = y_ref.permute(0, 2, 3, 1).reshape(-1, y_ref.shape[1])
                    y_raw = y_raw.permute(0, 2, 3, 1).reshape(-1, y_raw.shape[1])
                    self._channel_dim[name] = 1
            elif y_ref.dim() == 2:
                # [N, C]
                self._channel_dim[name] = 1
            else:
                y_ref = y_ref.reshape(y_ref.shape[0], -1)
                y_raw = y_raw.reshape(y_raw.shape[0], -1)
                self._channel_dim[name] = 1
            
            # Per-channel least squares
            eps = 1e-6
            mean_raw = y_raw.mean(dim=0)
            mean_ref = y_ref.mean(dim=0)
            var_raw = y_raw.var(dim=0, unbiased=False)
            cov = ((y_raw - mean_raw) * (y_ref - mean_ref)).mean(dim=0)
            
            gamma = cov / (var_raw + eps)
            beta = mean_ref - gamma * mean_raw
            
            self.gamma[name] = gamma
            self.beta[name] = beta
        
        self.fitted = True
        print(f"Affine calibration fitted for {len(self.gamma)} targets")
    
    def apply(self, name: str, output: torch.Tensor) -> torch.Tensor:
        """Apply fitted calibration to an output tensor."""
        if not self.fitted or name not in self.gamma:
            return output
        
        gamma = self.gamma[name].to(output.device)
        beta = self.beta[name].to(output.device)
        channel_dim = self._channel_dim.get(name, 1)
        
        # Handle different output shapes
        if output.dim() == 4:
            if channel_dim == -1 or channel_dim == 3:
                # [N, H, W, C]
                gamma = gamma.view(1, 1, 1, -1)
                beta = beta.view(1, 1, 1, -1)
            else:
                # [N, C, H, W]
                gamma = gamma.view(1, -1, 1, 1)
                beta = beta.view(1, -1, 1, 1)
        elif output.dim() == 2:  # [N, C]
            gamma = gamma.view(1, -1)
            beta = beta.view(1, -1)
        else:
            # Flatten and reshape
            orig_shape = output.shape
            output = output.reshape(output.shape[0], -1)
            gamma = gamma.view(1, -1)
            beta = beta.view(1, -1)
            calibrated = gamma * output + beta
            return calibrated.reshape(orig_shape)
        
        return gamma * output + beta
    
    def export(self, path: str):
        data = {
            'gamma': {k: v.cpu().tolist() for k, v in self.gamma.items()},
            'beta': {k: v.cpu().tolist() for k, v in self.beta.items()},
        }
        with open(path, 'w') as f:
            json.dump(data, f)
    
    def load(self, path: str):
        with open(path) as f:
            data = json.load(f)
        self.gamma = {k: torch.tensor(v) for k, v in data['gamma'].items()}
        self.beta = {k: torch.tensor(v) for k, v in data['beta'].items()}
        self.fitted = True


def disable_all_analog_noise(model: nn.Module):
    """Disable noise on all analog layers (for reference pass)."""
    saved = []
    for m in model.modules():
        if hasattr(m, 'config'):
            saved.append((m, {
                'noise_enabled': m.config.noise_enabled,
                'sigma_c2c': m.config.sigma_c2c,
                'sigma_d2d': m.config.sigma_d2d,
            }))
            m.config.noise_enabled = False
            m.config.sigma_c2c = 0.0
            m.config.sigma_d2d = 0.0
    return saved


def restore_analog_noise(saved: list):
    """Restore saved noise configs."""
    for m, cfg in saved:
        m.config.noise_enabled = cfg['noise_enabled']
        m.config.sigma_c2c = cfg['sigma_c2c']
        m.config.sigma_d2d = cfg['sigma_d2d']


def fit_block_affine_calibration(
    model: nn.Module,
    dataloader: torch.utils.data.DataLoader,
    device: str,
    target_blocks: List[str],
    num_calib_batches: int = 4,
    num_raw_averages: int = 5,
) -> AffineCalibrator:
    """Fit block-output affine calibration on a small calibration set.
    
    Args:
        model: The analog model to calibrate
        dataloader: Calibration data (e.g., 32-128 samples)
        device: 'cuda' or 'cpu'
        target_blocks: List of module names to calibrate
        num_calib_batches: Number of batches to use for calibration
        num_raw_averages: Number of forward passes to average for raw outputs
                          (reduces C2C noise variance, isolates D2D drift)
    
    Returns:
        Fitted AffineCalibrator
    """
    model.eval()
    calibrator = AffineCalibrator()
    
    # Register hooks on target blocks
    captures = {}
    handles = []
    for name, module in model.named_modules():
        if any(name.endswith(tb) or name == tb for tb in target_blocks):
            cap = ActivationCapture()
            captures[name] = cap
            handles.append(module.register_forward_hook(cap))
    
    # Pass 1: Collect raw analog outputs (averaged over multiple passes)
    raw_accum = {name: [] for name in captures.keys()}
    with torch.no_grad():
        for _ in range(num_raw_averages):
            for cap in captures.values():
                cap.clear()
            for i, (images, _) in enumerate(dataloader):
                if i >= num_calib_batches:
                    break
                images = images.to(device)
                _ = model(images)
            for name, cap in captures.items():
                raw_accum[name].append(cap.get_concatenated())
    
    raw_outputs = {name: torch.stack(tensors).mean(dim=0) for name, tensors in raw_accum.items()}
    
    # Clear captures
    for cap in captures.values():
        cap.clear()
    
    # Pass 2: Collect reference outputs (noise disabled)
    saved = disable_all_analog_noise(model)
    
    with torch.no_grad():
        for i, (images, _) in enumerate(dataloader):
            if i >= num_calib_batches:
                break
            images = images.to(device)
            _ = model(images)
    
    ref_outputs = {name: cap.get_concatenated() for name, cap in captures.items()}
    
    # Cleanup
    restore_analog_noise(saved)
    for h in handles:
        h.remove()
    
    # Fit
    calibrator.fit(ref_outputs, raw_outputs)
    return calibrator
