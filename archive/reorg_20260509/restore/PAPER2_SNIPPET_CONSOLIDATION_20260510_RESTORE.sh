#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../../.."

printf 'Restoring Paper2 manuscript snippet compatibility layout...\n'

test -d paper2/manuscript/snippets

if [ -e manuscripts/paper2/snippets ] && [ ! -L manuscripts/paper2/snippets ]; then
  printf 'Refusing: manuscripts/paper2/snippets exists and is not a symlink.\n' >&2
  exit 1
fi

rm -f manuscripts/paper2/snippets
mkdir -p manuscripts/paper2
mv paper2/manuscript/snippets manuscripts/paper2/snippets
rmdir paper2/manuscript 2>/dev/null || true

rm -f paper2_aihwkit_baseline/r10e_tex_paragraph.tex
ln -s ../manuscripts/paper2/snippets/r10e_tex_paragraph.tex paper2_aihwkit_baseline/r10e_tex_paragraph.tex

printf 'Restore complete. Re-run symlink/docs validation before continuing active work.\n'
