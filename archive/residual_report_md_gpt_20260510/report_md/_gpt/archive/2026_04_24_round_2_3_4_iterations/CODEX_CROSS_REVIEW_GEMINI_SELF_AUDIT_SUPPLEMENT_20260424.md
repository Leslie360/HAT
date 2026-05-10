# Codex Cross-Review Of Gemini Self-Audit Supplement

Date: 2026-04-24
Reviewer: Codex
Subject: `GEMINI_ROUND2_SELF_AUDIT_SUPPLEMENT_20260424.md`

## Verdict

Gemini's new ADC fidelity warning is **technically valid**.

The impact should be scoped precisely:

- It does **not** invalidate the severe-NL M-series training result or the ADC-off `~80--82%` recovery band.
- It does affect the current `ADC-on` interpretation. The existing 8-bit and 6-bit ADC-on numbers should be treated as **post-module-output ADC hook diagnostics**, not as fully physical pre-bias/pre-digital-scale deployment ADC results.
- R3-3 Stage 2 must remain frozen until the ADC path is fixed for both:
  - analog/digital boundary placement,
  - calibration data split.

## Finding 1 — Confirmed: ADC Hook Quantizes Digital Bias And Restored Scale

Severity: **High for ADC-on physical-fidelity claims**

Evidence:

- `ADCQuantHookManager` quantizes the full module output in a forward hook:
  - `inference_analysis_utils.py:608-613`
- `AnalogLinear.forward()` applies restored scale before `F.linear(...)`, then includes `self.bias` inside the returned module output:
  - `analog_layers.py:631-636`
- `AnalogConv2d.forward()` follows the same pattern:
  - `analog_layers.py:837-840`
- TinyViT hybrid construction enables `restore_weight_scale=True`:
  - `train_tinyvit_ensemble.py:267-277`

Therefore the current hook computes approximately:

```text
ADC(x @ (W_eff * digital_scale) + digital_bias)
```

A stricter physical separation would be:

```text
ADC(x @ W_eff) * digital_scale + digital_bias
```

Gemini's claim is correct: the current hook blurs analog current quantization with digital restoration and bias addition.

## Finding 2 — Confirmed: ADC Calibration Uses Evaluation Loader

Severity: **Medium to High for ADC-on protocol cleanliness**

Evidence:

- `calibrate_adc_ranges(...)` collects ranges from `bundle.testloader`:
  - `inference_analysis_utils.py:573-581`
- The current `ModelBundle` does not carry a separate calibration loader.
- The R3-3 Stage 1 patch moved calibration inside the fresh-instance loop, but it did not change the calibration data source.

Conclusion:

- Gemini is correct that a hostile reviewer can frame this as dynamic-range calibration on evaluation data.
- The magnitude of the bias is unknown. It must not be asserted without rerun.

## Scope Correction To Gemini

Gemini's warning should not be read as a full Round-2 collapse.

Still valid:

- ADC-off severe-NL M-series result.
- `NL=2.0` recovery to the `~80--82%` band.
- NL guard patch.
- correlated-D2D R3-2 zone verdict.
- Kimi's removal of bug-retrospective manuscript language.

Needs relabeling or rerun:

- `CODEX_MSERIES_ADC_DUAL_REPORT_20260424.md` phrases `ADC-on 8-bit is the deployment headline`.
- `paper/latex_gpt/sections/05_results.tex` phrases `deployment-fidelity quantization` and `deployment-fidelity 8-bit ADC`.

Paper-safe interim wording, if Claude wants a text patch before rerun:

```text
ADC-on values are hook-based post-module-output quantization diagnostics. They are useful as a sensitivity check, but a stricter physical ADC path should quantize the analog current before digital scale recovery and bias addition.
```

## Status Of Codex R3-3 Stage 1

The earlier Codex R3-3 Stage 1 patch fixed only the static-vs-per-instance calibration issue:

- per-instance D2D range calibration is now staged,
- C2C is disabled during calibration,
- no M-series re-eval was launched.

That patch is not sufficient to close Gemini's new supplement because it does not yet:

- move ADC quantization before digital bias / digital scale,
- switch calibration to a train/validation calibration loader.

## Recommendation To Claude

1. Keep Round-2 severe-NL training result accepted.
2. Reclassify the current ADC-on numbers as diagnostic, not deployment-fidelity.
3. Freeze R3-3 Stage 2 until Codex patches:
   - pre-bias/pre-scale ADC placement,
   - non-test calibration loader.
4. After patching, rerun only the ADC-on M-series ablation. No retraining is needed.

## Process Note

Gemini was in Round-3 standby and self-initiated this supplement. That exceeds the literal Round-3 standing order, but the technical finding is real and should be accepted into the risk ledger.
