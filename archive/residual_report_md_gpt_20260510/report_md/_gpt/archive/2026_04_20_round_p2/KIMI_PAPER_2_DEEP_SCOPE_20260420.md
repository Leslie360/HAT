# Deep Scoping: Three Alternative Routes for Paper \#2

**Date:** 2026-04-20
**Status:** Strategic memo — PI decision support
**Word count:** ~1,500

---

## Executive Summary

This memo scopes three post-thesis publication routes (R-A, R-B, R-C) that extend the compute-ViT platform beyond the current NC submission. Each route is evaluated on novelty, compute cost, collaborator needs, venue fit, and explicit delta over the existing manuscript. A comparative table and explicit recommendation are provided for 12-month research planning.

---

## Route R-A: Joint MLP-Linear + Ensemble HAT — Deployment-Grade Result

### (a) Hook sentence
> *By coupling block-level write-nonlinearity repair with epoch-level device-instance resampling, we break the 32 % fresh-instance ceiling that has prevented severe-nonlinear organic CIM from reaching deployment-grade accuracy.*

### (b) Key claim
The single main contribution is a **joint training recipe** that simultaneously mitigates the two deepest failure modes identified in the thesis: (1) severe write nonlinearity (NL = 2.0) via MLP-linear surrogate protection, and (2) hardware-instance overfitting via Ensemble HAT with per-epoch D2D resampling. If successful, this is the first demonstration of **≥80 % fresh-instance accuracy** under a global severe nonlinearity on an analog-mapped vision transformer.

### (c) Experiments needed
- **E-A1 — Warm-start joint training (primary):** Load canonical Ensemble HAT checkpoint (NL = 1.0, 86.37 ± 1.54 % fresh-instance), reset optimizer state, and fine-tune with MLP blocks linearized (NL = 1.0 surrogate) while attention blocks see full NL = 2.0 and D2D is resampled every epoch. Target: 100 epochs × 3 seeds.
- **E-A2 — Cold-start joint training (ablation):** Same protocol but from random initialization. Tests whether Ensemble HAT pre-training provides a favourable basin.
- **E-A3 — Fixed-mask MLP-linear re-baseline:** Re-run the existing 32 % ceiling baseline with identical hyperparameters to ensure comparability.
- **E-A4 — Fresh-instance evaluation:** All checkpoints evaluated under the canonical `10 arrays × 5 MC` protocol. Primary metric: fresh-instance mean ± std; secondary: source-domain accuracy.
- **E-A5 — Per-layer gradient-norm tracking:** Diagnostic logging to confirm that attention-block gradients remain stable when MLP path is linearized under epoch-resampling.

### (d) Compute estimate
| Component | Runs | GPU-hr per run | Subtotal |
|:---|:---|:---|:---|
| Warm-start joint (3 seeds) | 3 | ~3.0 | ~9 |
| Cold-start joint (3 seeds) | 3 | ~12.0 | ~36 |
| Fixed-mask rebaseline (3 seeds) | 3 | ~12.0 | ~36 |
| Fresh-instance eval (`10 × 5` MC) | 150 | ~0.05 | ~8 |
| Gradient-norm diagnostics | 9 | ~0.5 | ~5 |
| **Total** | — | — | **~95 GPU-hours** |

*Assumes 1× A100 or RTX 4090 equivalent; Tiny-ViT V4 on CIFAR-10.*

### (e) Venue fit
1. **Nature Electronics** — Strongest fit. A deployment-grade result that couples device physics (write nonlinearity) with algorithmic training is exactly the device–algorithm co-design the journal targets. The 80 % fresh-instance threshold is a credible "system works" milestone.
2. **Nature Communications** — Also strong, slightly lower bar for physical novelty but expects broader interdisciplinary appeal. Risk: overlap with NC #1 if reviewers treat it as an incremental extension.
3. **NeurIPS / ICML** — Weaker fit. The contribution is a domain-specific training recipe, not a general algorithmic advance. Could be reframed as "distributional robustness for structured deployment noise," but the device specificity may alienate pure-ML reviewers.

### (f) Collaborator needs
- **None essential** for the simulation experiments. The compute-ViT framework is self-contained.
- **Device collaborator (optional):** If the manuscript claims deployment readiness, a co-author from the fabrication side who can confirm NL = 2.0 is a realistic bound for the current organic-RRAM generation would strengthen credibility.
- **Statistics collaborator (optional):** To formalise the `10 × 5` protocol as a minimum-variance unbiased estimator rather than an ad-hoc rule.

### (g) Novelty relative to NC #1
| Dimension | NC #1 | R-A |
|:---|:---|:---|
| NL severity | NL = 1.0 (moderate) | NL = 2.0 (severe) |
| Instance overfitting | Diagnosed, not cured under NL = 2.0 | Jointly mitigated via MLP-linear + epoch resampling |
| Fresh-instance accuracy | 86.37 ± 1.54 % | Target ≥80 % under strictly harder physics |
| Training recipe | Single-objective HAT | Block-heterogeneous surrogate + distributional training |

The delta is **not** "same experiment, bigger number." It is a qualitatively new training objective that treats layer groups as distinct noise regimes.

---

## Route R-B: Organic-RRAM Language-Model CIM Scaling

### (a) Hook sentence
> *As vision transformers reach their analog deployment envelope, the next frontier is the language model—and with it, a new physics bottleneck: KV-cache retention drift under autoregressive token generation.*

### (b) Key claim
The first systematic study of **hardware-aware training for LLMs mapped to tiled organic-RRAM arrays**, identifying KV-cache retention as the dominant scaling bottleneck and proposing head-level mismatch resampling as the analogue of Ensemble HAT for multi-head attention parallelism.

### (c) Experiments needed
- **E-B1 — GPT-2-small baseline on WikiText-103:** Digital baseline perplexity; establish mapping feasibility for 124 M parameters.
- **E-B2 — Tile-level D2D sweep:** Map MLP and attention layers to tiled crossbars (256×256 tiles). Vary tile count and per-tile mismatch correlation. Measure perplexity gap versus digital baseline.
- **E-B3 — KV-cache retention ablation:** Simulate analog KV storage with double-exponential drift (thesis retention model). Measure perplexity degradation as a function of sequence length and token position. Compare analog versus digital KV paging.
- **E-B4 — Head-level resampling cadence:** Sweep resampling granularity (per-head, per-head-group, per-layer) under fixed total training epochs. Target: identify optimal cadence that mimics the per-epoch optimum found in vision.
- **E-B5 — Llama-3-1B pilot (stretch):** If GPT-2 results support the hypothesis, scale to 1B parameters to test weight-precision requirements (4-bit differential may be insufficient; test 6-bit and grouped-vector mapping).

### (d) Compute estimate
| Component | Runs | GPU-hr per run | Subtotal |
|:---|:---|:---|:---|
| GPT-2-small digital baseline | 3 | ~40 | ~120 |
| Tile-level D2D sweep (5 configs × 3 seeds) | 15 | ~60 | ~900 |
| KV-cache retention ablation | 20 | ~30 | ~600 |
| Head-cadence sweep (5 configs × 3 seeds) | 15 | ~60 | ~900 |
| Llama-3-1B pilot (stretch, 2 configs) | 2 | ~400 | ~800 |
| **Total (without stretch)** | — | — | **~2,500 GPU-hours** |
| **Total (with stretch)** | — | — | **~3,300 GPU-hours** |

*Assumes 8× A100 80 GB or equivalent for GPT-2; Llama-3-1B requires model parallelism.*

### (e) Venue fit
1. **NeurIPS / ICML** — Strongest fit if framed as algorithmic contribution. "Scaling HAT to LLMs" is a generalisable systems-ML problem. The KV-cache retention analysis and head-cadence results are novel enough for a top-tier ML conference, provided the empirical matrix is dense.
2. **Nature Electronics** — Strong if coupled with measured device data (e.g., actual retention curves for organic arrays at KV-cache timescales). Without physical measurements, the device community may view it as speculative simulation.
3. **Nature Communications** — Viable middle ground, but the LLM audience at NC is thinner than at NeurIPS.

### (f) Collaborator needs
- **NLP / LLM training expert:** Essential. HAT for autoregressive transformers introduces complications (causal masking, variable sequence length, gradient checkpointing under noise) that the vision codebase does not handle.
- **Device fabrication collaborator:** Highly desirable for measured KV-retention data. Without it, the retention ablation relies on the same double-exponential surrogate used in the thesis, weakening claims about LLM-specific timescales.
- **Systems / architecture collaborator:** For tiling strategy, ADC periphery energy modelling, and realistic mapping of 1B parameters to array dimensions.

### (g) Novelty relative to NC #1
| Dimension | NC #1 | R-B |
|:---|:---|:---|
| Model scale | 5 M (Tiny-ViT) | 124 M–1 B |
| Task type | Vision (classification) | Language (perplexity / generation) |
| Attention geometry | Spatial patches, fixed length | Temporal tokens, variable length |
| Memory bottleneck | Weight retention | KV-cache retention |
| Parallelism unit | Global D2D map | Tile-level maps + head-level mismatch |

The delta is **workload-scale and geometry-scale**. NC #1 asks "does ViT-on-CIM work?" R-B asks "does the principle survive the dominant AI workload of the decade?"

---

## Route R-C: Theory-Only — HAT-as-Regularizer + Ensemble-Frequency Effective Width

### (a) Hook sentence
> *We show that epoch-level hardware-instance resampling is not merely a training trick, but a distributionally robust empirical risk minimiser whose implicit regulariser is the device-instance distribution itself.*

### (b) Key claim
A **theoretical unification** of hardware-aware training under the regularisation framework: (1) a proved bound linking D2D resampling variance to Hessian trace (flat-minimum principle), and (2) the ensemble-frequency effective-width hypothesis that predicts an inverted-U relationship between resampling cadence and fresh-instance accuracy, validated by simulation on existing data.

### (c) Experiments needed
*No new GPU training. All validation uses existing checkpoints and logs.*

- **E-C1 — Hessian trace estimation:** Compute top-K Hessian eigenvalues at convergence for fixed-mask, per-epoch, and per-batch checkpoints using PyHessian or power iteration. Test prediction: Tr H(θ*_ens) ≤ (C/σ²_M) E[‖∇θℓ‖²].
- **E-C2 — Effective-width validation:** Use existing 50-epoch ablation data (per-epoch 88.41 %, fixed-mask 87.18 %, per-batch 86.16 %) to fit the inverted-U curve. Extend with intermediate cadences (resample every k batches, k ∈ {10, 50, 200}) if existing logs are insufficient; these can be run cheaply (~10 GPU-hours total) or requested from archived sweeps.
- **E-C3 — PAC-Bayes bound tightening:** Derive closed-form bound for fresh-instance risk under Gaussian-process prior over mismatch maps. Validate bound tightness by comparing bound value versus measured fresh-instance error on existing `10 × 5` data.
- **E-C4 — SAM formal correspondence:** Prove or disprove that Ensemble HAT is equivalent to SAM in device-instance space under convexity assumptions. If equivalence fails, characterise the gap structurally.

### (d) Compute estimate
| Component | Runs | GPU-hr per run | Subtotal |
|:---|:---|:---|:---|
| Hessian trace (3 checkpoints × 5 seeds) | 15 | ~0.5 | ~8 |
| Intermediate cadence sweep (if needed) | 4 | ~2.5 | ~10 |
| PAC-Bayes validation (diagnostic) | 1 | ~2 | ~2 |
| **Total** | — | — | **≤20 GPU-hours** |

*Primary cost is researcher time (proofs, LaTeX), not compute.*

### (e) Venue fit
1. **COLT / AISTATS** — Strongest fit. The Hessian bound and effective-width hypothesis are pure learning-theory contributions. COLT in particular values PAC-Bayes extensions and implicit-regularisation analyses.
2. **NeurIPS / ICML (Theory track)** — Strong. The device-instance setting is a novel domain for classical generalisation theory; reviewers in the theory track appreciate domain-driven formalism.
3. **JMLR** — Viable if the theory is extensive enough to warrant journal length. Slower turnaround (12–18 months) but deeper archival value.
4. **Nature Electronics / NC** — Poor fit. Without new physical measurements or deployment results, the experimental audience will question relevance.

### (f) Collaborator needs
- **Theoretical ML collaborator:** Strongly recommended. The PAC-Bayes bound with Gaussian-process prior over spatial mismatch maps requires expertise beyond standard textbook PAC-Bayes. A collaborator with published work in implicit regularisation or SAM theory would de-risk the proofs.
- **Optimisation theorist (optional):** For the mixing-time analysis underlying effective width (τ_mix in the AR(1) model).
- **No experimentalists required.** This is the only route that can be executed without access to fabrication or new GPU clusters.

### (g) Novelty relative to NC #1
| Dimension | NC #1 | R-C |
|:---|:---|:---|
| Contribution type | Empirical (simulation + training) | Theoretical (proofs + bound validation) |
| HAT mechanism | Described phenomenologically | Derived as Monte Carlo marginalisation |
| Per-epoch superiority | Observed ablation | Predicted by effective-width hypothesis |
| Instance overfitting | Diagnosed empirically | Explained via collapsed Hessian bound (σ²_M → 0) |
| Generalisation metric | Fresh-instance accuracy | PAC-Bayes risk bound |

The delta is **explanatory depth**. NC #1 shows *that* Ensemble HAT works; R-C proves *why* it works and predicts *when* it will fail.

---

## Comparative Table

| Criterion | R-A: Joint MLP-linear + Ensemble HAT | R-B: LLM CIM Scaling | R-C: Theory-only HAT Regulariser |
|:---|:---|:---|:---|
| **Risk (technical)** | Medium — may hit the 32 % ceiling if severe NL and instance overfitting are fundamentally incompatible | High — LLM HAT may be intractable at current compute budget; KV-cache problem may dominate | Low — proofs can be sharpened incrementally; existing data already validates main trend |
| **Risk (reviewer)** | Low-Medium — clear device+algorithm story; risk is "incremental over NC #1" | Medium — NeurIPS reviewers may question physical realism; device reviewers may question simulation-only LLM claims | Low — theory venues reward rigour over headline numbers |
| **Reward (impact)** | High within organic-CIM community; moderate in broad ML | Very high if executed — first LLM-on-organic-CIM study | Medium-High — unifies empirical HAT literature under one framework |
| **Timeline to submission** | 3–4 months (experiments + writing) | 9–12 months (requires LLM infrastructure + possibly device data) | 4–6 months (proofs + validation on existing data) |
| **Novelty type** | Empirical advance (new training recipe) | Scale advance (new domain) | Conceptual advance (new theory) |
| **Venue fit (best)** | Nature Electronics | NeurIPS / ICML | COLT / NeurIPS Theory |
| **Compute (GPU-hr)** | ~95 | ~2,500–3,300 | ≤20 |
| **Collaborator intensity** | Low (optional device co-author) | High (LLM + device + systems) | Medium (theory co-author) |
| **Fallback value** | Strong — even partial success refines deployment envelope | Weak — expensive failure leaves little salvageable | Strong — partial proofs still publishable as workshop or short paper |

---

## Recommendation

**Recommended route: R-A (Joint MLP-linear + Ensemble HAT).**

R-A offers the optimal risk–reward ratio for the next 12 months: it addresses the single most acute open question from the thesis (the severe-NL fresh-instance ceiling), requires no new collaborators or infrastructure, costs <100 GPU-hours, and targets Nature Electronics — a venue where a deployment-grade result carries immediate credibility. If R-A succeeds, it also de-risks R-B by validating that the joint-mitigation principle scales before committing to LLM-scale compute.

**Rationale in two sentences:** R-A is the only route that converts a known thesis limitation into a high-impact publication with bounded cost and no external dependencies; it is the natural next step before attempting the computationally expensive domain transfer of R-B or the theoretically demanding but lower-ceiling R-C.

---

## Fallback Plan

If R-A fails — i.e., if the joint warm-start does not exceed 50 % fresh-instance accuracy and the ablation confirms a fundamental incompatibility between first-order NL surrogates and distributional training — the fallback is **R-C (Theory-only)**.

**Why R-C, not R-B?**

- A failed R-A generates *data* (gradient norms, loss landscapes, convergence traces) that are grist for the theoretical mill: the theory can explain *why* the incompatibility exists.
- R-B is too expensive to launch without confidence that the core joint-mitigation principle works at vision scale.
- R-C can be executed in parallel with thesis writing and requires no GPU queue, making it the ideal consolation prize.

If R-A succeeds (≥80 % fresh-instance), the subsequent priority order becomes: **R-B first** (leverage the validated principle for the high-impact LLM story), then **R-C as a companion theory paper** that explains *why* R-A and R-B work.

---

*End of memo.*
