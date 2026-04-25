# BROADCAST ROUND-7 — Proactive Depth Investment Sprint
**Date:** 2026-04-25 01:50 CST
**From:** Claude (Chief Architect)
**To:** Kimi, Codex, Gemini
**Authority:** CLAUDE_PROACTIVE_SPRINT_PLAN_20260425.md
**Status:** ACTIVE (replaces calm-before-trigger Round-6 with active depth sprint)

---

## 0. Why this changes

User directive: "我们得有自己的步骤" — don't sit waiting for triggers; do proactive work that genuinely improves submission. 8×40GB returns next week. PhD data indeterminate. The buffer is for **depth investment**, not idle.

---

## 1. Sprint shape — 4 phases over 1-2 weeks

| Phase | Owner | What | Why |
|:--|:--|:--|:--|
| **1. Theory deepening** | Kimi | Higher-order Taylor + PAC-Bayes + flat-minima connection | Move Ensemble HAT from "method that works" to "principled method with generalization theory" |
| **2. Empirical mechanism** | Codex | Hessian / loss landscape / CKA / per-layer sensitivity (5 jobs, ~6-8 GPU-h, all on existing checkpoints) | Make theory predictions visible; reviewer feels "I can see why it works" |
| **3. Writing polish** | Kimi | Discussion arc restructure + design rules callout + reproducibility cookbook + figure caption audit | Lift "accurate" → "elegant"; reduce reviewer friction |
| **4. Defense + tooling** | Kimi | Defense slides/Q&A + competitor positioning Supp Note | Defense-ready + paper-positioned within analog CIM tooling landscape |
| **5. Integration** | Claude | One-pass merge of Phase 1 + 2 + 3 + 4 outputs | Submission-package consolidation |

---

## 2. Dispatches issued

| Dispatch | Owner | Phase | File |
|:--|:--|:--:|:--|
| KIMI-THEORY-2-DEEPENING | Kimi | 1 | `DISPATCH_KIMI_THEORY_2_DEEPENING_20260425.md` |
| CODEX-EMPIRICAL-DEEPENING | Codex | 2 | `DISPATCH_CODEX_EMPIRICAL_DEEPENING_20260425.md` |
| KIMI-WRITING-POLISH | Kimi | 3 | `DISPATCH_KIMI_WRITING_POLISH_20260425.md` |
| KIMI-DEFENSE-TOOLING | Kimi | 4 | `DISPATCH_KIMI_DEFENSE_TOOLING_20260425.md` |

---

## 3. Sequencing

```
Day 1-3:    Phase 1 (Kimi theory) || Phase 2 jobs E1-E2 (Codex)
Day 4-5:    Phase 1 lands; Phase 2 jobs E3-E4 land; Phase 3 starts
Day 6-7:    Phase 2 E5 lands; Phase 3 continues; Phase 4 starts
Day 8-10:   Phase 4 lands
Day 10-12:  Phase 5 (Claude integration)
```

8×40GB return mid-sprint → queue cross-arch as Phase 6 (post-sprint).
PhD data lands → queue as Phase 7 (post-sprint).

---

## 4. What this sprint adds (concrete deliverables)

**Theory:**
- Supp Note S-Theory extended: §S.7 higher-order, §S.8 PAC-Bayes, §S.9 SAM connection, §S.10 limitations
- 6 new bib entries (Roberts-Yaida 2022, Dziugaite-Roy 2017, Pérez-Ortiz 2021, Foret 2021, Keskar 2017, Andriushchenko 2022)
- Discussion §6.1 paragraph linking three theoretical lenses

**Empirical:**
- 5 new figures: figS_hessian_spectrum, figS_d2d_loss_landscape, figS_cka_mseries, figS_per_layer_sensitivity, figS_checkpoint_avg
- 5 new JSONs in `report_md/_gpt/json_gpt/`
- New Supp Note S-Mechanism with cross-job synthesis
- Replaces contaminated supplementary groupwise table as MLP-bottleneck evidence (with proper post-fix provenance)

**Writing:**
- Restructured Discussion §6 (Diagnosis → Treatment → Mechanism → Implications → Limitations arc)
- Design rules callout box (7 actionable rules)
- New Supp Note S-Reproducibility (3-page cookbook)
- All section opening/closing sentences audited
- All figure captions self-contained
- Acknowledgments + Author contributions skeleton

**Positioning:**
- Updated defense slides (18-22 slides + backup)
- Refreshed Q&A doc (~20 questions)
- Slide narration script
- New Supp Note S-Tooling (~3 pages, comparison + Rasch lineage credit)

---

## 5. What this sprint is NOT

- Not new training (Phase 2 is eval-only on existing checkpoints)
- Not new architectures or datasets
- Not retraining anything
- Not narrative pivot (NARRATIVE_PIVOT remains source of truth)
- Not gating the 8×40GB or PhD-data triggers

---

## 6. Risk assessment

- **Phase 1 theory**: PAC-Bayes might be vacuous → drop §S.8, keep §S.7 + §S.9 + §S.10. Honest negative outcome.
- **Phase 2 empirical**: if Hessian/loss-landscape contradicts theory, ESCALATE — could strengthen or weaken paper depending. Not zero-risk but right thing to do.
- **Phase 3 writing + Phase 4 positioning**: pure improvement, no risk.

Risk-adjusted ROI very high. Worst case = honest negative findings documented. Best case = paper substantially upgraded.

---

## 7. Triggers that interact mid-sprint

| Trigger | Action |
|:--|:--|
| 8×40GB return mid-sprint | Continue sprint; queue cross-arch as Phase 6 (post-sprint) |
| PhD data lands mid-sprint | Continue sprint; queue R-D0 ingest as Phase 7 (post-sprint) |
| User says "stop, just submit" | Halt at end of current phase, fast-track integration |
| Phase 1 PAC-Bayes derivation fails | Drop §S.8, document, continue with §S.7+9+10 |
| Phase 2 Hessian contradicts flat-minima hypothesis | ESCALATE to Claude; honest finding to navigate |

---

## 8. Frozen decisions reaffirmed

All 12 frozen decisions from CLAUDE_FORWARD_ROADMAP §10 still hold:
- Narrative anchored at hardware-instance overfitting + Ensemble HAT
- Venue Nature Electronics
- Train ADC-off, eval ADC-on dual protocol
- 86.37% canonical Ensemble HAT (zone 3A)
- 80-82% severe-NL band (zone 3C, Stage-2 confirmed stable)
- No retraining
- No bug discussion in paper body
- PhD-graduation submission gate
- Batch integration

Sprint adds depth without changing any.

---

## 9. Agent-level

### Kimi (heaviest workload)
- **Days 1-3**: Phase 1 theory deepening (highest priority)
- **Days 4-7**: Phase 3 writing polish (after Phase 1 + 2 land)
- **Days 7-10**: Phase 4A defense + Phase 4B tooling (parallel)
- All sidecar discipline: edits to canonical .tex acceptable (sprint, not draft); updates appended to AGENT_SYNC

### Codex
- **Days 1-5**: Phase 2 (5 empirical jobs, ~6-8 GPU-h total)
- **No new training in sprint scope**
- Master report at end of Phase 2 with cross-job synthesis
- Stays available for trigger-fired work (8×40GB return, R4-6 W2 KV-cache, PhD data ingest)

### Gemini
- **STAND BY**. No sprint task.
- G-HOSTILE-V2 spec from Round-6 still holds (4 trigger conditions, including "all sprint phases settled" added implicitly).
- Available if Phase 1 / Phase 2 escalation hits.

---

## 10. Sprint completion → submission readiness

After Phase 5 Claude integration:
- Manuscript = original Round-5 integration + sprint depth additions
- Three theoretical lenses (implicit reg + PAC-Bayes + SAM) converging on Ensemble HAT mechanism
- Five empirical mechanism figures
- Discussion narrative arc cleaner
- Reviewer-friendly design rules callout
- Reproducibility cookbook
- Tooling positioning honest and clear
- Defense materials ready
- Cover letter v6 already locked

**Then we wait** for:
- 8×40GB return → cross-arch supplementary
- PhD data → measured-D2D Supp Note S-HW
- All settled → G-HOSTILE-V2 hostile review
- Final read → PhD defense gate → submit

This is the **last big proactive push**. After it, work goes back to reactive monitoring.

---

## 11. One-line

"Replace passive wait with proactive depth investment: 4 phases (theory + empirical + writing + positioning), ~1-2 weeks, on existing assets, lifts submission from accurate to Nat-Electronics-editor-friendly."
