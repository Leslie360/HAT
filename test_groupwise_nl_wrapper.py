import unittest
from types import SimpleNamespace

import torch
import torch.nn as nn

from analog_layers import AnalogLinear, AnalogLinearConfig, StraightThroughQuantize, convert_to_hybrid
from scripts._gpt.run_tinyvit_groupwise_nl_comp import make_groupwise_setter


def _make_module():
    return AnalogLinear(4, 4, config=AnalogLinearConfig())


def _make_cfg(*, hat_training, noise_enabled, sigma_c2c=0.05, sigma_d2d=0.10):
    return SimpleNamespace(
        hat_training=hat_training,
        noise_enabled=noise_enabled,
        sigma_c2c=sigma_c2c,
        sigma_d2d=sigma_d2d,
        noise_mode="uniform",
        nl_ltp=2.0,
        nl_ltd=-2.0,
    )


class GroupwiseNlWrapperTests(unittest.TestCase):
    def test_analog_layers_do_not_share_config_instance(self):
        cfg = AnalogLinearConfig()
        a = AnalogLinear(4, 4, config=cfg)
        b = AnalogLinear(4, 4, config=cfg)
        self.assertIsNot(a.config, b.config)

    def test_convert_to_hybrid_assigns_distinct_configs_per_layer(self):
        model = nn.Sequential(nn.Linear(4, 4), nn.Linear(4, 4))
        cfg = AnalogLinearConfig()
        hybrid = convert_to_hybrid(model, config=cfg, analog_layer_names=["0", "1"])
        self.assertIsInstance(hybrid[0], AnalogLinear)
        self.assertIsInstance(hybrid[1], AnalogLinear)
        self.assertIsNot(hybrid[0].config, hybrid[1].config)

    def test_negative_delta_g_eff_autofills_from_effective_train_noise(self):
        module = _make_module()
        cfg = _make_cfg(hat_training=False, noise_enabled=True)

        setter = make_groupwise_setter(
            selector=lambda _name: True,
            protected_nl_ltp=1.0,
            protected_nl_ltd=-1.0,
            train_mode=True,
            use_second_order_ste=True,
            delta_g_eff=-1.0,
            second_order_alpha=1.0,
        )

        setter(module, cfg)

        self.assertEqual(module.config.sigma_c2c, 0.0)
        self.assertEqual(module.config.sigma_d2d, 0.10)
        self.assertEqual(module.config.delta_g_eff, 0.10)

    def test_zero_delta_g_eff_is_literal_zero_not_autofill(self):
        module = _make_module()
        cfg = _make_cfg(hat_training=True, noise_enabled=True)

        setter = make_groupwise_setter(
            selector=lambda _name: True,
            protected_nl_ltp=1.0,
            protected_nl_ltd=-1.0,
            train_mode=True,
            use_second_order_ste=True,
            delta_g_eff=0.0,
            second_order_alpha=1.0,
        )

        setter(module, cfg)

        self.assertEqual(module.config.sigma_c2c, 0.05)
        self.assertEqual(module.config.delta_g_eff, 0.0)

    def test_so2_off_resets_stale_state(self):
        module = _make_module()
        cfg = _make_cfg(hat_training=True, noise_enabled=True)
        module.config.use_second_order_ste = True
        module.config.delta_g_eff = 9.0
        module.config.second_order_alpha = 3.0

        setter = make_groupwise_setter(
            selector=lambda _name: True,
            protected_nl_ltp=1.0,
            protected_nl_ltd=-1.0,
            train_mode=True,
            use_second_order_ste=False,
            delta_g_eff=-1.0,
            second_order_alpha=1.0,
        )

        setter(module, cfg)

        self.assertFalse(module.config.use_second_order_ste)
        self.assertEqual(module.config.delta_g_eff, 0.0)
        self.assertEqual(module.config.second_order_alpha, 1.0)

    def test_ltp_backward_includes_nl_multiplier(self):
        x = torch.tensor([0.25], dtype=torch.float32, requires_grad=True)
        y = StraightThroughQuantize.apply(x, 16, 0.0, 1.0, 2.0, -2.0, None, False, 0.0, 1.0)
        y.backward(torch.ones_like(y))
        # For nl=2 and x=0.25 in the LTP branch, ratio=(1-0.25)=0.75, so
        # the first-order scale should be 2 * 0.75 = 1.5.
        self.assertAlmostEqual(float(x.grad.item()), 1.5, places=5)

    def test_ltd_backward_includes_nl_multiplier(self):
        x = torch.tensor([0.25], dtype=torch.float32, requires_grad=True)
        y = StraightThroughQuantize.apply(x, 16, 0.0, 1.0, 2.0, -2.0, None, False, 0.0, 1.0)
        y.backward(-torch.ones_like(y))
        # For nl=2 and x=0.25 in the LTD branch, ratio=0.25, so
        # the first-order scale should be 2 * 0.25 = 0.5.
        self.assertAlmostEqual(float(x.grad.item()), -0.5, places=5)


if __name__ == "__main__":
    unittest.main()
