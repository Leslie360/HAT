#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../../.."

printf 'Restoring Paper1 manuscript/provenance compatibility layout...\n'

test -d paper1/manuscript
test -d paper1/provenance/manifests
test -d paper1/provenance/asset_archive

if [ -e manuscripts/paper1/src ] && [ ! -L manuscripts/paper1/src ]; then
  printf 'Refusing: manuscripts/paper1/src exists and is not a symlink.\n' >&2
  exit 1
fi
if [ -e manuscripts/paper1/manifests ] && [ ! -L manuscripts/paper1/manifests ]; then
  printf 'Refusing: manuscripts/paper1/manifests exists and is not a symlink.\n' >&2
  exit 1
fi
if [ -e manuscripts/paper1/asset_archive ] && [ ! -L manuscripts/paper1/asset_archive ]; then
  printf 'Refusing: manuscripts/paper1/asset_archive exists and is not a symlink.\n' >&2
  exit 1
fi

rm -f manuscripts/paper1/src manuscripts/paper1/manifests manuscripts/paper1/asset_archive
mv paper1/manuscript manuscripts/paper1/src
mv paper1/provenance/manifests manuscripts/paper1/manifests
mv paper1/provenance/asset_archive manuscripts/paper1/asset_archive

while IFS= read -r link_path; do
  target=$(readlink "$link_path")
  case "$target" in
    ../../provenance/asset_archive/*)
      ln -snf "../../asset_archive/${target#../../provenance/asset_archive/}" "$link_path"
      ;;
    ../../../provenance/asset_archive/*)
      ln -snf "../../../asset_archive/${target#../../../provenance/asset_archive/}" "$link_path"
      ;;
  esac
done < <(find manuscripts/paper1/src/figures -type l 2>/dev/null | sort)

printf 'Restore complete. Re-run symlink/docs validation before continuing active work.\n'
