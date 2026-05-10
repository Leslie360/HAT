<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# Citation Graph Forecast: *Profile-Driven Hardware Simulation for Organic Optoelectronic Edge Vision*

**Date:** 2026-04-21
**Forecast Horizon:** 6 / 12 / 24 months (October 2026 – April 2028)
**Base Case Assumption:** Nature Communications (NC) accepted after one major revision; arXiv preprint posted within 30 days of this forecast; code and device-profile bundles released on Zenodo/GitHub concurrently; at least one invited talk at a major venue (IEDM / MLCAD / NeurIPS workshop) within 12 months.

---

## Executive Summary

This paper occupies a narrow but high-value niche: it is the first system-level behavioral simulator to connect *literature-derived organic optoelectronic device metrics* to *task-level Vision Transformer accuracy* under mixed-signal deployment. The two most citation-worthy assets are **(a)** the Ensemble HAT training protocol (epoch-level D2D resampling, 86.37 ± 1.54 % fresh-instance accuracy) and **(b)** the negative-result boundary around severe write nonlinearity (~30 % ceiling under first-order surrogates). Both are reusable by communities that do not otherwise overlap: analog-CIM simulator builders, robust-training researchers, edge-ViT engineers, organic device physicists, and methodology scholars.

Our base-case forecast projects **8–15 citations at 6 months, 25–40 at 12 months, and 60–95 at 24 months**. The upside case (rapid NC acceptance + press amplification + code adoption) could push the 24-month tally above 140. The downside case (NC rejection + delayed code release + field pivot to digital-CIM) could suppress it below 30.

---

## 1. Who Will Cite Us? — Six Citation Communities

### 1.1 Analog CIM Simulation Frameworks (CrossSim v2, AIHWKIT v2, New Organic Simulators)

**Why they will cite us:** The manuscript explicitly positions itself as an *organic-specific complement* to the four dominant inorganic simulators (DNN+NeuroSim, MemTorch, AIHWKIT, CrossSim). Any of these teams that adds organic-device primitives—photoresponse nonlinearity, double-exponential retention, or inverse-gamma front-end compensation—will need a baseline to validate against. Our OPECT zero-shot case study (88.53 ± 0.08 %) provides a ready-made benchmark.

| Citing Paper (Projected) | Team / Venue | Likely Citation Angle | Confidence |
|---|---|---|---|
| **CrossSim v2 / Organic Extension** (Sandia + external collaborators) | Sandia Nat. Labs, *IEEE TCAD* or arXiv | "Behavioral organic surrogate validated against Li et al." | Medium |
| **AIHWKIT v2 Device-Model Expansion** | IBM Research | Add organic OECT/OPECT lookup tables; cite our profile interface as prior art. | Medium |
| **MICSim Organic Plug-in** | Tsinghua / ASP-DAC follow-up | Modular simulator extension; compare hybrid-mapping accuracy to our Tiny-ViT baseline. | Low–Medium |
| **New Organic-Specific Simulator** (Zhang / OPECT group or Liu / wearable group) | *Nature Electronics* or *Nature Communications* | Need a system-level accuracy anchor; our framework is the only published ViT-on-organic benchmark. | High |
| **MemTorch Retention & Drift Extension** | Univ. of Michigan or spin-off | Our retention-aware V8 model and double-exponential decay provide a PyTorch-native reference. | Medium |

**Catalytic event to watch:** If Sandia or IBM publish an organic-device module in Q3–Q4 2026, our citation velocity jumps immediately, because these groups are high-volume citers (their simulator papers routinely attract 50+ references and reciprocate to baseline benchmarks).

---

### 1.2 HAT / Robust Training Methods (New HAT Variants, Domain Randomization for Hardware)

**Why they will cite us:** Ensemble HAT is a *training-schedule innovation*, not a hardware innovation. It is conceptually adjacent to domain randomization (Tobin et al., 2017) and to the 2025 "Analog Foundation Models" work, but it targets *spatially structured, instance-fixed D2D mismatch* rather than i.i.d. noise. This makes it directly reusable for any analog or memristive platform where mismatch maps are frozen per chip.

| Citing Paper (Projected) | Team / Venue | Likely Citation Angle | Confidence |
|---|---|---|---|
| **Analog Foundation Models — ViT/CV Follow-up** | ETH / IBM / arXiv | Extend per-channel noise injection to spatial-instance resampling; cite Ensemble HAT as the ViT precedent. | High |
| **Domain Randomization for CIM** (sim-to-real transfer) | Robotics + EDA crossover, *ICRA* / *MLCAD* | "Hardware-instance randomization via epoch-resampled mismatch maps [Li et al.]" | Medium |
| **Learned Affine Calibration + HAT** | UC Berkeley / Stanford, *NeurIPS* / *ICML* | Use our fixed-mask collapse (10.00 %) as the motivational baseline for learned calibration. | Medium |
| **Meta-Learning for Analog Deployment** | Meta / academic lab, *ICLR* | Fast adaptation to fresh hardware instances; our Ensemble HAT accuracy is the zero-shot bar to beat. | Low–Medium |
| **Quantization-Aware Training Survey Update** (Nagel et al. or successor) | *OpenReview* / journal | Our ADC 6-bit cliff and Sobol analysis ($S_{\text{ADC}}=0.98$) provide a clean analog-complement data point. | Medium |

**Catalytic event to watch:** A NeurIPS or ICML 2026 workshop on "Machine Learning for Analog Hardware" would make Ensemble HAT a mandatory citation for any submission in that track.

---

### 1.3 ViT Deployment on Edge (TinyViT Follow-ups, Efficient Attention)

**Why they will cite us:** The manuscript is one of the few papers that deploys Tiny-ViT-5M (and ConvNeXt-Tiny) under *analog* noise and quantifies exactly where the attention pathway breaks. For edge-ViT researchers who treat quantization and low-bit inference as solved problems, our work introduces the *analog non-ideality* dimension.

| Citing Paper (Projected) | Team / Venue | Likely Citation Angle | Confidence |
|---|---|---|---|
| **TinyViT v2 / EfficientViT-Lite** | Microsoft Research, *CVPR* / *ECCV* | "Beyond quantization: analog-CIM deployment envelope for efficient ViT families [Li et al.]" | Medium |
| **Mamba / State-Space Models on CIM** | Princeton / CMU, *ICML* / *ISSCC* | Our severe-NL ceiling motivates attention-free architectures; cite the ~30 % barrier as the analog-attention cost. | High |
| **Linear-Attention Analog Accelerators** | UC San Diego / industry, *ISCA* / *MICRO* | Replace softmax attention with linear operators to avoid our identified MLP-pathway collapse. | Medium |
| **Low-Bit ViT Quantization (follow-ups to PTQ-ViT, Q-ViT)** | Academic groups, *CVPR* / *ECCV* | Our 6-bit ADC cliff parallels their 6-bit quantization cliff; cross-citation is natural. | Medium |
| **On-Device Transfer Learning for ViT** | IBM / Intel, *IEDM* / *VLSI* | Our CIFAR-10 → CIFAR-100 accuracy matrix under noise provides a crossbar-deployment baseline. | Low–Medium |

**Catalytic event to watch:** If a major efficient-ViT paper (e.g., from Microsoft Research or Apple) adds an "analog-aware" evaluation column to their benchmark table, we become a standard reference.

---

### 1.4 Device Physics Papers Needing System-Level Validation

**Why they will cite us:** The organic-device literature is overwhelmingly device-centric. The manuscript provides the *system-level accuracy table* that device physicists need to justify fabrication investments. A paper reporting a new organic synapse with NL = 1.8 can now point to our work and say: "This lies in the severe-NL regime where first-order software recovery is structurally limited to ~30 %; our novel material pushes NL below 1.2, entering the recoverable regime."

| Citing Paper (Projected) | Team / Venue | Likely Citation Angle | Confidence |
|---|---|---|---|
| **OPECT Array Follow-up** (Zhang group, 2026–2027) | *Nature Nanotechnology* / *Nature Electronics* | "System-level accuracy on CIFAR-10 validated via profile-driven simulation [Li et al.], reaching 88.53 %." | High |
| **Wearable OECT Platform Extension** (Liu group, 2024 wearable follow-up) | *Nature Electronics* | Stretchable arrays need system benchmarks; our framework is the only published ViT baseline. | Medium |
| **Organic Neuron + Synapse Integration** (Harikesh / Ji / Beller groups) | *Nature Communications* / *Science Advances* | "While prior system-level studies were limited to perceptrons [Lin 2016], Li et al. established ViT-scale behavioral simulation." | Medium |
| **New Organic Memristor with Improved Retention** | Multi-group, *Advanced Materials* / *Nature Electronics* | Our retention-drift V8 model and plateau behavior (79 % at 10 000 s) set the accuracy-expectation baseline. | Medium |
| **Temperature-Resilient Organic Synapse Follow-up** (Fuller / Guo groups) | *Nature Communications* | Our iso-accuracy contours in (D2D, ADC) space provide the system-level validation they lack. | Low–Medium |

**Catalytic event to watch:** Any 2026–2027 *Nature Electronics* or *Nature Nanotechnology* paper on organic arrays that includes a "neural network demonstration" section will almost certainly cite us as the state-of-the-art system-level benchmark.

---

### 1.5 Reproducibility / Negative-Result Methodology Papers

**Why they will cite us:** The severe-NL result is a *falsification* of three independent mitigation strategies (MLP-linear, all-linear, joint training), all converging on the same ~30 % ceiling. In a field where negative results are under-published, this is a scarce and valuable citation target for methodology researchers.

| Citing Paper (Projected) | Team / Venue | Likely Citation Angle | Confidence |
|---|---|---|---|
| **Falsification Methodology in Neuromorphic Computing** | TU Dresden / U. Zurich, *Front. Neurosci.* / *Neuromorph. Comput. Eng.* | "Li et al. exemplify how systematic falsification of candidate mitigations can localize structural limits." | Medium |
| **Reproducibility Standards for CIM Simulation** | Community white paper, arXiv / *IEEE Design & Test* | Our locked-numbers script (16/16 passed) and JSON provenance manifest are reusable reproducibility templates. | Medium |
| **Negative-Result Publishing in Hardware–ML** | Meta-science group, *PNAS* / *Nature Human Behaviour* | The 30 % ceiling and the explicit "what does not work" narrative provide a case study. | Low–Medium |
| **Benchmark Design for Emerging Memory** | IEEE / JEDEC working group | Our fresh-instance evaluation protocol (10 arrays, 5 MC runs per instance, no-AMP recovery) is a proposed standard. | Low–Medium |
| **Open-Source Release Impact Studies** (MLCommons / academic) | *JMLR* / *PLOS ONE* | compute_vit release metrics (if tracked) can be cited as a hardware-simulation open-source success story. | Low |

**Catalytic event to watch:** A dedicated workshop or special issue on "Negative Results in Neuromorphic Engineering" (e.g., at COINS or NICE 2027) would make the severe-NL section a canonical reference.

---

### 1.6 Grant Proposals Citing Our Deployment Envelope

**Why they will cite us:** Grant reviewers in the US (NSF ECCS/CISE, DOE BES/ASCR, DARPA MTO), EU (Horizon Europe Chips JU, FET-Open), and Asia (NRF Korea, MEXT Japan) increasingly demand *quantified deployment envelopes* for proposed hardware. Our iso-accuracy contour map (Fig. 6) and Sobol sensitivity indices provide ready-made justification paragraphs.

| Citing Document (Projected) | Agency / Program | Likely Citation Angle | Confidence |
|---|---|---|---|
| **NSF ECCS — Analog & Mixed-Signal Design** | NSF | "Prior work has established that ADC resolution dominates organic-CIM accuracy above 6 bits [Li et al., Sobol $S_{\text{ADC}}=0.98$]; this proposal targets 8-bit SAR ADC design." | High |
| **DARPA MTO — Near-Zero-Power Edge AI** | DARPA | "Ensemble HAT demonstrates 86 % fresh-instance recovery without per-chip calibration [Li et al.]; we propose on-chip calibration to close the remaining gap." | Medium |
| **Horizon Europe — Chips for Edge Intelligence** | EU Chips JU | "Organic optoelectronic CIM has demonstrated 88.53 % zero-shot transfer on CIFAR-10 [Li et al.]; this project scales to ImageNet." | Medium |
| **DOE BES — Organic Electronic Materials** | DOE | "The severe-NL ceiling (~30 %) indicates that materials with $NL < 1.5$ are required for system viability [Li et al.]." | High |
| **NIH / NIBIB — Wearable Neuromorphic Biosensors** | NIH | "Stretchable OECT arrays have reached system-level simulation [Li et al.]; this proposal fabricates and validates the first wearable ViT-CIM array." | Low–Medium |
| **NVIDIA Academic / Industry Grants** | NVIDIA | "Profile-driven simulation established the risk-aware evaluation paradigm [Li et al.]; we extend it to multi-task embodied AI." | Medium |

**Catalytic event to watch:** NSF ECCS and DOE BES program officers frequently circulate "success stories" to reviewers. If our NC paper is featured in a Dear Colleague Letter or PI meeting, grant citations become self-sustaining.

---

## 2. Citation Velocity Forecast

The table below estimates cumulative citations (Google Scholar / Web of Science) under three scenarios. These are *not* predictions of impact factor or h-index; they are market-sizing estimates for a single paper in a subfield with ~200–400 active authors worldwide.

| Month | Milestone | Conservative | Moderate | Optimistic |
|---|---|---|---|---|
| **M3** | arXiv live; code released; blog published | 2–4 | 4–8 | 8–15 |
| **M6** | NC decision (accept / RR / reject); first citations from arXiv | 3–6 | 8–15 | 15–28 |
| **M9** | NC online (if accepted); first follow-up simulators on arXiv | 5–10 | 15–25 | 30–50 |
| **M12** | Conference season (IEDM, NeurIPS, ICCAD); invited talk circuit | 8–15 | 25–40 | 50–80 |
| **M18** | Device-physics follow-ups in *Nature* family; grant cycle | 12–22 | 40–60 | 80–120 |
| **M24** | Second-generation citations (papers citing papers that cite us); potential survey inclusion | 18–30 | 60–95 | 120–180 |

### Scenario Definitions

**Conservative (P ≈ 25 %):** NC rejected after two rounds; paper resubmitted to *IEEE JSSC* or *TCAS-I* with 6-month additional delay. Code released but not actively maintained. No invited talks. Field attention shifts to digital-CIM (TensorCIM, Fe-GC) and away from organic analog. arXiv version garners modest attention from the core CIM community only.

**Moderate / Base Case (P ≈ 50 %):** NC accepted after one major revision (8-month turnaround from submission to online). arXiv preprint gains traction via Twitter/X and LinkedIn among EDA/MLCAD researchers. One invited talk at IEDM 2026 or NeurIPS 2026 workshop. Code used by 3–5 external groups for baseline comparisons. Press coverage limited to university newsroom and EE Times / Semiconductor Engineering article.

**Optimistic (P ≈ 25 %):** NC accepted with minor revisions (5-month turnaround). arXiv version highlighted by Nature Portfolio social media accounts. Blog post ("We Thought Joint Training Would Fix Everything. It Didn't.") goes viral on Hacker News / ML Twitter, driving 10 000+ views. Invited talks at IEDM 2026, MLCAD 2026, and a NeurIPS workshop. Code adopted as a benchmark in at least one DARPA or industry R&D program. Survey paper (e.g., Lanza et al. 2027 update) includes us as a key milestone.

---

## 3. Key Factors — What Accelerates Citations?

### 3.1 Code & Data Release (High Impact, Controllable)

The compute_vit repository—with its replaceable device-profile JSON interface, pre-trained checkpoints, and locked-numbers validation script—is the single highest-leverage accelerator. Simulator papers that do not release code typically plateau at 20–40 % of the citation volume of their open-source counterparts. Our planned Zenodo deposit (source data v1) and GitHub release should be executed *before* the NC acceptance decision, because arXiv + code drives early citations that later snowball.

**Action:** Ensure the README includes a "Cite this work" BibTeX snippet and a one-paragraph description of the Ensemble HAT API. Papers are more likely to cite a tool they can install in 30 seconds.

### 3.2 arXiv Preprint Timing (High Impact, Controllable)

Posting to arXiv within days of NC submission (or immediately after desk-reject) captures the attention of the fast-moving ML/CV community before the 6–12 month peer-review delay. For interdisciplinary papers at the devices–systems boundary, arXiv citations often outnumber journal citations in the first 18 months.

**Action:** The arXiv checklist (K-X21) should be executed no later than 2026-04-25. Include the blog blurb in the "Comments" field to drive social-media sharing.

### 3.3 Press & Social Amplification (Medium Impact, Partially Controllable)

The press-release draft ("Researchers Discover Both a Fix and a Fundamental Limit...") and the blog narrative ("We Thought Joint Training Would Fix Everything. It Didn't.") are well-constructed for non-specialist amplification. A single EE Times or Semiconductor Engineering article can drive 5–10 citations from industry R&D teams that do not monitor arXiv.

**Action:** Pitch the blog to Hacker News and the press release to trade media within 48 hours of arXiv posting. The narrative hook (fix + limit) is stronger than either story alone.

### 3.4 Invited Talks & Conference Visibility (Medium Impact, Controllable)

An invited talk at IEDM, ISSCC, or a NeurIPS workshop converts passive readers into active citers. The devices community (IEDM/ISSCC) cites slowly but heavily; the ML community (NeurIPS/ICML) cites quickly but forgets after 12 months. The optimal strategy is to hit both.

**Action:** Submit an abstract to the IEDM 2026 "Memory Technology" session and to the NeurIPS 2026 workshop on "Machine Learning for Physical Systems." The 5-minute talk script (K-X24) is already drafted.

### 3.5 Survey & Review Inclusion (High Impact, Not Directly Controllable)

The most durable citation source is inclusion in review articles. Mario Lanza's *Nature* perspective (2025) on the memristor industry is already a citation magnet; a 2027 update that includes organic CIM would almost certainly cite us. Similarly, a future *Nature Electronics* review on edge-ViT accelerators or a *Proceedings of the IEEE* survey on CIM would be high-value targets.

**Action:** Send a polite email to authors of high-citation review papers (Lanza, Harikesh, Xu) with a preprint and a one-slide summary. Review authors are time-constrained and appreciate being handed a ready-made paragraph.

---

## 4. Key Risks — What Suppresses Citations?

### 4.1 NC Rejection or Prolonged Revision (High Risk)

NC rejection would delay the official publication stamp by 6–12 months (resubmission to *Nature Electronics*, *IEEE JSSC*, or *Advanced Materials*). While arXiv preserves visibility, some communities (particularly device physicists and grant reviewers) overweight journal-branded publications. A desk reject without transfer would be the most damaging outcome, because it signals a scope mismatch that other editors may read as weakness.

**Mitigation:** The response-letter arsenal (K-X19–K-X22) and red-team audits are already in progress. Ensure the revised manuscript addresses the "missing top-journal organic neuron" and "missing IEDM silicon" gaps identified in the literature-landscape review (K-X16).

### 4.2 Code Not Released or Release Delayed (High Risk)

If the code remains behind institutional firewall or the Zenodo deposit is delayed beyond M3, external groups will build their own baselines rather than cite ours. The reproducibility-package plan (K-X15) must be treated as a co-equal deliverable to the manuscript itself.

**Mitigation:** Execute the reproducibility package (source data v1 + code snapshot ledger) within 7 days of arXiv posting, regardless of NC status.

### 4.3 Field Moves On (Medium Risk)

The CIM-Transformer field is moving rapidly. If a 2026 IEDM or ISSCC paper demonstrates a *silicon* organic optoelectronic ViT accelerator with >90 % accuracy, our simulation-only work could be framed as "preliminary." Conversely, if the field pivots sharply to digital-CIM (FeFET, SRAM-based digital-CIM) or to spiking neuromorphic (Intel Loihi 2, IBM NorthPole), organic analog-CIM citations could dry up.

**Mitigation:** Emphasize in all communications that the framework is *device-agnostic* (replaceable profiles) and *architecture-agnostic* (ResNet, ConvNeXt, ViT). Position the work as a "risk-aware evaluation methodology" rather than an "organic-only simulator."

### 4.4 Competition from Similar Preprints (Medium Risk)

If another group posts an arXiv preprint in Q2–Q3 2026 with overlapping scope—e.g., a PyTorch-native organic-CIM simulator or a ViT HAT study on ReRAM—our novelty claim could be diluted. The most credible threat is a follow-up from the Zhang OPECT group or from an IBM AIHWKIT extension team.

**Mitigation:** Speed. The arXiv posting (K-X21) should go live this week. In fast-moving subfields, first-to-arXiv often captures the citation network even if the journal acceptance is slower.

### 4.5 Ensemble HAT Seen as Obvious (Low Risk)

A hostile reviewer or competitor might argue that epoch-resampling D2D masks is "just domain randomization applied to HAT." If this framing takes hold in the community, the methodological citation value of Ensemble HAT could be suppressed.

**Mitigation:** The manuscript already contains the one-sample t-test ($p < 10^{-15}$) and the ablation cadence scan (epoch vs. per-batch vs. fixed) that empirically justify the scheduling choice. Ensure the blog and FAQ prominently feature the ablation data, not just the concept.

---

## 5. Strategic Recommendations

| Priority | Action | Owner | Deadline | Expected Citation Impact |
|---|---|---|---|---|
| P0 | Post arXiv preprint with inlined bbl and flattened source | K-X21 | 2026-04-25 | +30–50 % M6 velocity |
| P0 | Release Zenodo source-data bundle + GitHub repo with README cite snippet | K-X15 | 2026-04-28 | +40–60 % long-tail |
| P1 | Publish blog post on personal/Medium account; submit to Hacker News | K-X23 | 2026-04-26 | +10–20 % M3–M6 |
| P1 | Distribute press release to EE Times, Semiconductor Engineering, university newsroom | K-X25 | 2026-04-29 | +5–15 % industry citations |
| P1 | Submit IEDM 2026 abstract (invited or contributed) | Author | 2026-05-15 | +20 % M12 devices-community |
| P2 | Email preprint + one-slide summary to 5 review-paper authors (Lanza, Harikesh, Xu, Joshi, Rasch) | Author | 2026-05-01 | +10 % M18 survey inclusion |
| P2 | Prepare NeurIPS / MLCAD 2026 workshop abstract | Author | 2026-05-30 | +15 % M12 ML-community |
| P2 | Track code downloads / GitHub stars; add citation badge after NC acceptance | Author | Ongoing | Reputational signal for reviewers |

---

## 6. Bottom Line

This paper has **asymmetric citation upside**: the Ensemble HAT protocol is reusable across any analog-CIM platform, and the severe-NL ceiling is a scarce negative result. In the base-case scenario, we project **60–95 citations at 24 months**, driven primarily by (1) simulator teams adding organic modules, (2) HAT researchers extending epoch-resampling, and (3) device physicists anchoring system-level claims. The optimistic tail (120–180 citations) requires rapid NC acceptance + strong press amplification + code adoption by a major R&D program. The conservative floor (18–30 citations) is protected by the niche value of the OPECT zero-shot benchmark and the reproducibility package, even if the broader field pivots.

**The single highest-return action this week is arXiv + code release.** Everything else—press, talks, grants—builds on that foundation.

---

*Forecast prepared for Task K-X27. Method: bottom-up community sizing + top-down velocity benchmarking against comparable NC/IEDM papers in CIM and neuromorphic engineering (Joshi 2020 NC: ~120 citations at 24 months; Lammie 2022 MemTorch: ~80 citations at 24 months; Rasch 2021 AIHWKIT: ~200 citations at 24 months). Adjusted downward for organic-device niche factor (~0.6×) and upward for negative-result scarcity premium (~1.3×).*
