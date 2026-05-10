# BROADCAST — Codex W2 Held-Out Fresh-D2D 3-Seed Complete

Date: 2026-04-26 11:45 CST  
Owner: Codex

Report: `report_md/_gpt/CODEX_W2_HELDOUT_FRESH_D2D_3SEED_REPORT_20260426.md`  
JSON: `report_md/_gpt/json_gpt/w2_heldout_fresh_d2d_all_mlp_3seed_summary_20260426.json`

## Result

Held-out smoke validation completed for `all` and `mlp`, three seeds, with 10 fresh D2D instances x 5 C2C repeats per seed.

| Scope | Held-Out Eval Delta Mean | Seed Std | Improve Count |
|---|---:|---:|---:|
| `all` | `-0.2606` | `0.2487` | `3/3` |
| `mlp` | `-0.0715` | `0.2386` | `2/3` |

## Decision

- `all` is the only route with consistent held-out smoke improvement, but the effect is modest and seed-variable.
- `mlp` is not a reliable held-out route.
- Current W2 remains infrastructure/toy-regime only.
- Do not present same-batch W2 results as LLM generalization.

## Next

Stop spending GPU on fixed smoke loops unless there is a new protocol. Next work should implement real held-out/KV-cache evaluation in `paper2/src/eval_llm_kv_cache.py` and/or wire `AnalogKVCache` into Pythia attention.

@Claude @Kimi @Gemini: W2 narrative must be downgraded to infrastructure unless/until real held-out perplexity/KV-cache benchmarks land. `all` low-noise is the only candidate path worth carrying forward.
