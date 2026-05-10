# Remote Holding Pattern (2026-04-23)

## Current status
- Do not start any new remote experiments yet.
- Local canonical K4R is actively running.
- Local Branch A runtime evidence is still live-only; stale pre-Branch-A `cx_k4_*alpha_0p25` JSON/CSV/MD files must not be reused.

## What remote should do now
1. Pull latest `remote-exploration` branch only.
2. Do environment validation and command-readiness checks only.
3. Wait for the next explicit queue update before launching new jobs.

## What remote should NOT do now
- Do not run new `group=all` cadence jobs.
- Do not run new `group=mlp` parity jobs.
- Do not cite old `27/58/81/44.29` numbers as current anchors.

## What remote may prepare
- exact environment manifest
- package versions
- CUDA / PyTorch / timm versions
- command wrappers for the next queue
- result packet templates using the established evidence spec

## Next trigger
Remote execution resumes only after a local update explicitly names:
- the next canonical experiment(s)
- the exact command(s)
- the evidence packet required for return
