# External Review Synthesis (GPT)

This file condenses the recent strict reviewer-style feedback (Hunyuan, DeepSeek, Kimi, Doubao, Qwen, Perplexity, NVIDIA-style review) into an actionable manuscript checklist.

## Overall Verdict Trend

- Common external assessment:
  - `Major Revision / Reject & Resubmit`
- Shared positive view:
  - the framework idea is novel and potentially valuable
  - the materials-to-system bridge is worth publishing if validated more rigorously
- Shared concern:
  - the current manuscript can overclaim relative to the present behavioral-model evidence

## Highest-Priority Shared Criticisms

### 1. Bridge Validity Still Needs a Concrete Case Study

Multiple reviewers independently converged on the same point:
- the JSON/profile substitution interface is promising
- but the manuscript still lacks a concrete demonstration of how a measured or literature-derived device profile is fitted, injected, and then compared against another profile or an idealized baseline

**Actionable implication**:
- add one compact measured-profile case study
- even a synthetic-measured or literature-derived example is better than leaving the bridge purely conceptual

### 2. Parameter Disclosure Must Be Complete

Reviewers repeatedly objected that core behavioral parameters can currently look arbitrary if they are not fully exposed with provenance.

Parameters explicitly called out:
- `sigma_C2C`
- `sigma_D2D`
- ADC assumptions
- retention constants
- `NL_LTP / NL_LTD`
- conductance window / effective state count

**Actionable implication**:
- ensure the paper or supplement clearly states which parameters are:
  - literature-anchored
  - assumed but plausible
  - stress-test-only

### 3. The Experimental Section Must Stay Extremely Clean

The harshest reviews focused on readability failures:
- unclear experiment aliases
- figure-number drift
- stale or inconsistent wording
- ambiguity between `best checkpoint` and `MC mean ± std`

**Actionable implication**:
- keep `best` vs `MC` strictly separated
- keep figure captions self-contained
- remove all stale placeholders and garbled text

### 4. Need Clearer Contrast Against Mainstream Inorganic CIM Simulators

Several reviews wanted a more explicit answer to:
- why not just use NeuroSim / MemTorch / AIHWKIT?

**Actionable implication**:
- keep the new `§2` differentiation
- emphasize:
  - explicit photoresponse modeling
  - profile-driven substitution for arbitrary device technologies
  - unified accuracy / retention / energy protocol across CNN and transformer backbones

### 5. Conclusions Must Stay Bounded

The most common overclaim risks identified were:
- treating behavioral trends as if they were chip-predictive
- overstating CNN vs Transformer differences without caveats
- overstating Flowers-102 as a universal failure case

**Locked safe wording**:
- `first-order behavioral simulation framework`
- `Flowers-102` = `low-data boundary` / `data-volume floor`
- `Task 34` = `distribution-matched recovery`
- `Task 36` = `architecture-gap evidence`, not universal CNN superiority

### 6. The Current Paper Is Still Closer to a Parameter-Sensitivity Study Than a Validated Emulator

The newest Perplexity-style review sharpened a point that was already implicit in earlier feedback:
- the work is valuable
- but, in its present form, it is still better described as a **behavioral parameter-sensitivity framework** than as a validated predictive hardware emulator

**Actionable implication**:
- Abstract, Results, Discussion, and Conclusion should keep explicitly distinguishing:
  - what is demonstrated by simulation under literature-anchored priors
  - what remains to be validated by measured-device substitution
  - what should be treated only as stress-test evidence

### 7. Author / Reproducibility Metadata Cannot Stay Implicit

The new reviews also called out several submission-readiness issues that are mundane but fatal in practice:
- `Author list TBD` is unacceptable at submission time
- Monte Carlo sample counts must be stated explicitly
- code / config release path must be clear
- training hyperparameters and HAT scheduling details must be reproducible

**Actionable implication**:
- create or finalize a submission-facing reproducibility table that includes:
  - optimizer
  - learning-rate schedule
  - batch size
  - epoch count
  - Monte Carlo sample counts
  - profile source / checkpoint identity / evaluation semantics

### 8. Several Limitations Need Their Own Honest Subsection

Perplexity and the NVIDIA-style review both converged on the same structural concern:
- some limitations are currently acknowledged, but they are spread across the text rather than framed as a deliberate boundary statement

The most important ones are:
- no measured-device calibration loop yet
- no temperature sensitivity model
- no full ADC/DAQ physical timing/area model
- no state-dependent retention validation against real measurements
- scratch-vs-finetune confound in ConvNeXt vs Tiny-ViT comparisons

**Actionable implication**:
- add or strengthen an explicit `Limitations` subsection so the paper reads as self-aware rather than defensive

## Secondary But Important Reviewer Requests

### 6. ADC Discussion Should Stay Physically Grounded

Reviewers noted that saying `6-bit ADC is the bottleneck` can be too abstract if area / delay / readout cost are not acknowledged.

**Actionable implication**:
- keep the claim phrased as a `critical practical threshold under the present simulator assumptions`
- avoid implying a hardware-universal optimum

### 7. Flowers-102 Interpretation Needs Restraint

Reviewers objected to any direct statement that low data volume is the sole cause.

**Safe interpretation**:
- current HAT recipe fails on this low-data regime
- data volume is the leading interpretation, but domain gap and recipe mismatch remain plausible contributors

### 8. Transformer Fragility Needs Confounder Awareness

At least one review highlighted the scratch-vs-finetune confound:
- ConvNeXt is from scratch
- Tiny-ViT is fine-tuned

**Actionable implication**:
- avoid absolute statements that architecture alone explains the full gap
- keep wording focused on observed deployment behavior under the present training/testbeds

### 9. Fresh-Instance Transfer Is Now a Stronger Story, but It Must Be Written Precisely

The newer Gemini result changes the balance of evidence:
- standard `V4` fresh-instance transfer collapses to `10.00 ± 0.00%`
- `Task 37 Ensemble HAT` rises to `86.37 ± 1.54%`

This is now a genuine strength of the paper.

**But**:
- it does not prove universal hardware transferability
- it does not yet eliminate the need for literature-derived or measured-profile substitution
- it should be framed as **evidence that multi-instance-aware training can mitigate hardware-instance overfitting in this setting**

## Recommended Immediate Priorities

1. Add a measured-profile case study subsection or supplement.
2. Keep parameter provenance explicit and centralized.
3. Maintain strict `best vs MC` separation everywhere.
4. Preserve the simulator differentiation in `§2`.
5. Add a submission-facing reproducibility / hyperparameter disclosure block.
6. Add or strengthen an explicit limitations subsection.
7. Keep all conclusions bounded by the behavioral-model caveats.

## Codex Judgment

My own current reviewer-style judgment is:

- the paper now has a much stronger scientific spine than it did earlier, especially because:
  - cross-dataset complexity scaling is now well supported
  - physical-stress tests reveal meaningful failure modes
  - `Task 37` provides a real positive result on fresh-instance transfer
- however, the paper is **still vulnerable on rigor-of-framing rather than lack-of-results**

The two most important remaining risks are:
1. readers may still misread the framework as more predictive than it currently is
2. the bridge claim still looks stronger than the present evidence unless the measured/literature-derived profile workflow is shown very concretely

If I were reducing risk for resubmission, I would prioritize:
1. a literature-derived fitted-profile case study
2. a fully explicit parameter-provenance appendix/table
3. a crisp limitations subsection
4. a reproducibility block with MC counts and HAT details

## Alignment Note

This synthesis should be used as a reviewer-facing pressure test for both:
- the English manuscript
- the Chinese mirrored manuscript

It is not a replacement for `CANONICAL_RESULT_LOCK_gpt.md`; it is a risk-management companion.

## 2026-04-08 Re-review Update

The newest round of reviewer-style feedback materially changes the decision boundary:

- older overall trend:
  - `Major Revision / Reject & Resubmit`
- newest trend:
  - several reviewers now place the paper at
    - `Conditional Accept`
    - `Minor Revision`
    - or `Minor Revision bordering on Major`

This shift is driven by three concrete additions that multiple reviewers explicitly praised:

1. `Task 37 Ensemble HAT`
   - now viewed as a real methodological contribution rather than only a rescue experiment
   - strongest locked evidence:
     - standard `V4` fresh-instance = `10.00 ± 0.00%`
     - ensemble HAT fresh-instance = `86.37 ± 1.54%`
2. `§5.11` literature-calibrated Zhang 2026 OPECT case study
   - now accepted as a genuine bridge demonstration
   - but still not equivalent to full measured-device closure
3. expanded `Limitations` + `Reproducibility`
   - reviewers now recognize that the paper is being framed more honestly as a bounded behavioral framework

### Newly Convergent Positive Consensus

The latest reviewers repeatedly praised:
- Ensemble HAT as the strongest revision
- the Zhang 2026 literature-derived device case study
- the explicit limitations section
- the clearer framing of the framework as a reusable methodology, not a chip-accurate emulator

### Still-Open Mandatory / Near-Mandatory Issues

Across the new reviews, the most consistent remaining blockers are:

1. **Author metadata**
   - this is the only currently confirmed formal red flag in the repo
   - `paper/latex_gpt/main.tex` still contains:
     - `\\author{Author list TBD}`
   - this must be replaced before submission

2. **Basic proofreading / spelling / formatting**
   - several reviewers explicitly downgraded the paper because of proofreading quality
   - some of these complaints may come from a generated PDF snapshot rather than current markdown alone
   - regardless, a full final proofread remains mandatory

3. **Ensemble HAT cost discussion**
   - multiple reviewers now accept the method, but want one explicit sentence about cost
   - e.g. training-time overhead from per-epoch D2D resampling, and why that one-time cost is acceptable for deployment-critical settings

### High-Value Quantitative Clarifications

These are not as universally mandatory as the three items above, but they are the most likely to strengthen acceptance:

1. **Zhang case-study uncertainty / proxy-estimate sensitivity**
   - reviewers want a clearer accounting of how `sigma_c2c = 2%` and `sigma_d2d = 3%` were obtained
   - best next step:
     - appendix note or sensitivity scan around those proxy values

2. **Interconnect / routing bounding analysis for energy**
   - several reviewers accept the current first-order energy framing but still want a bound:
     - if interconnect / data marshaling overhead were 10% / 30% / 50%, how much would the `11.45x` claim compress?

3. **Flowers-102 causality remains a hypothesis**
   - the newer reviewers explicitly appreciated the softened language
   - but still do not accept `data starvation` as a proved causal statement without ablations
   - current safe phrasing should remain:
     - low-data boundary / hypothesis, not proof

4. **Nonlinear-write failure must remain visible**
   - the `27.72 ± 0.82%` result is now seen as a serious boundary of applicability
   - reviewers are more comfortable if this is framed as:
     - a real remaining failure mode
     - not just an inconvenient outlier

5. **Scratch-vs-finetune confound**
   - newer reviews continue to push on the ConvNeXt-vs-Tiny-ViT fairness issue
   - safe writing should keep emphasizing:
     - complementary testbeds
     - observed deployment behavior under different training protocols
     - not pure architecture superiority

### Likely Snapshot-Specific or Partly Stale Critiques

Some complaints in the newest reviews may reflect an older compiled PDF snapshot rather than the current repository state. These should be verified before spending more effort:

- claims that canonical `V4` or retention numerics may have drifted after Gemini's code changes
  - now checked and closed by Claude/Codex:
    - `91.69 ± 0.23%` canonical accuracy
    - retention still plateaus near `~79%`
- claims that fresh-instance mitigation remained unresolved
  - now stale because `Task 37` has fresh-instance evidence
- some figure-pending complaints may refer to an earlier compiled PDF
  - the repo still contains placeholder logic in plotting utilities
  - but manuscript-level action should be based on the current submission files, not old export traces

### Practical Decision Frame for Claude

If Claude wants the highest-value next actions, the review synthesis now suggests a narrow priority list:

1. replace `Author list TBD`
2. do one full proofreading / typo / figure-reference sweep
3. add a 1-paragraph **Ensemble HAT cost** discussion
4. optionally add one compact **proxy-uncertainty / energy-bounding** note

In other words:
- the paper is no longer primarily blocked by lack of results
- it is now primarily blocked by **submission hygiene** and **quantitative framing discipline**

## 2026-04-09 Addendum: `审稿人意见from_model.md`

The newly collected model-generated reviews in `/home/qiaosir/projects/compute_vit/report_md/审稿人意见from_model.md` do not materially change the existing external-review picture, but they sharpen three themes:

1. **Nature Communications fit remains questioned**
   - several reviewers now explicitly say the current contribution may fit a strong hardware/EDA venue more naturally unless the paper keeps emphasizing that its lasting value is the decision-bridge methodology, not chip-predictive physical emulation
   - practical implication:
     - keep the "first-order behavioral simulation" framing prominent
     - avoid language that sounds like a full hardware-validation claim

2. **AIHWKIT / inorganic-tool comparison is still a reviewer pressure point**
   - the newer reviews continue to ask for either:
     - a true side-by-side benchmark, or
     - a sharper explanation of what is uniquely convenient in the present framework
   - practical implication:
     - current manuscript stance is acceptable only if it remains explicit that AIHWKIT cross-validation is future work, not silently omitted

3. **Attention-map figures are stronger with one compact quantitative supplement**
   - this was a recurring request in the new reviews
   - status update:
     - now partially addressed in the manuscript by adding mean head-averaged attention entropy numbers for the representative samples
     - current narrative support:
       - V1: `3.38`
       - V3: `3.61`
       - V4: `3.07`
       - V4 restores the correct class on all three displayed examples, while V3 is correct on only one

### Practical reading of the addendum

These new reviews mostly reinforce the same conclusion:
- the paper is strongest when presented as a **profile-driven deployment-decision framework**
- the most valuable defenses are:
  - bounded claims
  - quantitative supplements to qualitative figures
  - honest acknowledgment that AIHWKIT-style cross-validation remains future work

## 2026-04-09 Addendum B: `审稿人意见from_model.md` distilled for Claude

I re-read the full bundle in:
- `/home/qiaosir/projects/compute_vit/report_md/审稿人意见from_model.md`

The new bundle does **not** overturn the current strategy, but it is useful because it separates into:
- a few still-valid manuscript issues
- several partly stale criticisms that likely target an older PDF snapshot

### Still-valid pressure points

1. **Nature Communications fit remains fragile**
   - multiple model-reviewers still read the paper as better suited to a strong methodology / device-modeling venue unless we keep the "decision bridge" framing front and center
   - safest response:
     - keep `first-order behavioral simulation framework`
     - keep "deployment-decision bridge"
     - avoid predictive-emulator language

2. **AIHWKIT / inorganic baseline comparison remains the most persistent external-comparison request**
   - the bundle repeatedly asks for either:
     - one true side-by-side regime, or
     - a sharper explanation of why the current framework is uniquely convenient for organic optoelectronic profile substitution
   - current safe stance:
     - explicit future-work item
     - no silent implication that this comparison has already been done

3. **Reference placeholders are still a real submission risk**
   - repository audit confirms `refs_gpt.bib` still contains many `and others` / `Author and others` style placeholders
   - this criticism is current, not stale

4. **Training-variance concern is only partially closed**
   - newer reviews ask for seed-aware training evidence
   - current repo status:
     - `V1` three-seed is now a real positive defense
     - but `V4/C1/C4` multi-seed evidence is still in progress

5. **Energy framing still needs disciplined wording**
   - the new bundle repeatedly pushes on the `11.45x` claim
   - current manuscript is safer than earlier drafts because §6 already bounds interconnect overhead
   - but the main §5 sentence still reads stronger than ideal unless explicitly interpreted as operating-assumption-dependent

6. **Flowers-102 causality must remain hypothesis-level**
   - the bundle keeps hitting this point
   - current safe wording remains correct:
     - low-data boundary / hypothesis, not proof

### Criticisms that are partly stale or snapshot-dependent

1. **`Author list TBD`**
   - no longer true in the repo
   - current `paper/latex_gpt/main.tex` now has:
     - `\\author{Songqiao Li ...}`

2. **Attention maps are purely qualitative**
   - now only partly true
   - the manuscript now includes a compact entropy supplement:
     - `V1 = 3.38`
     - `V3 = 3.61`
     - `V4 = 3.07`
   - this does not make the section fully quantitative, but it is no longer "visual only"

3. **Some broad layout / placeholder complaints**
   - several likely refer to older compiled snapshots before the recent float cleanup, appendix compression, and figure resizing
   - manuscript-level action should therefore focus on current `.tex` output, not old exported PDFs

### Important active manuscript issues revealed by spot-check

1. **Front-end subsection still contains a likely figure-reference bug**
   - current text in `05_results.tex` still says:
     - `Figure 6 summarizes the ResNet-18 (R4) and Tiny-ViT (V6) results under various frontend configurations.`
   - this should be rechecked against the current compiled figure numbering

2. **Main energy-result sentence still deserves one more caveat**
   - current text says:
     - `11.45x reduction ... under the present operation-count assumptions`
   - better than older drafts, but still a natural place for reviewers to press if they want "upper-bound" language closer to the headline number

### Best practical reading for Claude

The new model-generated reviews mostly say:
- the paper is now scientifically stronger than before
- the remaining vulnerabilities are less about missing experiments than about:
  - venue fit framing
  - external-baseline expectations
  - citation hygiene
  - variance / uncertainty disclosure
  - and a few lingering wording / figure-reference details

If only a short response plan is needed, the highest-value actions are:
1. clean placeholder bibliography entries
2. fix the front-end figure cross-reference
3. keep `11.45x` bounded in the most visible sentence
4. continue using `V1` multi-seed as the reproducibility defense while the overnight queue fills in `V4/C1/C4`
