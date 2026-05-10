# Remote Holding Pattern V2 (2026-04-23)

## Status
- Do not launch any remote experiments.
- Local canonical path is under re-evaluation due to dual implementation issues:
  - second-order coefficient
  - branch-swap in LTP/LTD mapping

## What remote should do now
- freeze all planned launches
- archive current notes and environment manifests
- wait for a new exact command set after local fixes land

## What remote should NOT do now
- do not run new `group=all` or `group=mlp` jobs
- do not use `K4R` as canonical anchor
- do not extend `P1-C` or `P1-C2`

## Resume condition
Remote execution resumes only after local broadcast explicitly names:
1. the fix commit hash
2. the new minimal canonical rerun
3. the exact return packet format
