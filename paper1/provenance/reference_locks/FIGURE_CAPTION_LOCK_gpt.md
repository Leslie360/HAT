# Figure Caption Lock (GPT)

This file records the caption-level semantics that should remain stable during final template migration.

It is intentionally short. It does not replace `FIGURE_PLAN.md`; it only locks the paper-facing wording that is easiest to accidentally drift during late-stage edits.

## Scope

- Applies to the English submission package.
- `paper_zh/` may mirror these points, but Codex does not edit it.

## Locked Caption Semantics

### Fig.1

- Present as a **hybrid analog/digital system overview**.
- Must explicitly show that `QK^T`, `AV`, `softmax`, and `LayerNorm` remain digital.
- Do not imply a fully analog transformer.

### Fig.2

- Present as a **behavioral weight-to-conductance mapping flow**.
- Do not imply pulse-accurate write dynamics or full circuit predictiveness.
- Caption should reinforce the paper-wide downgrade:
  - `first-order behavioral simulation framework`

### Fig.4

- Present as the **cross-dataset accuracy comparison**.
- Axes/caption should preserve:
  - datasets: `CIFAR-10 / CIFAR-100 / Flowers-102`
  - architectures: `ConvNeXt-Tiny / Tiny-ViT-5M`
  - training regimes: `FP32 / Standard-noise / HAT`
- `Flowers-102` should be framed as a **low-data boundary**, not a generic method failure.

### Fig.5

- Present as the **degradation / recovery summary**, not a second raw-accuracy plot.
- Left panel:
  - `FP32 -> Standard-noise` degradation
- Right panel:
  - `Standard-noise -> HAT` recovery
- Caption should note that FP32 baselines are also shown so that weak absolute baselines are not hidden.

### Fig.6

- Present as the **physical front-end compensation trade-off**.
- Must preserve the message:
  - inverse-gamma compensation can recover signal in dark/high-dark-current regimes
  - bright-region noise amplification remains a real cost

### Fig.7

- Present only the **canonical retention curves**:
  - ConvNeXt C9
  - corrected Tiny-ViT V4
- The Tiny-ViT plateau must be described as **near 79\%**, not `84\%`.
- If uncertainty bands are mentioned, state explicitly:
  - `shaded bands denote ±1 std across Monte Carlo runs`

### Fig.8

- Present as a **Pareto-style energy/accuracy summary** under the current operation-count assumptions.
- Do not claim a globally optimal frontier independent of future measured-device calibration.

### Fig.9

- Present as **continuous noise sensitivity + ADC threshold evidence**.
- The `6-bit` knee should be explicit in the caption.
- Missing companion data, if any, should be described as pending rather than implied complete.

### Fig.10

- Must be described as **Zero-Shot Hardware Transferability**.
- Do not caption it as cross-device peak-performance comparison.
- Keep the distinction between:
  - same-instance robustness
  - fresh-instance transferability

### Fig.11

- Present as the **energy breakdown** under the current profiler assumptions.
- Avoid implying measured silicon power.

### Fig.12

- Present as a **qualitative attention-map comparison**.
- Do not overclaim from a small fixed sample set.

## Alignment Notes for Gemini

- If the Chinese captions are mirrored later, preserve the same scientific boundaries:
  - `Flowers-102` = low-data boundary
  - `Fig.7` = corrected `~79%` plateau
  - `Fig.10` = zero-shot transferability
  - `Fig.2` = behavioral abstraction, not full physical predictiveness
