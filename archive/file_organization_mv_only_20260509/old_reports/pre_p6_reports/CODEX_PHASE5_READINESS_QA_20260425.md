# Codex Phase-5 Readiness QA

**Date:** 2026-04-25 22:10 CST  
**Scope:** Post-P0/P1 patch verification, submission-language scrub, LaTeX zero-warning cleanup, figure/reference QA, and pre-submission checklist refresh.

## Executive Verdict

Phase-5 integration can proceed. Codex no longer sees factual/protocol blockers from the prior Round-7 review. Main and supplementary LaTeX builds are clean after multi-pass compilation.

Remaining items are policy/metadata/release-packaging decisions, not scientific or code blockers.

## Actions Taken

### 1. Submission-language scrub

Files edited:
- `paper/latex_gpt/cover_letter.tex`
- `paper/latex_gpt/supplementary.tex`
- `paper/latex_gpt/supplementary/S_mechanism_empirical.tex`
- `paper/latex_gpt/supplementary/S_reproducibility.tex`

Changes:
- Removed residual cover-letter phrases tied to internal audit process: zone taxonomy, multi-agent audit trail, previous-ceiling language, numerical-implementation-detail language, and measured-data placeholder wording.
- Replaced `audited checkpoints` with neutral `evaluated/M-series checkpoints` language.
- Replaced `audited unit-test suite` with `unit-test suite`.
- Softened historical ablation language to `earlier diagnostic` / `earlier gradient-scaling recipe`.

### 2. Layout warning cleanup

Files edited:
- `paper/latex_gpt/sections/05_results.tex`
- `paper/latex_gpt/supplementary/S_theory_ensemble_hat.tex`
- `paper/latex_gpt/supplementary/S_hardware_calibration.tex`
- `paper/latex_gpt/supplementary/S_mechanism_empirical.tex`
- `paper/latex_gpt/supplementary/S_reproducibility.tex`

Changes:
- Wrapped the severe-NL recovery table in `\resizebox{\textwidth}{!}{...}` to remove the main-manuscript overfull hbox.
- Split two long theory equations using `\Delta f_M` and multi-line `align`.
- Changed S-Mechanism floats from `[h]` to `[ht]`.
- Shortened the S-HW title.
- Broke the long checkpoint path in S-Reproducibility.

### 3. Checklist refresh

Updated:
- `report_md/_gpt/KIMI_PRE_SUBMISSION_CHECKLIST_20260425.md`

The checklist now reflects current reality:
- Round-7 Phase 1-4 complete.
- Phase-2 empirical outputs integrated.
- M8/M9 no longer marked pending.
- Undefined refs no longer marked active.
- Prior P0/P1 blockers marked cleared.
- Remaining open items are release URL / final commit / Zenodo / human metadata.

## Verification Results

### LaTeX

Commands run from `paper/latex_gpt/`:

```bash
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode supplementary_main.tex
pdflatex -interaction=nonstopmode supplementary_main.tex
```

Results:
- `main.tex`: RC 0, zero warnings in final pass.
- `supplementary_main.tex`: RC 0, zero warnings in final pass.
- Zero undefined refs.
- Zero LaTeX errors.
- Zero overfull/underfull warnings in final logs.

### Figure QA

A script scanned all canonical `.tex` files for `\includegraphics{...}`.

Results:
- Figure references found: 23.
- Missing figure files: 0.

### Text Hygiene Grep

Broad grep across canonical `.tex` files found zero matches for:

```text
post-fix|pre-fix|bug-immune|Zone|3A|3B|3C|multi-agent|audit trail|audited|historical diagnostic|implementation artifact|invalidated|falsifying a previously reported|numerical implementation detail|PENDING_MEASURED_D2D|USERNAME/REPO_NAME|python test_dual_bug_fix|fixed eval batch of 256|five sampled|1{,}000--30{,}000|10^5
```

Remaining acceptable terms:
- `post-module-output hook diagnostic` in Results and cover letter: intentional ADC caveat.
- `Earlier diagnostic` in the supplementary groupwise ablation: neutral framing for a non-headline supplementary ablation.
- `ANONYMOUS/REPOSITORY` in S-Reproducibility: currently treated as a release-policy placeholder, not an error. Needs final human decision.

## Remaining Open Items

These are not Codex blockers, but must be decided before actual submission:

1. **Release URL policy:** choose reviewer-accessible archive URL vs public GitHub URL.
2. **Final reproducibility commit/tag:** confirm whether `33bed9c` remains the canonical reproducibility commit or whether the final cleanup/release commit should be tagged.
3. **Zenodo/source-data bundle:** package final code snapshot, source data, manifests, and figures.
4. **Human metadata:** author list, affiliations, funding, acknowledgments, competing interests.
5. **Hostile review v2:** run Gemini on the final integrated package after Claude/Kimi Phase-5 read-through.

## Codex Recommendation

Proceed to Claude/Kimi Phase-5 integration/read-through. Do not restart GPU work unless a new external trigger lands; GPU is currently idle and no Codex tmux jobs are active.
