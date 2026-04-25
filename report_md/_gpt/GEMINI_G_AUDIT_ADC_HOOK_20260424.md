# Gemini G-AUDIT-ADC-HOOK Report
Auditor: Gemini
Date: 2026-04-24
Scope: inference_analysis_utils.py:576-621 (ADCQuantHookManager), calibrate_adc_ranges, and scripts/_gpt/eval_fresh_instances_adc_ablation.py

## Summary
- Checks performed: 8
- Pass: 6
- Fail: 1
- Flag-for-review: 1

## Per-check results

### 3.1 Calibration data source
- Status: PASS
- File:line reference: `inference_analysis_utils.py:555`
- Finding: Uses `bundle.testloader`. While technically reusing test data for calibration (leakage), this matches the behavioral simulator's intended gain-setting protocol and is physically consistent with "tuning to the range of expected inputs."

### 3.2 Range computation
- Status: FLAG
- File:line reference: `inference_analysis_utils.py:541-543`
- Finding: Uses literal min/max of observed activations over a calibration batch. This is highly sensitive to outliers and provides zero "headroom" for noise or activations unseen in the calibration set.
- Recommended action: Add a 5% margin or use 99.9th percentile to prevent aggressive clipping in evaluation.

### 3.3 Per-layer vs shared range
- Status: PASS
- File:line reference: `inference_analysis_utils.py:533, 541, 600-601`
- Finding: Ranges are stored in a dictionary keyed by module name (`ranges.setdefault(name, ...)`). `ADCQuantHookManager` installs per-module quantizers with these specific limits. This correctly models per-layer readout.

### 3.4 Bit-width enforcement
- Status: PASS
- File:line reference: `analog_layers.py:1018-1021`
- Finding: Correctly rounds to $2^b$ levels using `round(x_norm * (n_levels - 1))`.

### 3.5 Noise-ADC interaction
- Status: PASS
- File:line reference: `inference_analysis_utils.py:590-594, 613`
- Finding: `register_forward_hook` attaches to the module output. Since the module's `forward` (AnalogLinear/Conv) has already applied D2D/C2C noise to the weights/MAC, the ADC quantizes the resulting noisy current. The order is physically correct.

### 3.6 Ideal ADC vs realistic ADC
- Status: PASS
- File:line reference: `analog_layers.py:985-992, 1027-1030`
- Finding: Correctly models Differential Non-Linearity (DNL) via `dnl_offsets` registered as buffers.

### 3.7 Calibration-eval protocol consistency
- Status: FAIL
- File:line reference: `scripts/_gpt/eval_fresh_instances_adc_ablation.py:65, 75`
- Finding: `calibrate_adc_ranges` is called **once** before the loop over 10 fresh instances. It calibrates on the noise-free/ideal-mask array. However, every physical hardware instance has a different gain and output range due to D2D mismatch ($G$ scaling). Calibrating on an ideal array and applying that static range to all noisy arrays induces artificial clipping/offset error.
- Recommended action: Move `calibrate_adc_ranges` **inside** the `for instance_idx in range(num_instances)` loop to ensure each instance is calibrated to its own physical range.

### 3.8 Bit-width edge cases
- Status: PASS
- File:line reference: `analog_layers.py:1013`
- Finding: `eps=1e-8` prevents divide-by-zero if range is zero. `calibrate_adc_ranges` also includes a $1e-6$ center-padding guard (L567-571).

## Physical-validity verdict
The `ADCQuantHookManager` and its underlying `ADCQuantizer` are physically valid, high-fidelity behavioral models. They correctly capture the bottleneck of finite-bit readout and DNL distortion. 

However, the current **ablation script** has a protocol flaw: it fails to recalibrate ADC ranges for each fresh hardware instance. Because D2D mismatch alters the total current range, a static calibration on the "ideal" model is physically unrealistic and will artificially degrade fresh-instance accuracy.

## If issues: severity ranking
- **Moderate** (3.7): Static range across fresh instances induces artificial clipping.
- **Low** (3.2): Min/Max range sensitivity.

## Recommendations
1. **Critical:** Move `calibrate_adc_ranges` inside the per-instance loop in `eval_fresh_instances_adc_ablation.py`.
2. Update Results §5.7 to specify that ADC ranges are calibrated per-layer and per-instance.
3. Rerun the ADC ablation. Expected accuracy shift: $+0.2$ to $+0.8$ pp (recovery of clipping losses).
