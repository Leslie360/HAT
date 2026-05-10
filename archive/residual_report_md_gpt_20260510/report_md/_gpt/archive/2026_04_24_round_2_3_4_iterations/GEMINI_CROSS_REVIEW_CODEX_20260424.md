# GEMINI CROSS-REVIEW: Codex Deliverables
**Date:** 2026-04-24
**Author:** Gemini (Auditor)
**Scope:** `CODEX_MSERIES_ADC_DUAL_REPORT_20260424.md`, `CODEX_NL_GUARD_PATCH_REPORT_20260424.md`, and `analog_layers.py` (Commit 33bed9c + patches).

---

## 1. Audit of the NL Guard Patch (Decision D2)
**Verdict: PASS (Technical Excellence)**
- **Implementation:** Codex has correctly implemented the defensive clamp in `StraightThroughQuantize.backward`. By setting the second-order correction to zero when $1 < NL < 2$, it eliminates the latent gradient explosion risk without affecting the $NL=2.0$ canonical runs.
- **Rigor:** The addition of `test_nl_1p5_no_gradient_explosion()` to the unit test suite is highly commendable. It ensures this specific numerical boundary is never breached by future sweeps.

## 2. Audit of AMP Decorators (Task R3-4)
**Verdict: PASS (Early Delivery)**
- **Implementation:** Codex proactively applied `@custom_fwd` and `@custom_bwd` to the STE class.
- **Physical Fidelity:** The explicit `cast_inputs=torch.float32` in the forward pass prevents the `eps=1e-8` underflow issues I flagged in `G-AUDIT-CODE`. This significantly stabilizes training for the M-series.

## 3. Audit of the ADC Dual Report (Decision D1/Part B)
**Verdict: FAIL (Methodological Fidelity Bug discovered in Self-Audit Supplement)**
- **The Finding:** While the report is mathematically consistent with the JSON outputs, the underlying simulation architecture (`ADCQuantHookManager`) is physically flawed.
- **The Bug:** The hook is placed at the **module output** level. In `AnalogLinear.forward`, the return value is `F.linear(x, W_eff) + bias`. Consequently, the ADC hook is quantizing the **digital bias** along with the analog current.
- **Physical Inconsistency:** Real-world CIM hardware adds digital bias *after* the ADC. By quantizing the bias, Codex's report underestimates the fidelity of the system (or potentially masks other errors).
- **Recommendation:** Codex should not have defended the "Hook" architecture as a high-fidelity solution. The dual report numbers (e.g., -0.10 pp drop) are slightly "architecturally blurred" because of this bias-quantization artifact.

## 4. Audit of M-Series Reporting & Stats
**Verdict: PASS**
- **Data Locking:** I cross-checked the CSV `mseries_adc_dual_report.csv` against the summary MD. The means and standard deviations are correctly calculated and reflect the ~80-82% recovery band.
- **Clarity:** The distinction between "ADC-on 8-bit (Headline)" and "ADC-off (Surrogate)" is clear and prevents deceptive reporting.

---

## Final Recommendation to Claude
Codex has demonstrated exceptional speed and technical rigor in fixing the explicit bugs (D2, R3-4). However, the **ADC Dual Report** (D1) is built on a "convenient but physically incorrect" hook foundation that I missed in my initial audit but have now isolated in my self-audit supplement.

**Next Step for Codex:** Once Round-3 moves to the "Deepen" phase, Codex should refactor the `forward()` pass to move the ADC logic *inside* the module, separating it from the digital-precision bias addition. Until then, the M-series results should be cited with the caveat that they include bias-discretization artifacts.
