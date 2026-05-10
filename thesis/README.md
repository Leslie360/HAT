# thesis/

Degree thesis deliverable lane.

## Active structure

| Path | Purpose |
|:--|:--|
| `en/` | English thesis draft/source. |
| `cn/` | Chinese thesis draft/source. |
| `xjtu_template/` | XJTU template and template assets. |
| `latex_gpt` | Compatibility path to Paper1 manuscript assets when present. |

## Rules

- Thesis may reuse Paper1 figures/data, but reuse must be traceable through manifests or compatibility paths.
- Thesis-only figures/data should stay in thesis paths, not Paper1 release paths.
- Old thesis template surveys or agent notes belong in `archive/`, not in active thesis source.
- Build outputs should not be mixed with source unless required by the template; if retained, they should be documented.

## Related indexes

- Thesis asset map: `THESIS_ASSET_MAP_20260510.tsv`
- Paper1/thesis figure reuse: `../paper1/provenance/manifests/thesis_used_figures_20260510.tsv`
- Manuscript asset map: `../manuscripts/MANUSCRIPT_ASSET_INDEX_20260510.md`
- Ideal layout plan: `../coordination/active/COMPUTE_VIT_IDEAL_LAYOUT_PLAN_20260510.md`
