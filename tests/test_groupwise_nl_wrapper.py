import unittest

import torch
import torch.nn as nn

from analog_layers import AnalogLinear, AnalogLinearConfig, StraightThroughQuantize, convert_to_hybrid


def _run_backward(
    x_value: float,
    grad_value: float,
    *,
    nl_ltp: float = 2.0,
    nl_ltd: float = -2.0,
    use_second_order_ste: bool = False,
    delta_g_eff: float = 0.0,
    second_order_alpha: float = 1.0,
) -> float:
    x = torch.tensor([x_value], dtype=torch.float32, requires_grad=True)
    y = StraightThroughQuantize.apply(
        x,
        16,
        0.0,
        1.0,
        nl_ltp,
        nl_ltd,
        None,
        use_second_order_ste,
        delta_g_eff,
        second_order_alpha,
    )
    y.backward(torch.tensor([grad_value], dtype=torch.float32))
    return float(x.grad.item())


class GroupwiseNlWrapperTests(unittest.TestCase):
    def test_negative_grad_uses_ltp_scale(self):
        grad = _run_backward(0.25, -1.0, nl_ltp=2.0, nl_ltd=-2.0)
        self.assertAlmostEqual(grad, -0.75, places=5)

    def test_positive_grad_uses_ltd_scale(self):
        grad = _run_backward(0.25, 1.0, nl_ltp=2.0, nl_ltd=-2.0)
        self.assertAlmostEqual(grad, 0.25, places=5)

    def test_first_order_has_no_nl_prefactor(self):
        grad = _run_backward(0.25, -1.0, nl_ltp=3.0, nl_ltd=-3.0)
        # LTP scale = (1 - 0.25)^(3 - 1) = 0.75^2 = 0.5625.
        # A leading nl multiplier would incorrectly produce 1.6875.
        self.assertAlmostEqual(grad, -0.5625, places=5)

    def test_second_order_negative_grad_uses_ltp_branch(self):
        grad = _run_backward(
            0.25,
            -1.0,
            nl_ltp=2.0,
            nl_ltd=-2.0,
            use_second_order_ste=True,
            delta_g_eff=0.1,
        )
        # First-order: -1 * 0.75 = -0.75
        # LTP correction: -0.5 * (2 - 1) * 0.75^(0) * 0.1 = -0.05
        # Branch mapping: negative grad uses LTP correction, so
        #   grad_input = -0.75 + (-1 * -0.05) = -0.70
        self.assertAlmostEqual(grad, -0.70, places=5)

    def test_second_order_positive_grad_uses_ltd_branch(self):
        grad = _run_backward(
            0.25,
            1.0,
            nl_ltp=2.0,
            nl_ltd=-2.0,
            use_second_order_ste=True,
            delta_g_eff=0.1,
        )
        # First-order: 1 * 0.25 = 0.25
        # LTD correction: -0.5 * (2 - 1) * 0.25^(0) * 0.1 = -0.05
        # Branch mapping: positive grad uses LTD correction, so
        #   grad_input = 0.25 + (1 * -0.05) = 0.20
        self.assertAlmostEqual(grad, 0.20, places=5)

    def test_second_order_zero_delta_is_literal_first_order(self):
        grad = _run_backward(
            0.25,
            -1.0,
            nl_ltp=2.0,
            nl_ltd=-2.0,
            use_second_order_ste=True,
            delta_g_eff=0.0,
        )
        self.assertAlmostEqual(grad, -0.75, places=5)

    def test_analog_layers_copy_config_per_module(self):
        cfg = AnalogLinearConfig(NL_LTP=2.0, NL_LTD=-2.0)
        layer_a = AnalogLinear(4, 4, config=cfg)
        layer_b = AnalogLinear(4, 4, config=cfg)

        self.assertIsNot(layer_a.config, layer_b.config)
        layer_a.config.NL_LTP = 1.0
        layer_a.config.use_second_order_ste = True

        self.assertEqual(layer_b.config.NL_LTP, 2.0)
        self.assertFalse(layer_b.config.use_second_order_ste)

    def test_convert_to_hybrid_copies_config_per_replacement(self):
        model = nn.Sequential(nn.Linear(4, 4), nn.Linear(4, 2))
        cfg = AnalogLinearConfig(NL_LTP=2.0, NL_LTD=-2.0)

        converted = convert_to_hybrid(model, config=cfg, analog_layer_names=["0", "1"])
        layer_a = converted[0]
        layer_b = converted[1]

        self.assertIsInstance(layer_a, AnalogLinear)
        self.assertIsInstance(layer_b, AnalogLinear)
        self.assertIsNot(layer_a.config, layer_b.config)

        layer_a.config.NL_LTP = 1.0
        self.assertEqual(layer_b.config.NL_LTP, 2.0)

    @unittest.skipUnless(torch.cuda.is_available(), "CUDA is required for AMP autocast regression")
    def test_ste_under_amp_no_nan(self):
        config = AnalogLinearConfig(
            NL_LTP=2.0,
            NL_LTD=-2.0,
            use_second_order_ste=True,
            delta_g_eff=0.1,
            sigma_c2c=0.0,
            sigma_d2d=0.0,
            noise_enabled=False,
        )
        layer = AnalogLinear(8, 4, config=config).cuda()
        x = torch.randn(16, 8, device="cuda", requires_grad=True)

        with torch.amp.autocast("cuda"):
            loss = layer(x).square().mean()
        loss.backward()

        self.assertTrue(torch.isfinite(x.grad).all())
        self.assertTrue(torch.isfinite(layer.weight.grad).all())
        if layer.bias is not None:
            self.assertTrue(torch.isfinite(layer.bias.grad).all())


if __name__ == "__main__":
    unittest.main()
