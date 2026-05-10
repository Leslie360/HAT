# Pedagogical Critique: `tutorial_compute_vit.ipynb`

**Reviewer:** Code Agent (Task G-FF16)
**Date:** 2026-04-21
**Word count:** ~480

---

## 1. Prerequisites
**Score: 3 / 5**
The intro lists PyTorch, torchvision, `timm`, and the repo on `PYTHONPATH`, but omits assumed knowledge of dataclasses, checkpoint serialization, and basic conductance-array concepts.
*Fix:* Add a "What you should already know" box covering Python dataclasses and a one-sentence definition of D2D/C2C noise.

## 2. Pacing
**Score: 2 / 5**
The notebook claims completion in ≤30 minutes, yet Sections 4 and 5 each run 10 fresh instances × 5 eval runs (50 full passes), and Section 6.5 adds 20 more—far exceeding 30 min on a typical CPU or single-GPU workstation.
*Fix:* Reduce the default `fresh_instances` to 3 and `eval_runs` to 2, with a callout box showing how to scale up for paper-grade reproduction.

## 3. The negative-result section (30 % ceiling)
**Score: 2 / 5**
Section 6.5 never states the ~30 % ceiling explicitly; it describes the gap as "about a third" without upfront numbers and offers only a single cryptic sentence on interpretation ("structural limit in the attention pathway"). A beginner will not grasp *why* nonlinearity matters or why this result is important.
*Fix:* State the ceiling value in the section header, add a 2-sentence intuition for write nonlinearity, and explain the implication ("analog attention layers may be impractical beyond NL≈1.5").

## 4. Code quality
**Score: 3 / 5**
The `Path(__file__)` idiom in Cell 1 crashes in Jupyter because `__file__` is undefined in notebook kernels. Hard-coded relative paths (`../checkpoints/`) assume a specific working directory. Placeholder-like snippets (e.g., `weights_only=False` without security warning) are present.
*Fix:* Replace `Path(__file__)` with `Path.cwd()`, wrap checkpoint paths in existence checks with informative `FileNotFoundError` messages, and add a comment explaining `weights_only=False`.

## 5. Missing sections
**Score: 2 / 5**
There is no troubleshooting guide, FAQ, glossary, expected runtime per cell, or guidance for users lacking the paper-locked checkpoints. Advanced topics (custom noise distributions, multi-device ensembles) are absent.
*Fix:* Append a "Troubleshooting & FAQ" cell covering missing checkpoints, CUDA OOM mitigation, and a 10-term glossary (D2D, C2C, HAT, NL, OPECT, etc.).

## 6. Accessibility
**Score: 3 / 5**
The tone is conversational and welcoming ("Here is the **mistake** most ML engineers make"), but jargon is introduced without inline definitions—e.g., "OPECT," "fresh instance," and "Ensemble HAT" appear before they are fully unpacked. Non-hardware ML engineers may feel excluded.
*Fix:* Add parenthetical definitions on first use and a "Jargon cheat-sheet" tooltip-style markdown cell.

---

## Final Verdict

**Needs revision — see items above.**

The tutorial has a strong narrative arc and a compelling visual payoff, but pacing overruns, missing guard-rails for beginners, and technical brittleness (`__file__`, hard-coded paths) prevent it from being release-ready without moderate revision.
