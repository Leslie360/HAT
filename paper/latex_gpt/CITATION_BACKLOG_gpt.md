# Citation Backlog (GPT)

This file tracks the remaining citation-normalization work on the **English** manuscript side.

Use it together with:
- `paper/latex_gpt/CITATION_MAP_gpt.md`
- `paper/latex_gpt/refs_gpt.bib`

## Status

- LaTeX sections `00`--`07` now use draft BibTeX keys where practical.
- The submission-critical English markdown sections (`paper/01_introduction.md`, `paper/02_related_work.md`, `paper/03_methodology.md`) are now largely normalized.
- Remaining citation cleanup is no longer a broad manuscript-wide blocker; it is mainly a matter of unresolved bibliographic choices and historical/planning documents that are outside the submission package.

## Remaining Submission-Relevant Items

None. All mapped in `CITATION_MAP_gpt.md`.

### Main English manuscript

- `Fault-Aware Training Survey` (RESOLVED: `sun2024survey`)
- `MemTorch` (RESOLVED: `lammie2022memtorch`)

### Historical / non-submission documents

These files may still contain narrative placeholders, but they are not part of the current submission package:

- `paper/PAPER_OUTLINE.md`
- `paper/参考文献库.md`

## Resolved by Current Citation Map

These placeholders already have locked keys in `CITATION_MAP_gpt.md`:

- `Horowitz 2014`
- `Peng et al. 2020`
- `Alibart 2016`
- `Xu et al. 2025`
- `Guo et al. 2024`
- `Zeng et al. 2023`
- `Jung et al. 2024`
- `Vincze et al. 2026`
- `MemTorch`
- `Wu et al. 2023`
- `Wang et al. 2024`
- `Ge et al. 2024`
- `Jacob et al. 2018`
- `Bengio et al. 2013`

## Still Unresolved

- `Fault-Aware Training Survey`
  - keep explicit until the exact review/survey paper is chosen
- `MemTorch`
  - draft key exists, but bibliographic form may still need venue-specific refinement

## Recommended Closeout Order

1. Keep `paper/*.md` scientifically stable.
2. Treat the main English manuscript as citation-normalized unless a specific unresolved key is intentionally left explicit.
3. Use `CITATION_MAP_gpt.md` as the authoritative mapping.
4. Leave unresolved placeholders explicit rather than inventing polished but uncertain references.
