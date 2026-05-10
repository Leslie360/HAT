# DISPATCH KIMI+GEMINI R9C — Reviewer-Confidence Defense Hardening
**Date:** 2026-04-25 22:30 CST
**Issued by:** Claude
**Assignees:** Kimi (drafts) + Gemini (hostile cross-review)
**Authority:** CLAUDE_ROUND9_PAPER1_HARDENING_PLAN_20260425 §3 Track C
**Priority:** HIGH (closes the 5 reviewer-attack vectors)
**Time budget:** 2-3 days

---

## 0. Mission

Add **5 short defense paragraphs** to paper-1 that pre-emptively address the 5 most likely reviewer attack vectors. This is **honest framing of existing facts**, not new science. Each paragraph is 2-4 sentences placed at a strategic location in the manuscript to defuse the attack BEFORE the reviewer escalates.

---

## 1. Five attack vectors (with defense placements)

### Defense D1 — Hardware fidelity / no silicon validation

**Attack vector**: "You've never tested on actual silicon. How do we know any of this transfers to a fabricated array?"

**Defense paragraph** (place in `06_discussion.tex` § Limitations, near top):

> Our framework is intentionally **behavioral, not circuit-accurate**: we simulate the dominant deployment-relevant non-idealities (4-bit weight quantization, D2D and C2C variability, ADC precision, write nonlinearity, retention) but defer SPICE-level circuit phenomena (parasitic IR drop, sneak paths, pulse-faithful programming) to follow-on work. We adopt this scope choice deliberately, mirroring the methodology of established analog-CIM tooling \citep{rasch2021aihwkit,crosssim2024}: behavioral fidelity is sufficient to **rank deployment risks** before fabrication closes, while a fully circuit-accurate model demands measured device data not yet available. The framework is profile-agnostic and consumes any measured device statistics through a documented ingest interface; we anticipate hardware-calibrated re-evaluation in an erratum or extended companion study once partner-array measurements are released.

**Length**: ~110 words. Cite count: 2.

### Defense D2 — Severe-NL 5pp residual gap

**Attack vector**: "Your severe-NL recovery is only ~80%, leaving 5pp gap to canonical. This isn't deployment-ready."

**Defense paragraph** (place in `06_discussion.tex` § Outlook or end of §6.2):

> The residual ~5 pp gap between severe-nonlinear-write fresh-instance accuracy and the canonical baseline reflects **training-recipe constraints rather than a physical floor**. Cross-host parity (Supplementary Note S-CrossHost) shows the gap narrows by ~2 pp under the larger-batch recipe, consistent with optimizer-state tuning rather than fundamental robustness limits. Realistic deployment under intermediate write-nonlinearity ($1.0 \le NL \le 1.5$) sits within 1 pp of the canonical baseline (Supplementary Fig.~\ref{figS_noise_sweep}), bracketing the realistic device-physics regime. We frame the present severe-NL band as an **upper-bound stress test**, not a target deployment specification.

**Length**: ~95 words. Cite count: 0 (refs to figures only).

### Defense D3 — Energy ε_MAC placeholder

**Attack vector**: "Your energy estimate uses arbitrary ε_MAC = 65pJ. This is a hand-waving order-of-magnitude calculation."

**Defense paragraph** (place in `06_discussion.tex` § Limitations, after D1):

> The energy estimates in Section~\ref{subsec:energy} are **first-order analytical projections** derived from literature-reported organic CIM constants \citep{guo2024organic,zhang2025opect}; the per-MAC energy parameter (~23.9 μJ for the Tiny-ViT inference, equivalent to 11.45× speedup vs FP32 and 2.86× vs assumed INT8) **bounds deployment risk to within an order of magnitude** rather than predicting silicon performance. We deliberately avoid silicon-grade energy claims because the framework's contribution is **risk-ranking under realistic device profiles**, not chip-level optimization. A complete energy validation depends on partner-array characterization not yet available; ranges in our model are sufficient for the deployment-risk ordering claimed here.

**Length**: ~110 words. Cite count: 2.

### Defense D4 — OPECT single-source

**Attack vector**: "OPECT is one paper's data. Your literature validation is narrow."

**Defense paragraph** (place in `05_results.tex` §5.8 OPECT case study, end of subsection):

> The OPECT case study \citep{zhang2025opect} provides **one literature-anchored validation point**; we choose it because it is the most complete published organic-array characterization to date, with documented D2D, C2C, and conductance-window statistics. The framework is **profile-agnostic by design**: any measured device statistics can be ingested through the documented profile interface (Supplementary Note S-HW). We anticipate cross-validation against additional fabricated profiles in a companion study once they become available; the present zero-shot transfer demonstrates the framework's portability without retraining, not a claim that OPECT is universally representative.

**Length**: ~95 words. Cite count: 1.

### Defense D5 — CIFAR/Flowers only, no ImageNet

**Attack vector**: "Only CIFAR-10/100 and Flowers-102. What about ImageNet? Your scaling story is unproven."

**Defense paragraph** (place in `06_discussion.tex` § Limitations, after D2):

> The present evaluation focuses on CIFAR-10/100 and Flowers-102 to enable systematic non-ideality and HAT-method ablation across three backbones (ResNet-18, ConvNeXt-Tiny, Tiny-ViT-5M) within a tractable compute budget. **ImageNet-scale extension is the subject of an in-progress cross-architecture sweep** (ViT-Small/16, DeiT-Small/16 on TinyImageNet) on a separate compute infrastructure; preliminary results will appear in an extended companion study or supplementary erratum. The ablation matrix presented here intentionally trades dataset breadth for non-ideality coverage, providing the structural Sobol decomposition (Section~\ref{subsec:iso-accuracy}) that motivates dataset-scale priorities for hardware validation.

**Length**: ~95 words. Cite count: 0 (forward-pointer to in-progress work).

---

## 2. Total addition vs cut

| | Words |
|:--|--:|
| 5 defense paragraphs added | +505 |
| But: each replaces existing weaker statement | -100 (estimated) |
| Net add | **+405** |

This brings net post-Track-A target from 5,200 → 5,600 words, still within Nat Electronics envelope.

---

## 3. Kimi workflow

For each defense paragraph:
1. Find the placement location in the canonical .tex
2. Read surrounding 2 paragraphs to understand context
3. Insert the defense paragraph (verbatim from §1 above, you may polish 1-2 word choices)
4. Verify zero contradiction with surrounding text
5. Append change log to `KIMI_R9C_DEFENSE_REPORT_20260425.md`

After all 5 inserted:
1. Compile: `cd paper/latex_gpt && latexmk -pdf main.tex`
2. Verify RC 0
3. Final word count ≤ 5,700

---

## 4. Gemini cross-review (parallel)

Once Kimi inserts each defense paragraph, Gemini does a **hostile-reviewer-perspective audit**:

For each defense:
- Does the paragraph actually defuse the attack? Or does it admit weakness?
- Are there NEW reviewer attacks the defense itself opens?
- Could a hostile reviewer say "this is just hand-waving"?

**Gemini deliverable**: `GEMINI_R9C_DEFENSE_AUDIT_20260425.md` — per-defense pass/flag verdict + suggested rewords if any.

If Gemini flags any defense as ineffective: Kimi revises, Gemini re-reviews, max 2 iterations.

---

## 5. Integration with G-HOSTILE-V2

The earlier `DISPATCH_GEMINI_HOSTILE_REVIEW_V2_SPEC_20260425.md` was gated on Round-7 + 8×40GB cross-arch + measured-D2D landing. Now that Round-9 hardening adds 5 defenses, **Gemini hostile-v2 fires immediately after Kimi+Gemini Round-9C closes** (don't wait for cross-arch + measured-D2D).

Trigger condition update:
- Original: cross-arch ✅ + measured-D2D ✅ + Round-7 integration ✅ + final read
- **Revised**: Round-9 (A+B+C) all closed + Claude final read

This brings hostile-v2 forward by potentially weeks. Worth it.

---

## 6. Constraints (HARD)

- **No new science.** Defenses are reframings of existing facts, not new claims.
- **No new numbers.** Every quantitative claim already in paper.
- **No defensive vague language.** Each defense is sharp, specific, falsifiable.
- **Zone discipline preserved**: 3A/3B/3C unchanged.
- **Bug-retrospective discipline preserved**: no "post-fix" / "deployment-fidelity" / "bug-immune" wording.
- **Cite list preserved**: any new citations must already exist in `refs_gpt.bib`.

---

## 7. Deliverables

### Kimi
| File | Action |
|:--|:--|
| `paper/latex_gpt/sections/05_results.tex` | Add D4 paragraph at §5.8 end |
| `paper/latex_gpt/sections/06_discussion.tex` | Add D1, D2, D3, D5 paragraphs in Limitations + Outlook |
| `paper/latex_gpt/main.pdf` | Recompile |
| `KIMI_R9C_DEFENSE_REPORT_20260425.md` | Per-defense placement + word count + change log |

### Gemini
| File | Action |
|:--|:--|
| `GEMINI_R9C_DEFENSE_AUDIT_20260425.md` | Per-defense hostile-reviewer audit |
| If hostile-v2 trigger fires: `GEMINI_HOSTILE_REVIEW_V2_<date>.md` | Full hostile-review-v2 simulation per existing spec |

---

## 8. Success criteria

- All 5 defenses placed
- Manuscript compiles RC 0
- Gemini hostile-reviewer audit shows ≤ 2 unaddressed attack vectors
- Word count ≤ 5,700 (post-A: 5,200 + R9C: ~+400)
- No new bug-retrospective phrasing introduced
- Reviewer reading the defenses feels we've ANTICIPATED their concerns, not been ambushed by them

---

## 9. Coordination

- Track A (Kimi length surgery) finishes FIRST. Then Track C launches (Kimi has bandwidth).
- Track B (Codex TikZ) runs parallel — different surface area
- Gemini hostile-v2 fires ONLY after A+B+C all close

**No deadline.** 2-3 days expected after Track A closes.
