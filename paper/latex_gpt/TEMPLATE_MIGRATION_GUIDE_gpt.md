# Template Migration Guide (GPT)

This file explains how to port the locked `latex_gpt` scaffold into a final journal or conference template with minimal ambiguity.

## Purpose

The current `latex_gpt` directory is a journal-agnostic staging area. It is not the final submission template.

This guide assumes:
- the English markdown in `paper/*.md` is already frozen
- `paper_zh/` is maintained separately by Gemini
- figures under `paper/figures/` are already the canonical assets

## Migration Order

1. Copy the target venue template into a new working directory.
2. Move or copy these files into the template workspace:
   - `paper/latex_gpt/sections/00_abstract.tex`
   - `paper/latex_gpt/sections/01_introduction.tex`
   - `paper/latex_gpt/sections/02_related_work.tex`
   - `paper/latex_gpt/sections/03_methodology.tex`
   - `paper/latex_gpt/sections/04_experimental_setup.tex`
   - `paper/latex_gpt/sections/05_results.tex`
   - `paper/latex_gpt/sections/06_discussion.tex`
   - `paper/latex_gpt/sections/07_conclusion.tex`
   - `paper/latex_gpt/refs_gpt.bib`
3. Copy the figure assets actually cited by the manuscript from `paper/figures/`.
4. Rewrite `main.tex` into the venue’s front-matter style rather than forcing the venue template to mimic the scaffold.
5. Reinsert captions using:
   - `paper/FIGURE_CAPTION_DRAFTS_gpt.md`
   - `paper/FIGURE_CAPTION_LOCK_gpt.md`
6. Recheck the final numbers against:
   - `paper/CANONICAL_RESULT_LOCK_gpt.md`

## What Is Already Locked

- section structure and basic prose
- citation mapping, except the explicitly unresolved bibliography items
- cross-dataset canonical numbers
- corrected retention wording (`~79% plateau`)
- physical-stress wording boundaries for `Task 34/35/36`
- caption semantics for `Fig.3`--`Fig.12`

## What Still Needs Venue-Specific Work

- title block, author list, affiliations, acknowledgements
- target-specific bibliography style
- figure float placement
- table environment formatting
- any template-specific equation, caption, or hyperlink packages

## High-Risk Items During Migration

1. **Best vs MC confusion**
   - use `paper/CANONICAL_RESULT_LOCK_gpt.md`
   - do not silently replace cross-dataset best results with MC means

2. **Retention wording drift**
   - keep Tiny-ViT V4 as `~79% plateau`
   - do not resurrect the obsolete `84.28%` wording

3. **Cross-dataset vs physical-stress mixing**
   - keep `Task 34/35/36` in the `§5.9` physical-extension lane
   - do not fold them into `Fig.4 / Fig.5`

4. **Flowers-102 overclaim**
   - keep it as a low-data boundary
   - do not rewrite it as universal method failure

## Recommended Companion Files

- `paper/CANONICAL_RESULT_LOCK_gpt.md`
- `paper/FIGURE_CAPTION_LOCK_gpt.md`
- `paper/FIGURE_CAPTION_DRAFTS_gpt.md`
- `paper/FIG1_FIG2_BRIEF_gpt.md`
- `paper/latex_gpt/SUBMISSION_PACKET_gpt.md`
- `paper/latex_gpt/CITATION_MAP_gpt.md`
- `paper/latex_gpt/CITATION_BACKLOG_gpt.md`
- `paper/latex_gpt/CLOSEOUT_CHECKLIST_gpt.md`

## Gemini Coordination Note

If the Chinese manuscript mirrors the final English template later, use the canonical result lock and caption lock as the shared ground truth rather than copying from intermediate logs.
