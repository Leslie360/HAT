# Codex CX-L1 Preflight

**Date:** 2026-04-23 20:07 CST
**Owner:** Codex
**Scope:** Non-GPU preparation for Work 2 CX-L1 TinyLlama baseline.

## Status

CX-L1 is now **environment-ready** but not yet model-ready.

Completed:

- Installed missing Python dependencies in `/home/qiaosir/miniconda3/envs/LLM`:
  - `transformers 5.6.1`
  - `datasets 4.8.4`
  - `accelerate 1.13.0`
  - `evaluate 0.4.6`
  - `sentencepiece 0.2.1`
  - `tokenizers 0.22.2`
- Created download-free environment checker:
  - `scripts/_gpt/cx_l1_env_check.py`
  - output: `report_md/_gpt/json_gpt/cx_l1_env_preflight.json`
- Created CX-L1 baseline runner:
  - `scripts/_gpt/cx_l1_tinyllama_baseline.py`
  - dry-run output: `report_md/_gpt/json_gpt/cx_l1_tinyllama_baseline.dryrun.json`

## Current Preflight Result

| Item | Status |
|---|---|
| Required Python deps | pass |
| CUDA-visible PyTorch | pass (`torch 2.10.0+cu128`) |
| TinyLlama cache | missing |
| GPT2-medium fallback cache | missing |
| WikiText dataset cache | not verified/downloaded |
| CX-L1 full run | blocked until R2 releases GPU and model/dataset download/cache is allowed |

## Execution Guard

Do not run full CX-L1 while R2 owns the GPU. The script is ready, but model download and perplexity evaluation are deferred until Work 1 GPU queue is clear.

## Prepared Full Command

Primary TinyLlama command, to run after R2 completes:

```bash
cd /home/qiaosir/projects/compute_vit
/home/qiaosir/miniconda3/envs/LLM/bin/python scripts/_gpt/cx_l1_tinyllama_baseline.py \
  --model-id TinyLlama/TinyLlama-1.1B-intermediate \
  --dataset wikitext \
  --dataset-config wikitext-103-raw-v1 \
  --split validation \
  --device cuda \
  --dtype fp16 \
  --amp \
  --block-size 1024 \
  --stride 512 \
  --max-tokens 10000 \
  --json-out report_md/_gpt/json_gpt/cx_l1_tinyllama_baseline.json
```

Fallback GPT2-medium command if TinyLlama fails:

```bash
cd /home/qiaosir/projects/compute_vit
/home/qiaosir/miniconda3/envs/LLM/bin/python scripts/_gpt/cx_l1_tinyllama_baseline.py \
  --model-id gpt2-medium \
  --dataset wikitext \
  --dataset-config wikitext-103-raw-v1 \
  --split validation \
  --device cuda \
  --dtype fp16 \
  --amp \
  --block-size 1024 \
  --stride 512 \
  --max-tokens 10000 \
  --json-out report_md/_gpt/json_gpt/cx_l1_gpt2_medium_baseline.json
```
