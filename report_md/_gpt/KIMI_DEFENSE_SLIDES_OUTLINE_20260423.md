# Defense Slides Outline (Branch A)

**Date:** 23 April 2026  
**Model:** Tiny-ViT-5M on CIFAR-10  
**Canonical semantics:** Branch A — no-multiplier first-order STE, sign-corrected second-order (`group=all` uniform-NL mainline)  
**Commit:** `ab56c2d`  
**Duration:** 45-minute defense + 15-minute Q&A  
**Total Slides:** 12 (10 core + 2 appendix)

> **Branch A Compliance Note:** All pre-Branch-A numbers (pre-`ab56c2d`) are marked **[INVALID]**. Only V4 canonical (~97%) is likely valid (NL=1 default, bug is no-op). K4R fresh-eval is the first canonical Branch A experiment; its result is **[PENDING]**.

---

## Slide 1: Title

- **Title:** "Analog Compute-in-Memory for Vision Transformers with Organic Optoelectronic Devices"
- **Candidate:** [Name], [Department], [University]
- **Committee:** [Member 1], [Member 2], [Member 3]
- **Key claim (thesis statement):** Vision Transformers can be deployed on noisy analog CIM with deployment-grade accuracy through structured hardware-aware training and a first-order behavioral surrogate matched to organic device physics.
- **Key number:** —

**Speaker notes:** Welcome the committee. State the central question: how do we run Vision Transformers on analog CIM arrays when noise, drift, and device variability threaten every multiply-accumulate operation? Introduce the organic optoelectronic platform and its unique challenges.

---

## Slide 2: Motivation

- The energy wall: data-movement dominates AI inference; analog CIM offers 10–100× potential savings
- Vision Transformers are the accuracy frontier but memory-bound and attention-heavy
- Organic optoelectronic devices enable wafer-scale, low-temp, flexible-substrate fabrication
- **But:** heavy-tailed noise, asymmetric conductance response, and slow retention dynamics break digital assumptions
- Need a systematic simulation framework to evaluate *before* tape-out
- **Key number:** ~88% of parameters mapped to analog; ~60% energy still digital (attention)

**Speaker notes:** Start with the familiar energy wall. The audience must feel the urgency: digital CMOS cannot scale inference energy for ViTs at the edge. Analog CIM is promising but not plug-and-play. Organic devices differ fundamentally from RRAM/PCM in noise statistics.

---

## Slide 3: System Architecture

- Hybrid analog/digital stack: dense linear ops → analog crossbars; control-heavy ops → digital
- Analog partition: patch embeddings, Q/K/V projections, output projections, feed-forward layers
- Digital partition: softmax, layer normalization, GELU, positional encoding, residuals, class token
- Tiny-ViT-5M: 4-layer encoder + MLP head, 224×224 CIFAR-10 input
- **Key number:** ~88% of parameters analog; attention stays digital per established heterogeneous CIM practice

**Speaker notes:** Present the target architecture. We study a minimal viable ViT that still exhibits core behaviors (attention, MLP, layer norm) but fits in simulation. The analog/digital split follows Lin et al., Kim et al., and recent heterogeneous CIM accelerators.

---

## Slide 4: Analog Crossbar Simulation

- Custom `AnalogLinear` layer: PyTorch nn.Module wrapping CrossSim simulator
- Forward pass: weight → conductance → noisy MAC → ADC → digital residual
- Differential-pair encoding suppresses common-mode noise; 16 conductance levels ($n_{\mathrm{states}}$)
- Device profile: JSON parameter bundle $(\sigma_{\mathrm{D2D}}, \sigma_{\mathrm{C2C}}, n_{\mathrm{states}}, G_{\min}, G_{\max}, \ldots)$
- Profile-driven substitution: swap technology without code changes
- **Key number:** 4-bit differential mapping (16 levels) is the canonical programming resolution

**Speaker notes:** Explain how we bridge PyTorch training and realistic analog inference. The same code trains digitally and evaluates on analog; no model rewriting. The profile interface is the key extensibility mechanism.

---

## Slide 5: Hardware-Aware Training (HAT)

- HAT injects physical non-idealities into the forward path while back-propagating via STE
- Standard HAT: fixes one D2D mismatch field $M_0$ for the entire run
- Ensemble HAT: resamples $M^{(e)} \sim p(M)$ at each epoch (block-stationary training)
- Fresh-instance transfer: evaluate on 10 unseen hardware instances × 5 MC passes each
- **Key number:** Standard HAT source-domain: **[INVALID pre-Branch-A]**; fresh-instance collapse to ~10% is **[INVALID pre-Branch-A]** — awaiting K4R re-anchor

**Speaker notes:** Introduce HAT as the training methodology. The critical design choice is resampling cadence: epoch-level block-stationarity gives the optimizer stability within an epoch and distributional breadth across epochs. All pre-Branch-A ensemble numbers are invalidated; K4R will re-establish the canonical baseline.

---

## Slide 6: Nonlinearity Mitigation — Branch A Mainline

- **group=all uniform-NL:** all analog-mapped layers share the same nonlinearity parameters
- **Domain randomization:** epoch-level D2D resampling acts as structured augmentation matched to the deployment distribution
- **No-multiplier STE (Equation S2):** `torch.pow(ratio, nl-1)` — intentional design, not a bug
  - The absence of an explicit `NL` prefactor is a behavioral proxy for position-dependent update difficulty, not the strict derivative of $f(G)=G^{NL}$
- **Second-order brake correction:** negative signs ($-0.5$) for both LTP and LTD — curvature braking, not acceleration
- **Key number:** $NL_{\mathrm{LTP}}=1.0$, $|NL_{\mathrm{LTD}}|=1.0$ for ideal write; $NL=2.0$ for severe-NL diagnostic regime

**Speaker notes:** This is the Branch A semantics slide. Be prepared to defend the no-multiplier form: it is an intentional behavioral proxy ratified by the user, not a coding error. The second-order negative signs act as a brake on curvature, preventing the optimizer from exploiting fragile minima in the severe-NL landscape. The `group=all` mainline is the canonical configuration; `group=mlp` is diagnostic-only.

---

## Slide 7: Results — What We Know

- **V4 canonical (NL=1 default):** ~97% CIFAR-10 — **likely valid** because the NL=1 default renders the STE semantics bug a no-op
- **Ensemble HAT fresh-instance:** **[INVALID]** — pre-`ab56c2d`, wrong second-order signs
- **K2 (N=30) severe-NL:** **[INVALID]** — pre-`ab56c2d`
- **K4 alpha sweep (old):** **[INVALID]** — pre-`ab56c2d`
- **K4R (canonical Branch A):** **[PENDING]** — first experiment on `ab56c2d`; training completed; fresh-eval (10×5 instances) queued
- **Key number:** V4 canonical ~97% ✅; all other numbers ❌ until K4R fresh-eval completes

**Speaker notes:** This is the honesty slide. State clearly that the previous headline results (86.37%, 38.95%, etc.) were produced with incorrect second-order signs and are invalid under Branch A. The V4 baseline survives because NL=1 makes the STE surrogate identity. K4R is the first live canonical experiment.

---

## Slide 8: Robustness & Physical Realism

- Framework validated at extremes: zero noise → digital accuracy; maximum noise → random guess
- Correlated D2D, retention drift, heavy-tailed noise, temperature, and IR-drop are all modeled
- OPECT zero-shot transfer: substituting Zhang 2025 parameters into the JSON profile changes accuracy without retraining
- Inverse-gamma photoresponse front-end: $P_{\mathrm{in}} = X^{1/\gamma_{\mathrm{phys}}}$ restores linearity
- **Key number:** OPECT profile ($\sigma_{\mathrm{D2D}}=3\%$, $\sigma_{\mathrm{C2C}}=2\%$) zero-shot transfer result is **[PENDING]** pending K4R re-anchor

**Speaker notes:** Emphasize that the framework is physics-agnostic at the code level; only the JSON profile changes. The physical realism extensions (correlated D2D, retention, heavy tails) are built in but their canonical numerical outputs await the K4R re-anchor.

---

## Slide 9: Limitations & Future Work

- **Dataset scale:** CIFAR-10 only; ImageNet scaling is future work
- **Architecture scale:** 4-layer ViT; full-scale ViT-Base needs validation
- **Simulator fidelity:** first-order behavioral surrogate, not SPICE; no hardware-in-the-loop yet
- **STE semantics:** no-multiplier form is an intentional proxy, but physical calibration against pulsed write data is still needed
- **Yield:** parametric variation only; hard defects and stuck-at faults not modeled
- **Key number:** —

**Speaker notes:** Be honest about boundaries. A strong defense acknowledges limitations. The first-order surrogate trades physical fidelity for gradient-path flexibility and computational tractability — essential for sweeping hundreds of training runs. Hardware-in-the-loop is the highest-priority next step.

---

## Slide 10: Conclusion

- **Framework:** first end-to-end PyTorch-to-analog-CIM framework for Vision Transformers with organic device-profile integration
- **Methodology:** structured HAT taxonomy (cadence × noise profile) enables rigorous attribution of accuracy loss to physical causes
- **Branch A semantics:** no-multiplier first-order STE + sign-corrected second-order brake + `group=all` uniform-NL mainline
- **Current status:** K4R pending — first canonical Branch A experiment will re-anchor all fresh-instance claims
- **Key number:** V4 canonical ~97% ✅; K4R fresh-instance **[PENDING]**

**Speaker notes:** Summarize in three messages: (1) the framework enables rapid ablation of analog non-idealities, (2) the Branch A semantics are ratified and intentional, (3) the community should wait for K4R fresh-eval before citing any new canonical numbers.

---

## Appendix Slide A1: Branch A Provenance Chain

- **Commit `ab56c2d`:** `fix(analog_layers): Branch A — no-multiplier first-order, sign-corrected second-order`
- **First-order STE:** `torch.pow(ratio, nl-1)` — no `NL` multiplier; matches paper Equation S2 intentionally
- **Second-order signs:** negative (`-0.5`) for both LTP and LTD — brake, not accelerator
- **Previous commits:** `0ff3b2f` (multiplier added) → `c3dbeb3` (user-ratified multiplier, now reverted) → `ab56c2d` (Branch A)
- **Invalidated experiments:** J1d, K2, K3, K4 alpha=0.00/0.25/0.50, all parity probes, first K4R attempt
- **Key number:** —

**Speaker notes:** (If asked) Walk the committee through the provenance chain. The no-multiplier form is not a bug fix; it is a reversion to the intentionally designed behavioral proxy. The second-order negative signs were derived by Gemini and ratified by the user. All experiments before `ab56c2d` used wrong signs and are invalid.

---

## Appendix Slide A2: Why Pre-Branch-A Numbers Died

- **Root cause:** second-order signs were positive (accelerator) instead of negative (brake)
- **Effect:** optimizer exploited fragile curvature minima in the severe-NL landscape
- **Result:** source-domain accuracy looked high, but fresh-instance transfer was structurally compromised
- **K2 bimodal distribution:** some instances >50%, others ~10% — signature of fragile-minima overfitting
- **Fix:** sign-corrected second-order acts as a brake, preventing the optimizer from entering narrow ravines
- **Key number:** Old K2 mean 38.95% **[INVALID]**; K4R will be the first valid severe-NL fresh-instance measurement

**Speaker notes:** (If asked) Explain the technical mechanism. The positive second-order sign amplified curvature in the wrong direction, letting the optimizer find minima that were mathematically valid under the surrogate but physically unstable under fresh D2D. The negative sign corrects this by braking curvature. This is why all old numbers had to be scrubbed.

---

## Metadata

- **Total core slides:** 10
- **Appendix slides:** 2
- **Branch A compliance:** All pre-`ab56c2d` numbers tagged [INVALID] or [PENDING]
- **Locked numbers:** V4 canonical ~97% (likely valid, NL=1 default); K4R fresh-instance [PENDING]
- **Build instructions:** Each slide entry contains sufficient detail for direct PowerPoint or Beamer construction without additional clarification.
- **Word count target:** ~1,800 words (outline density: directive, bullet-level)
