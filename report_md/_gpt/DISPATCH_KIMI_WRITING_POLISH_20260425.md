# DISPATCH KIMI — Writing Polish + Reproducibility Cookbook (Phase 3)
**Date:** 2026-04-25 01:50 CST
**Issued by:** Claude
**Assignee:** Kimi
**Authority:** CLAUDE_PROACTIVE_SPRINT_PLAN_20260425.md Phase 3
**Priority:** MEDIUM (depends on Phase 1 + Phase 2 outputs landing first, but skeleton can start now)
**Time budget:** ~3-4 days

---

## 0. Mission

Lift the integrated manuscript from "scrubbed and accurate" to "Nat-Electronics-editor-friendly". Senior-paper editorial pass. Plus reproducibility cookbook supplementary that reviewers love.

---

## 1. Task A — Section opening + closing sentences audit

### Goal
Every section starts with a strong topic sentence (states the section's claim) and ends with a clear bridge (sets up the next section). This is paper-craft 101 but easy to neglect during scrub iterations.

### Method
For each of these files, audit opening + closing of every subsection:
- `paper/latex_gpt/sections/00_abstract.tex`
- `paper/latex_gpt/sections/01_introduction.tex`
- `paper/latex_gpt/sections/02_related_work.tex`
- `paper/latex_gpt/sections/03_methodology.tex`
- `paper/latex_gpt/sections/04_experimental_setup.tex`
- `paper/latex_gpt/sections/05_results.tex`
- `paper/latex_gpt/sections/06_discussion.tex`
- `paper/latex_gpt/sections/07_conclusion.tex`

For each subsection:
- Opening sentence: does it state the claim, or does it dive into mechanics? Rewrite if mechanics-first.
- Closing sentence: does it bridge to next section, or just stop? Add bridge if missing.

### Deliverable
Edit canonical `.tex` files in place. Append summary of changes to `KIMI_WRITING_POLISH_20260425.md`.

### Time: ~1 day

---

## 2. Task B — Discussion narrative arc restructuring

### Goal
Discussion §6 currently follows a "by topic" structure (bottlenecks / sensitivity / scale-masking / energy / limitations). Restructure to a clear narrative arc:

1. **§6.1 Diagnosis**: Hardware-instance overfitting as primary failure mode (subsume current §6.1)
2. **§6.2 Treatment**: Ensemble HAT mitigation across three scenarios (subsume current §6.2 + Tiny-ViT sensitivity)
3. **§6.3 Mechanism**: Theory + empirical — cite Phase 1 KIMI-THEORY-2 + Phase 2 Codex empirical analyses
4. **§6.4 Implications**: Design rules callout (new — see Task C)
5. **§6.5 Limitations + Outlook**: subsume current limitations + outlook

This Diagnosis → Treatment → Mechanism → Implications → Limitations arc reads like a top-tier paper.

### Constraints
- Don't lose any current content; reorganize, don't delete
- Each renamed subsection has clear opening sentence stating its function
- Cross-references update (figure refs, equation refs, etc.)
- Total length similar to current

### Deliverable
Restructured `paper/latex_gpt/sections/06_discussion.tex`.

### Time: ~1 day

---

## 3. Task C — Design rules callout box

### Goal
End of §6.4 — a one-page boxed callout titled **"Design rules for organic optoelectronic CIM transformer deployment"**. Reviewer-friendly takeaway block that engineers can use directly.

### Content (5-7 actionable rules with quantitative thresholds)

Draft (Kimi to refine):

> **Box 1: Design rules for organic optoelectronic CIM transformer deployment**
>
> 1. **Secure ≥6-bit ADC readout first.** Below 6-bit, transformer inference degrades by ~7 pp per row across all D2D levels (Section~\ref{subsec:iso-accuracy}).
>
> 2. **Then minimize device-to-device variability.** Within the operational envelope ($\geq$6-bit, $\sigma_{\mathrm{D2D}} \leq 15\%$), D2D explains 92.2\% of residual accuracy variance.
>
> 3. **Train with mismatch-distributed objective (Ensemble HAT), not fixed-mask.** Standard fixed-mask HAT collapses on fresh hardware instances (10\%); Ensemble HAT recovers $86.37\pm1.54\%$ canonical and $88.53\pm0.08\%$ on literature-calibrated reference.
>
> 4. **Per-epoch D2D resampling, not per-batch.** Empirical ablation: per-epoch reaches 88.41\%; per-batch only 86.16\%; fixed 87.18\%.
>
> 5. **Apply scale recovery calibration after readout.** Without it, the analog perturbation is no longer bounded below the LSB and the recovered-weight protection vanishes.
>
> 6. **Compensate front-end sublinear photoresponse via inverse-gamma preprocessing.** Restores up to +5.8 pp at $\gamma_{\mathrm{phys}}=2.0$.
>
> 7. **Calibrate against measured D2D distribution when available.** Literature priors are an upper-bound proxy; deployment risk should be re-assessed once fabricated array statistics are in hand (see Supp Note S-HW).

### Format
LaTeX `\fbox{}` or `tcolorbox` (Kimi chooses). Place at end of §6.4.

### Deliverable
Inserted into `paper/latex_gpt/sections/06_discussion.tex` end of §6.4.

### Time: ~2 hours

---

## 4. Task D — Reproducibility cookbook (new Supp Note)

### Goal
3-page step-by-step "reproduce paper-1 from clone to fresh-eval" guide. Reviewers + future users love this.

### File
`paper/latex_gpt/supplementary/S_reproducibility.tex`

### Content (3 pages)

#### S-R.1 Environment setup (~0.5 page)
- `git clone <repo>` at commit `<hash to be filled>`
- `conda env create -f environment.yml`
- Verify GPU + CUDA versions

#### S-R.2 Verification suite (~0.5 page)
- `python test_dual_bug_fix.py` → expect 7/7
- `python test_groupwise_nl_wrapper.py` → expect 9/9
- `python test_adc_perinstance_calibration.py` → expect pass

#### S-R.3 Canonical Ensemble HAT training (~0.75 page)
- Command: `python train_tinyvit_ensemble.py --hat-training True --noise-mode uniform --nl-ltp 1.0 --nl-ltd -1.0 --sigma-d2d 0.10 --sigma-c2c 0.05 --epochs 100 --batch-size 64 --seed <S>`
- Expected wall-clock on RTX 5070 Ti: ~10-12 hours
- Expected best test accuracy: ~91% (single seed)

#### S-R.4 Fresh-instance evaluation (~0.75 page)
- Command: `python eval_fresh_instances_postfix.py --checkpoint <ckpt> --num-instances 10 --mc-runs 5 --nl-ltp 1.0 --nl-ltd -1.0`
- Expected wall-clock: ~30-45 min
- Expected aggregate: $86.37 \pm 1.54\%$ for canonical Ensemble HAT

#### S-R.5 ADC ablation (~0.5 page)
- Command: `python scripts/_gpt/eval_fresh_instances_adc_ablation.py --checkpoint <ckpt> --bits 8 --calibration-scope per_instance`
- Expected wall-clock: ~30 min
- Expected: within 0.5 pp of ADC-off result

### Constraints
- Concrete commands, not pseudo-code
- Real expected outputs, not approximate
- Specify hardware (CPU + GPU model) + library versions
- Note non-determinism sources (seeded but cuDNN nondeterministic in some ops)

### Deliverable
`paper/latex_gpt/supplementary/S_reproducibility.tex` ready for `\input` into main supplementary.

### Time: ~0.5 day

---

## 5. Task E — Figure captions self-contained audit

### Goal
Every figure caption must be readable without body text. Reviewer who reads only the figures should understand the result.

### Method
Audit each figure in `paper/figures/`:
- Fig 4 accuracy comparison
- Fig 5 HAT recovery
- Fig 10 zero-shot transferability
- Fig contour-map
- Fig ensemble-hat concept
- Fig postfix severe NL
- Fig S-noise sweep
- Fig S-retention
- Fig S-frontend
- Fig S-corr-d2d
- Phase 2 new figures (after they land): Hessian / loss landscape / CKA / per-layer / checkpoint avg

For each:
- Caption opens with ONE-sentence claim of what the figure shows
- Defines all axes / colors / shaded regions
- States sample size / error bar definition
- Bridges to relevant section (e.g., "see also \S5.7")

### Deliverable
Edits to canonical `.tex` files. Summary in `KIMI_WRITING_POLISH_20260425.md`.

### Time: ~0.5 day

---

## 6. Task F — Acknowledgments / Author contributions / Funding skeleton

### Goal
Submission packet items that are easy to forget. Add to `cover_letter.tex` or as separate file.

### Content
- Acknowledgments: thank PhD collaborator for measured D2D data (forward-looking, can update after data lands), thank computing resources (8×40GB at NVIDIA Apamayo), thank any reviewers
- Author contributions: per CRediT taxonomy (Conceptualization / Methodology / Software / Validation / Investigation / Writing / Visualization / Supervision / Funding)
- Funding statement: skeleton for user to fill specifics

### Deliverable
`paper/latex_gpt/acknowledgments_funding_credits.tex` skeleton. User completes funding details.

### Time: ~30 min

---

## 7. Constraints across all tasks

- **Zone discipline**: every number cited maps to NARRATIVE_PIVOT zone 3A / 3B / 3C
- **No bug-retrospective language** (continues from earlier doctrine)
- **"Hook diagnostic" not "deployment-fidelity"** for ADC numbers
- **"Structural analogue" not "exact equivalence"** for theory connections
- **No new claims** beyond what data + theory support
- **Senior-paper voice**: declarative not hedging; precise not vague; technical but not jargon-laden

---

## 8. Sequencing within Phase 3

Day 4-5 (after Phase 1 + 2 outputs land):
- Task B Discussion restructuring (uses Phase 1 + 2 deliverables)
- Task A opening/closing audit

Day 5-6:
- Task C design rules callout
- Task E figure captions audit
- Task D reproducibility cookbook

Day 7:
- Task F acknowledgments skeleton
- Final consistency pass on all changes

---

## 9. Coordination with Phase 5 integration

After Phase 3 lands:
- Claude does Phase 5 integration pass: pulls Phase 1 theory + Phase 2 figures + Phase 3 polish into one cohesive submission package
- Kimi flags any cross-section inconsistencies during Phase 3 for Phase 5 attention
- Phase 5 is one-pass, no further Kimi input needed

---

## 10. Deliverables summary

| File | Source task |
|:--|:--|
| Edits to all `paper/latex_gpt/sections/*.tex` | A, B, C, E |
| `paper/latex_gpt/supplementary/S_reproducibility.tex` (new) | D |
| `paper/latex_gpt/acknowledgments_funding_credits.tex` (new) | F |
| `report_md/_gpt/KIMI_WRITING_POLISH_20260425.md` | Status + change summary per task |

---

## 11. Success criteria

- Reviewer who reads only the abstract + Discussion section understands the full contribution
- Reviewer who reads only the figures + captions can reconstruct the experimental story
- Engineer who reads only the design rules box knows what to build
- Independent researcher who reads only the reproducibility cookbook can replicate the headline result

These four "isolated reader" tests are how submission-readiness is measured.

No deadline. Polish is iterative; this is the discipline pass.
