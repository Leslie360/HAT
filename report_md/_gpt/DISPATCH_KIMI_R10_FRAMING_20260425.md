# DISPATCH KIMI R10 — Framing (3 sub-tracks)
**Date:** 2026-04-25 23:00 CST
**Issued by:** Claude
**Assignee:** Kimi
**Authority:** CLAUDE_ROUND10_SUBSTANTIVE_COMPLETION_PLAN
**Priority:** MEDIUM (after R10 experiments + characterization land; before R9A length surgery)
**Time budget:** ~5-6 hours total

---

## 0. Mission

Three reframing edits closing 3 reviewer-attack vectors that are TEXTUAL, not experimental:
- R10G: Novelty contrast vs Tobin 2017 + AIHWKit (closes "Ensemble HAT is just domain randomization" attack)
- R10I: "Three scenarios" → "single training, two evaluation regimes + one independent training" (closes "1.5 scenarios not 3" attack)
- R10B-text: Mechanism explanation paragraph (closes "10% is single-class collapse, not overfitting" attack — uses R10B Codex evidence)

---

## 1. R10G — Novelty contrast paragraph (4 hours)

### Why
Paper claims novelty for Ensemble HAT (per-epoch D2D mask resampling). But:
- Tobin 2017 domain randomization does per-iteration parameter resampling for sim2real (very similar mathematically)
- AIHWKit (Rasch 2023) has analog noise injection (similar in spirit)

Reviewer: "Per-epoch resampling is just domain randomization applied to analog HAT. Where's the novelty?"

We need to **explicitly contrast** rather than vaguely cite.

### Spec

Find current cites of Tobin 2017 + Rasch 2023 in `01_introduction.tex` and `02_related_work.tex` §2.1. Rewrite or add ONE paragraph (placement: end of §2.1 Hardware-Aware Training) that:

1. **Acknowledges connection** to domain randomization — don't hide it
2. **Differentiates** Ensemble HAT specifically:
   - **Substrate**: organic optoelectronic CIM has substrate-specific noise structure (spatial D2D + cycle C2C + nonlinear write); domain randomization for sim2real treats noise as i.i.d. parameters
   - **Granularity**: per-epoch (not per-iter) preserves D2D mask consistency within an epoch — empirically matters (paper §5.7 ablation: 88.41 epoch / 86.16 per-batch / 87.18 fixed)
   - **Theoretical interpretation** (KIMI-THEORY-1/2): structural analogue to SAM along D2D direction; not a method paper but a mechanism paper
   - **Paired with hardware-instance overfitting diagnosis**: domain randomization papers don't typically diagnose source-instance overfitting; we do (10.00% Standard HAT collapse → 86.37% Ensemble HAT recovery)
3. **Contrast vs AIHWKit** (Rasch 2023):
   - AIHWKit injects per-batch analog noise
   - We resample full structured D2D mismatch maps per epoch
   - When R10E head-to-head lands: cite specific numerical comparison

### Draft paragraph (template, polish wording)

```latex
\subsection{Hardware-Aware Training and Robustness}
% ... existing subsection content ...

\paragraph{Relation to domain randomization and existing analog HAT.}
Per-epoch D2D mask resampling shares the spirit of domain randomization 
in sim-to-real transfer~\citep{tobin2017domain}, where simulation parameters 
are perturbed during training to enable cross-domain generalization. Two 
distinctions matter for the analog CIM regime. First, organic optoelectronic 
hardware-instance overfitting arises from a spatially structured D2D mismatch 
mask whose realization is fixed for each fabricated array, not from i.i.d.\ 
parameter perturbations; preserving mask consistency within an epoch (rather 
than per-batch resampling) is empirically necessary—our ablation shows 
88.41\% (per-epoch) versus 87.18\% (fixed) versus 86.16\% (per-batch). 
Second, established analog HAT libraries~\citep{rasch2021aihwkit,crosssim2024} 
inject per-batch noise rather than full mask resampling; under our matched 
canonical settings, AIHWKit's per-batch analog noise yields fresh-instance 
accuracy of [PENDING\_R10E\_NUMBER]\% versus our Ensemble HAT's 86.37\%. 
The contribution thus is the substrate-specific analysis (spatial D2D, 
hardware-instance overfitting diagnostic) and the structural-analogue 
theory (Supp~Note~S-Theory) rather than a fundamentally new training 
primitive.
```

This is ~120 words. Place in §2.1 just before §2.2 (Organic Devices).

### Coordination
- AIHWKit specific number from R10E will fill `[PENDING_R10E_NUMBER]` placeholder
- If AIHWKit baseline isn't ready, leave placeholder; integration pass fills

### Deliverable
- Edit in `paper/latex_gpt/sections/02_related_work.tex` §2.1 end
- Append to `KIMI_R10_FRAMING_REPORT_20260425.md` with diff

### Time: 4 hours

---

## 2. R10I — "Three scenarios" reframing (1 hour)

### Why
Paper says "Ensemble HAT validated across three independent scenarios" but actually:
- Scenario 1 (canonical NL=1.0 fresh) and Scenario 2 (OPECT zero-shot) → **same canonical Ensemble HAT checkpoint**, just two evaluation regimes
- Scenario 3 (severe-NL NL=2.0) → **independent training** (M-series)

So really it's "one training + two evaluations + one independent training" = 1.5 scenarios. A senior reviewer will frame this critically.

### Spec

Find every place paper says "three scenarios" / "three independent scenarios" / "across three scenarios". List of probable locations:
- `00_abstract.tex`
- `01_introduction.tex` para 6
- `06_discussion.tex` §6.1
- `cover_letter.tex`

For each occurrence, replace with one of:

**Option A** (most honest):
> "across two evaluation regimes (canonical Gaussian D2D and the literature-anchored OPECT profile) of a single training, plus an independent severe-write-nonlinearity training arm"

**Option B** (more compact):
> "demonstrated under canonical evaluation, literature-anchored zero-shot transfer, and severe-NL stress"

I lean toward **Option B** for compactness. The honest framing is the substance — exact wording can be tight.

### Constraints
- Do NOT delete the three pieces of evidence; they're all real
- Do NOT change the numerical claims (86.37 / 88.53 / 80-82)
- ONLY change framing language

### Deliverable
- Edit affected files
- Append change log to `KIMI_R10_FRAMING_REPORT_20260425.md`

### Time: 1 hour

---

## 3. R10B-text — Mechanism explanation paragraph (~30 min, after Codex R10B lands)

### Why
Codex R10B produces class-distribution analysis showing Standard HAT collapses to single-class predictor. We need to integrate this finding into §5.5 with paper-safe language.

### Spec

Wait for Codex `CODEX_R10B_MECHANISM_REPORT_20260425.md` to land. It will provide the paper-safe paragraph. Your job: place it in §5.5 Hardware Transferability after the existing no-AMP confirmation, before the Ensemble-HAT-introduction sentence.

Verify:
- Numerical values match Codex's report
- Figure reference points to `figS_standard_hat_collapse_mechanism`
- Wording compatible with surrounding paragraph

### Time: 30 min after Codex deliverable

---

## 4. Constraints (HARD across all 3 sub-tracks)

- **No content additions beyond the 3 paragraphs/edits.**
- **No silent changes** — every change documented in `KIMI_R10_FRAMING_REPORT_20260425.md`
- **Zone discipline preserved**: 3A/3B/3C unchanged
- **No bug-retrospective language reintroduction**
- **R9A length surgery awareness**: your additions are part of the +400 word post-R10 budget; R9A target shifts from 5,500 → 5,900

---

## 5. Coordination

- R10B-text **waits for** Codex R10B report (Day 1 likely)
- R10G ideally **waits for** R10E AIHWKit number (Day 4-5); but can place placeholder earlier
- R10I has no dependencies — can fire Day 1
- R9A length surgery **starts after** all R10 framing edits land — Kimi's bandwidth shifts from R10 to R9A around Day 5-7
- R10C OPECT characterization (separate dispatch `DISPATCH_KIMI_R10_CHARACTERIZATION`) parallel — different surface area

---

## 6. Sequencing within Kimi

### Day 1
- R10I 3-scenarios reframing (1 hour)
- Start R10F literature freshness audit (in characterization dispatch)

### Day 2-3
- R10C OPECT characterization (in characterization dispatch)
- R10G novelty contrast paragraph draft (using existing AIHWKit literature)

### Day 4-5
- Codex R10B + R10E land
- R10B-text mechanism integration (30 min)
- R10G AIHWKit placeholder fill

### Day 6 (buffer)
- Integration check
- Hand off to R9A length surgery

---

## 7. Deliverables

| File | Action |
|:--|:--|
| `paper/latex_gpt/sections/02_related_work.tex` | EDIT — add R10G novelty contrast paragraph |
| `paper/latex_gpt/sections/00_abstract.tex` | EDIT — R10I 3-scenarios reframing |
| `paper/latex_gpt/sections/01_introduction.tex` | EDIT — R10I 3-scenarios reframing |
| `paper/latex_gpt/sections/05_results.tex` | EDIT — R10B-text mechanism integration |
| `paper/latex_gpt/sections/06_discussion.tex` | EDIT — R10I 3-scenarios reframing |
| `paper/latex_gpt/cover_letter.tex` | EDIT — R10I 3-scenarios reframing |
| `KIMI_R10_FRAMING_REPORT_20260425.md` | Per-edit diff log |

---

## 8. Success criteria

- "Three scenarios" language gone everywhere; replaced with honest framing
- Tobin/AIHWKit contrast paragraph present in §2.1
- Standard HAT 10% mechanism explanation in §5.5
- Manuscript compiles RC 0
- Reviewer reading these sections can no longer accuse vague novelty / 1.5-scenarios / unexplained collapse

---

## 9. Cold-start refs

- `CLAUDE_ROUND10_SUBSTANTIVE_COMPLETION_PLAN_20260425.md` — master plan
- `DISPATCH_CODEX_R10_EXPERIMENTS_20260425.md` — for R10B/R10E coordination
- `DISPATCH_KIMI_R10_CHARACTERIZATION_20260425.md` — companion (R10C/F/H)
- `paper/latex_gpt/refs_gpt.bib` — Tobin 2017 + Rasch 2023 already cited

**No deadline.** 5-6 hours of actual work spread across Days 1-5 (interleave with characterization tasks).
