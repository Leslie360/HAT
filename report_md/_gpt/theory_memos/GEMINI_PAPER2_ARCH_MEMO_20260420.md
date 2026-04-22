# G-GG5: Paper-2 Architectural Memo — Narrative Arc Analysis and Route Recommendation

**Date:** 2026-04-20  
**Author:** Gemini Phase β — Round P2  
**Scope:** Strategic positioning of Paper-2 for downstream Agent K-Y9. Theory-first orientation; no unreported experimental digits.  
**Sources:** `GEMINI_STRUCTURAL_LIMIT_FORMAL_20260420.md` (G-GG1), `GEMINI_HIGHER_ORDER_NL_DESIGN_20260420.md` (G-GG2), `GEMINI_PATHWAY_DECOMPOSITION_20260420.md` (G-GG3), `GEMINI_FIRST_ORDER_LIMIT_20260420.md` (G-GG4), Paper-2 skeleton (`paper/paper2/draft_v0/SKELETON.md`), and Paper-1 main text (`paper/latex_gpt/main.tex`).

---

## 1. Preamble: What Paper-2 Must Do

Paper-1 established a behavioral simulation framework, identified dominant failure modes (ADC cliff, hardware-instance overfitting, inverse-gamma front-end compensation), and demonstrated that Ensemble HAT recovers deployment-grade accuracy under moderate nonlinearity (`NL = 1.0`). Paper-2 must do something *qualitatively different*: it must push into the regime where Paper-1 stopped and answer the question that Paper-1 explicitly left open—whether the severe-NL boundary is a training inconvenience or a structural generalization barrier.

The current skeleton (`SKELETON.md`) adopts a falsification posture: three independent mitigations converge on the same `~30%` fresh-instance ceiling, suggesting a structural limit. However, a skeleton is not a narrative. This memo evaluates three candidate narrative routes (R-A, R-B, R-C), assesses their epistemic and strategic value, and recommends a primary route with secondary annexes.

---

## 2. Candidate Route R-A: Structural Limits / Falsification Study

### 2.1 Core claim
Severe write nonlinearity (`NL = 2.0`) imposes a **structural generalization barrier** in the attention pathway of analog-mapped Vision Transformers that first-order block-heterogeneous surrogates cannot overcome. The `~30%` fresh-instance ceiling is not an optimization failure but a falsifiable theoretical bound.

### 2.2 Theoretical engine
This route is powered by the three-pillar framework developed in G-GG1:

- **Pillar I (Rank collapse):** State-dependent gradient scaling under `NL = 2.0` biases Q/K projections toward low-rank subspaces aligned with the training-time D2D pattern.
- **Pillar II (Exponential amplification):** The softmax operator exponentiates systematic surrogate bias, causing attention-map re-ranking that is non-invertible by linear MLP compensation.
- **Pillar III (Scale-recovery mismatch):** The learned digital scale factor `s_ℓ` calibrates to the training-time second moment of the conductance distribution; at deployment, the second moment changes and introduces a systematic gain error.

These are **mathematical mechanisms**, not empirical correlations. They generate three falsifiable conditions (F1–F3 in G-GG1) that pre-register what would refute the hypothesis.

### 2.3 Narrative arc
1. **Setup:** Paper-1 showed that Ensemble HAT works for `NL = 1.0` but collapses for `NL = 2.0`. The obvious hypothesis is that MLP blocks dominate the error budget.
2. **Test:** Three independent mitigations (MLP-only linearization, all-linear, joint MLP-linear + Ensemble HAT) are designed to break the ceiling if the hypothesis is true.
3. **Result:** All three converge on `~30%` fresh-instance accuracy.
4. **Interpretation:** The convergence is strong converging negative evidence (Popperian falsification of the MLP-dominance hypothesis). The barrier is structural, localized in the attention pathway.
5. **Forward look:** The CX-J1b/c/d diagnostic protocol provides a decision tree for future work.

### 2.4 Strengths
- **Theory-first:** The core contribution is a *claim about functional form* (attention + first-order NL surrogate = structural barrier), supported by converging negative evidence. Numbers illustrate the claim; they do not constitute it.
- **Scientific rigor:** Pre-registration of predictions, falsifiable conditions, and explicit scope delimitation ("limit of the surrogate class, not absolute physical impossibility") insulate against reviewer accusations of overclaiming.
- **Differentiation:** No prior CIM-ViT paper subjects severe-NL mitigations to systematic falsification. Most papers report a single positive result; this paper reports a *pattern of negative results* that is scientifically informative.
- **Strategic safety:** The skeleton is already drafted. The locked numbers are from archived JSON logs and thesis chapters, so the paper can be written without waiting for new experiments.

### 2.5 Weaknesses
- **Negative-result stigma:** Some venues and reviewers undervalue negative results, despite growing awareness of publication bias (see G-GG4, §5.4).
- **Scope ceiling:** If CX-J1d (second-order surrogate) breaks the ceiling, the structural hypothesis is falsified and the paper becomes a *partial* limit theorem rather than a definitive barrier. This is epistemically healthy but narratively risky.
- **Scale limitation:** CIFAR-10 / Tiny-ViT scale may be questioned; ImageNet evidence is absent.

---

## 3. Candidate Route R-B: Higher-Order Surrogate Breakthrough

### 3.1 Core claim
The `~30%` ceiling is an **artifact of first-order gradient approximation**, not a structural barrier. A second-order Taylor-corrected STE or third-order cumulant expansion breaks the ceiling and restores deployment-grade accuracy under severe NL.

### 3.2 Theoretical engine
This route draws on G-GG2, which designs:
- A second-order STE: `Φ'(G) + ½ Φ''(G) ΔG_eff`
- An asymmetric branch extension for LTP/LTD mismatch
- A stochastic cumulant expansion that propagates variance and skewness sensitivity into the backward pass

The claim is that curvature correction re-aligns the training gradient with the physical inference loss landscape, enabling the optimizer to find conductance configurations that transfer across D2D instances.

### 3.3 Narrative arc
1. **Setup:** The first-order surrogate discards curvature, asymmetry, and stochasticity. Under severe NL, these omissions are catastrophic.
2. **Method:** We derive a second-order Taylor-corrected STE and a third-order cumulant expansion, both closed-form and cheap to evaluate (`~1.1×`–`1.5×` backward overhead).
3. **Result:** CX-J1d-2 and CX-J1d-3 break the `~30%` ceiling, achieving `> 50%` (or ideally `> 80%`) fresh-instance accuracy.
4. **Interpretation:** The barrier was surrogate-dependent, not architecture-dependent. The field should invest in higher-fidelity conductance models rather than architectural redesign.
5. **Forward look:** Physical validation on measured organic arrays; extension to iterative programming models.

### 3.4 Strengths
- **Positive-result appeal:** A breakthrough narrative is easier to publish and more likely to attract citations and funding.
- **Technical depth:** The second-order surrogate design is a genuine theoretical contribution to analog training; it has independent value beyond the immediate experiment.
- **Actionable:** It gives device engineers and algorithm designers a clear path forward.

### 3.5 Weaknesses
- **High epistemic risk:** The structural-limit hypothesis (G-GG1) predicts that second-order correction *will not* break the ceiling. If the hypothesis is correct, R-B becomes a *failed* breakthrough narrative, which is the worst of both worlds.
- **Dependency on unfinished experiments:** CX-J1d-2/3 have not been executed. Committing to R-B as the primary route requires waiting for experimental results, which introduces schedule risk.
- **Narrative fragility:** If second-order correction yields only `35%` (a modest lift), the story becomes muddled—neither a clear breakthrough nor a clear limit.
- **Against theory-first mandate:** R-B is implicitly number-first: the theory (second-order surrogate) is correct *because* the numbers improve. The structural-limit framework in R-A is theory-first: the numbers illustrate a claim about functional form.

---

## 4. Candidate Route R-C: Deployment Envelope / Industrial Translation

### 4.1 Core claim
Analog CIM for edge vision is not a single technology but a **design envelope** parameterized by nonlinearity, mismatch, ADC precision, and architecture. We map the Pareto frontier of accuracy versus device stress and derive actionable guidelines for fabrication roadmaps.

### 4.2 Theoretical engine
This route is less about a single mathematical mechanism and more about **systems-level boundary characterization**:
- Iso-accuracy contours in the (ADC bits, σ_D2D, NL) parameter cube
- Energy-accuracy trade-offs under mixed digital-analog partitioning
- TRL-guided maturity assessment for organic CIM

It synthesizes Paper-1 results, the structural-limit hypothesis, and higher-order surrogate prospects into a unified deployment framework.

### 4.3 Narrative arc
1. **Setup:** The analog-CIM community lacks a rigorous envelope definition. Device papers report isolated metrics; system papers assume ideal devices.
2. **Method:** We combine the compute-ViT framework with a multi-parameter design-space sweep and a formal Pareto analysis.
3. **Result:** A bounded operating envelope: NL < 1.5 for analog attention, 6-bit ADC minimum, σ_D2D < 15% for Ensemble HAT viability.
4. **Interpretation:** These are not absolute physical laws but engineering guidelines derived from the intersection of device physics and learning theory.
5. **Forward look:** Hardware-in-the-loop validation, technology transfer to foundry partners.

### 4.4 Strengths
- **Industrial relevance:** Directly addresses the concerns of semiconductor and optoelectronic partners (see G-GG8).
- **Grant appeal:** Funding agencies favor roadmap-style contributions with clear deliverables.
- **Scope for positive framing:** Even if the severe-NL barrier is structural, the envelope tells engineers where *not* to waste effort.

### 4.5 Weaknesses
- **Not theory-first:** The core contribution is empirical characterization and Pareto mapping, not a falsifiable theoretical claim. It contradicts the stated Paper-2 mandate.
- **Scope creep:** Requires extensive new sweeps (ADC × D2D × NL × architecture) that are computationally expensive and may not be complete in time for submission.
- **Lacks novelty:** Iso-accuracy contours and Pareto frontiers are standard in systems papers; without a new theoretical hook, the contribution is incremental.
- **Overlap with Paper-1:** Paper-1 already contains Sobol analysis and contour plots. R-C risks becoming "more of the same at higher resolution."

---

## 5. Comparative Analysis

| Criterion | R-A (Structural Limits) | R-B (Higher-Order Breakthrough) | R-C (Deployment Envelope) |
|---|---|---|---|
| **Theory-first fidelity** | ★★★ Excellent | ★★☆ Moderate | ★☆☆ Weak |
| **Epistemic risk** | Low (numbers already locked) | High (depends on CX-J1d) | Medium (requires new sweeps) |
| **Narrative clarity** | High (falsification arc) | High if breakthrough holds; muddled otherwise | Medium (systems roadmap) |
| **Venue fit** | NeurIPS/ICLR (theory), Nature Electronics (broad) | NeurIPS/ICML/MLSys | DATE/ISSCC/ASP-DAC |
| **Grant leverage** | Strong (negative results prevent wasted fab runs) | Strong (positive algorithmic advance) | Strong (direct industrial relevance) |
| **Schedule safety** | High (skeleton drafted) | Low (waits on CX-J1d) | Low (needs new experiments) |
| **Differentiation from Paper-1** | Strong (new theoretical claim) | Strong (new algorithm) | Weak (extension of existing analysis) |

---

## 6. Recommendation: R-A Primary, R-B Annex, R-C Framing

### 6.1 Primary route: R-A — Structural Limits / Falsification Study

**R-A is the only route that satisfies the theory-first mandate while minimizing schedule and epistemic risk.** The structural-limit hypothesis is a genuine theoretical claim with mathematical derivation (G-GG1), falsifiable conditions (F1–F3), and pre-registered diagnostic predictions (CX-J1b/c/d). The locked numbers already support the claim; the paper can be written now.

The narrative should be positioned not as a "failed experiment" but as a **limit theorem for a well-defined surrogate class**. The title should reflect this: *"Structural Limits of Analog CIM for Vision Transformers: A Falsification Study"* (as in the current skeleton) or similar. The abstract and introduction must foreground the Popperian logic: we designed three independent mitigations capable of refuting the structural hypothesis, and their convergence on the same ceiling strengthens the claim.

### 6.2 Secondary annex: R-B — Higher-Order Surrogate Theory

R-B should appear as a **theory-forward annex** within R-A, not as a competing primary route. The second-order surrogate design (G-GG2) is too valuable to omit—it demonstrates that the authors have thought seriously about how to break the barrier—but it should be framed as a **falsification probe** rather than a guaranteed breakthrough.

Specifically:
- §3.6 (Methods) or §5.3 (Discussion) should present the second-order STE derivation.
- The CX-J1d protocol should be pre-registered as a test of whether the barrier is "surrogate-dependent or architecture-dependent."
- If CX-J1d results are available before submission, they become a powerful concluding section: either the barrier is broken (structural hypothesis falsified, but the paper still makes a valuable contribution by showing *how* it is broken) or the barrier persists (hypothesis strengthened, and the second-order surrogate becomes part of the evidence that the limit is deeper than first-order approximation).

This **annex strategy** eliminates the epistemic risk of R-B while preserving its scientific value.

### 6.3 Framing device: R-C — Deployment Envelope

R-C should appear only as a **framing device** in the Discussion and Conclusion, not as a primary contribution. The paper can close with a concise "Deployment Guidelines" subsection that translates the structural limit into actionable engineering bounds (e.g., "For analog-mapped ViT attention, target NL < 1.5; for NL ≥ 2.0, migrate attention to digital or adopt attention-free architectures"). This gives industrial readers a takeaway without diluting the theoretical core.

The full R-C scope (multi-parameter Pareto sweeps, TRL assessment, industrial partnership brief) is deferred to **Paper-3** or to standalone grant proposals (see G-GG7 and G-GG8).

---

## 7. Implications for K-Y9

Agent K-Y9 (downstream paper-drafting agent) should receive the following marching orders:

1. **Adopt the R-A skeleton** (`paper/paper2/draft_v0/SKELETON.md`) as the scaffold. Do not pivot to R-B or R-C as primary narratives.
2. **Elevate the theoretical content** from G-GG1 (§2–3) to the main text. The current skeleton places definitions in Methods; consider moving Pillar I–III to a dedicated Theory section after Introduction or integrating them into the Results interpretation.
3. **Include the second-order surrogate derivation** from G-GG2 as a Methods subsection or Appendix. Frame it as a falsification probe (CX-J1d), not as a solved problem.
4. **Maintain strict scope discipline:** CIFAR-10 / Tiny-ViT, first-order surrogate class, simulation-only. Any sentence that smells of universal physical impossibility must be hedged with "under the first-order surrogate" or "within the present framework."
5. **Pre-register CX-J1b/c/d predictions explicitly** in the Methods or Supplementary. This is the paper's strongest methodological signature.
6. **Use the G-GG3 pathway-decomposition analysis** to explain *why* MLP linearization fails to help: the MLP path is a local refinement engine; the attention path is a global routing engine. Linearizing the former preserves the latter, but the latter is the bottleneck.

---

## 8. Summary

Three candidate routes were evaluated. **R-A (Structural Limits / Falsification Study)** is recommended as the primary narrative because it is theory-first, epistemically rigorous, schedule-safe, and differentiated from Paper-1. **R-B (Higher-Order Surrogate)** is retained as a secondary theory annex and falsification probe. **R-C (Deployment Envelope)** is demoted to a framing device in the Discussion, with its full scope deferred to future work. This partitioning maximizes scientific clarity while preserving strategic optionality for grants and industry engagement.
