#!/usr/bin/env python3
"""Lightweight unittest coverage for ConvNeXt report-only helpers."""

import tempfile
import unittest
from pathlib import Path
from unittest import mock

import torch

from analog_layers import AnalogLinear, AnalogLinearConfig
from train_convnext import (
    ExperimentConfig,
    get_experiment_configs,
    parse_training_log,
    parse_training_logs,
    resolve_experiment_amp,
    set_noise_for_eval,
    set_noise_for_train,
)


class ConvNeXtLogParsingTests(unittest.TestCase):
    def test_parse_training_log_extracts_finished_and_mc_results(self):
        log_text = """
======================================================================
Experiment C2: C2_4bit_no_noise
  n_states=16, C2C=0.0, D2D=0.0, HAT=False
======================================================================
  Finished in 3631s. Best test accuracy: 90.69%

======================================================================
Experiment C3: C3_4bit_noise_standard
  n_states=16, C2C=0.05, D2D=0.1, HAT=False
======================================================================
  Finished in 3636s. Best test accuracy: 70.48%
  Running Monte Carlo evaluation (10 runs)...
  Monte Carlo: 69.58% ± 0.55%
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "convnext.log"
            log_path.write_text(log_text, encoding="utf-8")
            results, histories = parse_training_log(str(log_path), get_experiment_configs(epochs=200))

        self.assertEqual([row["experiment"] for row in results], ["C2", "C3"])
        self.assertEqual(results[0]["best_test_acc"], 90.69)
        self.assertEqual(results[0]["mc_mean_acc"], 90.69)
        self.assertEqual(results[0]["mc_std_acc"], 0.0)
        self.assertEqual(results[1]["best_test_acc"], 70.48)
        self.assertEqual(results[1]["mc_mean_acc"], 69.58)
        self.assertEqual(results[1]["mc_std_acc"], 0.55)
        self.assertIn("C2", histories)
        self.assertIn("C3", histories)

    def test_parse_training_log_ignores_incomplete_experiment(self):
        log_text = """
======================================================================
Experiment C4: C4_4bit_noise_HAT
  n_states=16, C2C=0.05, D2D=0.1, HAT=True
======================================================================
  Epoch   0/200: train_loss=90.0443, train_acc=9.99%, test_acc=10.23% (best=10.23%), lr=0.004000, time=17s
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "convnext_partial.log"
            log_path.write_text(log_text, encoding="utf-8")
            results, histories = parse_training_log(str(log_path), get_experiment_configs(epochs=200))

        self.assertEqual(results, [])
        self.assertEqual(histories, {})

    def test_parse_training_logs_merges_multiple_sources(self):
        log_a = """
======================================================================
Experiment C1: C1_FP32_baseline
======================================================================
  Finished in 100s. Best test accuracy: 90.74%
"""
        log_b = """
======================================================================
Experiment C4: C4_4bit_noise_HAT
======================================================================
  Finished in 3700s. Best test accuracy: 89.91%
  Running Monte Carlo evaluation (10 runs)...
  Monte Carlo: 89.71% ± 0.17%
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            path_a = Path(tmpdir) / "a.log"
            path_b = Path(tmpdir) / "b.log"
            path_a.write_text(log_a, encoding="utf-8")
            path_b.write_text(log_b, encoding="utf-8")
            results, _ = parse_training_logs(
                [str(path_a), str(path_b)],
                get_experiment_configs(epochs=200),
            )

        self.assertEqual([row["experiment"] for row in results], ["C1", "C4"])
        self.assertEqual(results[0]["best_test_acc"], 90.74)
        self.assertEqual(results[1]["mc_mean_acc"], 89.71)
        self.assertEqual(results[1]["mc_std_acc"], 0.17)


class ConvNeXtAmpPolicyTests(unittest.TestCase):
    @mock.patch("train_convnext.amp_enabled_for_device", return_value=True)
    def test_auto_disables_amp_for_analog_experiment(self, _mock_amp):
        active_amp, note = resolve_experiment_amp(
            requested_amp=True,
            device="cuda",
            exp_cfg=ExperimentConfig(name="C3", use_analog=True),
        )
        self.assertFalse(active_amp)
        self.assertIn("auto-disabled", note)

    @mock.patch("train_convnext.amp_enabled_for_device", return_value=True)
    def test_keeps_amp_for_digital_experiment(self, _mock_amp):
        active_amp, note = resolve_experiment_amp(
            requested_amp=True,
            device="cuda",
            exp_cfg=ExperimentConfig(name="C1", use_analog=False),
        )
        self.assertTrue(active_amp)
        self.assertIsNone(note)


class ConvNeXtPhysicsOverrideTests(unittest.TestCase):
    def test_noise_routing_propagates_nl_and_noise_mode(self):
        model = torch.nn.Sequential(
            AnalogLinear(4, 3, config=AnalogLinearConfig()),
            AnalogLinear(3, 2, config=AnalogLinearConfig()),
        )
        cfg = ExperimentConfig(
            name="C4_test",
            use_analog=True,
            hat_training=True,
            noise_enabled=True,
            sigma_c2c=0.05,
            sigma_d2d=0.10,
            nl_ltp=2.0,
            nl_ltd=-2.5,
            noise_mode="proportional",
        )
        set_noise_for_train(model, cfg)
        set_noise_for_eval(model, cfg)

        for module in model.modules():
            if isinstance(module, AnalogLinear):
                self.assertEqual(module.config.noise_mode, "proportional")
                self.assertAlmostEqual(module.config.NL_LTP, 2.0)
                self.assertAlmostEqual(module.config.NL_LTD, -2.5)


if __name__ == "__main__":
    unittest.main()
