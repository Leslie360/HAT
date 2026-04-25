# BROADCAST — CODEX W2 PHASE 1 SCAFFOLD
**Date:** 2026-04-25  
**From:** Codex  
**To:** Claude, Kimi, Gemini, User  
**Status:** W1 scaffold landed; runtime validation awaits PyTorch environment

## Action
After completing W0, Codex advanced W1 non-GPU infrastructure.

## Files Written
- `paper2/src/analog_kv_cache.py`
- `paper2/src/llm_hybrid.py`
- `paper2/src/eval_llm_kv_cache.py`
- `paper2/src/train_llm_hybrid.py`
- `tests/test_w2_analog_kv_cache.py`
- `tests/test_w2_llm_hybrid_conversion.py`
- `tests/test_w2_perplexity_baseline.py`
- `report_md/_gpt/CODEX_W2_PHASE1_SCAFFOLD_REPORT_20260425.md`

## Current Capability
- Standalone analog KV-cache primitive exists.
- Persistent D2D and fresh C2C semantics are encoded.
- Pythia/GPT-NeoX module classifier/discovery exists.
- Hybrid conversion helper uses independent copied configs per layer.
- Train/eval CLIs are deliberate loud placeholders until forward smoke tests pass.

## Verification
- Syntax compile: PASS.
- W2 tests in Codex shell: `3 passed, 4 skipped`.
- Skip reason in Codex shell: active Python environment lacks PyTorch; this shell has `transformers 5.6.0` but no `torch`. Separate runtime validation under `/home/qiaosir/miniconda3/envs/LLM/bin/python` passed for standalone KV-cache and synthetic Pythia conversion.

## Important Boundary
Pythia config check: PASS via `AutoConfig.from_pretrained("EleutherAI/pythia-410m-deduped")`; model_type `gpt_neox`, hidden size 1024, 24 layers, 16 heads, intermediate size 4096, max positions 2048. No Pythia weights were loaded. No Pythia perplexity, no forward drift, and no training smoke have been run. Do not cite any W2 numerical result yet.

## Next
Run W1 runtime validation in a PyTorch-enabled environment, then implement explicit Pythia load/module-discovery and no-noise forward drift tests.
