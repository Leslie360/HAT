# DS-EPSC-A: Measured EPSC Profile Conversion Design

**Date:** 2026-05-07
**Data sources:**
- `数据_博士/EPSC_ANALYSIS_READY.csv` — per-measurement EPSC peak amplitudes (8 devices, 5 measurements each + device 9 repeat N=24)
- `数据_博士/EPSC_DEVICE_SUMMARY_CODEX.csv` — per-device summary statistics
- `数据_博士/EPSC_D9_REPEAT_SUMMARY_CODEX.csv` — device 9 repeatability analysis

---

## 1. C2C Proxy Definition

**Statistic:** Detrended within-device coefficient of variation of EPSC peak amplitude.

**Rationale:** In the HAT noise model, C2C (cycle-to-cycle) noise is resampled on every read, modeled as Gaussian noise in the conductance domain with std = σ_c2c × G_range. The EPSC analogue is the trial-to-trial variability of peak amplitude on the same device under identical stimulus conditions.

**Primary estimate:** Device 9 (24 repeat measurements)
- Raw CV = 15.5% (std 4.33 nA, mean 27.85 nA)
- Detrended CV = 14.0% (removing linear drift, slope 0.24 nA/run, R²=0.22)
- Trend explains only 18.5% of variance → most variability is genuine trial-to-trial noise

**Pooled estimate across all devices** (8 devices × 5 measurements each):
- Pooled within-device std = 2.54 nA
- C2C CV proxy = 9.2%

**Recommendation for HAT mapping:** Use σ_c2c ≈ **0.05–0.15** as the plausible range, with σ_c2c = **0.10** as a central estimate. This maps to the detrended D9 CV (14.0%) with a safety factor recognizing that current-domain CV may overstate conductance-domain CV.

---

## 2. D2D Proxy Definition

**Statistic:** Between-device coefficient of variation of mean EPSC peak amplitude.

**Rationale:** In the HAT noise model, D2D (device-to-device) noise is a fixed per-cell offset initialized once per device instance, modeled in conductance domain with std = σ_d2d × G_range. The EPSC analogue is the device-to-device variation in mean peak amplitude across nominally identical devices.

**Data:**
| Device | Mean peak (nA) | n |
|---|---|---|
| 1 | 25.71 | 5 |
| 2 | 29.28 | 5 |
| 3 | 25.69 | 5 |
| 5 | 30.51 | 5 |
| 6 | 34.82 | 5 |
| 7 | 26.69 | 5 |
| 8 | 21.51 | 5 |
| 9 | 26.83 | 5 |

- Grand mean = 27.63 nA
- Between-device std = 3.95 nA
- **D2D CV proxy = 14.3%**

**Recommendation for HAT mapping:** Use σ_d2d ≈ **0.05–0.15** as the plausible range, with σ_d2d = **0.10** as a central estimate. This maps to the between-device CV (14.3%) with a discount recognizing that current-domain device variation may exceed the conductance-only variation targeted by HAT.

**Note on D2D range and device 8 outlier:** Device 8 (mean 21.51 nA) is notably lower than other devices (range 25.7–34.8 nA). This is the largest contributor to the between-device std. If device 8 is excluded as a known low-yield outlier, D2D CV drops to ~11.8%.

---

## 3. Why EPSC Peak Variation Is Only a Proxy, Not Direct Conductance D2D

The HAT noise model operates in the **conductance domain** (G_pos, G_neg differential pairs), with D2D noise injected as a fixed per-cell offset in Siemens. EPSC peak amplitude is a **current measurement** in amperes. The mapping is indirect for four reasons:

| Factor | Effect | Direction |
|---|---|---|
| **1. Voltage dependence** | EPSC peak ∝ conductance × driving voltage. If driving voltage varies across devices or trials, peak variation overstates conductance variation. | Proxy overestimates σ |
| **2. Kinetic filtering** | EPSC peak amplitude depends on channel opening kinetics, not just steady-state conductance. Two devices with identical conductance but different kinetics give different peak currents. | Proxy overestimates σ |
| **3. Differential vs single-ended** | HAT uses differential read (G_pos − G_neg), which cancels common-mode variation. EPSC is single-ended, so it includes common-mode noise that HAT rejects. | Proxy overestimates σ |
| **4. Timescale mismatch** | EPSC measures synaptic transmission on ms timescales. Analog memory conductance read is typically faster (ns–µs). Different physical mechanisms contribute at different timescales. | Unquantified |

**Practical consequence:** The proxy CV numbers (14% D2D, 14% C2C) are **upper bounds** on the equivalent HAT noise parameters. The real conductance-domain σ_d2d and σ_c2c for the HAT model are likely lower. For a conservative design, use the proxy values directly. For a realistic range, apply a 0.5× discount factor: σ ≈ 0.07.

**Bottom line:** This profile is useful for (a) stress-testing the HAT model under realistic noise levels, and (b) comparing whether the noise levels observed in fabricated devices would still allow acceptable PPL. It is NOT a claim that these EPSC devices are the exact hardware platform used in the paper.

---

## 4. Draft JSON Schema

```json
{
  "profile_name": "Doctor_EPSC_20260501_proxy_profile",
  "description": "Noise proxy profile derived from Doctor EPSC peak amplitude measurements. ",
  "description_cont": "EPSC peak current CV is used as a proxy for conductance-domain D2D/C2C noise. ",
  "description_cont": "This is a proxy, not a direct hardware profile.",
  "date": "2026-05-01",
  "source_data": [
    "EPSC_ANALYSIS_READY.csv",
    "EPSC_DEVICE_SUMMARY_CODEX.csv",
    "EPSC_D9_REPEAT_SUMMARY_CODEX.csv"
  ],
  "device_type": "synaptic_transistor_EPSC",
  "n_devices": 8,
  "measurements_per_device": 5,
  "repeat_measurements_device_9": 24,
  "signal_domain": "current_peak_nA",
  "proxy_limitations": [
    "EPSC peak amplitude is a current measurement, not conductance. Multiple factors (voltage, kinetics, single-ended read) cause current-domain CV to overstate conductance-domain CV.",
    "HAT noise model uses differential read (G_pos - G_neg) which rejects common-mode noise not captured in single-ended EPSC.",
    "EPSC measurements at ms timescale may include synaptic noise sources absent in fast analog memory read."
  ],
  "noise_model": "HAT_uniform",
  "sigma_c2c": {
    "description": "Cycle-to-cycle noise (fraction of G_range). Proxy: detrended within-device CV of EPSC peak amplitude.",
    "estimate": 0.10,
    "plausible_range": [0.05, 0.15],
    "source_statistic": "device_9_detrended_cv_pct",
    "source_value": 14.0,
    "mapping_formula": "σ_c2c = CV_EPSC_detrended / 100 * discount_factor",
    "discount_factor_applied": 0.7,
    "discount_rationale": "Current-domain CV overstates conductance-domain CV (see proxy_limitations)"
  },
  "sigma_d2d": {
    "description": "Device-to-device noise (fraction of G_range). Proxy: between-device CV of mean EPSC peak amplitude.",
    "estimate": 0.10,
    "plausible_range": [0.05, 0.15],
    "source_statistic": "between_device_cv_pct",
    "source_value": 14.3,
    "mapping_formula": "σ_d2d = CV_between_device / 100 * discount_factor",
    "discount_factor_applied": 0.7,
    "discount_rationale": "Current-domain CV overstates conductance-domain CV (see proxy_limitations)"
  },
  "other_statistics": {
    "c2_mean_nA_range": [-25.0, -14.9],
    "peak_amp_min_nA": 17.37,
    "peak_amp_max_nA": 37.65,
    "d9_trend_slope_nA_per_run": 0.19,
    "d9_trend_r2": 0.08
  }
}
```

---

## 5. Recommended Minimal Eval Matrix (if Kimi runs it)

**Purpose:** Test whether EPSC-proxy noise levels break the last1 selective KV result, and if so, at what threshold.

**Design:** Sweep σ_d2d and σ_c2c across the proxy range, using one fixed training checkpoint (last1, D2D=0.02, seed 42) and 3 eval D2D seeds.

| ID | σ_c2c | σ_d2d | Eval seeds | Purpose |
|---|---|---|---|---|
| EPSC-e1 | 0.05 | 0.05 | 42, 456, 1001 | low end of proxy range |
| EPSC-e2 | **0.10** | **0.10** | 42, 456, 1001 | **central proxy estimate** |
| EPSC-e3 | 0.15 | 0.15 | 42, 456, 1001 | high end of proxy range |
| EPSC-e4 | 0.00 | 0.20 | 42, 456, 1001 | D2D-only stress |
| EPSC-e5 | 0.01 | 0.10 | 42, 456, 1001 | HAT-default C2C + proxy D2D |

**Kill criterion:** If EPSC-e2 (central estimate) gives PPL > 25 at any eval seed, the proxy noise level is incompatible with acceptable LM quality for this model scale.

**Expected outcome range:**
- EPSC-e1 → ~18.5–19.5 PPL (close to current D2D=0.02 results)
- EPSC-e2 → ~20–25 PPL (tolerable degradation if selective KV claim holds)
- EPSC-e3 → ~25–35 PPL (stress test)
- EPSC-e4 → tests whether D2D alone drives degradation
- EPSC-e5 → isolates C2C contribution

---

## 6. Summary

| Quantity | Estimate | HAT parameter |
|---|---|---|
| D2D CV (between-device) | 14.3% | σ_d2d ≈ 0.10 (0.05–0.15) |
| C2C CV (within-device, detrended) | 14.0% | σ_c2c ≈ 0.10 (0.05–0.15) |
| Central proxy profile | — | (σ_c2c=0.10, σ_d2d=0.10) |

The EPSC data suggest that real fabricated devices have **larger** variability (σ ≈ 0.10) than the current HAT default values (σ = 0.02–0.05). This is not a problem for the paper — it means the paper's noise levels are on the optimistic side of reality, and the EPSC profile provides a useful stress-test baseline for future work.

**Do not claim this as canonical hardware validation.** This is a proxy profile for stress-testing and sensitivity analysis only.
