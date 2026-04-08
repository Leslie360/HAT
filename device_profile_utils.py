#!/usr/bin/env python3
"""Utilities for literature and measured device profile ingestion."""

from __future__ import annotations

import json
from dataclasses import asdict
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence


@dataclass(frozen=True)
class DeviceProfile:
    device_type: str
    dynamic_range: float
    n_states: int
    sigma_c2c: float
    sigma_d2d: float
    source: str
    noise_mode: str = "uniform"
    G_min: float = 1.0
    tau_1: Optional[float] = None
    tau_2: Optional[float] = None
    A_0: Optional[float] = None
    gamma_phys: Optional[float] = None
    I_dark: Optional[float] = None
    responsivity_alpha: Optional[float] = None
    NL_LTP: Optional[float] = None
    NL_LTD: Optional[float] = None
    pulse_count_max: Optional[int] = None
    profile_kind: str = "literature"
    notes: str = ""

    @property
    def G_max(self) -> float:
        return self.G_min * self.dynamic_range


DEFAULT_DEVICE_PROFILES: Sequence[DeviceProfile] = (
    DeviceProfile(
        "Organic OPECT",
        dynamic_range=10.0,
        n_states=16,
        sigma_c2c=0.05,
        sigma_d2d=0.10,
        noise_mode="uniform",
        source="Guo 2024 / handbook §2.1",
    ),
    DeviceProfile(
        "RRAM (HfOx)",
        dynamic_range=100.0,
        n_states=64,
        sigma_c2c=0.02,
        sigma_d2d=0.05,
        noise_mode="uniform",
        source="Alibart 2016; Prezioso 2015",
    ),
    DeviceProfile(
        "PCM (GST)",
        dynamic_range=50.0,
        n_states=32,
        sigma_c2c=0.03,
        sigma_d2d=0.08,
        noise_mode="uniform",
        source="Burr 2015; Ambrogio 2018",
    ),
    DeviceProfile(
        "Organic Pessimistic",
        dynamic_range=5.0,
        n_states=8,
        sigma_c2c=0.10,
        sigma_d2d=0.20,
        noise_mode="uniform",
        source="handbook pessimistic",
    ),
    DeviceProfile(
        "Ideal",
        dynamic_range=10.0,
        n_states=256,
        sigma_c2c=0.0,
        sigma_d2d=0.0,
        noise_mode="uniform",
        source="theoretical upper bound",
    ),
)


def _maybe_float(value):
    if value is None:
        return None
    return float(value)


def _extract_float(payload: dict, key: str, nested: Optional[dict], default=None):
    if key in payload:
        return float(payload[key])
    if nested and key in nested:
        return float(nested[key])
    if default is None:
        raise ValueError(f"Missing required device-profile field '{key}'")
    return float(default)


def _profile_from_payload(payload: dict, default_source: str) -> DeviceProfile:
    if not isinstance(payload, dict):
        raise ValueError("Each device profile payload must be a JSON object")

    noise = payload.get("noise") if isinstance(payload.get("noise"), dict) else {}
    retention = payload.get("retention") if isinstance(payload.get("retention"), dict) else {}
    photoresponse = payload.get("photoresponse") if isinstance(payload.get("photoresponse"), dict) else {}
    plasticity = payload.get("plasticity") if isinstance(payload.get("plasticity"), dict) else {}

    device_type = payload.get("device_type") or payload.get("name")
    if not device_type:
        raise ValueError("Each device profile needs 'device_type' or 'name'")

    G_min = float(payload.get("G_min", 1.0))
    if "dynamic_range" in payload:
        dynamic_range = float(payload["dynamic_range"])
    elif "G_max" in payload:
        G_max = float(payload["G_max"])
        dynamic_range = G_max / G_min
    else:
        raise ValueError("Each device profile needs 'dynamic_range' or 'G_max'")

    return DeviceProfile(
        device_type=str(device_type),
        dynamic_range=dynamic_range,
        n_states=int(payload["n_states"]),
        sigma_c2c=_extract_float(payload, "sigma_c2c", noise, default=0.0),
        sigma_d2d=_extract_float(payload, "sigma_d2d", noise, default=0.0),
        noise_mode=str(payload.get("noise_mode", noise.get("mode", "uniform"))),
        source=str(payload.get("source", default_source)),
        G_min=G_min,
        tau_1=_maybe_float(payload.get("tau_1", retention.get("tau_1"))),
        tau_2=_maybe_float(payload.get("tau_2", retention.get("tau_2"))),
        A_0=_maybe_float(payload.get("A_0", retention.get("A_0"))),
        gamma_phys=_maybe_float(payload.get("gamma_phys", photoresponse.get("gamma_phys"))),
        I_dark=_maybe_float(payload.get("I_dark", photoresponse.get("I_dark"))),
        responsivity_alpha=_maybe_float(payload.get("responsivity_alpha", photoresponse.get("responsivity_alpha", photoresponse.get("alpha")))),
        NL_LTP=_maybe_float(payload.get("NL_LTP", plasticity.get("NL_LTP"))),
        NL_LTD=_maybe_float(payload.get("NL_LTD", plasticity.get("NL_LTD"))),
        pulse_count_max=int(payload.get("pulse_count_max", plasticity.get("pulse_count_max"))) if payload.get("pulse_count_max", plasticity.get("pulse_count_max")) is not None else None,
        profile_kind=str(payload.get("profile_kind", "measured")),
        notes=str(payload.get("notes", "")),
    )


def load_device_profiles_json(path: str) -> List[DeviceProfile]:
    src_path = Path(path)
    with src_path.open("r", encoding="utf-8") as fh:
        payload = json.load(fh)

    default_source = str(src_path)
    if isinstance(payload, dict) and "profiles" in payload:
        raw_profiles = payload["profiles"]
        default_source = str(payload.get("source", default_source))
    else:
        raw_profiles = payload

    if isinstance(raw_profiles, dict):
        raw_profiles = [raw_profiles]

    if not isinstance(raw_profiles, list) or not raw_profiles:
        raise ValueError("Device profile JSON must contain a non-empty profile object or list")

    return [_profile_from_payload(item, default_source) for item in raw_profiles]


def select_device_profile(profiles: Sequence[DeviceProfile], profile_name: Optional[str]) -> DeviceProfile:
    if profile_name is None:
        if len(profiles) != 1:
            raise ValueError(
                "Profile JSON contains multiple entries; pass --profile-name to choose one"
            )
        return profiles[0]

    for profile in profiles:
        if profile.device_type == profile_name:
            return profile
    raise ValueError(
        f"Profile '{profile_name}' not found. Available profiles: "
        f"{', '.join(profile.device_type for profile in profiles)}"
    )


def profile_to_payload(profile: DeviceProfile) -> dict:
    payload = asdict(profile)
    payload["G_max"] = profile.G_max
    payload["noise"] = {
        "sigma_c2c": profile.sigma_c2c,
        "sigma_d2d": profile.sigma_d2d,
        "mode": profile.noise_mode,
    }
    payload["photoresponse"] = {
        "responsivity_alpha": profile.responsivity_alpha,
        "gamma_phys": profile.gamma_phys,
        "I_dark": profile.I_dark,
    }
    payload["plasticity"] = {
        "NL_LTP": profile.NL_LTP,
        "NL_LTD": profile.NL_LTD,
        "pulse_count_max": profile.pulse_count_max,
    }
    payload["retention"] = {
        "A_0": profile.A_0,
        "tau_1": profile.tau_1,
        "tau_2": profile.tau_2,
    }
    return payload


def dump_device_profiles_json(path: str, profiles: Sequence[DeviceProfile], source: str) -> str:
    payload = {
        "source": source,
        "profiles": [profile_to_payload(profile) for profile in profiles],
    }
    out_path = Path(path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    return str(out_path)
