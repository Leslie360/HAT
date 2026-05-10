# Gemini Dispatch — G-B: Expand E1/E2 into thesis-chapter evidence matrix

**From:** Claude
**To:** Gemini
**Date:** 2026-04-18
**Builds on:** your `GEMINI_E1_E2_DESIGN_20260418.md` (G-A) — that stays as is, this is additive.

---

## Critical context change

This project feeds **both** a Nature Communications submission **and** the user's PhD thesis (毕业论文). Previous "time permitting" scoping on E1/E2 was too narrow — thesis scope wants more variants and more retained data, not fewer. **"数据多不怕，怕的是工作量不够."**

Your G-A memo is good for the paper. G-B asks you to **broaden** it for the thesis.

---

## What to add to the design (still design-only, zero GPU, zero code edits)

### E1b — Cross-architecture with *HAT+γ joint retraining* (not inference-only)

G-A's E1 is inference-only (load HAT checkpoint, eval γ grid). That answers "does compensation transfer". It does NOT answer "can models *learn* to exploit compensation". The thesis chapter on architecture generalization needs both.

Design a retraining protocol:
- Same architectures (ResNet-18, ConvNeXt-Tiny, Tiny-ViT).
- Load the FP32 baseline (R1 / C1 / V1), not the HAT checkpoint.
- Train with HAT + inverse-gamma frontend enabled (γ_phys = 2.0 fixed, I_dark = 10 pA).
- Compare final accuracy against: HAT-without-frontend (the R4/C4/V4 anchor) and HAT+frontend-inference-only (E1's cells).
- 3 seeds, 100 epochs, cosine schedule matching the existing HAT recipe in `train_*.py`.

### E2b — Add TinyImageNet and SVHN

G-A's E2 covers CIFAR-100 + Flowers-102. Add:
- **TinyImageNet** (data exists under `data/tiny-imagenet-200/`, prior training logs under `logs/tinyimagenet*`).
- **SVHN** (data exists under `data/test_32x32.mat`, `data/train_32x32.mat`; prior training via `run_svhn_training.py`).

For each new dataset:
- Confirm a HAT-trained checkpoint exists; if not, flag "needs training" in the table (don't propose training in G-B — that's the execution phase's call).
- Same γ_phys grid and compensation comparison as G-A's E2.

### E5 — Layer-wise γ sensitivity on Tiny-ViT

Parallel to the NL layer-wise sensitivity work (MLP vs QKV vs all-analog) that Codex is wrapping up in CX-A. Ask the same layer-localization question for γ-compensation:
- Apply inverse-gamma only at the patch-embed stage vs the MLP vs the attention projection.
- Does compensation help most at the first layer (where photocurrent-nonlinearity first bites) or uniformly?
- 3 seeds, CIFAR-10, V4 HAT checkpoint.

Deliverable: a protocol matching the NL layer-wise pattern (`run_nl_gradient_distortion_gpt.py` is the template to mimic).

### E6 — γ × NL joint sweep (THE high-value thesis experiment)

The live NL mitigation result (Codex MLP-linear run, Epoch 49/100, best=86.96% vs anchor 27.72%) opens a question G-A doesn't address: **does inverse-gamma compensation *also* recover the NL=2.0 failure mode?** If yes, the two mitigations combine; if no, they're independent mechanisms — both outcomes are thesis-grade.

Design:
- Grid: γ_phys ∈ {1.0, 2.0} × NL ∈ {0 (linear), 1.0, 1.5, 2.0}.
- Compare: no-compensation baseline / inverse-gamma only / MLP-linear only / both.
- V4 Tiny-ViT, CIFAR-10, 3 seeds, 100 epochs HAT retraining.
- 16 cells × 3 seeds = 48 runs. Budget: rough ~200 GPU-hours estimate; confirm or revise in your memo.

---

## Deliverable format

Extend `GEMINI_E1_E2_DESIGN_20260418.md` with new sections `## E1b`, `## E2b`, `## E5`, `## E6`. For each:
1. Goal (one sentence).
2. Exact checkpoints / data paths (verify against `checkpoints/` and `data/`; write "missing — needs training" if absent).
3. Parameter grid.
4. Per-cell protocol (seeds, epochs, metric).
5. CLI invocation — **open the relevant script (`run_learnable_gamma_compensation_gpt.py`, `train_*.py`, `run_nl_gradient_distortion_gpt.py`) and cite real flags, do not invent**.
6. Runtime estimate (RTX 5070 Ti).
7. Thesis-chapter role (one sentence: which thesis chapter this populates — architecture generalization / dataset robustness / layer localization / mechanism interaction).
8. Risks / gotchas.

Add one closing section `## Evidence Matrix` — a table with rows = experiments (E1, E1b, E2, E2b, E3, E5, E6), columns = (paper-main, paper-supp, thesis-only, priority, runtime-hours, status). This is the cut-decision table Claude will use later.

---

## What NOT to do

- Do not execute GPU. Codex owns GPU; your role stays design-only.
- Do not edit `.tex`, `.bib`, `.py`.
- Do not propose NEW training that isn't covered above; the four sub-experiments are already ambitious.
- If a checkpoint is missing, FLAG it — do not propose the training run as part of G-B.
- Do not consolidate or rename `GEMINI_E1_E2_DESIGN_20260418.md`; edit in-place.

---

## Constraint

When in doubt, bias toward listing the experiment and marking `priority=thesis-only` rather than dropping it. Bias of this dispatch is inclusion, not pruning.
