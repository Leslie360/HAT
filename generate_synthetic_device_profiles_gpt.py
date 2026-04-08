#!/usr/bin/env python3
"""Generate combinatorial synthetic device-profile libraries for development sweeps."""

from __future__ import annotations

import argparse
from itertools import product
from typing import List, Optional, Sequence

from device_profile_utils import (
    DEFAULT_DEVICE_PROFILES,
    DeviceProfile,
    dump_device_profiles_json,
    load_device_profiles_json,
    select_device_profile,
)


def parse_float_list(values: Sequence[str]) -> List[float]:
    return [float(v) for v in values]


def parse_int_list(values: Sequence[str]) -> List[int]:
    return [int(v) for v in values]


def resolve_base_profile(profile_json: Optional[str], profile_name: Optional[str]) -> DeviceProfile:
    if profile_json:
        return select_device_profile(load_device_profiles_json(profile_json), profile_name)
    return select_device_profile(DEFAULT_DEVICE_PROFILES, profile_name or "Organic OPECT")


def make_profile_name(prefix: str, dynamic_range: float, n_states: int,
                      sigma_c2c: float, sigma_d2d: float) -> str:
    return (
        f"{prefix}_dr{dynamic_range:g}_ns{n_states}_"
        f"c2c{sigma_c2c:.3f}_d2d{sigma_d2d:.3f}"
    )


def build_profiles(base: DeviceProfile, dynamic_ranges: Sequence[float], n_states_list: Sequence[int],
                   sigma_c2c_list: Sequence[float], sigma_d2d_list: Sequence[float],
                   gamma_phys_list: Sequence[Optional[float]], I_dark_list: Sequence[Optional[float]],
                   tau1_scale_list: Sequence[float], tau2_scale_list: Sequence[float],
                   prefix: str, profile_kind: str) -> List[DeviceProfile]:
    profiles: List[DeviceProfile] = []

    gamma_phys_values = gamma_phys_list or [base.gamma_phys]
    I_dark_values = I_dark_list or [base.I_dark]
    tau1_scale_values = tau1_scale_list or [1.0]
    tau2_scale_values = tau2_scale_list or [1.0]

    for dynamic_range, n_states, sigma_c2c, sigma_d2d, gamma_phys, I_dark, tau1_scale, tau2_scale in product(
        dynamic_ranges,
        n_states_list,
        sigma_c2c_list,
        sigma_d2d_list,
        gamma_phys_values,
        I_dark_values,
        tau1_scale_values,
        tau2_scale_values,
    ):
        tau_1 = None if base.tau_1 is None else base.tau_1 * tau1_scale
        tau_2 = None if base.tau_2 is None else base.tau_2 * tau2_scale
        notes = (
            f"synthetic from base={base.device_type}; "
            f"tau1_scale={tau1_scale:g}, tau2_scale={tau2_scale:g}"
        )
        profiles.append(DeviceProfile(
            device_type=make_profile_name(prefix, dynamic_range, n_states, sigma_c2c, sigma_d2d),
            dynamic_range=float(dynamic_range),
            n_states=int(n_states),
            sigma_c2c=float(sigma_c2c),
            sigma_d2d=float(sigma_d2d),
            source=f"synthetic grid from {base.device_type}",
            G_min=base.G_min,
            tau_1=tau_1,
            tau_2=tau_2,
            A_0=base.A_0,
            gamma_phys=gamma_phys,
            I_dark=I_dark,
            responsivity_alpha=base.responsivity_alpha,
            NL_LTP=base.NL_LTP,
            NL_LTD=base.NL_LTD,
            pulse_count_max=base.pulse_count_max,
            profile_kind=profile_kind,
            notes=notes,
        ))
    return profiles


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic device-profile JSON libraries.")
    parser.add_argument("--base-profile-json", type=str, default=None)
    parser.add_argument("--base-profile-name", type=str, default="Organic OPECT")
    parser.add_argument("--dynamic-ranges", nargs="+", default=["5", "10", "20"])
    parser.add_argument("--n-states", nargs="+", default=["8", "16", "32"])
    parser.add_argument("--sigma-c2c", nargs="+", default=["0.01", "0.05", "0.10"])
    parser.add_argument("--sigma-d2d", nargs="+", default=["0.03", "0.10", "0.20"])
    parser.add_argument("--gamma-phys", nargs="+", default=None)
    parser.add_argument("--i-dark", nargs="+", default=None)
    parser.add_argument("--tau1-scale", nargs="+", default=["1.0"])
    parser.add_argument("--tau2-scale", nargs="+", default=["1.0"])
    parser.add_argument("--prefix", type=str, default="SyntheticOrganic")
    parser.add_argument("--profile-kind", type=str, default="synthetic")
    parser.add_argument("--output", type=str, default="device_profiles/generated_synthetic_profiles_gpt.json")
    args = parser.parse_args()

    base = resolve_base_profile(args.base_profile_json, args.base_profile_name)
    profiles = build_profiles(
        base=base,
        dynamic_ranges=parse_float_list(args.dynamic_ranges),
        n_states_list=parse_int_list(args.n_states),
        sigma_c2c_list=parse_float_list(args.sigma_c2c),
        sigma_d2d_list=parse_float_list(args.sigma_d2d),
        gamma_phys_list=parse_float_list(args.gamma_phys) if args.gamma_phys else [],
        I_dark_list=parse_float_list(args.i_dark) if args.i_dark else [],
        tau1_scale_list=parse_float_list(args.tau1_scale),
        tau2_scale_list=parse_float_list(args.tau2_scale),
        prefix=args.prefix,
        profile_kind=args.profile_kind,
    )
    out_path = dump_device_profiles_json(
        args.output,
        profiles,
        source=f"synthetic_grid_from_{base.device_type}",
    )
    print(f"Generated {len(profiles)} profiles -> {out_path}")


if __name__ == "__main__":
    main()
