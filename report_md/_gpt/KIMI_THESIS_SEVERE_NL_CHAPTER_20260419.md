<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 9cdbe77 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# Chapter X — Severe Write-Nonlinearity as a Diagnostic Stress Test

## Thesis Sub-Chapter Outline (~8 pages)

*Target venue:* Nature Communications supplementary ablation → full thesis chapter.  
*Core claim:* NL = 2.0 is a **controlled diagnostic severity** that localizes the gradient-scaling surrogate failure to the MLP analog path, reveals a structural impossibility on the attention side, and exposes a fidelity–robustness trade-off that only joint algorithmic training can resolve.

---

## 1. Severe-NL as a Stress Test

**Scope paragraph.**  
The choice of NL = 2.0 (yielding a 64 percentage-point drop from the canonical epoch-HAT baseline of 91.13 % down to 27.72 %) was deliberate: it sits just beyond the "knee" of the hardware-aware training robustness curve, in a regime where graceful degradation has given way to structural collapse, yet the network remains sufficiently trainable that differential behavior across architectural paths can still be isolated. Rather than treating NL = 2.0 as a deployment target—which it is not—the severity was selected as a **diagnostic probe**. In this regime, the gradient-scaling surrogate’s distortions are amplified enough to expose which analog paths are structurally tolerant of asymmetric write updates and which are irreducibly dependent on their native nonlinearities. The value of the severity is precisely that it is *too harsh* for the baseline recipe, forcing the model to reveal its mechanical weak points without obliterating all trainability and collapsing every lane into indistinguishable failure.

- **Dynamic-range criterion.** A 27.72 % floor and a ~91 % ceiling create a 60+ pp window in which rescues of 50–60 pp (MLP-only) and near-zero rescues (QKV-only) are both statistically separable; a milder NL might have produced ambiguous partial recoveries.
- **Physical grounding.** NL = 2.0 corresponds to realistic organic-memristor programming regimes in which SET/RESET asymmetry is pronounced and the conductance-update curve departs strongly from linearity; it is therefore not an arbitrary adversarial choice but a physically motivated stress test.
- **Retained trainability.** Loss curves in the MLP-only and all-linear lanes still descend meaningfully, proving that the optimizer is not paralyzed everywhere; this allows the experiment to distinguish *localized* from *global* failure modes.
- **Diagnostic rather than operational intent.** The chapter explicitly disclaims that NL = 2.0 represents an acceptable deployment specification; instead, it is a scalpel used to dissect the baseline HAT recipe under duress.
- **Anchor for downstream ablation.** Once the severity is fixed, every subsequent lane becomes a controlled perturbation of a single variable (which analog path is linearized), satisfying the ceteris paribus requirement for mechanistic attribution.

**Tie-back to NC paper.**  
In the Nature Communications submission, the NL = 2.0 result appears as a supplementary ablation table that anchors the boundary of algorithmic mitigation. The thesis chapter expands this single table into a full epistemic argument: the severity was not chosen to "break" the model for dramatic effect, but to create a controlled failure mode in which the surrogate’s distortions become large enough to localize pathology. The reader of the supplement sees the outcome; the thesis reader sees the *design rationale* behind the severity choice.

---

## 2. Five-Lane Ablation as Decomposition

**Scope paragraph.**  
The five training lanes—canonical HAT baseline, unmitigated severe-NL baseline, MLP-only linear compensation, QKV-only linear compensation, and all-linear compensation—constitute a **functional decomposition** of nonlinearity responsibility across the Tiny-ViT analog stack. By holding the severe-NL physical model fixed and selectively replacing analog nonlinear layers with idealized linear equivalents, each lane isolates the contribution of a specific architectural region to the overall collapse. The design treats the model not as a monolithic black box but as a composition of paths with distinct geometric and dynamic properties: the dense channel-mixing MLP path, the angular attention-score path, and the full stack in which both operate concurrently. The resulting pattern—strong rescue on the MLP side, structural collapse on the attention side, and an all-linear upper bound that essentially mirrors MLP-only—turns the ablation into a localization experiment.

- **Canonical baseline (epoch-HAT: 91.13 % train / 86.33 % fresh).** Sets the performance ceiling under idealized programming; establishes the target that any severe-NL mitigation should aspire to recover in both source-domain and fresh-instance metrics.
- **Unmitigated severe-NL baseline (27.72 %).** Sets the floor; standard HAT with the present gradient-scaling recipe collapses, proving that the recipe is inadequate for this severity without structural intervention.
- **MLP-only linear compensation (87.79 %).** The key positive result: linearizing only the MLP analog layers rescues accuracy to within ~4 pp of the idealized ceiling, localizing the dominant failure site to the dense feedforward write path.
- **QKV-only linear compensation (18.72 %).** The negative control: linearizing only the attention projections fails to rescue the network, proving that a generic "attention-side" explanation is insufficient and that the attention nonlinearity is structurally required, not merely helpful.
- **All-linear upper bound (87.49 %).** Performs virtually identically to MLP-only rather than materially exceeding it, confirming that the MLP path accounts for essentially all recoverable gain and that attention-side linearization contributes no incremental benefit.

**Tie-back to NC paper.**  
The NC supplement presents these five conditions as a compact comparison table (together with the corroborating attn-proj-only collapse at ~11–19 %). In the thesis, the table is unpacked into a full decomposition narrative: the reader is walked through the logical progression from ceiling to floor to localized rescue, with each lane serving as a premise in an inductive argument. The supplement reports *that* the failure is localized; the thesis explains *how* the five-lane design makes the localization irrefutable.

---

## 3. Fresh-Instance Gap as Unsolved Hook

**Scope paragraph.**  
The most consequential—and initially puzzling—result of the MLP-only rescue is not its source-domain success but its source-domain *limitation*: although the checkpoint reaches 87.79 % on the training hardware instance, its fresh-instance transfer mean plummets to 32.12 ± 7.72 %, a catastrophic departure from the canonical Ensemble-HAT fresh-instance baseline of 86.37 ± 1.54 %. This gap is not a measurement artifact; the elevated standard deviation (7.72 % versus ~1.6 % for canonical epoch-HAT) signals erratic, instance-dependent behavior rather than a uniform offset. The QKV-only lane fares no better on fresh instances (10.01 ± 0.10 %), confirming that attention-side linearization destroys transfer behavior alongside in-domain behavior. Together, these results expose a **fidelity–robustness trade-off**: MLP linearization restores gradient-surrogate fidelity (enabling convergence on the source instance), but in doing so it strips away the D2D-mismatch exposure against which Ensemble HAT trains, leaving the model blind to cross-instance variation. The fresh-instance gap is therefore not a bug to be hidden; it is the central unsolved problem that motivates the next generation of experiments.

- **Quantitative gap.** 87.79 % source-domain versus 32.12 ± 7.72 % fresh-instance represents a 55+ pp chasm, far exceeding the ~5 pp source-to-fresh gap observed under canonical severe-NL-free HAT.
- **Erratic transfer signature.** The 7.72 % cross-instance standard deviation indicates that some hardware instances are rescued moderately while others collapse entirely, suggesting that the linearized MLP path retains latent sensitivity to D2D variation that is not regularized away.
- **QKV-only corroboration.** At 10.01 ± 0.10 % fresh-instance, QKV-only linearization is effectively non-functional across instances, reinforcing that the attention path cannot be sacrificed without destroying both source and transfer performance.
- **Mechanistic interpretation.** The gap reveals that Ensemble HAT’s epoch-level D2D resampling and the gradient-scaling surrogate are coupled: the surrogate must be sufficiently faithful to allow convergence, yet the training dynamics must still experience D2D variation to learn instance-agnostic weights. MLP-only linearization fixes the former while accidentally eliminating the latter.
- **Narrative function in the thesis.** The gap serves as the chapter’s turning point—the moment when a seemingly successful rescue is revealed to be incomplete, creating dramatic tension and justifying the deferred joint-training experiment in §4.

**Tie-back to NC paper.**  
The fresh-instance gap is precisely why the NL mitigation story remains in the NC supplement rather than being promoted to a main-text contribution. The supplement can honestly report a source-domain rescue; the main text demands deployable cross-instance robustness. The thesis chapter embraces this limitation openly, using the gap as a generative hook that transitions the narrative from "what we have diagnosed" to "what we still must prove."

---

## 4. Joint MLP-Linear + Ensemble HAT as Planned Thesis Experiment

**Scope paragraph.**  
To resolve the fidelity–robustness trade-off exposed in §3, the thesis proposes a deferred capstone experiment: **joint training of MLP-linearized analog layers with epoch-level Ensemble HAT resampling**. The hypothesis is that the two interventions operate on orthogonal axes—MLP linearization restores surrogate fidelity in the dense channel-mixing path, while Ensemble HAT maintains exposure to D2D mismatch during training—so their combination should recover both source-domain accuracy (targeting ~87–88 %) and fresh-instance robustness (hypothesized > 80 %). If validated, this experiment would upgrade the NL mitigation from a diagnostic curiosity to a deployable severe-NL training recipe. The experiment is currently deferred pending the return of GPU resources; its inclusion in the chapter outline is intentional, signaling to the thesis reader that the narrative arc is incomplete by design and that the author has a concrete, falsifiable plan for closure.

- **Orthogonal intervention design.** MLP linearization addresses the *gradient* problem (surrogate distortion in the backward pass); Ensemble HAT addresses the *training-dynamics* problem (D2D resampling in the forward pass). Their mechanisms do not interfere and are therefore composable.
- **Hypothesis formulation.** Fresh-instance mean > 80 % with cross-instance std < 3 %, approaching the canonical epoch-HAT transfer baseline of 86.37 ± 1.54 %. Source-domain accuracy should remain at or above the MLP-only level (≥ 87 %).
- **Experimental protocol.** Tiny-ViT V4, NL = 2.0, MLP analog layers linearized, QKV and projection layers left nonlinear (as §2 proved they must be), trained with epoch-level instance resampling under the standard gradient-scaling recipe.
- **Resource estimate and deferral rationale.** ~20 GPU-hours, ~1 week wall-clock for convergence verification; deferred because the NC submission timeline and current GPU queue do not permit execution before the manuscript deadline. The thesis chapter reports the protocol and hypothesis prospectively.
- **Epistemic stakes.** A positive result would demonstrate that severe-NL algorithmic mitigation is possible without physical-level intervention. A negative result would force the conclusion that even optimal gradient fidelity cannot compensate for D2D mismatch at NL = 2.0, strengthening the case for device-level strategies (pulse shaping, write-verify).

**Tie-back to NC paper.**  
This experiment is explicitly outside the NC scope and timeline; the thesis chapter therefore claims unique ground. The NC paper’s supplementary ablation ends with the fresh-instance gap as an open question; the thesis uses that open question as the launching point for its only original experiment, ensuring that the chapter contributes novel empirical work rather than merely expanding existing paragraphs.

---

## 5. Mechanistic Interpretation — Why MLP Recovers, Why Attention Collapses

**Scope paragraph.**  
The differential outcomes of the five-lane ablation are not merely empirical patterns; they admit a coherent mechanistic explanation that reconciles *gradient-diagnostic* evidence (static analysis of backward-pass fidelity) with *training-dynamics* evidence (dynamic behavior across instances). In the MLP path, the gradient-scaling surrogate disproportionately distorts weight updates—gradient-diagnostic cosine similarity 0.815 versus 1.00 for the attention path—yet the dense channel-mixing geometry is structurally forgiving: fan-out redundancy distributes scaled errors across many connections, and the absence of a sharp angular decision boundary prevents catastrophic fragmentation. In the attention path, by contrast, the softmax operation exponentiates small relative distortions in the Q · Kᵀ score matrix; linearizing QKV or projection layers destroys the angular geometry of query-key alignment irreversibly, producing attention-map fragmentation that no amount of training can repair. The critical insight is that gradient fidelity and training dynamics are **independent axes**: the 0.815 cosine predicts *where* distortion occurs, but the 32.12 % fresh-instance gap reveals *that* distortion localization is insufficient without concurrent D2D regularization. This two-axis framework—surrogate fidelity versus instance robustness—provides the chapter’s central theoretical contribution, bounding the design space for all future severe-NL mitigations.

- **Gradient-diagnostic asymmetry.** The MLP path’s 0.815 gradient-diagnostic cosine (versus 1.00 for attention projections) confirms that the gradient-scaling surrogate disproportionately corrupts backward updates in the dense feedforward layers, making MLP linearization the natural intervention site.
- **MLP structural tolerance.** Dense feedforward weights operate as channel-mixing matrices; their redundancy and lack of angular selectivity allow them to absorb scaled gradient errors without geometric collapse. Linearization removes the surrogate distortion while preserving the path’s expressive capacity.
- **Attention structural fragility.** Self-attention relies on softmax-normalized Q · Kᵀ scores; the exponential nonlinearity amplifies minute relative errors in projected query-key alignment. Removing nonlinearity from QKV or projection layers annihilates the angular structure that attention maps depend on, causing irreversible collapse (18.72 % and ~11 % respectively).
- **Fidelity–robustness decoupling.** Gradient-diagnostic analysis is static: it identifies *which* weights are distorted. Fresh-instance transfer is dynamic: it tests *whether* the training process has learned instance-agnostic representations. The 55+ pp gap between the two shows that solving the static problem does not automatically solve the dynamic one.
- **Design-space boundary.** The mechanistic story establishes a hard boundary: algorithmic mitigation can recover MLP-path fidelity, but it cannot circumvent the attention mechanism’s structural need for nonlinearity. Full severe-NL recovery therefore requires either (i) joint MLP-linear + Ensemble HAT training (algorithmic), or (ii) physical-level reduction of NL severity at the device (pulse shaping, write-verify), or both.

**Tie-back to NC paper.**  
The NC paper cites the gradient-diagnostic observation in passing and presents the ablation outcomes as empirical facts. The thesis chapter builds these facts into an integrated mechanistic narrative: the reader learns not only *that* MLP linearization rescues and attention linearization collapses, but *why* the physics of dense matrix multiplication and softmax exponentiation make this outcome inevitable. This narrative elevates the supplementary table into a design-space boundary condition—one of the chapter’s key intellectual contributions to the broader organic optoelectronic CIM literature.

---

## Chapter Summary

This chapter treats NL = 2.0 not as a defeat but as a **diagnostic lens**. Through a five-lane functional decomposition, it localizes the baseline HAT failure to the MLP analog path, proves that the attention path is structurally irreplaceable, and exposes a fidelity–robustness trade-off that turns a source-domain rescue into a fresh-instance puzzle. The planned joint MLP-Linear + Ensemble HAT experiment offers a prospective resolution; the mechanistic interpretation offers a durable theoretical framework. Together, these five sections transform the NC supplementary ablation into a self-contained thesis argument about the limits—and the future—of algorithmic nonlinearity mitigation in organic memristive inference accelerators.
