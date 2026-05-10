# Local GPU Mixed-Precision P0 Tasklist — 2026-05-10

## Objective

Use the local GPU for a thesis/Paper3-ready extension of Paper1: determine which Tiny-ViT analog layers are sensitive enough to deserve 8-bit/digital treatment and which can be safely mapped to 4-bit PCM.

## Why this is first

- Direct continuation of Paper1 PCM precision-retention frontier.
- Does not depend on Remote 107.
- P0 can start with inference/probing before expensive training.
- Produces thesis figures even if full mixed-precision training is deferred.

## Owner and scope

- Suggested implementation owner: Codex when assigned.
- Strategy/review owner: Claude/CC.
- Local GPU allowed only after `nvidia-smi` confirms safe capacity.
- Do not touch Paper1 release bundle.
- Do not modify checkpoints/data payloads except writing new experiment outputs under a dedicated results path.

## Output paths

Use a dedicated local-GPU thesis lane:

- `thesis/results/mixed_precision/`
- `thesis/figures/mixed_precision/` if figures are thesis-only.
- `logs/local_gpu_mixed_precision_*_20260510.log`
- `coordination/agent_reports/Codex/LOCAL_GPU_MIXED_PRECISION_P0_REPORT_20260510.md` or Claude equivalent.

## P0 tasks

### P0.0 GPU safety preflight

Commands must be logged.

- Run `nvidia-smi`.
- Record GPU name, utilization, VRAM used/free.
- If training/eval already active, stop and report.
- Do not run if VRAM would saturate; target <90% VRAM peak.

### P0.1 Locate current Paper1 model/eval entrypoints

Find and record:

- Tiny-ViT checkpoint/eval path.
- PCM / AIHWKit eval scripts.
- Figure/source-data provenance used by Paper1.
- Existing D2D/C2C/noise config interfaces.

Do not copy large checkpoints.

### P0.2 Define layer inventory

Output TSV:

`thesis/results/mixed_precision/layer_inventory_20260510.tsv`

Columns:

- layer_id
- module_path
- layer_type
- parameter_count
- current_mapping
- candidate_precision
- notes

### P0.3 Perturbation sensitivity probe

For each candidate analog layer:

- run a small eval subset or calibrated validation split;
- apply controlled perturbation/noise to one layer at a time;
- record accuracy/PPL delta or loss/logit delta;
- repeat over at least 3 D2D seeds if feasible.

Output TSV:

`thesis/results/mixed_precision/layer_sensitivity_20260510.tsv`

Columns:

- layer_id
- module_path
- perturbation_type
- sigma_d2d
- sigma_c2c
- seed
- metric_baseline
- metric_perturbed
- delta
- rank

### P0.4 Ranking figure

Create:

- `thesis/figures/mixed_precision/fig_layer_sensitivity_20260510.png`
- optional PDF version.

Figure must state whether it is pilot/probe or claim-bearing.

### P0.5 Report

Report must include:

- GPU preflight.
- exact commands.
- dataset/split.
- checkpoint identity.
- sensitivity ranking.
- recommended P1 mixed-precision maps.
- evidence grade: P0 probe, not final claim unless full protocol is complete.

## P1 candidate maps after P0

Use P0 ranking to evaluate:

1. all 8-bit PCM baseline.
2. all 4-bit PCM baseline.
3. top 10% sensitive layers 8-bit, rest 4-bit.
4. top 30% sensitive layers 8-bit, rest 4-bit.
5. top 50% sensitive layers 8-bit, rest 4-bit.
6. digital-sensitive / analog-robust hybrid if supported.

## Success criteria

P0 success:

- produces layer ranking and at least one usable figure.
- identifies top sensitive layers with clear effect sizes.

P1 success:

- mixed map approaches all-8-bit accuracy while using >=50-70% 4-bit analog layers.
- retention/drift penalty is better than all-4-bit.

## Stop conditions

- GPU already busy.
- missing checkpoint or dataset provenance.
- perturbation probe cannot reproduce baseline within tolerance.
- any result would require editing Paper1 release source.
