<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 9cdbe77 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# KIMI Thesis Chapter Outline — 2026-04-20

## Chapter title
Hardware-Aware Training, Fresh-Instance Transfer, and Robustness Boundaries in Organic Optoelectronic CIM

## Recommended structure

### 1. Problem framing: why device-level metrics are insufficient
- Reuse NC manuscript motivation.
- Thesis-only emphasis: deployment risk is a distributional problem, not a single-array benchmark.

### 2. Canonical failure mode: fixed-mask HAT collapses on fresh hardware
- Anchor result: standard-HAT `10.00 ± 0.00%` fresh-instance collapse.
- Figure: current fresh-instance robustness panel.
- Thesis-only angle: deterministic single-class collapse as an optimizer/distribution mismatch phenomenon.

### 3. Ensemble HAT as the main deployment remedy
- Anchor result: `86.37 ± 1.54%` canonical fresh-instance recovery.
- Reuse NC Eq. 4 / methodology instead of restating the whole derivation.

### 4. Severe-NL boundary: what can and cannot be rescued
- Anchor results:
  - global severe-NL baseline `27.72 ± 0.82%`
  - `MLP-only` in-domain rescue `87.79%`
  - `QKV-only` / `attn_proj-only` collapse
  - `all-linear` fresh-instance `32.60 ± 9.18%`
- Thesis-only point: source-domain rescue is not the same as deployment-grade transfer.

### 5. Spatial robustness beyond i.i.d. mismatch
- Anchor result:
  - correlated-D2D sweep: `86.33 ± 1.61%` → `84.57 ± 2.39%` → `82.12 ± 3.95%`
- Thesis-only point: ranking survives moderate spatial structure, but the variance budget widens.

### 6. Thesis-only next step: joint MLP-linear + Ensemble HAT training
- Use the 32% fresh-instance ceiling as the baseline to beat.
- This becomes the thesis punchline experiment rather than part of the NC paper.

### 7. Outlook
- ImageNet pilot
- fabricated-array calibration
- circuit-aware spatial / thermal layers
