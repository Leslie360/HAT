# Release Checklist

Use this checklist before publishing the repository, creating a public archive,
or attaching code to a submission.

## Release strategy

- Do not publish by zipping the working directory from `~/projects`.
- Prefer one of these two release paths:
  - create a dedicated public-release branch that removes internal trees
  - create a curated source archive from an allowlist of public files
- Treat the current workspace as a mixed environment containing both public
  code and internal materials.

## What should ship

The public release should contain the code and docs needed to install the
package, run the public smoke test, and understand the simulator boundary.

Keep at minimum:

- `README.md`
- `LICENSE`
- `requirements.txt`
- `requirements-optional.txt`
- `docs/`
- `device_profiles/`
- active source files in the repository root
- `scripts/run_public_smoke_test.sh`
- curated paper source files only if they are intentionally part of the
  release scope

## What must not ship

These paths are internal, generated, local-cache, or private-data areas and
must be excluded from any public release bundle:

- `_archive/`
- `logs/`
- `report_md/`
- `数据_博士/`
- `internal/`
- `outputs/`
- `checkpoints/`
- `data/`
- `__pycache__/`
- LaTeX build products such as `*.aux`, `*.bbl`, `*.blg`, `*.log`, `*.out`

Notes:

- `数据_博士/` is currently untracked, but it will leak immediately if you zip
  the workspace instead of creating a curated release.
- `report_md/` contains tracked internal reports and must not be assumed safe
  for public distribution just because it lives inside the repo.

## Repository hygiene

- Confirm `README.md` matches the current public scope and entrypoints.
- Confirm `LICENSE` is Apache 2.0 and the license section in `README.md`
  matches it.
- Confirm `docs/README.md` points users back to the repository root
  quickstart.
- Remove tracked `.pyc` files and `__pycache__/` artifacts from the release.
- Review `.gitignore` to ensure local artifacts are excluded without hiding
  source assets.
- Confirm public examples use generic measured-profile naming, not internal
  `doctor_*` names.

## Public preflight commands

Run these from the repository root in a clean environment before tagging a
release.

### 1. Install surface

```bash
python -m pip install -r requirements.txt
```

### 2. Public smoke test

```bash
bash scripts/run_public_smoke_test.sh
```

If your shell does not provide `python`, use:

```bash
PYTHON_BIN=python3 bash scripts/run_public_smoke_test.sh
```

### 3. Unit tests

```bash
python -m unittest discover -p 'test*.py'
```

### 4. Syntax compile

```bash
python - <<'PY'
import py_compile
from pathlib import Path

count = 0
for path in Path('.').rglob('*.py'):
    if '_archive' in path.parts or 'report_md' in path.parts:
        continue
    py_compile.compile(str(path), doraise=True)
    count += 1
print('compiled', count, 'python files')
PY
```

### 5. Release-facing leak scan

This scan intentionally excludes known-internal areas. It should print nothing.

```bash
python - <<'PY'
import subprocess
from pathlib import Path

patterns = [
    '/home/qiaosir',
    'DESKTOP-TLKV5NU',
    '2622507532@qq.com',
    'doctor_measured_profiles',
    'doctor_measured_profile',
    'DOCTOR_MEASURED_PROFILE_AUDIT',
    '数据_博士',
    'file:///home/qiaosir',
]
exclude_prefixes = ('_archive/', 'logs/', 'report_md/')

tracked = subprocess.check_output(['git', 'ls-files'], text=True).splitlines()
for path_str in tracked:
    if path_str.startswith(exclude_prefixes):
        continue
    path = Path(path_str)
    if not path.is_file():
        continue
    if path.suffix in {'.pdf', '.png', '.jpg', '.jpeg', '.pt', '.pth', '.pyc'}:
        continue
    text = path.read_text(encoding='utf-8', errors='ignore')
    for pat in patterns:
        if pat in text:
            print(f'{path}:{pat}')
PY
```

## Manual release review

- Check `git status --short` before packaging.
- Verify no private data or local caches were staged by accident.
- Verify the first command in `README.md` still works on a fresh clone.
- Verify the measured-profile demo still writes:
  - `measured_device_profiles.json`
  - `measured_device_profile_summary.json`
  - `MEASURED_DEVICE_PROFILE_AUDIT.md`
- Verify optional integrations are described as optional:
  - CrossSim
  - AIHWKIT
- Verify `README.md` does not require `report_md/` artifacts as runtime input.

## Packaging guidance

Preferred approach:

1. Create a public-release branch.
2. Remove internal trees from that branch.
3. Run the public preflight commands again on that branch.
4. Tag the release from that cleaned branch.

If a branch split is not practical, create a curated archive from an allowlist
of public files instead of publishing the raw repository checkout.

## Paper consistency

- Verify `best` vs `MC` numbers are not mixed.
- Verify Flowers-102 language remains hypothesis-level, not causal proof.
- Verify `Task 37` fresh-instance numbers and Zhang case-study numbers remain
  distinct.
- Recompile `paper/latex_gpt/main.tex` and confirm figure references resolve
  cleanly.

## Nature Communications submission packaging

- Confirm the first-submission manuscript file stays below the 30 MB
  single-file limit if text and figures are bundled together.
- Keep Supplementary Information as a separate upload and verify the compiled
  PDF matches the cited figure/table labels.
- Prepare a reviewer-accessible code archive or repository link for the custom
  code central to the main claims.
- Prepare source-data tables or a zipped raw-data bundle for graphs and charts
  so it can be supplied immediately if requested.
- Confirm overlapping or related manuscripts, reviewer
  suggestions/exclusions, and author-affiliation metadata are ready for the
  submission system.
