# GEMINI T1 Energy Interpretation
**Date:** 2026-04-23
**Scope:** T1 Energy Support (Auxiliary)

## (a) What the script currently computes
The `run_energy_sensitivity.py` script calculates the total analog inference energy by summing hardware-level components (ADC conversions, DAC conversions, and crossbar array accesses), and optionally sweeps the digital multiplier cost (`E_mult_fJ`) used for scale recovery.
In the original buggy output (`energy_sensitivity_analysis.json`), the script compared this total analog energy against a hardcoded, arbitrary micro-level digital baseline (e.g., 1 pJ), yielding a nonsensical speedup (e.g., 0.015x). In the corrected `energy_scale_recovery_sensitivity.json`, the analog energy is computed as `~23.92 µJ`. It then computes the scaling penalty, demonstrating that digital scale-recovery adds <0.1% overhead if `E_mult < 1 fJ`.

## (b) What the paper claim likely computes
The manuscript claims an **11.45x** energy efficiency improvement over a digital FP32 baseline.
This calculation requires a pre-computed or externally profiled full-system digital energy cost for FP32 inference on Tiny-ViT, which the paper assumes to be **273.94 µJ**.
The paper's algebra is strictly:
`Speedup = Digital_FP32_Energy / Analog_Total_Energy = 273.94 µJ / 23.924 µJ ≈ 11.45x`.
For the INT8 comparison, it assumes a linear 4x reduction: `Digital_INT8_Energy = 273.94 / 4 = 68.485 µJ`, resulting in `68.485 / 23.924 ≈ 2.86x`.

## (c) Why they diverge
The original divergence occurred because the script lacked the macroscopic system-level baseline (`273.94 µJ`) and improperly mixed device-level metrics with system-level claims.
The paper's `11.45x` claim is a *macro-level system comparison* (total analog CIM macro vs total digital accelerator). The script originally performed an internal bottom-up calculation but failed to use a matching top-down digital reference.
The new v2 JSON resolves the algebraic mismatch by directly injecting the `273.94 µJ` assumption. The script is now internally self-consistent with the paper's algebra. However, it must be noted that the INT8 baseline (`/ 4`) is a first-order architectural assumption, not an empirical hardware measurement.
