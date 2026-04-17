# Physics Stack

The simulator is intentionally a first-order behavioral framework rather than a
pulse-accurate or chip-predictive emulator.

## Canonical Physics

The default paper results use:

- differential-pair conductance mapping
- discrete conductance states (`n_states`)
- uniform window-referenced D2D and C2C Gaussian noise
- double-exponential retention
- digital scale recovery

## Extended Physics

The codebase also supports:

- proportional state-dependent noise
- nonlinear-write STE surrogates (`NL_LTP`, `NL_LTD`)
- conductance INL lookup tables
- partial support for state-dependent retention
- optoelectronic frontend terms (`gamma_phys`, `I_dark`, responsivity)

## Important Boundaries

The current framework does **not** claim to model:

- IR drop across large arrays
- sneak-path currents
- full optical non-uniformity and optical write crosstalk
- temperature-dependent drift
- pulse-by-pulse programming dynamics
- full ADC timing/area co-design

## Interpretation Guidance

- canonical retention plots use the uniform decay model
- literature-derived profiles validate the interface, not full measured-device closure
- proportional-noise HAT demonstrates matched-regime recovery, not broad cross-regime robustness
- nonlinear-write failure should be read as a real boundary for the current approximation
