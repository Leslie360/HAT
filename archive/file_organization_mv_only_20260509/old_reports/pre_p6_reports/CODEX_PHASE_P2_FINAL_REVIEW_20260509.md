# Codex Phase P2 Final Review — Release Candidate Bundle

Date: 2026-05-09
Owner: Codex
Input reports: Kimi P2, DS P2 audit, Mimo P2 audit

## Verdict

**Scientifically valid, but not final-accepted as a clean journal/reviewer bundle yet.**

The active manuscript, source data, guard checks, and PDFs are valid. However, the release candidate directory still contains non-release hygiene issues that should be removed before final packaging.

## What Passed

- `main.pdf` and `supplementary_main.pdf` are present.
- Active stale grep passes for old 6-bit claims and old `seed456_full100` references.
- Python PCM precision-ladder guard passes.
- No `.pt` checkpoint files were found.
- Source-data canonical JSON points to the corrected 2026-05-09 manifest.
- DS and Mimo both passed the scientific/reviewer-facing content.

## Blocking Hygiene Issues

The bundle contains draft/backup files that should not be in a clean submission/reviewer package:

```text
figures/figS1_asymmetry_concept.png.bak
figures/figS2_nonideality.png.bak
sections/00_abstract.tex.kimi_draft_v2
sections/00_abstract.tex.kimi_draft_v3
sections/01_introduction.tex.kimi_draft_v3
sections/03_methodology_ensemble_hat_v2.tex.kimi_draft
sections/05_results.tex.kimi_draft_v2
sections/05_results.tex.kimi_draft_v3
sections/06_discussion.tex.bak_20260425
sections/06_discussion.tex.kimi_draft_v2
sections/06_discussion.tex.kimi_draft_v3
sections/06_discussion_ensemble_hat_paragraph.tex.kimi_draft
sections/06_discussion_theory_paragraph.tex.kimi_draft
sections/07_conclusion.tex.kimi_draft_v3
```

Several nonessential large PNGs are also present. They are not catastrophic, but the P2R cleanup should decide whether they are actively referenced. Do not include unused large image references in the final reviewer package.

## Decision

Do not treat `release_artifacts/paper1_release_candidate_20260509/` as the final submission bundle. It is a valid candidate for cleanup.

Next action is folded into Superphase P3: create a cleaned `paper1_release_candidate_20260509_clean/` or equivalent, regenerate `MANIFEST_FILES.txt` and `SHA256SUMS.txt`, rerun all stale/size/PDF guards, then request DS/Mimo audit again.
