# Work 2 Architectural Mapping Spec
**Date:** 2026-04-25  
**Owner:** Codex  
**Round:** Round-8 W0  
**Status:** SOURCE OF TRUTH for W1 implementation and Kimi Methodology draft

## Scope
This spec maps Pythia 410M decoder-only inference/training components onto digital or analog compute/storage for Work 2.

The signature novelty is not merely analog attention projections. It is persistent analog KV-cache storage with device mismatch and read noise.

## Mapping Table
| Component | Work 2 Mapping | Implementation Target | Justification |
|---|---|---|---|
| Token embedding | Digital | `embed_in` / input embedding | Lookup dominated, not MAC-heavy; tying/output semantics make analogization noisy for little gain. |
| Positional/rotary operation | Digital | GPT-NeoX rotary path | Trigonometric/indexing operation, numerically sensitive, not a crossbar MAC. |
| Normalization | Digital | GPT-NeoX LayerNorm/RMSNorm-family modules | Same numerical-sensitivity rationale as Paper 1 norms. |
| QKV projection | Analog | Fused `query_key_value` or logical W_q/W_k/W_v slices | MAC-heavy attention path; direct analog to Paper 1 linear-layer mapping. |
| Attention output projection | Analog | Attention `dense` / output projection | MAC-heavy projection after attention aggregation. |
| Attention score matmul and softmax | Digital | `QK^T`, mask, scale, softmax | Softmax/logit scaling is numerically sensitive and not the Work 2 hardware claim. |
| MLP expansion | Analog | `dense_h_to_4h` | MAC-heavy feed-forward path; Pythia equivalent of Paper 1 MLP analog mapping. |
| MLP contraction | Analog | `dense_4h_to_h` | MAC-heavy feed-forward path. |
| Activation function | Digital | GELU | Nonlinear activation not implemented as crossbar MAC. |
| KV-cache storage | Analog | New `AnalogKVCache` | Work 2 signature: stored K/V states are conductance-coded and reread under persistent D2D plus fresh C2C. |
| LM head | Digital initially | `embed_out` / tied head | Output logits are sensitive and tied to embedding; defer analog LM head to a later ablation. |

## KV-Cache Option Lock
Use Option A: persistent analog KV-cache.

Rejected baseline-only Option B, digital KV-cache plus analog projections, is allowed as a W2 ablation but not as the main Work 2 claim.

## Analog KV-Cache Semantics
For each transformer layer `l`, cache position `t`, head `h`, and channel `d`, store K/V entries in an analog conductance-like representation.

Canonical W1/W2 semantics:
- Write once: when token `t` is processed, its K and V vectors are written into cache slots.
- Persistent D2D: each cache cell has a mismatch term sampled once per cache lifetime or fresh-instance seed and reused across reads.
- Fresh C2C: each read samples new cycle-to-cycle noise.
- Read-many stress: older tokens are read more times during autoregressive decode, exposing context-length-dependent degradation.
- Eval instances: fresh-instance eval resamples D2D masks; MC eval resamples C2C while holding D2D fixed.

Mathematically, for stored value `x`, read value uses a first W1 implementation target:

```text
x_read = Q_b(x) * (1 + eps_d2d) + eps_c2c * scale(x)
eps_d2d ~ N(0, sigma_d2d), persistent per cache cell
eps_c2c ~ N(0, sigma_c2c), fresh per read
```

`Q_b` is disabled in initial no-noise smoke mode and enabled for canonical analog-cache experiments. Default canonical precision is 4-bit for comparability with Paper 1, but W1 should expose bit-width as a config field because KV-cache is activation storage, not weight storage.

## Noise/Quantization Defaults
Use the Paper 1 canonical values unless explicitly running an ablation:
- Weight quantization: 4-bit symmetric.
- KV-cache quantization: 4-bit symmetric by default; no-quant smoke allowed.
- D2D noise: `sigma_d2d = 0.10`.
- C2C noise: `sigma_c2c = 0.05`.
- NL: `NL = 1.0` canonical for Work 2 first pass.
- Fresh eval: 10 D2D instances x 5 C2C MC samples after W1 smoke tests pass.

## W1 Code Boundaries
Work 2 must not modify Paper 1 source files such as `analog_layers.py` or `analog_layers_ensemble.py` during W1. It may import stable primitives from them.

New code locations:
- `paper2/src/analog_kv_cache.py`: cache storage/read noise primitive.
- `paper2/src/llm_hybrid.py`: Pythia/GPT-NeoX hybrid conversion.
- `paper2/src/train_llm_hybrid.py`: short finetune/smoke training entry point.
- `paper2/src/eval_llm_kv_cache.py`: perplexity and sliding-window decode eval.

New tests:
- `tests/test_w2_analog_kv_cache.py`
- `tests/test_w2_llm_hybrid_conversion.py`
- `tests/test_w2_perplexity_baseline.py`

## W1 Minimal Smoke Order
1. Implement and unit-test `AnalogKVCache` without loading Pythia.
2. Load Pythia 410M and discover actual module names programmatically.
3. Convert QKV/output/MLP linears to analog wrappers while leaving embedding/norm/softmax/rotary/LM head digital.
4. Run no-noise hybrid forward pass and compare loss/perplexity drift against FP baseline on a tiny text batch.
5. Enable cache noise in eval-only mode before attempting training.
6. Run 100-step training smoke only after forward/eval tests are green.

## Risk Register
| Risk | Mitigation |
|---|---|
| Fused QKV wrapper breaks tensor slicing | First wrap fused linear as one analog linear; add slice-specific ablations later. |
| KV-cache tensors are generated inside Hugging Face attention internals | Start with a standalone cache wrapper and then integrate by subclassing/monkey-patching the attention forward path. |
| Full WikiText-103 baseline is too slow locally | Use a fixed small validation shard for W1; full suite waits for W2. |
| Work 2 collides with Paper 1 trigger work | Pause Work 2 immediately; Paper 1 has priority. |
