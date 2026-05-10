# Position Memo: Why the First-Order NL Surrogate May Be Insufficient

**Date:** 2026-04-21
**Re:** Ceiling analysis bottleneck — first-order surrogate limitations

---

## 1. Physical Realism Gap

Real organic RRAM write dynamics involve filament formation, charge trapping, electrochemical reactions, and gradual set/reset transitions. A simple power-law mapping g → g^NL, while computationally convenient, is a gross simplification. It collapses these heterogeneous physical mechanisms into a single scalar nonlinearity parameter. By doing so, it ignores the rich temporal and voltage-dependent physics that govern actual conductance evolution. A training procedure that only sees g^NL learns to compensate for a caricature of the device, not the device itself.

## 2. Hysteresis

First-order surrogates typically ignore write-history dependence: the next conductance is treated as a deterministic function of the current state and pulse polarity. Real organic devices exhibit hysteresis loops — the conductance trajectory depends on prior cycling, cumulative pulse count, and even relaxation times between writes. If the surrogate erases this history dependence, training cannot learn adaptive strategies that exploit or mitigate hysteretic behavior. We may be discarding degrees of freedom that real hardware could use to improve accuracy.

## 3. Spatial Non-Uniformity

The first-order model applies a uniform NL across the entire array. In fabricated crossbars, device-to-device variation is substantial: different cells can have different switching voltages, endurance, and nonlinearities due to film thickness fluctuations, electrode roughness, and dopant distribution. A uniform surrogate forces the optimizer to find a single compromise update rule, when the array could in principle support cell-specific or region-specific strategies. This averaging effect artificially raises the apparent error floor.

## 4. Why This Matters for the Ceiling

If the true write dynamics are more complex than g^NL, then training on the first-order surrogate learns a mismatched task. The ~30% accuracy ceiling we observe may be an artifact of surrogate mismatch, not a true hardware limit. In other words, the optimizer has converged to the best policy for the *wrong* environment. Without validation on a higher-fidelity model, we cannot distinguish between "the hardware cannot do better" and "our model of the hardware is too coarse to reveal how to do better." The ceiling risks becoming a self-fulfilling prophecy.

## 5. Counter-Argument

That said, the first-order surrogate may still be sufficient for practical purposes. It is simple, tractable, and captures the dominant failure mode: symmetric, gradual conductance saturation that erases gradient information. If higher-order effects (hysteresis, spatial variation, filament dynamics) are secondary perturbations rather than primary error sources, then a more complex surrogate would add noise without improving the ceiling. The burden of proof lies with whoever argues for additional complexity: they must show that a richer model materially changes the optimal policy or the predicted accuracy. Until then, simplicity is a virtue — but it is also a potential blind spot.

---

*Bottom line: treat the ~30% ceiling as an upper bound contingent on surrogate fidelity, not a definitive hardware limit.*
