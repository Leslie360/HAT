# Remote Delivery 2026-04-24

Source: user-transcribed remote agent delivery.
Status: retained as remote-side result packet; local integration requires Claude direction.

## TL;DR

- Mixed-NL (`MLP=1.0`, others `2.0`) -> abandon. Ceiling is about `58%`, then collapses.
- Domain randomization (`uniform NL=1.0 + D2D resample`) -> remote best path. `r40`: `90.03%` source / `54.69%` fresh.
- ALL-linear (`uniform NL=1.0`) -> safe fallback. About `89.93%` source.

## Bugs Fixed Remotely

### 1. Config sharing

Remote patch:

```python
import copy

# convert_to_hybrid():
analog_layer = AnalogLinear(..., config=copy.copy(config))  # was: config=config
analog_layer = AnalogConv2d(..., config=copy.copy(config))  # was: config=config
```

Local integration status, 2026-04-24:

- `analog_layers.py`: patched to pass `copy.copy(config)` at conversion sites.
- `analog_layers_ensemble.py`: patched to pass `copy.copy(config)` at conversion sites.
- Note: local constructors already copied config objects, but conversion-site copying now matches the remote fix and removes ambiguity.

### 2. LTP/LTD swap

Remote patch:

```python
# was:
torch.where(grad_output >= 0, grad_output * ltp_scale, grad_output * ltd_scale)

# fixed:
torch.where(grad_output >= 0, grad_output * ltd_scale, grad_output * ltp_scale)
```

Local integration status, 2026-04-24:

- `analog_layers.py`: already fixed.
- `analog_layers_ensemble.py`: already fixed for first-order branch.
- Related local tests pass:
  - `test_dual_bug_fix.py`
  - `test_groupwise_nl_wrapper.py`

## Remote Results

| Model | Source | Fresh | Std |
|:--|--:|--:|--:|
| `r40 replica` | `90.03%` | `54.69%` | `+-9.75%` |
| `r50v2 replica` | `91.51%` | `48.51%` | `+-11.05%` |
| `r10 replica` | `91.72%` | `43.62%` | `+-8.80%` |
| `r50 replica` | `91.08%` | `44.01%` | `+-8.71%` |
| `ALL-linear 100ep` | `89.93%` | `~11%` | unknown |

## Remote Must-Rerun Warning

Remote says the following historical families must be rerun:

1. Any `|NL_LTP| != |NL_LTD|` experiment, because LTP/LTD swap invalidates it.
2. Any `group != all` historical result, because config sharing silently made them uniform.

## Delivered File

Remote says it produced:

- `HAT_DELIVERY_20260424.tar.gz` (`52KB`): full report, patch, JSON logs, stdout logs.

This archive is not yet present in the local workspace at the time of this retention note.

## Local Integration Notes

The remote delivery arrives after local post-fix reruns that introduced a separate local evidence stream:

- `postfix_ensemble_hat_v4_nl20_fresh_eval.json`: `81.6948%` fresh under explicit `NL=2.0/-2.0`, uniform noise.
- `V3_hybrid_standard_noise_standard_train_best_fresh_eval.json`: `82.6346%` fresh under explicit `NL=2.0/-2.0`, uniform noise.
- `V4_hybrid_standard_noise_hat_best_fresh_eval.json`: `90.8766%` fresh under explicit `NL=2.0/-2.0`, proportional noise.

Critical caution:

- The proportional checkpoint metadata currently records `nl_ltp=1.0`, `nl_ltd=-1.0`, while the fresh eval explicitly overrides `NL=2.0/-2.0`. This must be cross-reviewed before treating `90.8766%` as a canonical same-config result.
- Two root-level files named `CODEX_CROSS_REVIEW_STANDARD_HAT_20260424.md` and `CODEX_CROSS_REVIEW_PROPORTIONAL_HAT_20260424.md` are prompt/terminal-capture fragments, not valid review reports.

## Immediate Local Ruling Needed

Claude must decide the next route before remote launches more jobs:

1. Whether remote `r40 domain randomization` becomes the main scientific path.
2. Whether local post-fix uniform/proportional reruns supersede the older remote route.
3. Which minimal parity/evidence packet is required before remote resumes compute.
4. Whether the paper-1 narrative remains structural-limit, shifts to HAT recovery, or splits into uniform vs proportional noise regimes.
