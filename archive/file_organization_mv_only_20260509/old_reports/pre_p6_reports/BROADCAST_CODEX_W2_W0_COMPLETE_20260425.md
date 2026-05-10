# BROADCAST — CODEX W2 W0 COMPLETE
**Date:** 2026-04-25  
**From:** Codex  
**To:** Claude, Kimi, Gemini, User  
**Status:** W0 complete; W1 ready to start

## Action
Codex read the revised Round-8 broadcasts and completed the W0 deliverables requested in `DISPATCH_CODEX_W2_PHASE0_INFRASTRUCTURE_20260425.md`.

## Files Written
- `paper2/README.md`
- `paper2/WORK2_TESTBED_DECISION_20260425.md`
- `paper2/WORK2_ARCHITECTURAL_MAPPING_SPEC_20260425.md`
- `paper2/WORK2_BENCHMARK_SUITE_20260425.md`
- `report_md/_gpt/CODEX_W2_W0_REPORT_20260425.md`

## Locked Decisions
- Testbed: `EleutherAI/pythia-410m-deduped`.
- Fallback: `EleutherAI/pythia-160m-deduped` only if 410M blocks locally.
- Work 2 signature: persistent analog KV-cache with D2D persistent mismatch and C2C fresh-per-read noise.
- Digital components: embedding, normalization, rotary/position path, softmax/score normalization, activation functions, LM head initially.
- Analog components: QKV projection, attention output projection, MLP feed-forward linears, KV-cache storage/read path.

## Correction for Kimi/Claude
Pythia 410M is GPT-NeoX/Pythia, not LLaMA. Do not describe the Pythia MLP as `gate/up/down`. Use `dense_h_to_4h` and `dense_4h_to_h`. QKV may be a fused `query_key_value` projection and should be handled as fused first.

## W1 Start Order
1. Standalone `AnalogKVCache` primitive and unit test.
2. Pythia module discovery and no-edit hybrid conversion dry run.
3. No-noise hybrid forward drift test.
4. KV-cache eval-only noise injection.
5. 100-step training smoke only after tests pass.

## Verification
- `origin/master` verified at `a54767a6f71f95d726b0a2c477fe26c9d8a568cc`, matching local current master after BFG cleanup.
- W0 used zero GPU.
- Paper 1 files were not modified.

## Request to Kimi
Use `paper2/WORK2_ARCHITECTURAL_MAPPING_SPEC_20260425.md` as the source of truth for Methodology and Experimental Setup. Avoid LLaMA-specific module wording unless discussing future W3+ LLaMA extension.
