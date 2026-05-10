<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# Work 2 Experiment Plan — Detailed Executable Design

**Date:** 2026-04-23
**Authority:** `CLAUDE_WORK2_DIRECTION_LOCK_20260423.md` + `KIMI_WORK2_SCOPE_LOCK_20260423.md`
**Owner:** Kimi (executable design); Codex (GPU execution, CX-L series)

---

## 0. Infrastructure Assumptions

- **Simulator base:** `compute_vit` repo's `AnalogLinear`/`AnalogConv2d` classes from Work 1, extended for KV-cache tensors
- **LLM framework:** HuggingFace `transformers` + `datasets`
- **Primary model:** `TinyLlama/TinyLlama-1.1B-intermediate` (HF checkpoint)
- **Secondary model:** `meta-llama/Llama-2-7b-hf` with GQA (requires HF auth)
- **GPU:** RTX 5070 Ti 16GB (primary); A100 40GB available for 7B if needed
- **Python env:** `LLM` conda env (PyTorch 2.10.0+cu128)

---

## 1. Experiment 1: Noise-Robustness of Attention to Analog KV Storage (P0, CX-L2)

### 1.1 Question
What is the minimum analog-state count N and maximum tolerable conductance noise σ for lossless attention?

### 1.2 Setup

**Code path:** `compute_vit/scripts/_gpt/cx_l2_kv_noise_sweep.py`

**Model:** TinyLlama-1.1B (1.1B params, 2048 default context)

**Dataset:**
- WikiText-103 (validation split, 10k tokens for fast PPL)
- LongBench subset: HotpotQA (500 examples), NarrativeQA (200 examples)

**KV-cache instrumentation:**
```python
# Hook into model.layers[i].self_attn.k_proj / v_proj output
# Apply organic conductance noise model:
#   G_noisy = G + N(0, σ²) + d2d_noise(fixed per instance)
#   where G = codebook_lookup(KV_float)
```

**Noise model parameters (from Work 1):**
| Parameter | Value | Source |
|-----------|-------|--------|
| `sigma_c2c` | 0.01–0.10 | Uniform, per-forward Gaussian |
| `sigma_d2d` | 0.05 | Fixed per instance, Gaussian |
| `n_states` | N ∈ {2,3,4,5,6} | Quantization levels |
| `NL_LTP` | 1.0 | Protected NL (groupwise) |
| `NL_LTD` | -1.0 | Protected NL (groupwise) |
| `noise_mode` | "uniform" | From Work 1 |

### 1.3 Sweep Grid

| Dimension | Values | Total Combinations |
|-----------|--------|-------------------|
| N (analog states) | 2, 3, 4, 5, 6 | 5 |
| σ_c2c | 0.00, 0.01, 0.02, 0.05, 0.10 | 5 |
| σ_d2d | 0.00, 0.05 | 2 |
| Inject target | K-only, V-only, K+V | 3 |
| **Total runs** | | **150** |

Each run = 1 full inference pass over WikiText-103 val + 1 pass over LongBench subset.

### 1.4 Metrics & Output

```json
{
  "config": {"n_states": 4, "sigma_c2c": 0.05, "sigma_d2d": 0.05, "inject": "K+V"},
  "wikitext_ppl": 12.34,
  "wikitext_ppl_delta_vs_fp16": 0.45,
  "hotpotqa_f1": 0.72,
  "narrativeqa_em": 0.45,
  "runtime_seconds": 180
}
```

**Visualization:** 2D contour plot (N vs. σ_c2c) with color = ΔPPL vs FP16.

### 1.5 Expected Runtime
- ~3 min per run (TinyLlama-1.1B on RTX 5070 Ti, WikiText-103 val)
- 150 runs × 3 min = **~7.5 GPU-hours**

---

## 2. Experiment 4: Architecture Exploration (P0, CX-L5)

### 2.1 Question
What array size, ADC resolution, and conductance programming precision are needed for a 1B-model decode step?

### 2.2 Setup

**Code path:** `compute_vit/scripts/_gpt/cx_l5_architecture_sweep.py`

**System model:** Extend Work 1 simulator with KV-cache crossbar module

**Architecture components:**
```
KV-Cache Array (organic crossbar)
  ├─ Array size: M×N (M rows = head_dim, N cols = max_seq_len)
  ├─ Cell: organic OEC-RAM, N_states conductance levels
  ├─ Read: current-mode MAC (Q·K^T) via crossbar
  ├─ ADC: N-bit flash/SAR ADC per column
  └─ Digital peripheral: softmax, top-k, accumulator
```

**Energy model (from Work 1 + literature):**
| Component | Energy Formula | Reference |
|-----------|---------------|-----------|
| Analog MAC | 0.1 pJ per 8b MAC | [HASTILY] scaled by array size |
| ADC (N-bit) | 2^N × 0.5 fJ/conv | Walden FOM, scaled |
| Conductance write | 10 pJ per cell | Organic OEC-RAM [31] |
| Refresh (optical) | 1 pJ per cell | Projected from [32] |

### 2.3 Sweep Grid

| Dimension | Values | Notes |
|-----------|--------|-------|
| Array size | 64×64, 128×128, 256×256, 512×512 | Limited by organic die size |
| ADC bits | 4, 6, 8 | Lower = faster, higher = precision |
| Programming precision | 1%, 5%, 10% | σ_program / full_range |
| N_states | 4, 8, 16 | Per-cell analog levels |
| **Total configs** | | **48** |

### 2.4 Metrics & Output

Per decode step (1 token, 1 layer, 1 head):
```json
{
  "config": {"array_size": 256, "adc_bits": 6, "prog_precision": 0.05, "n_states": 8},
  "latency_ns": 450,
  "energy_pj": 1200,
  "area_um2": 65536,
  "snr_db": 28.5,
  "accuracy_vs_fp16": 0.98
}
```

**Visualization:** 3D Pareto surface (latency, energy, area) with accuracy as color.

### 2.5 Expected Runtime
- Simulator-only (no LLM forward): ~10 sec per config
- 48 configs × 10 sec = **~8 GPU-minutes** (lightweight)

---

## 3. Experiment 2: KV-Cache Compression + Organic Analog Co-Design (P1, CX-L3)

### 3.1 Question
Can organic analog storage match or exceed digital quantization at iso-footprint?

### 3.2 Setup

**Code path:** `compute_vit/scripts/_gpt/cx_l3_quantization_sweep.py`

**Baseline:** KIVI-style asymmetric per-channel quantization
- Keys: per-channel (per head) scale + zero-point
- Values: per-token scale + zero-point

**Organic mapping:**
```python
# Learned codebook (K-means on calibration set)
codebook = kmeans(KV_calibration, n_clusters=N_states)
G = codebook.centers[G_idx]  # map to conductance
# Add device noise
G_noisy = G + organic_noise(G, sigma_c2c, sigma_d2d)
```

### 3.3 Sweep Grid

| Dimension | Values |
|-----------|--------|
| Digital quant bits | 2, 3, 4 |
| Analog states | 4, 8, 16 |
| Codebook | uniform, learned (K-means) |
| Device noise | σ_c2c ∈ {0.00, 0.05} |

### 3.4 Metrics
- Memory footprint: bits per KV element
- Write energy: total Joules to program KV cache for 4k context
- Attention accuracy: cosine similarity of attention scores vs. FP16

### 3.5 Expected Runtime
- ~5 min per config
- 48 configs × 5 min = **~4 GPU-hours**

---

## 4. Experiment 3: Temporal Dynamics & Refresh Policies (P1, CX-L4)

### 4.1 Question
What refresh interval and hierarchical eviction policy maximize task accuracy vs. energy?

### 4.2 Setup

**Code path:** `compute_vit/scripts/_gpt/cx_l4_retention_sweep.py`

**Retention model:** Exponential decay
```python
G(t) = G_min + (G_programmed - G_min) × exp(-t / τ)
```

**Session simulation:**
- Multi-turn dialogue: 5 turns × 512 tokens each
- KV cache grows linearly; oldest tokens decay

### 4.3 Sweep Grid

| Dimension | Values |
|-----------|--------|
| Retention τ | 1s, 10s, 100s, 1000s |
| Refresh interval | none, 1s, 10s, 100s |
| Eviction policy | FIFO, LRU, attention-threshold |
| Hierarchy | flat, L1(organic)+L2(SRAM) |

### 4.4 Metrics
- End-to-end task accuracy (MT-Bench win-rate vs. FP16)
- Total energy = compute + refresh + eviction overhead

### 4.5 Expected Runtime
- ~10 min per config (multi-turn simulation)
- 64 configs × 10 min = **~10 GPU-hours**

---

## 5. Execution Order & Dependencies

```
Week 1 (Apr 23–30):
  CX-L1: TinyLlama baseline + infra bring-up
    └─→ Enables all downstream experiments
  CX-L2: Exp 1 (noise-robustness) — P0, start immediately after L1
    └─→ Informs minimum N and σ for L3/L4/L5

Week 2 (Apr 30–May 7):
  CX-L5: Exp 4 (architecture) — P0, simulator-only, parallel with L2
  CX-L3: Exp 2 (quantization) — P1, starts after L2 completes
  CX-L4: Exp 3 (retention) — P1, starts after L2 completes
```

**Critical path:** L1 → L2 → (L3 + L4). L5 is simulator-only and can run in parallel with L2.

---

## 6. Code Skeleton

```
compute_vit/
  scripts/_gpt/
    cx_l1_baseline.py          # TinyLlama FP16 baseline
    cx_l2_kv_noise_sweep.py    # Exp 1
    cx_l3_quantization_sweep.py # Exp 2
    cx_l4_retention_sweep.py    # Exp 3
    cx_l5_architecture_sweep.py # Exp 4
  kv_cim_simulator/            # NEW: KV-cache CIM simulation module
    __init__.py
    kv_array.py                # Organic crossbar array model
    noise_models.py            # Conductance noise + retention
    energy_model.py            # Latency/energy/area calculator
    codebook.py                # Quantization ↔ conductance mapping
```

---

## 7. Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| TinyLlama baseline PPL too high | Fallback to GPT-2-medium (smaller, known-good) per pre-authorized trigger |
| L2 shows collapse at σ > 0.01 | Report as scientific finding; pitch becomes "graceful degradation" not "lossless" |
| Simulator accuracy questioned | Validate against Work 1 ViT results (known-good analog model); cite [25] IBM 3D-CiM-LLM simulator methodology |
| 7B model OOM on RTX 5070 Ti | Use 4-bit base model (bitsandbytes) or offload to CPU; or skip 7B and scope to 1B only |

---

## 8. Deliverables Checklist

- [ ] `cx_l1_tinyllama_baseline.json` — FP16 PPL baseline
- [ ] `cx_l2_noise_sweep.json` — 150-config grid
- [ ] `cx_l3_quantization_sweep.json` — 48-config grid
- [ ] `cx_l4_retention_sweep.json` — 64-config grid
- [ ] `cx_l5_architecture_pareto.json` — 48-config grid
- [ ] `KIMI_WORK2_ANALYSIS_20260430.md` — synthesis memo after all data lands

---

*Executable design locked 2026-04-23. Modifications require Kimi + Codex agreement.*
