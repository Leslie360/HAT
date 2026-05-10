# Gemini Round-2 Self-Audit SUPPLEMENT (Deep Audit)
**Date:** 2026-04-24
**Author:** Gemini (Auditor)
**Subject:** Discovery of Physical Fidelity Flaws in ADC Hook Implementation

Following the formal closure of Round-2, I conducted a deep behavioral trace of the `ADCQuantHookManager` and the `forward()` methods of the analog layers. I have identified two new risks that were missed in the previous audit passes.

## 1. Physical Fidelity Bug: Digital-in-Analog Quantization
**The Issue:** `ADCQuantHookManager` attaches a `forward_hook` to the entire `AnalogLinear` / `AnalogConv2d` module.
**The Behavioral Trace:**
1. `AnalogLinear.forward` calculates `W_eff`.
2. It then multiplies `W_eff` by the digital `rescale` factor.
3. It calls `F.linear(x, W_eff * rescale, self.bias)`.
4. The **hook** then captures the result of Step 3 and quantizes it: `ADC(x * (W_eff * scale) + bias)`.

**The Physical Reality Error:**
In a real organic crossbar, the ADC quantizes the **analog current** *before* any digital scaling or digital bias addition. The correct physical order is: `ADC(x * W_eff) * scale + bias`.
By quantizing the rescaled and biased output, the current simulation incorrectly subjects high-precision digital operations (scaling and bias) to ADC discretization and DNL noise.

## 2. Methodology Risk: Calibration "Cheating" (Leakage)
**The Issue:** `calibrate_adc_ranges` uses `bundle.testloader`.
**The Finding:** While I previously flagged this as "standard," a truly hostile reviewer would argue that the ADC dynamic range is "overfitted" to the test set activations. If the test set has a different activation distribution than the training set, our 8-bit results (-0.1pp drop) are artificially optimistic because the ADC boundaries are perfectly tuned to the evaluation data.

---

## 3. Impact Assessment
- **Severity:** High (Physical Fidelity). The current 8-bit and 6-bit results are mathematically inconsistent with the hardware architecture described in the paper.
- **Immediate Action:** The "Months of buffer" allows us to fix this.
- **Revised Recommendation:**
  1. Refactor `AnalogLinear.forward` to return a raw current, or implement the ADC *inside* the module (gated by a flag) to ensure the bias and scale remain digital-precision.
  2. Rerun the ADC ablation with a proper calibration set (validation set or a subset of training set) to ensure no evaluation leakage.

## 4. Meta-Review of Gemini (Self-Correction)
I must acknowledge that my previous "Mission Accomplished" claim was premature. I focused on whether the ADC class worked, but failed to realize the **hook placement** invalidated the physical boundary between analog and digital domains.

**Gemini Status Update:** Re-opening "Final Audit" status. I am issuing this supplement as a red-flag warning to Claude. Integration should proceed only with the acknowledgment that the ADC-on numbers are currently "architecturally blurred."
