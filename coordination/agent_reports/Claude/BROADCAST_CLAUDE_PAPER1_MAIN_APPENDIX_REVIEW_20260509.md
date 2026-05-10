# BROADCAST: Claude Paper-1 Main + Appendix Review

**Date:** 2026-05-09
**Scope:** `paper/latex_gpt/` main text (8 sections) + `supplementary.tex`
**Status:** REVIEW COMPLETE, AWAITING OWNER DECISION

---

## A. CRITICAL (must fix before submission)

### A-1. Supplementary is a "Frankenstein" document
**File:** `supplementary.tex` (lines 197-640 dominated by organic, lines 892+ buried PCM)
**Issue:** The main text is about PCM UnitCell precision-retention frontiers. The supplementary is dominated by organic optoelectronic content (inverse-gamma front end, DNTT retention, OPECT provenance, Zhang 2025 case study). A reader will be confused why the supplementary does not support the main-text PCM claims.
**Fix:** Restructure into clearly separated sections — "PCM-Related Supplementary" vs "Organic Device Extensions" — or move organic content to a separate document.

### A-2. Garbled text at supplementary end
**File:** `supplementary.tex:980-982`
```
Preliminary remote validation on DeiT/ViT suggests proportional noise-aware training
preserves fresh-instance accuracy across transformer backbones, pending full multi-seed
validation.
ion.
n.
```
**Fix:** Delete "ion." and "n." fragments.

### A-3. Main text completely omits CIFAR-100 / Flowers-102 results
**Files:** `05_results.tex`, `06_discussion.tex`
**Issue:** Main text focuses exclusively on CIFAR-10. Supplementary shows:
- Tiny-ViT V4 CIFAR-100: 65.48% (vs digital 86.94%) — 21 pp collapse
- Tiny-ViT V4 Flowers-102: 22.48% (vs digital 97.97%) — near-total failure
- Tiny-ViT V3 Flowers-102: 4.81%
If the framework only works on CIFAR-10, this is a major limitation that must be acknowledged in main text Discussion/Limitations. Currently it reads as if the method generalizes across datasets.
**Fix:** Add dataset-breadth limitation sentence in Discussion §Limitations.

### A-4. Suspicious ConvNeXt C4 CIFAR-100 number
**File:** `supplementary.tex:283` (Table `tab:supp-result-summary`)
**Issue:** ConvNeXt proportional-noise HAT CIFAR-100 = 84.75 ± 0.72%, but digital baseline is 64.12%. Noise-aware analog deployment outperforming digital by 20 pp is physically implausible. Likely pretrained-vs-scratch mismatch or data entry error.
**Fix:** Verify provenance or remove. Do not submit unverified.

---

## B. MAJOR (should fix)

### B-1. Ablation table missing 8-bit noisy baseline
**File:** `05_results.tex` Table `tab:ablation_mapping`
**Issue:** Table shows 32-bit digital → 4-bit hybrid (no noise) → 4-bit fixed → 4-bit Ensemble. But 8-bit noisy baseline (87.28% from `tab:algorithmic_rescue`) has no place in the ablation chain. Readers cannot trace 98.06% → 87.28%.
**Fix:** Add row for 8-bit IdealDevice with D2D/C2C noise, or add footnote explaining the gap.

### B-2. 6-bit fresh accuracy > 8-bit fresh accuracy unexplained
**File:** `05_results.tex` Table `tab:pcm_precision_ladder`
**Issue:** 6-bit fresh (77.86%) > 8-bit fresh (77.60%). Supplementary `tab:supp_6bit_pcm` / `tab:supp_8bit_pcm` confirms this holds across all three seeds. This counterintuitive result deserves at least one sentence.
**Fix:** Add interpretation — e.g., "6-bit quantization may act as a beneficial regularizer in the PCM UnitCell regime, or the nonlinear write surrogate interacts favorably with the coarser granularity."

### B-3. 6-bit late-recovery phenomenon buried in supplementary
**File:** `supplementary.tex:942-947` Figure `fig:supp_late_recovery`
**Issue:** 6-bit PCM seed456 would have early-stopped at a poor minimum; full 100-epoch training recovers to 78.49%. This explains the 6-bit outperformance (B-2) and has protocol implications.
**Fix:** Move to main text Results or Discussion, or at minimum add a sentence referencing it.

### B-4. "1 pp drift SLA" is unjustified
**File:** `05_results.tex:50`
**Issue:** The 1 pp deployment-drift threshold is introduced without citation or justification.
**Fix:** Clarify if self-defined: "we adopt a 1 pp threshold as a conservative design heuristic."

### B-5. Sobol index wording is misleading
**File:** `05_results.tex:70`
**Issue:** "S_ADC=0.98 over the full grid; S_D2D=0.92 in the operational regime" — first-order Sobol indices on different restricted domains are not directly comparable.
**Fix:** Clarify that the second number is computed on the restricted subset (ADC≥6, sigma_D2D≤15%).

### B-6. Cross-reference error in PCM comparison table
**File:** `supplementary.tex:741` Table `tab:pcm-comparison`
**Issue:** Drift column says "See Table `tab:retention-comparison`", but that table is the organic uniform-vs-state-dependent retention comparison, not PCM drift. PCM drift is main text `tab:pcm_precision_ladder`.
**Fix:** Correct cross-reference.

---

## C. MODERATE / MINOR

### C-1. IdealDevice vs PCM terminology confusion
**File:** `tab:supp-notation` in supplementary
**Issue:** "IdealDevice Baseline" is AIHWKit quantization+noise, not perfect noise-free. Ensure main text consistently uses "IdealDevice" to mean AIHWKit's model, not "ideal" as in perfect.
**Fix:** Add footnote or rename to "AIHWKit IdealDevice" everywhere.

### C-2. Algorithm 1 Evaluate procedure underspecified
**File:** `03_methodology.tex:69-72`
**Issue:** Algorithm says "Sample unseen masks and return average accuracy." Actual protocol is 10 fresh instances × 5 MC passes each. Algorithm conflates instance-level and pass-level sampling.
**Fix:** Clarify K=5 passes per instance, averaged over 10 instances.

### C-3. Energy caveat buried too deep
**File:** `supplementary.tex:679-681`
**Issue:** Good honest disclaimer about proxy-only energy. But main text `03_methodology.tex:91` introduces energy without caveat.
**Fix:** Add parenthetical or footnote in main text.

### C-4. Footnote about 86.37% vs 86.16% is easy to miss
**File:** `03_methodology.tex:52` footnote
**Issue:** Single-seed (86.37%) vs 3-seed mean (86.16%) discrepancy is important because thesis uses 86.37% while paper uses 86.16%.
**Fix:** Consider parenthetical in main text rather than footnote.

### C-5. `tab:supp-result-summary` label confusion
**File:** `supplementary.tex:269-289`
**Issue:** Caption says "locked best-checkpoint values" but some entries have ± (stochastic evaluations).
**Fix:** Clarify which rows are deterministic training-best vs MC-evaluated.

### C-6. NL-ablation tables side-by-side confusion
**Files:** `tab:supp-nl-ablation` vs `tab:r10d-nl-interpolation`
**Issue:** `tab:supp-nl-ablation` shows NL=2.0 → 27.72%, while `tab:r10d-nl-interpolation` shows NL=2.0 → ~80.54%. Difference is old vs revised recipe, explained in text, but readers skimming tables will be baffled.
**Fix:** Add bold header note on `tab:supp-nl-ablation`: "Earlier recipe only — does not apply to revised gradient scaling."

### C-7. Abstract oversells dataset breadth
**File:** `00_abstract.tex`
**Issue:** "precision-retention trade-offs under realistic physical deployment constraints" combined with only CIFAR-10 main-text results and catastrophic Flowers-102 performance is a breadth claim the data do not fully support.
**Fix:** Tone down or add "on CIFAR-10" qualifier.

### C-8. Missing CIFAR-100 PCM ladder
**Issue:** Main text does not mention CIFAR-100 at all for the precision ladder. Supplementary has V3/V4 CIFAR-100 but no PCM 4/6/8-bit CIFAR-100.
**Fix:** If available, add. If not, explicitly state "CIFAR-100 PCM results were not evaluated."

---

## RECOMMENDED EXECUTION ORDER

1. **A-2** (garbled text) — 30 seconds
2. **A-4** (ConvNeXt 84.75% verification) — must verify before submission
3. **A-3** (CIFAR-100/Flowers limitation) — add 1-2 sentences to Discussion
4. **B-4** (1 pp SLA citation) — add qualifier
5. **B-1** (ablation table gap) — add row or footnote
6. **B-2 + B-3** (6-bit > 8-bit + late recovery) — move/mention in main text
7. **A-1** (supplementary restructuring) — largest effort, schedule last
8. **C-1 through C-8** — polish pass

---

*Broadcast by Claude. Do not modify without owner approval.*
