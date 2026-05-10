<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# Work 2 Scope Lock — LLM KV-Cache Mapping to Organic Optoelectronic CIM

**Date:** 2026-04-23
**Authority:** `CLAUDE_WORK2_DIRECTION_LOCK_20260423.md`
**Scope:** Paper-2 (English) + Thesis Chapter 6-7 (Chinese)

---

## 1. One-Sentence Claim

> Organic optoelectronic analog CIM is the only emerging memory technology whose retention-endurance-optical properties intrinsically match the KV-cache access pattern of edge LLM inference; we provide the first physics-grounded simulation benchmark that proves it.

---

## 2. Target Models & Context

| Model | Parameters | Context | Role | Rationale |
|-------|-----------|---------|------|-----------|
| **TinyLlama-1.1B** | 1.1B | 2k–4k (expandable to 8k) | **Primary** | Fits single organic crossbar array; fast simulation turnaround; edge-representative |
| **LLaMA-2-7B (GQA)** | 7B | 4k–32k | **Secondary** | Validates scaling to GQA/MQA; tests array-size limits |
| Qwen2.5-7B | 7B | 128k | **Out of scope** | Requires 3D stacking / hybrid offloading; not realistic near-term |

**Simulation-only acceptable for Master's.** One small-array experimental validation is a stretch goal (post-thesis).

---

## 3. Exact Benchmark List

### 3.1 Perplexity (Primary Metric)
- **WikiText-103** [Merity et al., 2016] — standard language modeling benchmark
- Reporting: perplexity (PPL) with 95% CI over 3 random seeds
- Baselines to report against: FP16, KIVI-2bit, KIVI-4bit

### 3.2 Downstream Tasks (Secondary)
| Task | Dataset | Metric | Why It Matters |
|------|---------|--------|----------------|
| Long-context QA | LongBench subset (HotpotQA, NarrativeQA) | F1 / EM | Tests attention-rank preservation under noisy KV |
| Reasoning | GSM8K | Accuracy | Tests whether KV noise corrupts chain-of-thought |
| Multi-turn | MT-Bench (subset) | Win-rate vs. FP16 | Tests retention across session boundaries |

### 3.3 System Metrics
| Metric | Unit | How Measured |
|--------|------|--------------|
| Energy per decode step | pJ/token | Simulator energy model (analog MAC + ADC + refresh) |
| Area per KV-cache tier | mm² | Crossbar array area model (μm-scale pitch) |
| Write endurance | cycles/layer | Organic device model (10³–10⁴) |
| Retention time | s | Exponential decay model fitted to device data |

---

## 4. Baselines (Fair-Comparison Matrix)

| Baseline | Technology | What We Compare | Pitfall to Avoid |
|----------|-----------|-----------------|-----------------|
| **FP16** | Digital DRAM | Upper-bound accuracy | Do not claim "we beat FP16"; claim "we approach FP16 at X× energy reduction" |
| **KIVI-2bit** [Liu et al., ICLR 2024] | Digital SRAM/DRAM + 2-bit quant | Iso-memory accuracy | KIVI is per-channel asymmetric; our analog mapping must use comparable granularity |
| **KIVI-4bit** | Digital SRAM/DRAM + 4-bit quant | Accuracy-compression trade-off | Same as above |
| **SRAM-CIM** [HASTILY, Ouroboros] | 7nm SRAM crossbar | Iso-technology energy/area | SRAM is volatile; our comparison must factor in refresh/standby power |
| **Oxide-RRAM-CIM** [ReTransformer, X-Former] | HfO₂ ReRAM crossbar | Organic-specific moat | RRAM retention is years (over-specced) and endurance ~10⁶; organic is softer but optically refreshable |

---

## 5. Prioritized Experiment Plan

### Exp 1 — Noise-Robustness of Attention to Analog KV Storage (P0, CX-L2)
**Question:** What is the minimum analog-state count N and maximum tolerable conductance noise σ for lossless attention?

- **Setup:** Instrument HuggingFace TinyLlama-1.1B KV cache with organic conductance noise model (from Work 1 simulator)
- **Sweeps:**
  - Device precision: N ∈ {2, 3, 4, 5, 6} levels
  - Conductance noise: σ ∈ {0.01, 0.02, 0.05, 0.10} of LSB
  - Independent K vs. V noise injection
- **Metrics:** WikiText-103 PPL, LongBench F1
- **Deliverable:** `cx_l2_noise_sweep.json` + noise-robustness contour plot

### Exp 4 — Architecture Exploration (P0, CX-L5)
**Question:** What array size, ADC resolution, and conductance programming precision are needed for a 1B-model decode step?

- **Setup:** Extend Work 1 simulator to model organic-CIM KV-cache module with analog MAC for attention scores
- **Sweeps:**
  - Array size: 64×64, 128×128, 256×256, 512×512
  - ADC bits: 4, 6, 8
  - Programming precision: 1%, 5%, 10% of full range
- **Metrics:** Latency (μs/token), energy (pJ/token), area (mm²)
- **Deliverable:** `cx_l5_architecture_pareto.json` + Pareto-front plot

### Exp 2 — KV-Cache Compression + Organic Analog Co-Design (P1, CX-L3)
**Question:** Can organic analog storage match or exceed digital quantization at iso-footprint?

- **Setup:** Map KIVI-style quantized KV vectors to organic conductance states using learned/non-uniform codebook
- **Sweeps:**
  - Digital quantization bits: 2, 3, 4
  - Analog states per device: 4, 8, 16
  - Codebook: uniform vs. learned (K-means on calibration set)
- **Metrics:** Memory footprint, write energy, attention accuracy
- **Deliverable:** `cx_l3_quantization_sweep.json`

### Exp 3 — Temporal Dynamics & Refresh Policies (P1, CX-L4)
**Question:** What refresh interval and hierarchical eviction policy maximize task accuracy vs. energy?

- **Setup:** Model exponential retention decay (τ ∈ {1s, 10s, 100s, 1000s}) across multi-turn dialogue
- **Sweeps:**
  - Refresh interval: none, 1s, 10s, 100s
  - Eviction policy: FIFO, LRU, attention-score threshold
  - Hierarchy: organic-CIM L1 → digital SRAM L2 → Flash L3
- **Metrics:** End-to-end task accuracy vs. total energy
- **Deliverable:** `cx_l4_retention_sweep.json`

---

## 6. Scope Boundaries (What We Will NOT Do)

| Out of Scope | Why |
|--------------|-----|
| >7B models | Organic density insufficient; 7B GQA is stretch goal only |
| >32k context | Requires 3D stacking or hybrid offloading; not organic-specific contribution |
| On-device training for KV cache | Endurance too low; that's Direction B (shelved to Ch.8) |
| Production deployment claim | Simulation-only thesis; prototype claim only |
| Full optoelectronic co-design (photodiode + CIM weights) | Direction D insight folds into §3.x frontend subsection, not standalone |
| Multi-tile / chiplet scaling | Direction A insight folds into §3 architecture-exploration subsection |

---

## 7. Deliverables & Timeline

| Deliverable | Path | Owner | Deadline |
|-------------|------|-------|----------|
| Scope lock (this doc) | `report_md/_gpt/KIMI_WORK2_SCOPE_LOCK_20260423.md` | Kimi | 2026-04-23 |
| Experiment plan | `report_md/_gpt/KIMI_WORK2_EXPERIMENT_PLAN_20260423.md` | Kimi | 2026-04-24 |
| Paper-2 skeleton v1 | `paper/paper2/skeleton_v1/SKELETON.md` | Kimi | 2026-04-25 |
| Paper-2 abstract | `paper/paper2/skeleton_v1/00_abstract.md` | Kimi | 2026-04-25 |
| Retention theory | `report_md/_gpt/GEMINI_WORK2_RETENTION_THEORY_20260423.md` | Gemini | 2026-04-24 |
| Quantization floor | `report_md/_gpt/GEMINI_WORK2_QUANTIZATION_FLOOR_20260423.md` | Gemini | 2026-04-25 |
| TinyLlama baseline | `report_md/_gpt/json_gpt/cx_l1_tinyllama_baseline.json` | Codex | 2026-04-26 |
| Noise sweep | `report_md/_gpt/json_gpt/cx_l2_noise_sweep.json` | Codex | 2026-04-28 |

---

## 8. Narrative Arc for Thesis Defense

1. **Ch.3-5 (Work 1):** Organic CIM inference of ViTs under severe NL → falsification, structural limit, mitigations tested and rejected.
2. **Ch.6-7 (Work 2):** Organic CIM storage of KV-cache for LLM inference → structural fit, retention match, simulation demonstration, architecture proposal.
3. **Ch.8 (Outlook):** Joint opto-electronic co-design (Direction D), CL on rewritable organic arrays (Direction B), multi-tile scaling (Direction A).

---

*Locked by Claude 2026-04-23. Modifications require architect approval.*
