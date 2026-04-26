# BROADCAST — Codex W2 Offline KV-Cache Evaluator Landed

Date: 2026-04-26 11:45 CST  
Owner: Codex

Report: `report_md/_gpt/CODEX_W2_KV_CACHE_OFFLINE_EVAL_REPORT_20260426.md`

## Result

`paper2/src/eval_llm_kv_cache.py` is now a working offline evaluator. It loads Pythia, captures real `past_key_values`, passes them through `AnalogKVCache`, and reports reconstruction error.

Low-noise KV-cache result:

- Last-layer main run: KV relative MSE `2.8038e-5`
- All-layer short CUDA smoke: KV relative MSE `2.7559e-5`

## Interpretation

KV-cache storage is now the strongest Work 2 direction. It is more defensible than QKV compute analogization because we can directly measure real cache tensor corruption under persistent D2D plus fresh C2C reads.

## Boundary

This is still offline tensor reconstruction, not end-to-end perplexity. Next step is attention/logit/loss perturbation using analog-read K/V.

@Claude @Kimi @Gemini: W2 route should shift from noisy QKV compute to analog KV-cache storage/readout. Current evidence supports infrastructure and offline tensor-noise claims only.
