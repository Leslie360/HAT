# READY TO STAGE SHORTLIST — 2026-04-17

Purpose: compact handoff for the next intentional commit after the 2026-04-17 repo-state cleanup pass.

## MANUSCRIPT CORE

Stage together when preparing the next paper-facing commit:

- `PROJECT_INDEX.md`
- `paper/latex_gpt/main.tex`
- `paper/latex_gpt/sections/*.tex`
- `paper/latex_gpt/refs_gpt.bib`
- `paper/latex_gpt/cover_letter.tex`
- `paper/latex_gpt/supplementary.tex`
- `paper/latex_gpt/supplementary_main.tex`
- `paper/latex_gpt/README_gpt.md`
- `paper/latex_gpt/CITATION_MAP_gpt.md`
- `paper/latex_gpt/CITATION_BACKLOG_gpt.md`
- `paper/latex_gpt/SUBMISSION_PACKET_gpt.md`
- `paper/FIGURE_PLAN.md`
- `paper/plot_paper_figures.py`
- curated static art assets kept visible by `.gitignore` exceptions:
  - `paper/latex_gpt/figures/fig1_system_architecture.pdf`
  - `paper/latex_gpt/figures/fig2_weight_mapping.pdf`
  - `paper/latex_gpt/figures/figA.png`
  - `paper/latex_gpt/figures/figB.png`
  - `paper/latex_gpt/figures/figC.png`
  - `paper/latex_gpt/figures/figD.png`
  - `paper/latex_gpt/figures/figS1_asymmetry_concept.png`
  - `paper/latex_gpt/figures/figS2_nonideality.png`
  - `paper/latex_gpt/figures/graphical_abstract.png`

## LIVE CODE

Track in a code-facing commit or fold into the same paper commit only if the changes are already manuscript-coupled:

- core runtime:
  - `analog_layers.py`
  - `device_profile_utils.py`
  - `eval_imagenet_analog.py`
  - `eval_measured_profile.py`
  - `inference_analysis_utils.py`
  - `visualize_attention.py`
- training / evaluation:
  - `train_resnet18.py`
  - `train_convnext.py`
  - `train_tinyvit.py`
  - `train_tinyvit_ensemble.py`
  - `eval_resnet18_checkpoints.py`
  - canonical `run_*.py` drivers and legacy-named live helpers such as `experiment_nonideality_sweep.py` and `ablation_ensemble_hat_vs_iid.py`
- tests:
  - `test_analog_layers.py`
  - `test_run_device_comparison.py`
- repo docs / policy:
  - `.gitignore`
  - `README.md`
  - `LICENSE`
  - `RELEASE_CHECKLIST.md`
  - `EXPERIMENT_PROTOCOL.md`
  - `docs/`

## ARCHIVAL MOVES

These are cleanup-only changes and can be committed separately from science/manuscript edits:

- `_archive/paper-drafts/`
  - retired prompt files:
    - `BANANA_JOURNAL_SCHEMATIC_PROMPTS_20260408_gpt.md`
    - `NANOBANANA_SCHEMATIC_PROMPTS_gpt.md`
    - `PERPLEXITY_TARGETED_CITATION_PROMPTS_gpt.md`
- `_archive/scripts-oneshot/`
  - 18 retired root-level `run_*.sh` queue launchers
- `_archive/figure-drafts/`
  - 12 intermediate `banana` / `clean` / `crop` / `enhanced` figure-art variants

Associated root deletions that belong with the same archival commit:

- retired one-shot helpers already removed from root:
  - `patch_fig11.py`
  - `port_05.py`
  - `sync_zh.py`
  - `upgrade_plots.py`
- retired root shell launchers now moved under `_archive/scripts-oneshot/`

## GENERATED / IGNORED

Do not stage these in the next intentional commit:

- `outputs/`
- `data/`
- `.vscode/`
- `auto_fitted_profile.json`
- `paper/figures/*.png`, `paper/figures/*.pdf`
- generated LaTeX-side figure exports under `paper/latex_gpt/figures/` except the curated static assets listed above
- build PDFs and LaTeX build artifacts under `paper/latex_gpt/`
- log files under `logs/`
- Python cache files

## KEEP EXCLUDED FOR NOW

These files are draft-superseded and still have live callers in `paper/latex_gpt/*.md`. Do not archive or stage them as cleanup until those callers are removed:

- `paper/01_introduction.md`
- `paper/02_related_work.md`
- `paper/03_methodology.md`
- `paper/04_experimental_setup.md`
- `paper/05_results.md`
- `paper/06_discussion.md`
- `paper/07_conclusion.md`
- `paper/PAPER_OUTLINE.md`
- `paper/FIG1_FIG2_BRIEF_gpt.md`
- `paper/FIGURE_CAPTION_DRAFTS_gpt.md`
- `paper/参考文献库.md`
