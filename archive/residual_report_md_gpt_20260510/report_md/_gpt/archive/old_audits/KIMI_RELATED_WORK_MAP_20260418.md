# Related-Work Reference Map — 2026-04-18

**Source:** `bibliography_structured.csv` aligned against manuscript Sections 1 (Introduction), 2 (Related Work), 6 (Discussion).

---

## Bucket 1: Simulator Positioning

| Key | Authors | Relevance | Safest Use | Do Not Overclaim |
|-----|---------|-----------|------------|------------------|
| `peng2020dnnneurosim` | X. Peng et al. | Canonical hierarchical CIM simulator (device→circuit→architecture). | "System-level CIM simulators such as DNN+NeuroSim established an effective template..." | Do not claim DNN+NeuroSim models organic devices; it does not. |
| `lammie2022memtorch` | C. Lammie et al. | PyTorch-native memristive simulator. | "MemTorch showed how memristive non-idealities can be embedded into PyTorch workflows..." | MemTorch does not target organic photoresponse. |
| `rasch2021aihwkit` | M.J. Rasch et al. | IBM analog crossbar toolkit; practical HAT stack. | "AIHWKIT exposed analog HAT and inference simulation in a practical mixed-signal software stack..." | AIHWKIT is inorganic PCM/ReRAM focused; our comparison is sanity-check only. |
| `crosssim2026` | Sandia National Laboratories | GPU-accelerated crossbar-accuracy workflow. | "CrossSim provides a GPU-accelerated crossbar-accuracy workflow with parasitic resistance, ADC, drift..." | CrossSim does not model organic-specific photoresponse or retention. |

## Bucket 2: Variation-Aware / Hardware-Aware Training

| Key | Authors | Relevance | Safest Use | Do Not Overclaim |
|-----|---------|-----------|------------|------------------|
| `joshi2020accurate` | Vinay Joshi et al. | PCM-based HAT for inference; inorganic precedent. | "HAT mitigates analog non-idealities by injecting hardware perturbations into the forward path during optimization [joshi2020accurate]." | PCM HAT ≠ organic HAT; device physics differ. |
| `choi2019pact` | Jungwook Choi et al. | QAT with parameterized clipping; foundational. | "Related in spirit to quantization-aware training [choi2019pact]..." | QAT is digital quantization, not analog mismatch. |
| `bengio2013estimating` | Y. Bengio et al. | STE theoretical foundation. | Implicit; no need to overcite unless discussing nonlinear-write gradient approximation explicitly. | STE is generic; do not imply Bengio et al. endorsed our surrogate. |

## Bucket 3: Domain-Randomization Adjacency

| Key | Authors | Relevance | Safest Use | Do Not Overclaim |
|-----|---------|-----------|------------|------------------|
| `tobin2017domain` | Josh Tobin et al. | Sim-to-real via environment randomization. | "Although related in spirit to... domain randomization in sim-to-real transfer [tobin2017domain], HAT for CIM faces an additional difficulty..." | Domain randomization randomizes the *environment*, not a fixed spatial mismatch map. The analogy is conceptual only. |

## Bucket 4: Organic Device / Array Motivation

| Key | Authors | Relevance | Safest Use | Do Not Overclaim |
|-----|---------|-----------|------------|------------------|
| `xu2025emerging` | Y. Xu et al. | 2025 review of organic synaptic devices. | "Organic optoelectronic and electrochemical synaptic devices are particularly attractive for edge vision applications..." | Review article; device parameters are ranges, not exact values for our simulator. |
| `guo2024organic` | H. Guo et al. | Gate-modulated multilevel organic optoelectronic synapse. | Cited as recent organic-device demonstration with multilevel memory. | Single-device paper; array behavior is extrapolated. |
| `zhang2026opect` | X. Liu et al. | 2025 OPECT array; lithographically patterned NIR. | "As a literature-anchored reference point, we simulated zero-shot transfer to a 2025 OPECT array [zhang2026opect]..." | We use their reported parameters as priors, not validated measured data. |
| `vincze2026dualplasticity` | T. Vincze et al. | Dual-plasticity organic synaptic transistor. | "First-order nonlinear-write and double-exponential retention surrogates are supported, with parameters anchored to measured DNTT transients [vincze2026dualplasticity]." | Parameters are extracted from their measured curves; our model is behavioral, not physics-based. |
| `melianas2020temperature` | A. Melianas et al. | Temperature-resilient organic synapses. | Can support retention discussion if needed. | Not currently cited in main text; reserve for supplementary if retention discussion expands. |

## Bucket 5: ViT-on-CIM / Mixed-Signal Partitioning

| Key | Authors | Relevance | Safest Use | Do Not Overclaim |
|-----|---------|-----------|------------|------------------|
| `kim2025hemlet` | M. Kim, J.-J. Kim | Heterogeneous CIM chiplet for ViT. | "Recent heterogeneous CIM accelerators for Vision Transformers confirm this pattern: linear projections are mapped to analog arrays, whereas attention scores... remain digital..." | HEMLet is a chiplet architecture proposal; our mapping logic is convergent, not derived from it. |
| `lin2024hardsea` | Y. Lin et al. | Hybrid analog-ReRAM + digital-SRAM for sparse attention. | Cited alongside HEMLet for hybrid analog-digital ViT deployment. | HARDSEA targets sparse attention acceleration; our attention remains fully digital. |
| `ge2024allspark` | M. Ge et al. | Workload orchestration for ViT on PIM. | Supports heterogeneous mapping rationale. | AllSpark is a scheduler; our deployment is static mapping. |
| `bettayeb2024memristorattention` | M. Bettayeb et al. | Memristor accelerator for self-attention. | "Analog memristor accelerators for self-attention have also been explored as a competing direction [bettayeb2024memristorattention], but they rely on a substantially different hardware partitioning strategy..." | Their strategy is different; do not conflate. |

## Bucket 6: ADC / Low-Bit Transformer Sensitivity

| Key | Authors | Relevance | Safest Use | Do Not Overclaim |
|-----|---------|-----------|------------|------------------|
| `liu2021ptqvit` | Z. Liu et al. | Post-training quantization for ViT. | "This focus is also consistent with recent low-bit ViT quantization studies, which repeatedly identify attention logits... as especially sensitive under aggressive precision reduction [liu2021ptqvit,li2022qvit,lin2023vitptq]." | PTQ is post-training; our analog noise is a different perturbation regime. |
| `li2022qvit` | Y. Li et al. | Q-ViT: fully quantized low-bit ViT. | Cited as low-bit ViT sensitivity reference. | Q-ViT targets 4-bit uniform quantization; our ADC cliff is analog readout resolution. |
| `lin2023vitptq` | Y. Lin et al. | FQ-ViT post-training quantization. | Cited for attention difficulty below 6 bits. | Same caution as above. |
| `wu2024blockwise` | X. Wu et al. | Block-wise mixed-precision for ReRAM accelerators. | Can support ADC-resolution discussion if cited. | Targets ReRAM block-wise quantization; our ADC is behavioral SAR proxy. |

---

## Weak / Unused Entries (Hold for Now)

| Key | Reason |
|-----|--------|
| `wang2024epim` | arXiv only; already cited but lower trust than peer-reviewed alternatives. |
| `li2024activematrix` | Good array paper but not currently needed in main argument. Reserve for response if reviewer asks for more array-level citations. |
| `cui2025multimode` | Excellent (Nature Nanotechnology) but currently only cited in intro sweep; can be promoted if array discussion deepens. |
| `yang2025fastir` / `liu2026iconniv` | IR-drop modeling; currently only in Discussion limitations. Keep if parasitic discussion expands. |
