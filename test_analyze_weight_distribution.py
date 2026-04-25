#!/usr/bin/env python3
"""Smoke-test the weight-distribution analyzer self-check."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "scripts" / "_gpt" / "analyze_weight_distribution.py"


def main() -> None:
    subprocess.run([sys.executable, str(SCRIPT), "--self-check"], cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
