#!/usr/bin/env python3
"""Regression tests for per-instance ADC calibration."""

from types import SimpleNamespace

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

from analog_layers import AnalogLinear, AnalogLinearConfig
from inference_analysis_utils import calibrate_adc_ranges, set_uniform_noise


def _make_bundle() -> SimpleNamespace:
    config = AnalogLinearConfig(
        sigma_c2c=0.0,
        sigma_d2d=0.30,
        noise_enabled=True,
        noise_mode="uniform",
    )
    model = nn.Sequential(AnalogLinear(4, 3, bias=False, config=config))
    with torch.no_grad():
        model[0].weight.copy_(
            torch.tensor(
                [
                    [0.40, -0.20, 0.10, 0.30],
                    [-0.10, 0.35, -0.25, 0.15],
                    [0.20, 0.10, 0.25, -0.30],
                ],
                dtype=torch.float32,
            )
        )
    inputs = torch.linspace(-1.0, 1.0, steps=32).reshape(8, 4)
    targets = torch.zeros(8, dtype=torch.long)
    return SimpleNamespace(
        model=model,
        testloader=DataLoader(TensorDataset(inputs, targets), batch_size=4),
        device="cpu",
        frontend=None,
        amp_enabled=False,
    )


def test_per_instance_adc_ranges_follow_d2d_buffers():
    bundle = _make_bundle()
    ranges = []
    for seed in (11, 22, 33):
        torch.manual_seed(seed)
        set_uniform_noise(
            bundle.model,
            sigma_c2c=0.0,
            sigma_d2d=0.30,
            noise_enabled=True,
            resample_d2d=True,
            noise_mode="uniform",
        )
        ranges.append(
            calibrate_adc_ranges(
                bundle,
                max_batches=1,
                use_current_noise=True,
                disable_c2c=True,
            )
        )

    observed = {(round(row["0"]["min"], 6), round(row["0"]["max"], 6)) for row in ranges}
    assert len(observed) >= 2, f"Expected ADC ranges to differ across D2D draws, got {observed}"


if __name__ == "__main__":
    test_per_instance_adc_ranges_follow_d2d_buffers()
    print("test_per_instance_adc_ranges_follow_d2d_buffers passed")
