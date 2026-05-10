# G-BB1: Heavy-tailed conductance distribution stress-test spec

## Goal
Stress-test whether the Ensemble HAT ranking survives when D2D mismatch departs from the current Gaussian assumption and acquires a rare heavy-tail component.

## Minimal experiment
- Base harness: reuse `eval_spatially_correlated_d2d.py` / fresh-instance evaluation protocol.
- Keep the canonical checkpoint fixed: `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt`.
- Replace the current Gaussian D2D sampler with a **mixture model**:
  - with probability `1-p_tail`, draw the usual zero-mean Gaussian mismatch;
  - with probability `p_tail`, draw from a truncated log-normal or Student-t component with matched median but inflated upper tail.

## Recommended parameterization
- Primary family: **Gaussian + truncated log-normal mixture**.
  - Rationale: preserves positive-skew outliers without introducing infinite-variance pathologies.
- Tail probability sweep: `p_tail = 0, 0.01, 0.03, 0.05`.
- Tail severity sweep: multiplicative outlier factor target `1.5x, 2x, 3x` relative to the nominal D2D scale.
- Optional cross-check family: Student-t with `df = 3, 5, 10` and matched variance.

## Compute budget
- Start with `5 fresh arrays × 3 MC runs` for screening.
- Promote only the most reviewer-relevant condition to full `10 arrays × 5 MC runs`.
- Estimated cost: low-to-medium CPU/GPU budget because no retraining is required.

## Success criterion
The main claim survives if:
1. Ensemble HAT still remains well above the standard-HAT collapse regime;
2. the rank ordering `iid > mild heavy-tail > stronger heavy-tail` remains monotonic; and
3. the drop under `p_tail <= 0.05` stays bounded (for example, <5 percentage points from the Gaussian baseline).

## Output
- one JSON per family/sweep;
- one supplementary robustness figure with mean ± std;
- one rebuttal sentence: “The ranking survives under rare heavy-tail perturbations, although the variance broadens as expected.”
