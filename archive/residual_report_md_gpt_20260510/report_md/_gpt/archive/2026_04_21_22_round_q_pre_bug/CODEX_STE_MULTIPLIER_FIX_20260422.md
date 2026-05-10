# [❌ RESCINDED — Branch A] Codex Note — STE Multiplier Fix (2026-04-22)
> **⚠️ RESCINDED (2026-04-22):** The "missing `nl` multiplier fix" described herein was reverted at commit `ab56c2d`. The no-multiplier form (`torch.pow(ratio, nl-1)`) is ratified as the intentional, paper-aligned (Equation S2) semantics under Branch A. The second-order sign corrections (LTP/ LTD `+0.5` → `-0.5`) remain valid and are ratified. Do not follow the first-order multiplier recommendation in this file.

---

*Original note follows below for archival purposes:*

# Codex Note — STE Multiplier Fix (2026-04-22)

## What was confirmed
A new local source audit confirmed a real mathematical bug in `analog_layers.py`:

- `LTP` first-order backward scale omitted the `nl_ltp` multiplier
- `LTD` first-order backward scale already included the `nl_ltd` multiplier
- second-order correction terms already included the `nl*(nl-1)` factors

So the previous backward implementation was asymmetric and mis-scaled.

## Fix applied
Files updated:
- `analog_layers.py`
- `analog_layers_ensemble.py`

Change:
- `ltp_scale = nl_ltp * torch.pow(ltp_ratio, nl_ltp - 1.0)`
- same fix applied to the old ensemble snapshot for consistency

## Verification
Added regression coverage in:
- `test_groupwise_nl_wrapper.py`

New tests verify:
- `LTP` backward includes the `nl` multiplier
- `LTD` backward includes the `nl` multiplier
- existing wrapper semantics remain correct

Unit test status after the fix:
- `7/7 OK`

## Consequence
Any historical K-series interpretation that relied on the pre-fix backward must now be treated as provisional.

This does **not** automatically invalidate the main paper line, but it does invalidate any claim that the old higher-order ablations were already running on a mathematically correct second-order STE.

## Current runtime action
A new local minimal parity probe is running under the fixed code to re-anchor the mixed-NL behavior before any further K-series interpretation.
