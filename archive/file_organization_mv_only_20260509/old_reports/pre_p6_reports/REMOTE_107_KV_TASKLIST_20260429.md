# Remote 107 KV-Cache Task List

**Date:** 2026-04-29
**Owner:** Remote 107 agent
**Coordinator:** Codex
**Scope:** Work-2 / analog KV-cache research only. Do not run Work-1 PCM or 105 multi-dataset jobs from this task file.

## 0. Clone Target

Use the branch supplied by Codex:

```bash
git clone -b remote-107-kv-20260429 git@github.com:Leslie360/HAT.git HAT_kv107
cd HAT_kv107
```

If SSH is unavailable:

```bash
git clone -b remote-107-kv-20260429 https://github.com/Leslie360/HAT.git HAT_kv107
cd HAT_kv107
```

Read these files first:

```text
paper2/README.md
paper2/WORK2_TESTBED_DECISION_20260425.md
paper2/WORK2_ARCHITECTURAL_MAPPING_SPEC_20260425.md
paper2/WORK2_BENCHMARK_SUITE_20260425.md
paper2/src/analog_kv_cache.py
paper2/src/eval_llm_kv_cache.py
paper2/src/train_llm_hybrid.py
report_md/_gpt/CODEX_W2_SCOPED_NOISE_PROBE_REPORT_20260425.md
report_md/_gpt/CODEX_W2_KV_CACHE_OFFLINE_EVAL_REPORT_20260426.md
```

## 1. Boundary Rules

1. Do not download models or datasets if the server policy forbids downloads. Use already cached Hugging Face models or a local model path.
2. Primary model is `EleutherAI/pythia-410m-deduped`. Fallback is `EleutherAI/pythia-160m-deduped` only if already cached.
3. Start with inference-only / offline KV-cache diagnostics. Do not train full noisy LLMs first.
4. Do not run full noisy all-module Pythia until offline KV and held-out eval pass.
5. Return compact `.md` summaries and small JSON summaries only. Do not attempt to send large model files/checkpoints back.
6. Keep Work-2 KV results separate from 105 multi-dataset validation.

## 2. Required Environment Record

Create `paper2/results/remote107/ENV_107.md` with:

```bash
git rev-parse HEAD
git status --short
python -V
python - <<'PY'
import torch, transformers, json
print(json.dumps({
  'torch': torch.__version__,
  'cuda_available': torch.cuda.is_available(),
  'cuda_device_count': torch.cuda.device_count(),
  'cuda_devices': [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())],
  'transformers': transformers.__version__,
}, indent=2))
PY
```

Also record whether `pythia-410m-deduped` and/or `pythia-160m-deduped` are available locally. If no model is locally available and downloads are forbidden, stop and report `ENV_BLOCKED_MODEL_CACHE`.

## 3. P0: Unit Tests and Model Load Smoke

Run:

```bash
mkdir -p paper2/results/remote107 logs/_gpt
python -m pytest -q \
  tests/test_w2_analog_kv_cache.py \
  tests/test_w2_llm_hybrid_conversion.py \
  tests/test_w2_perplexity_baseline.py \
  2>&1 | tee logs/_gpt/remote107_p0_pytest.log
```

Then run a minimal local-files smoke. Use `--local-files-only` if the model is cached:

```bash
python paper2/src/eval_llm_kv_cache.py \
  --model EleutherAI/pythia-410m-deduped \
  --device cuda \
  --dtype float16 \
  --local-files-only \
  --max-length 64 \
  --layers last \
  --instances 2 \
  --read-repeats 2 \
  --noise-disabled \
  --no-quantize \
  --output-json paper2/results/remote107/p0_kv_smoke_last_no_noise.json \
  2>&1 | tee logs/_gpt/remote107_p0_kv_smoke.log
```

Pass criteria:

- Tests pass or failures are clearly unrelated to KV-cache logic.
- Smoke JSON exists.
- No-noise/no-quantize `kv_relative_mse` should be near zero. If it is above `1e-6`, treat as implementation bug and stop.

## 4. P1: Offline KV-Cache Reconstruction Matrix

This is mandatory. It measures real Pythia KV tensors stored/read through `AnalogKVCache`, but does not yet patch Hugging Face attention.

Use `max-length=128`, `instances=10`, `read-repeats=5` unless memory fails.

### P1-A: Quantization-only bit sweep, last layer

Run bit widths `16, 8, 6, 4` with noise disabled:

```bash
for bw in 16 8 6 4; do
  python paper2/src/eval_llm_kv_cache.py \
    --model EleutherAI/pythia-410m-deduped \
    --device cuda --dtype float16 --local-files-only \
    --max-length 128 --layers last \
    --instances 10 --read-repeats 5 \
    --noise-disabled --bit-width "$bw" \
    --output-json "paper2/results/remote107/p1a_last_quant_bw${bw}.json" \
    2>&1 | tee "logs/_gpt/remote107_p1a_last_quant_bw${bw}.log"
done
```

### P1-B: Canonical low-noise sweep, last vs all layers

Run layers `last` and `all` at bit widths `16, 8, 6, 4` using canonical low noise `sigma_d2d=0.005`, `sigma_c2c=0.002`:

```bash
for layers in last all; do
  for bw in 16 8 6 4; do
    python paper2/src/eval_llm_kv_cache.py \
      --model EleutherAI/pythia-410m-deduped \
      --device cuda --dtype float16 --local-files-only \
      --max-length 128 --layers "$layers" \
      --instances 10 --read-repeats 5 \
      --sigma-d2d 0.005 --sigma-c2c 0.002 --bit-width "$bw" \
      --output-json "paper2/results/remote107/p1b_${layers}_n005002_bw${bw}.json" \
      2>&1 | tee "logs/_gpt/remote107_p1b_${layers}_n005002_bw${bw}.log"
  done
done
```

### P1-C: Noise-source split, last layer

Run D2D-only and C2C-only at 8-bit and 16-bit:

```bash
for bw in 16 8; do
  python paper2/src/eval_llm_kv_cache.py --model EleutherAI/pythia-410m-deduped \
    --device cuda --dtype float16 --local-files-only --max-length 128 --layers last \
    --instances 10 --read-repeats 5 --sigma-d2d 0.005 --sigma-c2c 0.0 --bit-width "$bw" \
    --output-json "paper2/results/remote107/p1c_last_d2donly_bw${bw}.json" \
    2>&1 | tee "logs/_gpt/remote107_p1c_last_d2donly_bw${bw}.log"
  python paper2/src/eval_llm_kv_cache.py --model EleutherAI/pythia-410m-deduped \
    --device cuda --dtype float16 --local-files-only --max-length 128 --layers last \
    --instances 10 --read-repeats 5 --sigma-d2d 0.0 --sigma-c2c 0.002 --bit-width "$bw" \
    --output-json "paper2/results/remote107/p1c_last_c2conly_bw${bw}.json" \
    2>&1 | tee "logs/_gpt/remote107_p1c_last_c2conly_bw${bw}.log"
done
```

## 5. P2: Context-Length Scaling

Only run after P1 completes. Use canonical low noise and compare last vs all layers.

```bash
for L in 64 128 256 512; do
  for layers in last all; do
    python paper2/src/eval_llm_kv_cache.py \
      --model EleutherAI/pythia-410m-deduped \
      --device cuda --dtype float16 --local-files-only \
      --max-length "$L" --layers "$layers" \
      --instances 10 --read-repeats 5 \
      --sigma-d2d 0.005 --sigma-c2c 0.002 --bit-width 8 \
      --output-json "paper2/results/remote107/p2_${layers}_ctx${L}_bw8_n005002.json" \
      2>&1 | tee "logs/_gpt/remote107_p2_${layers}_ctx${L}_bw8_n005002.log"
  done
done
```

If 512 OOMs, record OOM and stop at 256. Do not silently reduce batch/model without recording it.

## 6. P3: End-to-End Attention Integration Design, Not Full Training

After P1/P2, decide if end-to-end analog KV-cache is worth implementation.

Required design memo: `paper2/results/remote107/P3_ATTENTION_PATCH_DESIGN.md`

It must answer:

1. Where Pythia/GPT-NeoX creates and reads `past_key_values` in the installed `transformers` version.
2. Whether a clean monkey-patch/subclass can replace only cache read/write without modifying model weights.
3. How to compare four modes:
   - FP baseline, digital projections, digital KV.
   - Analog cache only, digital projections.
   - Analog projections only, digital KV.
   - Analog projections plus analog KV.
4. Exact perplexity/loss metric and text split.
5. Expected risk points.

Do not run long training in P3. If implementing a tiny patch, run only a smoke batch and report loss delta.

## 7. Kill Criteria

Stop and report instead of continuing if any condition occurs:

1. P0 no-noise/no-quantize `kv_relative_mse > 1e-6`.
2. Model cannot load locally and downloads are forbidden.
3. P1 all-layer 8-bit canonical noise produces `kv_relative_mse` more than 10x the last-layer value. In that case, stop all-layer lower-bit sweeps and focus on selective/last-layer cache.
4. Any end-to-end 8-bit analog KV-cache smoke increases loss/perplexity by more than 10% vs FP baseline. Stop lower-bit end-to-end experiments; report selective-cache alternatives.
5. Any run OOMs twice. Record command, GPU, memory, and stop that cell.

## 8. Return Format

Return one markdown file only if data transfer is constrained:

`REMOTE_107_KV_RETURN_YYYYMMDD.md`

Required sections:

```text
1. Environment summary
2. Exact git commit hash and branch
3. Model availability and local model path/cache status
4. P0 pass/fail
5. P1 table: layers, bit_width, sigma_d2d, sigma_c2c, kv_relative_mse, k_relative_mse, v_relative_mse
6. P2 context-length table
7. Any OOM/failure cells with exact command
8. Recommendation: last-layer only / selective layers / all-layer / abandon KV-cache path
9. Attach or paste compact JSON summaries for the top 5 most important runs
```

Do not send large checkpoints. If small JSONs can be sent, send only `paper2/results/remote107/*.json` and logs under 1 MB.

## 9. Current Prior Belief From Local Codex

Local smoke tests suggested:

- QKV and MLP analog projection paths are fragile under noise.
- Attention output is safer than QKV/MLP.
- KV-cache should be evaluated as its own storage problem before full noisy all-module LLM experiments.
- The main Work-2 novelty is persistent analog KV-cache storage with persistent D2D and fresh C2C reads, not merely analogizing projection weights.

Therefore 107 should prioritize **cache-only inference diagnostics** before any training-heavy claims.

---

## 10. Update After Remote 107 PPL Delivery — 2026-04-29 11:05 CST

Remote 107 has already moved beyond the original offline-only task list and reports end-to-end WikiText-2 PPL with analog KV-cache injection.

Reported provisional PPL table:

| Profile | Retention | PPL |
|---|---:|---:|
| PCM 32-state | off | 107.27 |
| Organic | off | 429.05 |
| Organic | on | 683.74 |
| PCM 32-state | on | 751.28 |

This result is promising, but must now pass reproducibility and parity gates before it is used as evidence.

### 10.1 Immediate Required Return

Return one Markdown file with:

```bash
git rev-parse HEAD
git status --short
git diff --stat
git diff -- paper2 scripts tests
python - <<'PY'
import torch, transformers, json
print(json.dumps({
  'torch': torch.__version__,
  'transformers': transformers.__version__,
  'cuda': torch.version.cuda,
  'device_count': torch.cuda.device_count(),
  'devices': [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())],
}, indent=2))
PY
```

Also report:

- exact model and tokenizer
- WikiText-2 split and preprocessing
- sliding-window max length, stride, overlap loss accounting, token count, total NLL
- exact PCM and Organic profile equations/parameters
- exact retention-time mapping for `0.1s`
- cache scope: K only, V only, or K+V; layer subset or all layers

### 10.2 Validation Gate

Run these before any larger sweep:

| Run | Purpose | Kill criterion |
|---|---|---|
| Digital FP baseline | evaluator baseline | PPL implausible for chosen model |
| Analog no-quant/no-noise/no-retention | injection parity | PPL differs from digital by >1% |
| PCM 32-state retention off, 3 seeds | static reproducibility | result not near reported 107.27 |
| PCM 32-state retention on, 3 seeds | avalanche reproducibility | result not near reported 751.28 |
| Organic retention off/on, 3 seeds | rank inversion stability | retention ranking not stable |

### 10.3 Next Sweep Priority

1. Retention time sweep: `0, 0.01, 0.03, 0.1, 0.3, 1.0s` for PCM and Organic.
2. Noise-source ablation: quantization only, static programming noise only, read/cycle noise only, retention only, full profile.
3. KV scope ablation: K only, V only, K+V.
4. Layer scope ablation: last 25% layers vs all layers.
5. Per-position NLL buckets to show whether failure is a late-context avalanche.

### 10.4 Updated Narrative Hypothesis

Do not frame the result as a broad material ranking yet. The correct provisional hypothesis is:

> Analog KV-cache viability is governed by temporal memory stability, not static write precision alone. Retention can invert material ranking: PCM is best statically but may collapse under cache lifetime dynamics, while Organic is worse statically but degrades more gradually.

See `report_md/_gpt/REMOTE_107_KV_DELIVERY_REVIEW_20260429.md` for Codex's full review.

---

## 11. Update After 107 Selective-Layer Results — 2026-04-29

107 returned new PPL data:

- Digital baseline: PPL 15.68.
- 8-bit all-layer zero-noise: PPL 17.48 = 1.115x baseline, fails 10% gate.
- 6-bit all-layer is not viable even without noise: PPL 32.41.
- Last-layer-only 8-bit passes:
  - zero-noise PPL 15.82 = 1.009x
  - realistic PPL 16.72 = 1.066x
- All-layer HAT warmup helps but remains far from acceptable: PPL 579.52 -> 142.27 after 50 steps.

### New Route Lock

All-layer analog KV-cache is abandoned. Continue only selective terminal-layer KV-cache plus HAT adaptation.

### Next Required Experiments

1. 8-bit selective depth sweep:

```text
last1, last2, last4, last6, last8, all24
zero-noise, realistic, D2D-only, C2C-only
```

2. 6-bit selective pilot:

```text
last1, last2, last4
zero-noise first; add realistic only if zero-noise passes.
```

3. Selective HAT warmup:

```text
last1 realistic 8-bit
last2 realistic 8-bit
last4 realistic 8-bit if not catastrophic
steps: 0, 50, 100, 200, 500
```

4. 3-seed repeat for the best passing scope:

```text
seeds: 42, 123, 456
```

### Gate

Baseline PPL is 15.68, so the 10% gate is:

```text
PPL <= 17.248
```

Stop expanding scope after two consecutive larger scopes fail under realistic noise.

Return compact Markdown only. Do not push from remote.

### 11.1 Addendum — HAT Rescue Pending

Do not overstate the all-layer decision before HAT validation returns.

Current status:

- Non-HAT all-layer analog KV-cache fails.
- Selective terminal-layer KV is currently the safest path.
- HAT-rescued all-layer remains under evaluation.

For the next 107 return, prioritize HAT step curves:

```text
all-layer 8-bit realistic: steps 0, 50, 100, 200, 500
last1/last2/last4 8-bit realistic: steps 0, 50, 100, 200, 500
```

Gate:

```text
PPL <= 1.10x baseline reopens the route.
PPL > 1.20x after adequate HAT steps closes that scope.
```
