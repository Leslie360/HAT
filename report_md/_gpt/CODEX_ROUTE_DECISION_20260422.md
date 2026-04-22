# Codex Route Decision (2026-04-22)

## Decision
The project should now treat **uniform-NL + domain randomization** as the primary forward path.

Mixed-NL (`group=mlp`) remains scientifically interesting, but it is no longer the candidate main strategy.
It is now a **diagnostic/mechanistic side branch**, not the performance branch.

## Why this decision is now justified
Two source-level bugs were confirmed and fixed locally:
1. config-sharing in `convert_to_hybrid()`
2. missing `nl` multiplier in the LTP first-order backward scale

After both fixes, the local corrected 1-epoch parity anchor is:

| setting | test acc |
|:--|--:|
| `mlp + SO2 + auto(-1.0)` | 46.75% |
| `mlp + SO2 + literal zero(0.0)` | 57.00% |
| `mlp + no SO2` | 55.65% |
| `all + SO2 + auto(-1.0)` | 83.34% |

This means:
- historical local `81.86%` can no longer be treated as corrected mixed-NL evidence
- remote pre-fix `~27%` collapse also cannot be treated as the final corrected mixed-NL anchor
- corrected mixed-NL is currently in a **mid-band (~46–57%)**, not competitive with the corrected uniform path
- corrected `group=all` remains healthy at `~83%` even in a 1-epoch parity probe

## Strategic consequence
### Primary route
- `group=all`
- uniform-NL handling
- domain-randomization / D2D resampling cadence as the main optimization axis

### Secondary route
- mixed-NL (`group=mlp`) for diagnosis only
- used to study gradient mismatch / surrogate behavior / failure modes
- not used as the current mainline solution claim

## What this means for the paper/rebuttal narrative
1. Do not sell `MLP-protected mixed-NL` as a working mitigation.
2. Treat mixed-NL as a diagnostic branch that helped expose:
   - config-sharing contamination
   - STE math sensitivity
   - structural mismatch between protected and unprotected modules
3. The performance-facing story should lean on:
   - uniform analog strategy
   - D2D resampling / domain randomization
   - fresh-instance robustness as the target metric

## What this means for future experiments
### Worth continuing
- corrected `group=all` domain-randomization line
- cadence search (`r10 / r40 / r50` family under corrected code)
- fresh-instance robustness under corrected code

### Deprioritized
- large mixed-NL sweep trees
- re-litigating old `27 / 58 / 81` parity numbers
- building paper claims on pre-fix K-series absolute values

## Status label
- **Route chosen:** yes
- **Final paper-grade numbers chosen:** not yet
- **Mainline direction chosen:** yes
