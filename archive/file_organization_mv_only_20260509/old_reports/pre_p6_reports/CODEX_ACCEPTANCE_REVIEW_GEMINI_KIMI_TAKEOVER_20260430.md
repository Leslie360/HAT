# Codex Acceptance Review — Gemini Takeover Of Kimi Tasks

Date: 2026-04-30 CST
Reviewer: Codex
Scope:

- `report_md/_gpt/GEMINI_R11D_PRECISION_LADDER_TABLES_20260430.md`
- `report_md/_gpt/GEMINI_HOSTILE_REVIEW_PASS_20260430.md`
- `report_md/_gpt/PAPER1_RESULTS_SPINE_20260430.md`
- `report_md/_gpt/PAPER1_SUPPLEMENTARY_INFO_20260430.md`

Verdict: **conditional pass, not final-text acceptance**.

Gemini correctly adopted the final architecture: pure 4-bit failure + Ensemble HAT rescue + PCM 4/6/8-bit precision ladder; 105 non-blocking; 107 Work-2. However, several line-level issues must be corrected before this can be integrated into paper text.

## Findings

### High — Wrong provenance seeds in Gemini precision-ladder provenance table

File: `report_md/_gpt/GEMINI_R11D_PRECISION_LADDER_TABLES_20260430.md`
Lines: 25-33

Issue:

The provenance table lists 8-bit seed `42` and 4-bit seed `42`, while the canonical 3-seed set is `123/456/789` for both 8-bit and 4-bit UnitCell. The actual canonical source is:

- `report_md/_gpt/R11D_FINAL_3SEED_SUMMARY_20260429.md`, lines 12-17.
- `report_md/_gpt/CODEX_LOCAL_R11D_6BIT_CORRECTED_FINAL_20260430.md`, lines 17-21.

Impact:

This can cause wrong checkpoint/path citation in SI and corrupt reproducibility claims.

Required fix:

Replace the provenance table with the corrected version already used in `PAPER1_SUPPLEMENTARY_INFO_20260430.md`, lines 42-52.

### Medium — Main Results overstates 6-bit as “optimal tradeoff”

File: `report_md/_gpt/PAPER1_RESULTS_SPINE_20260430.md`
Line: 31

Issue:

The sentence says 6-bit “provides the optimal tradeoff”. This exceeds the final ruling. We can call 6-bit the best tested Pareto midpoint in the tested PCM UnitCell regime, not globally optimal for PCM crossbars.

Required replacement:

```text
In the tested PCM UnitCell setting, 6-bit is the best observed Pareto midpoint: it maintains 8-bit-like drift stability while achieving comparable fresh accuracy. We therefore treat 6-bit as the recommended tested operating point, rather than a globally optimal precision.
```

### Medium — “Late-recovery mechanism inherent to PCM-preset simulations” is causal overreach

Files:

- `report_md/_gpt/GEMINI_R11D_PRECISION_LADDER_TABLES_20260430.md`, line 19.
- `report_md/_gpt/PAPER1_SUPPLEMENTARY_INFO_20260430.md`, line 36.

Issue:

The text calls late recovery an “inherent” mechanism of PCM-preset simulations. We observed late recovery in one corrected 6-bit seed under the full schedule; we did not prove an inherent PCM mechanism.

Required replacement:

```text
Complete 100-epoch training shows late recovery in this 6-bit seed, reaching 78.49%. All canonical precision-ladder results therefore use the matched full 100-epoch schedule to avoid early-stop artifacts being mistaken for physical instability.
```

### Medium — AIHWKit / IdealDevice semantics too strong

File: `report_md/_gpt/PAPER1_RESULTS_SPINE_20260430.md`
Line: 5

Issue:

The draft describes AIHWKit `IdealDevice` as “noise-free forward pass during training” with “realistic hardware noise during deployment evaluation.” That is too loose and risks AIHWKit semantics criticism. Safer wording should avoid claiming physical realism for IdealDevice deployment noise.

Required replacement:

```text
We first establish the behavior of the tested AIHWKit IdealDevice quantization/noise baseline. At 8-bit precision the baseline remains stable, achieving 87.28 ± 0.13% fresh-instance accuracy; at 4-bit precision it collapses to 14.64 ± 0.11%.
```

### Low/Medium — “Tape-out constraints” phrase invites physical-measurement attack

Files:

- `report_md/_gpt/PAPER1_RESULTS_SPINE_20260430.md`, line 13.
- `report_md/_gpt/GEMINI_HOSTILE_REVIEW_PASS_20260430.md`, line 10.

Issue:

“Physical tape-out constraints” is not needed and invites a reviewer to ask for silicon measurements. The final ruling only permits deployment-frontier phrasing.

Required replacement:

```text
The results reveal a precision-retention deployment frontier for the tested PCM simulation regime.
```

### Low — “No forbidden claims remain” is too broad

File: `report_md/_gpt/GEMINI_HOSTILE_REVIEW_PASS_20260430.md`
Line: 22

Issue:

The hostile review says no forbidden claims remain, but related draft files still contain over-strong phrases flagged above. The hostile review should say “the proposed replacement table avoids forbidden claims,” not that all current text is clean.

Required replacement:

```text
The replacement phrasings above avoid the forbidden claims, but downstream Results/SI drafts still require line-level wording cleanup before integration.
```

## What Passed

- Correct global architecture: paper-1 is local, not 105/107-driven.
- Correct main numeric table for 4/6/8-bit means.
- Correct decision to place 6-bit late recovery in SI plus one main-text sentence.
- Correct exclusion of 107 details from paper-1.
- Correct caution that proportional HAT does not universally beat digital baselines.

## Required Actions Before Integration

1. Patch the provenance table in `GEMINI_R11D_PRECISION_LADDER_TABLES_20260430.md`.
2. Patch over-strong wording in `PAPER1_RESULTS_SPINE_20260430.md` and `PAPER1_SUPPLEMENTARY_INFO_20260430.md`.
3. Re-run a quick forbidden-claim grep over all four deliverables.
4. Only after the above, treat the drafts as acceptable inputs for LaTeX integration.

## Acceptance Status

Current status: **conditionally accepted for direction, rejected for final text until line-level fixes land**.
