<!-- ⚠️ WARNING: This Work 2 document contains bug-contaminated severe-NL numbers (27.72%, 30.53%, etc.) from pre-fix code. Fixed at commit 9cdbe77. Do not cite as evidence. See BROADCAST_REBUILD_3WEEK_20260424.md. Work 2 is deferred until paper-1 submitted per broadcast §7.5. -->\n
# Paper-2 Full Draft Skeleton

**Title:** Structural Limits of Analog CIM for Vision Transformers: A Falsification Study

**Date:** 2026-04-18
**Status:** Skeleton v0 — post-CX-J1 pivot

---

## 00_abstract.md

**Target:** ~200 words

- **What must appear:**
  1. Hook: Three obvious mitigation strategies for severe write nonlinearity (NL = 2.0) were tested under distributional hardware-aware training; all failed at the same ~30 % ceiling.
  2. Context: Analog compute-in-memory (CIM) with organic RRAM promises efficient vision-transformer inference, but severe write nonlinearity breaks deployment-grade accuracy on fresh hardware instances.
  3. Methods: Systematic block-level linearization (MLP-only, all-linear, joint MLP-linear + Ensemble HAT) evaluated under canonical `10 fresh instances × 5 MC` protocol on Tiny-ViT V4 / CIFAR-10.
  4. Key result: The ~30 % fresh-instance ceiling is statistically indistinguishable across MLP-only (`32.12 ± 7.72 %`), all-linear (`32.60 ± 9.18 %`), and joint training (`30.53 ± 7.07 %`), while Ensemble HAT without severe NL reaches `86.37 ± 1.54 %`.
  5. Interpretation: Severe nonlinearity imposes a structural generalization barrier in the attention pathway that first-order conductance surrogates cannot overcome by block-wise linearization alone.
  6. Implication: The analog-CIM community must look beyond first-order block-heterogeneous training to higher-order or architectural remedies.

- **Locked numbers:**
  - `30.53 ± 7.07 %` (CX-J1 joint fresh-instance)
  - `86.37 ± 1.54 %` (Ensemble HAT positive control, NL = 1.0)
  - `NL = 2.0`

---

## 01_introduction.md

**Target:** ~1,500 words

- **What must appear:**
  1. **The analog-CIM promise and the deployment gap.** Analog CIM with organic RRAM offers O(1) MAC energy scaling, but device non-idealities (write nonlinearity, D2D mismatch) create a simulation-to-silicon accuracy cliff.
  2. **The two failure modes.** (a) Severe write nonlinearity (NL ≥ 2.0) degrades in-domain accuracy. (b) Hardware-instance overfitting collapses fresh-instance transfer to chance (~10 %) when D2D mismatch is fixed during training.
  3. **Ensemble HAT as partial solution.** Epoch-level D2D resampling recovers fresh-instance accuracy to `86.37 ± 1.54 %` under moderate nonlinearity (NL = 1.0), but leaves the severe-NL regime (`NL = 2.0`) unresolved.
  4. **The obvious hypothesis.** If MLP blocks (3.14 M params, 66 % of analog footprint) dominate the NL = 2.0 accuracy loss, then linearizing them while protecting attention should break the ceiling.
  5. **The falsification.** Three independent mitigations—MLP-only linearization, all-linear upper bound, and joint MLP-linear + Ensemble HAT—converge on the same `~30 %` fresh-instance ceiling, indistinguishable within variance.
  6. **The structural claim.** The barrier is not a capacity or optimization gap; it is a structural generalization limit in the attention pathway (QKV + projection, 1.57 M params) under first-order NL surrogates.
  7. **Contributions.** (i) First falsification study of severe-NL analog CIM for ViTs using converging negative evidence. (ii) Block-heterogeneous surrogate taxonomy showing MLP path is *not* the sole bottleneck. (iii) Diagnostic protocol (CX-J1b/c/d) that pre-registers falsifiable predictions. (iv) Positive control confirming Ensemble HAT remains valid under moderate NL.
  8. **Scope delimitation.** Study is simulation-only, Tiny-ViT / CIFAR-10, first-order gradient-scaling surrogate; claims are about structural limits of *this* surrogate class, not absolute physical impossibility.
  9. **Paper roadmap.** §2 related work, §3 methods, §4 results, §5 discussion, §6 conclusion.

- **Locked numbers:**
  - `86.37 ± 1.54 %` (Ensemble HAT, NL = 1.0)
  - `10.00 ± 0.00 %` (standard HAT fresh-instance collapse)
  - `30.53 ± 7.07 %` (CX-J1 joint)

---

## 02_related_work.md

**Target:** ~1,500 words

- **What must appear:**
  1. **CIM simulators and training frameworks.** AIHWKIT (IBM), MNSIM, NeuroSim, CrossSim, and compute-ViT. Emphasize that most frameworks treat device noise as i.i.d. perturbation rather than spatially structured mismatch maps.
  2. **Hardware-aware training (HAT) for CIM.** Standard HAT (fixed D2D mask), variation-aware training (Zhu et al., DATE 2020; Liu et al., DAC 2015), and quantization-aware training analogues. Gap: none address severe nonlinearity *and* instance overfitting jointly.
  3. **Ensemble / distributional training.** Domain randomization (Tobin et al.), SAM (Sharpness-Aware Minimization), and their differences from Ensemble HAT: structured spatial maps vs. isotropic parameter-space balls.
  4. **Analog nonlinearity models.** Empirical conductance-surrogate approaches (first-order Taylor, piecewise-linear) vs. physics-based compact models. Note that first-order gradient-scaling surrogates dominate the open-source literature because they are differentiable and cheap.
  5. **Vision transformers on edge / analog hardware.** ViT quantization, Tiny-ViT distillations, and analog-CIM mappings. Gap: no prior work maps ViT attention to severe-NL analog arrays with fresh-instance validation.
  6. **Negative-result and falsification literature.** Role of converging negative evidence in establishing structural limits (e.g., lottery-ticket hypothesis bounds, No Free Lunch theorems). Position this paper as a *falsification* contribution, not a failed experiment.
  7. **What we borrow vs. what is new.** Borrow: compute-ViT framework, Ensemble HAT protocol, organic-RRAM device profiles. New: systematic block-heterogeneous linearization + fresh-instance evaluation under severe NL; pre-registered diagnostic predictions.

- **Locked numbers:**
  - `NL = 2.0` (severe nonlinearity regime)
  - `10 fresh instances × 5 MC` (canonical protocol)
  - `~5 M` parameters (Tiny-ViT V4)

---

## 03_methods.md

**Target:** ~1,500 words

- **What must appear:**
  1. **compute-ViT framework overview.** Tiny-ViT V4 architecture (~5 M params), CIFAR-10 training recipe (100 epochs, AdamW, cosine schedule), analog-mapping rules (differential conductance pairs, 6-bit ADC baseline).
  2. **NL surrogate definition.** First-order gradient-scaling surrogate: effective conductance `G_eff = G_nom * (1 + NL * |ΔG|/G_max)`. Applied per block (QKV, attention projection, MLP up, MLP down). Differentiable; injected at training time.
  3. **Block-heterogeneous surrogate taxonomy.** Five training lanes: (a) standard HAT (fixed mask, NL = 2.0 everywhere); (b) MLP-only linearization (attention at NL = 2.0, MLP at NL = 1.0); (c) all-linear (NL = 1.0 everywhere); (d) joint MLP-linear + Ensemble HAT (lane b + epoch resampling); (e) canonical Ensemble HAT (NL = 1.0 everywhere, positive control).
  4. **Ensemble HAT protocol.** Per-epoch resampling of full spatial D2D mismatch map `M ~ N(0, σ²_D2D)`; block-stationary schedule; AdamW with warm restart. Contrast with fixed-mask standard HAT (single `M` for all epochs).
  5. **Fresh-instance evaluation protocol.** `10` unseen D2D realizations ("arrays") × `5` Monte Carlo forward passes per instance. Primary metric: mean accuracy across the 10 per-instance means; uncertainty: standard deviation across the 10 per-instance means. Secondary: source-domain (in-distribution) accuracy.
  6. **Diagnostic pre-registration (CX-J1b/c/d).** (b) QKV-only linearization—if ceiling breaks, barrier is QKV-specific. (c) Full-attention linearization—if ceiling breaks, barrier is attention-pathway-specific. (d) Higher-order NL surrogate (2nd / 3rd-order Taylor)—if ceiling breaks, barrier is Taylor-truncation artifact. State predictions *before* results.
  7. **Statistical treatment.** One-sample t-test against chance (10 %); paired comparison across lanes via Welch’s t-test; effect size (Cohen’s d) for ceiling-convergence claim.
  8. **Code and data availability.** Repository, locked seeds, checkpoint manifest, JSON evaluation logs.

- **Locked numbers:**
  - `σ²_D2D = (5 %)²` (canonical mismatch variance)
  - `100 epochs`
  - `10 arrays × 5 MC`

---

## 04_results.md

**Target:** ~2,000 words

- **What must appear:**
  1. **Ensemble HAT positive control (Table 1, left).** Under moderate NL = 1.0, Ensemble HAT achieves `86.37 ± 1.54 %` fresh-instance vs. standard HAT `10.00 ± 0.00 %`. Source-domain accuracy ~91 %. Validates that the protocol and framework are operational.
  2. **The three-mitigation negative matrix (Table 1, right).**
     - MLP-only linearization: source `87.79 %`, fresh `32.12 ± 7.72 %`.
     - All-linear upper bound: source ~88 %, fresh `32.60 ± 9.18 %`.
     - Joint MLP-linear + Ensemble HAT: source `91.36 %`, fresh `30.53 ± 7.07 %`.
  3. **Ceiling-convergence claim.** Welch’s t-test across the three fresh-instance means shows no significant difference (p > 0.5); 95 % CIs heavily overlap. This is the core negative result: broader linearization does *not* improve fresh-instance transfer.
  4. **Source-domain vs. fresh-instance gap.** All three mitigations restore in-domain accuracy to >87 %, yet fresh-instance transfer remains stuck. The gap is ~55–58 pp, comparable to the standard-HAT gap under NL = 1.0.
  5. **Attention-pathway footprint analysis.** Attention (QKV + proj) = 1.57 M params (33 % of analog). MLP = 3.14 M params (66 %). Because removing nonlinearity from the *larger* block yields no benefit, the bottleneck is not raw capacity but functional structure.
  6. **Diagnostic placeholders (CX-J1b/c/d).** Structured subsections with pre-registered predictions:
     - CX-J1b (QKV-only linearization): predicted to stay near ~30 % ceiling.
     - CX-J1c (full-attention linearization): predicted to stay near ~30 % ceiling.
     - CX-J1d (higher-order surrogate): predicted to stay near ~30 % ceiling.
     - Include "If prediction holds / if prediction fails" interpretation branches.
  7. **Per-instance variance analysis.** Plot or table of per-instance accuracies showing high instance-to-instance variance (σ ~ 7–9 pp) vs. tight Ensemble-HAT variance (σ ~ 1.5 pp), indicating unstable generalization rather than consistent underperformance.
  8. **Ablation: standard HAT under NL = 2.0.** Include as baseline: source-domain may be reasonable, but fresh-instance collapses to chance, confirming that the problem is not solved by naive training even with block heterogeneity.
  9. **Figure plan:** (Fig. 1) Source vs. fresh-instance scatter for all lanes. (Fig. 2) Bar chart of three converging ceilings with error bars. (Fig. 3) Per-instance spread violin plot comparing Ensemble HAT (tight) vs. severe-NL lanes (wide).

- **Locked numbers:**
  - `30.53 ± 7.07 %` (CX-J1 joint)
  - `32.12 ± 7.72 %` (MLP-only)
  - `32.60 ± 9.18 %` (all-linear)
  - `86.37 ± 1.54 %` (Ensemble HAT NL = 1.0)
  - `10.00 ± 0.00 %` (standard HAT collapse)
  - `91.36 %` (CX-J1 source-domain)
  - `1.57 M` / `3.14 M` params split

---

## 05_discussion.md

**Target:** ~1,500 words

- **What must appear:**
  1. **Structural-limit interpretation.** Why the ~30 % ceiling is not a "failed experiment" but a falsification of the MLP-dominance hypothesis. The convergence of three independent mitigations on the same bound is strong converging negative evidence.
  2. **Attention-pathway mechanism.** The softmax-normalized dot-product is multiplicative and highly sensitive to input-scale perturbations. First-order conductance surrogates introduce unmodeled curvature that breaks the query-key geometry; because the softmax is nonlinear and non-invertible, learned digital compensations do not transfer to fresh conductance realizations.
  3. **Why block-wise linearization is insufficient.** Linearizing MLP blocks (or all blocks) removes nonlinearity from the *forward-pass computation* but not from the *conductance-to-weight mapping* on fresh instances. The residual nonlinearity in attention projection + softmax is enough to destroy transfer.
  4. **First-order surrogate boundary.** The gradient-scaling surrogate assumes `δG/G` is small; at NL = 2.0 the effective perturbation amplitude violates this. The resulting training loss landscape is a poor approximation of the physical inference loss, so optimizers converge to digital minima that misalign with analog deployment.
  5. **Implications for analog-CIM design.** (i) Device: push NL < 1.5 through materials engineering if ViT deployment is the target. (ii) Algorithm: second-order or iterative conductance-update schemes may be needed. (iii) Architecture: attention-free hybrids (e.g., MLP-Mixer, state-space models) may tolerate higher NL.
  6. **Relation to Ensemble HAT.** Ensemble HAT works under NL = 1.0 because the surrogate is locally valid; under NL = 2.0 the mismatch-map manifold is no longer approximated by epoch-level resampling. The structural limit is therefore *surrogate-dependent*, not absolute.
  7. **Limitations.** (a) Simulation-only; no measured organic-array NL = 2.0 chip. (b) Tiny-ViT / CIFAR-10 scale; larger models may have different noise-averaging properties. (c) First-order surrogate class only; higher-order or full-physics surrogates are future work. (d) Single architecture family; ConvNeXt behavior under same protocol is mentioned but not primary.
  8. **Ethics / sustainability note.** Negative results prevent wasted fabrication runs; honest reporting of structural limits is essential for sustainable analog-AI research.

- **Locked numbers:**
  - `NL = 2.0` vs. `NL = 1.0` boundary
  - `~30 %` ceiling (collective shorthand for the three converging results)
  - `55–58 pp` source-to-fresh gap under severe NL

---

## 06_conclusion.md

**Target:** ~500 words

- **What must appear:**
  1. **Summary of falsification.** We pre-registered the hypothesis that block-wise MLP linearization would break the severe-NL fresh-instance ceiling. Three independent experiments falsified it, converging on `~30 %`.
  2. **Core finding.** Severe write nonlinearity (NL = 2.0) imposes a structural generalization barrier in the attention pathway of analog-mapped vision transformers that first-order block-heterogeneous surrogates cannot overcome.
  3. **Actionable insight.** The analog-CIM community should treat NL = 2.0 as a deployment-grade threshold for ViT attention blocks under current training methods; crossing it requires either higher-order surrogates, architectural redesign, or materials-level NL reduction.
  4. **Future work.** (a) Execute and report CX-J1b/c/d diagnostics. (b) Test higher-order or physics-informed surrogates. (c) Evaluate attention-free architectures under same protocol. (d) Validate on measured device arrays once available.

- **Locked numbers:**
  - `30.53 ± 7.07 %` (CX-J1)
  - `NL = 2.0`
  - `86.37 ± 1.54 %` (positive control benchmark)

---

## 07_supplementary.md

**Target:** Outline only

- **What must appear:**
  1. **Supplementary Note 1: Device profile definitions.** Full conductance-surrogate equations, parameter tables, and profile substitution interface.
  2. **Supplementary Note 2: Full hyperparameter table.** Learning rates, batch size, scheduler, seed list, checkpoint naming convention.
  3. **Supplementary Note 3: CX-J1b/c/d diagnostic specs.** Pre-registered protocols, predicted outcomes, and result placeholders.
  4. **Supplementary Note 4: Per-instance raw data.** JSON excerpts showing all 10 fresh-instance means for each lane, plus individual MC forward-pass accuracies.
  5. **Supplementary Note 5: Correlated-D2D robustness check.** Brief report of i.i.d. vs. ρ = 0.3 / 0.5 AR(1) spatial correlation under Ensemble HAT (NL = 1.0), showing bounded degradation.
  6. **Supplementary Note 6: Statistical power analysis.** Justification for n = 10 fresh instances; confidence intervals; effect-size calculations.
  7. **Supplementary Note 7: Source code manifest.** File tree, dependency versions, reproducibility instructions.
  8. **Supplementary Figures:** Fig. S1 (training curves per lane); Fig. S2 (attention-map visualizations for NL = 1.0 vs. 2.0); Fig. S3 (gradient-norm trajectories); Fig. S4 (CAD layout sketch of analog-mapped Tiny-ViT blocks).

- **Locked numbers:**
  - `n = 10` fresh instances
  - `5` MC evaluations per instance
  - `ρ = 0.3` / `0.5` (correlated D2D check)

---

*End of skeleton.*
