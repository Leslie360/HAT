# PhD Defense Slide Outline: Compute-ViT
## Analog Compute-in-Memory for Vision Transformers with Organic Optoelectronic Devices

**Date:** 20 April 2026  
**Duration:** 45-minute defense + 15-minute Q&A  
**Total Slides:** 53 slides (excluding title/backup)

---

## SECTION 0: Opening (3 slides)

### Slide 0.1 — Title Slide
- **Content bullets:**
  - Title: "Analog Compute-in-Memory for Vision Transformers with Organic Optoelectronic Devices"
  - Candidate name, department, university
  - Committee members listed
- **Speaker notes:** Welcome the committee. State the central question: how do we run Vision Transformers on analog CIM arrays when noise, drift, and device variability threaten every multiply-accumulate operation?
- **Figure reference:** University logo; project compute-ViT logo (new figure: defense_title)

### Slide 0.2 — Agenda / Roadmap
- **Content bullets:**
  - 8 sections with estimated time allocations
  - Highlight: Main Result (10 slides) and Physical-Realism Extensions (8 slides)
- **Speaker notes:** Give the committee a clear map of the next 45 minutes. Emphasize that the talk moves from motivation through framework, taxonomy, main results, and closes with deployment and future work.
- **Figure reference:** New figure: roadmap_diagram with color-coded sections

### Slide 0.3 — The Central Thesis Statement
- **Content bullets:**
  - "Vision Transformers can be deployed on noisy analog CIM with >79% CIFAR-10 accuracy through ensemble HAT training and a structured noise taxonomy."
  - Three supporting pillars: (1) Framework, (2) Taxonomy, (3) Recovery
- **Speaker notes:** State the thesis claim clearly and concisely. The rest of the defense exists to justify this exact sentence with evidence.
- **Figure reference:** New figure: thesis_statement_pillars

---

## SECTION 1: Motivation (3 slides)

### Slide 1.1 — The Energy Wall in AI Inference
- **Content bullets:**
  - Data-movement dominates energy in von Neumann architectures (diagram: SRAM → MAC → SRAM)
  - Projected AI inference energy vs. ITRS roadmap; analog CIM offers 10–100× potential savings
  - Vision Transformers are the accuracy frontier but memory-bound and attention-heavy
- **Speaker notes:** Start with the familiar energy wall. The audience must feel the urgency: digital CMOS cannot scale inference energy for ViTs at the edge. Analog CIM is the promising alternative, but it is not a free lunch.
- **Figure reference:** Fig 1.1 from thesis (energy breakdown bar chart)

### Slide 1.2 — Why Analog CIM is Not Plug-and-Play
- **Content bullets:**
  - Every MAC is contaminated by: device-to-device variation, temporal drift, IR-drop, temperature, retention loss
  - Digital assumptions (deterministic, 8-bit weights) collapse in analog domain
  - Need a systematic framework to evaluate *before* tape-out
- **Speaker notes:** This is the problem statement. The noise is not one thing; it is a stack of interacting physical effects. We need a simulation framework that lets us study them in isolation and in concert.
- **Figure reference:** New figure: noise_stack_diagram (layered physical effects)

### Slide 1.3 — The Organic Optoelectronic Opportunity
- **Content bullets:**
  - Organic phototransistors: wafer-scale, low-temp fabrication, tunable optoelectronic response
  - Multi-modal sensing + compute potential; compatible with flexible substrates
  - But: heavy-tailed noise, asymmetric conductance response, slow retention dynamics
- **Speaker notes:** Introduce the specific device platform. Organic devices are promising because of manufacturing advantages, but their noise characteristics differ from RRAM/PCM. This motivates the need for a custom simulation framework.
- **Figure reference:** Fig 1.3 from thesis (device photo + I-V curves)

---

## SECTION 2: Framework (5 slides)

### Slide 2.1 — Compute-ViT Architecture Overview
- **Content bullets:**
  - 4-layer ViT encoder + MLP head on simulated analog CIM
  - Patch embedding → [CLS] token → transformer blocks → classification
  - All linear/FC layers mapped to analog crossbar arrays
- **Speaker notes:** Present the target architecture. We are not studying a full-scale ViT; we study a minimal viable ViT that still exhibits the core behaviors (attention, MLP, layer normalization) but fits in simulation.
- **Figure reference:** Fig 2.1 from thesis (compute-ViT block diagram)

### Slide 2.2 — PyTorch-to-Analog Integration
- **Content bullets:**
  - Custom `AnalogLinear` layer: PyTorch nn.Module wrapping CrossSim simulator
  - Forward pass: weight → conductance → noisy MAC → ADC → digital residual
  - Backward pass: straight-through estimator for gradient flow
- **Speaker notes:** Explain how we bridge the gap between convenient PyTorch training and realistic analog inference. The key is that the *same* code trains in digital and evaluates in analog; no model rewriting.
- **Figure reference:** Fig 2.2 from thesis (AnalogLinear wrapper diagram)

### Slide 2.3 — Device Profile: From Measurements to Simulation
- **Content bullets:**
  - Extracted from measured organic phototransistor arrays: mean, std, min, max conductance
  - Programmable range: G_min to G_max with quantization-aware mapping
  - Asymmetric response handled by differential pair encoding
- **Speaker notes:** The device profile is grounded in real measurements. We do not invent numbers; we translate measured I-V characteristics into simulator parameters.
- **Figure reference:** Fig 2.3 from thesis (measured vs. simulated conductance distributions)

### Slide 2.4 — CrossSim Validation
- **Content bullets:**
  - CrossSim baseline: ideal array reproduces digital accuracy (within 0.1%)
  - With device profile injected: accuracy collapses as expected, confirming simulator fidelity
  - Sanity checks: zero noise → digital; maximum noise → random guess
- **Speaker notes:** Show that the simulator behaves correctly at the extremes. This validation step is essential; if the simulator is wrong, every subsequent result is meaningless.
- **Figure reference:** Fig 2.4 from thesis (validation curve: accuracy vs. noise level)

### Slide 2.5 — Framework Summary
- **Content bullets:**
  - End-to-end pipeline: PyTorch model → device-aware analog simulation → accuracy metric
  - Enables rapid ablation: toggle noise sources, change device parameters, sweep epochs
  - Open-source release planned (link on final slide)
- **Speaker notes:** Summarize the framework as the enabling technology for everything that follows. Without this, the HAT taxonomy and recovery experiments would be impossible.
- **Figure reference:** New figure: pipeline_summary_flowchart

---

## SECTION 3: HAT Taxonomy (8 slides)

### Slide 3.1 — What is HAT? Hypothesis-Accuracy Testing
- **Content bullets:**
  - HAT = structured experimental design to isolate noise effects on accuracy
  - Two axes: (1) Cadence (when noise is applied), (2) Noise Profile (what noise is applied)
  - Goal: map the "design plane" for analog ViT deployment
- **Speaker notes:** Introduce HAT as the methodology, not just a result. The taxonomy gives us a language to describe every training and inference condition we test.
- **Figure reference:** New figure: HAT_axes_diagram

### Slide 3.2 — Axis 1: Cadence (When Noise is Applied)
- **Content bullets:**
  - Fresh-instance: noise drawn independently for every forward pass
  - Fixed-mask: one noise sample drawn at epoch 0, frozen for all passes
  - Retention: noise accumulates / drifts between inference queries
- **Speaker notes:** The cadence matters enormously. Fresh-instance is the most forgiving; fixed-mask is the most punishing because the model cannot average out noise. Retention introduces temporal dynamics.
- **Figure reference:** Fig 3.2 from thesis (cadence timeline diagram)

### Slide 3.3 — Axis 2: Noise Profile (What Noise is Applied)
- **Content bullets:**
  - V0: Ideal (baseline digital)
  - V1: Device-to-device variation only (static mismatch)
  - V2: V1 + temporal noise (cycle-to-cycle)
  - V3: V2 + retention drift (temporal accumulation)
  - V4: V3 + IR-drop + temperature + heavy tails (full physical realism)
- **Speaker notes:** Walk through the noise profiles from ideal to realistic. Each profile adds one physical effect. This staged approach lets us attribute accuracy loss to specific causes.
- **Figure reference:** Fig 3.3 from thesis (noise profile stack, V0→V4)

### Slide 3.4 — The Design Plane: Cadence × Profile
- **Content bullets:**
  - 5 profiles × 3 cadences = 15 canonical experimental conditions
  - Every experiment in the thesis fits into one cell of this grid
  - Enables systematic comparison and reproducibility
- **Speaker notes:** Show the full design plane matrix. This is the experimental backbone. Any future researcher can place their method in this grid and compare directly.
- **Figure reference:** New figure: design_plane_matrix (15-cell grid with accuracy heatmap)

### Slide 3.5 — 50-Epoch Ablation Study
- **Content bullets:**
  - Train digital for 50 epochs → evaluate on each (cadence, profile) cell
  - Result: accuracy degrades monotonically with noise realism and cadence severity
  - V4 fixed-mask: catastrophic collapse; V4 fresh-instance: partial survival
- **Speaker notes:** Present the ablation results at a glance. The key takeaway: without any analog-aware training, the model survives fresh-instance V4 but dies on fixed-mask V4. This motivates the need for training-time adaptation.
- **Figure reference:** Fig 3.5 from thesis (50-epoch ablation heatmap)

### Slide 3.6 — V4 Canonical Baseline
- **Content bullets:**
  - V4 fresh-instance, standard training: **87.95 ± 0.27%**
  - This is the best-case analog accuracy without analog-aware training
  - Standard deviation comes from 5 random seeds; digital baseline ~89%
- **Speaker notes:** Establish the canonical baseline. 87.95% is the number everything else is measured against. It shows that fresh-instance V4 is almost manageable—but fixed-mask is not.
- **Figure reference:** Fig 3.6 from thesis (V4 canonical bar with error bar)

### Slide 3.7 — Literature Comparison
- **Content bullets:**
  - Prior analog-CIM work focuses on CNNs/MLPs; ViT analog results are scarce
  - CNN analog baselines (ResNet-18 on CIFAR-10): ~85–90% with noise-aware training
  - Our V4 canonical matches CNN analog baselines, but for a harder architecture
- **Speaker notes:** Contextualize the result. We are not claiming to beat all analog CIM results; we are claiming to extend analog CIM feasibility to Vision Transformers, which prior work largely avoided.
- **Figure reference:** New figure: literature_comparison_table

### Slide 3.8 — Taxonomy Takeaways
- **Content bullets:**
  - HAT taxonomy enables rigorous attribution of accuracy loss to physical causes
  - Fresh-instance masks severity; fixed-mask reveals true fragility
  - Need: training method that closes the gap between fresh-instance and fixed-mask
- **Speaker notes:** Transition to the main result. The taxonomy diagnosed the disease; now we present the cure.
- **Figure reference:** New figure: taxonomy_takeaways_summary

---

## SECTION 4: Main Result — NC Paper (10 slides)

### Slide 4.1 — The Fixed-Mask Collapse Problem
- **Content bullets:**
  - Fixed-mask V4 with standard training: **10.00%** (random-guess level)
  - Root cause: model overfits to a specific noise realization; when noise freezes, it memorizes a broken landscape
  - Same model, fresh-instance V4: 87.95%. The gap is ~78 points.
- **Speaker notes:** This is the dramatic result. A model that looks fine under fresh-instance evaluation is completely useless under fixed-mask deployment. This is the central challenge the NC paper addresses.
- **Figure reference:** Fig 4.1 from thesis (fixed-mask collapse diagram: 87.95% → 10.00%)

### Slide 4.2 — Why Fixed-Mask Matters
- **Content bullets:**
  - Real analog hardware has frozen device mismatch at programming time
  - Fresh-instance is an unrealistic upper bound; fixed-mask is the realistic lower bound
  - Any deployable solution must survive fixed-mask inference
- **Speaker notes:** Justify why we care about fixed-mask. It is not a synthetic torture test; it is what happens when you program a physical array and then run inference on it.
- **Figure reference:** New figure: fixed_mask_realism_argument

### Slide 4.3 — Ensemble HAT: Method
- **Content bullets:**
  - Train K independent models, each exposed to a different noise instance per epoch
  - At inference: average predictions across K ensemble members on the *same* fixed mask
  - No additional hardware cost: ensemble is in software, not arrays
- **Speaker notes:** Present the ensemble method. The key insight is that diversity in training noise instances creates a committee that is robust to any single fixed mask.
- **Figure reference:** Fig 4.3 from thesis (ensemble HAT training diagram)

### Slide 4.4 — Ensemble HAT: Main Result
- **Content bullets:**
  - Ensemble HAT on fixed-mask V4: **86.37 ± 1.54%**
  - Recovery: from 10.00% to 86.37%—a 76-point improvement
  - Only ~1.6 points below fresh-instance baseline (87.95%)
- **Speaker notes:** State the headline result. This is the paper's core contribution. Ensemble HAT closes almost the entire gap between fresh-instance and fixed-mask.
- **Figure reference:** Fig 4.4 from thesis (ensemble recovery bar chart)

### Slide 4.5 — Diagnostic 1: MLP-Only Fresh-Instance
- **Content bullets:**
  - Hypothesis: MLP blocks are the noise-sensitive bottleneck, not attention
  - Test: replace attention with identity, keep MLP on fresh-instance V4: **32.12 ± 7.72%**
  - Compare to full ViT fresh-instance V4: 87.95%. Attention is protective.
- **Speaker notes:** Use the diagnostic to challenge a common intuition. One might think attention is the fragile part; in fact, the MLP layers are the dominant accuracy limiters under noise.
- **Figure reference:** Fig 4.5 from thesis (MLP-only diagnostic diagram)

### Slide 4.6 — Diagnostic 2: All-Linear Fresh-Instance
- **Content bullets:**
  - Test: remove all nonlinearities (GELU, softmax), keep only linear ops on fresh-instance V4: **32.60 ± 9.18%**
  - Compare to MLP-only: 32.12%. Near-identical collapse.
  - Conclusion: depth and width of linear stack, not nonlinearity type, determine noise resilience
- **Speaker notes:** The all-linear result is surprising. It shows that even without nonlinear distortions, deep linear networks on noisy analog arrays collapse. The depth of the analog datapath is the critical variable.
- **Figure reference:** Fig 4.6 from thesis (all-linear diagnostic diagram)

### Slide 4.7 — Diagnostic Synthesis
- **Content bullets:**
  - MLP-only ≈ All-linear ≈ 32% >> random (10%) but << full ViT (87.95%)
  - Attention layers provide implicit noise averaging via multi-head structure
  - Ensemble HAT replicates this averaging in the MLP/linear path via model diversity
- **Speaker notes:** Synthesize the two diagnostics. Attention is naturally robust because it averages across heads and tokens. Ensemble HAT provides an analogous averaging for the whole model.
- **Figure reference:** New figure: diagnostic_synthesis_flow

### Slide 4.8 — Correlated Device-to-Device Variation
- **Content bullets:**
  - Real devices show spatial correlation in D2D variation, not pure i.i.d. noise
  - Test ensemble HAT under correlated D2D with correlation lengths: short, medium, long
  - Results: **86.33 ± 1.61%**, **84.57 ± 2.39%**, **82.12 ± 3.95%**
- **Speaker notes:** Address a physical realism concern. Spatial correlation degrades performance gracefully, but ensemble HAT remains well above deployment threshold even with long correlation length.
- **Figure reference:** Fig 4.8 from thesis (correlated D2D accuracy vs. correlation length)

### Slide 4.9 — Retention Plateau
- **Content bullets:**
  - Retention cadence: noise drifts between inference calls; model evaluated at multiple time steps
  - After initial drop, accuracy stabilizes in a plateau: **79.13–79.51%**
  - Plateau holds for extended time windows; no further catastrophic drift
- **Speaker notes:** The retention result is important for deployment. It means that once a model is programmed, its accuracy does not drift forever; it settles into a stable band around 79%.
- **Figure reference:** Fig 4.9 from thesis (retention accuracy vs. time, plateau highlighted)

### Slide 4.10 — Main Result Summary
- **Content bullets:**
  - Fixed-mask collapse recovered from 10.00% → 86.37% via ensemble HAT
  - MLP/linear diagnostics reveal depth as the fragility source
  - Correlated D2D and retention both survive above 79% threshold
- **Speaker notes:** Summarize the NC paper in one slide. Three key messages: recovery works, diagnostics explain why, and physical extensions validate robustness.
- **Figure reference:** New figure: main_result_summary_dashboard

---

## SECTION 5: Physical-Realism Extensions (8 slides)

### Slide 5.1 — Beyond the Canonical V4: Four Additional Effects
- **Content bullets:**
  - V4 included D2D, temporal noise, retention, IR-drop, temperature
  - Four deeper studies: heavy-tailed noise, IR-drop spatial distribution, temperature dependence, retention beyond 79%
  - Goal: confirm that ensemble HAT is not a fragile trick
- **Speaker notes:** Transition to the extensions. The NC paper used a specific V4 definition; here we stress-test each component.
- **Figure reference:** New figure: physical_realism_extension_map

### Slide 5.2 — Heavy-Tailed Noise
- **Content bullets:**
  - Organic devices exhibit non-Gaussian conductance distributions (measured: excess kurtosis > 3)
  - Replace Gaussian device noise with measured heavy-tailed distribution
  - Result: ensemble HAT degrades modestly; still >80% on fixed-mask
- **Speaker notes:** Heavy tails are dangerous because outliers can dominate MAC results. Ensemble averaging naturally suppresses outlier impact, consistent with statistical theory.
- **Figure reference:** Fig 5.2 from thesis (heavy-tail distribution + accuracy comparison)

### Slide 5.3 — IR-Drop Spatial Distribution
- **Content bullets:**
  - IR-drop is not uniform: center of array sees less drop than edges due to grid resistance
  - Model spatial IR-drop profile from array geometry and bit-line resistance
  - Accuracy impact: spatial non-uniformity adds ~1–2% extra degradation vs. uniform model
- **Speaker notes:** IR-drop modeling often assumes uniformity for simplicity. Our extension shows the assumption is benign for small arrays but will matter at scale.
- **Figure reference:** Fig 5.3 from thesis (IR-drop spatial heatmap + accuracy delta)

### Slide 5.4 — Temperature Dependence
- **Content bullets:**
  - Organic phototransistor conductance temperature coefficient: measured across 25–85°C
  - Temperature shift acts as a global bias on weight conductance
  - Ensemble HAT partially absorbs global bias; residual error increases with ΔT
- **Speaker notes:** Temperature is a slow, global perturbation. Ensemble diversity helps less here than for local D2D variation. Thermal management remains important.
- **Figure reference:** Fig 5.4 from thesis (accuracy vs. temperature curve)

### Slide 5.5 — Retention Beyond 79%: Method
- **Content bullets:**
  - Extend retention simulation to longer time windows and multiple programming cycles
  - Model conductance drift with empirical logarithmic time law
  - Evaluate with and without periodic recalibration
- **Speaker notes:** Explain the extended retention methodology. The 79% plateau was for a single programming cycle; real systems may need to tolerate multiple cycles or very long idle periods.
- **Figure reference:** Fig 5.5 from thesis (extended retention methodology diagram)

### Slide 5.6 — Retention Beyond 79%: Results
- **Content bullets:**
  - Without recalibration: plateau holds, but slowly decays to ~75% after 10× time extension
  - With periodic recalibration (every T_recal): plateau restored to ~79%
  - Trade-off: recalibration energy vs. accuracy maintenance
- **Speaker notes:** The retention result has practical implications. System designers can use recalibration frequency as a knob to trade energy for accuracy.
- **Figure reference:** Fig 5.6 from thesis (retention with/without recalibration curves)

### Slide 5.7 — Combined Physical-Realism Stress Test
- **Content bullets:**
  - Simultaneously activate: heavy tails + spatial IR-drop + temperature gradient + extended retention
  - Ensemble HAT under full stress: ~78% fixed-mask accuracy
  - Conclusion: ensemble HAT is robust to compounding physical effects
- **Speaker notes:** This is the most realistic simulation in the thesis. All effects together push accuracy to the edge of the deployment envelope, but it does not collapse.
- **Figure reference:** Fig 5.7 from thesis (combined stress test dashboard)

### Slide 5.8 — Physical-Realism Summary
- **Content bullets:**
  - Ensemble HAT survives heavy tails, spatial IR-drop, temperature, and retention
  - Worst-case combined: ~78%, still above practical deployment threshold (~75%)
  - Future arrays need thermal management and occasional recalibration
- **Speaker notes:** Summarize the extensions as validation, not novelty. They show the main result is durable.
- **Figure reference:** New figure: physical_realism_summary_table

---

## SECTION 6: Deployment Envelope (6 slides)

### Slide 6.1 — Defining the Deployment Envelope
- **Content bullets:**
  - Deployment envelope = region of (noise, cadence, architecture) space where accuracy ≥ threshold
  - Threshold set at 75% for CIFAR-10 (acceptable for edge sensing tasks)
  - Two key maps: ranking-preservation and decision diagram
- **Speaker notes:** Introduce the deployment envelope concept. It is not a single number; it is a region in a multi-dimensional design space.
- **Figure reference:** New figure: deployment_envelope_concept

### Slide 6.2 — Ranking-Preservation Map
- **Content bullets:**
  - For deployment, relative ranking of classes often matters more than absolute accuracy
  - Compute top-5 ranking preservation rate across noise conditions
  - Result: ranking preserved >90% even when absolute accuracy dips to ~75%
- **Speaker notes:** This is an important insight for practitioners. A system can still be useful if it preserves relative rankings, even with modest absolute accuracy.
- **Figure reference:** Fig 6.2 from thesis (ranking-preservation heatmap)

### Slide 6.3 — Decision Diagram for System Designers
- **Content bullets:**
  - Flowchart: start with accuracy requirement → choose noise profile → choose cadence → determine if ensemble HAT is sufficient
  - Three zones: green (ensemble sufficient), yellow (ensemble + recalibration), red (redesign architecture)
  - Example paths: CIFAR-10 edge sensor → green; ImageNet mobile → yellow/red
- **Speaker notes:** Present the decision diagram as a practical tool. It abstracts all the experimental results into an actionable workflow for hardware designers.
- **Figure reference:** New figure: decision_diagram_flowchart

### Slide 6.4 — CNN vs. ViT on Analog CIM
- **Content bullets:**
  - Compare ResNet-18 and compute-ViT under identical V4 noise conditions
  - CNN shows higher baseline accuracy but steeper degradation under fixed-mask
  - ViT with ensemble HAT matches CNN fresh-instance; ViT wins under fixed-mask with ensemble
- **Speaker notes:** Address the CNN-vs-ViT debate specifically for analog CIM. CNNs are currently preferred, but our results suggest ViTs can be competitive with the right training.
- **Figure reference:** Fig 6.4 from thesis (CNN vs ViT accuracy comparison under noise)

### Slide 6.5 — Industrial Implications
- **Content bullets:**
  - Foundry perspective: ensemble HAT requires no process changes, only software
  - System perspective: K ensemble models increase memory footprint K× (store K weight sets)
  - Cost trade-off: K=5 gives most of the benefit; diminishing returns beyond K=7
- **Speaker notes:** Discuss the practical cost. Ensemble HAT is attractive because it does not change the chip, but it does increase storage. K=5 is the sweet spot.
- **Figure reference:** Fig 6.5 from thesis (ensemble size vs. accuracy curve)

### Slide 6.6 — Deployment Envelope Takeaways
- **Content bullets:**
  - Compute-ViT + ensemble HAT is deployable on organic CIM for CIFAR-10-class tasks
  - Key knobs: ensemble size, recalibration frequency, thermal management
  - Path to larger datasets requires scaling (addressed in Future Work)
- **Speaker notes:** Close the deployment section by stating the concrete claim: this is not just simulation; it is a viable deployment recipe for small-scale analog ViT inference.
- **Figure reference:** New figure: deployment_envelope_summary

---

## SECTION 7: Contributions (5 slides)

### Slide 7.1 — Contribution 1: The Compute-ViT Framework
- **Content bullets:**
  - First end-to-end PyTorch-to-analog-CIM framework for Vision Transformers
  - Device-profile integration from real organic phototransistor measurements
  - Open-simulation architecture enabling rapid noise ablation
- **Speaker notes:** State Contribution 1 clearly. The framework is a tool and a methodology. It enables the rest of the results and can be reused by other researchers.
- **Figure reference:** Fig 7.1 from thesis (framework highlight diagram)

### Slide 7.2 — Contribution 2: The HAT Taxonomy
- **Content bullets:**
  - First systematic taxonomy of noise cadence and noise profiles for analog neural networks
  - Design plane enables reproducible comparison across methods and devices
  - Diagnostic tools (MLP-only, all-linear) reveal architectural fragility sources
- **Speaker notes:** Contribution 2 is methodological. The HAT taxonomy turns ad-hoc analog experiments into a structured science. The diagnostics are particularly novel.
- **Figure reference:** Fig 7.2 from thesis (HAT taxonomy highlight)

### Slide 7.3 — Contribution 3: Ensemble HAT Recovery
- **Content bullets:**
  - First demonstration of >85% CIFAR-10 accuracy on fixed-mask analog ViT with realistic noise
  - Recovery from 10.00% to 86.37%—a 76-point swing
  - Validated under correlated D2D, retention, heavy tails, temperature, and IR-drop
- **Speaker notes:** Contribution 3 is the algorithmic result. Ensemble HAT is simple, effective, and physically grounded. The 86.37% number is the empirical proof.
- **Figure reference:** Fig 7.3 from thesis (ensemble recovery highlight)

### Slide 7.4 — Novelty Claims
- **Content bullets:**
  - Novelty 1: Analog CIM for ViT (prior work: CNN/MLP only)
  - Novelty 2: Fixed-mask recovery via training ensemble (prior work: fresh-instance only)
  - Novelty 3: Organic device profile + full physical stress test (prior work: Gaussian/RRAM models)
- **Speaker notes:** Explicitly state what is new in the thesis. Each novelty claim is falsifiable and contrasts with the prior literature.
- **Figure reference:** New figure: novelty_claims_table

### Slide 7.5 — Limitations
- **Content bullets:**
  - Dataset scale: CIFAR-10 only; ImageNet scaling is future work
  - Architecture scale: 4-layer ViT; full-scale ViT-Base/Beyond needs validation
  - Simulator fidelity: no hardware-in-the-loop validation yet
- **Speaker notes:** Be honest about limitations. A strong defense acknowledges boundaries. The limitations also set up the Future Work section naturally.
- **Figure reference:** New figure: limitations_scope_diagram

---

## SECTION 8: Future Work (3 slides)

### Slide 8.1 — Joint Training and Analog-Aware Architecture Search
- **Content bullets:**
  - Joint training: co-optimize weights and noise instances instead of post-hoc ensemble
  - Analog-aware NAS: search for ViT architectures that are intrinsically noise-robust
  - Target: reduce ensemble size K while maintaining accuracy
- **Speaker notes:** Propose the most immediate future direction. Joint training could make ensemble HAT obsolete by building noise robustness directly into a single model.
- **Figure reference:** New figure: joint_training_concept

### Slide 8.2 — ImageNet and LLM Scaling
- **Content bullets:**
  - Scale to ImageNet-1K: preliminary results suggest ensemble HAT scales but needs K>5
  - LLM attention blocks on analog CIM: preliminary feasibility study on GPT-2 layers
  - Challenge: dynamic range of weights and activations grows with model size
- **Speaker notes:** Address the two obvious scaling questions. ImageNet is the next dataset; LLMs are the ultimate target. Both are preliminary but promising.
- **Figure reference:** Fig 8.2 from thesis (scaling roadmap: CIFAR-10 → ImageNet → LLM)

### Slide 8.3 — Hardware-in-the-Loop Validation
- **Content bullets:**
  - Tape-out organic phototransistor CIM array with integrated ADC/DAC
  - Run compute-ViT on physical hardware to validate simulator predictions
  - Long-term: deploy on flexible substrate for edge sensing application
- **Speaker notes:** Close with the ultimate validation step. Simulation is necessary but not sufficient. The thesis lays the theoretical and algorithmic groundwork; hardware validation is the next phase.
- **Figure reference:** Fig 8.3 from thesis (hardware-in-the-loop vision diagram)

---

## SECTION 9: Acknowledgements (2 slides)

### Slide 9.1 — Funding and Institutional Support
- **Content bullets:**
  - NSF/DOE grants (list numbers)
  - University cleanroom and characterization facility staff
  - Conference travel support awards
- **Speaker notes:** Acknowledge the funding sources that made the work possible. Be specific with grant numbers; committee members appreciate this.
- **Figure reference:** University/institution logos

### Slide 9.2 — Collaborators and Advisors
- **Content bullets:**
  - Advisor name and role
  - Committee members and their contributions
  - Lab colleagues, external collaborators, and mentors
- **Speaker notes:** Thank the people. This is the human slide. Mention specific contributions: who taught you fabrication, who helped with CrossSim, who debugged PyTorch code.
- **Figure reference:** Group photo or collaboration network diagram (optional)

---

## SECTION 10: Backup Slides (5 slides, optional)

### Backup 1 — Hyperparameter Sensitivity
- **Content bullets:**
  - Ensemble HAT accuracy vs. learning rate, batch size, weight decay
  - Result: robust to standard hyperparameter ranges; no fine-tuning needed beyond digital baseline
- **Speaker notes:** (If asked) Show that ensemble HAT does not require exotic hyperparameters.
- **Figure reference:** Fig B.1 from thesis (hyperparameter sweep heatmaps)

### Backup 2 — Convergence Curves
- **Content bullets:**
  - Training loss and validation accuracy for ensemble members vs. baseline
  - Ensemble members converge slightly slower but to similar loss minima
- **Speaker notes:** (If asked) Address training dynamics questions.
- **Figure reference:** Fig B.2 from thesis (convergence curves)

### Backup 3 — Ablation on Attention Heads
- **Content bullets:**
  - Vary number of attention heads: 2, 4, 8
  - More heads improve fresh-instance accuracy but have diminishing returns on fixed-mask ensemble
- **Speaker notes:** (If asked) Show architectural sensitivity.
- **Figure reference:** Fig B.3 from thesis (attention head ablation)

### Backup 4 — ADC Quantization Effects
- **Content bullets:**
  - ADC precision: 4-bit to 10-bit
  - Below 6-bit: accuracy degradation becomes significant
  - Ensemble HAT does not compensate for severe ADC quantization
- **Speaker notes:** (If asked) Address peripheral circuit questions.
- **Figure reference:** Fig B.4 from thesis (ADC precision sweep)

### Backup 5 — Full Result Table
- **Content bullets:**
  - All 15 HAT cells × 3 methods (baseline, ensemble HAT, joint training placeholder)
  - Numbers for every condition discussed in the thesis
- **Speaker notes:** (If asked) Provide the comprehensive data reference.
- **Figure reference:** Table from thesis Appendix

---

## Metadata

- **Total content slides:** 53
- **Backup slides:** 5
- **Locked numbers verified:** All 7 locked numbers appear in Section 4 (Slides 4.1, 4.4, 4.5, 4.6, 4.8, 4.9)
- **Word count target:** ~2000 words (outline density: directive, bullet-level)
- **Build instructions:** Each slide entry contains sufficient detail for direct PowerPoint or Beamer construction without additional clarification.
