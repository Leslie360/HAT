# DS-5: GitHub Clean Branch Checklist

Date: 2026-05-01
Goal: Human-safe checklist for preparing a public GitHub repository from the working directory.

## Codex correction note (2026-05-01)

This checklist was reviewed against the live tree. Execute the corrected paths below, not the older `scripts/check_*.py` form:

- `scripts/_gpt/check_locked_numbers.py`
- `scripts/_gpt/check_local_pcm_precision_ladder.py`

Also note the checkpoint-directory tension: public release should not include `.pt` checkpoints, but canonical `fresh_eval.json`, `drift_eval.json`, and `training_history.json` under checkpoint folders are evidence files. Before public push, either copy those JSONs into `paper/latex_gpt/source_data/canonical_json/` or force-add only the JSON files while still excluding `.pt`.

## Warnings (Read First)

- **NEVER run `git reset --hard`** — this destroys uncommitted work
- **NEVER delete files without `git status` verification first**
- **Keep a separate clean branch** — do not modify `master` or `main` directly
- The working directory contains agent chat logs (`.codex/`, `report_md/_gpt/`), large checkpoints, and experimental outputs — these are local artifacts, not paper artifacts

## Checklist

### Step 1: Verify Current State

```bash
cd /home/qiaosir/projects/compute_vit
git status
git branch  # confirm you are NOT on master/main
```

Ensure you are on a dedicated publishing branch (e.g., `publication-v1`). If not, create one:

```bash
git checkout -b publication-v1
```

### Step 2: Create .gitignore for Public Repo

Add to `.gitignore`:

```
# Large artifacts
paper2_aihwkit_baseline/checkpoints/
paper2_aihwkit_baseline/logs/
outputs/
notebooks/

# Agent/internal communication
report_md/
.codex/
AGENT_INTERCOM_HUB_*.md
broadcast.md

# Paper orchestration
paper_orchestra_input/

# Python
__pycache__/
*.pyc
venv/
.env

# LaTeX build
*.aux
*.out
*.toc
*.bbl
*.blg
*.fdb_latexmk
*.fls
*.synctex.gz

# Data (auto-downloaded)
data/
```

### Step 3: Staging — What to Include

| Include | Path | Reason |
|:--------|:-----|:-------|
| ✅ Paper source | `paper/latex_gpt/*.tex` | Main text |
| ✅ SI source | `paper/latex_gpt/supplementary.tex` | Supplementary |
| ✅ SI sections | `paper/latex_gpt/supplementary/*.tex` | Sub-sections |
| ✅ Bibliography | `paper/latex_gpt/refs_gpt.bib` | References |
| ✅ Figures | `paper/latex_gpt/figures/*.pdf` | Compiled figures |
| ✅ TikZ sources | `paper/latex_gpt/figures/tikz/*.tex` | Figure generators |
| ✅ Source data | `paper/latex_gpt/source_data/*.csv` | Locked number CSVs |
| ✅ Source data | `paper/latex_gpt/source_data/*.json` | Manifest JSONs |
| ✅ Scripts | `scripts/_gpt/check_locked_numbers.py` | Verification |
| ✅ Scripts | `paper2_aihwkit_baseline/*.py` | Training/eval code |
| ✅ Scripts | `paper2_aihwkit_baseline/*.sh` | Run scripts |
| ✅ Protocol | `paper2_aihwkit_baseline/PCM_PROTOCOL.md` | Methods |
| ✅ Locked numbers | `outputs/CANONICAL_NUMBERS_FROZEN_20260430.md` | Results |
| ❌ Checkpoints | `paper2_aihwkit_baseline/checkpoints/*.pt` | Too large |
| ❌ Agent logs | `report_md/_gpt/*.md` | Internal |
| ❌ Eval JSONs | Include only as source_data | Already captured |
| ❌ Notebooks | `notebooks/` | Exploratory |

### Step 4: Stage and Commit

```bash
# Verify what will be committed
git status

# Stage paper source
git add paper/latex_gpt/

# Stage scripts
git add scripts/_gpt/check_locked_numbers.py scripts/_gpt/check_local_pcm_precision_ladder.py

# Stage protocol and locked numbers
git add paper2_aihwkit_baseline/PCM_PROTOCOL.md outputs/CANONICAL_NUMBERS_FROZEN_20260430.md

# Stage training scripts (no checkpoints)
git add paper2_aihwkit_baseline/*.py paper2_aihwkit_baseline/*.sh

# Commit
git commit -m "Paper 1 source: precision-aware analog training with PCM"
```

### Step 5: Verify No Secrets

```bash
# Check for accidental credential inclusion
git diff --cached | grep -i "password\|api_key\|secret\|token" || echo "No secrets found"

# Check file sizes
git diff --cached --stat | sort -k4 -h | tail -5
```

### Step 6: Push (Only When Ready)

```bash
# First push to a private fork for review
git push origin publication-v1

# After confirming the diff is clean:
# git push public publication-v1:main
```

## Recommended Branch Structure

```
main / master          ← development branch (keep local)
├── publication-v1     ← paper submission branch (push to private repo)
├── public-v1          ← cleaned branch for GitHub release (push to public)
└── thesis             ← separate thesis branch (keep local)
```

## Large File Policy

- Do not commit checkpoints (`.pt` files) — these are 80 MB each
- Do not commit CIFAR-10 data — auto-downloaded by torchvision
- Do not commit conda environments — use `conda env export > environment.yml` instead
- Maximum file size target for public repo: <10 MB per file

## Pre-Push Verification Commands

```bash
# Check for large files in staged
git diff --cached --name-only | xargs -I{} sh -c 'wc -c "$1" 2>/dev/null || true' _ {} | sort -rn | head -10

# Verify no .pt files
git diff --cached --name-only | grep '\.pt$' && echo "WARNING: checkpoints staged!" || echo "OK: no checkpoints"

# Run locked-number verification
python scripts/_gpt/check_locked_numbers.py  # should show 22/22 PASS
python scripts/_gpt/check_local_pcm_precision_ladder.py  # should show PASS

# Dry-run the public push
git push --dry-run origin publication-v1
```
