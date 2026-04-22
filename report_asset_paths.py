#!/usr/bin/env python3
"""Shared helpers for keeping report assets organized."""

import os


def _is_gpt_output_dir(output_dir: str) -> bool:
    return os.path.basename(os.path.normpath(output_dir)) == "_gpt"


def asset_subdir(output_dir: str, kind: str) -> str:
    if kind not in {"image", "csv", "json"}:
        raise ValueError(f"Unknown asset kind: {kind}")

    if _is_gpt_output_dir(output_dir):
        mapping = {
            "image": "images_gpt",
            "csv": "csv_gpt",
            "json": "json_gpt",
        }
    else:
        mapping = {
            "image": "images",
            "csv": "csv",
            "json": "json",
        }
    return mapping[kind]


def ensure_asset_dirs(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    for kind in ("image", "csv", "json"):
        os.makedirs(os.path.join(output_dir, asset_subdir(output_dir, kind)), exist_ok=True)


def asset_path(output_dir: str, kind: str, filename: str) -> str:
    ensure_asset_dirs(output_dir)
    return os.path.join(output_dir, asset_subdir(output_dir, kind), filename)


def asset_ref(output_dir: str, kind: str, filename: str) -> str:
    """Return markdown-friendly relative path from the report root."""
    return f"{asset_subdir(output_dir, kind)}/{filename}"
