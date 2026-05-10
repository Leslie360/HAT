# Paper Directory Map

Date: 2026-05-10

## Why there are multiple paper-related directories

The repository currently has multiple paper-like names because it has gone through several reorganization passes while preserving compatibility for LaTeX builds, old scripts, release bundles, and Work-2 experiments.

## Directory roles

| Path | Role | Status | Keep? | Notes |
|:--|:--|:--|:--|:--|
| `paper1/manuscript/` | Editable Paper1 LaTeX source | active canonical | yes | Main/supplement/cover-letter source and active figures live here. |
| `manuscripts/paper1/src/` | Compatibility symlink to `paper1/manuscript/` | compatibility | temporary yes | Kept so old TeX/scripts/docs still resolve. Do not add new files here directly. |
| `paper/latex_gpt` | Compatibility symlink to Paper1 manuscript source | compatibility | temporary yes | Kept so old TeX/scripts/docs still resolve. Do not add new files here directly. |
| `paper/figures/` | Compatibility symlink pool to legacy Paper1 figure assets | compatibility | temporary yes | Symlinks point to `paper1/provenance/asset_archive/legacy_parallel_paper_figures/`; do not add new figure payloads here. |
| `paper/` | Legacy compatibility shell | compatibility/mixed | temporary yes | Contains compatibility symlinks only for Paper1 manuscript, reference locks, old plotting helpers, figure pool, and thesis links. |
| `paper1/` | Paper1 manuscript/release/provenance/report lane | active canonical | yes | Editable manuscript, frozen release, provenance archive, and current reports. |
| `paper1/provenance/reference_locks/` | Paper1 frozen result/caption/figure/credit locks | active canonical | yes | Old `paper/*.md` lock paths are compatibility symlinks here. |
| `paper1/provenance/manifests/` | Paper1 generated manifests | active canonical | yes | Figure/table/LaTeX dependency manifests moved here from `manuscripts/paper1/manifests/`. |
| `paper1/provenance/asset_archive/` | Paper1 unused/legacy asset archive | active provenance | yes | Unused figure candidates and legacy parallel-paper figure assets. |
| `manuscripts/paper1/release` | Symlink to final Paper1 release bundle | convenience symlink | yes | Do not edit through this path. |
| `paper2/` | Paper2 / 107 KV-cache code/results/manuscript lane | active canonical for Work-2 | yes | Current 107 selective KV-cache work plus Paper2 manuscript snippets. |
| `paper2/manuscript/snippets/` | Paper2 manuscript snippets | active canonical | yes | Current snippet: `r10e_tex_paragraph.tex`. |
| `manuscripts/paper2/snippets/` | Compatibility symlink to `paper2/manuscript/snippets/` | compatibility | temporary yes | Kept so old snippet references still resolve. |
| `paper2_aihwkit_baseline/` | Paper2 AIHWKit/PCM baseline lane | active/protected local payload | yes | Large 6.9G checkpoint/data area; indexed, not moved casually. |
| `thesis/` | Degree thesis lane | active canonical | yes | English/Chinese thesis and XJTU template. |
| `manuscripts/thesis/` | Convenience symlinks to thesis areas | compatibility/convenience | yes | Helps manuscript asset index navigate thesis sources. |

## Ideal long-term naming

```text
paper1/                  # Paper1 manuscript/release/provenance/report lane
paper1/manuscript/       # Paper1 editable LaTeX source
paper1/provenance/       # Paper1 manifests and asset archive
manuscripts/paper1/src/  # compatibility symlink to Paper1 manuscript
paper2/                  # Paper2/107 active code/results/manuscript snippets
paper2/manuscript/       # Paper2 manuscript snippets
paper2_aihwkit_baseline/ # Paper2 PCM/AIHWKit protected baseline payload
thesis/                  # degree thesis
paper/                   # compatibility only, eventually minimized
```

## Do not do yet

- Do not delete `paper/latex_gpt`; it is a compatibility symlink used by old paths.
- Do not move `paper1/release/` or final submission bundles.
- Do not move `paper2_aihwkit_baseline/checkpoints/` without explicit approval.
- Do not rename `paper2/` to `paper2_107/` until all references and scripts are updated.
- `paper/paper2/` legacy drafts are archived under `archive/reorg_20260509/paper2_legacy_drafts_20260510/paper/paper2/` with a restore script.

## Next cleanup target

1. No more low-risk paper-directory moves remain in this pass.
2. Keep `paper/` as a compatibility shell until old docs/scripts stop referencing `paper/latex_gpt`, `paper/figures`, and lock-file paths.
3. Do not move `paper2_aihwkit_baseline/` into `paper2/baselines/aihwkit/` without explicit approval because it contains 6.9G protected checkpoint/data payloads.
