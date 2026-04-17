# `latex_gpt` Working Manuscript

This directory is the current working LaTeX manuscript for the English paper.

Important state notes:

- `sections/*.tex` and `main.tex` are now the live paper source.
- The project is **not** locked to a single venue right now.
- Current strategy is multi-track: keep the paper submission-ready, keep venue choice open, allow selective high-ROI experiments, and prepare for future measured-data integration.
- The exact compile-time figure assets live in `/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/`.
- `/home/qiaosir/projects/compute_vit/paper/figures/` may hold synchronized mirrors, but the LaTeX package itself compiles from `latex_gpt/figures/`.
- Historical markdown files in `/home/qiaosir/projects/compute_vit/paper/*.md` are helpful mirrors, but should not override the current LaTeX source if drift appears.

## Current contents

- `main.tex`: minimal journal-agnostic master file
- `supplementary_main.tex`: supplementary-information master file
- `supplementary.tex`: supplementary body included by `supplementary_main.tex`
- `cover_letter.tex`: current editorial cover letter
- `sections/*.tex`: synchronized LaTeX prose drafts mapped to the current markdown sections
- `refs_gpt.bib`: initial bibliography derived from `paper/参考文献库.md`
- `CITATION_MAP_gpt.md`: placeholder-to-BibTeX mapping shared across English LaTeX closeout and Gemini cross-checking
- `CITATION_BACKLOG_gpt.md`: the remaining unresolved citation decisions and non-submission historical leftovers
- `TEMPLATE_MIGRATION_GUIDE_gpt.md`: exact file-level migration order for moving this scaffold into a venue template
- `SUBMISSION_PACKET_gpt.md`: one-page final handoff for manuscript, figures, citations, and template migration
- `../CANONICAL_RESULT_LOCK_gpt.md`: locked result values and wording boundaries for manuscript writing
- `../FIGURE_CAPTION_LOCK_gpt.md`: caption-level semantics that should remain stable during template migration

## Current state

- `main.pdf`, `supplementary_main.pdf`, and `cover_letter.pdf` compile locally.
- The title currently used in source is:
  - `Profile-Driven Hardware Simulation for Organic Optoelectronic Edge Vision`
- The manuscript has already been hardened for `simulation-first / behavioral-simulation` positioning.
- Ensemble HAT, the ADC cliff, and measured-data readiness are active narrative anchors.
- Venue-specific reweighting is still allowed later.

## Build and view

Preferred local compiler:

- `/home/qiaosir/miniconda3/envs/LLM/bin/tectonic`

Direct commands:

```bash
cd /home/qiaosir/projects/compute_vit/paper/latex_gpt
/home/qiaosir/miniconda3/envs/LLM/bin/tectonic -X compile main.tex --keep-logs --keep-intermediates
/home/qiaosir/miniconda3/envs/LLM/bin/tectonic -X compile supplementary_main.tex --keep-logs --keep-intermediates
/home/qiaosir/miniconda3/envs/LLM/bin/tectonic -X compile cover_letter.tex --keep-logs --keep-intermediates
```

VSCode workspace tasks are also configured for root-independent use:

- `Build Main PDF`
- `Build Supplementary PDF`
- `Build Cover Letter PDF`
- `Build All LaTeX PDFs`

If LaTeX Workshop is focused on a log/output tab rather than a `.tex` file, prefer these tasks or reopen `main.tex` / `supplementary_main.tex` before invoking the extension build command.

## Recommended truth references

For paper-state truth, check:

1. `/home/qiaosir/projects/compute_vit/MASTER_PLAN.md`
2. `/home/qiaosir/projects/compute_vit/report_md/_gpt/CLAUDE_TASK_gpt.md`
3. `/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md` (latest Codex block)
4. `main.tex`
5. `sections/*.tex`

## Recommended next steps

1. Keep the LaTeX manuscript as the active paper source.
2. Apply only source-grounded edits from sidecar agents.
3. Preserve multi-venue flexibility until a final editorial decision is made.
4. Add measured-device calibration later as an upgrade, not as a prerequisite for the current manuscript.
