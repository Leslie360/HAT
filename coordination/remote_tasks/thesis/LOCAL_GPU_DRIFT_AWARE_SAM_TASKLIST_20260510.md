# Local GPU Drift-Aware SAM Tasklist — 2026-05-10

## Objective

Test whether training for flatness along physical PCM drift directions improves long-horizon retention more than generic flatness methods such as SAM/SWA.

## Thesis/Paper value

This becomes a physics-aligned optimization chapter/possible Paper3 direction:

> generic flat minima are not necessarily physically stable; drift-aware flatness should target the device's time-evolution vector field.

## Start condition

Do not start until either:

- mixed-precision P0 is complete, or
- user explicitly prioritizes drift-aware optimization.

## Output paths

- `thesis/results/drift_aware_sam/`
- `thesis/figures/drift_aware_sam/`
- `logs/local_gpu_drift_aware_sam_*_20260510.log`
- `coordination/agent_reports/Codex/LOCAL_GPU_DRIFT_AWARE_SAM_REPORT_20260510.md`

## Tasks

### D0 GPU and provenance preflight

- Run `nvidia-smi`.
- Confirm checkpoint/dataset provenance.
- Confirm no ongoing local GPU training.
- Tee all logs.

### D1 Drift-vector profiling

For a selected PCM setting, compute/estimate the conductance drift vector between:

- t=0
- t=1 day
- t=7 days
- optional t=30 days extrapolated

Output:

`thesis/results/drift_aware_sam/drift_vectors_20260510.npz` or TSV/JSON summary.

Report:

- drift model source.
- device profile.
- layer-wise drift norms.
- correlation with weight magnitude / conductance state.

### D2 Baseline training/eval matrix

Compare:

1. AnalogSGD / standard optimizer baseline.
2. SWA if already implemented.
3. standard SAM if feasible.
4. Drift-aware SAM.

Keep first pass small:

- one backbone.
- one dataset.
- one PCM precision setting.
- 3 seeds if feasible; 1 seed pilot acceptable if marked pilot.

### D3 Drift-aware SAM algorithm

Prototype:

1. compute drift-aligned perturbation direction.
2. evaluate loss under drift-perturbed conductance/weights.
3. update model to minimize worst drift-aligned loss.

Record exact implementation assumptions.

### D4 Long-horizon evaluation

Evaluate each method at:

- fresh t=0.
- t=1 day.
- t=7 days.
- t=30 days extrapolated if model supports.

Outputs:

- `drift_aware_sam_summary_20260510.tsv`
- `fig_drift_retention_curves_20260510.png/.pdf`

## Success criteria

Strong success:

- Drift-aware SAM improves 7-day or 30-day accuracy by >=3 pp over standard optimizer without large fresh-accuracy penalty.

Moderate success:

- It reduces drift loss variance or preserves the 1 pp SLA better than SWA/SAM.

Negative result still useful if:

- generic SAM/SWA worsens physical drift, supporting Paper1's cautionary framing.

## Stop conditions

- drift model cannot be traced to current Paper1 provenance.
- training is too expensive for local GPU.
- implementation requires destabilizing active Paper1 code.

## Evidence labels

- P0/D1 profiling: pilot/protocol evidence.
- D2-D4 multiseed matrix: possible thesis claim if metadata complete.
