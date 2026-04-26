# Codex W2 Fresh-D2D All/MLP 3-Seed Report

Date: 2026-04-26  
Owner: Codex  
Scope: Work 2 Pythia-410M low-noise fresh-D2D validation for the two viable scopes from the 3-seed long matrix.

## Executive Verdict

The `all` and `mlp` W2 routes both survive post-training fresh-D2D multi-instance evaluation across three seeds. This strengthens the previous fixed final-D2D result: the improvement is not just adaptation to a single terminal noise sample.

The route distinction is now clearer:

- `all`: strongest training/eval adaptation, but higher fresh-D2D instance variance.
- `mlp`: smaller adaptation effect, but lower fresh-D2D variance and tighter cross-seed consistency.

These are still fixed smoke-text results, not held-out perplexity. They are suitable for route selection and infrastructure validation only.

## Protocol

- Model: `EleutherAI/pythia-410m-deduped`
- Train scope: last GPT-NeoX block
- Steps: `1000`
- Seeds: `1234`, `456`, `789`
- Eval repeats: `5`
- Fresh-D2D eval: `10` fresh D2D instances per seed, `5` C2C repeats per instance
- Analog precision: `--high-precision-analog`
- Noise: `sigma_d2d=0.005`, `sigma_c2c=0.002`
- D2D resampling during train: every `10` steps
- LR: `5e-6`
- Limitation: fixed four-text smoke batch, no held-out perplexity yet

## Aggregate Results

| Scope | Eval Delta Mean | Eval Delta Seed Std | Fresh-D2D Seed Mean Loss | Fresh-D2D Seed Std | 30-Instance Fresh-D2D Std |
|---|---:|---:|---:|---:|---:|
| `all` | `-0.6132` | `0.3206` | `6.5309` | `0.0550` | `0.2011` |
| `mlp` | `-0.4589` | `0.1810` | `5.8459` | `0.0215` | `0.1077` |

JSON summary: `report_md/_gpt/json_gpt/w2_fresh_d2d_all_mlp_3seed_summary_20260426.json`.

## Per-Seed Results

| Scope | Seed | Eval Delta | Fresh-D2D Mean Loss | Fresh-D2D Std |
|---|---:|---:|---:|---:|
| `all` | 1234 | `-0.3623` | `6.4978` | `0.2140` |
| `all` | 456 | `-0.5030` | `6.5944` | `0.1835` |
| `all` | 789 | `-0.9744` | `6.5007` | `0.1783` |
| `mlp` | 1234 | `-0.2951` | `5.8677` | `0.0992` |
| `mlp` | 456 | `-0.6531` | `5.8455` | `0.1336` |
| `mlp` | 789 | `-0.4284` | `5.8247` | `0.0709` |

## Route Decision

1. Keep `all` as the strongest toy-regime path because it has the largest average eval improvement and uses the most complete analogized compute path.
2. Keep `mlp` as the safest scoped fallback because fresh-D2D variance is about half of `all` and cross-seed fresh means are tighter.
3. Do not headline `qkv` compute; the earlier 3-seed long matrix had a failed seed.
4. Do not overclaim `attention_output`; it was stable but weak.

## Implementation Note

Codex added two CLI options to `paper2/src/train_llm_hybrid.py`:

- `--fresh-d2d-instances`
- `--fresh-d2d-repeats`

This keeps fresh-D2D evaluation inside the same trusted protocol and logs a `fresh_d2d_eval` event with per-instance means.

## Next Required Step

The next bottleneck is not more fixed-batch GPU time. It is held-out evaluation:

1. Implement a real `paper2/src/eval_llm_kv_cache.py` held-out perplexity path.
2. Add an explicit train/eval text split or local held-out shard for `train_llm_hybrid.py`.
3. Only then rerun `all` and `mlp` as paper-candidate W2 results.

Until then, these results should be described as controlled adaptation smokes.
