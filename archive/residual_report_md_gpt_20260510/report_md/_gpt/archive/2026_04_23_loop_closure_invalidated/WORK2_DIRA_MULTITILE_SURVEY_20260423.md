# Work 2 Direction A — Literature Survey: Multi-Tile Organic CIM Array Mapping & Communication

**Date:** 2026-04-23
**Scope:** Tiled CIM architectures, NN mapping strategies, inter-tile communication, and multi-tile Vision-Transformer acceleration (2022–2026).
**Relevance filter:** Direct > Indirect > Inspirational for organic optoelectronic CIM edge inference.

---

## 1. Motivation: Why Multi-Tile Matters for Scaling

Work 1 demonstrated that a single organic photodetector-array CIM chip can execute Tiny-ViT / ConvNeXt on CIFAR-10. However, monolithic arrays face hard physical limits:
- **IR-drop & parasitics** cap practical crossbar dimensions (typically <1k×1k for organic/OPD arrays).
- **Yield & fabrication variability** favor smaller, identical tiles that can be defect-mapped or reconfigured.
- **Model size growth** (even compact ViTs) exceeds on-chip weight storage; tiling enables layer-wise or channel-wise partitioning.
- **Energy/latency trade-offs**: Analog CIM saves MAC energy, but inter-tile data movement can erase gains if the network-on-chip (NoC) is poorly matched to the activation traffic.

Conclusion: a multi-tile organic CIM system is not optional for scaling beyond single-chip demos—it is a prerequisite for practical edge deployment.

---

## 2. SOTA Landscape (5 Key Works)

### A. CLSA-CIM — Cross-Layer Scheduling for Tiled CIM *(Direct)*
- **Ref:** R. Pelke *et al.*, “CLSA-CIM: A Cross-Layer Scheduling Approach for Computing-in-Memory Architectures,” *DATE*, 2024.
- **Key finding:** On an RRAM tiled CIM with weight duplication, cross-layer scheduling improves PE utilization by up to **17.9×** and end-to-end inference speedup by **29.2×** vs. naive layer-by-layer scheduling.
- **Relevance:** Directly applicable to organic CIM scheduling. The paper explicitly notes that inter-tile data-movement cost was *not* differentiated; this is the exact gap a multi-tile organic study must close.

### B. Hemlet — Heterogeneous CIM Chiplet for ViT *(Direct)*
- **Ref:** C. Wang *et al.*, “Hemlet: A Heterogeneous Compute-in-Memory Chiplet Architecture for Vision Transformers with Group-Level Parallelism,” arXiv:2511.15397, 2025.
- **Key finding:** ACIM (RRAM) + DCIM (SRAM) + IDP chiplets interconnected via a 256 GB/s mesh NoP. Proposed Group-Level Parallelism (GLP) interleaves columns across ADC groups, boosting ACIM throughput by resolving ADC-serialization bottlenecks. Achieves **9.56 TOPS** and **4.98 TOPS/W** on ViT-B/16.
- **Relevance:** Strongest direct precedent. Shows that chiplet/partitioning overhead can be masked by fine-grained pipelining and blocked dynamic VMMs. The GLP concept can be ported to organic tiles by treating each OPD sub-array group as a parallel channel.

### C. LionHeart — Layer-Based Mapping for Analog IMC Tiles *(Direct)*
- **Ref:** C. Lammie *et al.*, “LionHeart: A Layer-Based Mapping Framework for Heterogeneous Systems with Analog In-Memory Computing Tiles,” *IEEE Trans. Emerg. Top. Comput.*, 2025.
- **Key finding:** Hybrid analog–digital mapping guided by a user-specified accuracy threshold. Hardware-aware retraining + analog noise injection yields **>6× runtime reduction** and energy-efficiency gains vs. fully digital FP baselines.
- **Relevance:** Provides the mapping heuristic (which layers go analog vs. digital) that a multi-tile organic system will need when some tiles are too noisy for sensitive layers (e.g., final classifier).

### D. X-Former — Hybrid NVM/CMOS Transformer Accelerator *(Indirect)*
- **Ref:** S. Sridharan *et al.*, “X-Former: In-Memory Acceleration of Transformers,” *IEEE Trans. Comput.*, 2023.
- **Key finding:** ReRAM tiles for static weights, SRAM tiles for dynamic MHA computations; sequence-blocking dataflow overlaps SRAM and ReRAM execution. **69.8× latency reduction** vs. GPU baseline.
- **Relevance:** Demonstrates that static/dynamic workload splitting is essential for transformers. Organic CIM must similarly decide whether to keep attention-generated weights in volatile SRAM-like buffers or write them back to photodetector arrays.

### E. IBM HERMES / 64-Core PCM Chip *(Inspirational)*
- **Ref:** IBM Research, “HERMES-Core” (ISSCC 2022) and follow-up 64-core PCM chip (2023); inter-tile PWM signaling demonstrated.
- **Key finding:** First large-scale memristor chip with integrated inter-tile communication. PWM-based analog communication between tiles reduces ADC/DAC conversion cost.
- **Relevance:** Suggests that organic CIM could exploit analog or mixed-signal inter-tile links (e.g., current-mode or photonic waveguides) rather than full digitization at every hop.

---

## 3. The Gap: What Is Missing That This Student Could Fill

| Dimension | Existing SOTA | Missing Piece (Student Opportunity) |
|-----------|---------------|-------------------------------------|
| **Technology** | RRAM, PCM, SRAM CIM dominate literature. | **Organic/OPD photodetector arrays** have unique constraints: low on/off ratio, photo-bleaching drift, and large pixel pitch. No prior work models multi-tile communication for organic CIM. |
| **Partitioning** | Layer-wise (Hemlet, LionHeart) or weight-duplication (CLSA-CIM). | **Channel-wise tiling + adaptive remapping** under organic device non-idealities (variability, temporal drift) is unstudied. |
| **Inter-tile comm.** | NoC-mesh (ISAAC, PUMA), NoP-mesh (Hemlet), PWM analog links (IBM). | **Energy/latency model of analog inter-tile links specific to organic CIM**—including whether to digitize at tile boundaries or forward analog partial sums. |
| **ViT on tiled CIM** | Hemlet targets big ViT (ImageNet); X-Former uses ReRAM+SRAM. | **Tiny-ViT / ConvNeXt on resource-constrained organic tiles** with full-stack accuracy-energy co-optimization. |
| **Simulators** | NeuroSim, MNSIM, CrossSim support hierarchical tiles. | **No simulator includes organic photodetector device models + multi-tile NoC energy.** Work 1’s framework can be extended to fill this. |

**Bottom line:** The student can be first to systematically answer: *“Given organic CIM’s noise, area, and bandwidth constraints, how should a Tiny-ViT be partitioned across tiles, and what is the optimal analog/digital boundary for inter-tile data?”*

---

## 4. Feasibility Assessment

- **Simulator base:** Work 1 already has a PyTorch→organic-CIM inference pipeline. Extending it to model multiple tiles with configurable NoC bandwidth and tile-to-tile energy is straightforward (add a network latency model per tensor transfer).
- **Device data:** Organic OPD arrays from literature show 32×32 to 128×128 feasible sizes; multi-tile simply replicates these with modeled inter-tile wire/load capacitance.
- **Partitioning search space:** For Tiny-ViT (~5M params) and CIFAR-10, the layer count is small enough that exhaustive or heuristic (genetic) mapping search is tractable.
- **Risk:** Inter-tile communication energy could dominate if every activation is digitized and packetized. Mitigation: explore analog current-mode buses or time-domain signaling between nearby tiles.

---

## 5. Preliminary Experiment Design

1. **Baseline:** Single-tile organic CIM (Work 1) for Tiny-ViT on CIFAR-10.
2. **Tile model:** Instantiate *N* identical organic CIM tiles (e.g., N = 2, 4, 8). Each tile has:
   - Fixed array size (e.g., 64×64 or 128×128 OPD pixels)
   - Local ADC + buffer
   - Inter-tile link with parameterized bandwidth & energy/bit
3. **Mapping strategies to compare:**
   - **Layer-wise:** Each tile holds 1 or more complete layers.
   - **Channel-wise (GLP-inspired):** Split output channels across tiles for Conv/FC layers.
   - **Weight-duplication + cross-layer (CLSA-CIM-inspired):** Duplicate hot weights to adjacent tiles to reduce fan-in traffic.
4. **Metrics:** End-to-end latency, total energy (compute + communication), CIFAR-10 accuracy under organic noise models.
5. **Sensitivity sweep:** NoC bandwidth (1–256 GB/s), tile count (1–8), analog vs. digitized inter-tile links.

---

## 6. Citation List

1. R. Pelke *et al.*, “CLSA-CIM: A Cross-Layer Scheduling Approach for Computing-in-Memory Architectures,” *DATE*, 2024.
2. C. Wang *et al.*, “Hemlet: A Heterogeneous Compute-in-Memory Chiplet Architecture for Vision Transformers with Group-Level Parallelism,” arXiv:2511.15397, 2025.
3. C. Lammie *et al.*, “LionHeart: A Layer-Based Mapping Framework for Heterogeneous Systems with Analog In-Memory Computing Tiles,” *IEEE Trans. Emerg. Top. Comput.*, 2025.
4. S. Sridharan *et al.*, “X-Former: In-Memory Acceleration of Transformers,” *IEEE Trans. Comput.*, 2023.
5. A. Shafiee *et al.*, “ISAAC: A Convolutional Neural Network Accelerator with In-Situ Analog Arithmetic in Crossbars,” *ISCA*, 2016.
6. A. Ankit *et al.*, “PUMA: A Programmable Ultra-Efficient Memristor-Based Accelerator for Machine Learning Inference,” *ASPLOS*, 2019.
7. M. Stanisavljevic *et al.*, “HERMES-Core — A 1.9-TOPS/mm² PCM on 14-nm CMOS In-Memory Compute Core,” *JSSC*, 2022.
8. IBM Research, 64-core PCM chip with inter-tile PWM signaling, *IEDM/VLSI*, 2023.
9. S. Yu *et al.*, “NeuroSim: A Circuit-Level Macro Model for Benchmarking Neuro-Inspired Architectures in Online Learning,” *TCAD*, 2018.
10. Y. Wang *et al.*, “A Spatial-Designed CIM Architecture Based on Monolithic 3D Integration,” *ASPLOS*, 2025 (inter-tile latency analysis).

---
*Prepared for Master’s thesis Work 2 scoping — Direction A: Multi-Tile Organic CIM.*
