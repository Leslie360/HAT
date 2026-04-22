#!/usr/bin/env python3
"""Wrapper around train_tinyvit_ensemble.py for group-wise NL mitigation studies.

This keeps the upstream training loop intact and only overrides how NL_LTP/NL_LTD
are applied to selected analog module groups. It is intended for targeted
reviewer-facing follow-up experiments such as "linearize the MLP surrogate while
keeping global NL=2.0 elsewhere".
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Callable, Dict

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analog_layers import AnalogConv2d, AnalogLinear
import train_tinyvit_ensemble as base


AnalogModule = (AnalogLinear, AnalogConv2d)


def build_selector(group: str) -> Callable[[str], bool]:
    normalized = group.lower()
    selectors: Dict[str, Callable[[str], bool]] = {
        "none": lambda _name: False,
        "all": lambda _name: True,
        "mlp": lambda name: ".mlp.fc1" in name or ".mlp.fc2" in name,
        "qkv": lambda name: ".attn.qkv" in name,
        "attn_proj": lambda name: ".attn.proj" in name,
        "patch_embed": lambda name: name.startswith("patch_embed.") and ".conv" in name,
    }
    # Support comma-separated multiple groups (e.g., "qkv,attn_proj")
    if "," in normalized:
        parts = [p.strip() for p in normalized.split(",")]
        for p in parts:
            if p not in selectors:
                raise ValueError(f"Unsupported protected group in list: {p}")
        return lambda name: any(selectors[p](name) for p in parts)
    if normalized not in selectors:
        raise ValueError(f"Unsupported protected group: {group}")
    return selectors[normalized]


def make_groupwise_setter(selector: Callable[[str], bool],
                          protected_nl_ltp: float,
                          protected_nl_ltd: float,
                          train_mode: bool,
                          use_second_order_ste: bool = False,
                          delta_g_eff: float = 0.0,
                          second_order_alpha: float = 1.0):
    def setter(model, exp_cfg):
        for name, module in model.named_modules():
            if not isinstance(module, AnalogModule):
                continue
            if train_mode:
                if exp_cfg.hat_training:
                    module.config.noise_enabled = exp_cfg.noise_enabled
                    module.config.sigma_c2c = exp_cfg.sigma_c2c
                elif exp_cfg.noise_enabled:
                    module.config.noise_enabled = True
                    module.config.sigma_c2c = 0.0
                else:
                    module.config.noise_enabled = False
                    module.config.sigma_c2c = 0.0
            else:
                module.config.noise_enabled = exp_cfg.noise_enabled
                module.config.sigma_c2c = exp_cfg.sigma_c2c

            module.config.sigma_d2d = exp_cfg.sigma_d2d
            module.config.noise_mode = exp_cfg.noise_mode
            if selector(name):
                module.config.NL_LTP = protected_nl_ltp
                module.config.NL_LTD = protected_nl_ltd
            else:
                module.config.NL_LTP = exp_cfg.nl_ltp
                module.config.NL_LTD = exp_cfg.nl_ltd
            # Propagate higher-order surrogate settings
            if use_second_order_ste:
                module.config.use_second_order_ste = True
                if delta_g_eff < 0:
                    # Auto-compute from the effective module configuration already
                    # written above. This keeps train/eval semantics aligned with
                    # the active C2C policy instead of the nominal exp_cfg values.
                    module.config.delta_g_eff = (
                        float(getattr(module.config, "sigma_d2d", 0.0))
                        + float(getattr(module.config, "sigma_c2c", 0.0))
                    )
                else:
                    module.config.delta_g_eff = delta_g_eff
                module.config.second_order_alpha = second_order_alpha
            else:
                module.config.use_second_order_ste = False
                module.config.delta_g_eff = 0.0
                module.config.second_order_alpha = 1.0

    return setter


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--protected-group", default="mlp")
    parser.add_argument("--protected-nl-ltp", type=float, default=1.0)
    parser.add_argument("--protected-nl-ltd", type=float, default=-1.0)
    parser.add_argument("--name-suffix", default="_groupwise_nl_comp")
    parser.add_argument("--use-second-order-ste", action="store_true", help="Enable 2nd-order Taylor-corrected STE (CX-J1d)")
    parser.add_argument("--delta-g-eff", type=float, default=-1.0, help="Effective perturbation scale for curvature correction (negative=auto, 0=literal zero)")
    parser.add_argument("--second-order-alpha", type=float, default=1.0, help="Scalar multiplier on the 2nd-order correction term")
    args, passthrough = parser.parse_known_args()

    selector = build_selector(args.protected_group)

    original_get_configs = base.get_v_experiment_configs

    def patched_get_configs(epochs: int = 100, batch_size: int = 64):
        configs = original_get_configs(epochs=epochs, batch_size=batch_size)
        for cfg in configs.values():
            if cfg.use_hybrid:
                cfg.name = f"{cfg.name}{args.name_suffix}"
        return configs

    base.get_v_experiment_configs = patched_get_configs
    base.set_noise_for_train = make_groupwise_setter(
        selector=selector,
        protected_nl_ltp=args.protected_nl_ltp,
        protected_nl_ltd=args.protected_nl_ltd,
        train_mode=True,
        use_second_order_ste=args.use_second_order_ste,
        delta_g_eff=args.delta_g_eff,
        second_order_alpha=args.second_order_alpha,
    )
    base.set_noise_for_eval = make_groupwise_setter(
        selector=selector,
        protected_nl_ltp=args.protected_nl_ltp,
        protected_nl_ltd=args.protected_nl_ltd,
        train_mode=False,
        use_second_order_ste=args.use_second_order_ste,
        delta_g_eff=args.delta_g_eff,
        second_order_alpha=args.second_order_alpha,
    )

    print(
        "Group-wise NL mitigation wrapper active: "
        f"group={args.protected_group}, "
        f"protected_nl=({args.protected_nl_ltp}, {args.protected_nl_ltd}), "
        f"name_suffix={args.name_suffix}, "
        f"2nd_order_ste={args.use_second_order_ste}, "
        f"delta_g_eff={args.delta_g_eff}, "
        f"second_order_alpha={args.second_order_alpha}"
    )

    sys.argv = [sys.argv[0]] + passthrough
    base.main()


if __name__ == "__main__":
    main()
