#!/usr/bin/env bash
set -euo pipefail

DISTRO="${HOST_WSL_DISTRO:-Ubuntu-22.04}"
REPO_DIR="${HOST_WSL_REPO_DIR:-/home/qiaosir/projects/compute_vit}"

if [ "$#" -eq 0 ]; then
  echo "usage: $0 '<command>'" >&2
  exit 2
fi

CMD="$*"
"/mnt/c/Windows/System32/wsl.exe" -d "$DISTRO" bash -lc "cd '$REPO_DIR' && $CMD"
