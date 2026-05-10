# LaTeX Missing Reference Diagnosis

Date: 2026-05-10
Scope: `compute_vit` Paper-1/thesis LaTeX manifests

## Summary

The manifest pass found 11 missing references. Paper-1 itself has no missing references in the generated manifest; all missing entries are thesis-side.

## Missing-reference classes

| Class | Count | Interpretation | Proposed handling |
|---|---:|---|---|
| Missing thesis compatibility path `thesis/latex_gpt` | 8 | Thesis files reference `../latex_gpt/...`; direct builds from `thesis/en` or `thesis/cn` need `thesis/latex_gpt -> ../paper/latex_gpt` now, or later `../manuscripts/paper1/src` | Create compatibility symlink before moving figures or manuscript source |
| Optional thesis placeholder inputs | 2 | `thesis/en/main.tex` references commented/optional `abstract` and `appendix_a`; parser captured them conservatively | Do not block cleanup; leave as documented optional placeholders |
| Thesis bibliography via compatibility path | 1 | `../latex_gpt/refs_gpt` resolves through the same missing `thesis/latex_gpt` path | Fixed by the same compatibility symlink |

## Immediate implication

Do not move Paper-1 figures yet. First create a compatibility path for direct thesis builds:

```text
compute_vit/thesis/latex_gpt -> ../paper/latex_gpt
```

If Paper-1 source is later moved to `compute_vit/manuscripts/paper1/src`, update this symlink to:

```text
compute_vit/thesis/latex_gpt -> ../manuscripts/paper1/src
```

## Files

- Raw missing refs: `latex_missing_refs_20260510.tsv`
- Paper-1 used figures: `paper1_used_figures_20260510.tsv`
- Thesis used figures: `thesis_used_figures_20260510.tsv`
- Unused figure candidates: `paper1_unused_figure_candidates_20260510.tsv`
