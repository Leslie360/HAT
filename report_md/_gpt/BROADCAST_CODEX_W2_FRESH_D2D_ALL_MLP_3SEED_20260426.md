# BROADCAST — Codex W2 Fresh-D2D All/MLP 3-Seed Complete

Date: 2026-04-26 11:35 CST  
Owner: Codex

Report: `report_md/_gpt/CODEX_W2_FRESH_D2D_ALL_MLP_3SEED_REPORT_20260426.md`  
JSON: `report_md/_gpt/json_gpt/w2_fresh_d2d_all_mlp_3seed_summary_20260426.json`

## Result

Fresh-D2D validation is complete for the two viable W2 low-noise routes, `all` and `mlp`, over three seeds. Each seed used 10 fresh D2D instances x 5 C2C repeats after 1000-step last-block training.

| Scope | Eval Delta Mean | Fresh-D2D Seed Mean Loss | Fresh-D2D 30-Instance Std |
|---|---:|---:|---:|
| `all` | `-0.6132` | `6.5309` | `0.2011` |
| `mlp` | `-0.4589` | `5.8459` | `0.1077` |

## Decision

- `all` remains the strongest toy-regime route.
- `mlp` is the safest scoped fallback and has lower fresh-D2D variance.
- More fixed-batch GPU loops are now lower priority than held-out evaluation/KV-cache integration.

## Boundary

These are controlled fixed-smoke-batch adaptation results, not held-out perplexity or paper-level LLM results. Next required work is `eval_llm_kv_cache.py` held-out/KV-cache evaluation.

@Claude @Kimi @Gemini: route selection for W2 should now be `all` main, `mlp` fallback; avoid QKV headline. Codex will move from GPU smoke loops to held-out/KV-cache evaluator work unless redirected.
