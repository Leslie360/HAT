# Codex W2 Held-Out Fresh-D2D 3-Seed Report

Date: 2026-04-26  
Owner: Codex  
Scope: Work 2 Pythia-410M held-out smoke validation for `all` and `mlp` low-noise routes.

## Executive Verdict

Held-out smoke validation sharply reduces the strength of the W2 claim.

- `all` improves on the held-out text set in all 3/3 seeds, but the mean effect is modest and seed-variable: `-0.2606 +/- 0.2487` eval loss delta.
- `mlp` is not reliable on held-out text: only 2/3 seeds improve, with mean `-0.0715 +/- 0.2386`; seed1234 worsens.

Therefore current Work 2 should remain an infrastructure/toy-regime result. The honest next route is: keep `all` as the only weak held-out smoke candidate, but do not present it as a paper-level LLM result until a real benchmark corpus/perplexity evaluator and KV-cache integration exist.

## Protocol

- Model: `EleutherAI/pythia-410m-deduped`
- Train scope: last GPT-NeoX block
- Eval text set: `heldout` via new `--eval-text-set heldout`
- Steps: `1000`
- Seeds: `1234`, `456`, `789`
- Eval repeats: `5`
- Fresh-D2D eval: `10` fresh D2D instances per seed, `5` C2C repeats per instance
- Analog precision: `--high-precision-analog`
- Noise: `sigma_d2d=0.005`, `sigma_c2c=0.002`
- D2D resampling during train: every `10` steps
- LR: `5e-6`

## Aggregate Results

| Scope | Held-Out Eval Delta Mean | Seed Std | Improve Count | Fresh-D2D Mean Loss | Fresh-D2D 30-Instance Std |
|---|---:|---:|---:|---:|---:|
| `all` | `-0.2606` | `0.2487` | `3/3` | `7.1851` | `0.1340` |
| `mlp` | `-0.0715` | `0.2386` | `2/3` | `6.4484` | `0.0964` |

JSON summary: `report_md/_gpt/json_gpt/w2_heldout_fresh_d2d_all_mlp_3seed_summary_20260426.json`.

## Per-Seed Results

| Scope | Seed | Eval Before | Eval After | Eval Delta | Fresh-D2D Mean | Fresh-D2D Std |
|---|---:|---:|---:|---:|---:|---:|
| `all` | 1234 | `7.3127` | `7.2691` | `-0.0436` | `7.1505` | `0.1707` |
| `all` | 456 | `7.5192` | `6.9872` | `-0.5320` | `7.2102` | `0.0996` |
| `all` | 789 | `7.3246` | `7.1184` | `-0.2062` | `7.1947` | `0.1052` |
| `mlp` | 1234 | `6.4877` | `6.6775` | `+0.1898` | `6.4696` | `0.0865` |
| `mlp` | 456 | `6.7796` | `6.5020` | `-0.2776` | `6.4097` | `0.0913` |
| `mlp` | 789 | `6.4517` | `6.3249` | `-0.1268` | `6.4658` | `0.0941` |

## Route Decision

1. `all` remains the only W2 route with consistent held-out smoke improvement, but it is weak and seed-variable.
2. `mlp` should be treated as a training-path fallback, not a held-out route.
3. The previous same-batch result is useful for debugging analog training flow, but it must not be used as a generalization claim.
4. QKV compute remains unstable and should not be headlined.

## Code Changes

`paper2/src/train_llm_hybrid.py` now includes:

- `--fresh-d2d-instances`
- `--fresh-d2d-repeats`
- `--eval-text-set {train,heldout}`

The default remains backward-compatible (`--eval-text-set train`).

## Next Work

The next Work 2 step should be code, not more fixed smoke loops:

1. Implement `paper2/src/eval_llm_kv_cache.py` as a real held-out perplexity/context evaluator.
2. Wire `AnalogKVCache` into the Pythia attention cache path or produce an explicit offline KV-cache read-noise benchmark.
3. Only then rerun the low-noise `all` route for a candidate paper-level W2 result.
