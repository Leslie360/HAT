# Codex W2 Offline Analog KV-Cache Evaluation Report

Date: 2026-04-26  
Owner: Codex  
Scope: Work 2 offline Pythia KV-cache tensor read-noise evaluation.

## Executive Verdict

`paper2/src/eval_llm_kv_cache.py` is no longer a scaffold. It now loads Pythia, captures real `past_key_values`, stores them in `AnalogKVCache`, and measures reconstruction error after quantization plus persistent D2D and fresh C2C reads.

At the low-noise setting used in W2 (`sigma_d2d=0.005`, `sigma_c2c=0.002`, 16-bit analog cache), the offline KV-cache tensor error is small: relative KV MSE is about `2.8e-5`. This supports KV-cache storage as a plausible Work 2 route, but it is still not end-to-end perplexity.

## Code Changes

Updated `paper2/src/eval_llm_kv_cache.py`:

- Loads `EleutherAI/pythia-410m-deduped` locally.
- Captures real Hugging Face `past_key_values` with `use_cache=True`.
- Supports current `transformers.cache_utils.DynamicCache` via `.layers[*].keys/.values`.
- Evaluates selected layers: `--layers last`, `--layers all`, or comma-separated indices.
- Writes JSON metrics via `--output-json`.

## Results

| Run | Layers | Seq Len | D2D Instances | Reads/Instance | KV Relative MSE |
|---|---:|---:|---:|---:|---:|
| CPU smoke | last | 16 | 2 | 2 | `2.7903e-5` |
| CUDA smoke | all 24 | 16 | 2 | 2 | `2.7559e-5` |
| CUDA main | last | 19 effective | 10 | 5 | `2.8038e-5` |

Main JSON: `report_md/_gpt/json_gpt/w2_kv_cache_offline_last_n005002_bw16_i10r5_20260426_114032.json`  
All-layer smoke JSON: `report_md/_gpt/json_gpt/w2_kv_cache_offline_alllayers_cuda_smoke_20260426.json`  
CPU smoke JSON: `report_md/_gpt/json_gpt/w2_kv_cache_offline_cpu_smoke_20260426.json`

## Notes

- The `--max-length 64` input produced an effective sequence length of 19 because the fixed held-out texts are shorter than 64 tokens.
- A full all-layer max-length-64 run exited without traceback before JSON was written. Short all-layer CUDA and last-layer max-length-64 both pass, so this is not blocking the evaluator but should be treated as a runtime-scale fragility in WSL/CUDA.
- This evaluator measures tensor reconstruction only. It does not yet inject analog KV reads back into attention or report perplexity.

## Interpretation

The offline KV route is more promising than QKV compute analogization:

1. KV storage noise is directly measurable on real Pythia cache tensors.
2. Relative error at the low-noise point is stable and small.
3. The next scientific step is end-to-end cache-read injection or a controlled attention-output perturbation benchmark, not more same-batch training loops.

## Next Step

Implement one of the following before any W2 paper claim:

1. End-to-end Pythia attention patch that reads K/V through `AnalogKVCache` during eval.
2. Offline attention-output perturbation benchmark that recomputes attention using analog-read K/V and compares logits/loss to digital K/V.

Until then, W2 remains infrastructure plus offline tensor-noise evidence.
