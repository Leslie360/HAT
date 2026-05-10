# CLAUDE Patch Gating Matrix
**Date:** 2026-04-23

| Document Class | Classification | Rationale |
|:---|:---|:---|
| `paper/latex_gpt/*` | `do not touch` | Must wait until the minimal clean rerun lands to prevent drafting on hallucinated physics. |
| `远端/*.md` | `patch after fixes` | Remote must be synced to the exact commit of the atomic fix and given the new parity anchor. |
| `report_md/_gpt/*route*` | `patch now` | Add errata explicitly stating that previous route decisions were based on bugged data. |
| `report_md/_gpt/*checklist*` | `do not touch` | Hold until final numbers and narrative are settled post-rerun. |
