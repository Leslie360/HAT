# Remote Handoff Packet (2026-04-22)

## Use this packet first
If you only read one file before resuming remote work tomorrow, read this one.

## Current authoritative route
The chosen mainline is:
- **uniform-NL / `group=all`**
- **domain-randomization / D2D resampling cadence**

Mixed-NL / `group=mlp` is now a **diagnostic branch**, not the mainline solution path.

## Why the route changed
Two source-level bugs were confirmed locally and fixed:
1. config-sharing in `convert_to_hybrid()`
2. missing `nl` multiplier in the LTP first-order backward scale

After both fixes, the corrected local 1-epoch parity anchor is:

| setting | test acc |
|:--|--:|
| `mlp + SO2 + auto(-1.0)` | 46.75% |
| `mlp + SO2 + literal zero(0.0)` | 57.00% |
| `mlp + no SO2` | 55.65% |
| `all + SO2 + auto(-1.0)` | 83.34% |

Interpretation:
- old local `81.86%` is not a valid corrected mixed-NL anchor
- old remote `~27%` is not a valid corrected mixed-NL anchor
- corrected mixed-NL now sits in a mid-band (`46–57%`)
- corrected `group=all` remains clearly healthy (`83.34%`)

## Remote should do next
Use:
- `REMOTE_TASK_QUEUE_V5_20260422.md`

Priority order:
1. corrected `r40`
2. corrected `r50`
3. corrected `r10`
4. corrected `r50 50ep vs 100ep`

## Remote should NOT do next
- do not spend major GPU budget trying to rescue `group=mlp` as the main strategy
- do not continue arguing over old `27 / 58 / 81` parity numbers
- do not use pre-fix mixed-NL numbers as final ceiling claims

## Required reply format
Still use:
- `REMOTE_EVIDENCE_PACKAGE_SPEC_20260422.md`

Minimum package:
1. exact command
2. code diff
3. checkpoint md5
4. protected module count + first module names
5. source best / final
6. fresh per-instance table
7. one-line verdict

## Supporting authoritative files
1. `REMOTE_ROUTE_DECISION_20260422.md`
2. `REMOTE_TASK_QUEUE_V5_20260422.md`
3. `REMOTE_REPLY_AND_NEXT_TASKS_V2_20260422.md`
4. `REMOTE_LOCAL_PARITY_REANCHOR_20260422.md`
5. `REMOTE_REPLY_TO_PARITY_DISSECTION_20260422.md`

## Local/remote coordination status
- GitHub user: `Leslie360`
- repo: `https://github.com/Leslie360/HAT.git`
- branch: `remote-exploration`

## Bottom line
The route is now chosen.
Remote value is no longer to prove mixed-NL parity.
Remote value is to rapidly optimize the corrected **uniform-NL + domain-randomization** branch.
