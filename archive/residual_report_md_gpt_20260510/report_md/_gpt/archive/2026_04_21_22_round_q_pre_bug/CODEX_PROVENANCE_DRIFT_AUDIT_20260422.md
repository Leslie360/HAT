# [✅ RESOLVED — Branch A] Codex Provenance Drift Audit (2026-04-22)
> **✅ RESOLVED (2026-04-22):** The no-multiplier implementation observed in the working tree is ratified as canonical under Branch A. The "drift" claim is therefore moot — the working tree was actually correct. However, the parity numbers referenced herein were run **before** the second-order sign fix (`ab56c2d`), so they remain invalid pending re-run on fully corrected code. The `corr_allcad_q` queue stoppage was appropriate given the unresolved semantics at the time.

---

*Original audit follows below for archival purposes:*

# Codex Provenance Drift Audit (2026-04-22)

## Conclusion
The current working tree does **not** match the already-broadcast claim that the local corrected parity anchor was produced after fixing a missing `nl` multiplier in the LTP first-order backward scale.

## Evidence
1. Current implementation in `analog_layers.py` uses:
   - `ltp_scale = ratio^(nl-1)`
   - `ltd_scale = ratio^(nl-1)`
   with no leading `nl` factor.
2. Current implementation in `analog_layers_ensemble.py` matches the same no-multiplier semantics.
3. Current regression tests explicitly assert the no-multiplier behavior (`0.75` and `-0.25` for the synthetic `nl=2` probes).
4. Existing broadcast/route-decision files still state that a missing `nl` multiplier bug was fixed and that the `46.75 / 57.00 / 55.65 / 83.34` parity numbers were obtained after that fix.

## Impact
- The current `corr_allcad_q` corrected cadence queue was running on a code state that is inconsistent with the published/broadcast interpretation.
- Therefore any new numbers from that queue must **not** be treated as authoritative corrected-mainline results.
- This does not by itself falsify the route choice (`group=all` still appears healthier than `group=mlp`), but it invalidates the current provenance chain for the newly relaunched corrected-mainline queue.

## Immediate action taken
- Stopped the active local tmux queue `corr_allcad_q`.
- Preserved logs, checkpoint artifacts, and the 1-epoch smoke output for forensic reference only.

## Required next step
A single semantics arbitration is needed before further GPU work:
1. either confirm that the no-multiplier implementation is the intended final surrogate semantics, then revert/update all broadcasted text;
2. or confirm that the multiplier fix is intended, then restore that implementation and rerun parity/cadence under the genuinely corrected code.
