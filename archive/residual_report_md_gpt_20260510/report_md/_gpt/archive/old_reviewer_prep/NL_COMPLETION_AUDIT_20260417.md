# NL Completion Audit (2026-04-17)

## Scope

This note consolidates all currently available nonlinear-write (`NL`) evidence so
the manuscript, rebuttal, and follow-up experiments stop relying on scattered
coordination logs.

## Canonical manuscript-facing results

| Setting | Source | Best / Summary | Status |
| --- | --- | ---: | --- |
| `NL=2.0` full V4 retraining | `task35_v4_nl2_hat` | `27.37% @ epoch 15` train best; `27.72 ± 0.82%` eval | Canonical severe-NL anchor |
| `NL=3.0` full V4 retraining | `task23/v4_nl_severe` | `27.54% @ epoch 12` | Canonical extra severe point |
| `NL=1.5` host-WSL rerun | `task24/v4_nl_interp15` | `19.01% @ epoch 1`, final `9.76%` | Rebuttal-side instability evidence |

## Legacy landscape scan (historical but real CUDA runs)

These runs exist under `checkpoints/gm_e4_nl_scan/` and corresponding logs
`logs/_gpt/gm_e4_nl_*.log`.

| NL | Epoch-0 best | Final tail | Interpretation |
| --- | ---: | ---: | --- |
| `1.2` | `59.46%` | `~10.11%` | collapses during training |
| `1.5` | `58.01%` | `~9.52%` | collapses during training |
| `1.8` | `56.84%` | `~9.94%` | collapses during training |
| `2.2` | `56.43%` | `~9.22%` | collapses during training |
| `2.5` | `53.56%` | `~10.22%` | collapses during training |

These runs are useful as a historical failure landscape, but they are not clean
manuscript-grade artifacts because they predate the later paper lock state and
write only to generic sinks.

## Mechanistic evidence already completed

`nl_gradient_distortion_gpt.json` localizes the severe-`NL` distortion to the MLP
path:

- `MLP`: affected-gradient cosine `0.8150`, norm ratio `0.6713`
- `All analog`: affected-gradient cosine `0.8158`, norm ratio `0.6759`
- `Patch Embed`: `1.0000 / 1.0000`
- `Attention QKV`: `1.0000 / 1.0000`
- `Attention Proj`: `1.0000 / 1.0000`

This means the current `NL=2.0` failure is concentrated in the MLP surrogate
path, not uniformly across the entire Tiny-ViT analog stack.

## Practical interpretation

The combined picture is now stronger than the manuscript's original single-point
story:

1. `NL=2.0` is not an isolated cliff artifact.
2. Intermediate and higher `NL` settings repeatedly show training instability
   under the present gradient-scaling surrogate.
3. The distortion is localized primarily to the MLP write path.

That supports the reviewer-facing claim that the observed boundary is a limit of
the current training surrogate / recipe, rather than a proven physical device
law.

## Remaining gap

The main missing experiment is no longer "another blind NL sweep". It is a
targeted mitigation check:

- keep global `NL=2.0`
- restore the MLP group to linear surrogate (`NL=1.0`)
- test whether accuracy rebounds substantially

That is the cleanest next step because it upgrades the current mechanism story
into a mechanism-backed mitigation result.
