# P3: End-to-End Attention Integration Design

**Date:** 2026-04-29
**Author:** Remote 107
**Target Model:** EleutherAI/pythia-410m-deduped (GPTNeoX architecture)

## 1. Where Pythia/GPT-NeoX creates and reads `past_key_values`
In `transformers==5.7.0`, Pythia relies on `GPTNeoXAttention` defined in `transformers/models/gpt_neox/modeling_gpt_neox.py`. 
During the `forward` pass, the cache is passed as `layer_past: Cache | None = None`. The attention module reads and updates the cache using the standard Cache API:
```python
if layer_past is not None:
    key_states, value_states = layer_past.update(key_states, value_states, self.layer_idx)
```
The actual storage is managed by the `Cache` object (typically a `DynamicCache`), which maintains `.key_cache` or `.layers` internally.

## 2. Feasibility of a Clean Monkey-Patch / Subclass
**Yes, a completely clean patch is possible without modifying model weights or attention source code.**
Instead of modifying `GPTNeoXAttention`, we can subclass `transformers.cache_utils.DynamicCache` to create an `AnalogDynamicCache`. By overriding its `update()` method, we can intercept the standard KV write process:
1. Receive incoming `key_states` and `value_states`.
2. Pass them through our `AnalogKVCache._float_to_conductance` quantization and noise injection.
3. Apply retention decay based on token ages.
4. Return the analog-recovered `key_states` and `value_states` back to the attention module.
We then simply pass this `AnalogDynamicCache` object to the `past_key_values` argument in the generation or PPL evaluation loop.

## 3. How to Compare the Four Modes
We can cleanly separate projection quantization from KV cache quantization:
- **FP baseline (Digital Projections, Digital KV):** Standard `model.forward` with the default Hugging Face `DynamicCache`.
- **Analog Cache Only (Digital Projections, Analog KV):** Standard Pythia weights, but we pass our `AnalogDynamicCache` object into the `past_key_values` argument during inference.
- **Analog Projections Only (Analog Projections, Digital KV):** Run our `convert_to_hybrid()` utility to replace `nn.Linear` (e.g., `query_key_value` and `dense`) with `AnalogLinear`. Use the default `DynamicCache` for KV.
- **Analog Projections + Analog KV:** Use the `convert_to_hybrid()` model weights AND pass the `AnalogDynamicCache` to `past_key_values`.

## 4. Exact Perplexity/Loss Metric and Text Split
- **Dataset/Split:** `wikitext-2-raw-v1`, `test` split. Concatenated with `

`.
- **Metric:** Sliding-window Perplexity (PPL).
- **Formula:** 
  - `max_length=1024`, `stride=512`.
  - For each window, target labels for the overlapping context (the first 512 tokens) are masked with `-100` (ignore index).
  - Loss is computed only on the newly shifted tokens using `CrossEntropyLoss(reduction='sum')`.
  - Final PPL = `exp(total_summed_nll / total_predicted_tokens)`.

## 5. Expected Risk Points
1. **Rotary Positional Embeddings (RoPE):** GPTNeoX applies RoPE to `key_states` *before* they are cached. Injecting analog D2D/C2C noise into pre-rotated key matrices might result in non-linear phase corruption that behaves differently than noise injected into standard absolute-position keys.
2. **Cache API Contract:** The `AnalogDynamicCache` must correctly maintain the `get_seq_length()` and `get_max_cache_shape()` protocol expected by `transformers==5.7.0`. Breaking this contract will cause indexing errors in downstream attention calculations.
3. **Simulation Overhead:** Running token-by-token 16-state STE quantization (and tracking per-token retention ages) inside python loops will introduce significant overhead, making long context evaluations extremely slow if not heavily vectorized across the batch dimension.
