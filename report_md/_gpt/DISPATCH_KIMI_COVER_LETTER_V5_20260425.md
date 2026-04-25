# DISPATCH KIMI — Cover Letter v5 Update
**Date:** 2026-04-25 00:55 CST
**Issued by:** Claude
**Assignee:** Kimi
**Priority:** MEDIUM (R4-4)
**Time budget:** ~1 day

---

## 0. Objective

Update the cover letter to reflect the post-Round-3 manuscript state. Current `cover_letter_v5.tex.kimi_draft_v3` was drafted pre-ADC-dual-report and pre-correlated-D2D-zone-confirmation. It needs a refresh.

Target venue: **Nature Electronics** (per NARRATIVE_PIVOT §5). Cover letter v6 file.

---

## 1. Key updates vs v5 draft

### 1.1 Strengthen the post-ADC-dual-report framing

Current §5.7 narrative is stronger than v5 reflects:
- Hook-based diagnostic 8-bit ADC numbers locked (§5.7 table)
- Stage-2 per-instance calibration en route (R4-3), will land before submission
- 6-bit ADC cliff backed up by iso-accuracy map (zone 3A) + §5.7 body prose

Cover letter should advertise the dual-column discipline as a novelty signal: "We report deployment accuracy under two ADC protocols (ADC-off surrogate + ADC-on per-instance calibration) to bound realistic deployment performance."

### 1.2 Add correlated D2D evidence

Now confirmed zone 3A. Cover letter can cite:
- Worst-case fresh instance 73.7% at ρ=0.5 AR(1)
- Monotonic degradation pattern matching theory
- Bounded degradation narrative strengthens "robustness across spatial structures"

### 1.3 KIMI-THEORY-1 explicit cite

Cover letter should say explicitly: "Ensemble HAT is theoretically grounded as a distribution-matching objective equivalent to implicit gradient-L2 regularization (structural analogue of dropout-as-L2, Wager 2013), derived in Supp Note S-Theory." This is a methodological contribution that differentiates us from "we tried training with more noise and it helped."

### 1.4 Hardware-calibration readiness advertised

Mention `DATA_INGEST_PROTOCOL` infrastructure: "Our framework is fabrication-ready: measured device statistics from a fabricated organic optoelectronic array will be integrated in revision stage via the ingest pipeline described in Supp Note S-HW."

Do NOT promise specific measured-D2D numbers. Use placeholder `[PENDING_MEASURED_D2D]` discipline.

### 1.5 Three-scenario evidence spine (from NARRATIVE_PIVOT §2)

Ensure cover letter hits all three pillars:
1. Canonical NL=1.0 fresh-instance: 10% → 86.37% (+76pp)
2. OPECT zero-shot: 10% → 88.53% (+78pp)
3. Post-fix severe-NL NL=2.0: 80-82% recovery (placeholder for Stage-2 updated number)

### 1.6 Work 2 preview hook

Mention (without over-promising): "A companion paper will extend the framework to the attention pathway (KV-cache analog CIM); a preliminary subsection demonstrates the diagnostic-treatment signature generalizes."

If R4-6 (Work 2 preview) hasn't landed yet by time of cover letter finalization, soften this to "Outlook section previews the attention-pathway extension."

---

## 2. Structural outline (target ~1.5 pages)

1. **Paragraph 1 (~4 sentences)**: Hook — hardware-instance overfitting as named failure mode; Ensemble HAT as principled treatment with theoretical grounding; three-scenario validation.

2. **Paragraph 2 (~4 sentences)**: Why Nature Electronics — hardware-algorithm co-design, emerging substrate, first-isolation of hardware-instance overfitting in analog CIM literature, calibration-ready against fabricated-array data.

3. **Paragraph 3 (~3 sentences)**: Methodological rigor — dual-column deployment fidelity reporting, zone-partitioned evidence discipline (3A/3B/3C), independent multi-agent audit trail ensures reproducibility.

4. **Paragraph 4 (~2 sentences)**: Companion paper / hardware collaboration — attention-pathway extension and measured-D2D integration roadmap.

5. **Close (~2 sentences)**: Fit to journal, significance for the field, suggested editor if applicable.

---

## 3. Constraints

- **No bug-retrospective language** in cover letter (same discipline as paper body)
- **Zone-mapped numbers only**: every number cited maps to 3A or post-fix 3C
- **Hook-diagnostic wording** for ADC (not deployment-fidelity until Stage-2 lands)
- **Placeholders for R4-3 outputs**: use `[STAGE2_ADC_ENSEMBLE_HEADLINE]` etc. for mechanical fill-in
- **Cite KIMI-THEORY-1 Supp Note S-Theory** by name
- **No Work 2 overpromise**: keep it as companion-paper / preview framing

---

## 4. Deliverable

`paper/latex_gpt/cover_letter_v6.tex.kimi_draft_v3`

Also update/create:
- `paper/latex_gpt/cover_letter_v6_EDITORS.md` — suggested editors + reviewers list if we have suggestions (optional, can be empty if not)
- Append to `KIMI_COVER_LETTER_V6_DELIVERY_<date>.md`: what changed vs v5, placeholders used, integration notes

---

## 5. Timing

- Start immediately (does not block on anything else)
- Keep placeholders open for R4-3 Stage-2 ADC numbers
- Final lock happens at Claude integration pass (Round-5)

---

## 6. Success criteria

- Cover letter reads as a top-tier hardware-algorithm co-design submission
- Every paragraph justifies "why this is Nature Electronics"
- Zero bug-retrospective or ceiling-language
- Reviewer reading this cover letter alone understands the 3-scenario Ensemble HAT story
- Placeholders mechanical for post-Stage-2 swap
