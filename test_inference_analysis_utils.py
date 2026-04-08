#!/usr/bin/env python3
"""Lightweight tests for inference-only analysis helpers."""

import unittest

import torch

from analog_layers import AnalogLinear, AnalogLinearConfig
from inference_analysis_utils import (
    ModelBundle,
    adc_bits_label,
    build_sparsity_rows,
    collect_analog_noise_diagnostics,
    merge_rows,
    restore_analog_state,
    set_uniform_noise,
    snapshot_analog_state,
)
from run_layer_sensitivity import (
    group_specs_for,
    rank_group_drops,
    select_robust_groups_for_phase2,
)
from run_noise_sweep import parse_adc_bits


class InferenceAnalysisUtilsTests(unittest.TestCase):
    def test_merge_rows_replaces_duplicate_keys(self):
        existing = [
            {"model": "tinyvit", "experiment": "V4", "sweep_type": "noise", "sigma_c2c": 0.05, "sigma_d2d": 0.10, "adc_label": "native", "test_acc_mean": 90.0},
        ]
        new_rows = [
            {"model": "tinyvit", "experiment": "V4", "sweep_type": "noise", "sigma_c2c": 0.05, "sigma_d2d": 0.10, "adc_label": "native", "test_acc_mean": 91.5},
            {"model": "convnext", "experiment": "C4", "sweep_type": "adc", "sigma_c2c": 0.05, "sigma_d2d": 0.10, "adc_label": "4-bit", "test_acc_mean": 88.0},
        ]
        merged = merge_rows(
            existing,
            new_rows,
            key_fields=("model", "experiment", "sweep_type", "sigma_c2c", "sigma_d2d", "adc_label"),
        )

        self.assertEqual(len(merged), 2)
        tinyvit_row = next(row for row in merged if row["model"] == "tinyvit")
        self.assertEqual(tinyvit_row["test_acc_mean"], 91.5)

    def test_parse_adc_bits_supports_ideal(self):
        self.assertEqual(parse_adc_bits(["3", "ideal", "10"]), [3, None, 10])
        self.assertEqual(adc_bits_label(None), "ideal")
        self.assertEqual(adc_bits_label(6), "6-bit")

    def test_group_specs_cover_expected_ids(self):
        self.assertEqual([group[0] for group in group_specs_for("tinyvit")], ["A", "B", "C", "D", "E", "F"])
        self.assertEqual([group[0] for group in group_specs_for("convnext")], ["A", "B", "C", "D", "E", "F"])

    def test_snapshot_and_restore_analog_state(self):
        model = torch.nn.Sequential(
            AnalogLinear(4, 3, config=AnalogLinearConfig(sigma_c2c=0.05, sigma_d2d=0.10)),
            AnalogLinear(3, 2, config=AnalogLinearConfig(sigma_c2c=0.05, sigma_d2d=0.10)),
        )
        snapshot = snapshot_analog_state(model)

        set_uniform_noise(model, sigma_c2c=0.0, sigma_d2d=0.0, noise_enabled=False)
        for module in model.modules():
            if isinstance(module, AnalogLinear):
                self.assertFalse(module.config.noise_enabled)
                self.assertEqual(module.config.sigma_c2c, 0.0)
                self.assertEqual(module.config.sigma_d2d, 0.0)

        restore_analog_state(model, snapshot)
        for module in model.modules():
            if isinstance(module, AnalogLinear):
                self.assertTrue(module.config.noise_enabled)
                self.assertEqual(module.config.sigma_c2c, 0.05)
                self.assertEqual(module.config.sigma_d2d, 0.10)

    def test_set_uniform_noise_can_resample_d2d_buffers(self):
        model = torch.nn.Sequential(
            AnalogLinear(4, 3, config=AnalogLinearConfig(sigma_c2c=0.0, sigma_d2d=0.0, noise_enabled=False)),
        )
        layer = next(module for module in model.modules() if isinstance(module, AnalogLinear))
        self.assertAlmostEqual(float(layer.d2d_noise.abs().sum().item()), 0.0)

        set_uniform_noise(model, sigma_c2c=0.05, sigma_d2d=0.10, noise_enabled=True, resample_d2d=True)

        self.assertTrue(layer.config.noise_enabled)
        self.assertEqual(layer.config.sigma_c2c, 0.05)
        self.assertEqual(layer.config.sigma_d2d, 0.10)
        self.assertGreater(float(layer.d2d_noise.abs().sum().item()), 0.0)

    def test_collect_analog_noise_diagnostics_reports_ratios(self):
        model = torch.nn.Sequential(
            AnalogLinear(4, 3, config=AnalogLinearConfig(sigma_c2c=0.05, sigma_d2d=0.10, noise_enabled=True)),
        )
        layer = next(module for module in model.modules() if isinstance(module, AnalogLinear))
        with torch.no_grad():
            layer.weight.copy_(torch.tensor([
                [1.0, -0.5, 0.2, -0.1],
                [0.7, -0.3, 0.4, -0.2],
                [0.6, 0.1, -0.8, 0.5],
            ]))

        rows = collect_analog_noise_diagnostics(model)
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertIn("noise_to_weight_ratio", row)
        self.assertIn("noise_to_effective_weight_ratio", row)
        self.assertGreaterEqual(row["d2d_noise_std_conductance"], 0.0)
        self.assertGreaterEqual(row["total_noise_std_conductance"], row["d2d_noise_std_conductance"])

    def test_phase2_group_selection_prefers_small_accuracy_drop(self):
        phase1_rows = [
            {"model": "tinyvit", "experiment": "V4", "phase": "isolated", "group_id": "A", "group_label": "Attention QKV", "test_acc_mean": 89.0},
            {"model": "tinyvit", "experiment": "V4", "phase": "isolated", "group_id": "B", "group_label": "Attention Proj", "test_acc_mean": 87.0},
            {"model": "tinyvit", "experiment": "V4", "phase": "isolated", "group_id": "C", "group_label": "FFN", "test_acc_mean": 90.5},
            {"model": "tinyvit", "experiment": "V4", "phase": "isolated", "group_id": "D", "group_label": "Patch Embed", "test_acc_mean": 88.5},
            {"model": "tinyvit", "experiment": "V4", "phase": "isolated", "group_id": "E", "group_label": "All analog", "test_acc_mean": 80.0},
            {"model": "tinyvit", "experiment": "V4", "phase": "isolated", "group_id": "F", "group_label": "None", "test_acc_mean": 91.0},
        ]

        ranked = rank_group_drops(phase1_rows)
        self.assertEqual([row["group_id"] for row in ranked[:2]], ["C", "A"])
        self.assertEqual(select_robust_groups_for_phase2(phase1_rows, top_k=2), ["C", "A"])

    def test_build_sparsity_rows_exports_relative_and_absolute_metrics(self):
        bundle = ModelBundle(
            model_type="tinyvit",
            experiment="V4",
            experiment_name="V4_hybrid_standard_noise_hat",
            dataset="cifar10",
            device="cpu",
            model=torch.nn.Identity(),
            exp_cfg=None,
            testloader=None,
            criterion=torch.nn.CrossEntropyLoss(),
            frontend=None,
            checkpoint_path="checkpoints/V4_hybrid_standard_noise_hat_best.pt",
            checkpoint_epoch=99,
            checkpoint_best_acc=91.94,
            amp_enabled=False,
        )
        sparsity_report = {
            "model_mean_relative_zero_frac": 0.20,
            "model_mean_absolute_zero_frac": 0.35,
            "layers": [
                {
                    "layer": "blocks.0.mlp.fc2",
                    "kind": "AnalogLinear",
                    "samples": 10,
                    "relative_scale": 0.01,
                    "absolute_threshold": 0.01,
                    "mean_relative_zero_frac": 0.20,
                    "mean_relative_nonzero_frac": 0.80,
                    "last_relative_zero_frac": 0.18,
                    "mean_absolute_zero_frac": 0.35,
                    "mean_absolute_nonzero_frac": 0.65,
                    "last_absolute_zero_frac": 0.33,
                }
            ],
        }

        rows = build_sparsity_rows(bundle, sparsity_report, context={"sweep_type": "noise"})
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["model"], "tinyvit")
        self.assertEqual(row["sweep_type"], "noise")
        self.assertAlmostEqual(row["mean_relative_zero_frac"], 0.20)
        self.assertAlmostEqual(row["mean_absolute_zero_frac"], 0.35)
        self.assertAlmostEqual(row["model_mean_relative_zero_frac"], 0.20)
        self.assertAlmostEqual(row["model_mean_absolute_zero_frac"], 0.35)


if __name__ == "__main__":
    unittest.main()
