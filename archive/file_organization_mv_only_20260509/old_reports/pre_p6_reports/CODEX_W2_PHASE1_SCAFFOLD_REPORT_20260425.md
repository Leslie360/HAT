# Codex W2 Phase 1 Scaffold Report
**Date:** 2026-04-25  
**Owner:** Codex  
**Task:** Round-8 W1 analog KV-cache infrastructure scaffold  
**Status:** PARTIAL W1 COMPLETE; runtime blocked only by missing local PyTorch package

## Files Written
- `paper2/__init__.py`
- `paper2/src/__init__.py`
- `paper2/src/analog_kv_cache.py`
- `paper2/src/llm_hybrid.py`
- `paper2/src/eval_llm_kv_cache.py`
- `paper2/src/train_llm_hybrid.py`
- `tests/test_w2_analog_kv_cache.py`
- `tests/test_w2_llm_hybrid_conversion.py`
- `tests/test_w2_perplexity_baseline.py`

## Implemented
### `AnalogKVCache`
Standalone per-layer analog KV-cache primitive:
- shape convention `(batch, heads, seq, head_dim)`;
- `write(token_idx, k_token, v_token)` stores one token;
- `read(start_pos, end_pos)` returns cached K/V;
- persistent D2D masks are sampled once per cache lifetime;
- C2C noise is freshly sampled per read;
- optional symmetric bit-width quantization for cached activations;
- `reset()` and `resample_d2d()` support fresh-instance eval discipline.

### Pythia/GPT-NeoX hybrid helpers
`paper2/src/llm_hybrid.py` includes:
- `classify_pythia_linear(name)`;
- `discover_pythia_linear_modules(model)`;
- `convert_pythia_to_hybrid(model, config, ...)` with independent `copy.copy(config)` per replacement.

The helper deliberately treats Pythia as GPT-NeoX:
- `query_key_value` -> QKV analog;
- `attention.dense` -> attention output analog;
- `dense_h_to_4h` / `dense_4h_to_h` -> MLP analog;
- LM head skipped.

### CLI scaffolds
`train_llm_hybrid.py` and `eval_llm_kv_cache.py` are placeholders that fail loudly until forward smoke tests are implemented. This prevents accidental fake benchmark runs.

## Verification
Commands run:
```bash
python -m py_compile paper2/src/analog_kv_cache.py paper2/src/llm_hybrid.py paper2/src/eval_llm_kv_cache.py paper2/src/train_llm_hybrid.py tests/test_w2_analog_kv_cache.py tests/test_w2_llm_hybrid_conversion.py tests/test_w2_perplexity_baseline.py
pytest -q tests/test_w2_analog_kv_cache.py tests/test_w2_llm_hybrid_conversion.py tests/test_w2_perplexity_baseline.py
```

Result:
- Syntax compile: PASS.
- Pytest in Codex shell: `3 passed, 4 skipped`.
- Skipped tests require PyTorch. Current active Codex shell has `transformers 5.6.0` but no `torch` package. A separate conda env at `/home/qiaosir/miniconda3/envs/LLM/bin/python` has `torch 2.10.0+cu128`, `transformers 5.6.1`, and CUDA available; standalone runtime smoke passed there.

## Additional Runtime Smoke
Using `/home/qiaosir/miniconda3/envs/LLM/bin/python`:
- `torch 2.10.0+cu128`, CUDA available.
- `analog_kv_cache_d2d_persistent`: PASS.
- `analog_kv_cache_c2c_fresh`: PASS.
- `pythia_module_discovery_synthetic`: PASS.
- `hybrid_conversion_synthetic`: PASS.

No full Pythia weights were loaded; only lightweight Hugging Face config metadata was accessed.
- Pythia config check: PASS via `AutoConfig.from_pretrained("EleutherAI/pythia-410m-deduped")`; model_type `gpt_neox`, hidden size 1024, 24 layers, 16 heads, intermediate size 4096, max positions 2048.

## Blocking Item
Install/select a Python environment with PyTorch before W1 runtime validation:
```bash
python - <<'PY'
import torch
print(torch.__version__, torch.cuda.is_available())
PY
```

Until that works, do not claim Pythia forward/perplexity numbers.

## Next W1 Steps
1. Use an environment with PyTorch.
2. Run `pytest -q tests/test_w2_analog_kv_cache.py tests/test_w2_llm_hybrid_conversion.py tests/test_w2_perplexity_baseline.py` and require the runtime tests to pass, not skip.
3. Add a Pythia module discovery smoke command that loads `EleutherAI/pythia-410m-deduped` only when explicitly requested.
4. Implement no-noise hybrid forward drift check.
5. Only then start the 100-step training smoke.
