#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
SRC="$ROOT/archive/reorg_20260509/legacy_root_docs_20260510"

mv "$SRC/project/EXPERIMENT_PROTOCOL.md" "$ROOT/EXPERIMENT_PROTOCOL.md"
mv "$SRC/project/MASTER_PLAN.md" "$ROOT/MASTER_PLAN.md"
mv "$SRC/project/RELEASE_CHECKLIST.md" "$ROOT/RELEASE_CHECKLIST.md"
mv "$SRC/reproducibility/README_REPRODUCIBILITY_PAPER1.md" "$ROOT/README_REPRODUCIBILITY_PAPER1.md"
mv "$SRC/reproducibility/REPRODUCIBILITY.md" "$ROOT/REPRODUCIBILITY.md"
mv "$SRC/workspace/ROOT_REORG_PLAN_20260509.md" "$ROOT/ROOT_REORG_PLAN_20260509.md"
mv "$SRC/workspace/WORKSPACE_FINAL_CLEAN_STATUS_20260510.md" "$ROOT/WORKSPACE_FINAL_CLEAN_STATUS_20260510.md"
mv "$SRC/workspace/WORKSPACE_LAYOUT_V2_20260509.md" "$ROOT/WORKSPACE_LAYOUT_V2_20260509.md"

rmdir "$SRC/project" "$SRC/reproducibility" "$SRC/workspace" "$SRC" 2>/dev/null || true
