# Kimi P7 Track B: Git Hygiene and Commit Scope

**Date:** 2026-05-09
**Auditor:** kimi
**Scope:** `/home/qiaosir/projects/compute_vit` working tree

---

## 1. Git Status Inventory

| Category | Count | Description |
|----------|-------|-------------|
| Modified (`M`) | 96 | Active paper sources, figures, thesis, canonical JSON, source data |
| Deleted (`D`) | 30 | `.kimi_draft*` files (already removed by P6 cleanup) |
| Untracked (`??`) | 332 | Mixed: build residues, temp files, remote review data, ChatGPT images, deprecated dirs |

---

## 2. Modified Files Grouped by Category

### 2.1 Paper Active (Safe to Commit)

| Path Pattern | Files | Note |
|--------------|-------|------|
| `paper/latex_gpt/*.tex` | main.tex, supplementary.tex, cover_letter.tex | Core manuscript |
| `paper/latex_gpt/sections/*.tex` | 00_abstract through 07_conclusion | Main sections |
| `paper/latex_gpt/supplementary/*.tex` | S_energy, S_hardware, S_mechanism, S_opect, S_repro, S_theory, S_tooling | Supplementary sections |
| `paper/latex_gpt/figures/tikz/*.tex` | fig1_system_architecture, fig2_weight_mapping | TikZ sources |
| `paper/latex_gpt/refs_gpt.bib` | 1 | Bibliography |
| `paper/latex_gpt/source_data/*.csv` | fig1_spine, fig2_decision_map, tab_pcm_precision_ladder | Source data tables |
| `paper/latex_gpt/source_data/canonical_json/*/fresh_eval.json` | pcm_6bit_seed123, pcm_6bit_seed789 | Updated evals |
| `paper/latex_gpt/source_data/canonical_json/*/drift_eval.json` | pcm_6bit_seed123, pcm_6bit_seed789 | Updated evals |
| `paper/latex_gpt/source_data/canonical_json/*/training_history.json` | pcm_6bit_seed123, pcm_6bit_seed789 | Updated histories |
| `paper/latex_gpt/source_data/canonical_json/README.md` | 1 | Manifest readme |

### 2.2 Generated Figures (Safe to Commit — Vector/PNG)

| Path Pattern | Count | Note |
|--------------|-------|------|
| `paper/figures/*.png` | 9 | Main figure PNGs |
| `paper/latex_gpt/figures/*.png` | 9 | LaTeX figure PNGs |
| `paper/latex_gpt/figures/*.pdf` | 5 | Vector PDFs (fig1_spine, fig2_decision_map, fig2_weight_mapping, fig_nl_gradient_distortion) |

### 2.3 Thesis (Safe to Commit — Separate Scope)

| Path Pattern | Count | Note |
|--------------|-------|------|
| `paper/thesis/*.tex` | 8 | Thesis chapters 1-8 |
| `paper/thesis/*.pdf` | 1 | Compiled thesis PDF |
| `paper/thesis/*.bbl`, `*.blg` | 2 | BibTeX outputs |

### 2.4 PDFs (Questionable — Large Binaries)

| File | Size | Recommendation |
|------|------|----------------|
| `paper/latex_gpt/main.pdf` | 208 KB | **Commit** — active manuscript |
| `paper/latex_gpt/supplementary_main.pdf` | 2.8 MB | **Commit** — active supplement |
| `paper/latex_gpt/cover_letter.pdf` | 21 KB | **Commit** — active cover letter |

**Verdict:** PDFs are reasonable size (< 3 MB each, < 10 MB total). Commit.

### 2.5 Deleted Drafts (Already Cleaned)

30 `.kimi_draft*` files deleted. These were temporary drafts from earlier rounds. The deletion is correct and should be committed.

---

## 3. Untracked Files Classification

### 3.1 KEEP_ACTIVE (Do Not Delete)

| Path | Reason |
|------|--------|
| `broadcast.md` | Active cross-agent broadcast log |
| `report_md/_gpt/KIMI_P7_*` | P7 deliverables |
| `report_md/_gpt/CODEX_PHASE_P6_*` | Codex acceptance |
| `report_md/_gpt/DS_PHASE_P6_*` | DS audit |
| `report_md/_gpt/MIMO_PHASE_P6_*` | Mimo audit |
| `HAT_105_results_review/` | Remote 105 review data |
| `HAT_107_clean_review/` | Remote 107 review data |

### 3.2 KEEP_RELEASE (Do Not Delete)

| Path | Reason |
|------|--------|
| `release_artifacts/paper1_submission_bundle_20260509_final/` | Final submission bundle |
| `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` | Final tarball |
| `release_artifacts/paper1_provenance_archive_20260509/` | Provenance archive |
| `release_artifacts/paper1_provenance_archive_20260509.tar.gz` | Provenance tarball |

### 3.3 KEEP_CANONICAL_DATA (Do Not Delete)

| Path | Reason |
|------|--------|
| `paper/latex_gpt/source_data/canonical_json/` | Canonical JSON data |
| `paper/latex_gpt/source_data/*.csv` | Source data tables |
| `paper/latex_gpt/source_data/manifest_*.json` | Manifests |

### 3.4 KEEP_REMOTE_REVIEW (Do Not Delete)

| Path | Reason |
|------|--------|
| `HAT_105_results_review/` | Remote 105 data |
| `HAT_107_clean_review/` | Remote 107 data |

### 3.5 QUARANTINE_CANDIDATE (Review Before Action)

| Path | Size | Reason |
|------|------|--------|
| `paper/latex_gpt/deprecated/` | Unknown | Old LaTeX files |
| `paper/latex_gpt/figures/deprecated_20260424/` | Unknown | Old figures |
| `paper/latex_gpt/source_data/canonical_json/deprecated_20260501_old_protocol/` | Unknown | Old protocol data |
| `paper/latex_gpt/*.pdf` (test/merged) | Various | Test renderings and merged PDFs |
| `paper/latex_gpt/supp_*_merged_*.pdf` | Various | Merged supplement test PDFs |
| `paper/latex_gpt/ChatGPT Image *.png` | 4 files | ChatGPT-generated images |
| `paper/latex_gpt/cover_letter_v6.tex.pdf` | Unknown | Old cover letter draft |
| `paper/latex_gpt/BROADCAST_EOF` | Tiny | Artifact |
| `paper/latex_gpt/1` | Tiny | Artifact |
| `paper/latex_gpt/temp_render.tex` | Tiny | Temp file |
| `paper/latex_gpt/render_s3.py` | Small | Render script |
| `paper/latex_gpt/render_tikz.py` | Small | Render script |
| `paper/plot_merged_S10_S11.py` | Small | Plot script |
| `AGENT_INTERCOM_HUB_*.md` | 3 files | Old intercom files |
| `GPU_SCHEDULE_20260428.md` | 1 file | Old schedule |
| `REMOTE_105_MULTIDATASET_TASKLIST_20260429.md` | 1 file | Old tasklist |
| `REMOTE_HANDOFF_README_20260429.md` | 1 file | Old handoff |
| `REMOTE_NO_PUSH_RETURN_PROTOCOL_20260429.md` | 1 file | Old protocol |
| `gpu_watcher.sh` | Small | Old script |
| `output.md` | Small | Unknown output |
| `paper2/REMOTE_107_KV_TASKLIST_20260429.md` | 1 file | Old tasklist |
| `paper2/REMOTE_NO_PUSH_RETURN_PROTOCOL_20260429.md` | 1 file | Old protocol |

### 3.6 DELETE_SAFE (Build/Cache Residues)

| Path | Reason | Command |
|------|--------|---------|
| `__pycache__/` | Python cache | `find . -type d -name __pycache__ -exec rm -rf {} +` |
| `paper/latex_gpt/*.fls` | LaTeX build residues (main.fls, supplementary_main.fls) | `rm -f paper/latex_gpt/*.fls` |
| `.claude/` | Claude session cache | **Keep** — may contain scheduled tasks |
| `paper/thesis_cn/*.toc` | LaTeX TOC output | `rm -f paper/thesis_cn/*.toc` |

---

## 4. Large File Report (≥ 20 MB)

| Path | Size | Category | Action |
|------|------|----------|--------|
| `checkpoints/*.pt` | 33 GB total | Old experiment checkpoints | **Do not commit** — keep in `.gitignore` |
| `data/` | 15 GB | Dataset | **Do not commit** — keep in `.gitignore` |
| `paper2_aihwkit_baseline/` | 6.9 GB | AIHWKit experiments + checkpoints | **Do not commit** — keep in `.gitignore` |
| `release_artifacts/*.tar.gz` | ~200 MB | Release tarballs | **Do not commit** — keep in `.gitignore` |

---

## 5. Checkpoint/Binary Safety Check

| Check | Result |
|-------|--------|
| `.pt` / `.pth` / `.ckpt` in commit scope | ❌ None — all in `checkpoints/` which is already `.gitignore`d |
| Raw datasets in commit scope | ❌ None — all in `data/` which is already `.gitignore`d |
| Build residues in commit scope | ⚠️ `*.fls` files — remove before commit |
| Large logs in commit scope | ❌ None |

---

## 6. Branch and Commit Proposal

### 6.1 Branch Name

`paper1-freeze-20260509`

### 6.2 Commit Message

```
freeze: Paper-1 submission bundle 2026-05-09

- Final manuscript sources with P6-locked numbers
- 6-bit seed123 rerun integrated (best=68.51%, fresh=68.49%)
- PCM precision ladder CSV updated (n=4 for 6-bit)
- Generated figures and PDFs rebuilt
- Deleted 30 temporary .kimi_draft* files
- Supplementary and cover letter synced to locked values

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
```

### 6.3 Files to Stage (Exact List)

```bash
# Core manuscript
git add paper/latex_gpt/main.tex
git add paper/latex_gpt/supplementary.tex
git add paper/latex_gpt/cover_letter.tex
git add paper/latex_gpt/sections/*.tex
git add paper/latex_gpt/supplementary/*.tex
git add paper/latex_gpt/figures/tikz/*.tex
git add paper/latex_gpt/refs_gpt.bib

# Source data
git add paper/latex_gpt/source_data/*.csv
git add paper/latex_gpt/source_data/canonical_json/README.md
git add paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed123/
git add paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed789/
git add paper/latex_gpt/source_data/manifest_paper1_spine.json

# Figures
git add paper/figures/*.png
git add paper/latex_gpt/figures/*.png
git add paper/latex_gpt/figures/*.pdf

# PDFs
git add paper/latex_gpt/main.pdf
git add paper/latex_gpt/supplementary_main.pdf
git add paper/latex_gpt/cover_letter.pdf

# Thesis (optional separate commit)
git add paper/thesis/*.tex
git add paper/thesis/main.pdf
git add paper/thesis/main.bbl
git add paper/thesis/main.blg

# Report deliverables
git add report_md/_gpt/KIMI_P7_*.md
git add report_md/_gpt/CODEX_PHASE_P6_*.md
git add report_md/_gpt/DS_PHASE_P6_*.md
git add report_md/_gpt/MIMO_PHASE_P6_*.md

# Deletions
git add -u  # Stage all deletions (.kimi_draft* files)
```

### 6.4 Files to Explicitly Ignore

```bash
# Already in .gitignore — verify no accidental staging
git status --short | grep "^A" | grep -E "\.(pt|pth|ckpt)$" || echo "No checkpoints staged"
```

---

## 7. Pre-Commit Command Block

```bash
# Step 1: Remove build residues
rm -f paper/latex_gpt/*.fls

# Step 2: Stage deletions (draft files)
git add -u

# Step 3: Stage additions (use the list above or interactive)
git add paper/latex_gpt/main.tex paper/latex_gpt/supplementary.tex paper/latex_gpt/cover_letter.tex
git add paper/latex_gpt/sections/*.tex
git add paper/latex_gpt/supplementary/*.tex
git add paper/latex_gpt/figures/tikz/*.tex
git add paper/latex_gpt/refs_gpt.bib
git add paper/latex_gpt/source_data/*.csv
git add paper/latex_gpt/source_data/canonical_json/README.md
git add paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed123/
git add paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed789/
git add paper/latex_gpt/source_data/manifest_paper1_spine.json
git add paper/figures/*.png
git add paper/latex_gpt/figures/*.png
git add paper/latex_gpt/figures/*.pdf
git add paper/latex_gpt/main.pdf paper/latex_gpt/supplementary_main.pdf paper/latex_gpt/cover_letter.pdf
git add paper/thesis/*.tex paper/thesis/main.pdf paper/thesis/main.bbl paper/thesis/main.blg
git add report_md/_gpt/KIMI_P7_*.md
git add report_md/_gpt/CODEX_PHASE_P6_*.md
git add report_md/_gpt/DS_PHASE_P6_*.md
git add report_md/_gpt/MIMO_PHASE_P6_*.md

# Step 4: Verify no large binaries staged
git diff --cached --stat | grep -E "\.pt$|\.pth$|\.ckpt$" || echo "No checkpoints staged"

# Step 5: Review staged changes
git diff --cached --stat

# Step 6: Commit
git commit -m "freeze: Paper-1 submission bundle 2026-05-09

- Final manuscript sources with P6-locked numbers
- 6-bit seed123 rerun integrated (best=68.51%, fresh=68.49%)
- PCM precision ladder CSV updated (n=4 for 6-bit)
- Generated figures and PDFs rebuilt
- Deleted 30 temporary .kimi_draft* files
- Supplementary and cover letter synced to locked values

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"

# Step 7: Do NOT push without user approval
echo "Commit ready. DO NOT PUSH without explicit user confirmation."
```

---

## 8. Verdict

| Check | Result |
|-------|--------|
| Safe-to-commit files identified | ✅ 96 modified + selected untracked |
| Must-not-commit files identified | ✅ Checkpoints (33 GB), data (15 GB), tarballs |
| No large binaries in commit scope | ✅ Verified |
| Build residues handled | ✅ `*.fls` to be removed before commit |
| Deletions staged correctly | ✅ `.kimi_draft*` deletions via `git add -u` |
| Branch name proposed | ✅ `paper1-freeze-20260509` |
| Commit message drafted | ✅ |
| Exact command block provided | ✅ |
| No push without approval | ✅ Explicit warning included |

**Track B Status: COMPLETE**

---

*Report by kimi. 2026-05-09.*
