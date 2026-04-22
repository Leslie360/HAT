# Submission Packet (GPT)

This file is the shortest English-side handoff for final submission work.

Use it when:
- migrating into a venue template
- checking whether the manuscript, figures, and bibliography agree
- aligning Gemini's Chinese mirror against the locked English results

## Locked Source of Truth

- English manuscript:
  - `paper/01_introduction.md`
  - `paper/02_related_work.md`
  - `paper/03_methodology.md`
  - `paper/04_experimental_setup.md`
  - `paper/05_results.md`
  - `paper/06_discussion.md`
  - `paper/07_conclusion.md`
- LaTeX scaffold:
  - `paper/latex_gpt/main.tex`
  - `paper/latex_gpt/sections/00_abstract.tex`
  - `paper/latex_gpt/sections/01_introduction.tex`
  - `paper/latex_gpt/sections/02_related_work.tex`
  - `paper/latex_gpt/sections/03_methodology.tex`
  - `paper/latex_gpt/sections/04_experimental_setup.tex`
  - `paper/latex_gpt/sections/05_results.tex`
  - `paper/latex_gpt/sections/06_discussion.tex`
  - `paper/latex_gpt/sections/07_conclusion.tex`

## Result Locks

- Canonical numeric and wording lock:
  - `paper/CANONICAL_RESULT_LOCK_gpt.md`
- Figure semantics:
  - `paper/FIGURE_CAPTION_LOCK_gpt.md`
  - `paper/FIGURE_CAPTION_DRAFTS_gpt.md`
- Manual schematic briefs:
  - `paper/FIG1_FIG2_BRIEF_gpt.md`

## Bibliography Assets

- Working BibTeX file:
  - `paper/latex_gpt/refs_gpt.bib`
- Mapping and unresolved decisions:
  - `paper/latex_gpt/CITATION_MAP_gpt.md`
  - `paper/latex_gpt/CITATION_BACKLOG_gpt.md`

## Figures to Carry Into the Venue Template

Use the exact package-matched exports under:

- `paper/latex_gpt/figures/`

The mirrored files under `paper/figures/` are useful for plotting workflows, but template migration should start from the `latex_gpt/figures` copies that match the current compiled PDFs.

Main external figures actually used by the current LaTeX manuscript:

- `paper/latex_gpt/figures/fig4_accuracy_comparison.png`
- `paper/latex_gpt/figures/fig5_hat_recovery.png`
- `paper/latex_gpt/figures/fig_contour_map.png`
- `paper/latex_gpt/figures/figS3_ensemble_hat.png`
- `paper/latex_gpt/figures/fig10_zero_shot_transferability.png`

Supplementary external figures actually used by the current LaTeX supplement:

- `paper/latex_gpt/figures/fig_proxy_sensitivity_map.png`
- `paper/latex_gpt/figures/fig_sobol_sensitivity.png`
- `paper/latex_gpt/figures/fig9_noise_sensitivity.png`
- `paper/latex_gpt/figures/fig_fresh_instance_ablation.png`
- `paper/latex_gpt/figures/fig_attention_maps.png`
- `paper/latex_gpt/figures/fig7_retention_curve.png`
- `paper/latex_gpt/figures/fig6_physical_compensation.png`
- `paper/latex_gpt/figures/fig3_snr_curves.png`
- `paper/latex_gpt/figures/fig8_pareto_energy_accuracy.png`
- `paper/latex_gpt/figures/figS1_asymmetry_concept.png`
- `paper/latex_gpt/figures/figS2_nonideality.png`

## Three Rules That Must Survive Template Migration

1. Keep `Fig.4 / Fig.5` limited to canonical cross-dataset results.
   `Task 34/35/36` stay in `§5.9` as physical-extension results.
2. Keep Tiny-ViT corrected retention described as:
   `rapid early drop followed by a broad plateau near 79%`.
3. Keep `Flowers-102` described as:
   `low-data boundary` / `data-volume floor`, not universal method failure.

## Still Unresolved but Non-Blocking

- exact `Fault-Aware Training Survey` reference
- final bibliographic form for `MemTorch`
- manual drawing of `Fig.1 / Fig.2`
- actual venue-template front matter

## Gemini Alignment

- `paper_zh/*` remains Gemini-owned.
- If the Chinese manuscript mirrors the English one, it should mirror this packet through:
  - `CANONICAL_RESULT_LOCK_gpt.md`
  - `FIGURE_CAPTION_LOCK_gpt.md`
  - `SUBMISSION_PACKET_gpt.md`
