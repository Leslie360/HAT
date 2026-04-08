#!/usr/bin/env python3
"""Lightweight tests for ImageNet analog evaluation helpers."""

import tempfile
import unittest
from pathlib import Path

from eval_imagenet_analog import build_markdown, resolve_imagenet_val_dir


class EvalImagenetAnalogTests(unittest.TestCase):
    def test_resolve_imagenet_val_dir_prefers_explicit_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            explicit = Path(tmpdir) / "custom_val"
            explicit.mkdir()
            resolved = resolve_imagenet_val_dir("/tmp/unused", str(explicit))
            self.assertEqual(resolved, str(explicit))

    def test_resolve_imagenet_val_dir_autodetects_common_layouts(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            val_dir = root / "imagenet" / "val"
            val_dir.mkdir(parents=True)
            resolved = resolve_imagenet_val_dir(str(root), None)
            self.assertEqual(resolved, str(val_dir))

    def test_build_markdown_lists_conditions(self):
        rows = [
            {
                "condition": "digital_fp32_pretrained",
                "use_hybrid": False,
                "noise_enabled": False,
                "test_acc_mean": 72.0,
                "test_acc_std": 0.0,
                "eval_runs": 1,
                "checkpoint_path": None,
            },
            {
                "condition": "hybrid_standard_noise",
                "use_hybrid": True,
                "noise_enabled": True,
                "test_acc_mean": 65.0,
                "test_acc_std": 0.5,
                "eval_runs": 10,
                "checkpoint_path": None,
            },
        ]
        markdown = build_markdown(rows, "/data/imagenet/val", 50000)
        self.assertIn("ImageNet Zero-Shot Analog Deployment Results", markdown)
        self.assertIn("digital_fp32_pretrained", markdown)
        self.assertIn("hybrid_standard_noise", markdown)


if __name__ == "__main__":
    unittest.main()
