#!/usr/bin/env python3
"""Lightweight tests for device comparison helpers."""

import json
import tempfile
import unittest

import torch

from analog_layers import AnalogLinear, AnalogLinearConfig
from device_profile_utils import load_device_profiles_json
from run_device_comparison import DEVICE_PROFILES, apply_device_profile


class DeviceComparisonTests(unittest.TestCase):
    def test_profiles_cover_expected_device_types(self):
        labels = [profile.device_type for profile in DEVICE_PROFILES]
        self.assertEqual(
            labels,
            ["Organic OPECT", "RRAM (HfOx)", "PCM (GST)", "Organic Pessimistic", "Ideal"],
        )

    def test_apply_device_profile_updates_analog_config(self):
        model = torch.nn.Sequential(
            AnalogLinear(4, 3, config=AnalogLinearConfig()),
            AnalogLinear(3, 2, config=AnalogLinearConfig()),
        )
        updated = apply_device_profile(model, DEVICE_PROFILES[1])
        self.assertEqual(updated, 2)
        for module in model.modules():
            if isinstance(module, AnalogLinear):
                self.assertEqual(module.config.n_states, 64)
                self.assertAlmostEqual(module.config.G_min, 1.0)
                self.assertAlmostEqual(module.config.G_max, 100.0)
                self.assertAlmostEqual(module.config.sigma_c2c, 0.02)
                self.assertAlmostEqual(module.config.sigma_d2d, 0.05)
                self.assertEqual(module.config.noise_mode, "uniform")
                self.assertGreater(float(module.d2d_noise.abs().sum().item()), 0.0)

    def test_load_measured_profile_json_supports_nested_noise_and_retention(self):
        payload = {
            "source": "unit-test",
            "profiles": [
                {
                    "device_type": "Measured Device",
                    "G_min": 2.0,
                    "G_max": 20.0,
                    "n_states": 12,
                    "noise": {"sigma_c2c": 0.07, "sigma_d2d": 0.11, "mode": "proportional"},
                    "plasticity": {"NL_LTP": 2.0, "NL_LTD": -2.5},
                    "retention": {"A_0": 0.55, "tau_1": 0.2, "tau_2": 0.8},
                }
            ],
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8") as fh:
            json.dump(payload, fh)
            fh.flush()
            profiles = load_device_profiles_json(fh.name)

        self.assertEqual(len(profiles), 1)
        profile = profiles[0]
        self.assertEqual(profile.device_type, "Measured Device")
        self.assertAlmostEqual(profile.G_min, 2.0)
        self.assertAlmostEqual(profile.G_max, 20.0)
        self.assertAlmostEqual(profile.dynamic_range, 10.0)
        self.assertEqual(profile.n_states, 12)
        self.assertAlmostEqual(profile.sigma_c2c, 0.07)
        self.assertAlmostEqual(profile.sigma_d2d, 0.11)
        self.assertEqual(profile.noise_mode, "proportional")
        self.assertAlmostEqual(profile.NL_LTP, 2.0)
        self.assertAlmostEqual(profile.NL_LTD, -2.5)
        self.assertAlmostEqual(profile.A_0, 0.55)
        self.assertAlmostEqual(profile.tau_1, 0.2)
        self.assertAlmostEqual(profile.tau_2, 0.8)


if __name__ == "__main__":
    unittest.main()
