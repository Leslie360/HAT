# Manuscripts Compatibility Index

Date: 2026-05-10
Scope: `/home/qiaosir/projects/compute_vit/manuscripts`

`manuscripts/` is now a compatibility/index layer, not the canonical home for active products. Canonical homes are `paper1/`, `paper2/`, and `thesis/`.

## Compatibility layout

| Path | Purpose | Canonical target |
|---|---|---|
| `paper1/src/` | Paper1 LaTeX source compatibility path | `../paper1/manuscript/` |
| `paper1/release` | Paper1 frozen release convenience link | `../paper1/release/paper1_submission_bundle_20260509_final/` |
| `paper1/manifests/` | Paper1 generated manifest compatibility path | `../paper1/provenance/manifests/` |
| `paper1/asset_archive/` | Paper1 asset archive compatibility path | `../paper1/provenance/asset_archive/` |
| `paper2/snippets/` | Paper2 LaTeX snippet compatibility path | `../paper2/manuscript/snippets/` |
| `thesis/en` | English thesis compatibility path | `../thesis/en/` |
| `thesis/cn` | Chinese thesis compatibility path | `../thesis/cn/` |
| `thesis/template` | XJTU template compatibility path | `../thesis/xjtu_template/` |

## External compatibility paths

| Old path | Target |
|---|---|
| `paper/latex_gpt` | `../manuscripts/paper1/src` |
| `thesis/latex_gpt` | `../manuscripts/paper1/src` |
| `paper/thesis` | `../thesis/en` |
| `paper/thesis_cn` | `../thesis/cn` |
| `paper2_aihwkit_baseline/r10e_tex_paragraph.tex` | `../paper2/manuscript/snippets/r10e_tex_paragraph.tex` |

## Verification

- Canonical Paper1 source is `paper1/manuscript/`.
- Canonical Paper2 snippets are under `paper2/manuscript/snippets/`.
- Canonical thesis source is `thesis/`.
- Active broken symlinks: 0 after the 2026-05-10 consolidation passes.

## Restore scripts

- `../archive/reorg_20260509/restore/PAPER1_CONSOLIDATION_20260510_RESTORE.sh`
- `../archive/reorg_20260509/restore/PAPER2_SNIPPET_CONSOLIDATION_20260510_RESTORE.sh`
- `../archive/reorg_20260509/restore/THESIS_LATEX_GPT_COMPAT_20260510_RESTORE.sh`
