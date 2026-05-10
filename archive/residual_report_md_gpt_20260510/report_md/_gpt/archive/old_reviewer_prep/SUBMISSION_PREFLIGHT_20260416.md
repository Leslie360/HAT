# Submission Preflight — 2026-04-16

## Scope

Artifacts checked:

- `/home/qiaosir/projects/compute_vit/paper/latex_gpt/main.tex`
- `/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary_main.tex`
- `/home/qiaosir/projects/compute_vit/paper/latex_gpt/cover_letter.tex`

This pass was intentionally limited to non-claim-changing closeout work:

- build chain
- package consistency
- figure handoff paths
- front-matter / authorship consistency

No scientific result values or manuscript claims were modified in this pass.

## Build Status

Compiler used:

- `/home/qiaosir/miniconda3/envs/LLM/bin/tectonic`

Local compile status:

- `main.tex`: pass
- `supplementary_main.tex`: pass
- `cover_letter.tex`: pass

Observed page counts from the local logs:

- `main`: 15 pages
- `supplementary_main`: 15 pages
- `cover_letter`: 2 pages

## Source-Level Warning Audit

Current log grep found no source-level:

- undefined references
- multiply defined citations
- `Overfull \hbox`
- `Underfull \hbox`

Tectonic still emits a CLI-layer rerun message of the form:

- `internal consistency problem when checking if *.bbl changed`

This did not correspond to LaTeX source errors in the current pass. PDFs were generated successfully.

## Closeout Changes Landed

1. VSCode tasks now support root-independent builds for:
   - main PDF
   - supplementary PDF
   - cover letter PDF
   - build-all workflow

2. `paper/latex_gpt/README_gpt.md` now matches the current package reality:
   - actual manuscript title
   - actual figure directory
   - actual Tectonic workflow

3. `paper/latex_gpt/SUBMISSION_PACKET_gpt.md` now points template migration to the package-matched assets under:
   - `paper/latex_gpt/figures/`

4. `cover_letter.tex` now carries a Tectonic magic comment for editor/tool consistency.

5. The stale plural-author sentence was removed from:
   - `paper/latex_gpt/sections/07_conclusion.tex`

## Remaining Non-Blocking Notes

1. The current environment does not provide standard PDF inspection tools such as `pdfinfo`, `pdftotext`, or `pdffonts`.
2. This pass therefore verified submission readiness through:
   - successful local compilation
   - source/log warning audit
   - package/path consistency
   rather than full text extraction or font-embedding inspection.
3. If a stricter submission portal requires embedded-font auditing or PDF/A-style metadata checks, that should be done in a richer desktop/tooling environment.
