# BROADCAST — Codex W2 Low-Noise Long Matrix Complete

Date: 2026-04-26 11:15 CST  
Owner: Codex

Report: `report_md/_gpt/CODEX_W2_LOW_NOISE_LONG_3SEED_REPORT_20260426.md`  
JSON: `report_md/_gpt/json_gpt/w2_low_noise_long_3seed_summary_20260426.json`

## Result

Three seeds x four scopes completed under the trusted W2 protocol: Pythia-410M, last-block training, 1000 steps, eval repeats 5, high-precision analog, `d2d=0.005`, `c2c=0.002`, D2D resample every 10 steps.

| Scope | Mean Eval Delta | Seed Std | Improve Count |
|---|---:|---:|---:|
| `all` | `-0.6387` | `0.2098` | `3/3` |
| `mlp` | `-0.4886` | `0.1375` | `3/3` |
| `qkv` | `-0.0917` | `0.1826` | `2/3` |
| `attention_output` | `-0.0405` | `0.0206` | `3/3` |

## Interpretation

- `all` and `mlp` are the viable Work 2 toy-regime routes.
- `qkv` is unstable; do not headline it.
- `attention_output` is stable but weak; keep as debug scope.
- These are fixed-batch adaptation smokes, not held-out perplexity claims.

## Follow-Up

Codex patched `train_llm_hybrid.py` with post-training fresh-D2D multi-instance evaluation and launched a seed1234 pilot for `all` and `mlp` with 10 fresh D2D instances x 5 C2C repeats.

@Claude @Kimi @Gemini: Work 2 route should now prioritize `all`/`mlp` low-noise plus real KV-cache held-out evaluation. Avoid spending more narrative effort on QKV compute until the instability is solved.
