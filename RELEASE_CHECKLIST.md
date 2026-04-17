# Release Checklist

Use this checklist before publishing the repository or preparing a submission
artifact.

## Repository hygiene

- Confirm `README.md` matches the current project scope and entrypoints.
- Confirm `LICENSE` is Apache 2.0 and the license section in `README.md` matches it.
- Remove stale `_gpt` coordination notes that should not ship publicly.
- Remove machine-specific absolute paths from public-facing docs.
- Review `.gitignore` to ensure local artifacts are excluded without hiding source assets.

## Artifact cleanup

- Keep only curated figures and release-quality logs needed for reproducibility.
- Exclude raw checkpoints unless a deliberate model-release package is planned.
- Remove temporary smoke directories such as `_codex_smoke_*`.
- Remove transient LaTeX build products before tagging a release.

## Paper consistency

- Verify `best` vs `MC` numbers are not mixed.
- Verify Flowers-102 language remains hypothesis-level, not causal proof.
- Verify `Task 37` fresh-instance numbers and Zhang case-study numbers remain distinct.
- Recompile `paper/latex_gpt/main.tex` and confirm figure references resolve cleanly.

## Open-source readiness

- Review public scripts for defensive argument validation.
- Confirm docs for profile schema, experiment registry, and physics stack are up to date.
- Confirm `docs/README.md` is present and linked from the repository `README.md`.
- Ensure no personal tokens, API keys, or private paths remain in committed files.

## Nature Communications submission packaging

- Confirm the first-submission manuscript file stays below the 30 MB single-file limit if text and figures are bundled together.
- Keep Supplementary Information as a separate upload and verify the compiled PDF matches the cited figure/table labels.
- Prepare a reviewer-accessible code archive or private repository link for the custom code central to the main claims.
- Prepare source-data tables or a zipped raw-data bundle for graphs and charts so it can be supplied immediately if requested.
- Confirm any overlapping or related manuscripts, reviewer suggestions/exclusions, and author-affiliation metadata are ready for the submission system.
