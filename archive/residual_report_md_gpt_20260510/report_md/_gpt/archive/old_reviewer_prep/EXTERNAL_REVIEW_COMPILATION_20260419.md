# External Review Compilation — Nature Communications Submission

**Date:** 2026-04-19
**Scope:** Multiple independent senior reviewer assessments of manuscript "Profile-Driven Hardware Simulation for Organic Optoelectronic Edge Vision"
**Target Journal:** Nature Communications
**Status:** Compilation of external review reports for internal triage

---

## Reviewer A — Detailed Technical Assessment

**Manuscript ID:** NCOMMS-24-XXXXX-Sim
**Title:** Profile-Driven Hardware Simulation for Organic Optoelectronic Edge Vision
**Reviewer Recommendation:** Major Revision Required (Leaning Acceptable if Revisions are Substantive)

### Overall Assessment

This manuscript presents a well-engineered, transparent, and highly detailed behavioral simulation study of analog in-memory computing for organic optoelectronic devices. The Ensemble HAT finding is genuine and significant—the recovery from 10% to 86% on fresh instances addresses a critical, often-overlooked deployment failure mode in analog AI. The methodological hygiene (locked numbers, seed reporting, Sobol sensitivity) is excellent.

However, the manuscript currently suffers from framing tension. It wants to be a "Materials-to-System Decision Aid," but the empirical scope (CIFAR-scale, ViT-Tiny) and lack of physical validation keep it firmly in the simulation methodology domain. The abstract and introduction are slightly over-rotated toward deployment claims, while the Discussion correctly hedges. This mismatch will trigger pushback from Nature Communications editors and reviewers who expect a clear, unhedged claim at the top.

### 1. Central Claim Stress Test: Ensemble HAT (10% → 86.37%)

**Defensibility:** Strong.
The 10.00% baseline is credible as a collapsed predictor (class-balanced chance for CIFAR-10). The supplementary Fig. S6 shows per-instance bars, confirming that standard HAT fails on every fresh array, not just on average. The framing survives scrutiny.

**Potential Reviewer Pushback:**
- Is this just "data augmentation" for D2D? Reviewers may argue that resampling the D2D mask per epoch is equivalent to domain randomization. The manuscript preempts this by distinguishing structured spatial mismatch from i.i.d. noise. You must defend this distinction in the rebuttal: "Standard domain randomization perturbs input data; we perturb the weight representation itself under a spatial correlation structure fixed per epoch."

**Recommendation:** Clarify in §3.7 caption or text that the 10.00% is not a random guess but a specific failure mode (e.g., predicting a single class with ~10% accuracy because CIFAR-10 is balanced). The manuscript currently implies this, but stating it explicitly closes a potential loophole.

### 2. Generality vs. Over-Reach: CIFAR vs. ImageNet

**Scoping Honesty:** Good, but slightly evasive.
The paper explicitly states "edge-scale datasets" and "CIFAR-scale transformer benchmarks." This is appropriate for a methods paper.

**First ImageNet-Scale Failure Mode Prediction:**
1. Throughput of Ensemble HAT: Resampling D2D masks requires re-quantizing weights per epoch. On ImageNet-1k with ViT-Base, this is computationally expensive but not prohibitive. The failure would be practical: researchers may balk at the training overhead.
2. State-Dependent Noise Amplification: In larger models, the proportional-noise collapse seen in V4 (10.00%) might occur even with Ensemble HAT because the softmax attention becomes more sensitive to token variance.
3. The manuscript does not acknowledge this. §4.5 Limitations focuses on hardware parasitics, not on model scale.

**Recommendation:** Add a sentence to §4.5: "The present evaluation uses CIFAR-scale backbones; scaling Ensemble HAT to ImageNet-sized ViTs remains an open challenge due to increased training overhead and potentially sharper sensitivity to proportional state-dependent noise in deeper attention layers."

### 3. Methodological Holes: Hardware-ML Reviewer's Checklist

| Hole | Severity | Current Mitigation | Remaining Risk |
|------|----------|-------------------|----------------|
| Gaussian D2D/C2C vs. real spatial correlation | High | Acknowledged in §4.5 ("spatially correlated D2D... absent"). | Reviewers may demand a sensitivity test (e.g., introduce a correlation length parameter). Suggestion: State explicitly that the framework can ingest a spatial covariance matrix from measured array data; the current Gaussian assumption is a placeholder. |
| CrossSim subset disclosure | Medium | Excellent transparency in Supplementary Note SX.Y. | A determined reviewer could argue that 1,000 images is too small to claim "consistent baseline." Response: The 86.2% vs. 83.7% difference is small; the 14 pp gap under noise is the real story. Frame this as a calibration difference, not a validation. The current wording is already careful. |
| Energy estimates | Low | §4.4 explicitly calls them "first-order upper bounds under placeholder constants." | No creep detected. The manuscript is honest here. |

**Additional Omission:** The manuscript does not discuss write-verify overhead. In real organic devices, achieving a precise 4-bit conductance state requires iterative program-and-verify pulses. The energy/latency model assumes ideal programming. This should be acknowledged in Limitations.

### 4. Severe-NL Supplementary Ablation (Table S16)

**Framing Honesty:** Good, but requires a preemptive strike in the main text.

The supplement states: "This is a backward-surrogate distortion effect... MLP is the dominant recoverable failure site... attention-side linearizations collapse structurally." This is clear.

However, a reviewer skimming the supplement might miss the crucial caveat: the MLP-linearized model's fresh-instance transfer is ~32% (much worse than Ensemble HAT's 86%) — this detail is not in the PDF you provided. If true, it must be added to Table S16's caption or a footnote. Without it, a reviewer might accuse you of hiding a "fifth contribution" (NL mitigation) that doesn't actually work in deployment.

**Recommendation:** Add a sentence to the Table S16 caption: "Note that while linearizing the MLP path identifies the bottleneck, this intervention does not recover fresh-instance transfer (~32%), confirming that this is a diagnostic insight rather than a deployable mitigation."

### 5. Rebuttal Risk: Top 3 Hardest Objections

| Rank | Objection | Likelihood of Major Revision | Fastest Disarmament |
|------|-----------|------------------------------|---------------------|
| 1 | "Where is the hardware validation? This is just a simulation paper." | 90% (if editor is materials-focused) | Pre-submit fix: Change title to "Simulation Framework for Organic Optoelectronic Compute-in-Memory..." and Abstract first sentence to "We present a simulation framework..." The current "Profile-Driven Hardware Simulation" is slightly misleading. Also, add to §4.5: "Validation against fabricated organic arrays is deferred to future work." (This is already implied but should be explicit). |
| 2 | "The 6-bit ADC cliff is obvious; we've known this from quantization literature." | 70% | The novelty is the Sobol decomposition showing the two-phase constraint hierarchy (ADC dominates only below 6-bit; D2D dominates above). Emphasize this in the abstract and conclusion. The current abstract buries this. Suggestion: Move "Sobol decomposition... S_ADC=0.98" earlier in the abstract. |
| 3 | "Ensemble HAT is just Multi-Instance HAT; it's a minor tweak." | 50% | The ablation showing per-epoch vs. per-batch vs. fixed (Fig. S6 right) is your defense. Per-batch hurts accuracy. This proves it's not just i.i.d. noise injection. Highlight this in the main text: "Per-batch perturbation degrades performance (86.16%), confirming that structured epoch-level resampling is required." |

### 6. Figures: Error Bar Consistency (Figure 1 / Figure 4)

**Issue:** Figure 1 mixes deterministic baselines (no error bars) with MC runs (error bars). The caption discloses this. Is it enough? For a specialized journal, yes. For Nature Communications' broad audience, no.

**Recommendation:** Add a visual cue. Place a small "dagger" (†) symbol next to bars without error bars, with a footnote: "† Deterministic baseline or single-run estimate; error bars omitted." This prevents a non-expert reader from assuming missing error bars mean zero variance.

### 7. Structure: Narrative-First Order

**Readability:** Good. The narrative-first order (Results before full Methods) is standard for NC and works well here. The Methods section is sufficiently detailed. No issue.

### 8. One-Liner Verdict

**Verdict:** (b) Major revision needed — but the revisions are cosmetic and framing adjustments, not new experiments. The core science is solid.

**Single most load-bearing reason:** The manuscript over-promises "deployment" in the title/abstract while the Discussion correctly limits itself to "simulation-based decision aid." This mismatch will provoke a "scope creep" rejection from an editor. Fix the framing, and the paper is a strong NC methods contribution.

---

## Reviewer B — Senior Hardware-ML + CIM Background

### 1. Central Claim Stress Test

Your headline claim—that Ensemble HAT recovers fresh-instance accuracy from 10.00% to 86.37±1.54%—is defensibly scoped and arguably the strongest algorithmic contribution of the paper.

**The ~10% Baseline:** Reporting exactly 10.00% on CIFAR-10 strongly implies a collapsed predictor (the network predicting a single class for all inputs), not just a noisy dispersion around class-balanced chance. Your framing is currently honest, but if a reviewer asks for raw per-instance outputs, you should be prepared to explicitly confirm that the network has suffered complete representational collapse.
**Survival:** The framing survives easily. Demonstrating that standard HAT severely overfits a single spatial mismatch map to the point of catastrophic collapse on fresh hardware is a highly impactful finding for the CIM community.

### 2. Generality vs. Over-reach

Your scoping to edge-scale datasets (CIFAR-10/100, Flowers-102) is appropriate and justified by the computational cost of simulating per-epoch hardware variation.

**ImageNet Failure Mode:** If pushed to ImageNet, the first failure mode would likely be fine-grained feature collapse driven by device-to-device (D2D) mismatch destroying spatial attention maps. ImageNet requires distinguishing between highly similar classes (e.g., 120 breeds of dogs); the 6-bit ADC cliff you identified for CIFAR/Flowers would likely shift to 8-bit for foundation models on ImageNet-scale tasks, as the noise tolerance tightens. Your paper acknowledges that harder datasets require finer decision boundaries, but an explicit sentence in the discussion bounding the expectations for ImageNet-scale transfer would preemptively disarm reviewers.

### 3. Methodological Holes

You have done an excellent job of building a "firewall" around your methodology in the Limitations section.

**Gaussian vs. Correlated Noise:** You explicitly state that spatially correlated D2D and heavy-tailed distributions are not modeled. This is the correct way to handle it. Hardware reviewers know this is a gap, but admitting it upfront turns a fatal flaw into a "future work" constraint.

**CrossSim Comparison:** Disclosing the 1-run clean / 3-run noise setup on a 1,000-image subset is critical. You frame this as a "throughput-constrained methodological anchor," which is exactly the right tone. It proves you aren't operating in a vacuum without claiming you out-benchmarked a mature simulator.

**Energy Estimates:** The manuscript consistently refers to these as "analytical placeholders" and "upper bounds." The marketing does not creep back in.

### 4. Severe-NL Supplementary Ablation

The framing in the supplementary material is highly transparent. You explicitly note that linearizing only the MLP layers recovers accuracy to 86.22% (final), while QKV and attention projection collapse to ~10%. Furthermore, you clearly state that "the dual attention-side failure limits the generality of any single-path mitigation claim."

**Verdict:** This reads as exactly what it is: a rigorous, highly structured bottleneck diagnostic. Reviewers will not think you are smuggling in a 5th contribution; they will appreciate the depth of the failure-mode analysis.

### 5. Rebuttal Risk (Top 3 Objections)

1. **Compute Overhead of Ensemble HAT:** Objection: Resampling D2D masks per epoch is computationally brutal for large models. How does this scale? Risk: High. ML reviewers care deeply about training costs. Disarm: Emphasize that Ensemble HAT is a one-time offline training cost amortized across thousands of edge deployments.
2. **ADC Power Negating Energy Claims:** Objection: You identified a 6-bit ADC knee. Real 6-bit ADCs have significant power and area overheads that might consume the 11x energy reduction gained from the analog MACs. Risk: Medium. Disarm: Point back to your explicit caveat that the energy numbers are analytical placeholders, not routed-circuit predictions.
3. **Lack of Physical Validation:** Objection: This is a purely behavioral simulation with proxies drawn from ReRAM for IR drops. Risk: Low to Medium (for NC). Disarm: Rely on your literature-anchored OPECT case study and reiterate that this is a system-level design aid, not a chip emulator.

### 6. Figures (Mixing Error Bars)

Your captions cleanly disclose that missing error bars indicate deterministic baselines or single-run estimates. However, mixing them visually in Figure 1 and 2 is a slight risk for a top-tier journal.

**Recommendation:** Visual differentiation is safer than relying on the caption. Use hatched/patterned bars for the single-run ConvNeXt estimates and solid bars for the Monte Carlo Tiny-ViT runs. This instantly communicates the methodological difference to a skimming reviewer.

### 7. Structure

The Nature Communications narrative-first structure (Abstract → Intro → Related Work → Results → Discussion → Methodology) serves this paper perfectly. By keeping the dense mathematical mapping of straight-through estimators and inverse-gamma derivations in the later sections, you allow the applied physics audience to digest the system-level impact (the "what") before getting bogged down in the inference infrastructure (the "how").

### 8. One-Liner Verdict

**Gut Call:** Accept with Minor Revision.
**Load-Bearing Reason:** The manuscript combines an unapologetically honest bounding of its own simulation limitations (e.g., ideal digital rescaling, lack of spatial correlation) with a highly practical, statistically rigorous algorithmic solution (Ensemble HAT) that directly addresses a critical failure mode in CIM deployment.

---

## Reviewer C — Detailed Single-Pass Critical Read

### 1. Central Claim Stress Test

The headline claim — "Ensemble HAT raises fresh-instance accuracy from 10.00% to 86.37±1.54%" — is defensibly scoped, but requires one important clarification before submission.

The 10.00% baseline is correctly identified as a collapsed predictor, not mere chance performance. The Welch t-test reporting (p < 10⁻¹⁵, n = 10 fresh arrays per arm) in Figure 4 is solid, and the per-arm standard deviation is disclosed (10.00±0.00% vs. 86.37±1.54%). The ±0.00% on the collapsed arm is itself a diagnostic signal — it shows every single fresh array collapses, not a distribution that happens to average near chance — and the paper implicitly relies on this interpretation without stating it explicitly.

**What would not survive a "show me raw per-instance outputs" challenge:** The paper reports that 10 fresh instances were used for Ensemble HAT evaluation, with 5 Monte Carlo runs per instance. The aggregate statistic (86.37±1.54%) is therefore a mean-of-means over a two-level hierarchy. The manuscript does not make this hierarchy explicit in the main text. A reviewer who asks for raw per-instance numbers will find the aggregate statistic is the mean of 10 per-instance means, not the mean of 50 independent evaluations — a subtlety that could draw a revision request.

**Pre-submit fix recommended:** add one sentence in the Methods (Section 5.2, around Eq. 4) that makes the two-level MC structure explicit, e.g., "each fresh-instance mean is itself the mean of 5 forward-pass MC evaluations; the reported ±1.54% is the standard deviation across the 10 per-instance means."

### 2. Generality vs. Over-Reach

The scoping to CIFAR-10/100 and Flowers-102 is honest but underdefended; the manuscript should preemptively name what an ImageNet-scale experiment would test differently.

**The most predictable ImageNet-scale failure modes, in order of severity:**

1. Attention head specialization at scale. Tiny-ViT-5M is fine-tuned from an ImageNet checkpoint. On CIFAR-10, its attention heads are already specialized; re-training under analog noise starts from a useful feature representation. At ImageNet scale with fresh random initialization, the optimization landscape under structured D2D mismatch would be far more rugged. The Ensemble HAT guarantee (convergence to a mismatch-distribution-aware checkpoint) has not been demonstrated in that regime.
2. Scale of the D2D mismatch map. On CIFAR-10 with 32×32 inputs and a 5M-parameter model, the total weight volume is small enough that 10% D2D at 4-bit precision has bounded total perturbation energy. An ImageNet-scale ViT (e.g., ViT-B/16, ~86M parameters) with the same σ_D2D would have roughly 17× more mismatch entries, and their cumulative effect on deep MLP projections is not characterized in this framework.
3. ADC cliff scaling. The 6-bit ADC cliff finding is presented as a robust result, but it was established on Tiny-ViT-5M. Larger models with deeper MLP blocks and wider projections may exhibit a different cliff location. This is a plausible rebuttal target.

**Recommended fix:** Add two sentences to Section 4.5 (Limitations) explicitly naming the ImageNet generalization gap: "The 6-bit ADC cliff and Ensemble HAT transfer results are established on CIFAR-scale tasks with a 5M-parameter fine-tuned backbone. Extrapolation to ImageNet-scale deployment — larger model footprints, fresh random initialization, and higher-dimensional mismatch maps — requires separate validation not provided here."

### 3. Methodological Holes

**Three genuine holes, ordered by reviewer impact:**

**3a. Fixed Gaussian D2D — not disclosed prominently enough**
The spatial mismatch model is i.i.d. Gaussian, which is explicitly called out in Limitations as an assumption ("Spatially correlated D2D and heavy-tailed conductance distributions are also absent"). However, this disclosure is buried in Section 4.5, not in the Methodology section where the model is defined. The consequence is real: structured spatial correlations (e.g., gradient-like IR-drop-induced trends across a crossbar tile) can break the "each fresh instance is i.i.d." assumption that underlies Ensemble HAT's theoretical motivation. If the true mismatch distribution has spatial correlations, drawing i.i.d. Gaussian M ~ N(0, σ²_D2D) per epoch does not approximate the deployment distribution.

**Risk rating:** Medium-high for major revision if reviewers have crossbar hardware experience. **Disarming experiment:** A single run with a spatially-correlated mismatch model (e.g., 2D AR(1) with ρ = 0.3) compared against the i.i.d. Gaussian baseline on the same Ensemble HAT checkpoint would show whether the structured correlation degrades fresh-instance transfer. The paper already has the infrastructure for this; it would take ~1 day.

**3b. CrossSim comparison — the caveat is present but the conclusion still over-reaches**
The paper discloses: "single-run clean baseline, 3-run Monte Carlo under noise, 1,000-image CIFAR-10 test subset." The stated gap is 81.63±0.56% (ours) vs. 67.20±2.67% (CrossSim) at σ = 5%, a 14.43 pp difference. With n = 3 runs on a 1,000-image subset, the CrossSim ±2.67% std is computed over very few samples. The conclusion drawn — "highlighting the sensitivity of accuracy predictions to the noise-to-conductance mapping" — is legitimate, but the specific 14.43 pp gap cannot be trusted to ±0.5 pp. A reader could reasonably ask whether the gap would hold at n = 10 on the full 10,000-image test set. The caveat in Section 4.6 says "the subset protocol is disclosed explicitly because of CrossSim throughput constraints; see Supplementary Note SX.Y" — but SX.Y is a placeholder that does not appear to exist in the current supplementary. **This is a concrete error that must be fixed before submission.**

**Risk rating:** High for minor revision if a reviewer checks the cross-reference. **Disarming fix:** Write the one-paragraph SX.Y supplementary note, or promote the disclosure sentence to the main text with explicit n=1/n=3 statistics framing.

**3c. Energy estimates — hedging is mostly consistent, one slip**
The abstract says "first-order behavioral simulation framework" and Section 4.4 says "first-order upper bounds under placeholder constants." The Discussion correctly uses "approximately 11×" and "upper bound." The one place where marketing creep reappears is in the Conclusion: the energy figures (273.94 µJ, 11× gain) appear without the "placeholder" qualifier that appears elsewhere. This is a minor inconsistency but reviewers who read the Conclusion independently may flag it.

### 4. Severe-NL Supplementary Ablation Framing

The ablation is honest; the framing risk is real but manageable.

Table S16 shows:
- Baseline (NL=1.0): 87.95±0.27%
- NL=2.0 global: 27.72±0.82%
- MLP-only linearized: 87.79% (best), 86.22% (final)
- QKV-only linearized: 18.72% (collapse)
- Attn-proj-only: 18.86% (collapse)

The interpretation note is explicit: "These results are presented as a supplementary ablation rather than a main-text contribution because the dual attention-side failure limits the generality of any single-path mitigation claim." This framing is correct and appropriately self-limiting.

**The real risk is not in the supplement — it is in the fourth contribution listed in the Introduction.** The Introduction states Contribution 4 as: "it turns two frequently qualitative concerns... into bounded system-level evidence by... localizing the present NL = 2.0 surrogate failure primarily to the MLP path." A reviewer who then checks the supplement will find that the MLP-linearized model's fresh-instance transfer is not reported in Table S16 — only its CIFAR-10 in-distribution accuracy (87.79%) is shown. The supporting context you provided states this fresh-instance transfer is ~32%, much worse than Ensemble HAT's 86%. This gap is currently invisible in the main text and supplement.

**This is a scoping integrity problem.** If you claim "localizing the failure to the MLP path" as a contribution, a reviewer is entitled to ask: "does MLP linearization actually fix the deployment problem?" The answer (32% fresh-instance transfer) would say no. The framing survives only if "localizing the bottleneck" is explicitly distinguished from "solving the deployment problem."

**Pre-submit fix required:** Add one sentence to Table S16's interpretation note: "Note that the MLP-linearized model achieves [X]% fresh-instance transfer accuracy under the same 10-array evaluation protocol used for Ensemble HAT, compared to 86.37±1.54% for Ensemble HAT, confirming that the MLP linearization functions as a training-diagnostic ablation rather than a deployment-grade mitigation."

### 5. Rebuttal Risk Assessment

**Objection R1:** "Gaussian i.i.d. D2D mismatch is not physically realistic for organic crossbars"
- (a) Major revision probability: 60% — If the reviewer has crossbar fabrication experience, this is a first-round objection that requires a substantive response.
- (b) Fastest disarm: Run one spatially-correlated mismatch experiment (2D AR process) and report it in one supplementary table. Even a negative result ("structured correlation changes absolute accuracy by X pp but does not change the Ensemble HAT vs. standard HAT ranking") is sufficient to disarm the objection.

**Objection R2:** "The CrossSim comparison is underpowered and references a non-existent supplementary note"
- (a) Major revision probability: 40% — A missing cross-reference is a concrete error, but the paper does not need the CrossSim comparison to support its core claims.
- (b) Fastest disarm: Fix the SX.Y cross-reference before submission. If throughput allows, run n=5 CrossSim evaluations on the 1,000-image subset and update the ±std.

**Objection R3:** "CIFAR-10 results do not justify the scope of the title and abstract for 'edge vision' applications"
- (a) Major revision probability: 55% — Nature Communications expects broad significance. "Edge vision" in the title implies real-world applicability. CIFAR-10 is a toy benchmark for 2026 standards.
- (b) Fastest disarm: This cannot be resolved with new experiments before submission. The defense is framing: the paper is explicitly a simulation framework paper, not a deployed-system paper. The Conclusion's phrasing "simulation-based materials-to-system decision aid" is the right defense.

### 6. Figure Mixed Error Bars (Figure 1)

The disclosure is necessary but not sufficient; the figure needs one visual fix.

Figure 1 (cross-dataset accuracy, formerly Figure 4 in the prompt) mixes deterministic baselines (no error bars) with Monte Carlo-derived error bars (HAT, ±1 std). The caption states: "Error bars denote ±1 standard deviation where Monte Carlo statistics are available; bars without visible error bars indicate deterministic baselines or currently available point estimates."

The disclosure is honest. However, visually, a bar chart where some bars have error bars and some do not creates a perceptual asymmetry — a reader's eye interprets a missing error bar as "zero variance" rather than "unknown variance." This is a well-known data visualization problem that NC reviewers and editors frequently cite.

**Recommended fix:** Use a visual marker (e.g., a diagonal hatch pattern on ConvNeXt bars, or a footnote symbol) to distinguish "point estimate, variance unknown" from "MC-derived mean ± std." This does not require splitting the figure. Alternatively, add a dashed outline to the single-run bars.

### 7. Structure Assessment

The narrative-first order works for NC; one section is misplaced.

The order (Abstract → Introduction → Related Work → Results → Discussion → Methodology → Conclusion) is consistent with NC's preferred format for methods papers that position methodology after results. This is not a problem in principle.

However, Section 3 (Results) refers to equations defined in Section 5 (Methodology) — specifically, Eq. 1 (the scale-recovery formula), Eq. 3 (the Ensemble HAT objective), and Eq. 8 (the Sobol index) are first cited in Results but only defined 6–8 pages later. This is a real readability problem. A reader following Section 3.2 encounters "the recovered-weight law later formalized in Eq. 1", which is an awkward forward reference to an equation in a section they have not yet read. NC allows Methods-after-Results, but forward-referencing equations from Results to Methods is unusual and may trigger copyeditor queries.

**Recommended fix:** Either move the key equations (Eqs. 1, 3, 8) to a short "Model" subsection between Related Work and Results, or convert the forward references to prose descriptions in Results that are then formalized in Methods.

### 8. One-Liner Verdict

**(b) Minor revision needed.** Not major revision, not rejection.

**The single most load-bearing reason for this call:** The missing or placeholder supplementary cross-reference (SX.Y in Section 4.6) and the undisclosed two-level MC hierarchy in the headline Ensemble HAT statistic are both concrete errors that a diligent reviewer will find on first pass. Neither is a scientific problem — the underlying data and analysis are solid — but both signal that the manuscript has not been fully proofread for internal consistency at submission quality. At NC, these small but visible inconsistencies shift a borderline "accept with minor revision" toward "major revision" simply because they raise the reviewer's prior that other details may also be inconsistently handled. Fix these two items and the manuscript is ready to submit.

The science is real. The Ensemble HAT result is genuine and well-supported. The Sobol decomposition is the clearest quantitative contribution in the paper and is correctly presented. The framework's honest self-description as "first-order behavioral" rather than "chip-predictive" is a sign of scientific maturity. If the five pre-submit items below are addressed, this paper will receive minor revision or direct acceptance from a hardware-ML reviewer at NC.

**Pre-Submit Fix Checklist (Priority Order):**

| # | Item | Section | Fix Type |
|---|------|---------|----------|
| P1 | Write or remove Supplementary Note SX.Y (CrossSim subset disclosure) | §4.6 | Concrete error |
| P2 | Disclose two-level MC hierarchy for Ensemble HAT headline statistic | §5.2, Eq. 4 | Statistical transparency |
| P3 | Add fresh-instance transfer accuracy for MLP-linearized model to Table S16 | Supp §Table S16 | Scoping integrity |
| P4 | Add spatial correlation caveat for D2D model to §5.2, not only §4.5 | §5.2 | Preemptive rebuttal |
| P5 | Add visual disambiguation for single-run vs. MC bars in Figure 1 | Figure 1 | Reviewer perception |

---

## Reviewer D — Concise Assessment (Accept with Minor Revision)

**Gut Call:** Accept with Minor Revision.

**Load-Bearing Reason:** The manuscript combines an unapologetically honest bounding of its own simulation limitations (e.g., ideal digital rescaling, lack of spatial correlation) with a highly practical, statistically rigorous algorithmic solution (Ensemble HAT) that directly addresses a critical failure mode in CIM deployment.

**Key Points:**
- 10.00% baseline: Honest framing as collapsed predictor
- Scoping: CIFAR-10/100 + Flowers-102 appropriate for edge vision
- Gaussian D2D: Acknowledged as limitation, correct handling
- CrossSim: 1,000-image subset disclosure sufficient
- Energy: Consistent hedging, no marketing creep
- NL ablation: Transparent diagnostic framing
- Top rebuttal risks: Compute overhead of Ensemble HAT, ADC power negating energy claims, lack of physical validation
- Figures: Need visual differentiation for deterministic vs. stochastic bars
- Structure: Narrative-first works well for NC

---

## Reviewer E — Concise Assessment (Major Revision, Achievable)

**Gut Call:** (b) Major revision needed — but achievable in one round.

**Load-Bearing Reason:** The paper's central contribution (Ensemble HAT) rests on a D2D model that is i.i.d. Gaussian, but the paper's own §4.5 acknowledges that real organic arrays will have spatially correlated mismatch. Without even a single ablation showing how Ensemble HAT degrades when the training noise model is mismatched to the evaluation noise model (e.g., i.i.d. training, correlated evaluation), the fresh-instance claim is conditional on an assumption the paper explicitly flags as incorrect. A reviewer who reads carefully will not let this pass. This is the one experiment worth running before submission.

**Priority Actions Before Submission:**
1. Run a correlated D2D ablation (even a 2D Gaussian kernel with correlation length ~5 devices) to bound the fresh-instance transfer gap. Add as one supplementary table.
2. Check and disclose what the standard-HAT collapse looks like per instance (single-class mode vs. uniform) — resolves R3 above.
3. Add a "Fresh-instance transfer accuracy" column or footnote to Table S16 to prevent the MLP-linearization ablation from being misread as a solved mitigation.
4. Fix Figure 1 visual encoding for deterministic vs. stochastic bars (hatching or separate panels).
5. Add forward references "defined in §5.X" at every pre-definition equation citation in §3.
6. In §4.6, soften the CrossSim noise-divergence conclusion from a stated 14.43 pp gap to "suggestive at n=3, requires full-test comparison."

---

## Final Synthesis — Coordinator's Consolidated Assessment

### Overall Trajectory

The manuscript has evolved from an "NC risk draft" to a "competitive NC major-revision draft." The most significant improvements are:

1. **Contribution crystallization:** Four bounded contributions with clear scope
2. **ADC evidence chain:** Complete Sobol decomposition + contour + hook-based checks
3. **Ensemble HAT maturity:** Cadence ablation + i.i.d. noise distinction
4. **NL ablation honesty:** Explicitly framed as diagnostic, not mitigation
5. **Community alignment:** AIHWKIT consistency check + CrossSim preliminary comparison

### Current State

| Dimension | Status |
|-----------|--------|
| Novelty | ✅ Clear methodological advance (profile-driven workflow + hardware-instance overfitting discovery) |
| Impact | ✅ Addresses real deployment gap in organic CIM |
| Statistical rigor | ✅ Excellent (locked numbers, seed reporting, Welch tests) |
| Scope fit | 🟡 Borderline — CIFAR-only may trigger "toy benchmark" objections |
| Physical realism | 🟡 Gaussian i.i.d. D2D is the biggest vulnerability |
| External validation | 🟡 AIHWKIT check helps; CrossSim still thin |
| Framing | 🟡 Title/abstract slightly over-rotate toward deployment |
| Internal consistency | 🔴 SX.Y missing, two-level MC undisclosed, MLP fresh-instance gap invisible |

### Recommended Path Forward

**Submit to Nature Communications** with the following pre-submit fixes:

**🔴 Must-fix (blockers):**
1. Fix or remove SX.Y cross-reference
2. Disclose two-level MC hierarchy in Methods
3. Add MLP fresh-instance transfer to Table S16 caption

**🟡 Should-fix (strongly recommended):**
4. Run one spatially-correlated D2D ablation (~1 day)
5. Add ImageNet failure mode prediction to Limitations
6. Visual differentiation for deterministic vs. stochastic bars
7. Add forward pointers for pre-definition equation citations
8. Soften CrossSim 14.43 pp gap claim

**🟢 Nice-to-have:**
9. Consider title adjustment to emphasize "simulation framework"
10. Add per-batch HAT baseline to main text to preempt "straw man" accusations

### Bottom Line

**The paper is ready to submit after the 3 must-fix items are resolved.** The remaining should-fix items can be addressed during revision if reviewers raise them, but the 3 blockers are low-effort/high-impact fixes that prevent immediate credibility damage on first pass.

The core science is solid. The Ensemble HAT finding is genuine. The framework fills a real methodological gap. With proper framing, this is a competitive Nature Communications submission.

---

## Codex Addendum — 2026-04-19 Late-Cycle Triage

This addendum records the post-compilation state after the reviewer-facing low-risk fixes and the fresh-instance control reruns were actually executed on disk.

### What is now closed

1. **B-1 is not a live blocker.**
   - The missing `SX.Y` complaint came from a stale snapshot.
   - The live supplementary source now contains a canonical `Supplementary Note~SX.Y`, and the earlier duplicate text has been collapsed into a forward pointer.

2. **B-2 and B-3 are now fixed in source.**
   - The two-level Monte Carlo hierarchy for the `86.37 ± 1.54%` Ensemble HAT statistic is now disclosed explicitly in the methodology.
   - The severe-NL supplementary interpretation now states that `MLP-only` linearization reaches only `32.12 ± 7.72%` fresh-instance transfer, versus `86.37 ± 1.54%` for canonical Ensemble HAT, so it must be read as a diagnostic ablation rather than a deployment-grade mitigation.

3. **The standard-HAT 10.00% fresh-instance collapse survived the no-AMP integrity check.**
   - The no-AMP rerun produced `10.00 ± 0.00%` across `10` fresh instances, with `5` Monte Carlo evaluations per instance.
   - This means the collapsed-predictor story is real; it is not an AMP artifact.

### New scientific constraint learned after the external reviews

The final missing severe-NL lane that was still "pending" in several earlier broadcasts is now known:

- `all-linear` fresh-instance transfer is only `32.60 ± 9.18%`
- This is close to the already-known `MLP-only` fresh-instance result (`32.12 ± 7.72%`)
- Therefore, the severe-NL lane remains a **source-domain rescue / localization tool**, not a deployment-transfer solution

This strengthens the existing manuscript decision to keep the severe-NL mitigation story in the **supplementary** rather than promote it to a new main-text contribution.

### Updated recommendation hierarchy

If only one non-text experiment is still worth spending GPU on before submission, it remains Reviewer E's point:

1. **Run one spatially correlated D2D ablation**
   - canonical Ensemble HAT checkpoint
   - same `10 fresh instances × 5 MC` protocol
   - i.i.d. Gaussian baseline vs. correlated D2D evaluation
   - goal is not to preserve the exact absolute number, but to show that the ordering `Ensemble HAT >> standard HAT collapse` survives moderate spatial structure

2. **Do not spend more submission time on new severe-NL mitigation variants**
   - the fresh-instance evidence now shows that even broader linearization does not recover deployment-grade transfer
   - this line is scientifically useful for thesis discussion and reviewer response, but no longer the highest-value path for the submission package

### Bottom line after the late-cycle reruns

At this point the reviewer-facing remaining risk is no longer "hidden numerical inconsistency."
It is primarily:

- whether a correlated-D2D stress test preserves the manuscript's ranking claims, and
- whether the submission package cleanly reflects the already-landed clarifications.

That is a materially stronger state than the one reflected in the earlier external-review snapshots.

---

## Codex Addendum II — 2026-04-19 Round-K Text Closure

This second addendum records the state after the Round-K fold-in tasks were executed directly in the live manuscript and response package rather than left as external recommendations.

### What changed after the first addendum

1. **The major reviewer-facing numerical clarifications are now folded into the response package.**
   - `RESPONSE_LETTER_FINAL_20260419.md` now explicitly states that:
     - the standard-HAT fresh-instance collapse remains exactly `10.00 ± 0.00%` under FP32 / no-AMP inference,
     - the severe-NL `all-linear` upper-bound control reaches only `32.60 ± 9.18%` under fresh-instance transfer,
     - the preliminary correlated-D2D probe yields `86.78%` at `rho = 0.3` versus `87.45%` under the matched i.i.d. baseline (`Δ = 0.67 pp`) while the full `10 × 5` sweep is still running.

2. **The residual Round-J text items are now closed at the source level.**
   - A dedicated audit confirms that the abstract framing hedge, the softened CrossSim claim, the ImageNet boundary statement, the formal forward pointer in the results section, and the exploratory per-batch cadence caveat are all present in the live source:
     - `KIMI_ROUND_J_RESIDUAL_AUDIT_20260419.md`

3. **The locked-number consistency sweep is now in acceptable shape.**
   - The second-pass sweep confirms:
     - `86.37` remains paired with `±1.54`,
     - `14.43 pp` remains confined to the softened preliminary CrossSim statement,
     - `32.12` and `32.60` remain explicitly diagnostic rather than deployment-grade,
     - the `10.00%` fresh-instance collapse is now anchored in both the main results section and the supplementary no-AMP note.
   - See:
     - `KIMI_CONSISTENCY_SWEEP_V2_20260419.md`

### Updated triage

The earlier external review synthesis said the paper was ready after three must-fix items. That statement is now outdated: those must-fix items have been resolved in source, and the main remaining experimental gate is the full correlated-D2D harvest.

If a reviewer were to attack the manuscript now, the strongest remaining live target would be:

1. **Whether the full correlated-D2D stress test preserves the ranking claim under the full `10 fresh instances × 5 MC` protocol**

It is no longer:

- missing SX.Y references,
- missing MC disclosure,
- unqualified severe-NL mitigation breadth,
- or ambiguity about whether the `10.00%` collapse is numerical.

### Bottom line after Round-K text closure

The submission is now in a state where the remaining uncertainty is concentrated in one still-running robustness check rather than spread across multiple text-level credibility gaps. That is the right late-cycle risk profile for submission: one bounded empirical tail item, rather than several unresolved presentation defects.
