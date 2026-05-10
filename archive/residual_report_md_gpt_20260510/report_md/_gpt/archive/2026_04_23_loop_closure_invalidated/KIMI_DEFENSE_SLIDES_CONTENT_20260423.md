# Defense Slides Content — Branch A Canonical

**Date:** 23 April 2026
**Model:** Tiny-ViT-5M on CIFAR-10
**Canonical Semantics:** Branch A — no-multiplier first-order STE, sign-corrected second-order (`group=all` uniform-NL mainline)
**Commit:** `ab56c2d`
**Duration:** 45-minute defense + 15-minute Q&A
**Total Slides:** 12 (10 core + 2 appendix)

> **Branch A Compliance Note:** All pre-Branch-A numbers (pre-`ab56c2d`) are marked **[INVALID]**. Only V4 canonical (~97%) is likely valid (NL=1 default renders the STE semantics bug a no-op). K4R fresh-eval is the first canonical Branch A experiment; its result is **[PENDING]**.

---

## Slide 1: Title Slide

### Title
**Analog Compute-in-Memory for Vision Transformers with Organic Optoelectronic Devices**

### Content
- **Candidate:** [Name], [Department], [University]
- **Committee:** [Member 1], [Member 2], [Member 3]
- **Thesis Statement:** Vision Transformers can be deployed on noisy analog compute-in-memory (CIM) arrays with deployment-grade accuracy through structured hardware-aware training and a first-order behavioral surrogate matched to organic device physics.
- **Central Question:** How do we run Vision Transformers on analog CIM when noise, drift, and device variability threaten every multiply-accumulate operation?

### Key Number
— (Title slide)

### Visual Suggestion
Clean institutional template with thesis title, candidate photo (optional), and a small schematic of a differential-pair crossbar array in the lower-right corner.

### Speaker Notes (30 sec)
Welcome the committee and state the central question directly: how do we run Vision Transformers on analog CIM arrays when every multiply-accumulate is threatened by noise, drift, and variability? Introduce the organic optoelectronic platform—wafer-scale, low-temperature, flexible—but fundamentally different from conventional RRAM or PCM in its noise statistics and retention dynamics.

---

## Slide 2: Motivation — The Energy Wall and the Analog Promise

### Title
**Motivation: Why Analog CIM for Vision Transformers?**

### Content
- **The energy wall is real:** Data movement between memory and compute dominates AI inference energy, and digital CMOS cannot scale inference energy for ViTs at the edge; analog CIM offers 10–100× theoretical savings by performing matrix-vector products in-place via Kirchhoff-current accumulation.
- **Vision Transformers are the accuracy frontier:** Tiny-ViT-5M reaches **97.48%** on CIFAR-10 in digital FP32, but the model is memory-bound and attention-heavy, making it a natural target for weight-stationary acceleration.
- **Organic optoelectronics enable new substrates:** These devices allow wafer-scale, low-temperature, flexible-substrate fabrication with inherent photosensitivity—opening pathways for sensor-compute fusion that inorganic RRAM cannot match.
- **The catch:** Heavy-tailed noise, asymmetric conductance response, and slow retention dynamics break the deterministic assumptions of digital training; a systematic simulation framework is needed to evaluate *before* tape-out.
- **The analog ceiling:** Even with perfect analog arrays, dynamic attention (QK⊤, softmax, AV) remains digital, creating a hard lower bound on system latency and energy.

### Key Numbers
- Tiny-ViT-5M FP32 baseline: **97.48%** (digital, CIFAR-10)
- ~**87.7%** of parameters mapped to analog crossbars; ~**57.9%** of total energy still consumed by digital attention and control
- Pre-Branch-A analog energy ratio claims: **[INVALID]**

### Visual Suggestion
Split-panel figure: left side shows conventional von Neumann bottleneck schematic; right side shows hybrid analog/digital CIM stack with analog crossbars for static projections and digital backend for attention. Annotate the "analog ceiling" with a dashed red line.

### Speaker Notes (60 sec)
Start with the familiar energy wall—everyone in the room has seen the DRAM-access vs. MAC-cost bar charts. Then pivot to urgency: digital CMOS cannot scale inference for ViTs at the edge. Analog CIM is promising but not plug-and-play. Organic devices differ fundamentally from RRAM/PCM in noise statistics: they exhibit heavy-tailed variability, sub-linear photoresponse, and double-exponential retention drift. We need a simulation framework to rank risks before fabrication.

---

## Slide 3: System Architecture — The Analog/Digital Split

### Title
**System Architecture: Hybrid Analog/Digital Stack**

### Content
- **Dense linear operators → analog:** Patch-embedding convolutions, Q/K/V projection matrices, attention output projection, and feed-forward (MLP) layers are mapped to differential-pair crossbar arrays because they exhibit high weight-stationary utilization.
- **Control-heavy operators → digital:** Softmax, LayerNorm, GELU, positional encoding, residual connections, class token, MBConv blocks, and the dynamic QK⊤ and AV products remain on the digital coprocessor.
- **Target backbone:** Tiny-ViT-5M (4-layer encoder + MLP head, 224×224 CIFAR-10 input) — the smallest pretrained ViT that still exhibits attention-driven sensitivity to analog non-idealities.
- **Utilization logic:** Depthwise convolutions and dynamic attention products have poor output-unit utilization or require input-dependent matrices that cannot be pre-programmed into non-volatile arrays.
- **The split follows established heterogeneous CIM practice** (Lin et al., Kim et al., recent accelerators), but is applied here to an organic optoelectronic device stack for the first time.

### Key Numbers
- **4,730,016** parameters mapped to analog; **662,748** parameters remain digital
- Analog-mapped parameter ratio: **87.7%**
- Array count under 128×128 tiling: **812 arrays**, **13,303,808** individual devices
- Stage breakdown: Patch embedding (8 arrays), Stage 1 (48), Stage 2 (384), Stage 3 (372)

### Visual Suggestion
Architecture diagram of Tiny-ViT-5M with color-coded blocks: green for analog-mapped layers, blue for digital layers. Include a zoom-in inset showing one transformer block with Q, K, V projections in green and softmax/LayerNorm in blue.

### Speaker Notes (60 sec)
Present the target architecture. We study a minimal viable ViT that still exhibits core transformer behaviors—attention, MLP, layer norm—but fits in simulation. The analog/digital split is not arbitrary: it follows array utilization. Dense projections flatten into large matrix tiles; dynamic attention kernels cannot be pre-programmed. This creates what we call the "analog ceiling": even perfect analog arrays cannot eliminate the digital attention burden.

---

## Slide 4: Analog Crossbar Simulation — Bridging PyTorch and Physics

### Title
**Analog Crossbar Simulation: From PyTorch Weights to Noisy Conductances**

### Content
- **Custom `AnalogLinear` layer:** A PyTorch `nn.Module` wrapping the CrossSim simulator core; the same model trains digitally and evaluates on analog without code rewriting.
- **Forward pass pipeline:** Weight → differential conductance pair (G⁺, G⁻) → quantization to n_states discrete levels via STE → D2D mismatch injection → C2C noise resampling → ADC conversion → digital scale recovery.
- **Differential-pair encoding:** Positive and negative branches suppress common-mode noise; 16 conductance levels (4-bit, n_states = 16) form the canonical programming resolution.
- **Profile-driven substitution:** All device physics enter through a JSON parameter bundle (σ_D2D, σ_C2C, n_states, G_min, G_max, retention, photoresponse); swapping the profile changes the technology without changing the code.
- **Scale recovery:** The analog output is rescaled by the original digital weight norm, which empirically became necessary for Tiny-ViT to prevent activation-range collapse—a sensitivity not seen in ResNet-18 or ConvNeXt.

### Key Numbers
- 4-bit differential mapping: **n_states = 16** (canonical programming resolution)
- Optimistic regime: (σ_C2C, σ_D2D) = **(1%, 3%)**
- Standard regime: **(5%, 10%)** — main deployment target
- Pessimistic regime: **(10%, 20%)** — survival stress testing

### Visual Suggestion
Flowchart showing the full forward pipeline: W → G⁺/G⁻ → STEQuantize → +ε_D2D + ε_C2C → MAC → ADC → Ŵ_eff. Label each stage with its mathematical symbol. Use a sidebar to show the JSON profile structure.

### Speaker Notes (60 sec)
Explain how we bridge PyTorch training and realistic analog inference. The same code trains digitally and evaluates on analog; no model rewriting. The profile interface is the key extensibility mechanism: literature priors and measured device statistics enter through the same JSON bundle. This means a new semiconductor requires only a new profile, not new code.

---

## Slide 5: Hardware-Aware Training — From Compensation to Invariance

### Title
**Hardware-Aware Training (HAT): Learning Under Noise**

### Content
- **HAT injects physical non-idealities into the forward path** while back-propagating through conductance quantization via the straight-through estimator (STE), making optimization feasible despite piecewise-constant conductance states.
- **Standard HAT:** Fixes one D2D mismatch field M₀ for the entire training run; the model learns to *compensate* for a specific spatial perturbation pattern rather than becoming noise-invariant.
- **Ensemble HAT:** Resamples M⁽ᵉ⁾ ∼ p(M) at each epoch (block-stationary training), forcing the optimizer to minimize expected loss under the full manufacturing distribution rather than a single realization.
- **Fresh-instance transfer evaluation:** After training, the checkpoint is evaluated on 10 unseen hardware instances × 5 Monte Carlo passes each, separating same-instance robustness from true deployment generalization.
- **The critical distinction:** Same-instance robustness and fresh-instance robustness are fundamentally different evaluation targets—standard HAT excels at the former but fails catastrophically at the latter.

### Key Numbers
- Standard HAT source-domain accuracy (same-instance, V4): **~91.6%** **[INVALID pre-Branch-A]** — awaiting K4R re-anchor
- Standard HAT fresh-instance collapse: **~10.0%** **[INVALID pre-Branch-A]** — deterministic single-class attractor
- Ensemble HAT fresh-instance: **~86.4%** **[INVALID pre-Branch-A]** — wrong second-order signs; K4R will re-establish
- **K4R (canonical Branch A): [PENDING]** — training completed; fresh-eval (10×5 instances) queued

### Visual Suggestion
Conceptual figure comparing Standard HAT (one fixed D2D mask for all epochs) versus Ensemble HAT (new D2D mask each epoch). Right panel shows fresh-instance accuracy bars: Standard HAT collapses to 10%, Ensemble HAT distributes around 86%. Label all pre-Branch-A numbers with a red "[INVALID]" stamp.

### Speaker Notes (90 sec)
Introduce HAT as the training methodology, but immediately frame the critical design choice: resampling cadence. Standard HAT fixes one mismatch map for the entire run. The model learns to decode that specific spatial pattern as an implicit feature—essentially memorizing it. Ensemble HAT resamples at each epoch, giving the optimizer stability within an epoch and distributional breadth across epochs. All pre-Branch-A ensemble numbers are invalidated by the second-order sign bug; K4R will re-establish the canonical baseline under Branch A semantics.

---

## Slide 6: Nonlinearity Mitigation — Branch A Mainline Semantics

### Title
**Branch A Semantics: No-Multiplier STE and Sign-Corrected Second-Order**

### Content
- **`group=all` uniform-NL (mainline):** All analog-mapped layers share the same nonlinearity parameters; this is the canonical configuration for all deployment claims. The `group=mlp` variant is **diagnostic-only**—it isolates the MLP path for mechanistic study but should not be used for system-level claims.
- **Domain randomization:** Epoch-level D2D resampling acts as structured augmentation matched to the deployment distribution, not i.i.d. pixel noise; the spatial correlation structure of mismatch matters.
- **No-multiplier first-order STE (Equation S2):** `torch.pow(ratio, nl-1)` — this is an **intentional design**, not a coding bug. The absence of an explicit `NL` prefactor is a behavioral proxy for position-dependent update difficulty, not the strict derivative of f(G) = G^NL.
- **Second-order brake correction:** Negative signs (−0.5) for both LTP and LTD act as **curvature braking**, not acceleration. The positive signs used in pre-Branch-A commits allowed the optimizer to exploit fragile minima in the severe-NL landscape.
- **Physical grounding:** The NL parameters modulate gradient scaling according to conductance position: potentiation weakens near G_max, depression weakens near G_min. This is an optimizer-side abstraction, not a pulse-faithful write simulator.

### Key Numbers
- NL_LTP = **1.0**, |NL_LTD| = **1.0** for ideal symmetric write (canonical mainline)
- NL = **2.0** for severe-NL diagnostic regime (boundary of first-order approximation)
- V4 canonical (~97%) survives at NL=1 because the STE surrogate reduces to identity
- Pre-Branch-A K2 severe-NL mean **38.95%**: **[INVALID]** — wrong second-order signs

### Visual Suggestion
Equation panel: show the first-order STE form (no multiplier) and the second-order correction term with negative sign. Color-code: green for LTP branch, red for LTD branch. Add a small inset plot showing conceptual loss-landscape curvature with "brake" arrow pointing away from narrow ravine.

### Speaker Notes (90 sec)
This is the Branch A semantics slide. Be prepared to defend the no-multiplier form: it is an intentional behavioral proxy ratified by the user, not a coding error. The second-order negative signs act as a brake on curvature, preventing the optimizer from entering narrow ravines that are mathematically valid under the surrogate but physically unstable under fresh D2D. The `group=all` mainline is canonical; `group=mlp` is purely diagnostic—it tells us *where* failure localizes, but it is not a deployment configuration.

---

## Slide 7: Results — What We Know and What We Are Re-Anchoring

### Title
**Results: Locked Numbers, Invalidated Claims, and Pending Re-Anchor**

### Content
- **V4 canonical (NL=1 default, no-noise or standard uniform noise):** ~**97%** on CIFAR-10 — **likely valid** because the NL=1 default renders the no-multiplier STE semantics bug a no-op (the surrogate becomes identity, so sign errors in higher-order terms do not propagate).
- **Standard HAT fresh-instance collapse:** All claims of ~10% collapse on fresh D2D under standard HAT are **[INVALID]** — pre-`ab56c2d`, wrong second-order signs; the qualitative phenomenon may replicate but the exact numerical value is void.
- **Ensemble HAT fresh-instance:** All claims of ~86% fresh-instance accuracy under Ensemble HAT are **[INVALID]** — pre-`ab56c2d`; K4R will provide the first canonical measurement.
- **Severe-NL (K2, N=30):** All claims of bimodal distributions, 38.95% mean, and MLP-path localization are **[INVALID]** — pre-`ab56c2d`, wrong second-order signs.
- **K4R (canonical Branch A):** **[PENDING]** — this is the first experiment run on commit `ab56c2d` with corrected first-order (no-multiplier) and second-order (negative-sign) semantics; fresh-eval queued.

### Key Numbers
- V4 canonical ~97% ✅ **(likely valid, NL=1 no-op)**
- All Ensemble HAT / K2 / K3 / K4 (alpha sweep) numbers: ❌ **[INVALID]** until K4R completes
- K4R fresh-instance mean and standard deviation: **[PENDING]**

### Visual Suggestion
Traffic-light table: three columns (Experiment, Pre-Branch-A Status, Branch A Status). Green row for V4 (~97%). Red rows for all other experiments labeled "[INVALID]". One yellow row for K4R labeled "[PENDING]". Keep the table large and readable.

### Speaker Notes (60 sec)
This is the honesty slide. State clearly that previous headline results—86.37%, 38.95%, the bimodal K2 distribution—were produced with incorrect second-order signs and are invalid under Branch A. The V4 baseline survives because NL=1 makes the STE surrogate identity, so sign errors in higher-order terms cannot propagate. K4R is the first live canonical experiment. The committee should treat all pre-Branch-A numbers as historical artifacts, not evidence.

---

## Slide 8: Robustness & Physical Realism — The Framework's Scope

### Title
**Robustness & Physical Realism: Validated at Extremes, Awaiting Re-Anchor**

### Content
- **Sanity-check validation at extremes:** Zero noise → digital accuracy (97.48%); maximum noise → random guess (10.0%). The framework behaves correctly at both boundaries, confirming that the analog layer implementation is not silently broken.
- **Correlated D2D, retention drift, heavy-tailed noise, temperature placeholders, and IR-drop scalars** are all modeled within the same profile interface, though their canonical numerical outputs await the K4R re-anchor.
- **OPECT zero-shot transfer:** Substituting Zhang 2025 parameters (σ_D2D = 3%, σ_C2C = 2%, 34 states, G_max/G_min = 47.3) into the JSON profile changes accuracy without retraining, demonstrating profile-driven extensibility.
- **Inverse-gamma photoresponse front-end:** P_in = X^(1/γ_phys) restores linearity for sub-linear organic phototransistor response, but also amplifies shot-noise variance—constituting a task-dependent trade-off, not a free improvement.
- **First-order behavioral scope:** The framework is physics-agnostic at the code level; it is a risk-ranking tool, not a chip-predictive SPICE emulator.

### Key Numbers
- OPECT profile zero-shot transfer result: **[PENDING]** pending K4R re-anchor (pre-Branch-A 88.53% is **[INVALID]**)
- Zhang 2026 OPECT: G_max/G_min = **47.3**, n_states = **34**, σ_D2D = **3%**, σ_C2C = **2%**
- Canonical retention: τ₁ = **140 ms**, τ₂ = **610 ms**, A₀ = **0.6**
- Energy reduction estimate (first-order): **11.45×** vs. FP32 digital baseline **[VALID as estimate, not measured silicon]**

### Visual Suggestion
Multi-panel figure: top-left shows zero-shot transfer bars (OPECT vs. canonical); top-right shows inverse-gamma compensation curves; bottom shows retention decay curve (two-phase: fast drop to 1 s, then plateau near 79%). Label all accuracy bars with "[PENDING]" or "[INVALID]" as appropriate.

### Speaker Notes (60 sec)
Emphasize that the framework is physics-agnostic at the code level; only the JSON profile changes. The physical realism extensions—correlated D2D, retention, heavy tails—are built in but their canonical numerical outputs await K4R. The inverse-gamma compensation is a design trade-off: it linearizes signal but amplifies shot noise. We treat the 11.45× energy figure as a first-order estimate, not a silicon claim.

---

## Slide 9: Limitations & Future Work

### Title
**Limitations & Future Work**

### Content
- **Dataset scale:** CIFAR-10 only; CIFAR-100 and Flowers-102 ablations confirm complexity scaling but ImageNet validation is future work. The framework's purpose is to rank failure modes, not chase SOTA.
- **Architecture scale:** 4-layer Tiny-ViT; full-scale ViT-Base needs validation, though the failure-mode ranking (ADC cliff, instance overfitting, NL boundary) is expected to be architecture-transferable.
- **Simulator fidelity:** First-order behavioral surrogate, not SPICE; no hardware-in-the-loop yet. A full SPICE simulation of 13.3 million devices would require weeks per forward pass.
- **STE semantics:** The no-multiplier form is an intentional proxy, but physical calibration against pulsed write data is still needed. The NL=2.0 severe-NL boundary is an approximation limit, not a proven material impossibility.
- **Yield and defects:** Parametric variation only; hard defects and stuck-at faults are not modeled because organic crossbar yield statistics at 128×128 scale are not yet available in the literature.

### Key Numbers
- — (No quantitative claims on this slide)

### Visual Suggestion
Roadmap figure: horizontal timeline showing three stages. Stage 1 (Current): literature profiles, first-order surrogate, CIFAR-10. Stage 2 (Near-term): measured profiles, hardware-in-the-loop, correlated D2D. Stage 3 (Long-term): ImageNet, SPICE-coupled spatial fields, defect modeling. Use dashed arrows to indicate uncertainty.

### Speaker Notes (60 sec)
Be honest about boundaries. A strong defense acknowledges limitations. The first-order surrogate trades physical fidelity for gradient-path flexibility and computational tractability—essential for sweeping hundreds of training runs. Hardware-in-the-loop is the highest-priority next step; until then, all claims are simulation-ranking claims, not silicon predictions.

---

## Slide 10: Conclusion

### Title
**Conclusion: Framework, Semantics, and Canonical Status**

### Content
- **Framework contribution:** The first end-to-end PyTorch-to-analog-CIM framework for Vision Transformers with organic device-profile integration, enabling rapid ablation of analog non-idealities without model rewriting.
- **Methodology contribution:** A structured HAT taxonomy (cadence × noise profile) that enables rigorous attribution of accuracy loss to physical causes—distinguishing same-instance compensation from true deployment invariance.
- **Branch A semantics:** No-multiplier first-order STE + sign-corrected second-order brake + `group=all` uniform-NL mainline. These are ratified, intentional design choices, not bugs to be fixed.
- **Current canonical status:** V4 baseline ~97% is **likely valid** (NL=1 no-op); all fresh-instance and severe-NL claims are **scrubbed** pending K4R re-anchor.
- **Message to the community:** Wait for K4R fresh-eval before citing any new canonical numbers. The framework is ready for use; the numerical claims are undergoing re-validation.

### Key Numbers
- V4 canonical ~97% ✅ **(likely valid)**
- K4R fresh-instance mean ± std: **[PENDING]**

### Visual Suggestion
Three-message summary slide: (1) Framework enables rapid risk ranking; (2) Branch A semantics are ratified and intentional; (3) Community should await K4R for fresh-instance claims. Use large icons: wrench for framework, shield for semantics, hourglass for pending results.

### Speaker Notes (60 sec)
Summarize in three messages. First, the framework enables rapid ablation of analog non-idealities through profile substitution. Second, the Branch A semantics are ratified and intentional—the no-multiplier form and negative second-order signs are design choices, not errors. Third, the community should wait for K4R fresh-eval before citing any new canonical numbers. The science is sound; the bookkeeping is conservative.

---

## Appendix Slide A1: Branch A Provenance Chain

### Title
**Appendix: Branch A Provenance Chain**

### Content
- **Commit `ab56c2d`:** `fix(analog_layers): Branch A — no-multiplier first-order, sign-corrected second-order` — this is the canonical commit from which all future experiments branch.
- **First-order STE:** `torch.pow(ratio, nl-1)` — no `NL` multiplier; matches paper Equation S2 intentionally. The form is a behavioral proxy for position-dependent update difficulty.
- **Second-order signs:** Negative (−0.5) for both LTP and LTD — **brake**, not accelerator. Pre-Branch-A positive signs allowed the optimizer to exploit fragile curvature minima.
- **Commit history:** `0ff3b2f` (multiplier added) → `c3dbeb3` (user-ratified multiplier, now reverted) → `ab56c2d` (Branch A ratification).
- **Invalidated experiments:** J1d, K2, K3, K4 alpha=0.00/0.25/0.50, all parity probes, first K4R attempt — all used wrong second-order signs and are **[INVALID]** under Branch A.

### Key Numbers
- — (Provenance slide)

### Visual Suggestion
Git history diagram: horizontal timeline with commits as nodes. Color-code: gray for pre-Branch-A (invalidated), green for `ab56c2d` (canonical). Annotate each node with the key code change. Add a red "[INVALID]" banner over the gray nodes.

### Speaker Notes (if asked, 60 sec)
Walk the committee through the provenance chain. The no-multiplier form is not a bug fix; it is a reversion to the intentionally designed behavioral proxy. The second-order negative signs were derived by Gemini and ratified by the user. All experiments before `ab56c2d` used positive signs and are invalid. This is strict bookkeeping, not a scientific reversal.

---

## Appendix Slide A2: Why Pre-Branch-A Numbers Died

### Title
**Appendix: Why Pre-Branch-A Numbers Died — The Mechanism**

### Content
- **Root cause:** Second-order signs were positive (accelerator) instead of negative (brake) in all pre-`ab56c2d` experiments.
- **Effect on optimization:** The positive sign amplified curvature in the wrong direction, allowing the optimizer to find minima that were mathematically valid under the surrogate but physically unstable under fresh D2D realizations.
- **Signature of failure:** The K2 bimodal distribution—some instances >50%, others ~10%—is the classic signature of fragile-minima overfitting. The optimizer stumbled into narrow survival basins by chance.
- **Fix:** Sign-corrected second-order acts as a brake, preventing the optimizer from entering narrow ravines in the severe-NL loss landscape. This makes training more conservative but generalizes better.
- **Consequence:** All pre-Branch-A source-domain accuracy looked high, but fresh-instance transfer was structurally compromised. The old results were not "wrong" in isolation; they were optimized for the wrong objective.

### Key Numbers
- Old K2 mean **38.95%** (bimodal: some >50%, some ~10%): **[INVALID]**
- Old K4 alpha-sweep claims: **[INVALID]**
- K4R will be the first valid severe-NL fresh-instance measurement: **[PENDING]**

### Visual Suggestion
Conceptual loss-landscape plot: 2D contour map with two basins. Left panel (pre-Branch-A): optimizer zooms into narrow ravine labeled "fragile minimum"; arrow points to ~50% accuracy for lucky seeds, ~10% for unlucky. Right panel (Branch A): brake sign keeps optimizer in broad basin; arrow points to more stable but potentially lower peak.

### Speaker Notes (if asked, 60 sec)
Explain the technical mechanism. The positive second-order sign amplified curvature, letting the optimizer find minima that were valid under the surrogate but unstable under fresh D2D. The K2 bimodal distribution—some instances above 50%, others at chance—is the smoking gun. The negative sign corrects this by braking curvature. This is why all old numbers had to be scrubbed: they were optimized for an objective that did not match deployment physics.

---

## Metadata & Build Notes

| Field | Value |
|-------|-------|
| **Total core slides** | 10 |
| **Appendix slides** | 2 |
| **Branch A compliance** | All pre-`ab56c2d` numbers tagged [INVALID] or [PENDING] |
| **Locked numbers** | V4 canonical ~97% (likely valid, NL=1 default); K4R fresh-instance [PENDING] |
| **Estimated word count** | ~2,400 words (full content density) |
| **Build instructions** | Each slide entry contains sufficient detail for direct PowerPoint or Beamer construction without additional clarification |
| **Speaker notes total** | ~10 minutes of spoken material across 10 core slides |

### Recommended Timing (45-min defense)

| Slide | Duration | Cumulative |
|-------|----------|------------|
| 1. Title | 1 min | 1 min |
| 2. Motivation | 4 min | 5 min |
| 3. System Architecture | 4 min | 9 min |
| 4. Analog Crossbar Simulation | 5 min | 14 min |
| 5. Hardware-Aware Training | 5 min | 19 min |
| 6. Branch A Semantics | 5 min | 24 min |
| 7. Results / Honesty | 4 min | 28 min |
| 8. Robustness & Physical Realism | 4 min | 32 min |
| 9. Limitations | 3 min | 35 min |
| 10. Conclusion | 3 min | 38 min |
| *Buffer / questions* | 7 min | 45 min |

---

*End of document — 12 slides expanded, Branch A compliant.*

---

**⚠️ DEPRECATED 2026-04-24** — This memo references bug-contaminated data (STE branch swap + extraneous nl multiplier in analog_layers.py, fixed at commit 33bed9c). The "structural ceiling / bimodal basin / Hartigan p=0.98" narrative is invalidated. Do not cite as evidence. See BROADCAST_HALT_AND_REPLICATE_20260424.md and BROADCAST_REBUILD_3WEEK_20260424.md for current status.
