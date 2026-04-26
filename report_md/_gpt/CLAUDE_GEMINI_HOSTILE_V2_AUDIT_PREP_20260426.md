# Gemini Hostile-V2 Audit Prep — Evidence Package
**Date:** 2026-04-26 05:00 CST
**Author:** Claude (Chief Architect)
**Purpose:** Pre-assemble all R9/R10 evidence for Gemini's Day-6 hostile-v2 substantive audit per `DISPATCH_GEMINI_HOSTILE_REVIEW_V2_SPEC_20260425.md`

---

## 1. Eleven Concerns → Closure Status

| # | Concern | R10 Track | Status | Evidence | Verdict |
|:--|:--|:--|:--|:--|:--|
| A1 | 86.37% headline single-seed | R10A | **CLOSED** | 3-seed aggregate `86.16 ± 0.19%` (10 fresh × 5 MC per seed) | Multi-seed canonical replaces single-seed headline |
| A2 | Standard HAT 10% mechanism | R10B | **CLOSED** | Deterministic single-class predictor: entropy≈0, max-class freq=100% | Mechanism is mode-collapse, not noise dispersion |
| A3 | OPECT distribution missing | R10C | **CLOSED** | QQ/AD/kurtosis analysis; distribution shape unknown but parameter-shifted | Honest disclosure: shape invariance not proven, only parameter-shift robustness |
| B1 | Standard vs Ensemble compute parity | — | **CLOSED by design** | Per-epoch resampling cost documented in §3 methodology | Acknowledged as modest overhead (~1.3× epoch time) |
| B3 | Ensemble seed variance ±0.47% suspicious | folded into R10A | **CLOSED** | 3-seed std = 0.19% (seed-means); pooled std = 1.52% (instance-means) | Variance is instance-level, not seed-level; 0.19% is healthy |
| C1 | Tobin novelty contrast missing | R10G | **CLOSED** | §2.1 novelty paragraph distinguishes i.i.d. domain-randomization vs structured D2D-map resampling | Explicitly acknowledges Tobin link then downgrades it |
| C2 | "1.5 scenarios not 3" | R10I | **CLOSED** | Cover letter + §6.2 reframed: "canonical evaluation + zero-shot transfer + severe-NL stress" | Independence claims removed |
| D1 | Framework framing too thin | R10F + R9C-D1 | **CLOSED** | Freshness audit finds zero direct prior art; D1 defense paragraph in §6.5 | Framing as "risk-ranking before fabrication" is established |
| D2 | AIHWKit baseline absent | R10E | **OPEN** | Not yet started; GPU idle, ready to launch | Head-to-head number pending |
| D3 | Energy ε provenance murky | R10H + R9C-D3 | **CLOSED** | `E_cell=100fJ` has Gebregiorgis anchor; ADC/DAC are order-of-magnitude estimates honestly labeled | D3 defense paragraph in §6.5 |
| E3 | 5pp severe-NL "recipe not floor" no evidence | R10D + R9C-D2 | **CLOSED** | NL interpolation shows gradual degradation 1.0→1.2→1.5→1.8→2.0 | Monotonic trend supports training-recipe framing |

**Closure rate:** 10/11 closed. Only D2 (R10E AIHWKit) remains open.

---

## 2. Per-Concern Evidence Files

### A1 — R10A Multi-Seed
- `report_md/_gpt/json_gpt/r10a_canonical_ensemble_hat_3seed_fresh_eval.json`
- `report_md/_gpt/json_gpt/r10a_seed456_fresh_eval.json`
- `report_md/_gpt/json_gpt/r10a_seed789_fresh_eval.json`
- `report_md/_gpt/CODEX_R10A_FINAL_INTEGRATION_REPORT_20260426.md`

### A2 — R10B Collapse Mechanism
- `report_md/_gpt/json_gpt/r10b_standard_hat_class_distribution.json`
- `paper/latex_gpt/figures/figS_standard_hat_collapse_mechanism.pdf`
- `report_md/_gpt/CODEX_R10B_CANONICAL_MECHANISM_REPORT_20260426.md`

### A3 — R10C OPECT Distribution
- `report_md/_gpt/KIMI_R10C_OPECT_DISTRIBUTION_REPORT_20260425.md`
- `report_md/_gpt/json_gpt/literature_profile_eval.json` (88.53% anchor)

### B1/B3 — Compute / Variance
- §3 methodology (Ensemble HAT implementation details)
- R10A aggregate JSON (cross-seed stats)

### C1 — R10G Novelty
- `report_md/_gpt/KIMI_R10G_NOVELTY_CONTRAST_20260425.md`
- `paper/latex_gpt/sections/02_related_work.tex` (landed paragraph)

### C2 — R10I Scenarios
- `report_md/_gpt/KIMI_R10I_SCENARIOS_REFRAMING_20260425.md`
- `paper/latex_gpt/cover_letter.tex`
- `paper/latex_gpt/sections/06_discussion.tex`

### D1 — R10F Framing
- `report_md/_gpt/KIMI_R10F_LITERATURE_FRESHNESS_AUDIT_20260425.md`
- R9C-D1 paragraph in §6.5

### D2 — R10E AIHWKit (OPEN)
- No evidence yet — this is the single remaining open concern

### D3 — R10H Energy
- `report_md/_gpt/KIMI_R10H_ENERGY_PROVENANCE_REPORT_20260425.md`
- R9C-D3 paragraph in §6.5

### E3 — R10D NL Interpolation
- `report_md/_gpt/json_gpt/r10d_nl_interpolation_summary.json`
- `report_md/_gpt/json_gpt/r10d_nl1.2_fresh_eval.json`
- `report_md/_gpt/json_gpt/r10d_nl1.5_fresh_eval.json`
- `report_md/_gpt/json_gpt/r10d_nl1.8_fresh_eval.json`
- `report_md/_gpt/CODEX_R10D_NL_INTERPOLATION_REPORT_20260426.md`
- §5.7 interpolation paragraph + supplementary Table~\ref{tab:r10d-nl-interpolation}

---

## 3. Manuscript Compile Status

| File | Pages | Status |
|:--|:--|:--|
| `main.pdf` | 16 | RC 0, 2 minor overfull hbox (<3pt, non-blocking) |
| `supplementary_main.pdf` | 37 | RC 0, 1 minor overfull hbox (<3pt, non-blocking) |
| `cover_letter.pdf` | 2 | RC 0 |

**LaTeX health:** zero undefined references, zero multiply-defined citations.

---

## 4. Remaining Risks for Gemini to Probe

Even with 10/11 concerns closed, the following angles remain vulnerable:

1. **R10E AIHWKit gap:** If R10E shows AIHWKit ≥ Ensemble HAT, the head-to-head novelty claim in R10G collapses.
2. **8×40GB cross-arch:** If remote results show TinyImageNet-scale failure, the "CIFAR-only" attack revives.
3. **Measured-D2D partner delay:** If partner data is >2 months away, Nat Elec experimental bar becomes harder to defend.
4. **R10A seed 789 variance:** Fresh std = 1.94% for seed 789 vs 0.72% for seed 456. Pooled std = 1.52%. A hostile reviewer could ask why seed 789 is noisier.
5. **R10D monotonicity:** Source accuracy is not monotone (83.12 → 82.81 → 82.77), though fresh-instance is. A careful reviewer could flag this.

---

## 5. Audit Trigger

This package is ready for Gemini hostile-v2 audit. Trigger when:
- R10E closes (preferred — full 11/11 closure)
- OR user explicitly requests early audit with D2 flagged as pending

---

## 6. One-Line

10 of 11 substantive concerns are closed with traceable evidence. Only R10E AIHWKit head-to-head remains open. Manuscript compiles clean. Package ready for Gemini hostile-v2 audit upon R10E completion or user directive.
