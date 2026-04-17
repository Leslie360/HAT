#!/usr/bin/env python3
"""Focused regression tests for device_profile_utils validation."""

import json
import tempfile
import unittest

from device_profile_utils import DeviceProfile, load_device_profiles_json


class DeviceProfileValidationTests(unittest.TestCase):
    def test_valid_profile_round_trip_loads(self):
        payload = {
            "source": "unit-test",
            "profiles": [
                {
                    "device_type": "Validated Device",
                    "G_min": 1.0,
                    "G_max": 10.0,
                    "n_states": 8,
                    "noise": {"sigma_c2c": 0.01, "sigma_d2d": 0.02, "mode": "uniform"},
                    "retention": {"A_0": 0.6, "tau_1": 0.14, "tau_2": 0.61},
                }
            ],
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8") as fh:
            json.dump(payload, fh)
            fh.flush()
            profiles = load_device_profiles_json(fh.name)

        self.assertEqual(len(profiles), 1)
        self.assertEqual(profiles[0].device_type, "Validated Device")
        self.assertEqual(profiles[0].noise_mode, "uniform")

    def test_invalid_noise_mode_is_rejected(self):
        payload = {
            "profiles": [
                {
                    "device_type": "Bad Device",
                    "G_min": 1.0,
                    "G_max": 10.0,
                    "n_states": 8,
                    "noise": {"sigma_c2c": 0.01, "sigma_d2d": 0.02, "mode": "mystery"},
                }
            ]
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8") as fh:
            json.dump(payload, fh)
            fh.flush()
            with self.assertRaises(ValueError):
                load_device_profiles_json(fh.name)

    def test_invalid_conductance_span_is_rejected(self):
        payload = {
            "profiles": [
                {
                    "device_type": "Flat Device",
                    "G_min": 5.0,
                    "G_max": 5.0,
                    "n_states": 8,
                    "sigma_c2c": 0.01,
                    "sigma_d2d": 0.02,
                }
            ]
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8") as fh:
            json.dump(payload, fh)
            fh.flush()
            with self.assertRaises(ValueError):
                load_device_profiles_json(fh.name)

    def test_direct_profile_constructor_rejects_bad_inl_table(self):
        with self.assertRaises(ValueError):
            DeviceProfile(
                device_type="Bad INL",
                dynamic_range=10.0,
                n_states=8,
                sigma_c2c=0.01,
                sigma_d2d=0.02,
                source="unit-test",
                inl_table=[1.0, 0.9, 2.0],
            )


if __name__ == "__main__":
    unittest.main()
