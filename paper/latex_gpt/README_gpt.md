# `latex_gpt` Scaffold

This directory is a GPT-scoped LaTeX scaffold for the paper. It is intentionally conservative:

- Markdown files in `/home/qiaosir/projects/compute_vit/paper/*.md` remain the source of truth.
- Figures are reused from `/home/qiaosir/projects/compute_vit/paper/figures/`.
- This scaffold is journal-agnostic for now and is meant to be migrated into the final venue template later.

## Current contents

- `main.tex`: minimal journal-agnostic master file
- `sections/*.tex`: synchronized LaTeX prose drafts mapped to the current markdown sections
- `refs_gpt.bib`: initial bibliography derived from `paper/参考文献库.md`
- `CITATION_MAP_gpt.md`: placeholder-to-BibTeX mapping shared across English LaTeX closeout and Gemini cross-checking
- `CITATION_BACKLOG_gpt.md`: the remaining unresolved citation decisions and non-submission historical leftovers
- `TEMPLATE_MIGRATION_GUIDE_gpt.md`: exact file-level migration order for moving this scaffold into a venue template
- `SUBMISSION_PACKET_gpt.md`: one-page final handoff for manuscript, figures, citations, and template migration
- `../CANONICAL_RESULT_LOCK_gpt.md`: locked result values and wording boundaries for manuscript writing
- `../FIGURE_CAPTION_LOCK_gpt.md`: caption-level semantics that should remain stable during template migration

## Current limitations

- No TeX toolchain is installed locally right now (`pdflatex`, `latexmk`, `pandoc` were previously unavailable).
- Sections `00`--`07` are now synchronized as concise LaTeX prose drafts, but they are still lighter than the markdown source and need venue-specific polish.
- Citation normalization is mostly complete for the main English manuscript, but two unresolved decisions remain:
  - the exact `Fault-Aware Training Survey` reference
  - the final bibliographic form of `MemTorch`

## Recommended next step after data lock

1. Freeze the markdown paper text.
2. Expand the synchronized LaTeX sections into the target journal template, following `TEMPLATE_MIGRATION_GUIDE_gpt.md`.
3. Lock the last unresolved reference decisions using `CITATION_MAP_gpt.md` and the keys in `refs_gpt.bib`.
4. Add manual Fig.1/Fig.2 assets and venue-specific front matter.
5. Move this scaffold into the target journal template or Overleaf project.
