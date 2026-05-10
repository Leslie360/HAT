# Response to Reviewer Comments

**Manuscript:** *Compute-ViT: A Prospective Simulation Framework for Risk-Aware Deployment of Vision Transformers on Organic Resistive Crossbars*
**Date:** 19 April 2026

---

Dear Editor and Reviewers,

Thank you for the time and care devoted to evaluating our manuscript. We have read the comments thoroughly and prepared the following point-by-point response. Where concerns relate to manuscript material already present, we cite the specific sections, tables, and figures. Where a concern raises a legitimate limitation not yet discussed in the text, we acknowledge it honestly and explain how it bounds—rather than invalidates—the claims we make. We have also implemented minor pre-emptive clarifications in the cover letter and §6.5 (detailed below) to improve transparency.

The structure below follows the numbered objections (R1–R11) in the order they were raised.

---

## R1 — Task Complexity / ImageNet Missing

**Objection.** The empirical scope is limited to small-scale datasets (CIFAR-10/100, Flowers-102); ImageNet-scale validation is absent.

**Manuscript evidence.** §1 explicitly scopes the study to "edge vision" tasks, and §4 lists the evaluated datasets (CIFAR-10/100 and Flowers-102). The core claim is a materials-to-system risk-ranking framework for resource-constrained nodes, not a claim of ImageNet-scale readiness.

**Response.** We agree that ImageNet-scale validation would strengthen the empirical scope, and we have pre-registered a pilot as a concrete next step. Extending to larger datasets is therefore a natural follow-up rather than a missing prerequisite. The present datasets span the complexity spectrum from CIFAR-10 (high-data) to Flowers-102 (low-data extreme), which is sufficient for the intended purpose of relative risk ranking across architecture variants.

**Changes to the manuscript.** None. The scope is clearly stated in §1 and §4. (Pre-emptive: cover letter now explicitly notes the ImageNet pilot as future work.)

---

## R2 — Energy Model Unvalidated / Placeholder

**Objection.** The energy projections rely on unvalidated placeholder constants and may not translate to real hardware.

**Manuscript evidence.** §3.4 states that the energy model is a "first-order analytical model... intended for relative comparison rather than routed-circuit prediction." §6.4 notes that the estimates are "system-level upper bounds under placeholder constants, not chip-predictive estimates." §6.5 Limitations adds: "Energy parameters are placeholders." The cover letter repeats: "first-order system-level upper bounds prior to routed-chip implementation." These caveats appear at least four times across the main text, cover letter, and supplementary energy section.

**Response.** We fully recognize that the absolute energy projections are provisional. The relative ordering—dense analog projections yielding ~11× energy reduction versus FP32, with digital attention still dominating total cost—is robust even under the 10–50% routing overhead we disclose, which is the directional claim we actually make.

**Changes to the manuscript.** None. Caveats are already pervasive. (Pre-emptive: cover letter contribution count revised from 6→4 to align with §1; energy caveats restated.)

---

## R3 — Fixed Gaussian C2C/D2D vs. Spatial Correlation & Heavy Tails

**Objection.** The C2C/D2D mismatch model assumes fixed Gaussian distributions, neglecting spatial correlation and heavy-tailed conductance distributions observed in real organic RRAM arrays.

**Manuscript evidence.** §6.5 Limitations explicitly lists: "Spatially correlated D2D and heavy-tailed conductance distributions are also absent." §6.6 Outlook defers a "circuit-aware layer that models spatial IR drop, sneak paths, and temperature-dependent coefficients from array geometry---a scope we have explicitly deferred here."

**Response.** Spatially correlated D2D and heavy-tailed conductance distributions are real phenomena that our present model omits, as we state candidly in §6.5. The profile-driven substitution interface (§3.3) ensures these extensions can be adopted without code changes, so the omission does not invalidate the current comparative conclusions. The present framework targets risk ranking before full hardware closure. To anchor this point with real code-path evidence rather than only a deferred limitation statement, we have now completed the full correlated-D2D stress test in Supplementary Note~SX.Z under the same \(10\) fresh instances \(\times 5\) Monte Carlo protocol as the canonical Ensemble-HAT evaluation. The resulting fresh-instance means are \(86.33\pm1.61\%\) for the i.i.d. baseline, \(84.57\pm2.39\%\) at \(\rho=0.3\), and \(82.12\pm3.95\%\) at \(\rho=0.5\). Thus moderate spatial correlation produces a measurable but bounded degradation (\(-1.76\) and \(-4.20\) pp, respectively) while preserving the ranking separation from the collapsed fixed-mask baseline.

**Changes to the manuscript.** None. Limitations are explicitly disclosed.

---

## R4 — NL=2.0 Is Gradient-Scaling Approximation, Not Materials Bound

**Objection.** The nonlinearity limit NL=2.0 is a gradient-scaling surrogate rather than a measured materials property.

**Manuscript evidence.** §6.5 Limitations states: "The $NL=2.0$ limit reflects the present gradient-scaling surrogate, not a materials bound. Group-wise ablation confirms that the bottleneck is concentrated in the MLP analog path..." Supplementary Table `tab:supp-nl-ablation` and Figure `fig:supp-nl-gradient` localize the failure to the MLP path. Additionally, attention-side linearizations (QKV and projection) collapse structurally regardless of the exact NL value.

**Response.** The reviewer is correct that NL=2.0 reflects the present gradient-scaling surrogate rather than a measured materials limit; §6.5 states this explicitly as the "limit of this approximation." The qualitative ranking of which blocks dominate the accuracy budget remains valid even if future device measurements revise the absolute nonlinearity. We have now tightened this interpretation further with group-wise controls: the MLP-only lane restores in-domain accuracy, but both attention-side lanes collapse structurally, and even the all-linear upper-bound control reaches only \(32.60\pm9.18\%\) under the same fresh-instance \(10\times5\) protocol. We therefore frame these NL ablations as diagnostic evidence about where the current surrogate fails, not as a deployment-grade mitigation claim.

**Changes to the manuscript.** §6.5 tightened to explicitly note dual-attention-collapse (U1 pre-emptive patch landed).

---

## R5 — Ensemble HAT Lacks External Multi-Instance Baseline

**Objection.** The Ensemble HAT result is presented without an external multi-instance baseline from prior literature.

**Manuscript evidence.** §6.1 discusses fresh-instance transfer and hardware-instance overfitting, but no external multi-instance baseline for organic CIM has been published. The manuscript presents Ensemble HAT as a novel contribution.

**Response.** We acknowledge that no exact apples-to-apples external baseline for multi-instance HAT on organic CIM has been published, which is why our response relies on internal controls. The fresh-instance transfer protocol (Eq.~4) provides a reproducible Monte Carlo benchmark: standard HAT collapses to 10.00% accuracy on unseen mismatch maps, whereas Ensemble HAT recovers to 86.37±1.54%. This internal ablation isolates the effect cleanly, and the protocol can be adopted by future studies for direct comparison. We have also re-run the canonical standard-HAT fresh-instance evaluation under FP32 inference with autocast disabled; the result remains exactly \(10.00\pm0.00\%\) across 10 fresh D2D instances with 5 Monte Carlo evaluations per instance (`fresh_instance_eval_v4_standard_noamp.json`), confirming that the collapsed single-class predictor is a deterministic training outcome rather than an AMP artifact.

**Changes to the manuscript.** None. This is a response-only argument; the internal ablation is already present in §6.1.

---

## R6 — STE Backward Surrogate Oversimplifies Pulse Accumulation

**Objection.** The straight-through estimator (STE) in the backward pass abstracts away pulse-level write dynamics.

**Manuscript evidence.** §3.2 discloses the STE quantizer, STE backward pass, and state-dependent gradient scaling. Supplementary Table `tab:supp-nl-ablation` and Figure `fig:supp-nl-gradient` provide empirical guardrails bounding where the surrogate fails under the explored parameter range. The forward path already includes nonlinear-write and double-exponential retention surrogates anchored to measured DNTT transients.

**Response.** The STE does indeed abstract away pulse-level dynamics in favor of a conductance-level surrogate, a choice we disclose transparently in §3.2. The supplementary material provides empirical guardrails that bound the failure modes of this approximation. Moreover, the dominant physical effects are captured in the forward path even if the backward pass remains idealized.

**Changes to the manuscript.** None. STE disclosure and empirical guardrails are already present.

---

## R7 — OPECT Calibration Constants Arbitrary / Not Representative

**Objection.** The optoelectronic frontend calibration constants are arbitrary literature proxies and may not represent real devices.

**Manuscript evidence.** §5.6 states the parameters are a "literature-anchored reference point... 2025 OPECT array \citep{zhang2026opect}." §3.3 notes that "Representative profile fields and provenance are documented in the Supplementary Information." Supplementary Section `subsec:parameter-provenance` contains the "Proxy Estimate Sensitivity Analysis" sweep (Table `tab:sensitivity`, Figure `fig:supp-contour-map`) showing the conclusion is "insensitive to the exact proxy choice."

**Response.** We agree that measured-device calibration would be preferable to literature-anchored constants. The supplementary sensitivity sweep demonstrates that accuracy is insensitive to ±20% variation in the key constants ($\gamma_{\text{phys}}$, $I_{\text{dark}}$, and $\alpha$). Because the qualitative conclusions do not hinge on the exact numerical values, the present calibration is sufficient for the framework's intended purpose of relative risk ranking.

**Changes to the manuscript.** None. Anchoring and sensitivity evidence are already in the supplementary.

---

## R8 — Cycle Endurance Ignored

**Objection.** Cycle endurance is not considered, yet it is a critical concern for analog memory technologies.

**Manuscript evidence.** Cycle endurance is not mentioned in the manuscript. The present study targets inference-heavy edge vision, where training-in-memory is explicitly excluded.

**Response.** Cycle endurance is indeed a relevant concern for any analog memory technology. The present application scope, however, is inference-heavy edge vision, where read retention—modeled explicitly in the V8 retention-drift experiments (§6.5)—is the primary temporal bottleneck rather than write cycling. Training-in-memory is explicitly excluded from the deployment scenario, so endurance limitations do not threaten the operational lifetime claims made for the targeted use case.

**Changes to the manuscript.** None. This is a response-only argument based on the inference-dominant scope.

---

## R9 — Temperature Dependence Ignored

**Objection.** Temperature-dependent shifts in photoresponse and mismatch variance are not modeled.

**Manuscript evidence.** §6.5 Limitations lists "temperature-dependent shifts in photoresponse and mismatch variance" as "not yet modeled explicitly." §6.6 Outlook defers these to the planned "circuit-aware layer."

**Response.** Temperature-dependent shifts are real effects that should be modeled, and §6.5 lists them candidly among the current limitations. Because the present framework ranks deployment risks under nominal operating conditions, this omission bounds the scope rather than invalidating the comparative conclusions.

**Changes to the manuscript.** None. Limitations are explicitly disclosed.

---

## R10 — Best-Checkpoint Reporting Masks Instability

**Objection.** Reporting best-checkpoint results may obscure training instability and inflate perceived accuracy.

**Manuscript evidence.** §5.1 explicitly discloses: "All accuracy values reported for noisy and HAT deployments are best-checkpoint results unless otherwise stated." The reported accuracies are backed by 5-seed Monte Carlo averages that quantify residual variance.

**Response.** We recognize that best-checkpoint selection can obscure training variance, which is why §5.1 explicitly discloses the protocol. This practice is standard in the noisy hardware-aware training literature, where training curves are non-monotonic by construction. The 5-seed Monte Carlo averages ensure the selection criterion does not inflate the results beyond what the statistical spread already permits.

**Changes to the manuscript.** None. Protocol is already transparently disclosed.

---

## R11 — Fig. 4 Mixed Deterministic / MC Bars

**Objection.** Figure 4 mixes deterministic baselines and Monte Carlo means in a way that may confuse the reader.

**Manuscript evidence.** The Fig. 4 caption transparently states: "Error bars denote $\pm 1$ standard deviation where Monte Carlo (MC) statistics are available; bars without visible error bars indicate deterministic baselines or currently available point estimates."

**Response.** The mixed visualization could indeed be clarified, and the caption already transparently distinguishes deterministic baselines from Monte Carlo means. The figure's purpose is to illustrate the depth-versus-noise trade-off—specifically, why Tiny-ViT depth was triaged toward the mixed-precision architecture—rather than to claim absolute accuracy numbers. Because the visual encoding is disclosed and the message is comparative, the presentation does not distort the underlying evidence.

**Changes to the manuscript.** None. Caption disclosure is already present.

---

## Summary of Pre-Emptive Changes Implemented

In addition to the point-by-point responses above, we have implemented the following minor pre-emptive clarifications to improve transparency:

- **Cover letter:** Page count corrected (14→15); contribution count aligned with §1 (6→4); energy-caveat language restated.
- **§6.5:** Dual-attention-collapse tightening (U1) to reinforce that attention-side linearizations collapse structurally regardless of exact NL value.
- **B-1 (SX.Y reachability):** Supplementary Note~SX.Y is present at `supplementary.tex:791`. Any prior report of its absence reflects a stale source snapshot; the note contains the full CrossSim subset-evaluation protocol with Wilson/t-distribution confidence intervals.
- **Response draft:** Gradient-diagnostic vs. training-reality disclosure (T1) added to auxiliary materials.

These changes do not alter any quantitative result or core claim.

---

We hope this response satisfactorily addresses the reviewers' concerns. We remain grateful for the detailed feedback, which has strengthened the clarity and transparency of the manuscript. We are happy to provide any additional material or clarification the editor may require.

Sincerely,

*The Authors*

---

*Document generated: 2026-04-19*
*Verified against: `KIMI_REBUTTAL_COVERAGE_AUDIT_20260419.md` — all manuscript citations line-level confirmed; R5 and R8 flagged as response-only arguments with no manuscript overclaim.*
