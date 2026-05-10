# Literature Supplement (T4) — Safe, Bib-Backed Candidate Insertions

This supplement has been rewritten to include only references that are already
present in `paper/latex_gpt/refs_gpt.bib` and have been explicitly used or
validated during the current manuscript pass. It is intended as a safe staging
document for Claude, not as an invitation to blindly bulk-insert citations.

## 1. Organic CIM / Organic Optoelectronic Array Anchors

1. **Hu et al.**
   - **Title:** *An Energy-Efficient Solid-State Organic Device Array for Neuromorphic Computing*
   - **Venue:** IEEE Transactions on Electron Devices, 2023
   - **DOI:** `10.1109/TED.2023.3327947`
   - **BibTeX key:** `gebregiorgis2023organiccim`
   - **Best use:** `§2.1 Related Work`
   - **Suggested sentence:** Recent deployment-relevant organic array demonstrations include energy-efficient solid-state organic device arrays that move beyond isolated single-device characterization toward integrated neuromorphic hardware \citep{gebregiorgis2023organiccim}.

2. **Liu et al.**
   - **Title:** *Near-infrared organic photoelectrochemical synaptic transistors by photolithography for neuromorphic visual systems*
   - **Venue:** Nature Communications, 2026
   - **DOI:** `10.1038/s41467-025-66891-6`
   - **BibTeX key:** `zhang2026opect`
   - **Best use:** `§2.1 Related Work`, `§5.11 Case Study`
   - **Suggested sentence:** Lithographically patterned near-infrared OPECT arrays now provide a realistic literature-calibrated bridge case for system-level evaluation of organic optoelectronic CIM \citep{zhang2026opect}.

3. **Guo et al.**
   - **Title:** *An Organic Optoelectronic Synapse with Multilevel Memory Enabled by Gate Modulation*
   - **Venue:** ACS Applied Materials & Interfaces, 2024
   - **DOI:** `10.1021/acsami.3c19624`
   - **BibTeX key:** `guo2024organic`
   - **Best use:** `§2.1 Related Work`
   - **Suggested sentence:** Recent organic optoelectronic synapses have demonstrated multilevel memory and gate-tunable conductance evolution, reinforcing the need for profile-driven behavioral models rather than binary device abstractions \citep{guo2024organic}.

## 2. Optical Non-Uniformity / Crosstalk / Array-Level Optical Constraints

4. **Liu et al.**
   - **Title:** *Artificial Visual Synaptic Architecture with High-Linearity Light-Modulated Weight for Optoelectronic Neuromorphic Computing*
   - **Venue:** ACS Applied Materials & Interfaces, 2023
   - **DOI:** `10.1021/acsami.3c11495`
   - **BibTeX key:** `visionarch2023crosstalk`
   - **Best use:** `§2.1 Related Work`, `§6.6 Limitations`
   - **Suggested sentence:** Recent optoelectronic visual-synapse architectures explicitly identify crosstalk and integration constraints as obstacles to high-fidelity system scaling \citep{visionarch2023crosstalk}.

5. **Li et al.**
   - **Title:** *An Active-Matrix Synaptic Phototransistor Array for In-Sensor Spectral Processing*
   - **Venue:** Advanced Science, 2024
   - **DOI:** `10.1002/advs.202406401`
   - **BibTeX key:** `amspa2024insensor`
   - **Best use:** `§2.1 Related Work`, `§6.6 Limitations`
   - **Suggested sentence:** Active-matrix synaptic phototransistor arrays underscore that array-level optical addressing, spatial response control, and crosstalk suppression are first-class system concerns rather than peripheral implementation details \citep{amspa2024insensor}.

## 3. ViT-on-PIM / Hardware Mapping References

6. **Ge et al.**
   - **Title:** *Allspark: Workload Orchestration for Visual Transformers on Processing In-Memory Systems*
   - **Venue:** IEEE Transactions on Computers, 2025
   - **DOI:** `10.1109/TC.2024.3483633`
   - **BibTeX key:** `ge2024allspark`
   - **Best use:** `§2.3 Hardware-Aware Training and Hybrid Mapping`
   - **Suggested sentence:** ViT-oriented PIM work such as Allspark reinforces that operator orchestration and dataflow partitioning are central to efficient transformer deployment on memory-centric hardware \citep{ge2024allspark}.

7. **Wang et al.**
   - **Title:** *EPIM: Efficient Processing-In-Memory Accelerators based on Epitome*
   - **Venue:** DAC, 2024
   - **DOI:** `10.1145/3649329.3657377`
   - **BibTeX key:** `wang2024epim`
   - **Best use:** `§2.3 Hardware-Aware Training and Hybrid Mapping`
   - **Suggested sentence:** EPIM likewise illustrates that transformer execution on PIM requires operator-specific adaptation rather than naive whole-model analogization \citep{wang2024epim}.

## 4. ViT PTQ / Attention-Sensitivity References

8. **Liu et al.**
   - **Title:** *Post-Training Quantization for Vision Transformer*
   - **Venue:** NeurIPS, 2021
   - **URL:** NeurIPS proceedings page in `refs_gpt.bib`
   - **BibTeX key:** `liu2021ptqvit`
   - **Best use:** `§5.4 ADC and Quantization Thresholds`
   - **Suggested sentence:** PTQ4ViT established that attention statistics and ranking sensitivity make Vision Transformers unusually brittle under low-precision quantization \citep{liu2021ptqvit}.

9. **Li et al.**
   - **Title:** *Q-ViT: Accurate and Fully Quantized Low-Bit Vision Transformer*
   - **Venue:** NeurIPS, 2022
   - **URL:** OpenReview entry in `refs_gpt.bib`
   - **BibTeX key:** `li2022qvit`
   - **Best use:** `§5.4 ADC and Quantization Thresholds`
   - **Suggested sentence:** Q-ViT further shows that maintaining ViT accuracy at low bitwidth requires explicit protection of attention-sensitive operations \citep{li2022qvit}.

10. **Lin et al.**
    - **Title:** *FQ-ViT: Post-Training Quantization for Fully Quantized Vision Transformer*
    - **Venue:** IJCAI 2022 / arXiv entry as stored in current bib
    - **DOI:** `10.48550/arXiv.2111.13824`
    - **BibTeX key:** `lin2023vitptq`
    - **Best use:** `§5.4 ADC and Quantization Thresholds`
    - **Suggested sentence:** FQ-ViT complements these results by showing that even post-training schemes must explicitly handle transformer-specific quantization bottlenecks \citep{lin2023vitptq}.

## 5. Temperature Sensitivity / Environmental Robustness

11. **Melianas et al.**
    - **Title:** *Temperature-resilient solid-state organic artificial synapses for neuromorphic computing*
    - **Venue:** Science Advances, 2020
    - **DOI:** `10.1126/sciadv.abb2958`
    - **BibTeX key:** `fuller2020tempresilient`
    - **Best use:** `§6.6 Limitations`
    - **Suggested sentence:** Temperature-dependent drift and threshold shifts remain practically relevant for organic synapses, as demonstrated by temperature-resilient solid-state artificial synapse studies \citep{fuller2020tempresilient}.

12. **Guo et al.**
    - **Title:** *Organic High-Temperature Synaptic Phototransistors for Energy-Efficient Neuromorphic Computing*
    - **Venue:** Advanced Materials, 2024
    - **DOI:** `10.1002/adma.202310155`
    - **BibTeX key:** `guo2024hightemp`
    - **Best use:** `§6.6 Limitations`
    - **Suggested sentence:** High-temperature organic synaptic phototransistors confirm that environmental robustness is measurable and nontrivial, reinforcing the need for explicit temperature-aware extensions in future simulators \citep{guo2024hightemp}.

## Notes

- This file is now intentionally limited to citations that are already present in
  the active manuscript bibliography.
- If a new citation is added here later, it should not be considered safe until
  the corresponding BibTeX entry is also added to `refs_gpt.bib` and compiled
  successfully into `main.pdf`.
