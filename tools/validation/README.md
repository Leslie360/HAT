# tools/validation/

Reusable validation scripts for locked claims, source data, release gates, and provenance checks.

## Current scripts

| Script | Validates | Inputs | Status |
|:--|:--|:--|:--|
| `check_local_pcm_precision_ladder.py` | Paper1 PCM precision-ladder evidence | Paper1 canonical JSON/source data and local evidence paths | active |

## Rules

- Check GPU state before running validation that may import torch or touch checkpoints.
- Always tee output to `logs/` with a timestamp.
- Validation scripts should state which paper/thesis claim they protect.
