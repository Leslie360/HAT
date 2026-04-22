# KIMI Rebuttal Master Index — 2026-04-20

**Scope:** Consolidated, deduplicated index of all anticipated reviewer objections across five source documents.  
**Constraint:** Reference document; bullet-heavy, scannable. PM should find any objection in <10 s.

---

## 1. Summary Table

| OBJ-ID | Topic | Covered? | Exp. needed? | Pri. | Source |
|--------|-------|----------|--------------|------|--------|
| OBJ-01 | No hardware-in-the-loop validation | Partial | Yes | P0 | CLAUDE_PREP |
| OBJ-02 | No analog/digital mapping ablation | Partial | Yes | P0 | CLAUDE_PREP |
| OBJ-03 | 10.00 % collapse = possible bug | Yes | No | P0 | CLAUDE_PREP |
| OBJ-04 | Incomplete multi-seed campaign | Partial | Yes | P1 | CLAUDE_PREP |
| OBJ-05 | "Risk-aware" title lacks formal metrics | Partial | No | P0 | CLAUDE_PREP |
| OBJ-06 | Heavy-tailed conductance distributions | Partial | Yes | P1 | ARSENAL_V1 |
| OBJ-07 | IR drop / sneak-path modeling | Partial | Yes | P1 | ARSENAL_V1 |
| OBJ-08 | Temperature drift and dynamic thermal variation | Partial | Yes | P1 | ARSENAL_V1 + GEN_V2 |
| OBJ-09 | ADC 6-bit threshold rationale | Yes | No | P0 | ARSENAL_V1 + METHODS_V2 |
| OBJ-10 | Ensemble HAT frequency (epoch vs. batch) | Partial | Yes | P1 | ARSENAL_V1 |
| OBJ-11 | Attention-head specialization | Partial | Yes | P1 | ARSENAL_V1 |
| OBJ-12 | NL gradient-scaling surrogate justification | Yes | Yes | P1 | ARSENAL_V1 |
| OBJ-13 | CIFAR-10 vs. CIFAR-100 headline choice | Yes | No | P1 | ARSENAL_V1 |
| OBJ-14 | Retention plateau beyond 79 % | Partial | Yes | P1 | ARSENAL_V1 |
| OBJ-15 | n = 10 fresh instances — statistical power | Yes | No | P1 | ARSENAL_V1 + STATS_V2 |
| OBJ-16 | Two-level MC hierarchy / proper SEM | Yes | No | P2 | STATS_V2 |
| OBJ-17 | Multiple comparisons correction (k = 6) | Partial | No | P2 | STATS_V2 |
| OBJ-18 | Cohen's d / effect size | Partial | No | P2 | STATS_V2 |
| OBJ-19 | Paired Δ CIs for correlated-D2D | Partial | No | P2 | STATS_V2 |
| OBJ-20 | Tiny-ViT scale vs. ViT-Base | Partial | Yes | P1 | METHODS_V2 |
| OBJ-21 | 4-bit conductance vs. 2/8-bit targets | Yes | No | P2 | METHODS_V2 |
| OBJ-22 | D2D σ = 10 % as canonical value | Yes | No | P2 | METHODS_V2 |
| OBJ-23 | Pairwise vs. joint attention–MLP perturbation | Partial | Yes | P1 | METHODS_V2 |
| OBJ-24 | Language-model workload transfer | Partial | Yes | P1 | GEN_V2 |
| OBJ-25 | CNNs outside studied class | Partial | No | P2 | GEN_V2 |
| OBJ-26 | FP8 digital inference vs. 4-bit analog | Partial | Yes | P1 | GEN_V2 |
| OBJ-27 | Fine-tuning-only HAT vs. from-scratch | Yes | No | P2 | GEN_V2 |

---

## 2. Deduplicated Objections

### OBJ-01 — No fabricated-array or hardware-in-the-loop validation
- **Objection:** The study is simulation-only; no real organic crossbar measurements validate simulator predictions against physical reality.
- **Response:** The JSON parameter interface (§3.5, `tab:measurement-mapping`) lets literature priors and measured profiles enter identically, making this an intentional simulation baseline. We acknowledge hardware validation as the next step and cite the AIHWKIT cross-framework sanity check (§6.6) as qualitative trend validation.
- **Pointer:** §6.6–6.7 (add proactive sentence now). Experiment: physical array correlation.
- **Cross-links:** —

### OBJ-02 — No analog/digital layer mapping ablation
- **Objection:** The hybrid mapping rule is fixed with no exploration of alternative splits, so the "digital attention creates an analog ceiling" conclusion assumes a specific mapping never varied.
- **Response:** The mapping follows standard CIM principles: dense static weights map to crossbars, while dynamic token-dependent operations cannot be pre-programmed. Arbitrary layer-wise assignment is already supported via configuration flags, so ablations are deferred future work.
- **Pointer:** §3.1 (add one clarifying sentence now). Experiment: layer-wise remapping ablation.
- **Cross-links:** —

### OBJ-03 — 10.00 % chance-level collapse could be a software bug
- **Objection:** The exactly 10.00 % figure (CIFAR-10 chance level) is suspiciously clean, raising concerns the collapse is a simulator bug rather than a real physical failure mode.
- **Response:** Determinism across 10 instances × 5 MC (10.00 ± 0.00 %) and differential architecture behavior argue against a universal code bug. Group-wise ablations confirm attention-side QKV and projection lanes collapse structurally regardless of NL value (Supplementary `tab:supp-nl-ablation`), localizing the failure.
- **Pointer:** §5.6, §5.8, §5.9, Supplementary `tab:supp-nl-ablation`; 51 unit tests passed.
- **Cross-links:** OBJ-15

### OBJ-04 — Incomplete multi-seed training campaign
- **Objection:** Only a seed-42 rerun is shown; reported ± values reflect C2C evaluation noise rather than training variance, weakening robustness claims.
- **Response:** The seed-42 rerun matches the canonical result within <1 pp, and MC evaluation variance (±0.48 %) is tighter than cross-instance variance (±1.54 %), so training-seed variance is sub-dominant. The fresh-instance protocol tests robustness to the largest source of analog variance.
- **Pointer:** §A.1 (appendix discloses interim state). Experiment: full multi-seed campaign (running).
- **Cross-links:** —

### OBJ-05 — "Risk-Aware Deployment" title claim lacks formal risk metrics
- **Objection:** The title promises risk-aware deployment, yet the paper uses accuracy as the sole metric with no worst-case guarantees, probability-of-failure, CVaR, or Bayesian framework.
- **Response:** "Risk-aware" means structured identification and ranking of hardware-induced failure modes prior to fabrication closure, not portfolio-theoretic optimization. The framework outputs a ranked risk map of device profiles and operating regimes by accuracy decile.
- **Pointer:** §1 (add clarifying sentence now). No experiment needed.
- **Cross-links:** —

### OBJ-06 — Heavy-tailed conductance distributions
- **Objection:** The mismatch model assumes Gaussian D2D/C2C noise, yet real organic RRAM arrays typically exhibit heavy-tailed (log-normal or Pareto) distributions that produce far more damaging outlier devices.
- **Response:** The manuscript acknowledges this in §6.5, and the profile interface (§3.5) allows heavy-tailed distributions without code changes once measured. The supplementary correlated-D2D stress test (ρ = 0.3, 0.5) shows bounded degradation while preserving ranking separation.
- **Pointer:** §6.5, Supplementary correlated-D2D. Experiment: log-normal D2D stress test.
- **Cross-links:** OBJ-22

### OBJ-07 — IR drop and sneak-path modeling
- **Objection:** The simulation ignores position-dependent IR drop along wordlines and bitlines, which introduces systematic, input-pattern-dependent weight distortion potentially more harmful than stochastic Gaussian noise.
- **Response:** IR drop and sneak paths are explicitly flagged as omitted in §3.6 and §6.5, framing results as upper bounds under idealized interconnect. A SPICE-calibrated positional bias plugin can be inserted through the existing layer extension without script changes.
- **Pointer:** §3.6, §6.5. Experiment: SPICE-calibrated array models.
- **Cross-links:** —

### OBJ-08 — Temperature drift and dynamic thermal variation
- **Objection:** Temperature-dependent mobility shifts are ignored, and dynamic thermal variation over the inference lifetime could degrade the 79 % retention plateau and 86.37 % Ensemble-HAT claim.
- **Response:** The study is scoped to nominal fixed-temperature conditions with temperature effects listed in §6.5 as a bounding limitation. Temperature-dependent coefficients can be added as new JSON profile fields once device characterization is available.
- **Pointer:** §6.5, §6.6. Experiment: temp-dependent retention + mismatch stats + time-varying sweep.
- **Cross-links:** OBJ-14

### OBJ-09 — ADC 6-bit threshold rationale
- **Objection:** The 6-bit ADC threshold appears empirical with no first-principles derivation from attention-score dynamic range or softmax precision requirements, raising questions whether it is fundamental or a simulator artifact.
- **Response:** The 6-bit threshold is empirically localized from a 63-point joint sweep (§5.5) and framed as a simulator-configured, architecture-dependent constraint. §6.6 already warns the cliff may shift for deeper MLP stacks, underscoring its regime-specific nature.
- **Pointer:** §5.4, §5.5, §6.1, §6.6. No experiment needed.
- **Cross-links:** OBJ-21

### OBJ-10 — Ensemble HAT frequency selection (epoch vs. batch)
- **Objection:** There is no ablation showing batch-level or layer-level resampling would not outperform the stated per-epoch Ensemble HAT frequency.
- **Response:** Epoch-level resampling balances mismatch exposure against stable Adam convergence, which batch-level changes would disrupt by injecting gradient noise. Ensemble HAT achieves 86.37 ± 1.54 % across 10 fresh instances, validating epoch-level exposure as sufficient.
- **Pointer:** §5.8, §6.6. Experiment: batch-level ablation (hyperparameter only).
- **Cross-links:** —

### OBJ-11 — Attention-head specialization
- **Objection:** Mapping entire Q, K, V projection matrices to analog assumes all attention heads are equally sensitive to conductance noise, but individual heads may exhibit widely different analog fragility.
- **Response:** Block-level evaluation matches crossbar mapping on concatenated weight tensors; per-head ablations would obscure the materials-to-system question. Prior ViT quantization studies show heads vary in sensitivity, so the block-level treatment is an upper-bound cost estimate.
- **Pointer:** §3.1, §5.4 (PTQ4ViT, Q-ViT, FQ-ViT). Experiment: per-head ablation + energy re-accounting.
- **Cross-links:** —

### OBJ-12 — NL gradient-scaling surrogate justification
- **Objection:** The NL = 2.0 failure boundary is derived from a gradient-scaling surrogate whose physical basis is unclear, so materials scientists may not trust a proxy that abstracts away pulse-level ionic migration.
- **Response:** The NL surrogate is a first-order behavioral proxy channeling write asymmetry into the optimizer (§3.3), not a pulse-accurate simulator. Supplementary group-wise ablations confirm attention-side collapse structurally regardless of exact NL value (`tab:supp-nl-ablation`), localizing the failure.
- **Pointer:** §3.3, §6.5, Supplementary `tab:supp-nl-ablation`. Experiment: pulse-level KMC or SPICE write model.
- **Cross-links:** —

### OBJ-13 — CIFAR-10 vs. CIFAR-100 headline dataset choice
- **Objection:** The abstract foregrounds CIFAR-10 while the most compelling HAT recovery (+21.42 pp) appears on CIFAR-100, suggesting the harder dataset is buried to make analog deployment seem more mature.
- **Response:** CIFAR-10 is the standard proof-of-concept in analog-CIM literature, enabling direct comparison with prior work, while CIFAR-100 is foregrounded in §5.3 and §6.3. The abstract notes the framework spans all three datasets without privileging any single metric.
- **Pointer:** §5.1, §5.3, §6.3. No experiment needed.
- **Cross-links:** —

### OBJ-14 — Retention plateau beyond 79 %
- **Objection:** The 79 % retention plateau from 10 s to 10 000 s is far below the 97.48 % digital baseline, with no concrete path shown to push retention accuracy higher.
- **Response:** The 79 % plateau is a lower bound under uniform double-exponential decay with co-decay of D2D buffers (§5.5), not a ceiling. State-dependent retention and inference-time drift tracking could recover accuracy by adapting digital scale factors post-drift.
- **Pointer:** §5.5, §3.5.2, §6.5. Experiment: adaptive gain-recalibration or state-dependent-retention HAT retraining.
- **Cross-links:** OBJ-08

### OBJ-15 — n = 10 fresh instances — statistical power and variance reliability
- **Objection:** With only n = 10 fresh instances, the reported 86.37 ± 1.54 % lacks sample size for a stable variance estimate, and a reviewer cannot distinguish genuine generalization from sampling noise.
- **Response:** The coefficient of variation is 1.78 %, and a one-sample t-test against 10 % chance yields t(9) = 149.25, p = 1.4 × 10⁻¹⁶ with 95 % CI [85.27 %, 87.46 %]. Power exceeds 0.999 at α = 0.001, so the verdict is not sample-size limited.
- **Pointer:** §5.8, §3.2; `fresh_instance_eval.json`. No experiment needed.
- **Cross-links:** OBJ-03, OBJ-16, OBJ-17, OBJ-18, OBJ-19

### OBJ-16 — Two-level MC hierarchy / proper SEM
- **Objection:** The ±1.54 pp spread looks like raw between-instance SD, not a hierarchical SEM accounting for both within-instance MC noise and between-instance D2D noise.
- **Response:** The ±1.54 pp is the between-instance SD; the hierarchical SEM from the 10 × 5 design is 0.51 pp, practically identical to the naive 0.49 pp because MC variance is negligible. The 95 % CI remains [85.27 %, 87.46 %], while standard HAT is [10.00 %, 10.00 %].
- **Pointer:** §3.2, §5.8; `fresh_instance_eval.json`. No experiment needed.
- **Cross-links:** OBJ-15, OBJ-17, OBJ-18, OBJ-19

### OBJ-17 — Multiple comparisons correction across four conditions
- **Objection:** The supplementary figure juxtaposes four conditions with six pairwise contrasts presented without Bonferroni, Tukey, or false-discovery correction.
- **Response:** Ensemble HAT vs. standard HAT survives Bonferroni (k = 6, α_adj = 0.0083) with p < 10⁻¹⁵. Holm-Bonferroni retains i.i.d. vs. ρ = 0.5 (p = 0.009), while i.i.d. vs. ρ = 0.3 falls to p = 0.067 and is reported as descriptive.
- **Pointer:** Supplementary Fig. correlated-D2D. No experiment needed.
- **Cross-links:** OBJ-15, OBJ-16, OBJ-18, OBJ-19

### OBJ-18 — Cohen's d / effect size on the 86.37 % vs. 10.00 % gap
- **Objection:** p < 10⁻¹⁵ with n = 10 is trivial when the null is 10 % chance, and standard HAT has zero variance, so what is the standardized effect size?
- **Response:** Standard HAT collapses deterministically to 10.00 ± 0.00 %, so pooled Cohen's d is undefined; the one-sample d against chance is 49.75. At this effect size, power is effectively 1.000 at α = 0.05 and α = 0.001.
- **Pointer:** §5.8; `fresh_instance_eval.json`, `fresh_instance_eval_v4_standard_noamp.json`. No experiment needed.
- **Cross-links:** OBJ-15, OBJ-16, OBJ-17, OBJ-19

### OBJ-19 — Paired confidence intervals for correlated-D2D Δ
- **Objection:** The supplementary figure shows marginal error bars for each correlated-D2D condition but no paired confidence intervals for the accuracy drop relative to the i.i.d. baseline.
- **Response:** Paired comparison using the same 10 seeds shows i.i.d. → ρ = 0.3 drops 1.76 pp, 95 % CI [0.97, 2.56] (paired t = 5.02, p = 0.0007), and i.i.d. → ρ = 0.5 drops 4.20 pp, 95 % CI [2.07, 6.34] (paired t = 4.46, p = 0.0016). Both intervals exclude zero.
- **Pointer:** Supplementary Fig. correlated-D2D; `fresh_instance_eval_v4_ensemble_correlated_d2d.json`. No experiment needed.
- **Cross-links:** OBJ-15, OBJ-16, OBJ-17, OBJ-18

### OBJ-20 — Tiny-ViT scale vs. ViT-Base
- **Objection:** Tiny-ViT-5M is a compact 5M-parameter model, and smaller models may artificially inflate analog fragility because narrower MLP hidden dimensions amplify per-device noise; conclusions about "transformer sensitivity" may be scale artifacts.
- **Response:** Tiny-ViT-5M is an ImageNet-pre-trained edge transformer matching the intended low-power organic optoelectronic use case. The manuscript frames the comparison as an architecture-and-training interaction, and §6.6 scopes ImageNet-scale extrapolation outside the evidence base.
- **Pointer:** §4, §6.2, §6.6. Experiment: ViT-Base/Small ablation (config change only).
- **Cross-links:** —

### OBJ-21 — 4-bit conductance vs. 2-bit or 8-bit commercial targets
- **Objection:** The canonical weight quantization uses 16 levels (4-bit), but commercial ReRAM roadmaps target 2-bit cells for density while high-precision demonstrators use 8-bit; the conclusion that quantization is sub-dominant may not hold at 2-bit or 8-bit.
- **Response:** 4-bit is a representative low-precision midpoint aligning with organic CIM demonstrations (OPECT ≈5-bit), and the zero-noise V2 control proves quantization is sub-dominant to ADC and D2D effects. n_states is a drop-in JSON parameter, so 2/8-bit ablations need no code changes.
- **Pointer:** §3.3, §5.2, Appendix `tab:measurement-mapping`. No experiment needed.
- **Cross-links:** OBJ-09

### OBJ-22 — D2D σ = 10 % as canonical value
- **Objection:** The canonical device-to-device variability is 10 %, yet the OPECT case study uses 3 % and organic ReRAM papers report <1 % to >20 %; readers may not trust conclusions drawn from a stress-test midpoint.
- **Response:** 10 % is a deliberate stress-test midpoint within a 1 %–20 % sweep (§5.5); the manuscript does not hinge on a single point. The OPECT proxy (3 %) is validated in the zero-shot case study (§5.9), and rank ordering holds across the span.
- **Pointer:** §3.3, §5.5, §5.9, Appendix `tab:measurement-mapping`. No experiment needed.
- **Cross-links:** OBJ-06

### OBJ-23 — Pairwise vs. joint attention–MLP perturbation
- **Objection:** The group-wise ablation treats QKV, output projection, and MLP as separate groups, so this one-factor-at-a-time design cannot detect interactions such as whether MLP noise is benign only when attention is clean.
- **Response:** Group-wise ablation localizes failure to specific blocks while keeping training tractable, and §6.5 does not overstate it as factorial. Both attention-side linearizations collapse independently, so their fragility does not depend on MLP noise; 2³ factorial is future work.
- **Pointer:** §6.5. Experiment: factorial joint-perturbation ablation.
- **Cross-links:** —

### OBJ-24 — Language-model workload transfer
- **Objection:** The conclusions—especially the 6-bit ADC cliff or Ensemble HAT recipe—may not transfer to large language models where sequence lengths are orders of magnitude longer and attention serves a different function.
- **Response:** The manuscript limits claims to vision backbones and edge-vision benchmarks (§1, §6.6), so language-model transfer is outside the evidence base. The core mechanisms—ADC quantization, D2D mismatch, ensemble resampling—are operator-agnostic and apply to any linear layer.
- **Pointer:** §1, §6.6. Experiment: LLM linear-layer analog CIM benchmark.
- **Cross-links:** —

### OBJ-25 — CNNs outside studied class (EfficientNet, MobileNet)
- **Objection:** ResNet-18 is an old design and ConvNeXt is essentially a Transformer-ized CNN, so conclusions may not generalize to modern efficient CNNs actually deployed at the edge.
- **Response:** The CNN-vs-Transformer comparison is framed as an architecture-and-training interaction, not a universal law (§6.2). The framework's profile-driven interface and operator substitution are backbone-agnostic, so EfficientNet or MobileNet require only configuration changes.
- **Pointer:** §5.1, §6.2, §3.4. No structural code changes needed.
- **Cross-links:** —

### OBJ-26 — FP8 digital inference vs. 4-bit analog
- **Objection:** Modern digital accelerators already ship FP8 inference with minimal accuracy loss, so noisy 4-bit analog arrays may not be justified when FP8 digital likely achieves comparable accuracy at lower risk.
- **Response:** The manuscript does not benchmark FP8; the energy comparison is strictly versus FP32 digital (§6.4), projecting roughly an order-of-magnitude dense-projection reduction. Whether that survives against optimized FP8 remains an open question outside the present scope.
- **Pointer:** §5.1, §6.4. Experiment: FP8 iso-accuracy energy comparison.
- **Cross-links:** —

### OBJ-27 — Fine-tuning-only HAT vs. training-from-scratch
- **Objection:** Tiny-ViT is fine-tuned from a pretrained checkpoint whereas ConvNeXt is trained from random initialization, raising the question of whether HAT only works with expensive pre-training.
- **Response:** ConvNeXt reaches 60.54 % on CIFAR-100 from scratch with HAT versus 23.86 % without, and Tiny-ViT is fine-tuned with HAT. Both recover strongly, so pre-training is not a prerequisite; the Ensemble HAT mechanism (Eq. 2, §3.2) is paradigm-agnostic.
- **Pointer:** §5.1, §6.2, §3.3. No experiment needed.
- **Cross-links:** —

---

## 3. Cross-Link Index

| Cluster | OBJ-IDs | Shared data / theme |
|---------|---------|---------------------|
| **A — n = 10 statistics** | OBJ-15, OBJ-16, OBJ-17, OBJ-18, OBJ-19 | `fresh_instance_eval.json`; 86.37 % vs. 10.00 % collapse |
| **B — ADC / conductance precision** | OBJ-09, OBJ-21 | ADC sweep (§5.4–5.5), `n_states` JSON profile |
| **C — D2D distributional assumptions** | OBJ-06, OBJ-22 | Gaussian vs. heavy-tailed; σ = 3 % (OPECT) to 20 % sweep |
| **D — Retention / thermal envelope** | OBJ-08, OBJ-14 | 79 % plateau (§5.5), uniform decay, state-dependent extension |
| **E — Collapse determinism** | OBJ-03, OBJ-15 | 10.00 % chance-level collapse across 10 instances × 5 MC |

---

## 4. P0 (Critical) — Pre-empt in manuscript or cover letter now

- **OBJ-01** — Add one sentence to §6.6/§6.7: hardware-in-the-loop validation is the highest-priority next step; present results are an intentional simulation baseline.
- **OBJ-02** — Insert one sentence in §3.1: the fixed split is a design choice grounded in array-utilization principles; layer-wise mapping ablations are deferred future work.
- **OBJ-03** — Add a methodological note in §5.6 or cover letter citing multi-architecture differential behavior and group-wise ablations as independent evidence against a global coding error.
- **OBJ-05** — Insert one clarifying sentence in §1 (or abstract) defining "risk-aware deployment" as structured identification and ranking of hardware-induced failure modes prior to fabrication closure.
- **OBJ-09** — Ensure §5.4/§6.1 explicitly frames the 6-bit threshold as empirically derived from a 63-point joint sweep and regime-specific, not a universal theorem.

---

## 5. P1 (Important) — Keep in response letter

OBJ-04, OBJ-06, OBJ-07, OBJ-08, OBJ-10, OBJ-11, OBJ-12, OBJ-13, OBJ-14, OBJ-15, OBJ-20, OBJ-23, OBJ-24, OBJ-26

---

## 6. P2 (Nice-to-have) — Only if explicitly raised

OBJ-16, OBJ-17, OBJ-18, OBJ-19, OBJ-21, OBJ-22, OBJ-25, OBJ-27

---

## 7. Quick-Stats Box

| Metric | Value |
|--------|-------|
| **Total objections** | 27 |
| **Covered in manuscript (Yes + Partial)** | 27 / 27 (100 %) |
| **Covered in manuscript (Yes only)** | 9 / 27 (33 %) |
| **Needing new experiments** | 14 / 27 (52 %) |
| **Median response length** | 36 words |
| **P0 / P1 / P2 split** | 5 / 14 / 8 |

---

*Generated: 2026-04-20*  
*Sources: CLAUDE_REBUTTAL_PREP_20260420.md, KIMI_REBUTTAL_ARSENAL_V1_20260420.md, KIMI_REBUTTAL_ARSENAL_V2_STATS_20260420.md, KIMI_REBUTTAL_ARSENAL_V2_METHODS_20260420.md, KIMI_REBUTTAL_ARSENAL_V2_GEN_20260420.md*
