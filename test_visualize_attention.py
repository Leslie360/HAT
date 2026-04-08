#!/usr/bin/env python3
"""Lightweight tests for attention-visualization helpers."""

import unittest

import numpy as np
import torch

from visualize_attention import (
    DEFAULT_EXPERIMENT_ORDER,
    DEFAULT_IMAGE_INDICES,
    aggregate_attention_map,
    build_markdown,
    find_representative_indices,
    resolve_visualization_indices,
)


class FakeCIFAR10:
    classes = ["plane", "car", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]

    def __init__(self):
        self.labels = [0, 2, 8, 3, 9, 2]

    def __iter__(self):
        for label in self.labels:
            yield object(), label


class VisualizeAttentionTests(unittest.TestCase):
    def test_find_representative_indices_by_class_name(self):
        dataset = FakeCIFAR10()
        indices = find_representative_indices(dataset, ["bird", "cat", "ship", "truck"])
        self.assertEqual(indices, [1, 2, 3, 4])

    def test_resolve_visualization_indices_defaults_to_fixed_paper_samples(self):
        dataset = FakeCIFAR10()
        indices = resolve_visualization_indices(dataset, explicit_indices=None, target_class_names=["bird"])
        self.assertEqual(indices, DEFAULT_IMAGE_INDICES)

    def test_aggregate_attention_map_normalizes_output(self):
        attn = torch.ones(1, 2, 4, 4)
        attn[0, :, :, 0] = 5.0
        attn_map = aggregate_attention_map(attn, resolution=(2, 2), mode="mean_queries")
        self.assertEqual(attn_map.shape, (2, 2))
        self.assertTrue(np.all(attn_map >= 0.0))
        self.assertTrue(np.all(attn_map <= 1.0))
        self.assertAlmostEqual(float(attn_map.max()), 1.0, places=6)

    def test_aggregate_attention_map_supports_center_query_mode(self):
        attn = torch.arange(1, 17, dtype=torch.float32).view(1, 1, 4, 4)
        attn_map = aggregate_attention_map(attn, resolution=(2, 2), mode="center_query")
        self.assertEqual(attn_map.shape, (2, 2))
        self.assertGreaterEqual(float(attn_map.max()), float(attn_map.min()))

    def test_default_experiment_order_includes_v6(self):
        self.assertEqual(DEFAULT_EXPERIMENT_ORDER, ["V1", "V3", "V4", "V6"])

    def test_markdown_includes_v6_predictions(self):
        samples = [{
            "index": 0,
            "label_name": "bird",
            "predictions": {"V1": "bird", "V3": "cat", "V4": "bird", "V6": "ship"},
            "maps": {},
            "image_np": np.zeros((4, 4, 3), dtype=np.float32),
        }]
        md = build_markdown(samples, "stages.3.blocks.0.attn", "fig.png", "diff.png")
        self.assertIn("V6 pred", md)
        self.assertIn("| 0 | bird | bird | cat | bird | ship |", md)


if __name__ == "__main__":
    unittest.main()
