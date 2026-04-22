#!/usr/bin/env python3
"""Lightweight tests for layer sensitivity helpers."""

import unittest

import torch

from analog_layers import AnalogLinear, AnalogLinearConfig
from run_layer_sensitivity import apply_group_noise


class LayerSensitivityTests(unittest.TestCase):
    def test_apply_group_noise_preserves_checkpoint_d2d_by_default(self):
        model = torch.nn.Module()
        model.group_a = AnalogLinear(4, 3, config=AnalogLinearConfig())
        model.group_b = AnalogLinear(3, 2, config=AnalogLinearConfig())
        before_a = model.group_a.d2d_noise.clone()
        before_b = model.group_b.d2d_noise.clone()

        active, total = apply_group_noise(
            model,
            sigma_c2c=0.05,
            sigma_d2d=0.10,
            selector=lambda name: name == "group_a",
        )

        self.assertEqual((active, total), (1, 2))
        self.assertTrue(torch.equal(before_a, model.group_a.d2d_noise))
        self.assertTrue(torch.equal(before_b, model.group_b.d2d_noise))
        self.assertTrue(model.group_a.config.noise_enabled)
        self.assertTrue(model.group_b.config.noise_enabled)
        self.assertAlmostEqual(model.group_a.config.sigma_c2c, 0.05)
        self.assertAlmostEqual(model.group_b.config.sigma_c2c, 0.0)

    def test_apply_group_noise_can_resample_enabled_layers(self):
        model = torch.nn.Module()
        model.group_a = AnalogLinear(4, 3, config=AnalogLinearConfig())
        model.group_b = AnalogLinear(3, 2, config=AnalogLinearConfig())
        before_a = model.group_a.d2d_noise.clone()
        before_b = model.group_b.d2d_noise.clone()

        active, total = apply_group_noise(
            model,
            sigma_c2c=0.05,
            sigma_d2d=0.10,
            selector=lambda name: name == "group_a",
            resample_d2d=True,
        )

        self.assertEqual((active, total), (1, 2))
        self.assertFalse(torch.equal(before_a, model.group_a.d2d_noise))
        self.assertTrue(torch.equal(before_b, model.group_b.d2d_noise))
        self.assertAlmostEqual(model.group_a.config.sigma_c2c, 0.05)
        self.assertAlmostEqual(model.group_b.config.sigma_c2c, 0.0)


if __name__ == "__main__":
    unittest.main()
