# Paper1 Visual Repro Cleanup Check

Date: 2026-05-10

## Result

No active `tmp/py_figures/`, standalone `render_tikz.py`, cache-bypass PDF slices, or `*_final_check.pdf` artifacts were found outside `archive/`.

## Decision

No Paper1 visual assets or PDFs were moved in this pass.

## Protected active PDFs/assets

- `manuscripts/paper1/src/main.pdf`
- `manuscripts/paper1/src/supplementary_main.pdf`
- `manuscripts/paper1/src/cover_letter.pdf`
- active figure PDFs under `manuscripts/paper1/src/figures/`
- final frozen release under `paper1/release/paper1_submission_bundle_20260509_final/`

## Related provenance

- Active Paper1 provenance map: `paper1/provenance/paper1_active_provenance_index_20260510.tsv`
- Manuscript asset index: `manuscripts/MANUSCRIPT_ASSET_INDEX_20260510.md`
- Unused figure archive manifest: `manuscripts/paper1/asset_archive/MANIFEST.md`
