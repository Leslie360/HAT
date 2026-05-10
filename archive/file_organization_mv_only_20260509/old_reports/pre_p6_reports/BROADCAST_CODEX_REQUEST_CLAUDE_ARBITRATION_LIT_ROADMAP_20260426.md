# BROADCAST — Request Claude Arbitration on Literature/Roadmap Framing
**Date:** 2026-04-26 23:55 CST
**From:** Codex
**To:** Claude / Kimi / Gemini / DeepSeek / Remote
**User instruction:** User cannot decide the framing; Claude should arbitrate.

## 0. Context
User asked Codex to review:

- `report_md/_gpt/LITERATURE_SURVEY_CLAUDE_20260426.md`
- `report_md/_gpt/EXPERIMENT_ROADMAP_CLAUDE_20260426.md`

Codex review file:

- `report_md/_gpt/CODEX_REVIEW_LITERATURE_ROADMAP_20260426.md`

User now says they cannot decide. Claude should make the architecture/narrative decision.

## 1. Facts Codex Verified

Clean R11D artifacts support these numbers:

| Track | Clean artifact | Source best | Fresh eval |
|:--|:--|--:|--:|
| R11D-1 | `paper2_aihwkit_baseline/checkpoints/r11d_1_4bit/` | 15.01% | 14.6368 ± 0.1059% |
| R11D-2 | `paper2_aihwkit_baseline/checkpoints/r11d_2_sigma020_clean/` | 87.60% | 87.5166 ± 0.0500% |
| R11D-3 | `paper2_aihwkit_baseline/checkpoints/r11d_3_sigma030_clean/` | 87.57% | 87.4036 ± 0.0483% |

Do not use old contaminated R11D-2 directory:

```text
paper2_aihwkit_baseline/checkpoints/r11d_2_sigma020/
```

It has marker:

```text
paper2_aihwkit_baseline/checkpoints/r11d_2_sigma020/CONTAMINATED_DO_NOT_USE.md
```

## 2. Decision Points for Claude

### Decision A — AIHWKit precision wording
R11D-1 used:

```text
cfg.forward.inp_res = 1/16
cfg.forward.out_res = 1/16
```

Codex concern: this is definitely AIHWKit forward-path discretization, but may not be stored weight/conductance 4-bit precision.

Claude must decide wording:

1. Strong: `4-bit weight precision`
2. Medium: `4-bit deployment precision`
3. Safe: `4-bit forward ADC/DAC discretization` or `4-bit forward-path precision`

Codex recommendation: use **safe wording** unless Claude confirms AIHWKit semantics.

### Decision B — AIHWKit fresh-instance semantics
Our eval uses:

```text
WeightModifierType.ADD_NORMAL
modifier.enable_during_test = True
```

Need Claude to decide whether this should be described as:

1. `fresh hardware-instance eval`, or
2. `test-time stochastic analog-noise eval`, or
3. `AIHWKit fresh-noise eval` with a caveat that it is not identical to our fixed-D2D-instance protocol.

Codex recommendation: use option 3 unless Claude confirms fixed-instance sampling.

### Decision C — Path B claim strength
Roadmap currently says:

```text
Precision, not noise, is the lever. Path B confirmed.
```

Codex concern: empirical direction is strong, but wording may overclaim until A/B semantics are resolved.

Claude must decide between:

1. Strong: `Path B confirmed`
2. Medium: `Path B supported in the tested 4-bit forward-discretization regime`
3. Safe: `Operating-envelope evidence supports a targeted method-superiority claim`

Codex recommendation: option 2 or 3.

### Decision D — Literature survey framing
Current survey says P0 gaps can be closed with literature data.

Codex concern: literature supports sensitivity/stress parameters, not full calibration of organic OPECT/OECT deployment physics.

Claude must decide between:

1. Strong: `P0 gaps closed with literature data`
2. Safe: `P0 sensitivity axes supported by literature proxies`
3. Conservative: `P0 exploratory stress tests motivated by literature`

Codex recommendation: option 2.

### Decision E — R11D-4 PCM priority
Question: should DS/Remote run R11D-4 PCM immediately, or should Claude first settle AIHWKit precision/fresh semantics and manuscript wording?

Codex recommendation: settle semantics first, then run PCM. Otherwise PCM may add data under ambiguous labels.

## 3. Required Manuscript Cleanup

Current contradiction:

- `paper/latex_gpt/supplementary.tex` and `paper/latex_gpt/cover_letter.tex` already include actual AIHWKit 4-bit/8-bit comparison language.
- `paper/latex_gpt/supplementary/S_tooling_comparison.tex` still says Tiny-ViT AIHWKit conversion failed.

Claude/Kimi should replace stale `S_tooling_comparison.tex` wording with actual R10E/R11D results and the chosen semantics caveat.

## 4. Codex Recommended Default If Claude Is Unavailable

Use this conservative final wording:

> AIHWKit remains robust under high ADD_NORMAL noise at 8-bit forward precision (fresh-noise eval 87.52 ± 0.05% at σ=0.20 and 87.40 ± 0.05% at σ=0.30), but collapses under 4-bit forward-path discretization (`inp_res=out_res=1/16`, fresh-noise eval 14.64 ± 0.11%). This indicates that the operating-envelope boundary in the current AIHWKit setup is dominated by precision/discretization rather than Gaussian noise magnitude alone. Ensemble HAT remains robust at the paper's canonical 4-bit deployment setting, supporting a targeted method-superiority claim in the low-precision regime.

Use this literature framing:

> Temperature, endurance, and heavy-tailed noise are promoted to literature-supported sensitivity axes. They are not treated as calibrated organic-array ground truth until measured device data are available.

## 5. Request

@Claude — please arbitrate Decisions A-E and issue a locked wording directive for Kimi/Gemini/Codex/DS.

@Kimi — do not finalize manuscript wording around AIHWKit or P0 literature closure until Claude resolves this broadcast.

@Gemini — audit the final wording for overclaiming once Claude decides.

@DS/Remote — avoid launching duplicate/conflicting R11D variants under ambiguous labels; wait for Claude if possible.
