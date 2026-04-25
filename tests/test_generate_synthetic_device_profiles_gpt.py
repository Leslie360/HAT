#!/usr/bin/env python3
"""Tests for synthetic device-profile generation."""

import json
import tempfile
import unittest

from device_profile_utils import DeviceProfile, load_device_profiles_json
from generate_synthetic_device_profiles_gpt import build_profiles


class SyntheticProfileGenerationTests(unittest.TestCase):
    def test_build_profiles_creates_combinatorial_grid(self):
        base = DeviceProfile(
            device_type="Base",
            dynamic_range=10.0,
            n_states=16,
            sigma_c2c=0.05,
            sigma_d2d=0.10,
            source="unit-test",
            tau_1=0.14,
            tau_2=0.61,
            A_0=0.6,
            gamma_phys=0.7,
            I_dark=1e-10,
        )
        profiles = build_profiles(
            base=base,
            dynamic_ranges=[5.0, 10.0],
            n_states_list=[8, 16],
            sigma_c2c_list=[0.01],
            sigma_d2d_list=[0.03, 0.10],
            gamma_phys_list=[0.7],
            I_dark_list=[1e-10],
            tau1_scale_list=[1.0],
            tau2_scale_list=[1.0],
            prefix="Test",
            profile_kind="synthetic",
        )
        self.assertEqual(len(profiles), 8)
        self.assertTrue(all(profile.profile_kind == "synthetic" for profile in profiles))

    def test_generated_profiles_round_trip_through_json_loader(self):
        payload = {
            "source": "synthetic",
            "profiles": [
                {
                    "device_type": "Synthetic A",
                    "G_min": 1.0,
                    "G_max": 8.0,
                    "n_states": 12,
                    "sigma_c2c": 0.03,
                    "sigma_d2d": 0.09,
                    "gamma_phys": 0.8,
                    "I_dark": 1e-11,
                    "profile_kind": "synthetic",
                }
            ],
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8") as fh:
            json.dump(payload, fh)
            fh.flush()
            profiles = load_device_profiles_json(fh.name)

        self.assertEqual(len(profiles), 1)
        self.assertEqual(profiles[0].device_type, "Synthetic A")
        self.assertAlmostEqual(profiles[0].dynamic_range, 8.0)
        self.assertEqual(profiles[0].n_states, 12)
        self.assertAlmostEqual(profiles[0].gamma_phys, 0.8)


if __name__ == "__main__":
    unittest.main()
