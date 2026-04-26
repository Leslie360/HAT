# Codex W2 Low-Noise Long Matrix — 3-Seed Report

Date: 2026-04-26  
Owner: Codex  
Scope: Work 2 Pythia-410M hybrid analog training smoke, local RTX 5070 Ti.

## Executive Verdict

The 1000-step low-noise W2 matrix is complete for three seeds (`1234`, `456`, `789`) and four analog scopes. Under the trusted protocol, `all` and `mlp` are the only stable routes: both reduced eval loss in all 3/3 seeds. `qkv` is unstable (2/3 seeds improve, 1/3 worsens). `attention_output` is stable but very weak.

This remains an infrastructure/toy-regime result, not a paper-level LLM benchmark: train and eval use the same fixed four-text smoke batch. It supports the claim that the Pythia hybrid path can backpropagate and adapt under low analog noise; it does not yet support held-out perplexity claims.

## Protocol

- Model: `EleutherAI/pythia-410m-deduped`
- Device: local `cuda`, dtype `float32`, local files only
- Train scope: last GPT-NeoX block only
- Steps: `1000`
- Eval repeats: `5`
- Seeds: `1234`, `456`, `789`
- Analog precision: `--high-precision-analog`
- Noise: `sigma_d2d=0.005`, `sigma_c2c=0.002`
- D2D resampling during train: every `10` steps
- Optimizer/LR: SGD, `5e-6`
- Batch: fixed four-sentence smoke batch with pad masking

## Aggregate Results

| Scope | Eval Delta Mean | Seed Std | Negative Deltas | Seed Deltas |
|---|---:|---:|---:|---|
| `all` | `-0.6387` | `0.2098` | `3/3` | `-0.4249`, `-0.6468`, `-0.8444` |
| `mlp` | `-0.4886` | `0.1375` | `3/3` | `-0.4866`, `-0.3521`, `-0.6270` |
| `qkv` | `-0.0917` | `0.1826` | `2/3` | `-0.2638`, `-0.1112`, `+0.0998` |
| `attention_output` | `-0.0405` | `0.0206` | `3/3` | `-0.0630`, `-0.0361`, `-0.0225` |

JSON summary: `report_md/_gpt/json_gpt/w2_low_noise_long_3seed_summary_20260426.json`.

## Interpretation

1. `all` is currently the strongest W2 toy-regime route. It adapts despite all QKV/attention-output/MLP modules being analogized and noisy.
2. `mlp` is the safest scoped route. It improves in every seed and has larger effects than `qkv` or `attention_output`.
3. `qkv` should not be a main route yet. One of three seeds worsened after training, confirming earlier concerns that QKV compute is fragile.
4. `attention_output` is not failing at `0.005/0.002`, but the effect size is small. It is a safe debug scope, not the strongest scientific route.
5. The final eval happens after D2D resampling at step 1000, so `eval_after` is already a one-instance fresh-D2D check. It is still only one D2D instance, so it is insufficient for robustness claims.

## Code/Protocol Sanity

- `paper2/src/train_llm_hybrid.py`, `paper2/src/llm_hybrid.py`, `paper2/src/analog_kv_cache.py`, and `paper2/src/eval_llm_kv_cache.py` passed `py_compile`.
- `pytest` is not installed in the `LLM` env, so no dependency install was performed.
- Manual `AnalogKVCache` assertions passed: persistent D2D, fresh C2C, prefix reads, and bit-width quantization bound.
- Manual `llm_hybrid` assertions passed: Pythia module classification, LM head skip, scope selection, and per-module config independence.

## Current Limitation

`paper2/src/eval_llm_kv_cache.py` is still a scaffold. The Work 2 signature claim requires true analog KV-cache integration plus held-out perplexity/context-length evaluation. The current matrix should be described only as last-block hybrid adaptation smoke under controlled analog noise.

## Follow-Up Already Started

Codex patched `train_llm_hybrid.py` with optional post-training fresh-D2D multi-instance evaluation:

- `--fresh-d2d-instances N`
- `--fresh-d2d-repeats K`

A pilot is running for the two viable scopes (`all`, `mlp`) at seed `1234`, with `10` fresh D2D instances and `5` C2C repeats per instance. Logs:

- `logs/_gpt/w2_freshd2d_all_n005002_lb1000_seed1234_20260426_111403.log`
- `logs/_gpt/w2_freshd2d_mlp_n005002_lb1000_seed1234_20260426_111403.log`

## Recommendation

For Work 2 planning, use this route order:

1. Main toy-regime path: `all`, low noise, resampled D2D.
2. Scoped fallback: `mlp`, low noise, resampled D2D.
3. Debug-only: `attention_output`.
4. Avoid as headline until fixed: `qkv` compute analogization.

Next substantive code task: implement real `eval_llm_kv_cache.py` rather than spending more GPU on fixed-batch smoke loops.
