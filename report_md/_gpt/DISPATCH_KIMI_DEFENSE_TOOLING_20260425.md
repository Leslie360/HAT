# DISPATCH KIMI — Defense Prep + Tooling Positioning (Phase 4)
**Date:** 2026-04-25 01:50 CST
**Issued by:** Claude
**Assignee:** Kimi
**Authority:** CLAUDE_PROACTIVE_SPRINT_PLAN_20260425.md Phase 4
**Priority:** MEDIUM (parallel to Phase 3 writing polish)
**Time budget:** ~3-4 days

---

## 0. Mission

Two parallel sub-deliverables:
- **4A**: Defense prep — slides + Q&A for PhD defense (user-facing, not paper-facing)
- **4B**: Tooling positioning supplementary note — comparative analysis vs CrossSim / AIHWKit / NeuroSim (paper-facing)

---

## Sub-phase 4A — Defense materials update

### A.1 Update `KIMI_DEFENSE_BEAMER_20260423.tex`

Current state: 12-slide defense outline, possibly stale post-Round-3 narrative scrub.

**Updates needed:**
- Remove all references to "severe-NL ceiling" / "30%" / "structural barrier"
- Replace with hardware-instance overfitting + Ensemble HAT 86.37% / 88.53% / ~80-82% three-scenario story
- Add 1 slide on Phase 1 KIMI-THEORY-2 (implicit gradient-L2 + flat minima connection) once that lands
- Add 1 slide on Phase 2 mechanism figures (Hessian / loss landscape) once they land
- Update energy numbers to locked 11.45× / 23.9 μJ values
- Add ADC dual-protocol slide (post-module-output hook diagnostic + per-instance recalibration)
- Backup slides: cross-arch validation (when 8×40GB returns), measured D2D (when PhD data lands)

**Target slide count:** 18-22 main + 8-10 backup

### A.2 Update `KIMI_DEFENSE_QA_PREP_20260420.md`

Refresh with anticipated questions for current narrative + answers:

- Q: "Why did Standard HAT collapse — single-class predictor or chance noise?" → A: confirmed deterministic single-class via no-AMP rerun (cite §5.5)
- Q: "ADC-on numbers are 80-82% — that's not deployment-fidelity. How do you defend?" → A: post-module-output hook diagnostic, dual-column reporting, framework provides bounded estimate not point prediction (cite §5.7 + Methods)
- Q: "Why per-epoch resampling specifically?" → A: empirical ablation 88.41% epoch / 86.16% per-batch / 87.18% fixed; theoretical structural analogue to SAM (KIMI-THEORY-2 §S.9); domain-randomization analog (Tobin 2017)
- Q: "Cross-architecture extension?" → A: 8×40GB cross-arch returning soon (placeholder until lands)
- Q: "Hardware validation plan?" → A: framework is calibration-ready via DATA_INGEST_PROTOCOL; measured-D2D Supp Note S-HW pending
- Q: "Energy estimate honesty?" → A: first-order analytical, ε_MAC placeholder, NOT silicon measurement; explicitly stated in §6 limitations
- Q: "Bug history?" → A: implementation details, not scientific findings; verified via 7+9+1 unit tests; Supp Note S-Verification documents the discipline
- Q: "Why Nature Electronics not Nature Communications?" → A: hardware-algorithm co-design fit, organic CIM substrate emerging audience there

Add ~20 questions covering methodology + theory + empirical + limitations + future work.

### A.3 Slide-by-slide narration script

New file: `KIMI_DEFENSE_NARRATION_20260425.md`

For each slide, 30-90 second spoken script. Helps user practice. Consistent with current narrative.

### A.4 Anticipated committee-specific questions

If user has named committee members, draft questions in their published research areas. (User signal needed for this — leave skeleton if no info.)

### A.5 Deliverables (4A)

| File | Status |
|:--|:--|
| `KIMI_DEFENSE_BEAMER_20260425.tex` | Updated 18-22 slide deck |
| `KIMI_DEFENSE_QA_PREP_20260425.md` | Refreshed Q&A doc |
| `KIMI_DEFENSE_NARRATION_20260425.md` | Slide narration script |
| `KIMI_DEFENSE_COMMITTEE_QA_SKELETON_20260425.md` | If user provides committee names |

---

## Sub-phase 4B — Tooling positioning supplementary

### B.1 Why this matters

Current paper has a small CrossSim comparison footnote in Outlook (Section 47). For Nat Electronics audience this is undersold — the analog CIM tooling landscape is something they care about. Expand to a proper Supp Note.

### B.2 New file

`paper/latex_gpt/supplementary/S_tooling_comparison.tex`

### B.3 Content (~3 pages)

#### S-T.1 Landscape (~0.5 page)

Compact tour of the major analog CIM simulation tools:
- **CrossSim** (Sandia / IBM lineage): physical-circuit-level simulator, accurate device modeling, narrow inference focus
- **AIHWKit** (Rasch et al. 2023, IBM): training-aware analog simulator with HAT primitives, broad ML-stack integration, surrogate gradient discipline
- **NeuroSim** (Peng et al. 2019, ASU): architecture-level performance + energy estimator
- **Our framework**: behavioral simulator + multi-instance HAT + variance-decomposition tooling, optimized for hardware-algorithm co-design risk ranking, organic substrate focus

Honest positioning: complementary to (not replacing) the above.

#### S-T.2 Comparison table (~0.5 page)

| Capability | CrossSim | AIHWKit | NeuroSim | Ours |
|:--|:--:|:--:|:--:|:--:|
| Physical device modeling | ⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐ |
| Differentiable HAT training | ⚠️ | ⭐⭐⭐ | ❌ | ⭐⭐⭐ |
| Multi-instance fresh-array eval | ❌ | ⚠️ | ❌ | ⭐⭐⭐ |
| Variance decomposition tooling | ❌ | ❌ | ❌ | ⭐⭐⭐ |
| ADC modeling | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ |
| Organic substrate priors | ❌ | ❌ | ❌ | ⭐⭐⭐ |
| Architecture-energy estimation | ❌ | ⚠️ | ⭐⭐⭐ | ⚠️ |

(Stars are positioning judgments, not literal benchmarks; honest qualitative claims.)

#### S-T.3 Quantitative cross-comparison (~1 page)

Reuse existing CrossSim comparison from current Outlook §47 + expand:
- 1000-image deterministic CIFAR-10 subset
- Single-run clean baseline (we report 86.2%, CrossSim reports 83.7% at 8-bit ADC)
- 3-run Monte Carlo under noise injection (we 81.63±0.56%, CrossSim 67.20±2.67% at σ=5%, 14.43 pp divergence)
- Discuss the 14 pp divergence: noise-to-conductance mapping convention difference (we use multiplicative D2D, CrossSim's default uses additive). Different physical assumptions, both internally consistent.
- Throughput note: CrossSim much slower per-eval for full sweeps; we trade off behavioral fidelity for sweep speed

#### S-T.4 Conceptual ancestry (~0.5 page)

Explicitly cite Rasch et al. 2023 AIHWKit as the conceptual ancestor of:
- Train-with-differentiable-surrogate / eval-with-ADC-hook discipline (D1 in our terminology)
- Per-epoch noise resampling primitives
- Hybrid analog/digital architecture conversion utilities

This is **proper credit** that strengthens our position rather than diluting it. Reviewers respect papers that cite their lineage cleanly.

#### S-T.5 Future bridges (~0.5 page)

Note opportunities for cross-tool integration:
- Calibrate our behavioral D2D priors against CrossSim physical extracted ranges
- Port our Ensemble HAT primitive into AIHWKit
- Use NeuroSim for architecture-energy validation of our energy estimates

Frames our work as community-contributing, not silo'd.

### B.4 Constraints

- **Honest positioning** — no inflating ours / deflating others
- **No empirical numbers** beyond what existing data supports
- **Star ratings are qualitative** — make this clear in caption
- **Cite Rasch 2023 AIHWKit prominently**, including in main paper Methods if not already there

### B.5 Deliverable

| File | Status |
|:--|:--|
| `paper/latex_gpt/supplementary/S_tooling_comparison.tex` | New 3-page Supp Note |
| Updated bib entries for AIHWKit (Rasch 2023), NeuroSim (Peng 2019), CrossSim (Marinella et al.) | Add to refs_gpt.bib |

---

## 5. Sequencing within Phase 4

- **Days 7-8**: Sub-phase 4A (defense materials) — large but mostly mechanical updates from existing files
- **Days 8-10**: Sub-phase 4B (tooling positioning) — fresh writing

Either can start first. Defense work is user-facing (helps user prepare), tooling is paper-facing (helps reviewer accept).

---

## 6. Constraints across both sub-phases

- Same zone discipline + wording rules as previous dispatches
- Defense materials: speak FROM user's voice; user delivers, narration written for that
- Tooling: don't trash competitors; honest positioning earns more respect than aggressive sales

---

## 7. Coordination

- 4A uses outputs from Phase 1 (theory) + Phase 2 (mechanism figures) once they land
- 4B is largely standalone but cites Methods + §5.7 for cross-comparison numbers
- Both feed into Phase 5 Claude integration for the supplementary `\input` chain

---

## 8. Success criteria

- **Defense materials**: user can walk into defense tomorrow and present cleanly. Q&A covers all anticipated reviewer attacks plus committee-specific topics.
- **Tooling positioning**: Nat Electronics editor sees we know our place in the analog CIM tooling ecosystem, cite our conceptual lineage properly, and contribute complementary primitives.

Both deliverables strengthen the submission AND the defense — high-leverage proactive work.

---

## 9. Open question for user

Does user have specific committee member names + research interests to seed sub-phase A.4? If yes: provide. If no: skeleton stays generic.
