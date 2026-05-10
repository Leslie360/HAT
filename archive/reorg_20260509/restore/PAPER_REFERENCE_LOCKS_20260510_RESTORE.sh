#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../../.."

printf 'Restoring Paper1 reference locks to paper/ ...\n'

test -d paper1/provenance/reference_locks
for name in CANONICAL_RESULT_LOCK_gpt.md CREDIT.md FIGURE_CAPTION_LOCK_gpt.md FIGURE_PLAN.md; do
  test -f "paper1/provenance/reference_locks/$name"
  if [ -e "paper/$name" ] && [ ! -L "paper/$name" ]; then
    printf 'Refusing: paper/%s exists and is not a symlink.\n' "$name" >&2
    exit 1
  fi
  rm -f "paper/$name"
  mv "paper1/provenance/reference_locks/$name" "paper/$name"
done
rmdir paper1/provenance/reference_locks 2>/dev/null || true

printf 'Restore complete. Re-run symlink/docs validation before continuing active work.\n'
