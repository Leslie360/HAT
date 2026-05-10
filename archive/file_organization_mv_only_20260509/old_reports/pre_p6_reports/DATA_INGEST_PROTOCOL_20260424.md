# DATA_INGEST_PROTOCOL — Real D2D/C2C Hardware Calibration
**Date:** 2026-04-24
**Author:** Claude
**Status:** ACTIVE — consume-ready pipeline for PhD team's measured device data
**Gate:** Data may land for internal use pre-graduation; paper submission blocks on PhD defense clearance.

---

## 1. Purpose

When PhD team delivers measured D2D/C2C data from the fabricated organic optoelectronic array, we must be able to swap **literature-prior distributions → measured distributions** in the simulator with minimum friction. This document is the interface spec so that the moment data arrives we don't scramble.

**Paper-level implication**: simulator status upgrades from "literature-calibrated" to "hardware-calibrated against measured device statistics". This lifts the venue ceiling to Nature Electronics.

---

## 2. Expected data format (from PhD team)

**Ask the PhD team for ONE of the following, in priority order:**

### Preferred: raw conductance matrices
- `conductance_matrix.npy` (or CSV): shape `(N_devices_per_array, N_arrays)` — actual measured conductance values in Siemens.
- Measurement conditions: read voltage, temperature, time since last program, number of read cycles per point.
- Metadata file `measurement_metadata.json`:
  - `array_size`: e.g. 128×128 or actual device layout
  - `programming_levels`: which target conductance levels were programmed (4-bit = 16 levels ideal)
  - `devices_per_level`: histogram support
  - `read_voltage_V`, `temperature_C`, `measurement_date`
  - `known_failures`: indices of stuck / open devices

### Acceptable: pre-computed D2D / C2C statistics
- `d2d_stats.json`: per-programmed-level mean + std + quantiles (Q05, Q25, Q50, Q75, Q95)
- `c2c_stats.json`: per-device repeated-read std across N reads
- Still ask for: raw scatter plot image even if no raw data — lets us digitize at low resolution if needed

### Minimum viable: literature-style summary
- Single scalar: σ_D2D_measured = X%, σ_C2C_measured = Y% with method note
- Less valuable — cannot do QQ plot — but still lets us replace our 10%/5% literature priors with actual numbers.

---

## 3. Ingest pipeline (scripts to pre-build)

These do not need data yet; we build them now so the moment data arrives it's a one-command pipeline.

### 3.1 `scripts/ingest_measured_conductance.py` (to be written by Codex)

**Input**: `conductance_matrix.npy` + `measurement_metadata.json`
**Output**:
- `data/measured_d2d_distribution.npy`: flattened per-level (conductance - level_mean) / level_mean values (unitless fractional mismatch)
- `data/measured_c2c_distribution.npy`: per-device read-to-read fractional std
- `data/measured_stats_summary.json`: fitted Gaussian params + Anderson-Darling test for Gaussianity + heavy-tail diagnostics (kurtosis, KS distance to Gaussian)
- `figures/qq_measured_vs_literature.pdf`: QQ plot of measured fractional D2D vs our literature-prior Gaussian(0, 0.1²)

### 3.2 `analog_layers.py` distribution-injection hook

Add one line enabling ensemble training to sample from measured distribution instead of Gaussian prior:
```python
if config.get("d2d_distribution_source") == "measured":
    d2d_samples = torch.from_numpy(np.load("data/measured_d2d_distribution.npy"))
    # bootstrap-sample with replacement to fill the mask shape
```

Codex should add this flag to `--d2d-distribution` CLI arg. Keep literature-prior as default for bug-immune canonical reproducibility.

### 3.3 `scripts/calibrate_iso_accuracy_map.py`

Re-runs the 63-point iso-accuracy sweep but swapping Gaussian prior for measured distribution at each σ level (via scaling the empirical distribution). Outputs fig_contour_map_measured.pdf.

---

## 4. Downstream re-runs once data lands

In order. Budget: ~1-2 weeks on local GPU (no A100 needed).

| Job | Runtime | Purpose |
|:--|:--|:--|
| R-D0 | 10 min | QQ plot + Gaussian-fit diagnostics. Report back to user + PhD team. If measured is ~Gaussian, our literature-prior results are calibrated. If heavy-tailed, we have a story. |
| R-D1 | ~6-8 GPU-h | Re-run Ensemble HAT canonical at measured D2D distribution, 10 fresh instances × 5 MC runs. Expected: within 2σ of 86.37±1.54%, or we learn something. |
| R-D2 | ~12-20 GPU-h | Re-run 63-point iso-accuracy map. Same grid, measured distribution. Expected: same 6-bit cliff, possibly different D2D transition points. |
| R-D3 | ~20-30 GPU-h | Scenario 3 (post-fix severe-NL) Ensemble HAT at measured D2D, 3 seeds. Fills the [PENDING] cell from NARRATIVE_PIVOT §2. |
| R-D4 | ~5 GPU-h | If measured is heavy-tailed: AR(1) spatial correlation analysis extended to measured spatial map (if PhD provides pixel layout). Currently in Supp Note S2 under i.i.d. assumption. |

**Gate to trigger these**: data ingested, R-D0 QQ plot reviewed by Claude. R-D1 only fires after QQ sanity.

---

## 5. Paper-level placeholders to leave in drafts

Kimi draft should include these **exact tags** so integration-phase sed-replace is mechanical:

- `[LITERATURE_CALIBRATED_D2D: σ=10%, Gaussian prior from ReRAM literature \citep{fastirdrop2025,iconniv2026}]` — currently used in sentences referring to D2D magnitude.
- `[LITERATURE_CALIBRATED_C2C: σ=5%, Gaussian prior]` — same.
- `[MEASURED_D2D_DISTRIBUTION: pending from coauthor data]` — placeholder in QQ-plot figure caption + Supp Note.
- `[MEASURED_SIGMA_D2D_VALUE]` and `[MEASURED_SIGMA_C2C_VALUE]` — scalar placeholders for tables.
- `[HARDWARE_CALIBRATION_SUPP_NOTE_REFERENCE]` — in Methods where we'd point to Supp Note S-HW.

Post-data-land, find-and-replace pass updates every draft in one commit.

---

## 6. Supplementary Note template: "S-HW Hardware-Calibrated Device Statistics"

Reserve a placeholder Supp Note with this structure. Kimi writes the prose now against the template, leaves numeric cells empty.

```
S-HW.1 Measurement setup
  - Array geometry, device process, measurement conditions (from PhD)
  - N devices measured across N arrays

S-HW.2 D2D distribution
  - Histogram of fractional mismatch per programmed level
  - Fitted Gaussian σ_D2D = [MEASURED_SIGMA_D2D_VALUE]
  - Anderson-Darling p = [...], KS distance to Gaussian = [...]
  - Heavy-tail diagnostics: kurtosis = [...]
  - QQ plot vs literature prior Gaussian(0, 0.1²)
  - Conclusion sentence: measured is [Gaussian / moderately heavy-tailed / heavy-tailed]

S-HW.3 C2C distribution
  - Analogous structure

S-HW.4 Impact on deployment predictions
  - Compare Ensemble HAT fresh-instance accuracy:
    - Literature-prior (86.37±1.54%)
    - Measured-D2D (R-D1 result)
  - Compare iso-accuracy contour map: does 6-bit cliff location shift?
  - Statement about whether literature prior over/under-estimates deployment risk

S-HW.5 Spatial structure
  - Autocorrelation map if raw matrix provided
  - AR(1) fit
  - Comparison to Supp Note S2 (literature AR(1) sensitivity study)
```

---

## 7. What Claude watches for during the waiting period

- Monthly: ping user about PhD team data status (not urgent, just keep it on radar)
- Monitor AGENT_SYNC for any Kimi/Codex/Gemini output that accidentally uses literature-prior numbers as if measured — catch these at PR-review time
- When data arrives: notify user immediately, run R-D0 within 24 hours, report back

---

## 8. Communication to PhD team (template user can send)

```
[Subject] Data format request for hardware-calibration supplementary

Hi [PhD name],

For the organic CIM paper we're drafting, we want to calibrate our simulator
against your measured device statistics. When you have the data ready to
share internally, could you deliver:

(1) Raw per-device conductance matrices (npy/csv), with programmed-level
    labels. Shape (N_devices, N_arrays) or equivalent.
(2) A small metadata JSON with: array geometry, read voltage, temperature,
    programmed levels, measurement date, any known failures/outliers.
(3) If raw is not feasible, per-level mean+std summary is a workable fallback.

We'll process this into QQ plots + fitted distributions + downstream
sensitivity re-runs. All derived results credit your measurements and stay
internal until your defense clearance.

Time budget on our side once data arrives: ~1-2 weeks for the full
re-calibration pass. No rush.

Thanks —
[User]
```
