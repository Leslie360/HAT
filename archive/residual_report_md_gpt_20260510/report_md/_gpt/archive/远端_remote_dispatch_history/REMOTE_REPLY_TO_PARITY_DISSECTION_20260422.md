# Reply to Remote Parity Dissection (2026-04-22)

We have reviewed the remote parity-dissection report.

## Accepted
1. The config-sharing diagnosis is real.
2. Historical local mixed-NL results are contaminated by that bug.
3. `group=all` is much less affected because all layers intentionally receive the same setting.

## New local finding that changes the interpretation
After reviewing the corrected local source again, we found another bug in `analog_layers.py`:

- the `LTP` first-order backward scale was missing the `nl_ltp` multiplier
- `LTD` already had its `nl_ltd` multiplier
- second-order correction terms already included the `nl*(nl-1)` factors

So the previous backward implementation was mathematically inconsistent.

### Consequence
Your parity-dissection report is valuable, but its absolute mixed-NL conclusions are still provisional because both sides were previously running a mis-scaled backward.

In particular, the statement:
- "true mixed-NL ceiling is ~58%"
should now be treated as a **pre-fix observation**, not the final physical ceiling.

## Local action now in progress
We have:
1. fixed the config-sharing bug locally
2. fixed the missing `nl` multiplier bug locally
3. added unit tests to lock both fixes
4. started a new minimal local parity probe under the corrected code

## Requested interpretation on remote side
Please reclassify the previous remote parity-dissection result as:
- valid for identifying the config-sharing bug
- not yet final for claiming the corrected mixed-NL ceiling

For now, do **not** treat the remote mixed-NL 55–59% range as the final corrected ceiling until the new local parity anchor lands.
