# Simulated Hostile Reviews — NC Submission

> **Deliverable:** Anticipated reviewer personas and pre-written response strategies.
> **Word count:** ~1,500 words.
> **Style:** Realistic reviewer prose — terse, critical, occasionally unfair.

---

## Reviewer A — The Methodologist

**Summary:** The authors propose a simulation framework for organic optoelectronic inference, but the empirical foundation is too thin to support the claims. With toy datasets, tiny sample sizes, and no power analysis, the paper mistakes statistical noise for engineering insight.

**Specific Criticisms:**

1. **Sample size is indefensible.** The entire "fresh-instance" generalization claim rests on n = 10 hardware instances. The authors report 86.37 ± 1.54 % without any power analysis, confidence-interval table, or discussion of what precision is required to distinguish their protocol from chance. With ten observations, the standard error of the standard deviation itself is roughly 35 % of the point estimate; the ±1.54 pp spread could easily be ±2.5 pp in reality. Show me the power analysis, or do not report the interval.

2. **CIFAR-10 is not a serious benchmark.** A 10-class dataset with 32 × 32 images is trivially separable by mid-sized CNNs trained on modern hardware. The fact that the authors can recover ~86 % under noise says more about the dataset than about their simulator. Where is ImageNet? Where is even CIFAR-100 at full resolution? The absence of a large-scale vision task makes the entire "edge vision" framing feel like scope inflation.

3. **No generative or sequence-task evaluation.** The title promises "modern vision tasks," but the experiments stop at image classification. Vision transformers are increasingly deployed for detection, segmentation, and as backbones for multimodal models. If the framework is truly architecture-agnostic, why is there no LLM token-throughput estimate, no CLIP-style contrastive probe, no generative diffusion ablation? The omission suggests the method does not scale.

4. **The CrossSim comparison is statistically hollow.** The authors compare their framework against CrossSim on a 1,000-image subset — less than 20 % of the CIFAR-10 test set — with only a single deterministic run for the clean baseline and three runs under noise. A 14.43 pp gap based on n = 3 is not a "divergence"; it is anecdote dressed up as evidence. The Wilson confidence interval on that subset spans roughly 16 percentage points. This comparison should be removed or massively expanded.

5. **Multiplicity is ignored.** The supplementary figures juxtapose four correlation conditions and multiple pairwise contrasts with no Bonferroni, Tukey, or false-discovery correction. When one runs six contrasts at α = 0.05, the family-wise error rate balloons to 26 %. The authors appear to have cherry-picked the significant pairs and buried the rest.

**Overall Recommendation:** Major Revision.

**Response Strategy:**

1. *We will report the post-hoc power explicitly: the observed coefficient of variation is 1.78 %, the one-sample t against chance yields t(9) = 149.25 (p = 1.4 × 10⁻¹⁶), and the 95 % CI [85.27 %, 87.46 %] is already tighter than many clinical-trial primary endpoints.*

2. *We will reframe CIFAR-10 as a controlled testbed for analog-deployment risk ranking, not as a scale demonstration, and cite §6.6 where ImageNet-scale extrapolation is explicitly scoped as future work.*

3. *We will note that the framework is backbone- and task-agnostic (§3.5) and that CLIP or detection deployment requires only a configuration change, but we will not claim results we do not have.*

4. *We will add the Wilson and t-distribution CIs to the supplementary note, disclose the subset rationale (CrossSim throughput constraints), and soften the quantitative framing to "qualitative divergence" if the editor agrees.*

5. *We will append a multiplicity-correction table: Bonferroni (k = 6) retains standard-vs-ensemble at p < 10⁻¹⁵, Holm-Bonferroni retains i.i.d. vs. ρ = 0.5 at p = 0.009, and we will flag the i.i.d. vs. ρ = 0.3 contrast as a descriptive trend.*

---

## Reviewer B — The Device Physicist

**Summary:** The paper offers a first-order behavioral model of organic optoelectronic compute-in-memory, but the device physics is so heavily abstracted that the results have no predictive value for real hardware. Without SPICE validation, foundry calibration, or measured array data, this is simulation theater.

**Specific Criticisms:**

1. **First-order surrogate is cartoon physics.** The authors reduce organic transistor behavior to a Gaussian noise injection on conductance states and a static retention drift. Real organic devices exhibit hysteresis, temperature-dependent mobility, contact-resistance variation, and history-dependent switching dynamics — none of which appear in the model. A first-order surrogate is not a simplification; it is a different physical system.

2. **No SPICE or circuit-level verification.** The analog readout path is modeled as a quantized matrix-vector product with additive noise. There is no transient simulation of the bitline swing, no parasitic RC extraction, no sense-amplifier offset, no crosstalk. The "6-bit ADC cliff" is purely empirical from the authors' own Python simulator; it could shift by several bits once real capacitive loading and comparator metastability are included. Where is the SPICE deck?

3. **No foundry data, no measured arrays.** The entire paper is a simulation exercise. The authors reference "recent organic array demonstrations" but never compare their conductance distributions, retention tails, or yield statistics against a single measured wafer. The OPECT case study is a literature proxy, not a calibration. Without a feedback loop to fabricated hardware, the framework cannot be validated, only debugged.

4. **Organic devices do not behave like this.** The canonical D2D variability is set to σ = 10 %, yet organic ReRAM and OPECT literature reports spreads from < 1 % to > 20 % depending on dielectric thickness, processing solvent, and encapsulation. The authors sweep 1 % to 20 % but then anchor all conclusions to the 10 % midpoint, which happens to suit their narrative. Worse, the retention model is exponential-decay-with-offset, a textbook approximation that fails in disordered organic semiconductors where dispersive transport produces power-law decay.

5. **The conductance-to-weight mapping is unphysical.** The authors assume linear conductance programming with symmetric up/down updates and no stuck-at-faults. Organic memories typically show highly asymmetric switching, significant cycle-to-cycle variation, and hard failures after fewer than 10⁴ cycles. The "fresh-instance" protocol resamples D2D noise but ignores cycling history entirely, as if each array were virgin silicon rather than a soft organic film.

**Overall Recommendation:** Reject.

**Response Strategy:**

1. *We will restate the paper's explicit positioning as a "simulation-first, first-order behavioral methodology" (Truth Pack §2) that ranks deployment risks under explicit assumptions, not as a tape-out predictor.*

2. *We will add a supplementary note clarifying that SPICE validation is future work and that the ADC cliff is regime-specific; we will not claim the number transfers to a full extracted netlist without further evidence.*

3. *We will cite the measured-data collection pipeline (Truth Pack §9) and note that the framework is designed for iterative calibration once device statistics arrive, but we will not pretend to have data we do not yet possess.*

4. *We will emphasize that the 10 % canonical value sits inside a 1 %–20 % sweep (§5.5) and that the OPECT proxy at 3 % is independently validated in the zero-shot case study (§5.9), so no conclusion hinges on the midpoint alone.*

5. *We will expand §6.5 (Limitations) to flag cycling history and stuck-at-faults explicitly, and we will reframe the conductance model as a best-case baseline that makes the reported accuracy drops conservative rather than optimistic.*

---

## Reviewer C — The ML Systems Person

**Summary:** The authors wrap analog noise injection and hardware-aware training into a custom simulator, but neither idea is novel and the evaluation is too small to matter. CrossSim and AIHWKIT already provide mature, peer-reviewed frameworks for exactly this workflow; the incremental contribution is a dataset-specific training script and a few ablation plots.

**Specific Criticisms:**

1. **Analog noise + training is a solved problem.** The core technical move — injecting device noise during transformer fine-tuning to improve analog robustness — has been demonstrated in ResNet, BERT, and GPT-2 analog deployments since 2020. The authors do not cite the full body of HWA-QAT literature, and their "Ensemble HAT" variant is merely a multi-seed average with resampled noise, a standard bagging technique applied to conductance maps. There is no new algorithm here.

2. **CrossSim already does this, and better.** Sandia's CrossSim simulator supports SPICE-calibrated device models, full analog-digital mixed-signal cosimulation, and validated foundry tape-outs. The authors' comparison against CrossSim on a 1,000-image subset with n = 3 runs is not a rigorous benchmark; it is an admission that their own framework is too immature to handle real device cards. If CrossSim exists, why does the world need another Python wrapper around PyTorch?

3. **AIHWKIT is the established baseline.** IBM's Analog AI Hardware Kit provides programmable noise models, tile-level parallelism, and demonstrated inference on real PCM and ReRAM arrays. The authors report 90.08 ± 0.21 % on an AIHWKIT benchmark but do not explain why anyone should abandon a platform with silicon validation for a simulator with none.

4. **No chip, no demo, no system.** The paper stops at simulation. There is no FPGA emulator, no taped-out test chip, no energy breakdown against a digital baseline measured in silicon, no end-to-end latency estimate that accounts for A/D conversion, row driver settling, or control logic. A systems paper without a system is an methods paper without a method.

5. **Tiny-ViT on CIFAR-10 is not a real benchmark.** A 5 M-parameter model fine-tuned from ImageNet to 32 × 32 images is a distillation artifact, not a deployment target. The transformer community evaluates on ImageNet-1K at minimum; edge-device papers use MobileNet-V3 or EfficientNet-Lite on at least 224 × 224 inputs. The authors' claim that their conclusions generalize to "edge vision" is unsupported by the evidence presented.

**Overall Recommendation:** Minor Revision (but barely).

**Response Strategy:**

1. *We will add a dedicated related-work paragraph distinguishing HWA-QAT (noise-aware quantization) from our profile-driven *organic-specific* behavioral stack, and we will cite the HWA-QAT lineage explicitly rather than leaving the gap for the reviewer to fill.*

2. *We will reframe the CrossSim comparison as a *sensitivity-to-mapping* sanity check, not a framework superiority claim, and we will move the discussion to supplementary material if the editor prefers to de-emphasize it.*

3. *We will clarify that AIHWKIT is a complementary benchmark (§5.1) used to validate numerical equivalence, not a competitor to be displaced, and that our contribution is the organic-specific profile interface, not a universal tile simulator.*

4. *We will add an energy-latency projection table (already computed in JSON) to the supplementary material and explicitly scope silicon demonstration as post-submission work in §6.6, without overstating current status.*

5. *We will defend Tiny-ViT-5M as an ImageNet-pre-trained, deployment-oriented edge transformer chosen for area/energy fit, but we will also commit to a ViT-Base or ImageNet-scale ablation in revision if the editor requests scale validation.*

---

*End of simulated reviews. These personas are intended for internal rebuttal rehearsal and should not be shared outside the author team.*
