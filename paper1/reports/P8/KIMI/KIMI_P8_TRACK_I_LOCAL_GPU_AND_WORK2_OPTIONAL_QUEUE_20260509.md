# Kimi P8 Track I: Local GPU and Work-2 Optional Queue

Date: 2026-05-09
Scope: local GPU policy and optional non-blocking Work-2 queue
Status: COMPLETE — planning only; no GPU job launched

## 1. Policy status

Paper-1 local GPU remains closed. No open-ended Paper-1 retraining or rerun is justified because Paper-1 values, CSV/JSON, captions, and bundle are frozen and verified.

## 2. What was executed locally

| Action | GPU? | Status |
|---|---:|---|
| LaTeX rebuild | No | PASS |
| Final bundle refresh/SHA cold-unpack | No | PASS |
| PCM precision ladder guard | CPU/Python only | PASS |
| Stale-value grep | No | PASS |
| Cleanup/quarantine | No | PASS |

No GPU training/evaluation was launched in P8.

## 3. Optional GPU queue if user wants no resource waste

Only run these if GPU is idle and user explicitly wants extra work. Check `nvidia-smi` first and do not saturate VRAM.

| Priority | Job | Condition | Output | Paper-1 impact |
|---:|---|---|---|---|
| 1 | Paper-1 guard smoke eval | Read-only output directory; no canonical JSON/CSV overwrite | PASS/FAIL log under `logs/` | none |
| 2 | 107 local smoke test | Only if 107 code and small WikiText eval can run locally without downloads/checkpoints | command + log, no claims | Work-2 only |
| 3 | Figure/source-data regeneration check | CPU preferred; run plotting scripts into temp output | diff/no-diff report | guard only |
| 4 | Tiny self-contained repro | no new dataset download, no claim mutation | env sanity log | none |

## 4. Forbidden jobs

| Job | Reason |
|---|---|
| Open-ended Paper-1 retraining | Frozen claims |
| Any run overwriting canonical JSON/CSV | Traceability risk |
| Any job without commit/command/env/seed/output metadata | Unusable evidence |
| Parallel GPU jobs without capacity approval | User memory: avoid VRAM saturation; sequential preferred |
| Python/GPU work while training is already active | User memory: no scripts during active GPU training |

## 5. Safe command templates

### GPU status check

```bash
nvidia-smi
```

### Metadata wrapper template

```bash
ts=$(date +%Y%m%d_%H%M%S)
log="logs/p8_optional_${ts}.log"
{
  git rev-parse HEAD
  git status --short
  nvidia-smi
  echo "COMMAND: <fill exact command>"
  <fill exact command>
} 2>&1 | tee "$log"
```

## 6. Verdict

Track I COMPLETE. No Paper-1 GPU work was reopened; optional jobs are guard-only or Work-2-only and require explicit user approval before execution.
