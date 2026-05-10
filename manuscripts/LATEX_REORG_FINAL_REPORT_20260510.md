# LaTeX Reorganization Final Report

Date: 2026-05-10
Scope: `/home/qiaosir/projects/compute_vit`
Policy: move-only, compatibility symlinks retained, no deletion, no commit/push.

## 1. Final layout

```text
compute_vit/manuscripts/
├── paper1/
│   ├── src/                         # active Paper-1 LaTeX source
│   ├── release -> ../../paper1/release/paper1_submission_bundle_20260509_final
│   ├── manifests/                   # TeX/figure/table manifests
│   └── asset_archive/
│       ├── unused_figures_candidates/
│       └── legacy_parallel_paper_figures/
├── paper2/snippets/                 # current Paper-2 LaTeX snippets
└── thesis/                          # symlinks to thesis roots
```

## 2. Compatibility paths

| Path | Target |
|---|---|
| `paper/latex_gpt` | `../manuscripts/paper1/src` |
| `thesis/latex_gpt` | `../manuscripts/paper1/src` |
| `manuscripts/thesis/en` | `../../thesis/en` |
| `manuscripts/thesis/cn` | `../../thesis/cn` |
| `manuscripts/thesis/template` | `../../thesis/xjtu_template` |
| `paper2_aihwkit_baseline/r10e_tex_paragraph.tex` | `../manuscripts/paper2/snippets/r10e_tex_paragraph.tex` |

## 3. Manifests

- `manuscripts/paper1/manifests/paper1_latex_inputs_20260510.tsv`
- `manuscripts/paper1/manifests/thesis_latex_inputs_20260510.tsv`
- `manuscripts/paper1/manifests/paper1_used_figures_20260510.tsv`
- `manuscripts/paper1/manifests/thesis_used_figures_20260510.tsv`
- `manuscripts/paper1/manifests/paper1_unused_figure_candidates_20260510.tsv`
- `manuscripts/paper1/manifests/unused_figure_moves_20260510.tsv`
- `manuscripts/paper1/manifests/paper1_tables_20260510.tsv`
- `manuscripts/paper1/manifests/thesis_tables_20260510.tsv`
- `manuscripts/paper1/manifests/latex_missing_refs_20260510.tsv`

## 4. Counts

| Item | Count |
|---|---:|
| Missing refs after compatibility fix | 0 |
| Unused figure candidate moves | 127 |
| Paper-1 table environments indexed | 116 |
| Thesis table environments indexed | 94 |
| Active broken symlinks | 0 |

## 5. Build verification

Paper-1 built successfully from both paths:

```text
compute_vit/manuscripts/paper1/src
compute_vit/paper/latex_gpt
```

Build log:

```text
logs/latex_build_manuscripts_paper1_20260510_004625.log
```

Tectonic produced warnings already known from LaTeX style/rerun behavior, but wrote `main.pdf` and `supplementary_main.pdf` successfully from both canonical and compatibility paths.

## 6. Protected assets

The following were not moved:

- `paper1/release/paper1_submission_bundle_20260509_final.tar.gz`
- `paper1/release/paper1_submission_bundle_20260509_final/`
- `paper1/provenance/`
- `data/`
- `checkpoints/`
- `paper2_aihwkit_baseline/checkpoints/`

Final bundle SHA remains:

```text
32959fac881ad1659d2da0a4ebeba30846dac72986e032dc411ea6e916c6f4a4  paper1/release/paper1_submission_bundle_20260509_final.tar.gz
```

## 7. Restore scripts

- `archive/reorg_20260509/restore/THESIS_LATEX_GPT_COMPAT_20260510_RESTORE.sh`
- `archive/reorg_20260509/restore/LATEX_MANUSCRIPT_REORG_20260510_RESTORE.sh`
- `archive/reorg_20260509/restore/LATEX_UNUSED_FIGURES_20260510_RESTORE.sh`

## 8. Completion verdict

Paper-1, Paper-2 snippets, and thesis LaTeX are now separated under `manuscripts/`. Figures used by current Paper-1/thesis builds remain accessible in the active build path, while unused candidates and legacy parallel figure pools are separated under `manuscripts/paper1/asset_archive/` with original paths retained as symlinks.
