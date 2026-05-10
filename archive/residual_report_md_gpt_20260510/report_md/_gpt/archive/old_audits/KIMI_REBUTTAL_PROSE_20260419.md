# Reviewer-Facing Rebuttal Prose — K-O2 (2026-04-19)

**Tone:** Calm, specific, citation-heavy. Each response acknowledges the concern, cites manuscript evidence, and closes with why the core claim stands.

---

## R1 — Task Complexity / ImageNet Missing

We agree that ImageNet-scale validation would strengthen the empirical scope, and we have pre-registered a pilot as a concrete next step. However, §1 explicitly scopes the study to "edge vision" tasks (CIFAR-10/100 and Flowers-102), and §4 lists the evaluated datasets. The core claim is a materials-to-system risk-ranking framework for resource-constrained nodes, not a claim of ImageNet-scale readiness; extending to larger datasets is therefore a natural follow-up rather than a missing prerequisite.

---

## R2 — Energy Model Unvalidated / Placeholder

We fully recognize that the absolute energy projections are provisional. Both §3.4 and §6.5 repeatedly qualify the estimates as "first-order upper bounds" under placeholder constants, and the cover letter restates this caveat. The relative ordering—dense analog projections yielding ~11× energy reduction versus FP32, with digital attention still dominating total cost—is robust even under the 10–50% routing overhead we disclose, which is the directional claim we actually make.

---

## R3 — Fixed Gaussian C2C/D2D vs. Spatial Correlation & Heavy Tails

Spatially correlated D2D and heavy-tailed conductance distributions are real phenomena that our present model omits, as we state candidly in the Limitations paragraph (§6.5). The Outlook explicitly scopes a "circuit-aware layer" that models spatial IR drop, sneak paths, and correlated mismatch from array geometry—a deferred priority because the present framework targets risk ranking before full hardware closure. The profile-driven substitution interface (§3.3) ensures these extensions can be adopted without code changes, so the omission does not invalidate the current comparative conclusions.

---

## R4 — NL=2.0 Is Gradient-Scaling Approximation, Not Materials Bound

The reviewer is correct that NL=2.0 reflects the present gradient-scaling surrogate rather than a measured materials limit; §6.5 states this explicitly as the "limit of this approximation." Group-wise ablation in the supplementary material localizes the bottleneck to the MLP analog path, while attention-side linearizations (QKV and projection) collapse structurally regardless of the exact NL value. Consequently, the qualitative ranking of which blocks dominate the accuracy budget remains valid even if future device measurements revise the absolute nonlinearity.

---

## R5 — Ensemble HAT Lacks External Multi-Instance Baseline

We acknowledge that no exact apples-to-apples external baseline for multi-instance HAT on organic CIM has been published, which is why our response relies on internal controls. The manuscript presents Ensemble HAT as novel, and the fresh-instance transfer protocol (Eq.~4) provides a reproducible Monte Carlo benchmark: standard HAT collapses to 10.00% accuracy on unseen mismatch maps, whereas Ensemble HAT recovers to 86.37±1.54%. This internal ablation isolates the effect cleanly, and the protocol can be adopted by future studies for direct comparison.

---

## R6 — STE Backward Surrogate Oversimplifies Pulse Accumulation

The straight-through estimator (STE) does indeed abstract away pulse-level dynamics in favor of a conductance-level surrogate, a choice we disclose transparently in §3.2. The supplementary material provides empirical guardrails (Table SX.N) that bound the failure modes of this approximation under the explored parameter range. Moreover, the forward path already includes nonlinear-write and double-exponential retention surrogates anchored to measured DNTT transients, so the dominant physical effects are captured even if the backward pass remains idealized.

---

## R7 — OPECT Calibration Constants Arbitrary / Not Representative

We agree that measured-device calibration would be preferable to literature-anchored constants. The optoelectronic frontend parameters are anchored to Zhang et al. (2025), and the supplementary sensitivity sweep demonstrates that accuracy is insensitive to ±20% variation in the key constants (γ_phys, I_dark, and α). Because the qualitative conclusions do not hinge on the exact numerical values, the present calibration is sufficient for the framework's intended purpose of relative risk ranking.

---

## R8 — Cycle Endurance Ignored

Cycle endurance is indeed a relevant concern for any analog memory technology. The present application scope, however, is inference-heavy edge vision, where read retention—modeled explicitly in the V8 retention-drift experiments (§6.5)—is the primary temporal bottleneck rather than write cycling. Training-in-memory is explicitly excluded from the deployment scenario, so endurance limitations do not threaten the operational lifetime claims made for the targeted use case.

---

## R9 — Temperature Dependence Ignored

Temperature-dependent shifts in photoresponse and mismatch variance are real effects that should be modeled, and §6.5 lists them candidly among the current limitations. The Outlook explicitly defers a temperature-aware extension to the planned "circuit-aware layer" that will incorporate temperature-dependent coefficients from array geometry. Because the present framework ranks deployment risks under nominal operating conditions, this omission bounds the scope rather than invalidating the comparative conclusions.

---

## R10 — Best-Checkpoint Reporting Masks Instability

We recognize that best-checkpoint selection can obscure training variance, which is why §5.1 explicitly discloses the protocol. This practice is standard in the noisy hardware-aware training literature, where training curves are non-monotonic by construction. The reported accuracies are further backed by 5-seed Monte Carlo averages that quantify residual variance, so the selection criterion does not inflate the results beyond what the statistical spread already permits.

---

## R11 — Fig. 4 Mixed Deterministic / MC Bars

The mixed visualization in Fig. 4 could indeed be clarified, and the caption already transparently distinguishes deterministic baselines from Monte Carlo means. The figure's purpose is to illustrate the depth-versus-noise trade-off—specifically, why Tiny-ViT depth was triaged toward the mixed-precision architecture—rather than to claim absolute accuracy numbers. Because the visual encoding is disclosed and the message is comparative, the presentation does not distort the underlying evidence.

---

*End of rebuttal prose. Each response is 2–3 sentences, citation-heavy, and closes with a scope-preserving justification.*
