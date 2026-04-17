# AIHWKIT Shared-Regime Benchmark Design (P13)

## Current status

This task is now **execution-ready** and has a CPU-smoke benchmark result:

- reviewer pressure point: `C1` shared-regime comparison against AIHWKIT
- required benchmark shape: **minimal, concrete, shared-regime**
- local environment: `aihwkit==1.1.0`, `torch`, and `torchvision` are available in the `LLM` conda env
- current implementation: `scripts/_gpt/aihwkit_shared_regime_benchmark_gpt.py`
- achieved result: a CPU benchmark on an existing ResNet-18/CIFAR-10 checkpoint, with digital-vs-AIHWKIT comparison on a fixed test subset

The old execution blocker has been cleared in the local benchmark environment; the remaining limitation is that the current result is a CPU subset smoke benchmark, not a full-scale reproduction sweep.

## Why this benchmark exists

Reviewers are no longer satisfied with a purely qualitative distinction between:

- this repo's organic/optoelectronic, profile-driven simulator, and
- mature inorganic CIM stacks such as AIHWKIT.

The narrow goal is **not** to prove that AIHWKIT can reproduce every organic-specific behavior. The goal is to answer the sharper reviewer question:

> Under one matched quantization/noise regime, does our framework produce materially different system-level conclusions from an established inorganic analog-simulation toolkit?

## Recommended minimal benchmark

### Backbone and dataset

- **Model**: `ResNet-18`
- **Dataset**: `CIFAR-10`

Reason:

- this repo already has a stable ResNet-18 training path in:
  - `/home/qiaosir/projects/compute_vit/train_resnet18.py`
- a ResNet benchmark is cheaper and cleaner than trying to force an initial AIHWKIT comparison on Tiny-ViT
- reviewer demand is "at least one shared-regime numeric comparison", not a full architecture sweep

### Shared regime to match

Use the repo's existing `R1/R4` semantics as the anchor:

| Regime | Local repo meaning | AIHWKIT approximation |
|:--|:--|:--|
| `R1` | FP32 digital baseline | ordinary PyTorch baseline |
| `R4` | 4-bit analog, `sigma_c2c=0.05`, `sigma_d2d=0.10`, HAT enabled | AIHWKIT analog tile with matched 4-bit-like effective state regime plus additive programming/read noise |

This gives the smallest reviewer-facing table:

1. Digital baseline
2. Analog noisy inference
3. Hardware-aware / analog-aware training

## Mapping assumptions

The comparison should be framed as **shared-regime**, not "identical physics":

| Component | Present framework | AIHWKIT approximation | Caveat |
|:--|:--|:--|:--|
| Weight mapping | differential conductance pair in `AnalogConv2d` / `AnalogLinear` | analog tile or equivalent differential mapping | exact device internals differ |
| Quantization | explicit `n_states` | tile granularity / clip / resolution settings | semantic match, not bit-for-bit identity |
| C2C noise | per-forward Gaussian `sigma_c2c` | read/program noise proxy | timing model differs |
| D2D mismatch | fixed initialization mask | programming noise / persistent weight perturbation | not identical persistence semantics |
| HAT | current repo HAT recipe | AIHWKIT analog-aware training / optimizer loop | optimizer implementation differs |
| Retention / photoresponse | supported here | not native | out of scope for the shared-regime benchmark |

## Minimal executable path

### Environment probe

```bash
/home/qiaosir/miniconda3/envs/LLM/bin/python -c "import aihwkit; print(getattr(aihwkit, '__version__', 'unknown'))"
```

### Local baseline anchor

Use the existing ResNet script and record the matched local regime first:

```bash
/home/qiaosir/miniconda3/envs/LLM/bin/python -u /home/qiaosir/projects/compute_vit/train_resnet18.py \
  --experiments R1 R4 \
  --epochs 200 \
  --batch-size 128 \
  --device cuda \
  --data-root ./data \
  --save-dir checkpoints/_gpt/aihwkit_anchor \
  --output-dir report_md/_gpt
```

### AIHWKIT script entrypoint

```bash
/home/qiaosir/miniconda3/envs/LLM/bin/python -u /home/qiaosir/projects/compute_vit/scripts/_gpt/aihwkit_shared_regime_benchmark_gpt.py \
  --device cpu \
  --test-samples 256 \
  --eval-runs 5 \
  --batch-size 64 \
  --train-samples 0
```

## Expected benchmark table

The paper only needs a compact result like:

| Framework | Regime | Accuracy |
|:--|:--|:--|
| PyTorch digital | FP32 baseline | `96.88%` on the CPU smoke subset |
| AIHWKIT | matched shared regime | `91.80 ± 1.02%` on the CPU smoke subset |

That is enough to support a bounded claim such as:

> Under a matched shared regime, the present framework tracks the same qualitative degradation trend as AIHWKIT while exposing organic-specific extensions that AIHWKIT does not natively model.

### CPU smoke benchmark result

- checkpoint: `/home/qiaosir/projects/compute_vit/checkpoints/R1_FP32_baseline_best.pt`
- digital subset accuracy: `96.88%`
- AIHWKIT subset accuracy: `91.80% ± 1.02%`
- subset size: `256`
- eval runs: `5`
- wall clock: `151.1s`

The machine-readable outputs are:

- `/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/p13_aihwkit_shared_regime_result_256.json`
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/P13_aihwkit_shared_regime_result_256.md`

## What this benchmark can and cannot prove

### It can support

- the framework is not numerically detached from established analog-CIM tooling
- our conclusions are not purely artifacts of a private simulator
- the organic-specific additions sit on top of a baseline that can be cross-checked

### It cannot support

- full physics equivalence between AIHWKIT and this organic/optoelectronic stack
- equivalence for photoresponse, retention, or organic non-linear writing
- cross-architecture fairness beyond the single shared benchmark

## Files most likely needed

- existing anchor:
  - `/home/qiaosir/projects/compute_vit/train_resnet18.py`
- likely new script:
  - `/home/qiaosir/projects/compute_vit/scripts/_gpt/aihwkit_shared_regime_benchmark_gpt.py`
- coordination references:
  - `/home/qiaosir/projects/compute_vit/report_md/_gpt/CLAUDE_TASK_gpt.md`
  - `/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md`
- manuscript hooks:
  - `/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/02_related_work.tex`
  - `/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/06_discussion.tex`

## Recommendation

For this morning's decision point:

- treat `P13` as **execution-ready with a CPU smoke benchmark complete**
- keep the current result as a reviewer-facing shared-regime comparison
- if a larger AIHWKIT run is desired later, it can be expanded from the same script without changing the manuscript-facing claims
