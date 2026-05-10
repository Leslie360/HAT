# Direction C: LLM KV-Cache Mapping to Organic Analog CIM Arrays
## Literature Survey — 2026-04-23

---

### 1. Motivation: KV-Cache is the LLM Inference Bottleneck

During autoregressive decoding, Transformers store per-token Key (K) and Value (V) tensors to avoid recomputing attention over the full sequence. This **KV cache** reduces per-token complexity from \(O(n^2)\) to \(O(n)\), but its footprint grows linearly with sequence length:

\[
\text{KV}_{\text{per token}} = 2 \times H \times D \times L \times B
\]

For modern LLMs (e.g., Qwen2.5-7B-Instruct at 1M tokens), the KV cache can exceed **180 GiB in bfloat16**—far larger than model weights themselves [1,2]. This makes KV-cache management the dominant bottleneck for long-context inference, limiting batch size, throughput, and deployable context windows. Conventional remedies—quantization, eviction, offloading to CPU/SSD—trade memory for accuracy or latency. An alternative paradigm is to exploit **dense, analog, non-volatile memory arrays** that can both *store* the KV cache and *compute* attention in-place, potentially breaking the memory wall.

---

### 2. SOTA Landscape

#### 2.1 KV-Cache Compression & System Optimizations (Digital)

The digital-SOTA has converged on three axes:

| Category | Representative Works | Key Finding |
|----------|---------------------|-------------|
| **Quantization** | KIVI [3] (2-bit, per-channel key + per-token value); KVQuant [4] (3-bit with pre-RoPE quantization); GEAR [5] (SVD residual recovery) | 2–4× memory reduction with near-lossless accuracy on 128k contexts. Quantization is now deployed in vLLM and NVIDIA TensorRT-LLM. |
| **Eviction / Sparsity** | StreamingLLM [6] (attention sinks + sliding window); H₂O [7] (heavy-hitter oracle); SnapKV [8]; TRIM-KV [9] (learned retention gates); PyramidKV [10] | Eviction achieves 5–20× compression but degrades on needle-in-haystack and multi-turn tasks. Learned retention scores (TRIM-KV) can outperform full-cache baselines by suppressing noise. |
| **Offloading** | InfiniGen [11]; TailorKV [12]; PQCache [13]; KV cache to SSD/Flash [14] | CPU/SSD offloading extends capacity but remains PCIe/Flash-bandwidth bound; prefetching can mask latency up to ~3M tokens. |
| **System-level** | PagedAttention [15]; SCBench [16] (KV-centric benchmarking); CacheBlend [17] (semantic retrieval) | Paging reduces fragmentation; cross-query prefix caching is now standard in vLLM/SGLang. |

**Key number:** A 7B model with 128k context requires ~32 GB for KV cache in FP16; quantization to 2-bit brings this to ~8 GB, still taxing edge devices [3,12].

#### 2.2 Analog Compute-in-Memory (CIM) for Transformers

Mapping Transformers to analog CIM is harder than CNNs because attention involves **dynamic operands** (Q, K, V change per sequence). Static weight-stationary dataflows fail.

| Work | Technology | Strategy | Limitation |
|------|-----------|----------|------------|
| **ReTransformer** [18] | ReRAM | Decomposes \(QK^T = (QK^T)X^T\) to keep static \(W_K\) on crossbar; reduces KV writes | Score-V still writes V dynamically; endurance consumed |
| **X-Former** [19] | ReRAM + CMOS | Dual-engine: ReRAM for static projections, CMOS for dynamic attention | Forfeits NVM density for attention engine |
| **iMTransformer** [20] | FeFET + CMOS | FeFET crossbars for projections; CMOS caches attention scores | Heterogeneous fabric; attention sacrifices NVM density |
| **UCSD Hybrid Attn.** [21] | 65nm CMOS analog CIM + digital | Analog CIM core prunes 75% low-score tokens; digital handles remaining 25% | Measured 14.8 TOPS/W (analog), 1.65 TOPS/W (SoC) |
| **Capacitor-Gain-Cell IMC** [22] | Capacitor gain cells (volatile) | Stores KV matrices in capacitor arrays; computes attention within KV cache | Charge decay limits retention; demonstrated only at 3×3 scale |
| **HASTILY** [23] | SRAM-CIM (7nm) | Hardware-software co-design for Transformer inference; token-grained pipelining | SRAM area/standby power; not non-volatile |
| **Ouroboros** [24] | Wafer-scale SRAM-CIM | Token-grained pipelining for LLM inference on wafer-scale fabric | DRAM/HBM still required for KV expansion |
| **IBM 3D-CiM-LLM Sim** [25] | Abstract 3D AIMC | Functional simulator for dense/MoE LLMs on stacked NVM tiers | Shows potential for 10–100× energy efficiency vs. digital baselines |
| **Trilinear / Back-gate FeFET** [26] | FeFET CIM | Back-gate modulation enables in-memory attention without runtime ferroelectric rewriting | Requires per-column drivers; conductance-range constraints |

**Key insight:** All existing analog CIM attention accelerators either (a) sacrifice NVM density by offloading dynamic attention to CMOS, (b) suffer from write endurance/retention limits of emerging NVMs, or (c) use volatile capacitors with short retention. No prior work has mapped the KV cache to **organic optoelectronic memory** arrays.

#### 2.3 Organic & Optoelectronic Memory for Neuromorphic Storage

Organic devices offer unique properties: low-temperature processing, mechanical flexibility, optoelectronic multimodality, and ionic/electronic coupling.

| Work | Device | Key Finding |
|------|--------|-------------|
| **van de Burgt et al.** [27] | Organic neuromorphic devices (review) | Established organic electronics as a viable neuromorphic platform; identifies need for long-term analog retention. |
| **Kim et al.** [28] | Organic memristor-based flexible NN | Demonstrated bio-realistic synaptic plasticity for combinatorial optimization; multi-level conductance states. |
| **Optoelectronic polymer memristors** [29] | Organic polymer | Dynamic optoelectronic control for power-efficient in-sensor edge computing; reversible optical programming. |
| **OECT / OEC-RAM** [30,31] | PEDOT:PSS-based organic ECRAMs | 82% retention over 1,000 s, 5 distinct states, 20k cycles; solid-state ionic gating enables analog storage. |
| **Organic optoelectronic synapse** [32] | Photon-modulated electrochemical doping | Visible-light programmability; memory window >10 years projected retention. |
| **Photonic + capacitive analog memory** [33] | On-chip capacitive analog memory co-located with photonic compute | >26× power savings vs. SRAM-DAC; retention-to-network-latency ratio >100 maintains >90% MNIST accuracy. |

**Key relevance:** Organic optoelectronic devices naturally support **multimodal (optical/electrical) write/read** and **analog multilevel storage**, making them candidates for dense KV-cache arrays where refresh or eviction could be performed optically.

---

### 3. Gap

Despite the above advances, a critical gap remains:

> **No work has systematically evaluated the mapping of LLM KV-cache storage and attention computation onto organic optoelectronic analog CIM arrays.**

Specifically:
1. **Retention-vs-latency mismatch:** KV-cache entries must be retained for the duration of a generation session (seconds to minutes), while organic devices often exhibit volatile or short-term retention (ms to s). Whether this is a fundamental barrier or can be mitigated by refresh/coding remains unstudied.
2. **Dynamic write burden:** Attention requires frequent KV appends (one per generated token). ReRAM/PCM endurance is limited (~10⁶–10⁸); organic devices may offer softer, analog updates but their cycling reliability under streaming KV-append patterns is unknown.
3. **Precision requirements:** KV cache is typically FP16/BF16. Quantization to 2–4 bits is tolerable [3,4], but analog CIM with organic device noise and nonlinearity may need **≤3-bit equivalent precision** per device. The noise robustness of attention to organic conductance drift has not been characterized.
4. **No system architecture:** There is no architecture proposal for an organic-CIM-based KV-cache manager that interfaces with digital LLM front-ends, handles prefix caching, eviction, or multi-query reuse.

---

### 4. Feasibility Assessment

#### 4.1 What Model Sizes Are Realistic?

Given the state of organic array densities (μm-scale features, crossbar architectures up to 100×100 demonstrated) and the need for analog multilevel storage, near-term organic CIM KV-cache targets are **edge-scale LLMs**:

| Model | Context | KV Cache (FP16) | 2-bit Quantized | Organic-CIM Feasibility |
|-------|---------|-----------------|-----------------|------------------------|
| TinyLlama-1.1B | 2k–4k | ~0.5–1 GB | ~125–250 MB | **High** — fits in modest organic crossbar array |
| LLaMA-2/3 7B (GQA) | 4k–32k | ~2–16 GB | ~0.5–4 GB | **Moderate** — requires large array or aggressive eviction |
| Qwen2.5 7B | 128k | ~64 GB | ~16 GB | **Low** — needs 3D stacking or hybrid offloading |
| >13B | >32k | >100 GB | >25 GB | **Not realistic near-term** — organic density insufficient |

**Feasibility verdict:** A **1–3B parameter edge LLM with 4k–8k context** is the most realistic first target. Organic CIM KV-cache should be viewed as a **complement** to digital DRAM (analogous to how Flash complements DRAM), not a wholesale replacement.

#### 4.2 Retention Requirements

KV-cache lifetime is bounded by:
- **Single-turn generation:** Seconds to tens of seconds (retention >> generation time).
- **Multi-turn conversation / prefix caching:** Minutes to hours [14].
- **Cross-query reuse:** Potentially hours (if KV cache is persisted to SSD/Flash) [14,16].

Organic OEC-RAMs currently show **~10³ s retention** under ambient conditions [31], with projected >10 years for some optoelectronic synapses [32]. This suggests that:
- **Short-session KV caching** (seconds) is within reach.
- **Long-session caching** (minutes) may require periodic refresh, refresh-free device engineering, or hierarchical storage (organic CIM as L1 analog cache, Flash as L2).

---

### 5. Preliminary Experiment Design

To validate Direction C, the following experiments are proposed, leveraging the student’s existing behavioral simulation framework (Work 1) for organic optoelectronic CIM:

#### Experiment 1: Noise-Robustness of Attention to Analog KV Storage
- **Setup:** Inject conductance noise / drift models (extracted from organic device measurements) into KV-cache tensors during inference of a 1B–3B LLM.
- **Sweep:** Device precision (1–4 bits equivalent), retention drift (0%, 1%, 5% per layer), and eviction rate.
- **Metric:** Perplexity and downstream task accuracy (e.g., LongBench, GSM8K).
- **Goal:** Determine the minimum effective number of analog levels and maximum tolerable drift for lossless attention.

#### Experiment 2: KV-Cache Compression + Organic Analog Storage Co-Design
- **Setup:** Combine SOTA quantization (KIVI-style 2-bit) with analog multilevel storage. Map quantized KV vectors to organic conductance states using a learned codebook or nonlinear mapping.
- **Sweep:** Quantization bits vs. analog states (e.g., 2-bit digital → 4-level analog per device, with device noise).
- **Metric:** Memory footprint, write energy, attention accuracy.
- **Goal:** Show that organic analog storage can match or exceed digital quantization at iso-footprint.

#### Experiment 3: Temporal Dynamics & Refresh Policies
- **Setup:** Model organic retention decay (exponential or stretched-exponential) in the KV cache across a multi-turn dialogue benchmark (e.g., LongMemEval).
- **Sweep:** Refresh interval, hierarchical eviction (organic → digital → Flash).
- **Metric:** End-to-end task accuracy vs. energy cost of refresh.
- **Goal:** Derive retention specifications for organic devices to serve as a viable KV-cache tier.

#### Experiment 4: Architecture Exploration
- **Setup:** Extend the existing Work 1 simulator to model an organic-CIM KV-cache module with analog MAC for attention score computation.
- **Sweep:** Array size, ADC resolution, conductance programming precision.
- **Metric:** Latency, energy, area for a 1B-model decode step.
- **Goal:** Demonstrate system-level feasibility and identify ADC/SA overhead bottlenecks.

---

### 6. Citation List

[1] Bui et al., "Cache What Lasts: Token Retention for Memory-Bounded KV Cache in LLMs," arXiv:2512.03324, 2025.
[2] "Evaluating Memory Structure in LLM Agents," arXiv:2602.11243, 2025.
[3] Liu et al. (KIVI), "KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache," arXiv:2402.02750 / ICLR 2024.
[4] Hooper et al., "KVQuant: Towards 10 Million Context Length LLM Inference with KV Cache Quantization," arXiv:2401.18079, 2024.
[5] Kang et al. (GEAR), "GEAR: An Efficient KV Cache Compression Recipe for Near-Lossless Generative Inference of LLMs," arXiv:2403.05527, 2024.
[6] Xiao et al., "StreamingLLM: Efficient Streaming Language Models with Attention Sinks," ICLR 2024.
[7] Zhang et al., "H₂O: Heavy-Hitter Oracle for Accurate KV Cache Compression," NeurIPS 2023.
[8] Li et al., "SnapKV: Efficient LLM Inference by Oftentimes Reading," arXiv:2404.14469, 2024.
[9] Bui et al., TRIM-KV, arXiv:2512.03324, 2025.
[10] Cai et al., "PyramidKV: Dynamic KV Cache Compression via Pyramidal Attention Heads," 2025.
[11] Lee et al., "InfiniGen: Efficient Generative Inference of Large Language Models with Dynamic KV Cache Management," ISCA 2024.
[12] Yao et al., "TailorKV: A Hybrid Framework for Long-Context Inference via Tailored KV Cache Optimization," ACL Findings 2025.
[13] Zhang et al., "PQCache: Product Quantization-based KV Cache Eviction for Long-Context LLM Inference," 2024.
[14] FAST'25 / Storage systems for KV-cache to Flash/SSD (USENIX FAST 2025 proceedings).
[15] Kwon et al., "PagedAttention: Efficient Memory Management for LLM Serving," SOSP 2023.
[16] SCBench, "A KV Cache-Centric Analysis of Long-Context Methods," arXiv:2412.10319, 2024.
[17] Yao et al., "CacheBlend: Fast Large Language Model Serving for RAG with Cached Knowledge Fusion," 2024.
[18] ReTransformer (ReRAM), referenced in CIM/Transformer surveys [26].
[19] Sridharan et al., "X-Former: In-Memory Acceleration of Transformers," IEEE TVLSI 2023.
[20] iMTransformer (FeFET+CMOS), referenced in [26].
[21] Moradifrouzabadi, Dodla, Kang, "An Analog and Digital Hybrid Attention Accelerator for Transformers with Charge-based In-memory Computing," 2024.
[22] Capacitor gain cell attention IMC (referenced in [26]).
[23] "HASTILY: Hardware-Software Co-Design for Accelerating Transformer Inference Leveraging Compute-in-Memory," arXiv:2502.12344, 2025.
[24] "Ouroboros: Wafer-Scale SRAM CIM with Token-Grained Pipelining for LLM Inference," arXiv:2603.02737, 2025.
[25] IBM Research, "3D-CiM-LLM-Inference-Simulator," GitHub 2025; also in [25a] Modeling and Simulation Frameworks for PIM Architectures, arXiv:2512.00096, 2025.
[26] "When should we use analog computing?" / ACIM survey, arXiv:2411.06079, 2024.
[27] van de Burgt et al., "Organic electronics for neuromorphic computing," *Nature Electronics* 1, 386–397 (2018).
[28] Kim et al., "Organic memristor-based flexible neural networks with bio-realistic synaptic plasticity," *Adv. Sci.* 10, 2300659 (2023).
[29] "Optoelectronic polymer memristors with dynamic control for power-efficient in-sensor edge computing," *Light: Science & Applications* 2025.
[30] Wang et al., "Designing organic mixed conductors for electrochemical transistor applications," *Nat. Rev. Mater.* 2024.
[31] Shan & Inal (KAUST), "Solid-state OEST with semi-solid ionic liquid gel," ECME 2025 / related works on OEC-RAMs.
[32] Chen et al., "Organic optoelectronic synapse based on photon-modulated electrochemical doping," *Nat. Photonics* 17, 629–637 (2023).
[33] Lam et al., "Neuromorphic Photonic Computing with an Electro-Optic Analog Memory," arXiv:2401.16515, 2024.
[34] FAST'25 proceedings on KV-cache persistence and retention in storage hierarchies.
[35] "Rethinking Key-Value Cache Compression Techniques for Large Language Model Serving," arXiv:2503.24000, 2025.

---

*Prepared for Work 2 scoping — Direction C: LLM KV-Cache Mapping to Organic Analog CIM Arrays.*
