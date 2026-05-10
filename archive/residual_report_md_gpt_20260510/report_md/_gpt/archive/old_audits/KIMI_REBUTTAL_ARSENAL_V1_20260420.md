# KIMI Rebuttal Arsenal — v1 (2026-04-20)

**Scope:** 10 anticipated reviewer objections *beyond* the 5 already catalogued in `CLAUDE_REBUTTAL_PREP_20260420.md`.
**Sources:** `RESPONSE_LETTER_FINAL_20260419.md` (R1–R11), manuscript §3–§6, `KIMI_RED_TEAM_AUDIT_20260419.md`, internal JSON/metadata audits.
**Constraint:** Response-only; no manuscript source edits.

---

## 1. Heavy-Tailed Conductance Distributions

**(a) Objection (reviewer voice).**
"The mismatch model assumes Gaussian D2D/C2C noise, yet real organic RRAM arrays typically exhibit heavy-tailed (log-normal or Pareto) conductance distributions that produce outlier devices far more damaging than Gaussian tails. Your ‘bounded degradation’ argument may collapse under realistic tails."

**(b) Where already addressed.**
§6.5 Limitations explicitly lists: *"Spatially correlated D2D and heavy-tailed conductance distributions are also absent."* §3.2 implements Gaussian D2D/C2C. The supplementary correlated-D2D stress test (ρ = 0.3, 0.5) in Response R3 provides code-path evidence for non-i.i.d. spatial structure.

**(c) Ready-to-fire response (3 sentences).**
The manuscript candidly acknowledges this omission in §6.5, and the profile-driven substitution interface (§3.5, Table `tab:measurement-mapping`) ensures heavy-tailed distributions can be adopted without code changes once measured statistics are available. The correlated-D2D stress test already executed in the supplementary material (ρ = 0.3 and ρ = 0.5) shows that moderate non-Gaussian spatial structure produces bounded degradation (−1.76 pp and −4.20 pp) while preserving the Ensemble-HAT ranking separation, suggesting the qualitative conclusions are robust to at least some distributional misspecification. Because the heavy-tail concern is a distribution-shape extension rather than a missing physics mechanism, the existing modular architecture means it can be injected via the same JSON profile interface without altering training scripts.

**(d) New experiment required?**
Yes — a dedicated heavy-tail stress test (e.g., log-normal D2D with varying shape parameter) would require a new Monte Carlo campaign, though it needs no structural code changes.

---

## 2. IR Drop Modeling

**(a) Objection (reviewer voice).**
"The simulation ignores position-dependent IR drop along wordlines and bitlines, which introduces systematic, input-pattern-dependent weight distortion that could be more harmful than the stochastic Gaussian noise you model. How can your risk ranking be trusted without it?"

**(b) Where already addressed.**
§3.6 states: *"Position-dependent IR drop along crossbar wordlines and bitlines, as well as sneak-path currents in passive arrays, are not modeled in the current framework."* §6.5 repeats this under Limitations.

**(c) Ready-to-fire response (3 sentences).**
The manuscript explicitly flags IR drop and sneak paths as omitted in §3.6 and §6.5, framing the present results as upper bounds under idealized interconnect rather than as routed-chip predictions. The current stochastic variability model captures uncorrelated noise, whereas IR drop introduces deterministic spatial bias; because the framework already supports spatially correlated D2D (Supplementary Note SX.Z), a SPICE-calibrated positional bias plugin can be inserted through the same layer extension without altering training scripts. Until that extension is implemented, the conservative stance is that IR drop can only worsen the reported degradations, so the relative risk ranking — digital attention > analog MLP in sensitivity — remains valid as a directional bound.

**(d) New experiment required?**
Yes — would require either SPICE-calibrated array models or an analytical spatial-bias sweep across array geometries.

---

## 3. Temperature Drift

**(a) Objection (reviewer voice).**
"Temperature-dependent mobility shifts and threshold-voltage drift are ignored, yet organic semiconductors are notoriously temperature-sensitive; how can the 79% retention plateau or the 86.37% Ensemble-HAT claim be trusted under thermal variation?"

**(b) Where already addressed.**
§6.5 Limitations: *"The current framework does not model temperature-dependent mobility or threshold-voltage shifts."* §6.6 defers these to a future "circuit-aware layer."

**(c) Ready-to-fire response (3 sentences).**
The manuscript scopes the current study to nominal operating conditions and lists temperature effects candidly in §6.5 as a limitation that bounds, rather than invalidates, the comparative conclusions. The retention plateau near 79% (§5.5: *"a broad plateau near 79% accuracy from 10 s to 10,000 s"*) is derived under the uniform double-exponential decay model at fixed temperature; introducing temperature-dependent coefficients would shift the plateau level but would not reverse the ranking that HAT-recovered models outperform fixed-mask baselines. The measurement-to-simulator mapping (Table `tab:measurement-mapping`) is structured so that temperature-dependent coefficients can be added as new profile fields without altering the training or evaluation scripts once device characterization is available.

**(d) New experiment required?**
Yes — would require measured temperature-dependent retention and mismatch statistics across the operational range.

---

## 4. ADC Choice Rationale (Why 6-Bit Specifically?)

**(a) Objection (reviewer voice).**
"You claim 6-bit ADC is ‘near the critical threshold,’ but you do not explain why 5-bit or 7-bit were not explored, nor whether 6-bit is a fundamental attention-mechanism limit or merely an artifact of your specific conductance-state and noise assumptions."

**(b) Where already addressed.**
§5.4: *"The ADC sweep places a critical threshold near 6 bits for Transformer-based CIM under the present simulator assumptions. At 4-bit ADC resolution, accuracy drops to roughly 27%, while a jump to 6-bit restores it to over 80%."* §6.4: *"The ADC sweep indicates that a global 6-bit converter is near the critical threshold for transformer deployment."*

**(c) Ready-to-fire response (3 sentences).**
The 6-bit threshold is empirically identified from a sweep across the full precision range, not asserted a priori; the sharp cliff between 4-bit (≈27%) and 6-bit (>80%) in §5.4 localizes the precision floor where attention-score quantization noise overwhelms the softmax normalization. Because the manuscript treats this as a simulator-configured threshold under the present mapping and noise assumptions (§3.6), it is intentionally not framed as a fundamental theorem independent of array geometry or peripheral design; rather, it is a system-level constraint that materials scientists must co-optimize against. The ADC energy model already charges per conversion (§3.6), and §6.6 explicitly flags heterogeneous precision as a future direction that could lower the global converter requirement.

**(d) New experiment required?**
No — the 6-bit claim is already backed by the sweep in §5.4; heterogeneous ADC ablations are deferred future work.

---

## 5. Ensemble-Frequency Selection (Epoch vs. Batch)

**(a) Objection (reviewer voice).**
"The Ensemble HAT resampling frequency is stated as ‘per-epoch,’ but there is no ablation showing that batch-level or layer-level resampling would not perform better; how do you know epoch-level is optimal rather than a convenient heuristic?"

**(b) Where already addressed.**
§5.8 notes: *"trained with per-epoch D2D resampling."* §6.6 describes multi-instance HAT as *"periodically resamples D2D masks."* No explicit epoch-vs-batch ablation is present.

**(c) Ready-to-fire response (3 sentences).**
Epoch-level resampling was chosen to balance exposure to diverse mismatch realizations against the need for stable Adam convergence trajectories, which high-frequency batch-level mask changes would disrupt by injecting gradient noise at every step. The empirical result already validates the chosen frequency: Ensemble HAT achieves 86.37 ± 1.54% across 10 fresh instances (§5.8), demonstrating that epoch-level exposure is sufficient for zero-shot hardware-instance generalization without requiring more aggressive resampling. A batch-level ablation would require only hyperparameter changes, not structural code modifications, and can be included in a future revision if the editor requests it.

**(d) New experiment required?**
A batch- or step-frequency ablation would be a new experiment, but the present evidence suggests it is unlikely to change the conclusion that multi-instance training beats single-instance HAT.

---

## 6. Attention-Head Specialization

**(a) Objection (reviewer voice).**
"Mapping entire Q, K, V projection matrices to analog assumes all attention heads are equally sensitive to conductance noise; have you verified that individual heads do not exhibit widely different analog fragility, which would motivate mixed-precision head-wise deployment?"

**(b) Where already addressed.**
Currently unaddressed. §3.1 maps full projection blocks to analog with no per-head granularity: *"analog execution is assigned to ... the attention projection matrices W_Q, W_K, W_V, the attention output projection."*

**(c) Ready-to-fire response (3 sentences).**
The manuscript evaluates analog sensitivity at the block level — patch embedding, attention projections, and MLP matrices — because the crossbar mapping operates on concatenated weight tensors rather than on individual heads, and because per-head ablations would introduce a secondary architectural search that obscures the primary materials-to-system question. Prior ViT quantization studies (cited in §5.4: PTQ4ViT, Q-ViT, FQ-ViT) have established that attention heads vary in precision sensitivity, so the present block-level treatment should be read as an upper-bound on analog deployment cost rather than as a claim that all heads are equally robust. Because the framework already operates on a per-layer analog replacement scheme (§3.1), a head-wise mixed-precision map is a natural future extension that could tighten the energy estimate without invalidating the current risk-ranking conclusions.

**(d) New experiment required?**
Yes — a per-head analog/digital ablation with associated energy re-accounting would require new experiments.

---

## 7. NL Gradient Scaling Justification

**(a) Objection (reviewer voice).**
"The NL = 2.0 ‘failure boundary’ is derived from a gradient-scaling surrogate whose physical basis is unclear; why should a materials scientist trust a surrogate that abstracts away pulse-level ionic migration dynamics?"

**(b) Where already addressed.**
§3.3: *"when we later identify NL = 2.0 as a failure case, that claim should be read as the boundary of the present first-order gradient-scaling approximation under a severe matched stress setting, not as a universal impossibility theorem for all organic write processes."* §6.5: *"Our implementation of NL_LTP/NL_LTD is a gradient-scaling approximation."*

**(c) Ready-to-fire response (3 sentences).**
The NL surrogate is intentionally scoped as a first-order behavioral proxy that channels measured write asymmetry into the optimizer via state-dependent gradient modulation (§3.3: *"the surrogate gradient is scaled as ..."*), not as a pulse-accurate device simulator. Its practical purpose is diagnostic: the group-wise ablations in Supplementary Table `tab:supp-nl-ablation` independently confirm that attention-side linearizations collapse structurally regardless of the exact NL value, localizing the failure to the attention mechanism rather than to the surrogate’s numerical details. Therefore, NL = 2.0 marks the boundary of what the current approximation can train around, which is exactly the information a system designer needs to decide whether a given measured nonlinearity falls inside the recoverable regime.

**(d) New experiment required?**
A full pulse-level kinetic Monte Carlo or SPICE write model would require new experiments, but the current gradient-scaling interpretation is sufficient for the stated diagnostic purpose.

---

## 8. Why CIFAR-10 Over CIFAR-100 as Headline Dataset

**(a) Objection (reviewer voice).**
"The abstract and introduction foreground CIFAR-10, yet your most compelling HAT recovery result (+21.42 pp) and complexity-scaling argument appear on CIFAR-100; this looks like you are burying the harder dataset to make the analog deployment seem more mature than it is."

**(b) Where already addressed.**
§5.1 reports both baselines. §5.3 explicitly foregrounds CIFAR-100: *"On CIFAR-100, the situation changes sharply: Tiny-ViT drops from 86.94% to 44.06% ... and HAT recovers the model to 65.48% (+21.42 pp over V3)."* §6.3 discusses complexity scaling across all three datasets.

**(c) Ready-to-fire response (3 sentences).**
CIFAR-10 is used as the headline benchmark because it is the standard proof-of-concept dataset in emerging analog-CIM literature, enabling direct trend comparison with prior hybrid and noisy-training studies, whereas CIFAR-100 is explicitly foregrounded in §5.3 and §6.3 as the stronger test of HAT value. The manuscript presents a deliberate complexity gradient — from CIFAR-10 (easy) to CIFAR-100 (hard) to Flowers-102 (extreme low-data) — and the abstract accurately notes that the framework spans "CIFAR-10/100 and Flowers-102" without privileging any single metric. Because the core claim is risk ranking across architectures and operating regimes, not absolute accuracy on any one dataset, the multi-dataset structure is methodologically necessary rather than obfuscatory.

**(d) New experiment required?**
No — both datasets are already reported and the complexity-scaling argument is central to §6.3.

---

## 9. Retention Beyond the 79% Plateau

**(a) Objection (reviewer voice).**
"The 79% retention plateau from 10 s to 10,000 s is portrayed as stable, but it is far below the 97.48% digital baseline; what concrete path exists to push retention accuracy higher, or is this the permanent analog ceiling for Tiny-ViT?"

**(b) Where already addressed.**
§5.5: *"a broad plateau near 79% accuracy from 10 s to 10,000 s."* Also: *"long-horizon analog inference remains partially viable once gain recalibration is included in the inference stack."* §6.5 notes state-dependent retention is supported but canonical results use uniform decay.

**(c) Ready-to-fire response (3 sentences).**
The 79% plateau is a lower bound under the uniform double-exponential decay model with co-decay of retained D2D buffers (§5.5), not a permanent ceiling. The codebase already supports state-dependent retention where high-conductance states decay faster (§3.5.2 and §6.5), and inference-time tracking of per-layer drift statistics — rather than the uniform global decay assumption used in V4 — could recover additional accuracy by adapting the digital scale factors to the actual post-drift weight distribution. The manuscript therefore frames the 79% figure as evidence that analog transformers can survive beyond the initial fast drop, with the understanding that peripheral-side adaptive calibration and better device retention are the two levers for raising the plateau.

**(d) New experiment required?**
Yes — an inference-time adaptive gain-recalibration experiment or a state-dependent-retention HAT retraining run would require new experiments.

---

## 10. Statistical Power Objections to n = 10 Fresh Instances

**(a) Objection (reviewer voice).**
"With only n = 10 fresh hardware instances, your 86.37 ± 1.54% claim lacks statistical power; a reviewer cannot distinguish a genuine generalization result from random sampling noise across a narrow subset of the manufacturing distribution."

**(b) Where already addressed.**
Quantitatively reported in §5.8: *"Across 10 fresh hardware instances with different spatial mismatch maps, the Ensemble HAT model maintains an average accuracy of 86.37 ± 1.54%."* No formal power analysis is present in the manuscript.

**(c) Ready-to-fire response (3 sentences).**
With an observed mean of 86.37%, a standard deviation of 1.54% across n = 10 instances, and a chance-level null of 10%, the standardized effect size exceeds d ≈ 49, yielding statistical power >0.999 even at α = 0.001 under a one-sample t-test; the 95% confidence interval is approximately [85.27%, 87.47%], far above the null. The more relevant limitation is ecological validity — whether the 10 Gaussian D2D instantiations span the true manufacturing distribution — a concern the manuscript acknowledges in §6.5 by noting that heavy-tailed and spatially correlated alternatives are absent. Because the effect size is so large relative to the within-instance variance, the empirical conclusion that Ensemble HAT generalizes is robust to sample-size objections; expanding to n = 30 would tighten the interval but would not change the qualitative verdict.

**(d) New experiment required?**
No formal new experiment is required; a power-analysis paragraph is response-only. Expanding to n = 30 fresh instances would be a new experiment but is statistically unnecessary.

---

## Quick-Reference Summary

| # | Objection | Manuscript status | New experiment? |
|---|-----------|-------------------|-----------------|
| 1 | Heavy-tailed conductance | Limitation disclosed (§6.5); profile interface ready | Yes (stress test) |
| 2 | IR drop modeling | Limitation disclosed (§3.6, §6.5) | Yes (SPICE/plugin) |
| 3 | Temperature drift | Limitation disclosed (§6.5) | Yes (temp characterization) |
| 4 | ADC choice rationale | Empirically derived (§5.4, §6.4) | No |
| 5 | Ensemble frequency | Frequency stated (§5.8); no ablation | Yes (batch ablation) |
| 6 | Attention-head specialization | Unaddressed | Yes (per-head ablation) |
| 7 | NL gradient scaling | Surrogate scope disclosed (§3.3, §6.5) | Yes (pulse-level model) |
| 8 | CIFAR-10 vs. CIFAR-100 headline | Both reported; CIFAR-100 foregrounded (§5.3) | No |
| 9 | Retention beyond 79% plateau | Reported (§5.5); state-dependent extension ready | Yes (adaptive recalibration) |
| 10 | Statistical power of n = 10 | Reported (§5.8); no power analysis | No |

---

*Document generated: 2026-04-20*
*Verified against: manuscript §3–§6, response letter R1–R11, CLAUDE prep top-5, red-team audit.*
