# KX43: 0412 Reviewer-Defense Addendum

> **Date**: 2026-04-13  
> **Status**: COMPLETED  
> **Scope**: Cover letter / rebuttal 增补 0412 最可能出现的攻击回应

---

## Editor Concerns → Answers (5条)

### EC1: Why NC without hardware validation?

**Editor Concern**: "Nature Communications emphasizes physical validation. Why accept pure simulation?"

**Answer**:
> This work positions itself as a **methodology paper**, not a device-characterization study. NC has precedent for pure-simulation methodology papers in the CIM domain (e.g., AIHWKIT, 2020), provided the contribution is a reusable framework with clear scope limitations. Our framework provides a transparent bridge from literature device metrics to system-level risk assessment—a contribution distinct from, and complementary to, individual device papers. The profile-driven interface explicitly anticipates future measured-data injection, making the current submission foundational infrastructure rather than preliminary findings.

---

### EC2: How do proxy parameters affect conclusion validity?

**Editor Concern**: "Can you trust system-level conclusions based on literature-extracted parameters?"

**Answer**:
> The paper's core conclusions concern **relative risk ranking** (ADC precision > D2D variation > C2C noise), not absolute quantitative predictions. This ranking emerges from the 
**structured interaction** between analog noise, digital calibration, and neural network training dynamics—physics that is robust across plausible parameter ranges. We validate this through extensive sensitivity analysis (Tables S3-S7): varying C2C 1-8% and D2D 5-20% does not invert the conclusion hierarchy. The proxy parameters enable exploratory simulation; the sensitivity analysis bounds the conclusions' validity domain.

---

### EC3: Is Ensemble HAT truly novel?

**Editor Concern**: "Resampling masks sounds like standard domain randomization."

**Answer**:
> Domain randomization (DR) perturbs input features with i.i.d. noise to bridge simulation-reality gaps. Ensemble HAT addresses a fundamentally different problem: **spatially-fixed hardware mismatch** that persists across all operations on a given array. The distinction is structural—DR adds noise; Ensemble HAT changes the underlying hardware realization being trained against. The 10.00%→86.37% fresh-instance recovery is impossible with i.i.d. augmentation because standard augmentation cannot simulate the spatial-structure mismatch causing instance-overfitting. We explicitly acknowledge DR as conceptual precedent while distinguishing our structural target.

---

### EC4: What is the physical basis for 11.45x energy claim?

**Editor Concern**: "Energy numbers appear to come from analytical placeholders."

**Answer**:
> The 11.45× is explicitly framed as a **first-order upper-bound estimate** under behavioral-model assumptions (100 fJ/MAC, 25 fJ/ADC). We do not claim circuit-validation. The contribution is the **methodology** for analog-digital decomposition and sensitivity analysis, not chip-predictive numbers. Routing overhead sensitivity (10-50% → 9.90-11.10×) demonstrates the qualitative conclusion's robustness to moderate unmodeled costs. Future tape-out validation will calibrate the absolute numbers; the present work establishes the evaluation framework.

---

### EC5: Is NL=2.0 a physical limit or model artifact?

**Editor Concern**: "The hard boundary at NL=2.0 seems arbitrarily drawn."

**Answer**:
> We explicitly scope NL=2.0 as an **approximation-limit boundary** of the gradient-scaling surrogate, not a materials constraint. The phrasing "under the present gradient-scaling surrogate" appears in the abstract, results, and limitations. Alternative training strategies (custom STE, meta-learning) may shift this boundary; identifying this as an open research direction is part of our contribution. The finding remains deployment-relevant: practitioners must know that standard HAT fails severely at NL=2.0, whether the limit is fundamental or methodological.

---

## Reviewer Concerns → Answers (8条)

### RC1: Proxy parameters create circular reasoning

**Reviewer Attack**: "You define boundaries using literature guesses, then claim discovery of those boundaries."

**Rebuttal**:
> The circularity concern is mitigated by three structural features: (1) **Explicit proxy labeling**: All proxy parameters are marked in Table S2 with full extraction methodology; (2) **Sensitivity bounding**: Tables S3-S4 show conclusions hold across ±50% parameter variation; (3) **Claim scope**: We claim deployment-risk ranking, not absolute predictions. The NL=2.0 finding, for example, is that standard HAT fails severely under the tested proxy value—a result useful for prioritizing device engineering vs. algorithm development, regardless of whether the exact threshold shifts ±20% with better measurements.

---

### RC2: C2C invariance proves you're in a protective bubble

**Reviewer Attack**: "C2C 1-8% shows zero change, so your parameters don't matter."

**Rebuttal**:
> The C2C invariance is **mechanistically explained** by scale-masking (Section 5.2): conductance noise is rescaled below the 4-bit LSB threshold. This is a model-internal conclusion valid when (a) scale recovery is active, (b) quantization dominates, and (c) noise is uniform (not proportional). We explicitly scope this: "In that regime, C2C has limited impact." The proportional-noise stress test (Section 5.6) breaks this protection, demonstrating regime-awareness rather than overgeneralization. The finding is useful precisely because it identifies when C2C engineering can be deprioritized.

---

### RC3: AIHWKIT comparison is validation theater

**Reviewer Attack**: "Two Gaussian models agreeing proves nothing about physical reality."

**Rebuttal**:
> Correct—and we do not claim physical validation. The AIHWKIT comparison is a **methodological consistency check**, analogous to cross-compiler testing: identical semantics should yield identical results. Its purpose is verifying our PyTorch implementation against an established tool, not claiming physical equivalence. We explicitly state: "this result only shows the same qualitative degradation trend under one matched regime; it does not establish full physics equivalence." The comparison provides implementation confidence; physical validation requires measured-device inference, scoped as future work.

---

### RC4: Ensemble HAT lacks baseline comparisons

**Reviewer Attack**: "Where is the comparison to stronger i.i.d. augmentation?"

**Rebuttal**:
> We acknowledge this as a valuable strengthening direction. The current manuscript distinguishes Ensemble HAT from i.i.d. augmentation on structural grounds (spatial-fixed vs. transient noise). A quantitative comparison to (a) per-forward i.i.d. D2D perturbation and (b) increased-noise-strength standard HAT would further strengthen the claim. These ablations are planned for the revision phase; the current statistical significance (10-run MC, three training seeds) and mechanistic explanation (hardware-instance overfitting) provide initial support for the structural distinction.

---

### RC5: 6-bit ADC cliff may be ViT quantization artifact

**Reviewer Attack**: "Is the ADC cliff from analog noise or ViT's natural quantization sensitivity?"

**Rebuttal**:
> The cliff is observed under the **full analog-noise + ADC model**, not pure digital quantization. Disentangling "analog noise + ADC" from "ADC alone" requires a pure-digital quantization sweep, which we acknowledge as valuable future work. However, the finding remains actionable: regardless of root cause, the 6-bit threshold defines a critical design specification for organic CIM deployment. The cross-architecture consistency (ResNet, ConvNeXt, Tiny-ViT) suggests the phenomenon is not ViT-specific. We scope the finding as "simulator-scoped" rather than claiming universal physics.

---

### RC6: Energy model lacks physical basis

**Reviewer Attack**: "100 fJ/MAC is a placeholder, not measured."

**Rebuttal**:
> Acknowledged—and explicitly disclosed. The energy model uses analytical placeholders labeled as "first-order" and "upper-bound." The contribution is the **energy-decomposition methodology** (identifying attention as 57.9% of hybrid stack) and sensitivity analysis, not absolute predictions. We report: "Adding routing overhead equal to 10--50\% of the analog-MAC budget reduces this gain to 11.10--9.90x," demonstrating that the qualitative conclusion (analog MAC advantage despite digital attention overhead) survives moderate unmodeled costs. Tape-out validation will calibrate absolute numbers; the framework enables pre-tape-out design-space exploration.

---

### RC7: No ImageNet-scale validation

**Reviewer Attack**: "CIFAR-10/100 is too simple for real edge vision."

**Rebuttal**:
> CIFAR-scale validation is standard for early-stage CIM simulation tools (AIHWKIT, MemTorch, CrossSim all use CIFAR-10/100 for initial framework validation). We explicitly acknowledge this as a limitation: "Experimental validation on full ImageNet-scale tasks remains future work." The current contribution is establishing the framework and identifying deployment-risk patterns (ADC cliff, instance overfitting) that are architecturally informative regardless of dataset scale. The profile-driven interface allows seamless scaling to ImageNet when computational resources permit.

---

### RC8: Parameter values from different devices don't compose

**Reviewer Attack**: "Vincze retention + Zhang noise parameters mix incompatible devices."

**Rebuttal**:
> The canonical profile (Table S2) is a **composite stress test** combining challenging values from different literature sources, not a claim about any single real device. This is standard practice in simulation studies to establish worst-case bounds. The profile-driven interface enables single-device calibration when unified measurements become available. We explicitly label the composite nature: "canonical profile combining reported values." The case study (Section 5.8) demonstrates single-device evaluation capability using Zhang 2025 parameters alone (88.53% zero-shot transfer). The composite profile tests framework robustness; single-device profiles evaluate specific literature claims.

---

## Usage Instructions

1. **Cover Letter**: Absorb EC1-EC5 into the "Why Nature Communications?" section
2. **Rebuttal Template**: Use RC1-RC8 as pre-written responses to anticipated reviewer comments
3. **Supplementary**: Add Parameter Risk Matrix (KX41 Defense 8) to preemptively address RC1/RC8

All responses are calibrated to be **assertive but not defensive**, acknowledging legitimate concerns while maintaining contribution scope.
