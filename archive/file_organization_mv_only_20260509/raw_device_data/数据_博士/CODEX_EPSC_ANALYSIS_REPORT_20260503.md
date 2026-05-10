# Codex EPSC Analysis Report — 2026-05-03

## Inputs

- Source directory: `compute_vit/数据_博士/`
- Valid EPSC CSV files analyzed: 64
- Excluded by brief: `1-4.csv` (non-EPSC IV-like format)
- Main channel: `CH1 Current 1`, converted from A to nA

## Outputs

- `EPSC_STATS_CODEX.csv`: per-file C1/C2/C3 feature table
- `EPSC_DEVICE_SUMMARY_CODEX.csv`: wafer-device aggregate statistics
- `EPSC_D9_REPEAT_SUMMARY_CODEX.csv`: D9 24-repeat trend summary
- `figures/epsc_device_consistency.(pdf|png)`
- `figures/epsc_d9_repeat_trend.(pdf|png)`
- `figures/epsc_representative_waveforms.(pdf|png)`
- `figures/epsc_feature_auxiliary_summary.(pdf|png)`

## Key Findings

1. Wafer-level device consistency is heterogeneous. The most stable wafer device by C1 inward peak amplitude is D9 with CV=1.3%; the least stable is D1 with CV=17.1%.
2. D9 24-repeat stability shows mean inward peak amplitude 28.07 ± 4.74 nA, CV=16.9%.
3. The D9 repeat linear trend slope is +0.189 nA per repeat with R²=0.080. This is a weak monotonic descriptor only; the visible run-to-run scatter is larger than the fitted drift trend.
4. C1 does not contain a resolved 1/e decay endpoint for these traces (0/64 resolved by threshold), so decay constants should not be reported from C1 alone.
5. C3 is useful as an auxiliary segment but not a universal endpoint: 50/64 files pass the ≥500-point criterion.

## Feature Definitions

- `C1_amp_nA_codex = baseline - peak`, positive for inward EPSC.
- `C1_rise_10_90_s`: first 10% to first 90% crossing before the C1 peak.
- `C1_tau_1e_decay_s`: time from peak until baseline-corrected signal falls below 1/e of peak amplitude; unresolved traces are left blank.
- `C1_charge_nC`: trapezoidal integral of positive baseline-corrected EPSC signal from 10% rise to post-peak 10% return. Since nA·s = nC, the unit is nC.

## Caveats

- Tau is not claimed as a robust result here because the C1 acquisition window generally ends before a 1/e recovery is reached.
- C3 truncation is preserved as a data-quality flag and is not treated as a parser error.
- The figures use positive inward amplitude for statistical comparisons, while waveform plots retain the physical negative-current convention.
