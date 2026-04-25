# Work 2 Testbed Decision
**Date:** 2026-04-25  
**Owner:** Codex  
**Round:** Round-8 W0  
**Status:** LOCKED for W1 implementation

## Decision
Use `EleutherAI/pythia-410m-deduped` as the local Work 2 testbed.

Fallback only if the model cannot be loaded or cached locally: `EleutherAI/pythia-160m-deduped`.

## Source Facts
The Hugging Face model card for `EleutherAI/pythia-410m-deduped` lists:
- License: Apache 2.0.
- Model type: transformer-based language model, GPT-NeoX/Pythia family.
- Architecture row for 410M: 24 layers, model dimension 1024, 16 attention heads, 302,311,424 non-embedding parameters.
- Total renamed parameter count for 410M: 405,334,016.
- Intended use: controlled scientific research on large language models, with fine-tuning/adaptation allowed under Apache 2.0.

Primary source: https://huggingface.co/EleutherAI/pythia-410m-deduped

## Why This Testbed
Pythia 410M is the right first Work 2 target because it is large enough to exercise real decoder-only attention/KV-cache behavior while still fitting local GPU constraints.

Decision criteria:
- Fits 16GB local GPU for W1 smoke tests and short W2 finetunes with AMP and small microbatches.
- Uses decoder-only causal attention with KV-cache, so the target mechanism is real rather than synthetic.
- Has 24 layers, 16 heads, hidden size 1024, and head dimension 64, giving enough depth and heads to test per-layer and per-head analog sensitivity.
- Apache 2.0 license is compatible with experimental code release.
- Public Hugging Face weights and tokenizer simplify reproducibility once the environment is ready.
- Smaller than LLaMA-2 7B, so it does not consume the 8x40GB server currently reserved for Paper 1 cross-architecture validation.

## Pythia-Specific Corrections
Some earlier Work 2 notes used LLaMA-style language. For Pythia 410M, the implementation target should use GPT-NeoX naming and structure:
- Normalization is treated as digital regardless of whether the module is LayerNorm/RMSNorm style.
- Positional encoding/rotary operations stay digital.
- Attention QKV may appear as a fused projection such as `query_key_value`; implementation should split or mask logical Q/K/V slices without assuming separate modules exist.
- MLP is not a LLaMA gated MLP. Pythia/GPT-NeoX uses the feed-forward pair commonly exposed as `dense_h_to_4h` and `dense_4h_to_h`.
- LM head remains digital initially because it is tied conceptually to the token embedding/output distribution and is numerically sensitive.

## W1 Acceptance Consequence
W1 infrastructure must first prove three minimal properties on Pythia 410M:
1. FP baseline load: tokenizer and model load locally and run a no-NaN forward pass on a short text batch.
2. Hybrid conversion: QKV/output/MLP linear modules can be wrapped without modifying Paper 1 source files.
3. KV-cache wrapper: persistent D2D and fresh C2C behavior is testable independently of full generation.

## Resource Policy
Do not use the 8x40GB remote for this phase. W1 uses local GPU only. If local GPU becomes needed for Paper 1 trigger work, Work 2 pauses.
