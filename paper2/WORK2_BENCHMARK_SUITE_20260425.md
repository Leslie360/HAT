# Work 2 Benchmark Suite
**Date:** 2026-04-25  
**Owner:** Codex  
**Round:** Round-8 W0  
**Status:** LOCKED for W1 smoke; expandable in W2

## Benchmark Principle
W1 benchmarks are infrastructure checks, not publication claims. W2 benchmarks become the first result-generating suite after smoke tests pass.

The benchmark suite must separate three effects:
1. Analog projection noise in QKV/output/MLP.
2. Analog KV-cache storage/read noise.
3. Context-length stress from repeated cache reads.

## W1 Smoke Metrics
| Metric | Dataset/Slice | Purpose | Acceptance |
|---|---|---|---|
| FP no-NaN forward loss | Tiny fixed text batch | Confirms model/tokenizer load and baseline forward path. | Runs without NaN/Inf. |
| No-noise hybrid loss drift | Same fixed batch | Confirms analog wrapper preserves weights and shape semantics. | Loss close to FP baseline; exact tolerance set after first run. |
| KV-cache deterministic read test | Synthetic tensor | Confirms D2D persistence and C2C freshness. | Same D2D across reads; different C2C under stochastic mode. |
| 100-step training smoke | Small WikiText-103 shard or local text shard | Confirms gradients and optimizer path work. | Loss decreases over the 100-step window. |
| GPU memory footprint | Pythia 410M W1 run | Confirms local feasibility. | Peak under 14GB on 16GB GPU. |

## W2 Primary Benchmark
Primary metric: WikiText-103 perplexity.

Protocol:
- Baseline: FP Pythia 410M, no analog wrappers.
- Projection-only analog: QKV/output/MLP analog, digital KV-cache.
- KV-cache analog: QKV/output/MLP analog plus persistent analog KV-cache.
- Standard HAT vs Ensemble HAT: compare source instance and fresh-instance behavior under identical noise settings.

Report:
- Mean perplexity.
- Relative perplexity increase vs FP baseline.
- Source/fresh gap.
- Fresh-instance mean and standard deviation over 10 D2D instances x 5 C2C MC samples.

## W2 Context-Length Stress Benchmark
Secondary metric: sliding-window or autoregressive decode perplexity under context lengths:
- 128 tokens
- 512 tokens
- 1024 tokens
- 2048 tokens

Purpose:
- Detect whether analog KV-cache degradation grows with context length.
- Separate persistent D2D effects from per-read C2C effects.
- Test the Work 2 theoretical claim that C2C can average across repeated reads while D2D remains instance-specific.

Report:
- Perplexity by context length.
- Degradation slope vs log context length.
- Projection-only vs analog-cache gap.
- Optional per-layer/per-head sensitivity heatmap if W2 time allows.

## Optional Tertiary Benchmark
MMLU 5-shot can be added only after W2 perplexity and context-length benchmarks are stable.

Reason for deferral:
- MMLU adds prompt formatting and variance concerns.
- Pythia 410M is not instruction-tuned, so absolute scores are weak; the useful signal would be relative degradation only.
- It should not block infrastructure validation.

## Dataset Policy
Preferred:
- WikiText-103 via Hugging Face `datasets` or a locally cached equivalent.

Fallback if network or dataset access blocks W1:
- Use a fixed local text shard for smoke tests only.
- Mark all results from fallback data as non-publication smoke results.
- Do not report fallback perplexity as a paper number.

## Result Table Template
| Run | Projections | KV-cache | Training | Noise | Context | PPL | Relative PPL | Fresh Mean | Fresh Std | Notes |
|---|---|---|---|---|---:|---:|---:|---:|---:|---|
| FP baseline | Digital | Digital | none | none | 2048 | TBD | 1.00x | N/A | N/A | W2 baseline |
| Hybrid no-noise | Analog wrappers | Digital | none | off | 2048 | TBD | TBD | N/A | N/A | W1/W2 sanity |
| Standard HAT | Analog | Analog | Standard | 5%C2C/10%D2D | 2048 | TBD | TBD | TBD | TBD | W2 |
| Ensemble HAT | Analog | Analog | Ensemble | 5%C2C/10%D2D | 2048 | TBD | TBD | TBD | TBD | W2 |

## Stop Conditions
Stop and escalate if:
- Pythia 410M cannot load locally after reasonable environment fixes.
- No-noise hybrid forward drift is large, implying conversion changed math.
- KV-cache integration requires invasive edits to Paper 1 code or Hugging Face internals that would make W1 brittle.
- Paper 1 trigger work arrives.
