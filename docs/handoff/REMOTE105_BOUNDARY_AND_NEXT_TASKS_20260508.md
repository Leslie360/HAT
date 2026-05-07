# Remote105 Boundary and Next Tasks — Experiment-Only Validation Role

Date: 2026-05-08  
From: Codex coordinator  
To: Remote105 agent  
Branch: `105-remote-results`

## Boundary Ruling

Remote105 is an experiment/validation server, not the manuscript workstation.

Do:
- run or verify TinyImageNet cross-architecture experiments;
- preserve JSON/CSV/logs/commands/environment;
- provide concise result tables and provenance;
- identify outliers and missing seeds.

Do not:
- write final manuscript prose;
- polish final figures;
- edit local Paper-1 LaTeX;
- change narrative framing beyond a short experimental recommendation.

Final paper writing, final figures, and narrative integration happen locally.

## Current Locked State

Remote105 latest full return is:
`docs/handoff/20260508_full_return.md`

Current interpretation:

- DeiT proportional beats digital in all three seeds: +1.98, +0.58, +2.75 pp fresh.
- ViT proportional beats digital in 2/3 seeds and is positive on average, but seed456 digital is a high outlier.
- Overall label: **provisional cross-architecture validation**.
- Proportional HAT has near-zero fresh degradation across tested seeds.
- Standard mode remains a strong negative control with ~30-34 pp collapse.

## Next Tasks

### 105-E1: Canonical Freeze Packet

Create/verify one final frozen package for Remote105:

- `results/summary/remote105_tinyimagenet_all_available_summary.csv`
- `results/summary/remote105_tinyimagenet_seed789_summary.csv`
- `docs/handoff/REMOTE105_CANONICAL_FREEZE_20260508.md`

The freeze MD must include:

1. exact training/eval commands;
2. environment;
3. per-seed source/fresh/std table;
4. proportional-vs-digital deltas;
5. metadata gap note for older seed123/456 JSONs;
6. one-sentence experimental recommendation.

### 105-E2: ViT Seed456 Outlier Note

Write a short diagnostic note:

`docs/handoff/REMOTE105_VIT_SEED456_OUTLIER_NOTE_20260508.md`

Answer:

- Is seed456 digital unusually high compared with seed123/789?
- Are commands/data splits/checkpoint paths identical?
- Does excluding seed456 change the conclusion?
- Should local team request more ViT seeds, or is current evidence sufficient as provisional validation?

No GPU needed unless a concrete metadata inconsistency is found.

### 105-E3: Optional Extra ViT Seeds Only If Cheap

Do not start new training unless E1/E2 says the outlier materially weakens the claim.

If needed, propose first:

`docs/handoff/REMOTE105_EXTRA_VIT_SEED_PROPOSAL_20260508.md`

Include expected GPU-hours, exact command, and which conclusion the run can change.

## Return Format

Every return must start with:

| Task | Status | GPU-hours | Changed locked claim? | Verdict |
|---|---:|---:|---:|---|

Keep returns concise and data-first.
