# Codex STE Semantics Evidence Pack (2026-04-22)

## Purpose
This memo records the exact mismatch that triggered the current arbitration freeze.

## E1. Current code semantics
### `analog_layers.py`
- Current first-order LTP scale:
  - [analog_layers.py:235](/home/qiaosir/projects/compute_vit/analog_layers.py#L235)
  - [analog_layers.py:237](/home/qiaosir/projects/compute_vit/analog_layers.py#L237)
- Current first-order LTD scale:
  - [analog_layers.py:241](/home/qiaosir/projects/compute_vit/analog_layers.py#L241)
  - [analog_layers.py:243](/home/qiaosir/projects/compute_vit/analog_layers.py#L243)
- Current code computes:
  - `ltp_scale = ratio^(nl_ltp-1)`
  - `ltd_scale = ratio^(nl_ltd-1)`
- There is **no leading `nl_*` multiplier** in the first-order branch.

### `analog_layers_ensemble.py`
- Current first-order LTP/LTD implementation:
  - [analog_layers_ensemble.py:123](/home/qiaosir/projects/compute_vit/analog_layers_ensemble.py#L123)
  - [analog_layers_ensemble.py:125](/home/qiaosir/projects/compute_vit/analog_layers_ensemble.py#L125)
  - [analog_layers_ensemble.py:129](/home/qiaosir/projects/compute_vit/analog_layers_ensemble.py#L129)
  - [analog_layers_ensemble.py:131](/home/qiaosir/projects/compute_vit/analog_layers_ensemble.py#L131)
- Same semantics: **no leading `nl_*` multiplier**.

## E2. Current tests assert the same no-multiplier semantics
- LTP test:
  - [test_groupwise_nl_wrapper.py:104](/home/qiaosir/projects/compute_vit/test_groupwise_nl_wrapper.py#L104)
  - expected gradient: `0.75`
- LTD test:
  - [test_groupwise_nl_wrapper.py:112](/home/qiaosir/projects/compute_vit/test_groupwise_nl_wrapper.py#L112)
  - expected gradient: `-0.25`
- Test comment explicitly says:
  - "no NL multiplier per paper"

## E3. Broadcasted interpretation currently says the opposite
### Local route memo
- [CODEX_ROUTE_DECISION_20260422.md:10](/home/qiaosir/projects/compute_vit/report_md/_gpt/CODEX_ROUTE_DECISION_20260422.md#L10)
- States that two source-level bugs were fixed locally, including:
  - "missing `nl` multiplier in the LTP first-order backward scale"

### Remote handoff packet
- [REMOTE_HANDOFF_PACKET_20260422.md:14](/home/qiaosir/projects/compute_vit/远端/REMOTE_HANDOFF_PACKET_20260422.md#L14)
- Repeats the same claim.

### Sync ledger
- [AGENT_SYNC_gpt.md:24243](/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md#L24243)
- Records the multiplier fix as completed fact.

## E4. The currently cited corrected parity numbers depend on that disputed claim
These files present the `46.75 / 57.00 / 55.65 / 83.34` anchor as corrected-post-fix output:
- [CODEX_CX_PARITY_MINIMAL_20260422.md:8](/home/qiaosir/projects/compute_vit/report_md/_gpt/CODEX_CX_PARITY_MINIMAL_20260422.md#L8)
- [REMOTE_LOCAL_PARITY_REANCHOR_20260422.md:19](/home/qiaosir/projects/compute_vit/远端/REMOTE_LOCAL_PARITY_REANCHOR_20260422.md#L19)
- [REMOTE_ROUTE_DECISION_20260422.md:18](/home/qiaosir/projects/compute_vit/远端/REMOTE_ROUTE_DECISION_20260422.md#L18)

## E5. New GPU work was started under the disputed interpretation
- Local corrected all-linear queue launch was broadcast as using the corrected post-parity route:
  - [AGENT_SYNC_gpt.md:24378](/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md#L24378)
- That queue has now been frozen by audit.
- The only output from it that currently exists is a forensic epoch-0 trace:
  - [V4_hybrid_standard_noise_hat_all_linear_r40_50ep.log](/home/qiaosir/projects/compute_vit/logs/_gpt/V4_hybrid_standard_noise_hat_all_linear_r40_50ep.log)
  - epoch-0 test: `76.38%`

## E6. What is NOT disputed
The following points remain stable regardless of the multiplier ruling:
1. config-sharing in `convert_to_hybrid()` was real and has been fixed.
2. `delta_g_eff` wrapper semantics were ambiguous and were fixed (`<0` auto-fill, `0.0` literal zero).
3. `group=all` still appears healthier than `group=mlp` directionally.
4. No new evidence suggests the mainline route should switch away from uniform-NL + cadence.

## E7. What must be decided
A single ruling is needed:
- If no-multiplier is intended, docs must be corrected and parity provenance re-labeled.
- If multiplier is intended, code/tests must be patched and parity/cadence rerun under the real corrected implementation.
