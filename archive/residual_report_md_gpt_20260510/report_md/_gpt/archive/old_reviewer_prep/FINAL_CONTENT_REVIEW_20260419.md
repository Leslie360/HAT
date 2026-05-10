# Final Scientific Content Review — Main Manuscript

**Date:** 2026-04-19
**Scope:** `compute_vit/paper/latex_gpt/` main manuscript (`main.tex` + 9 section files) + `supplementary.tex` + `cover_letter.tex`
**Cross-checks:** `compute_vit/report_md/_gpt/JSON_INVESTIGATION_20260419.md` and `compute_vit/report_md/_gpt/KIMI_REBUTTAL_COVERAGE_AUDIT_20260419.md`

---

## Executive Summary

| Severity | Count | Verdict |
|:--|:--:|:--|
| CRITICAL | 3 | The manuscript contains a broken central baseline (10.00%), omits an entire section that carries a key rebuttal caveat, and misrepresents CrossSim comparison statistics. |
| HIGH | 4 | Missing rebuttal support for R1/R5/R8, absent hyperparameters, and structural forward-reference issues. |
| MEDIUM | 3 | Unit ambiguities, epoch-label omission, and missing methodological detail. |
| LOW | 2 | Orphaned files and unsupported parameter-fraction claims. |

**Overall verdict: NEEDS MAJOR REVISION**

The three CRITICAL issues undermine the scientific credibility of the central Ensemble HAT claim, remove a key rebuttal defense from the compiled PDF, and misstate the empirical basis of the CrossSim comparison. These must be resolved before submission.

---

## 1. CRITICAL ISSUES

### C1. Standard-HAT fresh-instance baseline (10.00%) is derived from broken evaluation data

**Files / lines:**
- `compute_vit/paper/latex_gpt/sections/00_abstract.tex:5` — "collapses to 10.00\% on fresh hardware"
- `compute_vit/paper/latex_gpt/sections/01_introduction.tex:17` — "from chance level ($10.00\%$) to 86.37$\pm$1.54\%"
- `compute_vit/paper/latex_gpt/sections/05_results.tex:41` — "collapses to chance level (10.00\%) on arrays with different fixed D2D realizations"
- `compute_vit/paper/latex_gpt/sections/05_results.tex:77` — "Tiny-ViT V4 collapses to chance level (10.00\%) across all shown alternatives"
- `compute_vit/paper/latex_gpt/sections/06_discussion.tex:13` — "The collapse of V4 under fresh-instance transfer (10.00\% accuracy)"
- `compute_vit/paper/latex_gpt/sections/07_conclusion.tex:7` — "standard HAT collapses on fresh arrays, whereas Ensemble HAT raises fresh-instance accuracy from 10.00~\% to 86.37$\pm$1.54\%"

**Problem:** The 10.00\% value cited as the measured fresh-instance accuracy of standard HAT is sourced from `fresh_instance_eval.json` and `fresh_instance_cadence_control.json`. Both files show V4\_Standard mean = 10.0, std = 0.0, with all 10 fresh instances (and all 5 MC runs per instance) returning *exactly* 10.0\%.

`JSON_INVESTIGATION_20260419.md` explicitly flags this:
> "**V4\_Standard=10.0% is broken and should be ignored or replaced after re-run**"

Getting exactly 10.0\% on every fresh instance (CIFAR-10 chance level) with zero variance is statistically impossible under genuine model behavior; it is consistent with a numerical artifact (e.g., NaN propagation → uniform softmax). The test loss *does* vary across instances (e.g., 7.47 vs. 6.37), confirming the outputs are not literally uniform, yet the accuracy is pinned at exactly 10.0\% every time — a hallmark of a corrupted evaluation path.

**Impact:** The manuscript's central narrative — that Ensemble HAT raises fresh-instance accuracy from 10.00\% to 86.37\% — relies on a broken denominator. The one-sample $t$-test against chance ($p<10^{-15}$) cited in `05_results.tex:63` is therefore moot.

**Recommendation:** Re-run `eval_fresh_instances.py` on the standard V4 checkpoint with `--no-amp` (or on CPU) to obtain a valid fresh-instance baseline. If the corrected baseline is still near chance (e.g., 11–15\%), the qualitative claim survives but the exact 10.00\% must be replaced. If the corrected baseline is materially higher, the magnitude of the claimed improvement must be revised.

---

### C2. Related Work section (02_related_work.tex) is omitted from main.tex

**File / line:**
- `compute_vit/paper/latex_gpt/main.tex:45–50` — `\input{sections/01_introduction}` is followed directly by `\input{sections/05_results}`; `\input{sections/02_related_work}` is absent.

**Problem:** The compiled manuscript jumps from Introduction to Results without a Related Work section. Section `02_related_work.tex` exists on disk but is never included. This section contains the following critical caveat (line 7–8):

> "Existing open-source analog-training stacks are closer to i.i.d.\ perturbation injection than to full spatial-instance resampling... Our reviewer-facing comparisons therefore rely on internal controls---fixed-mask HAT, exploratory per-batch perturbation, and epoch-level structured resampling---rather than on a nonexistent apples-to-apples external baseline."

**Impact:** The rebuttal audit (`KIMI_REBUTTAL_COVERAGE_AUDIT_20260419.md`, R5) found that the manuscript "never compares Ensemble HAT against any external multi-instance baseline from prior literature, nor does it distinguish from i.i.d. ensemble methods." The missing Related Work section is the *only* place where this distinction is made. Its omission removes a key rebuttal defense and leaves the manuscript vulnerable to the charge that Ensemble HAT is presented without adequate contextualization.

**Recommendation:** Insert `\input{sections/02_related_work}` immediately after `\input{sections/01_introduction}` (or before it, per journal style).

---

### C3. CrossSim comparison misrepresents seed count and conceals subset evaluation

**File / line:**
- `compute_vit/paper/latex_gpt/sections/06_discussion.tex:47` — "A preliminary cross-framework comparison against CrossSim (**5-seed means**) shows consistent baseline inference (86.2\% ours vs.\ 83.7\% CrossSim at 8-bit ADC) but diverges under noise injection (**81.6\% vs.\ 67.2\%** at $\sigma=5\%$, a 14.43~pp gap)"

**Problem:** The underlying JSON files contradict this claim on two counts:

1. **Seed count:** `crosssim_clean_baseline.json` contains **1 run** (not 5). `crosssim_standard_noise.json` contains **3 runs** (not 5). `crosssim_low_noise.json` also contains 3 runs. No JSON in the repository contains 5 seeds for this comparison.

2. **Subset size:** All three files list `"max_samples": 1000`, meaning the comparison was performed on only 10\% of the CIFAR-10 test set (10\,000 images). The manuscript does **not** disclose this limitation.

`JSON_INVESTIGATION_20260419.md` confirms:
> "**Do NOT cite 81.63% as a full-set number.** It is a 1000-sample subset (10% of CIFAR-10 test)."

**Impact:** The phrase "5-seed means" is factually incorrect. Presenting 1000-sample subset accuracies without disclosure exaggerates the reliability of the comparison and risks misleading readers about the statistical power of the cross-framework check.

**Recommendation:** Either (a) re-run the CrossSim comparison on the full 10\,000-image test set with 5 seeds and update the numbers, or (b) revise the sentence to state the actual sample size and seed count: e.g., "A preliminary cross-framework comparison against CrossSim (1–3 runs on a 1\,000-image subset) shows..." The subset limitation must be disclosed.

---

## 2. HIGH ISSUES

### H1. R5 rebuttal claim is unsupported because Related Work is missing

**File:** `KIMI_REBUTTAL_COVERAGE_AUDIT_20260419.md`, R5 row

**Problem:** The rebuttal table's "Manuscript counter" column claims that "§6.1 distinguishes from i.i.d." for R5. The audit found this is false: §6.1 discusses fresh-instance transfer but does **not** distinguish Ensemble HAT from prior i.i.d. ensemble work. The only place this distinction appears is in the omitted `02_related_work.tex`.

**Recommendation:** Restore `02_related_work.tex` to the compiled manuscript (see C2). If that is not possible, add a 1–2 sentence caveat in §6.1 acknowledging the lack of a direct external multi-instance baseline.

---

### H2. R8 rebuttal claim is entirely absent from the manuscript

**Files:** `KIMI_REBUTTAL_COVERAGE_AUDIT_20260419.md`, R8 row

**Problem:** The rebuttal table marks R8 (cycle endurance ignored) as "✅ Ready" with the counter-argument: "Edge-vision = inference-heavy; retention is primary temporal bottleneck." The audit found that **this language does not exist anywhere in the manuscript** — neither main text nor supplementary mentions cycle endurance, write cycles, or device lifetime.

**Recommendation:** Add a one-sentence caveat in §6.5 Limitations (e.g., "Cycle endurance is not modeled because the present edge-vision regime is inference-dominant...") or explicitly reclassify R8 as response-only in the rebuttal table.

---

### H3. R1 rebuttal claim cites a non-existent manuscript passage

**Files:** `KIMI_REBUTTAL_COVERAGE_AUDIT_20260419.md`, R1 row

**Problem:** The rebuttal table claims "§6 defers ImageNet." The audit found that §6.3 discusses "Task Complexity and Data Starvation" and mentions Flowers-102 as the "low-data extreme," but **never names ImageNet or states it is deferred**. The "cost argument" for omitting ImageNet is also absent.

**Recommendation:** Remove "§6 defers ImageNet" from the rebuttal table. Anchor the scope argument on §1 ("edge-vision accuracy") and §4 (dataset list: CIFAR-10/100, Flowers-102).

---

### H4. Training hyperparameters are completely absent from both main text and supplementary

**Files / lines:**
- `compute_vit/paper/latex_gpt/sections/04_experimental_setup.tex:7` — "Detailed optimization settings and the Monte Carlo evaluation protocol are summarized in the Supplementary Information."
- `compute_vit/paper/latex_gpt/sections/04_experimental_setup.tex:32` — "Parameter provenance is summarized in the Supplementary Information, together with the optimization settings and evaluation conditions used for the reported runs."

**Problem:** Despite these promises, the supplementary information (`supplementary.tex`) contains **no** learning rate, batch size, optimizer, weight decay, learning-rate schedule, data augmentation, or number of training epochs for the main experiments. Only the physical-extension studies mention epoch counts (e.g., "100 epochs", "200 epochs"). The missing hyperparameters prevent independent reproduction without reading the source code.

**Recommendation:** Add a "Training Hyperparameters" table or paragraph to the Supplementary Methods (e.g., after `subsec:eval-protocol-details`) listing: optimizer, initial learning rate, batch size, epochs, scheduler, weight decay, and augmentation for each backbone/dataset combination.

---

### H5. Forward equation references in Results before Methodology appears

**File / line:**
- `compute_vit/paper/latex_gpt/main.tex:46–49` — Results and Discussion are compiled *before* Methodology and Experimental Setup.

**Problem:** Because of this order, every equation reference in Results is a forward reference. For example:
- `05_results.tex:13` — "recovered weight law in Eq.~\ref{eq:scale-recovery}" (Eq. 1 appears in `03_methodology.tex`)
- `05_results.tex:41` — "Ensemble HAT objective (Eq.~\ref{eq:hat-ensemble})" (Eq. 3 appears in `03_methodology.tex`)
- `05_results.tex:46` — "inverse-gamma preprocessor $P_{\text{in}} = X^{1/\gamma_{\text{phys}}}$ (Eq.~\ref{eq:inverse-gamma})" (Eq. 4 appears in `03_methodology.tex`)

LaTeX resolves these technically, but readers encounter references to equations they have not yet seen. Nature Communications allows Methods-after-Discussion, but the density of forward references to *four* different equations in the Results section is poor reader experience.

**Recommendation:** Either (a) move Methodology before Results, or (b) add brief inline reminders of each equation's content when first referenced in Results, so readers are not forced to flip backward.

---

## 3. MEDIUM ISSUES

### M1. Supplementary table "Degradation" columns use \% when meaning percentage points

**Files / lines:**
- `compute_vit/paper/latex_gpt/supplementary.tex:636–639` — Table `tab:asymmetry-sensitivity`: degradation entries "1.49\%", "6.05\%", "57.97\%", "81.78\%"
- `compute_vit/paper/latex_gpt/supplementary.tex:677–688` — Table `tab:nonideality-sensitivity`: degradation entries "0.96\%", "2.50\%", etc.

**Problem:** In both tables, "Degradation" is the arithmetic difference between two accuracy percentages (e.g., 91.78\% → 90.29\% = 1.49 pp). Labeling this as "1.49\%" is ambiguous: it could be interpreted as a relative percent drop (1.49/91.78 = 1.6\%). Scientific convention requires "pp" or "percentage points" for arithmetic differences between percentages.

**Recommendation:** Change column headers to "Degradation (pp)" and ensure all entries use "pp".

---

### M2. 88.41\% cadence scan not explicitly labeled as a 50-epoch training ablation in main text

**File / line:**
- `compute_vit/paper/latex_gpt/sections/05_results.tex:63` — "An exploratory single-run cadence scan (Supplementary Fig.~\SuppFigZeroShot) shows epoch-level resampling reaches 88.41\%, versus 87.18\% (fixed) and 86.16\% (per-batch)."

**Problem:** The supplementary figure caption (`supplementary.tex:480`) correctly notes: "In this **50-epoch scan**, epoch-level resampling reaches 88.41\%... The panel is intended to show that cadence matters, rather than to serve as the final paper-locked estimate for every schedule." However, the **main text** does not mention the 50-epoch budget or that this is a separate training ablation. The 88.41\% value comes from a model trained for 50 epochs, whereas the locked 86.37\% ensemble number comes from the canonical 100-epoch checkpoint. They are not directly comparable.

`JSON_INVESTIGATION_20260419.md` warns:
> "**Discard 88.41%** from any claim about the ensemble checkpoint's inference accuracy. If it is cited, it must be explicitly labeled as 'separate 50-epoch training ablation'."

**Recommendation:** Add "(50-epoch training ablation)" after "88.41\%" in the main text, or at minimum after "single-run cadence scan."

---

### M3. Compound stress test (89.61\%) lacks variance or replication detail in main text

**File / line:**
- `compute_vit/paper/latex_gpt/sections/06_discussion.tex:30` — "A single-run compound stress test combining all modeled non-idealities (2\% C2C, 3\% D2D, 6-bit ADC, 1\% IR drop, 1\% sneak path, and $1{,}000$ s retention) maintained an 89.61\% accuracy for Tiny-ViT"

**Problem:** The text correctly labels it "single-run," which is good. However, the Discussion presents this as evidence that "the framework remains reasonably resilient overall." A single-run result on a compound stress test is weak evidence for a broad resilience claim. No confidence interval or replication is provided.

**Recommendation:** Either replicate the compound stress test with 3–5 seeds and report mean ± std, or soften the sentence to "A single-run probe suggests that..." to avoid overstating the evidentiary weight.

---

## 4. LOW ISSUES

### L1. "Approximately 88\% of parameters are assigned to analog execution" lacks provenance

**File / line:**
- `compute_vit/paper/latex_gpt/sections/03_methodology.tex:10` — "Under this mapping, approximately 88\% of parameters are assigned to analog execution, whereas roughly 60\% of the estimated energy remains in the digital domain under the present placeholder constants..."

**Problem:** Neither a calculation nor a reference is provided for the 88\% figure. It is presented as a fact without derivation.

**Recommendation:** Add a parenthetical note or supplementary table showing the parameter count breakdown by operator domain for Tiny-ViT-5M.

---

### L2. 08_appendix.tex is orphaned

**File:** `compute_vit/paper/latex_gpt/sections/08_appendix.tex`

**Problem:** This file is not included in `main.tex` or in `supplementary.tex`. Its content (Parameter Provenance) is duplicated in `supplementary.tex` (Section `subsec:parameter-provenance`). The orphaned file risks confusion during production.

**Recommendation:** Delete `08_appendix.tex` from the submission bundle or add a comment at the top stating it is a legacy file and should not be compiled.

---

## 5. SCIENTIFIC ACCURACY — LOCKED NUMBER VERIFICATION

| Locked Number (per JSON_INVESTIGATION) | Appears in Manuscript? | Location | Verdict |
|:--|:--|:--|:--|
| **91.69%** V4 canonical eval mean (10-run MC) | **No** | Not cited in main text; supplementary Table S2 uses 91.94% (training best) with explicit "best-checkpoint" label. | **OK** — 91.69% is not used; 91.94% is correctly labeled. |
| **86.37 ± 1.54%** Ensemble HAT fresh-instance | **Yes** | Abstract, Introduction, Results §5.6, Conclusion | **OK** — matches `fresh_instance_eval.json`. |
| **88.53 ± 0.08%** OPECT zero-shot | **Yes** | Abstract, Results §5.7, Conclusion | **OK** — matches source data. |
| **27.72 ± 0.82%** NL=2.0 severe nonlinearity | **Yes** | Abstract, Results §5.6, Conclusion | **OK** — matches `v4_nl2_hat_eval_results_gpt.json`. |
| **+5.8 pp** inverse-gamma at γ_phys=2.0 | **Yes** | Abstract, Introduction, Results §5.3 | **OK** — 89.85% vs 84.04% = +5.81 pp; rounded correctly. |
| **10.00%** Standard HAT fresh-instance | **Yes** | Abstract, Introduction, Results §5.4/§5.7, Discussion §6.1/§6.2, Conclusion | **BROKEN** — see C1. |
| **97.39 ± 0.00%** V2 zero-noise hybrid control | **Yes** | Results §5.2 | **OK** — deterministic, zero variance is expected. |
| **88.41%** Epoch-level cadence scan | **Yes** | Results §5.6 | **OK** — labeled "exploratory single-run," but see M2 for incomplete labeling. |

---

## 6. INTERNAL CONSISTENCY CHECKS

| Check | Finding | Severity |
|:--|:--|:--|
| Abstract vs Results | All abstract claims have corresponding results passages. | Pass |
| Introduction contributions vs delivered | Four contributions listed in §1 all appear in Results/Discussion. | Pass |
| Figure/table reference order | Main text references Fig 4, Fig 5, Fig contour-map, Fig ensemble-hat-concept, Fig case-study-transfer in order of appearance. | Pass |
| Related Work inclusion | `02_related_work.tex` is **not included** in `main.tex`. | **Critical** (C2) |
| Equation forward references | Eq. 1–4 are referenced in Results but defined in Methodology (compiled later). | High (H5) |
| Rebuttal R1 support | "§6 defers ImageNet" is **fabricated**; §6.3 never names ImageNet. | High (H3) |
| Rebuttal R5 support | External baseline caveat exists only in omitted Related Work. | High (H1) |
| Rebuttal R8 support | Endurance argument is **absent** from manuscript. | High (H2) |

---

## 7. COMPLETENESS CHECKS

| Check | Finding | Severity |
|:--|:--|:--|
| Methods described for all results | Yes — all physical extensions (front-end, NL, Ensemble HAT, retention, OPECT) are described in §3 or Supplementary. | Pass |
| Acronyms defined on first use | CIM, ADC, HAT, ViT, CNN, D2D, C2C, OPECT, STE, MLP, IR, PCM, RRAM are all defined on first use. | Pass |
| Experimental setup reproducibility | **Fail** — hyperparameters (lr, batch size, optimizer, schedule, augmentation) are absent from both main text and supplementary despite explicit promises. | High (H4) |
| Energy model disclosure | Repeatedly labeled as "first-order," "placeholder constants," "not chip-predictive." | Pass |
| Best-checkpoint disclosure | §5.1 states: "All accuracy values reported for noisy and HAT deployments are best-checkpoint results unless otherwise stated." | Pass |
| Cycle endurance | Not mentioned. | High (H2) |

---

## 8. TONE AND SCOPE CHECKS

| Check | Finding | Severity |
|:--|:--|:--|
| Scope limited to simulation | Yes — repeatedly stated as "behavioral simulation framework," "simulation-based materials-to-system decision aid," "prospective first-order behavioral simulation study." | Pass |
| Limitations honestly disclosed | §6.5 discloses energy placeholders, unmodeled IR drop/sneak paths/temperature, spatially correlated D2D, heavy-tailed distributions, NL=2.0 surrogate approximation, and best-checkpoint reporting. | Pass |
| Tone appropriate for Nature Communications | Professional, cautious, non-promotional. | Pass |
| Overstated claims | "5-seed means" for CrossSim is an overstatement (C3). "Overwhelming standard HAT" in main text is qualified by a test against chance, not against standard HAT directly (minor imprecision). | Critical (C3) |

---

## 9. OVERALL VERDICT

**NEEDS MAJOR REVISION**

The manuscript is scientifically sound in its qualitative claims and appropriately scoped as a simulation study, but three CRITICAL defects require correction before submission:

1. **Replace or verify the 10.00\% standard-HAT fresh-instance baseline.** If the re-run confirms a numerical artifact, the headline contrast (10.00\% → 86.37\%) must be revised.
2. **Restore the Related Work section to `main.tex`.** Its omission removes the only manuscript-level acknowledgment that Ensemble HAT lacks an external multi-instance baseline, weakening the rebuttal to R5.
3. **Correct or disclose the CrossSim comparison statistics.** The "5-seed means" claim is factually wrong, and the 1000-sample subset must be disclosed.

Once these three issues are resolved, the remaining HIGH and MEDIUM items (hyperparameter table, endurance caveat, R1 citation fix, unit clarifications) can be addressed in a minor revision pass.

---

*Review completed 2026-04-19. All line references verified against `compute_vit/paper/latex_gpt/sections/*.tex`, `main.tex`, `supplementary.tex`, `cover_letter.tex`, `JSON_INVESTIGATION_20260419.md`, and `KIMI_REBUTTAL_COVERAGE_AUDIT_20260419.md`.*
