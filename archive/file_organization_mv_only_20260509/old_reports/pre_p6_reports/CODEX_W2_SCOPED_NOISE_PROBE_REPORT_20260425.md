# Codex W2 Scoped Noise Probe Report

Date: 2026-04-25 22:24 CST
Owner: Codex
Scope: Work 2 Pythia 410M smoke probes after W1 runtime validation.

## Executive Verdict

1. The scoped conversion path is now implemented and verified via `--analog-scope` in `paper2/src/train_llm_hybrid.py`.
2. No-noise scoped controls are healthy for QKV, attention output, and MLP. This rules out scoped conversion itself as the cause of noisy degradation.
3. At d2d=0.05/c2c=0.02, attention output is the safest analog entry point; QKV and MLP are immediately high-loss.
4. Noise-source split suggests QKV is especially sensitive to C2C/read noise, while MLP is especially sensitive to persistent D2D/resampling. Attention output is comparatively tolerant.
5. Even much lower noise d2d=0.01/c2c=0.005 remains nontrivial for QKV and MLP. Work 2 should not start from full noisy all-module HAT; it should stage from attention-output-only, then lower-noise QKV/MLP calibration, then KV-cache-specific persistent-D2D/fresh-C2C isolation.

## Code Change

`paper2/src/train_llm_hybrid.py` now exposes:

```bash
--analog-scope {all,qkv,attention_output,mlp,qkv_attention}
```

The script now reports converted module counts in the final JSON:

- `qkv_modules`
- `attention_output_modules`
- `mlp_modules`
- `discovered_*_modules`

A unit test was added for scoped MLP-only conversion in `tests/test_w2_llm_hybrid_conversion.py`.

Verification:

```text
pytest -q tests/test_w2_llm_hybrid_conversion.py tests/test_w2_analog_kv_cache.py tests/test_w2_perplexity_baseline.py
3 passed, 5 skipped

/home/qiaosir/miniconda3/envs/LLM/bin/python -m py_compile paper2/src/train_llm_hybrid.py paper2/src/llm_hybrid.py
PASS

manual scoped conversion PASS ['gpt_neox.layers.0.mlp.dense_4h_to_h', 'gpt_neox.layers.0.mlp.dense_h_to_4h']
```

Note: the LLM conda env lacks `pytest`, so a direct manual scoped-conversion assertion was run there.

## Data Files

Summary JSON:

- `paper2/results/w2_scoped_probe_summary_20260425.json`

Raw logs:

- `logs/_gpt/w2_llm_scope_*_20260425_221406.log`
- `logs/_gpt/w2_llm_scope_*_20260425_221532.log`
- `logs/_gpt/w2_llm_scope_*_20260425_221702.log`
- `logs/_gpt/w2_llm_scope_*_20260425_221843.log`

## Results: No-Noise Controls

| Scope | Initial | Final | Delta | Min | Modules | Verdict |
|---|---:|---:|---:|---:|---|---|
| QKV | 6.4883 | 6.2832 | -0.2051 | 6.2832 | 24 QKV | healthy |
| Attention output | 6.4880 | 6.4744 | -0.0135 | 6.4744 | 24 O | healthy but small trainable surface |
| MLP | 6.4879 | 6.2078 | -0.2801 | 6.2078 | 48 MLP | healthy |

Interpretation: scoped replacement and trainable-parameter selection are not the primary cause of noisy failures.

## Results: Combined Low/Moderate Noise

| Scope | Noise | Initial | Final | Delta | Min | Verdict |
|---|---|---:|---:|---:|---:|---|
| Attention output | d2d=0.05/c2c=0.02 | 6.7396 | 6.9337 | +0.1942 | 6.6347 | damaged but near baseline scale |
| QKV | d2d=0.05/c2c=0.02 | 11.9346 | 11.8197 | -0.1148 | 10.8376 | severe initial degradation |
| MLP | d2d=0.05/c2c=0.02 | 13.6724 | 13.4889 | -0.1835 | 11.9756 | severe initial degradation |
| Attention output | d2d=0.02/c2c=0.01 | 6.5048 | 6.5088 | +0.0040 | 6.4416 | strongest safe entry point |
| QKV | d2d=0.01/c2c=0.005 | 8.2420 | 7.8749 | -0.3671 | 7.5094 | still damaged |
| QKV | d2d=0.02/c2c=0.01 | 9.2771 | 9.4475 | +0.1703 | 8.9894 | damaged |
| MLP | d2d=0.01/c2c=0.005 | 7.1723 | 7.4280 | +0.2557 | 6.9109 | mild/moderate damage |
| MLP | d2d=0.02/c2c=0.01 | 9.5493 | 9.5127 | -0.0365 | 8.7875 | damaged |
| QKV+O | d2d=0.01/c2c=0.005 | 7.5252 | 7.8872 | +0.3621 | 7.3024 | combined attention path still fragile |

## Results: D2D vs C2C Split

| Scope | Noise Source | Initial | Final | Delta | Min | Readout |
|---|---|---:|---:|---:|---:|---|
| Attention output | C2C only 0.02 | 6.5641 | 6.5547 | -0.0094 | 6.4146 | tolerated |
| Attention output | D2D only 0.05 | 6.8798 | 6.8166 | -0.0632 | 6.7636 | tolerated, but offset |
| QKV | C2C only 0.02 | 8.9517 | 9.6626 | +0.7110 | 8.6929 | C2C-sensitive |
| QKV | D2D only 0.05 | 11.3961 | 11.2395 | -0.1566 | 11.2395 | also D2D-sensitive |
| MLP | C2C only 0.02 | 9.1994 | 8.2407 | -0.9587 | 8.2166 | adapts somewhat |
| MLP | D2D only 0.05 | 12.7308 | 13.1239 | +0.3932 | 11.9866 | D2D/resample-sensitive |

## Current Route Decision

Paper-safe W2 route after these probes:

1. Keep `attention_output` as first analogized LLM submodule because it is the only low-noise path close to baseline scale.
2. Treat QKV and MLP as high-risk. They require separate calibration before HAT-like training claims.
3. Do not run or claim noisy full all-module Pythia as the canonical baseline yet.
4. Next GPU jobs launched after this report:
   - digital last-block baseline;
   - all-module d2d=0.01/c2c=0.005;
   - attention-output d2d=0.02/c2c=0.01 for 1000 steps;
   - QKV d2d=0.005/c2c=0.002;
   - MLP d2d=0.005/c2c=0.002;
   - QKV+O d2d=0.005/c2c=0.002.

## Boundary

All results here are smoke-probe results on a tiny fixed text batch. They identify implementation risk and experiment direction. They are not WikiText perplexity, not long-context decode, and not paper-level claims.
