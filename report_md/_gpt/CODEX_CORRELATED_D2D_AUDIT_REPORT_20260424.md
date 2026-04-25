# Codex Correlated D2D Audit Report

Date: 2026-04-24
Task: R3-2 data-side audit from `DISPATCH_KIMI_CODEX_CORRELATED_D2D_AUDIT_20260424.md`
Owner: Codex

## Verdict

Correlated D2D zone verdict: **3A bug-immune, keep**.

No GPU reproduction is required for the current manuscript lock. The audited run is an evaluation-only `NL=1.0` canonical Ensemble HAT sweep with AMP disabled. It does not depend on the severe-NL STE path, mixed-NL groupwise path, ADC hook path, or the later `1 < NL < 2` guard patch.

## Source Artifacts

| Artifact | Path | Status |
|:--|:--|:--|
| Primary JSON | `report_md/_gpt/json_gpt/fresh_instance_eval_v4_ensemble_correlated_d2d.json` | Present, untracked workspace artifact |
| Release mirror | `release_artifacts/source_data_v1/fresh_instance_eval_v4_ensemble_correlated_d2d.json` | Present, git-tracked |
| Generator script | `scripts/_gpt/eval_spatially_correlated_d2d.py` | Present, git-tracked |
| Figure outputs | `paper/figures/figS_corr_d2d.png`, `paper/figures/figS_corr_d2d.pdf` | Present |

Integrity checks:

| Check | Result |
|:--|:--|
| JSON md5 | `68a9481a02277ec9a1a1e66e7f6cf9c4` for both primary and release mirror |
| JSON byte comparison | Identical |
| Release artifact git blob | `70207145586345ec754511aa80d58f0d15299b3f` |
| Generator script git blob | `733489ffd7d21cb5d013ef5cd42a2b39e9ca68ec` |
| Git commit adding tracked artifact/script | `15764d62ded10af2ab3e7da4da45796e11acf7d1` |
| Commit subject | `[Round Q Day 1] J1d reconciliation, K2 N=30 fresh eval, K3 delta_g_eff sweep init` |

Generation timestamp inside JSON: `2026-04-19T02:44:02.601771`.

The exact runtime commit was not embedded in the JSON. The tracked release artifact and generator script were later committed together at `15764d6`. This is a provenance limitation, but it is not a scientific blocker because the configuration is in the bug-immune zone and the JSON mirrors are byte-identical.

## Protocol

Checkpoint: `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt`

Checkpoint md5: `603e73bff8615b63e465dfd083a3970e`

Checkpoint config:

| Field | Value |
|:--|:--|
| name | `V4_hybrid_standard_noise_hat` |
| best_acc | `91.13` |
| best_epoch | `94` |
| nl_ltp | `1.0` |
| nl_ltd | `-1.0` |
| sigma_c2c | `0.05` |
| sigma_d2d | `0.1` |
| noise_mode | `uniform` |
| noise_enabled | `True` |
| hat_training | `True` |
| use_hybrid | `True` |
| epochs | `100` |
| batch_size | `64` |

Evaluation protocol from JSON:

| Field | Value |
|:--|:--|
| fresh instances | `10` |
| MC runs per instance | `5` |
| correlation model | `separable_ar1_2d` |
| evaluated rho values | `0.0`, `0.3`, `0.5` |
| eval AMP | disabled in generator call to `evaluate(..., amp_enabled=False)` |
| D2D modules touched | `42` resampled modules; `42` correlated modules for rho > 0 |

## Locked Results

| Condition | Mean (%) | Std (%) | Min instance (%) | Max instance (%) | Delta vs iid (pp) |
|:--|--:|--:|--:|--:|--:|
| iid, rho=0.0 | `86.3288` | `1.6093` | `83.696` | `88.560` | `0.0000` |
| AR(1), rho=0.3 | `84.5656` | `2.3923` | `80.146` | `87.160` | `-1.7632` |
| AR(1), rho=0.5 | `82.1244` | `3.9460` | `73.706` | `85.970` | `-4.2044` |

Rounded paper values are therefore:

| Condition | Paper value |
|:--|:--|
| matched iid baseline | `86.33 +- 1.61%` |
| rho=0.3 AR(1) | `84.57 +- 2.39%` |
| rho=0.5 AR(1) | `82.12 +- 3.95%` |
| minimum tested instance | `73.7%` |

The monotonic pattern required by the theory-side AR(1) discussion holds:

`86.33 > 84.57 > 82.12`, with increasing cross-instance variance `1.61 -> 2.39 -> 3.95`.

## Zone Classification

Classification: **Zone 3A**.

Reasoning:

- The checkpoint and run are `NL=1.0` / `NL_LTD=-1.0`; the severe-NL STE sign and second-order guard issues do not affect this result.
- The run is evaluation-only; no backward pass, no STE training dynamics, and no AMP training path are involved.
- The generator explicitly evaluates with `amp_enabled=False`.
- The groupwise mixed-NL config-sharing issue does not apply because this is a uniform canonical Ensemble HAT checkpoint, not a `group != all` mixed-NL experiment.
- The ADC hook issue does not apply to this claim; the correlated-D2D result is a fresh-instance robustness result under the standard analog forward protocol, not an ADC-on deployment-fidelity claim.

## Reproduction Decision

No rerun launched.

Rationale:

- Dispatch requires no GPU work unless the provenance is contaminated or verification is needed.
- The only provenance gap is missing runtime commit metadata in the JSON. The scientific path itself is bug-immune, the tracked release artifact matches the primary JSON byte-for-byte, and all values match current manuscript citations.
- A rerun would be confirmatory rather than corrective. It can be deferred unless Claude wants a stricter runtime-commit attestation.

## Paper-Safe Statement For Kimi

The correlated-D2D AR(1) sweep is classified as **Zone 3A bug-immune**. It evaluates the canonical Tiny-ViT V4 Ensemble HAT checkpoint at `NL=1.0`, using `10` fresh arrays and `5` Monte Carlo evaluations per array, with AMP disabled and a separable AR(1) perturbation applied only to the D2D mismatch buffers. The locked values are `86.33 +- 1.61%` for matched i.i.d. mismatch, `84.57 +- 2.39%` for `rho=0.3`, and `82.12 +- 3.95%` for `rho=0.5`; the worst tested instance is `73.7%`. The result supports a bounded, monotonic degradation claim under moderate spatial correlation, not a measured-device guarantee.

## Coordination

Signal to Kimi:

`Correlated D2D zone verdict: 3A bug-immune, keep. No rerun required unless Claude demands exact runtime-commit attestation. Use the paper-safe statement above for Supp Note S2 and thesis citations.`

