# CLAUDE-A Preliminary Decision — 2026-04-18

## Decision

**Option B**.

Keep the severe-`NL` mitigation story as a **supplementary ablation / mechanistic clarification**, not as a fifth main-paper contribution.

## Why this decision was taken

The original main-paper claim is still defensible in its narrowed form:

- the baseline severe-write recipe (`NL=2.0`) remains a hard failure mode for the present gradient-scaling surrogate,
- the failure is not uniformly distributed across all analog blocks,
- the strongest source-domain rescue is localized to the `MLP` path.

However, the new mitigation results do **not** yet support a clean, general, deployment-facing main-text claim.

## Evidence rows

### Source-domain training lanes

| Lane | Best acc (%) | Final acc (%) | Readout |
|:--|--:|--:|:--|
| Baseline severe `NL=2.0` | 27.72 | n/a | manuscript-locked anchor for the current baseline recipe |
| `MLP-only` linear compensation | 87.79 | 86.22 | strong positive rescue |
| `QKV-only` linear compensation | 18.72 | 10.15 | negative control; collapse |
| `all-linear` compensation | 87.49 | 84.81 | upper-bound control; no material gain over `MLP-only` |

### Fresh-instance transfer lanes

| Lane | Train best acc (%) | Fresh-instance mean (%) | Cross-instance std (%) | Status |
|:--|--:|--:|--:|:--|
| fixed HAT | 91.94 | 10.00 | 0.00 | canonical collapse |
| epoch-resampled Ensemble HAT | 91.13 | 86.33 | 1.61 | canonical positive transfer result |
| batch-resampled control | 90.30 | 89.48 | 0.36 | canonical cadence control |
| `MLP-only` severe-`NL` mitigation | 87.79 | 32.12 | 7.72 | source rescue does **not** transfer strongly |
| `QKV-only` severe-`NL` mitigation | 18.72 | 10.01 | 0.10 | complete fresh-instance collapse |
| `all-linear` severe-`NL` mitigation | pending at memo write time | pending | pending | targeted follow-up still running |

## Interpretation

### 1. Why `QKV-only` failure matters

`QKV-only` collapsing to `18.72%` in-domain and `10.01 ± 0.10%` fresh-instance is the critical negative control. It rules out a generic story of the form:

- "protecting any attention-side analog block rescues severe `NL`", or
- "the severe-`NL` failure is simply a transformer-wide precision issue with interchangeable sensitive sites".

Instead, the current evidence supports a **path-localized** explanation centered on the `MLP` analog path.

### 2. Why `MLP-only` success is still not enough for main-text escalation

`MLP-only` is a strong **source-domain** result, but not yet a strong **deployment-transfer** result:

- source-domain best: `87.79%`
- fresh-instance mean: `32.12 ± 7.72%`

That is a real mechanistic finding, but it is not the same class of deployment-stable evidence as the canonical Ensemble-HAT result (`86.37 ± 1.54%`).

### 3. Why `all-linear` does not currently force promotion

The source-domain `all-linear` result (`87.49%`) is effectively tied with `MLP-only`, which strengthens the localization story rather than overturning it. But until its fresh-instance behavior is known, it does not support a cleaner deployment-facing contribution than the supplementary ablation framing.

## What would flip this back into the main paper

Any of the following would justify reopening the main-text decision:

1. `attn_proj-only` completes above approximately `80%` and shows that the current failure is not as `MLP`-localized as it currently appears.
2. `all-linear` fresh-instance transfer lands in the same ballpark as the canonical Ensemble-HAT path (roughly `>80%` mean), showing a stable deployment-facing mitigation rather than a source-domain-only rescue.
3. `MLP-only` fresh-instance transfer is later improved into the same regime through a cleaner transfer-aware protocol, removing the current source/fresh mismatch.

Without one of those, the severe-`NL` mitigation story remains better suited to supplementary placement.

## Editorial consequence

### Main text

Keep the severe-`NL` language as:

- a **baseline-recipe bottleneck**,
- a limitation of the **present gradient-scaling surrogate / training recipe**,
- a motivation for follow-on mitigation work.

Do **not** rewrite the paper around a new headline mitigation contribution.

### Supplementary / response package

Promote the new ablation as:

- baseline severe `NL` anchor,
- `MLP-only` rescue,
- `QKV-only` collapse,
- `all-linear` upper-bound control,
- fresh-instance caveat where available.

## Preliminary caveat

This decision is **preliminary** because at memo-write time:

- `attn_proj-only` had not yet completed,
- `all-linear` fresh-instance transfer was still incomplete.

The current recommendation is therefore:

- **hold Option B**,
- finish the remaining lane(s),
- only escalate if the missing transfer-side evidence materially changes the interpretation.
