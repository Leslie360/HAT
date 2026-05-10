# Codex Review — Claude Paper-1 Broadcast + Current GPU Status

Date: 2026-05-09
Owner: Codex
Scope: Review of `BROADCAST_CLAUDE_PAPER1_MAIN_APPENDIX_REVIEW_20260509.md` and current Kimi GPU gate status.
Constraint: No figure / LaTeX / source edits in this pass because Gemini is actively working on figures.

## 1. Executive Verdict

Claude's review is mostly correct and should be treated as a real pre-submission risk list, but execution must be staged to avoid colliding with Gemini's active figure edits.

My ruling:

- Do not restructure the supplementary right now while Gemini is editing figures.
- Do fix or queue the text-only correctness issues after Gemini's figure batch stabilizes.
- Treat the ConvNeXt CIFAR-100 proportional HAT row as provenance-critical before submission.
- Treat CIFAR-100 / Flowers limitations as mandatory main-text disclosure.
- Pause the local 5-bit PCM expansion: strict seed123 has now failed the gate (<70%), so seed456/789 should not run unless Codex explicitly reopens the line.

## 2. Review of Claude Findings

### A-1 Supplementary is a Frankenstein document — AGREE, but defer large surgery

Claude is right: the current supplementary mixes PCM precision-retention, organic front-end physics, OPECT/profile fitting, legacy NL diagnostics, and remote validation in one linear document. This is confusing because the main text currently centers on PCM UnitCell precision-retention frontiers.

However, this is a structural LaTeX reorganization and will touch many figure/table placements. Because Gemini is actively editing appendix figures, do not do this now.

Recommended later fix:

1. `Supplementary Note S1: PCM Precision-Retention Evidence`
2. `Supplementary Note S2: Algorithmic HAT and Cross-Instance Robustness`
3. `Supplementary Note S3: Organic / OPECT / Front-End Extensions`
4. `Supplementary Note S4: Legacy Diagnostics and Tooling Comparisons`
5. `Supplementary Note S5: Provenance and Reproducibility`

### A-2 Garbled text at supplementary end — likely already resolved

Claude reported trailing fragments `ion.` and `n.` near the end of `supplementary.tex`. In the current working tree, the tail ends cleanly with the remote validation sentence and I do not see those fragments.

Action:

- Mark as already fixed or recheck after Gemini's next compile.
- No action required right now unless the fragments reappear in PDF/source.

### A-3 CIFAR-100 / Flowers limitation missing from main — AGREE, high priority

Claude is correct. Main text currently reads as if the method's evidence is centered on CIFAR-10, while supplementary contains much weaker or heterogeneous CIFAR-100 / Flowers evidence. This must be disclosed in Discussion/Limitations.

Preferred wording direction:

- Keep the main claim on CIFAR-10 / PCM UnitCell precision-retention.
- Say explicitly that CIFAR-100 and Flowers-102 are stress/extension evidence, not a closed generalization claim.
- Do not let the abstract imply broad dataset validity unless the main text supports it.

### A-4 ConvNeXt CIFAR-100 84.75% row — AGREE, provenance-critical

The row `ConvNeXt-Tiny Proportional-noise HAT (3-seed extension) = 84.75 +/- 0.72` while FP32 digital is `64.12` is a red flag. It may be real only if protocols differ, such as pretrained-vs-scratch, dataset split mismatch, or metric mismatch. Without clear provenance, it is dangerous.

Ruling:

- Do not submit that row as-is.
- Kimi should trace exact source JSON/log/command.
- DS should audit whether the row is same dataset, same architecture initialization, same metric, and same split.
- If provenance is not clean, replace the value with `not included / provenance pending` or move it to an exploratory note.

### B-1 8-bit noisy baseline missing from ablation chain — AGREE

The ablation table jumps from digital / zero-noise hybrid to 4-bit fixed / 4-bit ensemble, while the 8-bit noisy baseline lives in a separate table. This is logically defensible but visually confusing.

Recommended fix after figure batch:

- Add a footnote or one bridging sentence rather than expanding the table if space is tight.
- Explain that Table 1 gives the 8-bit noisy reference and Table 2 isolates the 4-bit failure boundary.

### B-2/B-3 6-bit > 8-bit and late recovery — AGREE, but wording must be conservative

Claude is right that 6-bit fresh accuracy slightly exceeds 8-bit and that the late-recovery seed456 curve is protocol-relevant. But do not oversell 6-bit as a unique sweet spot because Batch B/C/D already weakened the independent 6-bit Pareto-bridge narrative.

Recommended wording:

- `6-bit matches 8-bit within seed-level variation and shows drift-flat behavior.`
- `The small 6-bit numerical advantage should be treated as a training/regularization artifact, not as evidence that 6-bit is intrinsically superior.`
- Mention late recovery as an early-stop caution, not as a new mechanism claim.

### B-4 1 pp drift SLA — AGREE

The 1 pp threshold is currently self-defined. It should be described as a design heuristic, not an external standard, unless a citation is added.

Recommended wording:

- `we use a 1 pp 24-hour accuracy-loss threshold as a conservative reporting heuristic`.

### B-5 Sobol wording — AGREE

Claude is correct. The full-grid ADC Sobol index and restricted-domain D2D Sobol index are not directly comparable as one global decomposition. The current sentence should clarify the domain switch.

### B-6 PCM comparison cross-reference — AGREE

The table currently references `tab:retention-comparison`, which is not the right anchor for PCM drift. This should point to the PCM ladder / PCM precision tables instead.

### C-level issues — mostly valid

I agree with the broad direction:

- clarify `AIHWKit IdealDevice` terminology;
- specify 10 fresh instances x 5 MC passes in methodology;
- caveat proxy-only energy earlier;
- make single-seed vs 3-seed numbers visible enough;
- mark older NL tables as earlier diagnostics.

These are text-only and should be handled after Gemini's active figure pass.

## 3. Current GPU Gate Status: 5-bit Strict seed123 Failed Continue Criterion

Kimi appears to have run the strict 5-bit seed123 gate already, although I have not seen a formal Kimi report yet.

Observed files:

- `paper2_aihwkit_baseline/checkpoints/r11d_5bit_pcm_strict_seed123/training_history.json`
- `paper2_aihwkit_baseline/checkpoints/r11d_5bit_pcm_strict_seed123/fresh_eval.json`
- `paper2_aihwkit_baseline/checkpoints/r11d_5bit_pcm_strict_seed123/drift_eval.json`
- logs under `paper2_aihwkit_baseline/logs/r11d_5bit_pcm_strict_seed123_*`

Observed metrics:

| Metric | Value |
|---|---:|
| PCM preset | PCMPresetUnitCell |
| Best test/source | 63.26% |
| Fresh mean | 63.44 +/- 0.07% |
| Drift 0s | 63.36% |
| Drift 1h | 62.25% |
| Drift 1d | 60.84% |
| 0s -> 1d drop | 2.52 pp |

Interpretation:

- Metadata/drift path is now physically meaningful; this fixed the old baseline-script contamination.
- But performance is far below the 4/6/8-bit PCM ladder (~76-78%).
- It fails the dispatch gate: `If best test is below 70%, do not run 5-bit seed456/789 yet.`

Codex ruling:

- Pause 5-bit seed456/789 strict expansion.
- Kimi should write the formal report `KIMI_GPU_5BIT_PCM_STRICT_RESULT_20260508.md` with exact commands and JSON paths.
- DS should inspect whether 5-bit low accuracy is expected from AIHWKit quantization semantics or a script/config issue.
- Until DS clears a config bug, 5-bit should be treated as `KILL / non-frontier`, not as a new precision-ladder point.

## 4. Execution Order I Recommend

While Gemini is working on figures, do not touch figure files or major LaTeX structure. Use this order:

1. Kimi: formalize strict 5-bit seed123 report and pause seed456/789.
2. DS: audit strict 5-bit config vs 4/6/8-bit configs.
3. Kimi: verify ConvNeXt CIFAR-100 84.75 provenance.
4. After Gemini's current figure batch: apply text-only fixes A-3, B-4, B-5, B-6, C-1/C-2/C-3.
5. Only after figure layout stabilizes: consider A-1 supplementary section reorganization.

## 5. No-Conflict Rule During Gemini Figure Work

Until the user says Gemini's current figure batch is stable:

- Do not edit `paper/latex_gpt/figures/`.
- Do not regenerate `main.pdf` or `supplementary_main.pdf` unless requested.
- Do not reorder figures/tables.
- Text-only review and report files are safe.
