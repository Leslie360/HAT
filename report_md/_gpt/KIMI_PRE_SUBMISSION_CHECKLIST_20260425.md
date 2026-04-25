# Pre-Submission Checklist — Updated 2026-04-25 22:10 CST

## LaTeX Compile Status
- [x] `main.tex` compiles with BibTeX: RC 0, zero warnings after multi-pass.
- [x] `supplementary_main.tex` compiles after multi-pass: RC 0, zero warnings.
- [x] Zero undefined references in main and supplementary builds.
- [x] Zero duplicate bib entries observed in current BibTeX pass.
- [x] `tcolorbox` and theorem environments load correctly.
- [x] All 23 `\includegraphics{...}` references resolve to existing figure files.

## Round-7 Phase Status
- [x] Phase 1 Theory Deepening: `S_theory_ensemble_hat.tex` expanded and integrated.
- [x] Phase 2 Codex Empirical Mechanism: E1-E5 complete; JSONs, figures, and master report landed.
- [x] Phase 3 Writing Polish: Discussion restructure, design rules, reproducibility note, and supplementary wiring landed.
- [x] Phase 4 Defense/Tooling: defense materials and `S_tooling_comparison.tex` landed.
- [x] Phase 5 blockers from Codex/Gemini P0/P1 review cleared.

## Empirical Mechanism Integration
- [x] `S_mechanism_empirical.tex` integrated.
- [x] E2 alpha protocol matches JSON: `0,0.5,1,1.5,2,2.5,3`.
- [x] E2 caption uses three fresh masks, matching JSON.
- [x] E1 limitation uses fixed batch 32 and 4.73e6 analog parameters.
- [x] Severe-NL Hessian values described as absolute top eigenvalues, not undefined ratios.
- [x] Discussion mechanism wording is D2D-direction robustness, not global Hessian flatness.

## M-Series / Stage-2 Number Audit
- [x] Table 1 uses per-instance Stage-2 ADC-on numbers.
- [x] M1-M9 fresh-eval JSONs exist in `report_md/_gpt/json_gpt/`.
- [x] Main text reports three-seed M-series summary: Standard 81.20%, Ensemble 80.54%, Proportional 80.83%.
- [x] ADC-on wording remains diagnostic-only, not deployment-fidelity.

## Submission-Language Hygiene
- [x] Broad grep clean across canonical `.tex` for internal audit terms: `post-fix`, `pre-fix`, `bug-immune`, `Zone`, `3A/3B/3C`, `multi-agent`, `audit trail`, `invalidated`, `implementation artifact`.
- [x] Cover letter uses neutral source-data provenance language.
- [x] Supplementary historical ablation is framed as earlier diagnostic evidence, not current headline evidence.
- [x] No `TODO`, `FIXME`, `PENDING`, `USERNAME/REPO_NAME`, or stale root-level test commands in canonical `.tex`.

## Reproducibility / Code
- [x] `S_reproducibility.tex` test commands use `tests/test_*.py` paths after workspace cleanup.
- [x] `S_reproducibility.tex` describes the canonical 10x5 fresh-instance protocol and ADC hook diagnostic.
- [ ] Release URL / archive policy still needs final human decision: anonymous reviewer archive vs public GitHub URL.
- [ ] Confirm whether `9cdbe77` remains the canonical reproducibility commit, or whether a later cleanup/release commit should be tagged for submission.
- [ ] Final release bundle / Zenodo DOI placeholder still needs packaging after user approval.

## User-Supplied Metadata Still Needed
- [ ] Final author list and affiliations.
- [ ] Funding details.
- [ ] Acknowledgments wording.
- [ ] Competing interests statement confirmation.
- [ ] Reviewer/editor suggestion list if submitting to Nature Electronics.

## Remaining Technical Warnings
- [x] Main manuscript: zero warnings after latest Codex table-width fix.
- [x] Supplementary: zero warnings after latest Codex formula/path/title/float cleanup.

## Next Actions
1. Claude/Kimi can proceed with Phase-5 integration/read-through without prior P0/P1 blockers.
2. Decide release URL and final reproducibility commit/tag.
3. Fill user metadata and acknowledgments.
4. Prepare source-data/release bundle and reviewer-accessible archive.
5. Run Gemini hostile review v2 on the final integrated submission package.
