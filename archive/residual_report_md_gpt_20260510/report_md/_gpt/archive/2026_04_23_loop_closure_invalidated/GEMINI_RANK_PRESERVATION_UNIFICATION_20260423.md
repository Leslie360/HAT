# G-SLIM-3: Rank Preservation Unification Theory
**Date:** 2026-04-23
**Scope:** Round Q SLIM (Empirically Updated post-CX-K2)

## 1. The Unified Framework
The thesis spans two distinct works: Work 1 (falsifying/mitigating analog ViTs under severe NL) and Work 2 (mapping LLM KV-cache to organic OEC-RAM).
The unification of these two works lies in a single mathematical principle: **Top-k Rank Preservation through the Softmax Operator under Analog Noise**.

## 2. Work 1: Attention Softmax Rank Collapse (The Negative Case)
In Work 1, severe non-linearity (NL=2.0) creates a flat, high-variance loss landscape (the Structural Limit, mean 38.95% ± 9.85%). When a fresh D2D noise mask is applied at inference, the pre-softmax logits in the self-attention layer are perturbed. Because the optimization basin is flat, the weights lack the robustness to maintain a wide logit margin. The D2D noise variance easily exceeds the logit gap between the primary and secondary tokens, causing a rank flip. The Softmax operator exponentially amplifies this rank flip, shattering the attention map and plunging the instance's accuracy to near-chance levels.

## 3. Work 2: KV-Cache Top-k Survival (The Positive Case)
In Work 2, we map the KV-cache of an LLM to organic CIM arrays. LLM generative decoding is remarkably resilient as long as the relative ranking of the top-$k$ attended tokens in the KV-cache is preserved.
Because we do not require severe non-linear training updates (the KV cache is written once via reliable optical refresh), we avoid the high-variance structural limit of Work 1. We only contend with static quantization and drift noise. We can mathematically bound this noise to ensure it stays below the rank-flip threshold, defining the theoretical quantization floor (e.g., 4-bit or 2-bit equivalent) that guarantees near-lossless perplexity and top-k survival.

## 4. Conclusion
Both works evaluate the limits of analog arrays through the lens of Softmax rank preservation. Work 1 shows what happens when the rank preservation fails structurally due to NL-induced landscape shattering; Work 2 shows how to engineer a system where rank preservation succeeds predictably (stable LLM decoding) by sidestepping the electrical write non-ideality.
