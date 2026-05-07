# Remote107 Boundary and Next Tasks — Experiment-Only Server Role

Date: 2026-05-08  
From: Codex coordinator  
To: Remote107 agent  
Branch: `107-clean`

## Boundary Ruling

Remote107 is an experiment server, not the manuscript workstation.

Do:
- run K107/KV-cache experiments;
- generate JSON/CSV summaries;
- preserve exact commands, logs, git SHA, environment, and metadata;
- audit experiment code and feasibility;
- provide draft/check figures only as data sanity checks.

Do not:
- write final manuscript prose;
- polish final figures for publication aesthetics;
- edit Paper-1 LaTeX;
- decide narrative framing;
- mix old evaluator baselines into current K107 results.

Final paper writing, figure polish, and narrative integration happen locally.

## Current Locked State

- K107 canonical baseline: 22.1849 PPL under ctx=512, stride=256, batch=1.
- Deprecated baseline: 15.62/15.68 from old ctx=1024/stride=512/batch=8 evaluator.
- P0-B ladder: raw 22.185 -> B1 19.043 -> B2 19.060 -> B3 19.483 -> B4 19.644.
- EPSC central proxy C2C=0.10/D2D=0.10 max: 20.231 < 25, PASS.
- Scale trend: 410M 19.48 -> 1B 14.60 -> 2.8B 13.34 at D2D=0.02.
- 6.9B: blocked under fp32 single-GPU 32GB; only revisit with AMP/BF16/checkpointing or larger/multi-GPU setup.

## Next Tasks

### 107-E1: Keep Freeze Package Reproducible

If any new commits touch result aggregation, rerun and verify:

- `deliverable/results_v3/k107_canonical_summary.csv`
- `deliverable/results_v3/k107_plot_ready.json`
- `coordination/REMOTE107_K107_CANONICAL_FREEZE_20260508.md`

Return only if numbers change or a reproducibility bug is found.

### 107-E2: AMP/Frozen-Param Code Path Audit

You pushed `--freeze-non-target-params` and `--fp16` support. Provide a short audit return:

- exact changed files;
- whether old locked results remain valid without rerun;
- memory estimate before/after freeze;
- whether AMP changes numerical results in a smoke test;
- recommendation: keep code-only / rerun 2.8B / attempt 6.9B later.

Output:
`coordination/REMOTE107_AMP_FREEZE_AUDIT_RETURN_20260508.md`

### 107-E3: No New Long GPU Runs Unless Approved

Do not launch 6.9B or new large-model training without first writing:

`coordination/REMOTE107_LONG_RUN_PROPOSAL_YYYYMMDD.md`

It must include expected GPU-hours, memory plan, exact command, and what manuscript claim it changes.

## Return Format

Every return must start with:

| Task | Status | GPU-hours | Changed locked claim? | Verdict |
|---|---:|---:|---:|---|

Keep returns concise and data-first.
