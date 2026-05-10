# BROADCAST: Energy Numbers Over-Precision Issue

**Date:** 2026-04-18
**Reporter:** Claude (on user request)
**Status:** ⚠️ ACTIVE — needs manuscript patch before submission
**Scope:** `paper/latex_gpt/sections/03_methodology.tex`, `paper/latex_gpt/sections/06_discussion.tex`

---

## Problem Statement

The manuscript presents first-order energy estimates with **excessive numerical precision**, creating a false impression of measurement accuracy. Reviewers have already flagged this (see `report_md/审稿人意见from_model.md` multiple entries).

| Current Text | Issue |
|:--|:--|
| "87.7% of parameters are assigned to analog execution" | Exact percentage from one model profiling run; no error bar |
| "57.9% of the estimated energy remains in the digital domain" | Same — exact percentage from placeholder constants |
| "11.45× dense-projection energy reduction versus FP32" | Two-decimal precision for a first-order analytical model |
| "reduced to 9.90–11.10× after 10–50% routing overhead" | Overly precise interval endpoints |
| "273.94 µJ" (in dry-run report, not currently in main text) | Four significant digits for a placeholder model |

**Why this is dangerous:**
- Reviewer #4 (W1/W7) explicitly criticized: "energy estimates (273.94 µJ, 11.45× gain) are presented as point values without uncertainty ranges"
- Another reviewer: "The 11.45× energy reduction figure is eye-catching but must be interpreted with extreme caution... The paper is transparent about this limitation in Section 6.6, but the abstract and conclusion use the 11.45× figure without caveat"
- Exact decimals signal "measured" rather than "estimated"; first-order models should use rounded figures or ranges

---

## Root Cause

The numbers come from `EnergyProfiler` in `analog_layers.py`, which multiplies operation counts by placeholder constants (e.g., `E_analog_MAC = 100e-15 J`, `E_digital_INT8_MAC = 0.4e-12 J`). These constants are:
- **Not measured** from organic devices
- **Not validated** against any circuit simulation
- **Analytical placeholders** for relative comparison only

Presenting their product to 2-4 significant figures is a category error.

---

## Proposed Fix

### Strategy: Round to 1-2 significant figures; add explicit qualifier on first use

| Location | Current | Proposed |
|:--|:--|:--|
| `03_methodology.tex:10` | "87.7% of parameters are assigned to analog execution, whereas 57.9% of the estimated energy remains in the digital domain" | "**~88%** of parameters are assigned to analog execution, whereas **~58%** of the estimated energy remains in the digital domain" |
| `06_discussion.tex:38` | "A first-order energy model projects an 11.45× dense-projection energy reduction versus FP32, reduced to 9.90–11.10× after 10–50% routing overhead. Digital attention still dominates total energy (57.9%)." | "A first-order energy model projects an **~11×** dense-projection energy reduction versus FP32, reduced to **~10–11×** after 10–50% routing overhead. Digital attention still dominates total energy (**~60%**)." |

### Rationale for each rounding:

| Original | Rounded | Sig Figs | Justification |
|:--|:--|:--:|:--|
| 87.7% | ~88% | 2 | Model profiling is deterministic (parameter count), but "analog-mapped" definition has mapping-policy uncertainty |
| 57.9% | ~58% or ~60% | 2 | Energy is entirely placeholder-based; ±20% parameter variation would shift this meaningfully |
| 11.45× | ~11× | 2 | FP32 comparison baseline itself is a rough GPU estimate, not a measured chip |
| 9.90–11.10× | ~10–11× | 2 | Interconnect overhead range (10–50%) is itself a guess; endpoints are spuriously precise |
| 273.94 µJ | ~270 µJ or ~0.27 mJ | 2 | Already not in main text; if ever cited, round aggressively |

---

## Additional Hardening

1. **First-use qualifier in Methodology:** Add a short clause on the first energy mention:
   > "...whereas ~58% of the estimated energy remains in the digital domain **under the present placeholder constants**, largely because of attention operations."

2. **Discussion reinforcement:** Keep the existing "These are system-level upper bounds under placeholder constants, not chip-predictive estimates" sentence — it is already reviewer-safe.

3. **Cover letter:** Already safe — uses "first-order system-level upper bounds prior to routed-chip implementation". No change needed.

4. **Supplementary:** The `tinyvit_hybrid_dryrun_report_gpt.md` can keep exact numbers as internal engineering notes, but any reference from `.tex` to it should use rounded figures.

---

## Risk if not fixed

- Reviewer will flag as "misleading precision" or "false accuracy"
- Energy claims — already a reviewer pressure point — become easier to attack
- Undermines the otherwise honest "upper bound / placeholder" framing in Discussion

---

## Action Items

| # | Action | Owner | File |
|:--|:--|:--|:--|
| 1 | Round energy numbers in Methodology + Discussion | Claude | `03_methodology.tex`, `06_discussion.tex` |
| 2 | Add placeholder-constant qualifier on first use | Claude | `03_methodology.tex` |
| 3 | Recompile and verify page count | Claude | `main.pdf` |
| 4 | Update provenance audit if numbers change | Codex (later) | `PROVENANCE_AUDIT_20260418.md` |

---

**Recommended urgency:** High. This is a quick fix that preempts a likely reviewer complaint.
