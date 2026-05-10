# Paper-2 Skeleton — LLM KV-Cache on Organic Optoelectronic CIM

**Direction:** C (KV-Cache) per `CLAUDE_WORK2_DIRECTION_LOCK_20260423.md`  
**Rule:** Number-agnostic. All quantitative claims use `[TBD]` placeholders.  
**Supersedes:** `paper/paper2/skeleton_v0/*` (frozen reference)  

---

## 00 Abstract

See `00_abstract.md` (K-Z34). One-paragraph placeholder:

> [One-paragraph pitch from CLAUDE_WORK2_DIRECTION_LOCK_20260423.md §3, with all numbers replaced by `[TBD]` placeholders.]

---

## 01 Introduction

**File:** `01_intro.md` (K-Z13)

### 1.1 The KV-Cache Bottleneck
- Problem: LLM inference is memory-bound, not compute-bound, for autoregressive decoding
- KV cache footprint formula; growth with context length
- Key number: [TBD] GiB for [TBD] model at [TBD] context in FP16
- Existing remedies: quantization (KIVI), eviction (StreamingLLM), offloading — all trade accuracy/latency

### 1.2 Analog CIM as a Candidate
- Promise: dense, non-volatile, in-place compute
- Challenge: existing analog CIM work for transformers either sacrifices NVM density (offloads attention to CMOS) or suffers from endurance/retention limits
- Key gap: no prior work maps KV cache to organic optoelectronic memory

### 1.3 Organic-Specific Moat
- Retention ~10³ s matches LLM session length (seconds-to-minutes)
- Write-once-per-prefill pattern fits organic's limited cycling endurance
- Optical refresh sidesteps endurance cost
- Key claim: organic is the only emerging memory with this physics-level match

### 1.4 Contributions
1. First systematic evaluation of LLM KV-cache mapping to organic optoelectronic CIM
2. Behavioral simulator extending Work 1 to KV-cache tensors with noise/quantization/retention models
3. Characterization of attention degradation under organic device non-ideality; derivation of minimum analog-state count
4. Architecture proposal with energy/area/latency Pareto analysis

---

## 02 Related Work

**File:** `02_related.md` (K-Z14)

### 2.1 Digital KV-Cache Optimization
- Quantization: KIVI, KVQuant, GEAR (2-bit to 4-bit)
- Eviction: StreamingLLM, H₂O, SnapKV, PyramidKV, TRIM-KV
- Offloading: InfiniGen, TailorKV, PQCache
- System: PagedAttention, SCBench, CacheBlend
- **Our distinction:** We do not compress KV; we change the storage substrate to analog CIM

### 2.2 Analog CIM for Transformers
- ReTransformer (ReRAM): static weight dataflow, dynamic KV still writes
- X-Former, iMTransformer: heterogeneous ReRAM/FeFET + CMOS
- UCSD Hybrid Attention: analog CIM prunes 75% tokens; digital handles rest
- Capacitor gain cells: volatile, charge-decay limited
- HASTILY / Ouroboros: SRAM-CIM, not non-volatile
- IBM 3D-CiM-LLM: abstract simulator, no organic
- **Our distinction:** First organic-specific KV-cache mapping; first to exploit retention match and optical refresh

### 2.3 Organic & Optoelectronic Memory
- van de Burgt et al. (Nature Electronics 2018): organic neuromorphic review
- Kim et al. (Adv. Sci. 2023): organic memristor flexible NN
- OECT/OEC-RAM (KAUST): 82% retention over 1000 s, 5 states, 20k cycles
- Chen et al. (Nature Photonics 2023): photon-modulated electrochemical doping
- **Our distinction:** First application to LLM KV-cache; first system-level benchmark

---

## 03 Theory & Method

**File:** `03_theory.md` (K-Z15)

### 3.1 Organic Device Model
- Conductance quantization: `G = G_min + (G_max - G_min) × w / n_states`
- Noise: C2C (per-forward Gaussian) + D2D (fixed per instance)
- Retention: `G(t) = G_min + (G_0 - G_min) × exp(-t/τ)`
- Nonlinearity: NL_LTP/NL_LTD from Work 1
- **Placeholders:** all σ, τ, n_states values as `[TBD]`

### 3.2 KV-Cache Mapping
- Key/Value tensors: `[batch, n_heads, seq_len, head_dim]`
- Mapping to crossbar: each head gets one crossbar array
- Array dimensions: rows = head_dim, cols = max_seq_len
- Write pattern: prefill = bulk write; decode = append one column

### 3.3 Attention Computation in Analog
- Q·K^T: Q vector drives word-lines, K stored as conductance matrix
- Softmax: digital peripheral (analog softmax is hard)
- Attention·V: score vector drives word-lines, V stored as conductance matrix
- **Key design choice:** analog MAC for QK^T and AV; digital for softmax and residual

### 3.4 Quantization ↔ Conductance Co-Design
- Uniform codebook: linear mapping from float to conductance
- Learned codebook: K-means on calibration set, map centroids to conductance levels
- **Theory claim:** learned codebook can exploit organic NL to achieve higher effective precision than uniform

### 3.5 Refresh & Eviction Policies
- Optical refresh: pulse duration [TBD], energy [TBD] per cell
- Hierarchical: organic CIM L1 (hot tokens) → SRAM L2 (warm) → Flash L3 (cold)
- Eviction: FIFO, LRU, attention-score threshold

---

## 04 Experiment Plan

**File:** `04_experiment_plan.md` (K-Z16)

### 4.1 Model & Dataset
- Primary: TinyLlama-1.1B (HF `TinyLlama/TinyLlama-1.1B-intermediate`)
- Secondary: LLaMA-2-7B GQA (HF `meta-llama/Llama-2-7b-hf`)
- Datasets: WikiText-103, LongBench subset, GSM8K, MT-Bench
- Baselines: FP16, KIVI-2bit, KIVI-4bit, SRAM-CIM, oxide-RRAM-CIM

### 4.2 Exp 1: Noise-Robustness (CX-L2)
- See `KIMI_WORK2_EXPERIMENT_PLAN_20260423.md` §1
- Key figure: contour plot (N vs σ) with ΔPPL color map
- Key table: minimum N for "lossless" (ΔPPL < 1%) at each σ

### 4.3 Exp 4: Architecture Exploration (CX-L5)
- See `KIMI_WORK2_EXPERIMENT_PLAN_20260423.md` §2
- Key figure: 3D Pareto surface (latency, energy, area)
- Key table: recommended array config for 1B model decode step

### 4.4 Exp 2: Quantization Co-Design (CX-L3)
- See `KIMI_WORK2_EXPERIMENT_PLAN_20260423.md` §3
- Key figure: memory footprint vs. accuracy scatter (digital quant vs. analog states)
- Key claim: organic analog achieves [TBD]× footprint reduction at iso-accuracy vs. digital quant

### 4.5 Exp 3: Retention & Refresh (CX-L4)
- See `KIMI_WORK2_EXPERIMENT_PLAN_20260423.md` §4
- Key figure: task accuracy vs. total energy for each refresh policy
- Key claim: optical refresh every [TBD] s achieves [TBD]% accuracy at [TBD]× energy vs. SRAM

---

## 05 Discussion

**File:** `05_discussion.md` (K-Z17)

### 5.1 What the Results Mean
- If Exp 1 shows N ≥ 6 needed → organic needs 6-level cells; feasible with current OEC-RAM
- If Exp 1 shows collapse at σ > 0.01 → pitch becomes "graceful degradation" not "lossless"
- If Exp 4 shows ADC is bottleneck → architecture should prioritize low-bit ADC

### 5.2 Limitations
- Simulation-only (no fabricated organic array measurements)
- Device models extrapolated from Work 1 ViT experiments and literature
- No interconnect / routing modeled
- Single-device failure not modeled

### 5.3 Future Work
- Direction D (opto-electronic co-design): joint optimization of photodiode frontend + CIM weights
- Direction B (continual learning): online adaptation of KV cache to task drift
- Direction A (multi-tile): chiplet-scale organic CIM arrays for >7B models

---

## 06 Conclusion

- Recap: KV-cache is the LLM inference bottleneck; organic CIM has a physics-level match
- Contributions: first benchmark, first simulator extension, first architecture proposal
- Closing: organic CIM should be evaluated not as a general-purpose accelerator but as a domain-specific memory tier for generative inference

---

## Appendix A: Device Parameter Table

| Parameter | Symbol | Value | Source |
|-----------|--------|-------|--------|
| Conductance range | [G_min, G_max] | [TBD] | [31] |
| Analog states | N | [TBD] | [31] |
| C2C noise σ | σ_c2c | [TBD] | Work 1 |
| D2D noise σ | σ_d2d | [TBD] | Work 1 |
| Retention time | τ | [TBD] | [31, 32] |
| Cycling endurance | — | [TBD] | [31] |
| Write energy | E_write | [TBD] | [31] |
| Optical refresh energy | E_refresh | [TBD] | [32] projected |

---

## Appendix B: Simulator Validation

- Cross-validate against Work 1 ViT results: same noise model should produce consistent accuracy degradation when applied to linear layers
- Compare against IBM 3D-CiM-LLM simulator methodology [25]

---

*Skeleton v1 locked 2026-04-23. Section files: 01_intro.md, 02_related.md, 03_theory.md, 04_experiment_plan.md, 05_discussion.md.*
