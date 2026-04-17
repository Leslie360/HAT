# NL Gradient Distortion Diagnostic

- Generated: `2026-04-17 03:01:50`
- Experiment: `V4`
- Dataset: `cifar10`
- Batches: `8`
- Batch size: `16`
- Matched forward path: `sigma_c2c=0`, preserved D2D, eval-mode deterministic backprop

| Group | Affected Modules | Full-Grad Cosine | Affected-Grad Cosine | Full Norm Ratio | Affected Norm Ratio | Affected Sign-Flip | Mean Loss Delta |
|:--|--:|--:|--:|--:|--:|--:|--:|
| MLP | 20/42 | 0.9834 | 0.8150 | 0.9730 | 0.6713 | 0.0000 | +0.000000 |
| All analog | 42/42 | 0.9834 | 0.8158 | 0.9730 | 0.6759 | 0.0000 | +0.000000 |
| Patch Embed | 2/42 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | +0.000000 |
| Attention QKV | 10/42 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | +0.000000 |
| Attention Proj | 10/42 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | +0.000000 |

## Interpretation

- `Mean Loss Delta` staying near zero confirms that this diagnostic is measuring backward-surrogate distortion rather than a forward-path mismatch.
- Lower cosine similarity indicates stronger gradient-direction distortion under `NL=2.0` for the selected module group.
- Higher sign-flip rate indicates a larger fraction of affected parameters whose gradient direction reverses relative to the linear-surrogate baseline.

