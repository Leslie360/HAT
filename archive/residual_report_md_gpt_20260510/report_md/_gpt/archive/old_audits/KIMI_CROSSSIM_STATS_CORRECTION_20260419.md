# CrossSim Statistics Correction Deliverable

**Date:** 2026-04-19
**Scope:** C-3 fix per Claude’s Q2 decision (`AGENT_SYNC_gpt.md`).
**Goal:** Diff-ready prose that replaces the incorrect "5-seed means" claim with the actual run counts, inserts the mandatory subset-disclosure sentence, and drafts the supplementary note with variance estimates.

---

## 1. Current (incorrect) manuscript text

> A preliminary cross-framework comparison against CrossSim (**5-seed means**) shows consistent baseline inference (86.2\% ours vs.\ 83.7\% CrossSim at 8-bit ADC) but diverges under noise injection (81.6\% vs.\ 67.2\% at $\sigma=5\%$, a 14.43~pp gap), highlighting the sensitivity of accuracy predictions to the noise-to-conductance mapping.

*Location:* `compute_vit/outputs/submission_bundle_20260419/manuscript/sections/06_discussion.tex`, end of §6.6 / Outlook paragraph.
*Note:* The live manuscript source at `compute_vit/paper/latex_gpt/sections/06_discussion.tex` has already been updated with the corrected sentence below. The submission bundle still carries the old incorrect text.

---

## 2. Corrected text

Replace the incorrect sentence with:

> A preliminary cross-framework comparison against CrossSim on a deterministic 1\,000-image CIFAR-10 test subset (single-run clean baseline, 3-run Monte Carlo under noise) shows consistent baseline inference (86.2\% ours vs.\ 83.7\% CrossSim at 8-bit ADC) but diverges under noise injection ($81.63 \pm 0.56$\% vs.\ $67.20 \pm 2.67$\% at $\sigma=5\%$, a 14.43~pp gap), highlighting the sensitivity of accuracy predictions to the noise-to-conductance mapping. The subset protocol is disclosed explicitly because of CrossSim throughput constraints; see Supplementary Note~SX.Y for the subset-sampling protocol and variance estimate.

**Rationale for changes:**
- **Seed count:** The underlying JSONs contain **1 run** for the clean baseline (`crosssim_clean_baseline.json`) and **3 runs** for each noise-injection condition (`crosssim_low_noise.json`, `crosssim_standard_noise.json`). No 5-seed data exist for this comparison.
- **Formatting:** Restores the exact mean \pm std notation ($81.63 \pm 0.56$\% and $67.20 \pm 2.67$\%) used elsewhere in the manuscript, rather than the rounded 81.6\% / 67.2\%.
- **Subset disclosure:** The comparison was performed on `max_samples: 1000` (10\% of CIFAR-10 test). Without disclosure, readers may assume full-test-set statistics. The new sentence makes the limitation transparent and points to the supplementary note for details.
- **Deterministic vs. stratified:** The subset is a deterministic slice of the canonical test ordering, *not* a deliberately stratified sample. The first 1\,000 images happen to yield an approximately balanced class distribution (86–112 per class), but no stratification was applied.

---

## 3. Supplementary Note draft (SX.Y — Cross-framework subset-evaluation protocol)

**Supplementary Note SX.Y. Cross-framework subset-evaluation protocol.**
Because a single noisy evaluation on the full CIFAR-10 test set would extrapolate to roughly 15~h per condition for CrossSim (5,361~s per 1,000-image run) versus ~1~s per 1,000-image run for the native framework, the shared-regime sanity check was performed on a deterministic 1,000-image slice of the canonical CIFAR-10 test ordering (the first 1,000 images; no RNG seed was set). This slice yields an approximately balanced class distribution (86–112 images per class). The clean baseline was evaluated once per framework; the noise-injection settings were evaluated with three independent Monte Carlo draws. For the single-run clean baseline, the Wilson 95\% confidence intervals on the subset proportion are [83.9\%, 88.2\%] for our framework and [81.3\%, 85.9\%] for CrossSim. For the three-run noise condition, the t-distribution 95\% CIs (df = 2, $t_{0.975} = 4.303$) are [79.9\%, 83.3\%] for our framework and [59.1\%, 75.3\%] for CrossSim. The large CrossSim run-to-run spread ($\sigma_{\text{pop}} = 2.67$\%) reflects the sensitivity of its generic programming-error/read-noise mapping to the particular stochastic sample.

---

## 4. Impact assessment

The incorrect "5-seed means" assumption undermines the perceived statistical power of the CrossSim comparison. The following derived claims and coordination artifacts must be updated:

1. **Submission bundle `06_discussion.tex`** — Replace the incorrect sentence in `compute_vit/outputs/submission_bundle_20260419/manuscript/sections/06_discussion.tex` with the corrected text above.
2. **`PRE_SUBMISSION_CHECKLIST.md`** — Strike or rewrite the item "D9 CrossSim 14.43 pp \(\rightarrow\) '(5-seed means)' in \S6" to reflect the actual n=1/n=3 design.
3. **`PAPER_REVIEW_CLAUDE_20260418.md`** — Update the D9 remediation note ("add `(5-seed means; see Supp Table …)`") to reflect the actual replication counts and subset disclosure.
4. **Supplementary note `supplementary.tex`** — The live source already contains a placeholder note (line 715) explaining the deterministic subset and run counts, but it **lacks the variance estimate / confidence intervals**. Append the Wilson and t-distribution CI sentences from the draft above to that note.
5. **Rebuttal / response drafts** — Scan `REVIEWER_RESPONSE_DRAFT_gpt.md`, `KIMI_REBUTTAL_PROSE_20260419.md`, and any cover-letter drafts for "5-seed means" or "five seeds" in the CrossSim context; replace with the accurate replication counts. (Current audit: `REVIEWER_RESPONSE_DRAFT_gpt.md` already uses the correct numbers.)
6. **Figure / table captions** — If any figure or supplementary table cites the CrossSim numbers, the caption must be updated to disclose the 1,000-image subset. (The current audit found no such caption, but this should be verified before final submission.)
7. **Statistical interpretation** — The 14.43~pp gap must no longer be read as a robust 5-seed estimate. With only three CrossSim runs and a population standard deviation of 2.67\%, the 95\% t-interval for the CrossSim mean spans roughly 59\%–75\%. Qualitative claims about "divergence" remain defensible, but quantitative precision should be softened; e.g., "a 14.43~pp gap (n=3, large CrossSim variance)" rather than a precise point estimate.

---

*Deliverable prepared from:*
- `compute_vit/outputs/submission_bundle_20260419/manuscript/sections/06_discussion.tex` (incorrect source text)
- `compute_vit/paper/latex_gpt/sections/06_discussion.tex` (live source, already corrected)
- `compute_vit/paper/latex_gpt/supplementary.tex` (live supplementary note, missing variance estimate)
- `crosssim_clean_baseline.json`, `crosssim_low_noise.json`, `crosssim_standard_noise.json` (actual statistics)
- `run_crosssim_convnext.py` (subset-sampling method)
