# tools/plotting/

Reusable plotting scripts. Every script here should document its input data and output figure paths.

## Current scripts

| Script | Inputs | Outputs / consumers | Status |
|:--|:--|:--|:--|
| `plot_paper1_spine.py` | `paper1/manuscript/source_data/fig1_paper1_spine.csv` | Paper1 source/release figure assets | active |
| `plot_paper1_decision_map.py` | `paper1/manuscript/source_data/fig2_paper1_decision_map.csv` | Paper1 source/release figure assets | active |
| `plot_paper_figures.py` | Paper1 report JSON/CSV artifacts | `paper/figures/` compatibility outputs | legacy compatibility |
| `generate_schematic_figures_gpt.py` | Manual schematic layout definitions | `paper/latex_gpt/figures/fig1_system_architecture.pdf`, `fig2_weight_mapping.pdf` | legacy compatibility |
| `fix_plots.py` | `tools/plotting/plot_paper_figures.py` | In-place repair helper for legacy plot script | legacy one-shot |

## Rules

- Plot scripts must not silently write into Paper1 release bundles.
- Generate into manuscript source or a staging path, then update manifests.
- Old plotting one-offs belong in `archive/` with manifest/restore coverage.
