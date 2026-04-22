# Paper-2 Skeleton v0 — Structural Limits of First-Order Surrogate Training for Organic Optoelectronic CIM

**Date:** 2026-04-20  
**Agent:** Kimi Phase β — Round P2  
**Route:** R-A primary (Structural Limits / Falsification Study), R-B annex (Higher-Order Surrogate Theory), R-C framing (Deployment Envelope)  
**Status:** Skeleton complete; awaits experimental execution for §4 and §5.

---

## Narrative Arc

The paper tells a single coherent story in five movements:

1. **The Promise and the Boundary (§1).** Analog CIM with organic RRAM offers transformative efficiency for edge vision. Ensemble HAT recovers deployment-grade accuracy under moderate nonlinearity (NL = 1.0). But severe nonlinearity (NL = 2.0) collapses fresh-instance accuracy. Is this an optimization gap or a structural barrier?

2. **What Others Have Tried (§2).** Prior work catalogues simulators, HAT variants, and nonlinearity models, but no study has systematically falsified severe-NL mitigation strategies for ViT attention blocks with fresh-instance validation.

3. **The Hypothesis and Its Machinery (§3).** We formalize the Structural-Limit Hypothesis: three theoretical pillars (rank collapse, exponential amplification, scale-recovery mismatch) predict that first-order NL surrogates cannot train through severe nonlinearity in the attention pathway. We derive falsifiable conditions (F1–F3) and specify a second-order STE extension as a falsification probe.

4. **The Diagnostic Protocol (§4).** Six pre-registered experiments (CX-J1b/c/d-2/d-3, mixed partition, rank diagnostic) form a falsification lattice. Each experiment carries a pre-registered prediction and a falsification criterion. No measured values are reported here; the design is theory-first and measurement-agnostic.

5. **What It Means (§5, Discussion).** If the predictions hold, the ~30% ceiling is a structural generalization barrier, not an optimization failure. If they fail, the hypothesis is refined in a direction specified in advance. Either outcome is scientifically informative.

---

## File Map

| File | Section | Role | Word Target |
|:---|:---|:---|:---|
| `01_intro.md` | §1 Introduction | Hook, context, falsification posture, contributions, scope | ~1,800 |
| `02_related.md` | §2 Related Work | Positioning, gaps, negative-result literature | ~1,500 |
| `03_methods.md` | §3 Methods | Theory framework: 3 pillars, F1–F3, 2nd-order STE, protocols | ~2,200 |
| `04_experiments.md` | §4 Experimental Design | 6 CX-J experiments, predictions, falsification lattice | ~1,600 |
| `README.md` | — | Narrative arc, file map, agent notes | — |

---

## Core Claims (Theory-First)

1. **Structural-Limit Hypothesis.** Severe write nonlinearity (NL = 2.0) imposes a structural generalization barrier in the attention pathway of analog-mapped Vision Transformers. The ~30% fresh-instance ceiling is not an optimization failure but a falsifiable theoretical bound.

2. **Three-Pillar Mechanism.** The barrier arises from (I) gradient-asymmetry-induced rank collapse in Q/K, (II) exponential amplification of surrogate bias by softmax, and (III) instance-specific scale-recovery mismatch.

3. **Converging Negative Evidence.** Three independent mitigations (MLP-only linearization, all-linear, joint MLP-linear + Ensemble HAT) are designed to break the ceiling if the MLP-dominance hypothesis is true. Their convergence on the same bound falsifies the MLP-dominance hypothesis and strengthens the structural claim.

4. **Higher-Order Probe.** The second-order STE and third-order cumulant expansion are derived as falsification probes (CX-J1d). Whether they break the ceiling adjudicates between "surrogate-dependent" and "architecture-dependent" interpretations.

---

## Locked vs. Pre-Registered Numbers

| Number | Status | Source |
|:---|:---|:---|
| Ensemble HAT NL=1.0 fresh-instance (~86%) | **Locked** | Archived JSON / thesis |
| Standard HAT fresh collapse (~10%) | **Locked** | Archived JSON / thesis |
| MLP-only linearization fresh (~32%) | **Locked** | Archived JSON / thesis |
| All-linear fresh (~32%) | **Locked** | Archived JSON / thesis |
| Joint MLP-linear + Ensemble HAT fresh (~30%) | **Locked** | Archived JSON / thesis |
| CX-J1b/c/d-2/d-3, mixed partition | **Pre-registered predictions only** | §4 of this skeleton |

---

## Scope Discipline

- **Simulation-only.** No measured organic-array chips.
- **Tiny-ViT / CIFAR-10.** ~5M parameters.
- **First-order surrogate class.** Claims are about limits *of this class*, not absolute physical impossibility.
- **No universal laws.** Every structural claim is hedged: "under the first-order surrogate," "within the present framework."

---

## Downstream Agent Notes

- **Agent K-Y9 (drafting):** Elevate the three pillars from Methods to a dedicated Theory subsection if venue style permits. Maintain strict scope discipline. Use the CX-J1b/c/d predictions verbatim from §4; do not invent numbers.
- **Agent CX-J* (experiments):** Execute E1–E6 in parallel on 4-GPU node. Critical path: code patches for E3/E4 (second-order STE, double-backward) and E5 (digital-attention exclusion). Report results as mean ± std across 10 fresh instances; include Cohen's d and Welch's t-test against the joint-training baseline.
- **Agent G-GG* (theory):** If E3 or E4 breaks the ceiling, revise the structural-limit hypothesis to a "weak limit" (surrogate-dependent) and elevate the second-order derivation to a primary contribution. If E5 fails, revisit the pathway-decomposition analysis.
