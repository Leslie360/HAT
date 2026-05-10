#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../../.."

printf 'Restoring paper helper scripts to paper/ ...\n'

for name in plot_paper_figures.py generate_schematic_figures_gpt.py fix_plots.py; do
  test -f "tools/plotting/$name"
  if [ -e "paper/$name" ] && [ ! -L "paper/$name" ]; then
    printf 'Refusing: paper/%s exists and is not a symlink.\n' "$name" >&2
    exit 1
  fi
  rm -f "paper/$name"
  mv "tools/plotting/$name" "paper/$name"
done

python3 - <<'PY'
from pathlib import Path
for rel in ["paper/plot_paper_figures.py", "paper/generate_schematic_figures_gpt.py"]:
    p = Path(rel)
    txt = p.read_text()
    txt = txt.replace("ROOT = Path(__file__).resolve().parents[2]", "ROOT = Path(__file__).resolve().parents[1]")
    p.write_text(txt)
PY

printf 'Restore complete. Re-run symlink/docs validation before continuing active work.\n'
