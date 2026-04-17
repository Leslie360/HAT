# Gemini Task Brief: P13 + P14

## Read These First (in order)

1. Canonical task state:
   - `/home/qiaosir/projects/compute_vit/report_md/_gpt/CLAUDE_TASK_gpt.md`
2. Latest live coordination / evidence:
   - `/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md`
3. Your two concrete prep tasks:
   - `/home/qiaosir/projects/compute_vit/report_md/_gpt/AIHWKIT_COMPARISON_DESIGN_gpt.md`
   - `/home/qiaosir/projects/compute_vit/report_md/_gpt/P14_FLOWERS_ABLATION_PLAN_gpt.md`

Do **not** start by reading old handoff notes or broad review dumps. Treat the four files above as the canonical entrypoint.

## Context

The main paper/task stream is currently fixing the failed `C4` rerun path locally. Your job is to prepare the two highest-priority reviewer-response follow-ups in parallel without launching heavy GPU work unless explicitly necessary and clearly justified.

Current environment note:
- `aihwkit` is **not installed** in the current local Python environment (`ModuleNotFoundError`).
- Therefore, the first deliverable is a minimal, concrete benchmark plan and dependency/command checklist that can be executed once the package is available.

## P13: AIHWKIT Shared-Regime Benchmark Prep

### Goal
Prepare a minimal benchmark design that directly answers the reviewer pressure point: "why not use an inorganic simulator like AIHWKIT?"

### Minimum deliverable
1. A one-page implementation plan for a **shared-regime** benchmark.
2. The minimal command sequence that would run once AIHWKIT is installed.
3. The exact repo files that would need to change or be added.
4. A short note on what can and cannot be matched between AIHWKIT and the current framework.

### Recommended benchmark shape
- Backbone: `ResNet-18`
- Dataset: `CIFAR-10`
- Regime: one shared quantization/noise setting, matched as closely as possible to the current `C1/C4` semantics
- Objective: compare a single shared regime across:
  - quantization only
  - quantization + shared noise
  - hardware-aware training / fine-tuning under the same shared regime

### Likely command template after dependency availability
```bash
python -u <new_aihwkit_benchmark_script>.py \
  --backbone resnet18 \
  --dataset cifar10 \
  --shared-regime \
  --quant-bits 4 \
  --adc-bits 8 \
  --noise-mode shared \
  --eval-runs 10
```

### Local code-paths to inspect
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/AIHWKIT_COMPARISON_DESIGN_gpt.md`
- `/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/02_related_work.tex`
- `/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/06_discussion.tex`
- `/home/qiaosir/projects/compute_vit/train_convnext.py`
- `/home/qiaosir/projects/compute_vit/analog_layers.py`

### Exact prep commands
```bash
python -c "import aihwkit; print(getattr(aihwkit, '__version__', 'unknown'))"
python -u scripts/_gpt/<aihwkit_shared_regime_benchmark>.py --backbone resnet18 --dataset cifar10 --shared-regime --quant-bits 4 --adc-bits 8 --noise-mode shared --eval-runs 10
```

### Expected output
- A design note that can be cited in `§6.7` / future-work discussion if execution is blocked.
- If execution becomes possible, a tiny table with AIHWKIT vs current-framework accuracy under the same regime.

## P14: Flowers-102 Noise-Magnitude Ablation Prep

### Goal
Prepare the smallest defensible ablation that addresses the reviewer critique that the Flowers-102 HAT failure is only a hypothesis.

### Minimum deliverable
1. A minimal ablation plan that sweeps noise magnitude toward zero.
2. Exact commands for the current codebase.
3. The checkpoint / experiment paths to reuse.
4. A short interpretation note on what result would support or weaken the "data-volume floor" hypothesis.

### Recommended benchmark shape
- Use the current ConvNeXt or Tiny-ViT path already in the repo.
- Run one near-zero noise condition and one canonical noise condition.
- Prefer the smallest set of changes that still produce a reviewer-facing ablation.

### Local code-paths to inspect
- `/home/qiaosir/projects/compute_vit/run_noise_sweep.py`
- `/home/qiaosir/projects/compute_vit/train_convnext.py`
- `/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex`
- `/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/06_discussion.tex`

### Exact prep commands
```bash
python -u run_noise_sweep.py --help
python -u train_convnext.py --dataset flowers102 --seed 42 --batch-size 128 --mode train --experiments C4 --num-workers 0
python -u train_convnext.py --dataset flowers102 --seed 42 --batch-size 128 --mode eval --experiments C4 --checkpoint <path-to-best-ckpt> --eval-runs 10
```

### Expected output
- A concise plan note plus command template.
- If execution happens, a 2-row or 3-row ablation summary suitable for the appendix or rebuttal.

## Constraints

- Do not revert other agents' changes.
- Prefer read-only inspection and planning unless a file update is clearly needed.
- Keep the output concrete: command templates, file paths, and a recommendation about whether the experiment should be run now or kept as future work.
