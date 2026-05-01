# DS-3: Supplementary Hostile Claim Audit

Date: 2026-05-01
Scope: `supplementary.tex`, `S_theory_ensemble_hat.tex`, `S_mechanism_empirical.tex`, `S_hardware_calibration.tex`

## Summary

| Severity | Count | Patched |
|:---------|:------|:--------|
| BLOCKER | 0 | — |
| MAJOR | 2 | 2 |
| MINOR | 3 | 0 |
| OK (flagged but acceptable) | 5 | — |

---

## MAJOR

### M1. `supplementary.tex:586` — "critical layout constraint"

- **Original**: "The results indicate that differential-pair symmetry is a **critical** layout constraint"
- **Why risky**: "Critical" overstates what a first-order simulation with behavioral models can establish. The simulation shows rapid degradation but doesn't prove fabrication infeasibility.
- **Recommended**: "important layout constraint"
- **Patch applied**: ✅

### M2. `supplementary.tex:684` — "establishes ... decisive advantage"

- **Original**: "This **establishes** the 4-bit regime as the operating point where distribution-matching training provides a **decisive** advantage over per-batch noise alone."
- **Why risky**: "Establishes" and "decisive" are both overstrong. The comparison is between AIHWKit per-batch noise and Ensemble HAT on one architecture/dataset. "Decisive" implies a settled conclusion across regimes.
- **Recommended**: Replace "establishes" → "identifies", "decisive advantage" → "clear advantage"
- **Patch applied**: ✅

---

## MINOR

### m1. `supplementary.tex:638` — "demonstrate ... maintains reasonable accuracy"

- Original: "The results **demonstrate** that the hybrid-analog architecture **maintains reasonable accuracy**"
- Verdict: Acceptable because qualified by "tested lower-bound probe range" and "first-order behavioral models." Not overclaimed.
- **Action**: None needed.

### m2. `supplementary.tex:248` — "confirming that peripheral precision is gate-keeping"

- Original: "confirming that peripheral precision is gate-keeping only once errors exceed the moderate range"
- Verdict: Acceptable — directly supported by the ADC sweep data in the same table.
- **Action**: None needed.

### m3. `S_mechanism_empirical.tex:34` — "primary empirical evidence"

- Original: "This is the **primary** empirical evidence that per-epoch resampling yields D2D-directional robustness."
- Verdict: Factually accurate (it IS the main evidence for this claim). The surrounding text reports actual numbers.
- **Action**: None needed.

### m4. `S_mechanism_empirical.tex:64` — "also critical"

- Original: "the patch-embedding convolution ... is also **critical**"
- Verdict: Acceptable — qualified by "under the earlier source-domain diagnostic" and immediately caveated. Used descriptively for sensitivity ranking.
- **Action**: None needed.

### m5. `supplementary.tex:507` — "optimal compensation exponent"

- Original: "the **optimal** compensation exponent is milder than the physical inverse"
- Verdict: Acceptable — this is a mathematical optimum from a defined MSE objective, not a universal claim. The surrounding text clearly states the optimization criterion ("pixel-level mean-squared error rather than task-level classification loss").
- **Action**: None needed.

---

## OK (flagged keywords with acceptable usage)

| File | Line | Word | Why OK |
|:-----|:-----|:-----|:-------|
| `S_theory_ensemble_hat.tex` | 21 | optimal | Used in negated form ("no guarantee that the minimizer remains optimal") |
| `S_theory_ensemble_hat.tex` | 37 | dominant | "D2D-dominant approximation" — technical term, clearly caveated |
| `S_theory_ensemble_hat.tex` | 172 | dominant | "the dominant term is the squared-bias term" — mathematical dominance |
| `supplementary.tex` | 714 | demonstrates | Inside risk-assessment table, directly supported by sweep data |
| `supplementary.tex` | 758 | dominant | "dominant recoverable failure site **under the earlier $NL=2.0$ surrogate**" — heavily caveated |

---

## Patches Applied

### Patch 1: `supplementary.tex:586`

```
- differential-pair symmetry is a critical layout constraint
+ differential-pair symmetry is an important layout constraint
```

### Patch 2: `supplementary.tex:684`

```
- This establishes the 4-bit regime as the operating point where
  distribution-matching training provides a decisive advantage over
  per-batch noise alone.
+ This identifies the 4-bit regime as the operating point where
  distribution-matching training provides a clear advantage over
  per-batch noise alone.
```

---

## Files Checked

- `paper/latex_gpt/supplementary.tex` — 917 lines
- `paper/latex_gpt/supplementary/S_theory_ensemble_hat.tex` — 244 lines
- `paper/latex_gpt/supplementary/S_mechanism_empirical.tex` — 119 lines

S_hardware_calibration.tex skipped — contains protocol descriptions, not claims.

## Verdict

The SI text is generally well-qualified. Two overstrong words found and softened. No BLOCKER issues. The self-caveating style (especially in S_theory_ensemble_hat and the NL ablation tables) is commendable and should be preserved.
