#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../../.."

printf 'Restoring paper shell compatibility cleanup...\n'

if [ -d archive/reorg_20260509/paper2_legacy_drafts_20260510/paper/paper2 ]; then
  if [ -e paper/paper2 ]; then
    printf 'Refusing: paper/paper2 already exists.\n' >&2
    exit 1
  fi
  mkdir -p paper
  cp -a archive/reorg_20260509/paper2_legacy_drafts_20260510/paper/paper2 paper/paper2
elif [ -d archive/reorg_20260509/empty_compat_dirs_20260510/paper/paper2 ]; then
  if [ -e paper/paper2 ]; then
    printf 'Refusing: paper/paper2 already exists.\n' >&2
    exit 1
  fi
  mv archive/reorg_20260509/empty_compat_dirs_20260510/paper/paper2 paper/paper2
fi

while IFS= read -r link_path; do
  target=$(readlink "$link_path")
  case "$target" in
    ../../paper1/provenance/asset_archive/*)
      ln -snf "../../manuscripts/paper1/asset_archive/${target#../../paper1/provenance/asset_archive/}" "$link_path"
      ;;
    ../../../paper1/provenance/asset_archive/*)
      ln -snf "../../../manuscripts/paper1/asset_archive/${target#../../../paper1/provenance/asset_archive/}" "$link_path"
      ;;
  esac
done < <(find paper/figures -type l 2>/dev/null | sort)

printf 'Restore complete. Re-run symlink/docs validation before continuing active work.\n'
