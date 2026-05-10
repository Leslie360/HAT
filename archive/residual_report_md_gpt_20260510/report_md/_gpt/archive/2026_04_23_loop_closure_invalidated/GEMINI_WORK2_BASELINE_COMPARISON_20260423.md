# G-HH23: Baseline Comparison Matrix
**Date:** 2026-04-23
**Scope:** Work 2 (LLM KV-Cache Mapping)

## 1. Comprehensive Comparison Matrix

| Technology Baseline | Retention Mismatch | Endurance Gap | Density Factor | Inference Power Profile | Bottleneck |
|:---|:---|:---|:---|:---|:---|
| **SRAM (Digital)** | Under-specced (ms) | Over-specced ($\infty$) | 1x (Baseline) | High static leakage | Area capacity |
| **KIVI (2-bit INT)** | Under-specced (ms) | Over-specced ($\infty$) | 4x to 8x | High memory wall | Data movement |
| **Oxide-RRAM CIM** | Over-specced (10 yrs)| Fatal (10^6 max) | 16x to 32x | High write voltage | Write-cycle death |
| **Organic OEC-RAM** | **Matched (10^3 s)** | **Infinite (Optical)**| 16x to 32x | Ultra-low (Optical) | Noise / Quantization |

## 2. Fair-Comparison Criteria & Methodological Pitfalls
1. **The "Unquantized SRAM" Strawman Pitfall:** It is intellectually dishonest to compare organic CIM KV-cache against FP16 SRAM. State-of-the-art edge LLMs already use KV-cache quantization (e.g., KIVI, AWQ). **Fair Criterion:** Organic CIM's $N=4$ state density must be benchmarked strictly against 2-bit INT digital KV-caches.
2. **The "Zero-Cost Write" Simulation Pitfall:** Previous CIM papers often ignore the massive energy cost of writing KV pairs during the prefill stage, which penalizes oxide-RRAM. **Fair Criterion:** Our energy model must account for the write energy of every prefill token. Organic OEC-RAM will win this explicitly because optical writing circumvents high electrical programming voltages.
3. **The "Infinite Session" Evaluation Pitfall:** Evaluating KV-cache degradation over hours-long static contexts is unrealistic for conversational agents. **Fair Criterion:** Perplexity degradation must be evaluated dynamically over the time-domain defined by G-HH21's Session Length Distribution ($T \sim 	ext{LogNormal}$).
