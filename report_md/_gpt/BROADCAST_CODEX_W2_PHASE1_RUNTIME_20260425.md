# BROADCAST — CODEX W2 PHASE 1 RUNTIME SMOKE COMPLETE
**Date:** 2026-04-25  
**From:** Codex  
**To:** Claude, Kimi, Gemini, User  
**Status:** W1 runtime smoke complete; full KV-cache integration remains

## Action
Codex continued Round-8 W1 beyond scaffold and ran real Pythia 410M runtime smoke on the local 16GB GPU using:
```bash
/home/qiaosir/miniconda3/envs/LLM/bin/python
```

## Files Updated
- `paper2/src/smoke_pythia_hybrid.py`
- `paper2/src/train_llm_hybrid.py`
- `paper2/src/llm_hybrid.py`
- `report_md/_gpt/CODEX_W2_PHASE1_RUNTIME_REPORT_20260425.md`

## Key Results
- Pythia 410M loads locally on CUDA.
- Module discovery: 24 QKV, 24 attention output, 48 MLP, 1 skipped LM-head linear.
- FP16 FP smoke: loss 6.9124, peak memory 0.780GB.
- High-precision no-noise hybrid drift: FP32 FP loss 6.90776 vs hybrid 6.90762, delta -0.00014, peak memory 3.78GB.
- 4-bit no-noise hybrid: loss jumps to 11.0417. Direct 4-bit all-QKV/O/MLP wrapping is destructive before adaptation.
- 100-step training smoke, high-precision no-noise last block: loss 6.4882 -> 6.1901, peak memory 3.76GB.
- D2D resample counter works: 96 modules resampled at scheduled steps.
- Canonical noise smoke executes but does not improve: loss 12.3056 -> 13.6623 over 20 steps.

## Boundary
These are smoke numbers only, not WikiText-103 benchmark results and not paper claims.

## Recommendation
Do not start W2 with fully noisy all-module training. Use staged adaptation:
1. FP baseline.
2. High-precision analog projection no-noise.
3. 4-bit no-noise adaptation.
4. Scheduled D2D/C2C noise.
5. Analog KV-cache noise last.

## Remaining W1 Work
Full `AnalogKVCache` integration into Hugging Face/Pythia attention is not complete yet. Standalone cache primitive is implemented and tested; the next infrastructure task is wiring it into eval/generation without invasive Paper 1 source edits.
