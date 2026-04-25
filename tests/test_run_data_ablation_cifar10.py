#!/usr/bin/env python3
"""Smoke-test the CIFAR-10 data ablation wrapper self-check."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "scripts" / "_gpt" / "run_data_ablation_cifar10.py"


def main() -> None:
    subprocess.run([sys.executable, str(SCRIPT), "--self-check"], cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
