# DS-4: Reviewer Reproducibility Bundle Plan

Date: 2026-05-01
Goal: Plan a reviewer reproducibility tarball (not the actual tarball unless asked).

## Codex correction note (2026-05-01)

This plan was reviewed against the live tree. Two path/protocol details were corrected:

- verification scripts live under `scripts/_gpt/`, not `scripts/`;
- canonical PCM runs completed the intended 100-epoch schedule, but not every wrapper used the same `--early-stop-patience 0` CLI. At least one canonical 6-bit run used `patience=10` and did not trigger early stop. Public documentation should state completion/provenance from `training_history.json`, not a uniform patience flag.

## 1. Proposed Bundle Contents

### 1.1 Canonical Results (locked numbers)

| File | Description | Size estimate |
|:-----|:------------|:--------------|
| `outputs/CANONICAL_NUMBERS_FROZEN_20260430.md` | Locked number table | <1 KB |
| `paper2_aihwkit_baseline/PCM_PROTOCOL.md` | PCM evaluation protocol | <1 KB |
| `paper2_aihwkit_baseline/checkpoints/*/fresh_eval.json` | Fresh eval JSONs (9 seeds) | ~200 KB total |
| `paper2_aihwkit_baseline/checkpoints/*/drift_eval.json` | Drift eval JSONs (9 seeds) | ~50 KB total |
| `paper2_aihwkit_baseline/checkpoints/*/training_history.json` | Training history (9 seeds) | ~200 KB total |

### 1.2 Scripts Needed to Regenerate Numbers

| Script | Purpose | GPU needed? | CPU-only fallback? |
|:-------|:--------|:------------|:-------------------|
| `paper2_aihwkit_baseline/r11d4_train_pcm.py` | PCM UnitCell training | Yes | No |
| `paper2_aihwkit_baseline/eval_aihwkit_fresh.py` | Fresh-instance eval | Yes | No |
| `paper2_aihwkit_baseline/eval_aihwkit_drift.py` | Drift eval | Yes | No |
| `scripts/_gpt/check_locked_numbers.py` | Verify locked numbers match JSONs | No | Yes |
| `scripts/_gpt/check_local_pcm_precision_ladder.py` | PCM ladder consistency | No | Yes |

### 1.3 Figure Source Data

| Data | Path | CPU-regenerable? |
|:-----|:-----|:-----------------|
| PCM precision ladder table CSV | `paper/latex_gpt/source_data/tab_pcm_precision_ladder.csv` | Yes |
| Paper spine table CSV | `paper/latex_gpt/source_data/fig1_paper1_spine.csv` | Yes |
| Legacy SI figure data | `paper/latex_gpt/source_data/legacy/` (if reconstructed by DS-1) | Depends |

### 1.4 Main Text / SI Source

| File | Purpose |
|:-----|:--------|
| `paper/latex_gpt/main.tex` | Paper body |
| `paper/latex_gpt/supplementary.tex` | Supplementary Information |
| `paper/latex_gpt/refs_gpt.bib` | Bibliography |
| `paper/latex_gpt/supplementary/*.tex` | SI sub-sections |
| `paper/latex_gpt/figures/*.pdf` | Compiled figures |

## 2. Files to EXCLUDE

| Path | Reason |
|:-----|:-------|
| `paper2_aihwkit_baseline/checkpoints/*/best.pt` | 80 MB each, 18+ checkpoints = 1.5+ GB |
| `paper2_aihwkit_baseline/checkpoints/*/last.pt` | Duplicate of best.pt |
| `paper2_aihwkit_baseline/logs/` | Training logs (bulky, redundant with JSONs) |
| `paper2_aihwkit_baseline/checkpoints/t13v2*/` | Pre-canonical checkpoints (superseded by canonical runs) |
| `report_md/_gpt/` | Agent chat logs (internal) |
| `outputs/` except canonical files | Stale diagnostic outputs |
| `notebooks/` | Exploratory notebooks |
| `paper_orchestra_input/` | Orchestration configs |
| `venv/`, `__pycache__/`, `.git/` | Standard excludes |
| `*.log`, `*.aux`, `*.out`, `*.toc`, `*.bbl`, `*.blg` | LaTeX build artifacts |
| `data/` | CIFAR-10 dataset (auto-downloaded by torchvision) |

## 3. Proposed README_REPRODUCIBILITY.md Outline

```markdown
# Reproducibility Notes for "Precision-Aware Analog Training"

## Hardware Requirements
- GPU with ≥16 GB VRAM recommended for full training (RTX 5070 Ti used)
- CPU-only: evaluation scripts and locked-number verification work without GPU

## Environment
conda env create -f environment.yml  # or paper2_aihwkit_baseline/requirements.txt

## Locked Numbers
See outputs/CANONICAL_NUMBERS_FROZEN_20260430.md
All locked numbers are backed by JSON files in paper2_aihwkit_baseline/checkpoints/*/

## Quick Verification (CPU, <5 min)
python scripts/_gpt/check_locked_numbers.py
python scripts/_gpt/check_local_pcm_precision_ladder.py

## Full Regeneration (GPU, ~4h per seed × 9 seeds)
# Requires CUDA. Each PCM precision-ladder seed trains for 100 epochs.
bash paper2_aihwkit_baseline/run_kimi_r11d_batch_bc_20260430.sh

## Figure Regeneration
- TikZ figures: compile paper/latex_gpt/main.tex (pdflatex)
- Data-driven figures: source CSVs in paper/latex_gpt/source_data/

## Protocol Notes
- Canonical PCM precision-ladder artifacts completed the intended 100-epoch schedule; use `training_history.json` and provenance fields as the source of truth for early-stop status.
- Drift eval reads pcm_preset from checkpoint (no fallback)
- Fresh eval forces enable_during_test=True after checkpoint load

## Manifest
SHA256 sums: see MANIFEST_SHA256SUMS.txt
```

## 4. MANIFEST_SHA256SUMS.txt Generation

```bash
# Run from project root. Only include bundle files, not checkpoints.
cd /home/qiaosir/projects/compute_vit
find outputs/CANONICAL_NUMBERS_FROZEN_20260430.md \
     paper2_aihwkit_baseline/PCM_PROTOCOL.md \
     paper2_aihwkit_baseline/*.py \
     paper2_aihwkit_baseline/*.sh \
     paper/latex_gpt/*.tex \
     paper/latex_gpt/supplementary/*.tex \
     paper/latex_gpt/refs_gpt.bib \
     paper/latex_gpt/source_data/*.csv \
     paper/latex_gpt/source_data/*.json \
     -type f | sort | xargs sha256sum > MANIFEST_SHA256SUMS.txt
```

## 5. Bundle Creation Command (DRY RUN — not executed)

```bash
cd /home/qiaosir/projects/compute_vit
tar czf ../paper1_reproducibility_$(date +%Y%m%d).tar.gz \
    --exclude='*.pt' \
    --exclude='__pycache__' \
    --exclude='*.log' \
    --exclude='*.aux' \
    --exclude='.git' \
    --exclude='checkpoints/best.pt' \
    --exclude='checkpoints/last.pt' \
    --exclude='data/' \
    --exclude='report_md/' \
    --exclude='notebooks/' \
    --exclude='outputs/' \
    --exclude='venv/' \
    outputs/CANONICAL_NUMBERS_FROZEN_20260430.md \
    paper2_aihwkit_baseline/ \
    paper/latex_gpt/ \
    scripts/_gpt/check_locked_numbers.py \
    scripts/_gpt/check_local_pcm_precision_ladder.py \
    MANIFEST_SHA256SUMS.txt \
    README_REPRODUCIBILITY.md
```

Estimated tarball size (without checkpoints): **~5-10 MB**

## 6. Risks

| Risk | Mitigation |
|:-----|:-----------|
| Checkpoint paths hardcoded in eval JSONs | Document base path in README |
| Python/pinned dependency availability | Provide requirements.txt / environment.yml |
| GPU time for full regeneration | Point to pre-computed JSONs as primary evidence |
| AIHWKit version sensitivity | Pin `aihwkit==0.2.0` or later in requirements |
| LaTeX build differences | Provide compiled PDF in bundle |
