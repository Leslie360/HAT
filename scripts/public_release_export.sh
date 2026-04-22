#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STAMP="$(date +%Y%m%d_%H%M%S)"
OUT_PATH="${1:-$ROOT/outputs/release_exports/compute_vit_public_release_${STAMP}.tar.gz}"
ARCHIVE_DIRNAME="compute_vit_public_release"

TMPDIR="$(mktemp -d)"
PKG_DIR="$TMPDIR/$ARCHIVE_DIRNAME"
MANIFEST_PATH="$PKG_DIR/PUBLIC_RELEASE_MANIFEST.txt"

cleanup() {
  rm -rf "$TMPDIR"
}
trap cleanup EXIT

mkdir -p "$PKG_DIR"
mkdir -p "$(dirname "$OUT_PATH")"

should_include() {
  local path="$1"
  case "$path" in
    _archive/*|logs/*|report_md/*|数据_博士/*|internal/*|outputs/*|checkpoints/*|data/*|AGENT_SYNC/*)
      return 1
      ;;
    __pycache__/*|*/__pycache__/*|*.pyc|*.pyo)
      return 1
      ;;
    scripts/_gpt/profile_auto_fitter_gpt.py)
      return 0
      ;;
    scripts/_gpt/*)
      return 1
      ;;
    paper/latex_gpt/*.aux|paper/latex_gpt/*.bbl|paper/latex_gpt/*.blg|paper/latex_gpt/*.fdb_latexmk|paper/latex_gpt/*.fls|paper/latex_gpt/*.log|paper/latex_gpt/*.out|paper/latex_gpt/*.synctex.gz)
      return 1
      ;;
  esac
  return 0
}

copy_tracked_files() {
  cd "$ROOT"
  : > "$MANIFEST_PATH"
  while IFS= read -r -d '' path; do
    if ! should_include "$path"; then
      continue
    fi
    mkdir -p "$PKG_DIR/$(dirname "$path")"
    cp -a "$ROOT/$path" "$PKG_DIR/$path"
    printf '%s\n' "$path" >> "$MANIFEST_PATH"
  done < <(git ls-files -z)
}

verify_staged_tree() {
  local matches
  matches="$(
    rg -n -I \
      -e '/home/qiaosir' \
      -e 'DESKTOP-TLKV5NU' \
      -e '2622507532@qq.com' \
      -e 'doctor_measured_profiles' \
      -e 'doctor_measured_profile' \
      -e 'DOCTOR_MEASURED_PROFILE_AUDIT' \
      -e 'file:///home/qiaosir' \
      -e '数据_博士' \
      "$PKG_DIR" || true
  )"
  if [[ -n "$matches" ]]; then
    echo "Public release export failed: staged tree contains private or legacy markers." >&2
    echo "$matches" >&2
    exit 1
  fi
}

write_metadata() {
  cat > "$PKG_DIR/PUBLIC_RELEASE_NOTES.md" <<EOF
# Public Release Notes

This archive was generated from a curated export script rather than by zipping
the raw working directory.

Generated at: $(date -Iseconds)
Archive filename: $(basename "$OUT_PATH")

Excluded classes:

- internal coordination and archive trees
- logs and generated reports
- checkpoints, datasets, and local outputs
- private raw-data trees
- Python bytecode and LaTeX build artifacts

Start with:

\`\`\`bash
bash scripts/run_public_smoke_test.sh
\`\`\`
EOF
}

create_archive() {
  tar -czf "$OUT_PATH" -C "$TMPDIR" "$ARCHIVE_DIRNAME"
}

copy_tracked_files
write_metadata
verify_staged_tree
create_archive

echo "Created curated public release archive:"
echo "  $OUT_PATH"
echo
echo "Archive root:"
echo "  $ARCHIVE_DIRNAME/"
echo
echo "Included file count:"
wc -l < "$MANIFEST_PATH"
