#!/usr/bin/env python3
"""Shared path/bootstrap helpers for release-safe scripts."""

from __future__ import annotations

import os
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent


def ensure_repo_root() -> Path:
    root_str = str(REPO_ROOT)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)
    return REPO_ROOT


def add_python_path(path: Path | str) -> Path:
    resolved = Path(path).expanduser().resolve()
    resolved_str = str(resolved)
    if resolved_str not in sys.path:
        sys.path.insert(0, resolved_str)
    return resolved


def resolve_crosssim_root(env_var: str = "CROSSSIM_ROOT") -> Path:
    explicit = os.environ.get(env_var)
    if explicit:
        return Path(explicit).expanduser().resolve()
    return (REPO_ROOT.parent / "cross-sim").resolve()


def configure_crosssim_paths(env_var: str = "CROSSSIM_ROOT") -> Path:
    crosssim_root = resolve_crosssim_root(env_var=env_var)
    if not crosssim_root.exists():
        raise FileNotFoundError(
            f"CrossSim root not found: {crosssim_root}. "
            f"Set {env_var} or clone cross-sim next to this repository."
        )
    add_python_path(crosssim_root)
    add_python_path(crosssim_root / "applications" / "dnn")
    return crosssim_root
