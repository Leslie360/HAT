# HAT Research Directions — Future Opportunities

This document catalogs potential research and engineering directions for HAT
(Hardware-Aware Training with analog KV cache), prioritized by feasibility and
expected impact.

---

## P0: Immediate Deliverables

### 1. Autonomous Driving / Alpamayo VLM Scene Validation (Paper)

HAT's three selling points—deterministic latency, low power, small area—map
directly onto autonomous driving requirements.

**Path:**
- Fine-tune a VLM (e.g. Qwen2-VL) on Alpamayo / driving data
- Apply HAT analog KV cache (last1/last2) via existing training pipeline
- Evaluate: perplexity degradation, downstream perception task accuracy,
  energy/area projection

**Deliverable:** An application-driven paper—"HAT for Autonomous Driving VLM"—
  with real scenes, power modeling, and task-level accuracy.

**Timeline:** Data prep 1-2wk + experiments 2-4wk = 1-2mo to first draft.

**Why P0:** The author has data, domain expertise, and evaluation pipeline.
  Directly reusable code from p3_hat_train.py.

---

### 2. Noise-Scaling Laws for Analog KV Cache (Short Paper)

Existing data across 410M / 2.8B / 6.9B already supports a preliminary fit
of perplexity drop as a function of noise sigma and model scale.

**Key questions:**
- PPL_drop(sigma, N) = alpha * N^(-beta) * sigma^gamma ?
- How many extra parameters compensate a given noise budget?
- KV cache effective bit-width as log2(n_states): isomorphic to
  quantization-aware scaling laws.
- Compute-optimal HAT: choose digital vs analog layers, n_states, bit-width
  under a chip area constraint (analogous to Chinchilla but with area PPA).

**Deliverable:** A 4-6 page workshop / short paper.

**Timeline:** Analysis 1wk + 1-2 extra scale points 1-2wk = 2-3wk.

**Why P0:** Data already exists. No blocking dependency. Parallelizable with
  Paper 2.

---

## P1: Engineering + Paper

### 3. HAT + SGLang Integration (System Paper + Open-Source)

SGLang's RadixAttention has an explicit prefix-tree KV cache manager, making
it easier than vLLM to identify analog vs digital layer boundaries.

**Research problem:** HAT noise accumulation under prefix cache reuse—if a
  cached analog KV prefix is read multiple times, does the noise compound or
  stay independent per read? This is an unstudied question with direct
  deployment implications.

**Engineering:**
- Modify SGLang KV cache manager to accept an AnalogLinear backend for
  specified layers
- Integrate the HAT fused CUDA kernel (see #4 below) as the compute backend

**Deliverable:** MLSys / EuroSys-class system paper + open-source inference
  framework contribution.

**Timeline:** 3-4 months. Recommends completing #4 first.

---

### 4. HAT Inference CUDA Kernel (HPC: Ops / Fusion / Graph)

Current AnalogLinear is a naive PyTorch implementation: separate noise sampling
and matmul. A production kernel fuses the full pipeline.

**Fused kernel scope:**
- Noise sampling (uniform → normal via Box-Muller or sum-of-uniforms
  approximation for RRAM/PCM device distributions)
- Quantization to analog conductance levels
- Analog matmul (with structured noise injection inline)
- Dequantization to digital

**Compute graph / compiler angle:**
- HAT's compute pattern (contiguous matmul + element-wise noise) is a good
  benchmark for TorchDynamo / Triton auto-tuning
- The layer serves as a stress-test case for compiler fusion policies

**HAT + FlashAttention coexistence:**
- FlashAttention fuses QK^T→PV inside the attention computation
- HAT only touches the KV storage medium, not the attention logic
- The two fused kernels are independent and can stack in the memory hierarchy

**Deliverable:** Technical report + open-source CUDA kernel.

**Timeline:** 2-4 weeks for initial kernel.

---

## P2: Exploratory (Higher Risk)

### 5. RL (PPO / GRPO) + HAT

HAT noise injection acts as a stochastic regularizer. In RL this could either:
- Stabilize policy updates by preventing overfitting to early rollouts
- Destabilize by corrupting value function estimates

**Path:**
- Start with GRPO (no critic, group-based advantage) to avoid value-model
  complexity
- Validate convergence on GSM8K-scale tasks with 410M models
- If stable, scale up

**Deliverable:** Methodology paper.

**Risk:** Convergence not guaranteed. Recommend small-model exploration in
  parallel with P0/P1 work.

**Timeline:** 3-6 months.

---

### 6. vLLM Integration

PagedAttention's opaque block-level KV cache management makes layer-level HAT
harder than SGLang. However, vLLM has broader community adoption.

Recommend deferring until SGLang integration (#3) provides experience to
inform the vLLM approach.

---

## P3: Lower Priority

### 7. DeepSpeed ZeRO Compatibility

Pure engineering: AnalogLinear's noise-injection buffers need to be marked as
`_ddp_params_and_buffers_to_ignore` so ZeRO-3 doesn't partition them.
Not a research problem.

### 8. HPC Positioning (Narrative Only)

Analog noise injection can be framed as a new precision tier between fp32 and
fp16—trading controlled accuracy loss for energy/area gains. HPC communities
have long adopted approximate computing (mixed precision, algorithmic noise).
Can be developed as a positioning statement without experiments.

### 9. Drone / UAV VLM

Power-constrained scenario where HAT's benefit is strongest, but requires
either a dataset (UAVDT + VLM) or a collaborator. Low priority without either.

---

## Recommended Parallel Path

| Who | What | Timeline |
|-----|------|----------|
| Author | Alpamayo driving scene | 1-2 months |
| Assistant (Claude) | Noise-Scaling Law analysis | 2-3 weeks |
| Joint | SGLang + CUDA kernel | After Paper 2 wraps |

Scaling law and Alpamayo can run fully independently of each other. SGLang
integration depends on the CUDA kernel being available first.
