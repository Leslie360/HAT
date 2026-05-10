#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"

for f in "$ROOT/src/compute_vit"/*.py; do
  b="$(basename "$f")"
  [ "$b" = "__init__.py" ] && continue
  mv "$f" "$ROOT/$b"
done

rm -f "$ROOT/src/compute_vit/__init__.py"
rmdir "$ROOT/src/compute_vit" "$ROOT/src" 2>/dev/null || true
rm -f "$ROOT/cli"/*.py
rmdir "$ROOT/cli" 2>/dev/null || true
rm -f "$ROOT/tests/conftest.py"
