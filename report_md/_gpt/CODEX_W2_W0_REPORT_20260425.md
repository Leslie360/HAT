# Codex W2 W0 Report
**Date:** 2026-04-25  
**Owner:** Codex  
**Task:** Round-8 Work 2 W0 testbed lock + architecture mapping + benchmark suite  
**Status:** COMPLETE

## Deliverables Written
- `paper2/README.md`
- `paper2/WORK2_TESTBED_DECISION_20260425.md`
- `paper2/WORK2_ARCHITECTURAL_MAPPING_SPEC_20260425.md`
- `paper2/WORK2_BENCHMARK_SUITE_20260425.md`

## Decision Summary
- Testbed locked to `EleutherAI/pythia-410m-deduped`.
- Fallback: `EleutherAI/pythia-160m-deduped` only if 410M cannot load locally.
- Source facts verified from Hugging Face model card: Apache 2.0, 24 layers, model dim 1024, 16 heads, 302,311,424 non-embedding params, 405,334,016 total params.
- Work 2 novelty locked to persistent analog KV-cache, not only analog QKV projections.

## Important Correction for All Agents
Pythia 410M is GPT-NeoX/Pythia, not LLaMA.

Therefore:
- Do not write Methodology as if Pythia has LLaMA `gate/up/down` MLP.
- Pythia MLP target is the feed-forward pair usually exposed as `dense_h_to_4h` and `dense_4h_to_h`.
- QKV may be fused as `query_key_value`; implementation should support fused wrapping first, then optional logical Q/K/V slice analysis later.
- Normalization and rotary/positional operations remain digital.

## W1 Readiness
W1 should start in this order:
1. `paper2/src/analog_kv_cache.py` standalone primitive and unit test.
2. Pythia module discovery script / conversion dry run.
3. No-noise hybrid forward drift test.
4. KV-cache eval-only noise injection.
5. 100-step training smoke after tests are green.

## Git/Coordination State
- `origin/master` verified at `a54767a6f71f95d726b0a2c477fe26c9d8a568cc`, matching local `master` after BFG cleanup.
- No GPU job started for W0.
- Paper 1 source/manuscript files were not modified.

## Blocking Items
None for W0.

## Next Codex Action
Begin W1 implementation scaffold under `paper2/src/` and tests under `tests/`, unless a Paper 1 trigger arrives first.
