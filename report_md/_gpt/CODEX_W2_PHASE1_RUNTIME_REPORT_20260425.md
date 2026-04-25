# Codex W2 Phase 1 Runtime Report
**Date:** 2026-04-25  
**Owner:** Codex  
**Task:** Pythia 410M runtime smoke for Work 2 W1  
**Status:** CORE W1 RUNTIME SMOKE COMPLETE

## Environment
Runtime Python:
```bash
/home/qiaosir/miniconda3/envs/LLM/bin/python
```

Observed packages:
- PyTorch: `2.10.0+cu128`
- Transformers: `5.6.1`
- CUDA available: yes
- GPU: NVIDIA GeForce RTX 5070 Ti, 16GB

## Files Updated
- `paper2/src/smoke_pythia_hybrid.py`
- `paper2/src/train_llm_hybrid.py`
- `paper2/src/llm_hybrid.py`

## Fixes Made During Runtime Validation
1. `smoke_pythia_hybrid.py` now inserts the project root into `sys.path`, so it can be executed directly from `paper2/src/` and still import `analog_layers.py`.
2. `llm_hybrid.convert_pythia_to_hybrid()` now moves replacement `AnalogLinear` modules to the source module's device and dtype before copying weights. This avoids CPU/GPU or dtype mismatches after in-place conversion.
3. `train_llm_hybrid.py` is no longer a placeholder. It supports conservative Pythia training smoke with selectable train scope, local-files-only loading, high-precision analog mode, optional analog noise, and D2D resampling counters.

## Pythia FP Forward Smoke
Command:
```bash
/home/qiaosir/miniconda3/envs/LLM/bin/python paper2/src/smoke_pythia_hybrid.py --local-files-only --max-length 64
```

Result:
- Model: `EleutherAI/pythia-410m-deduped`
- Model type: `gpt_neox`
- Hidden size: 1024
- Layers: 24
- Heads: 16
- Intermediate size: 4096
- Max positions: 2048
- Input shape: `[2, 14]`
- Parameter count: 405,334,016
- QKV modules found: 24
- Attention output modules found: 24
- MLP modules found: 48
- Skipped linear modules: 1 (`embed_out`/LM head path)
- FP16 CUDA smoke loss: 6.912417888641357
- FP16 CUDA smoke perplexity: 1004.6734619140625
- Peak CUDA memory: 0.7803GB

This is a tiny smoke batch and must not be cited as a benchmark result.

## No-Noise Hybrid Forward Drift
Command:
```bash
/home/qiaosir/miniconda3/envs/LLM/bin/python paper2/src/smoke_pythia_hybrid.py --local-files-only --max-length 64 --dtype float32 --hybrid --high-precision-analog
```

Result:
- FP32 FP loss: 6.907759666442871
- FP32 FP perplexity: 1000.00439453125
- High-precision no-noise hybrid loss: 6.907618999481201
- High-precision no-noise hybrid perplexity: 999.8637084960938
- Loss delta: -0.00014066696166992188
- Peak CUDA memory: 3.7801GB

Verdict: high-precision no-noise analog wrapping preserves the Pythia forward path for this smoke batch.

## 4-bit No-Noise Hybrid Drift
Command:
```bash
/home/qiaosir/miniconda3/envs/LLM/bin/python paper2/src/smoke_pythia_hybrid.py --local-files-only --max-length 64 --dtype float32 --hybrid
```

Result:
- FP32 FP loss: 6.907759666442871
- 4-bit no-noise hybrid loss: 11.041693687438965
- Loss delta: +4.133934020996094
- FP32 FP perplexity: 1000.00439453125
- 4-bit no-noise hybrid perplexity: 62423.2890625
- Peak CUDA memory: 3.7801GB

Verdict: direct all-QKV/O/MLP 4-bit wrapping is highly destructive on Pythia 410M before any adaptation. W2 should treat this as a risk signal, not as a final failure.

## 100-step Training Smoke
Command:
```bash
/home/qiaosir/miniconda3/envs/LLM/bin/python paper2/src/train_llm_hybrid.py --local-files-only --dtype float32 --hybrid --high-precision-analog --train-scope last_block --steps 100 --lr 1e-5 --max-length 64 --resample-every 50
```

Setup:
- Hybrid: yes
- Analog: high-precision, no-noise
- Train scope: final GPT-NeoX block only
- Trainable parameters: 12,596,224
- Optimizer: SGD
- Data: fixed four-sentence smoke batch, not a benchmark dataset

Result:
- Initial loss: 6.488205909729004
- Final loss: 6.1901140213012695
- Loss delta: -0.2980918884277344
- Loss decreased: true
- D2D resample counter: 96 modules at step 49 and 96 modules at step 99
- Peak CUDA memory: 3.7608GB
- Elapsed: 12.35s

Verdict: W1 training/backprop/optimizer path works for a conservative last-block high-precision hybrid smoke and fits comfortably under 14GB.

## Canonical Noise Smoke
Command:
```bash
/home/qiaosir/miniconda3/envs/LLM/bin/python paper2/src/train_llm_hybrid.py --local-files-only --dtype float32 --hybrid --high-precision-analog --noise-enabled --sigma-d2d 0.10 --sigma-c2c 0.05 --train-scope last_block --steps 20 --lr 1e-5 --max-length 64 --resample-every 10
```

Result:
- Initial loss: 12.305581092834473
- Final loss: 13.662256240844727
- Loss delta: +1.356675148010254
- Loss decreased: false
- D2D resample counter: 96 modules at step 9 and 96 modules at step 19
- Peak CUDA memory: 3.7608GB

Verdict: canonical noise path executes and D2D resampling works, but direct noisy all-projection/all-MLP training is unstable on this smoke. W2 should not begin with fully noisy all-module training. Use staged adaptation: no-noise/high-precision sanity -> 4-bit schedule -> noise schedule -> KV-cache noise.

## Current W1 Acceptance Status
| Criterion | Status |
|---|---|
| Pythia loads locally | PASS |
| Module discovery works | PASS |
| No-NaN FP forward | PASS |
| No-noise hybrid forward drift | PASS in high-precision mode |
| 4-bit wrapper checked | PASS but destructive |
| 100-step training loss decreases | PASS for last-block high-precision no-noise smoke |
| D2D resample counter works | PASS |
| GPU memory under 14GB | PASS, peak ~3.78GB |
| Full analog KV-cache integration into HF attention | NOT YET |
| WikiText-103 perplexity baseline | NOT YET |

## Recommended Next Steps
1. Add eval-only integration of `AnalogKVCache` into Pythia attention or a controlled attention wrapper.
2. Add a staged W2 experiment ladder:
   - FP baseline.
   - High-precision analog projection no-noise.
   - 4-bit analog projection no-noise with last-block or layerwise adaptation.
   - 4-bit projection with scheduled D2D/C2C.
   - Add analog KV-cache noise last.
3. Do not launch full noisy all-module W2 training yet; the smoke shows it is too destructive.
