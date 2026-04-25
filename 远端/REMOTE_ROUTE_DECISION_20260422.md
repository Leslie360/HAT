# Remote Route Decision (2026-04-22)

## Short version
We have now chosen the main direction.

The mainline path is:
- **uniform-NL (`group=all`)**
- plus **domain randomization / D2D resampling cadence**

Mixed-NL (`group=mlp`) is no longer the main solution candidate.
It remains useful only as a diagnostic branch.

## Why
After fixing both:
1. config-sharing in `convert_to_hybrid()`
2. the missing `nl` multiplier in the local STE backward

our corrected local 1-epoch parity anchor is:

| setting | test acc |
|:--|--:|
| `mlp + SO2 + auto(-1.0)` | 46.75% |
| `mlp + SO2 + literal zero(0.0)` | 57.00% |
| `mlp + no SO2` | 55.65% |
| `all + SO2 + auto(-1.0)` | 83.34% |

Interpretation:
- old local `81.86%` is no longer a valid corrected mixed-NL anchor
- old remote `~27%` is also not the final corrected mixed-NL anchor
- corrected mixed-NL is currently a mid-band result, not a strong path
- corrected `group=all` remains clearly healthy

## Operational rule for remote
From now on, do **not** spend major GPU time trying to rescue `group=mlp` as the main route.

Use remote primarily to accelerate the corrected **uniform-NL + domain-randomization** branch.

Mixed-NL can still be used for small diagnostic probes, but not as the center of the queue.
