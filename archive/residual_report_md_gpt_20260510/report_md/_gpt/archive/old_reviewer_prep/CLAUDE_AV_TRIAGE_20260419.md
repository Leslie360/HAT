# CLAUDE-AV: Red-Team Triage

**Date:** 2026-04-19
**Scope:** All CRITICAL/SHOULD-FIX items from `KIMI_RED_TEAM_AUDIT_20260419.md`, the 7-agent parallel audit suite (`K-S2` figure captions, `K-S3` notation, `K-O3` bibliography, `K-O4` consistency, `K-O5` source-data README, `K-O7` rebuttal coverage, `B-1` SX.Y reachability), and the external-review compilation.
**Manuscript source verified:** `paper/latex_gpt/*.tex` (live source) and `outputs/submission_bundle_20260419/` (bundle snapshot).

---

## Accepted (patch now)

These items are factually correct concerns that remain open in the live source or bundle. They are low-risk, high-value patches.

1. **Source-data README overclaim and broken references** → `outputs/submission_bundle_20260419/README_SUBMISSION.txt` claims the zip contains "plotting scripts" and "code to reproduce every figure"; the zip contains zero scripts (76 files, all `.json`/`.csv`/`.md`). The inner `README.md` lists `a23_experiment_results.json` and `learnable_gamma_*.json` which do not exist, and misnames `tinyvit_v4_ensemble_results_gpt.json` / `tinyvit_v4_nl2_hat_eval_results_gpt.json` (actual files lack the `tinyvit_` prefix).
   **Patch:** (a) Replace "(raw data, CSVs, and plotting scripts)" with "(raw experiment JSONs and summary CSVs; plotting scripts are in the repository `paper/plot_paper_figures.py`)"; (b) Fix broken index entries in the inner README; (c) Add a JSON schema paragraph explaining which keys map to plotted values (`mc_mean_acc` vs `best_test_acc`).

2. **Source-data CSV incompleteness** → `fig4_source_data.csv` inside the zip covers only CIFAR-10 and CIFAR-100. It omits the Flowers102 panel that is present in Main Fig. 4.
   **Patch:** Append Flowers102 rows extracted from `convnext_flowers102_c134_results_gpt.json` and `tinyvit_flowers102_v134_results_gpt.json`, and add a `source_json` column for traceability.

3. **Figure caption failures (24/41 standalone, 35/41 cross-ref)** → `KIMI_FIGURE_CAPTION_AUDIT_20260419.md` documents systematic gaps: most captions omit model/dataset context needed for standalone reading, and 35/41 fail to cross-reference the equations or tables that define plotted quantities (e.g., `tab:exp-notation` for V1–V8 IDs, `eq:scale-recovery` for the mapping pipeline).
   **Patch:** Apply the 41 suggested caption patches from the audit. Priority order: Main Figs 1–5 > Appendix Tables A1–A5 > Supplementary Figs S1–S15 / Tables S1–S16.

4. **Supplementary-level notation gaps** → `KIMI_NOTATION_AUDIT_20260419.md` flags 37 undefined-first-use items. The main-body items that are genuine gaps (not artifacts of narrative-first ordering) are concentrated in the supplementary: DAC, INL, DNL, SAR, MAC, MSE, ISP, LN, MVM, AR(1), and several Greek symbols (`w_max`, `d_k`, `σ_sneak`, `δ_IR`) appear in supplementary without prior expansion.
   **Patch:** Add inline parentheticals on first use in `supplementary.tex` per the audit's patch list. Main-body forward-reference symbols (`σ_D2D`, `σ_C2C`, `S_ADC`, `S_D2D`) are already mitigated by "defined in Section~\ref{sec:methodology}" forward pointers; no additional patch needed there.

5. **Zenodo-ready archive not mentioned in bundle README** → `KIMI_RED_TEAM_AUDIT_20260419.md` SHOULD-FIX #2. The archive exists at `release_artifacts/zenodo_archive_v0/` but the bundle README does not reference it, weakening the reproducibility story.
   **Patch:** Add one sentence in `README_SUBMISSION.txt` under "Source Data": "A curated Zenodo-ready archive is also available at `release_artifacts/zenodo_archive_v0/`."

6. **Stale `cover_letter.tex` page-count reference** → `CLAUDE-S` audit flagged "14 pages" but the live cover letter currently reads "17-page main manuscript." However, the cover letter also claims the package includes a "17-page main manuscript PDF and a 23-page supplementary information PDF," which matches `pdfinfo` verification (Main 17, Supplementary 23). **No patch needed for page count.** The cover letter is correct as-is.

---

## Rejected (already addressed or incorrect)

These concerns are either factually wrong in the current live source, already patched by prior rounds, or acceptable given the target journal's conventions.

1. **IMRaD violation (section order: Results→Discussion→Methodology→Setup)** → *Rejected.* Nature Communications explicitly permits narrative-first ordering for methods-oriented hardware papers. External Reviewer B: "The narrative-first structure serves this paper perfectly." External Reviewer A: "Good. The narrative-first order is standard for NC." Forward pointers ("defined in Section~\ref{sec:methodology}, Eq.~\ref{eq:scale-recovery}") resolve the equation-reference readability issue without global reordering. Prior decision (`CLAUDE_REPLY_TO_KIMI_20260419.md` Q4) was to keep the current order.

2. **"Deployment" overclaiming (~31+ instances)** → *Rejected.* The abstract already carries the "simulated" hedge ("simulated canonical regime," "simulated edge-vision deployment"). The Discussion explicitly states: "the framework ranks deployment risks, not a chip-predictive emulator." The remaining ~30 uses are standard technical terminology in the simulation-methods literature ("hybrid analog/digital deployment," "deployment model," "deployment distribution," "deployment evaluation," "deployment-facing accuracy expectations"). They describe the simulated evaluation scenario, not a claim of fabricated hardware. External Reviewer A's framing concern was already absorbed into the abstract/conclusion hedges; no bulk replacement is needed.

3. **Sobol index methodological concern** → *Rejected.* The estimator was clarified in `03_methodology.tex:90` as "estimated directly from the 7×9 grid of Monte Carlo means as Var(mean_grid[X_i]) / Var(Y), with MC noise realizations drawn independently per grid point." External Reviewer C: "The Sobol decomposition is the clearest quantitative contribution in the paper and is correctly presented." External Reviewer B concurred. The forward pointer from Results to Methodology is also present.

4. **Missing error bars on single-run estimates** → *Rejected.* Main Fig. 1 and Fig. 2 mix deterministic baselines (no error bars) with MC runs (±1 SD). The captions already transparently disclose: "bars without visible error bars indicate deterministic baselines or currently available point estimates." This meets disclosure standards. External reviewers suggested visual differentiation (hatching, dagger symbols) as a *nice-to-have* for a broad-readership journal, but it is not a submission blocker. The red-team audit did not flag this as critical or should-fix.

5. **Citation key/year mismatches** → *Rejected.* These are cosmetic discrepancies between bib-key years and `year` fields (e.g., `peng2020dnnneurosim` → rendered 2021, `choi2019pact` → rendered 2018, `zhang2026opect` → rendered 2025). They do **not** affect rendered output. The mechanical citation integrity audit (`KIMI_CITATION_AUDIT_20260419.md`) reports **PASS**: 0 unresolved keys, 0 empty citations, 0 placeholder tokens.

6. **Bibliography integrity (zhang/lin/choi)** → *Rejected — already fixed in live source.** `zhang2025opect` already contains all 14 authors (including the 4 previously flagged as missing). The main text correctly cites "Lin \emph{et al.}" for `lin2016physical` (the prior "Alibart" mismatch was patched in `01_introduction.tex`). `choi2019pact` already carries `doi = {10.48550/arXiv.1805.06085}`.

7. **Page count stale (22 vs 23)** → *Rejected.* `pdfinfo` verifies: Main = 17 pages, Supplementary = 23 pages. The cover letter and red-team audit are consistent with the current compiled output. The prior "22-page supplementary" reference was from an older snapshot before the correlated-D2D figure was added.

8. **Stale supplementary interpretation text (`supplementary.tex:785`)** → *Rejected — already fixed.** The "pending completion" text for `attn_proj` row~(e) no longer exists. The live `supplementary.tex` correctly states: "both attention-side linearizations (QKV and projection) collapse structurally," and discloses the MLP-only (32.12±7.72%) and all-linear (32.60±9.18%) fresh-instance transfer bounds.

9. **CrossSim "5-seed means" claim** → *Rejected — already fixed.** The live `06_discussion.tex` now reads: "single-run clean baseline, 3-run Monte Carlo under noise" and "a large qualitative divergence of 14.43~pp at n=3, preliminary." The subset-disclosure supplementary note (`Supplementary Note~SX.Y`) exists and contains the variance estimate.

10. **Contribution count mismatch (6 vs 4)** → *Rejected — already fixed.** The live cover letter lists exactly 4 contributions, aligned with `01_introduction.tex` ("this study makes four concrete contributions").

---

## Escalated (needs user/Claude decision)

These are user-owned, structural, or high-risk items where the technical fix is trivial but the content or scope requires an explicit go/no-go.

1. **Bundle metadata placeholders (TBD)** → The red-team CRITICAL item. `README_SUBMISSION.txt` lines 7–9 read:
   ```
   Corresponding Author: TBD
   Contact Email: TBD
   Institution: TBD
   ```
   **Why it needs user/Claude input:** This is the one thing an editor notices immediately. The content is user-owned (name, email, affiliation). `USER_METADATA_REQUEST_20260420.md` exists but is empty.
   **Recommendation:** User fills the three fields; agent applies a one-line `sed` replacement. This is the only true submission blocker remaining.

2. **Visual differentiation for mixed deterministic/MC bars (Figures 1–2)** → External Reviewers B, C, and E all recommend adding hatching, a dagger symbol (†), or dashed outlines to single-run bars so that a skimming reviewer does not interpret missing error bars as "zero variance." The caption already transparently discloses the mix.
   **Why it needs user/Claude input:** Implementing hatching requires regenerating figures or editing the plotting script (`paper/plot_paper_figures.py`), which risks layout drift. A LaTeX-only workaround (e.g., overlaying a dagger in the `.tex` figure environment) is possible but non-standard.
   **Recommendation:** Keep caption-only disclosure for submission. If reviewers request visual differentiation in revision, regenerate then. This is a perception issue, not a scientific correctness issue. **Override:** If the user wants a pre-emptive fix, add a one-line footnote in the caption rather than regenerating figures.
