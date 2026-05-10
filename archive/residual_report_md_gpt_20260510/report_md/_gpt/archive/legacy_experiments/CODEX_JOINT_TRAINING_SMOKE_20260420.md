# Codex Joint Training Smoke — 2026-04-20

## Scope

Round M `CX-FA` authorized a cheap GPU smoke test for the thesis-only joint-training direction:

- severe nonlinear write: `NL_LTP=+2.0`, `NL_LTD=-2.0`
- protection: `MLP-linear`
- training regime: `Ensemble HAT`
- budget: `3 epochs`
- dataset: `CIFAR-10`
- backbone/recipe: `Tiny-ViT V4`

This run was intended to validate wiring and checkpoint/output plumbing, not to establish a publishable performance number.

## Artifact

- JSON: `report_md/_gpt/json_gpt/joint_mlp_linear_ensemble_hat_smoke.json`
- CSV: `report_md/_gpt/csv_gpt/joint_mlp_linear_ensemble_hat_smoke.csv`
- Markdown: `report_md/_gpt/joint_mlp_linear_ensemble_hat_smoke.md`
- Log: `logs/_gpt/joint_mlp_linear_ensemble_hat_smoke_20260420_manual.log`
- Best checkpoint:
  `checkpoints/_gpt/joint_mlp_linear_ensemble_hat_smoke/V4_hybrid_standard_noise_hat_joint_mlp_linear_ensemble_hat_smoke_best.pt`

## Result

- best test accuracy: `28.44%`
- best epoch: `1`
- final test accuracy: `25.25%`

## Interpretation

1. The joint-training code path is functional.
   - Training launched on CUDA.
   - Ensemble HAT resampling remained active.
   - MLP-only protected linearization was accepted by the wrapper.
   - Checkpoints and result files were emitted correctly.

2. The 3-epoch cold-start smoke is not evidence for the thesis target.
   - The thesis spec targets a warm-started joint run and `>=80%` fresh-instance recovery.
   - This smoke was started from the generic pretrained path, not from a clean warm-start of the canonical Ensemble HAT checkpoint.
   - The current resume semantics make naïve checkpoint reuse unsafe for a 3-epoch smoke, because copied epoch counters would skip training.

3. The correct conclusion is implementation viability, not algorithmic success.
   - No NaN/AMP/path failure was observed.
   - The poor `28.44%` best accuracy means the cold-start 3-epoch pilot is too weak to evaluate the scientific merit of the joint method.

## Round-N Recommendation

If a thesis GPU window is approved, the next valid experiment should be:

1. implement a safe warm-start / weight-load path that does not inherit stale epoch counters;
2. launch the joint `MLP-linear + Ensemble HAT` experiment under the canonical fresh-instance protocol;
3. compare against:
   - Ensemble HAT only,
   - MLP-linear only,
   - joint cold-start,
   - joint warm-start.

## Submission Impact

None for the NC manuscript. This result stays in the thesis/rebuttal planning lane and does not alter the current paper narrative.
