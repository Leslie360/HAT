#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STAMP="$(date +%Y%m%d_%H%M%S)"
OUT_DIR="${1:-$ROOT/outputs/remote_github_handoff_$STAMP}"
PKG_DIR="$OUT_DIR/compute_vit_remote_handoff"
MANIFEST="$PKG_DIR/HANDOFF_MANIFEST.txt"

rm -rf "$PKG_DIR"
mkdir -p "$PKG_DIR"

copy_top_level_files() {
  find "$ROOT" -maxdepth 1 -type f \
    \( -name '*.py' -o -name '*.sh' -o -name '*.md' -o -name '*.txt' -o -name '*.json' -o -name '*.csv' -o -name '*.yml' -o -name '*.yaml' \) \
    ! -name '*.pdf' ! -name '*.pptx' ! -name '*.docx' ! -name '*.log' \
    -print0 | while IFS= read -r -d '' f; do
      cp -a "$f" "$PKG_DIR/"
    done
}

copy_tree() {
  local rel="$1"
  rm -rf "$PKG_DIR/$rel"
  cp -a "$ROOT/$rel" "$PKG_DIR/$rel"
  find "$PKG_DIR/$rel" -type d -name '__pycache__' -prune -exec rm -rf {} +
  find "$PKG_DIR/$rel" -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
}

copy_selected_report_payloads() {
  rm -rf "$PKG_DIR/report_md"
  mkdir -p "$PKG_DIR/report_md/_gpt/json_gpt" "$PKG_DIR/report_md/_gpt/csv_gpt"

  find "$ROOT/report_md/_gpt" -maxdepth 1 -type f \
    \( -name '*.md' -o -name '*.json' -o -name '*.csv' -o -name '*.txt' \) \
    -print0 | while IFS= read -r -d '' f; do
      cp -a "$f" "$PKG_DIR/report_md/_gpt/"
    done

  find "$ROOT/report_md/_gpt/json_gpt" -maxdepth 1 -type f -name '*.json' \
    -print0 | while IFS= read -r -d '' f; do
      cp -a "$f" "$PKG_DIR/report_md/_gpt/json_gpt/"
    done

  find "$ROOT/report_md/_gpt/csv_gpt" -maxdepth 1 -type f -name '*.csv' \
    -print0 | while IFS= read -r -d '' f; do
      cp -a "$f" "$PKG_DIR/report_md/_gpt/csv_gpt/"
    done
}

copy_lightweight_paper_utils() {
  rm -rf "$PKG_DIR/paper"
  mkdir -p "$PKG_DIR/paper"
  find "$ROOT/paper" -maxdepth 1 -type f -name '*.py' \
    -print0 | while IFS= read -r -d '' f; do
      cp -a "$f" "$PKG_DIR/paper/"
    done
}

copy_baseline_checkpoint() {
  rm -rf "$PKG_DIR/checkpoints"
  mkdir -p "$PKG_DIR/checkpoints/_ensemble"
  cp -a "$ROOT/checkpoints/V4_hybrid_standard_noise_hat_best.pt" \
    "$PKG_DIR/checkpoints/V4_hybrid_standard_noise_hat_best.pt"
  cp -a "$ROOT/checkpoints/V4_hybrid_standard_noise_hat_best.pt" \
    "$PKG_DIR/checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt"
}

write_handoff_docs() {
  mkdir -p "$PKG_DIR/docs"

  cat > "$PKG_DIR/README_REMOTE_GITHUB.md" <<'EOF'
# Remote GitHub Mirror

This package is a broader execution-oriented mirror for remote GPU work.

Read in this order:
1. `docs/KEY_SOURCE_SYNC_20260422.md`
2. `docs/REMOTE_SERVER_GITHUB_HANDOFF.md`
3. `远端/INDEX.md`
4. `report_md/_gpt/AGENT_SYNC_gpt.md`

This mirror is still curated. It intentionally excludes:
- raw private data
- bulky logs
- most checkpoint families
- large manuscript binaries

Use it as the remote execution mirror, not as a full archival snapshot.
EOF

  cat > "$PKG_DIR/PUSH_TO_GITHUB.md" <<'EOF'
# Push To GitHub

SSH exact copy-paste block:

```bash
cd /home/qiaosir/projects/compute_vit/outputs/remote_github_handoff_YYYYMMDD_HHMMSS/compute_vit_remote_handoff
git init
git checkout -B remote-exploration
git add .
git commit -m "remote exploration handoff"
git remote remove origin 2>/dev/null || true
git remote add origin git@github.com:Leslie360/HAT.git
git push -u origin remote-exploration --force
```
EOF

  cat > "$PKG_DIR/docs/KEY_SOURCE_SYNC_20260422.md" <<'EOF'
# Key Source Sync 2026-04-22

This remote branch now carries a broader local source mirror.

Included:
- top-level execution-relevant source/config files (`*.py`, `*.sh`, `*.md`, `*.txt`, `*.json`, `*.csv`, `*.yml`, `*.yaml`)
- full `scripts/`
- full `docs/`
- full `device_profiles/`
- full `远端/`
- `report_md/_gpt/` top-level markdown/json/csv/txt plus `json_gpt/` and `csv_gpt/`
- lightweight `paper/*.py`
- one approved baseline checkpoint:
  - `checkpoints/V4_hybrid_standard_noise_hat_best.pt`
  - duplicate at `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt`

Excluded intentionally:
- raw datasets
- bulky logs
- manuscript PDFs/PPTX/DOCX
- large checkpoint families beyond the single baseline
- `.git/`, caches, temp outputs

Use this branch as the remote execution mirror. Do not assume the main local worktree is available.
EOF
}

copy_top_level_files
copy_tree "scripts"
copy_tree "docs"
copy_tree "device_profiles"
copy_tree "远端"
copy_selected_report_payloads
copy_lightweight_paper_utils
copy_baseline_checkpoint
write_handoff_docs

find "$PKG_DIR" -type f ! -path '*/.git/*' | sed "s#^$PKG_DIR/##" | sort > "$MANIFEST"

echo "Created remote GitHub handoff directory:"
echo "  $PKG_DIR"
echo
echo "Manifest:"
echo "  $MANIFEST"
echo
echo "Included file count:"
wc -l < "$MANIFEST"
