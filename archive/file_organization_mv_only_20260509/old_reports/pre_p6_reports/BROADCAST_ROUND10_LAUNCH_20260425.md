# BROADCAST ROUND-10 — Substantive Completion (Option 3 all-in)
**Date:** 2026-04-25 23:00 CST
**From:** Claude (Chief Architect)
**To:** Kimi, Codex, Gemini, User
**Authority:** CLAUDE_ROUND10_SUBSTANTIVE_COMPLETION_PLAN_20260425
**Status:** ACTIVE — 10 sub-tracks closing 11 reviewer-attack vectors before submission

---

## 0. User decision

Option 3 all-in: complete every substantive gap **before** submission, not in revision. **Pre-emptively kill 11 reviewer-attack vectors. Give the paper its strongest possible first-round shot.**

Round-10 sits BETWEEN R9 (presentation polish, in flight) and submission. R9 + R10 + R8 W2 + 8×40GB cross-arch all run **in parallel** — no resource conflicts.

---

## 1. The 11 concerns + 10 dispatches

| # | Concern | Sub-track | Owner |
|:--|:--|:--|:--|
| A1 | 86.37% headline single-seed | R10A multi-seed canonical Ensemble HAT | Codex |
| A2 | Standard HAT 10% mechanism unexplained | R10B class-distribution analysis | Codex |
| A3 | OPECT distribution missing | R10C OPECT statistical characterization | Kimi+Codex |
| B1 | Compute parity | R10I-prep / footnote | Kimi |
| B3 | Ensemble seed variance ±0.47% suspicious | folded into R10A | — |
| C1 | Tobin novelty contrast missing | R10G novelty paragraph | Kimi |
| C2 | "1.5 scenarios not 3" | R10I scenarios reframing | Kimi |
| D1 | Framework framing thin | R10F freshness + framing decision | Kimi |
| D2 | AIHWKit baseline absent | R10E AIHWKit head-to-head | Codex |
| D3 | Energy ε provenance murky | R10H ε provenance table | Kimi |
| E3 | 5pp gap "recipe not floor" no evidence | R10D intermediate NL sweep | Codex |

**Total**: 7-10 days, ~40 GPU-h local.

---

## 2. Dispatches issued

| File | Owner | Sub-tracks |
|:--|:--|:--|
| `CLAUDE_ROUND10_SUBSTANTIVE_COMPLETION_PLAN_20260425.md` | Claude | Master plan |
| `DISPATCH_CODEX_R10_EXPERIMENTS_20260425.md` | Codex | R10A + R10B + R10D + R10E (4 experiments) |
| `DISPATCH_KIMI_R10_CHARACTERIZATION_20260425.md` | Kimi (+ Codex assist) | R10C + R10F + R10H (3 characterization) |
| `DISPATCH_KIMI_R10_FRAMING_20260425.md` | Kimi | R10G + R10I + R10B-text (3 framing) |
| `BROADCAST_ROUND10_LAUNCH_20260425.md` | This file | Master broadcast + R10J venue memo |

---

## 3. Resource matrix (R10 vs R9 vs R8 vs 8×40GB)

| Resource | R10 | R9 | R8 W2 | 8×40GB |
|:--|:--:|:--:|:--:|:--:|
| Local GPU | 50% (R10A+D+E) | 0% | 50% (W2 P2) | 0% |
| Codex bandwidth | 50% experiments | 20% TikZ | 30% W2 | 0% |
| Kimi bandwidth | 50% characterization+framing | 30% R9A+C | 20% W2 paper-2 outline | 0% |
| Gemini bandwidth | 30% (audit at end) | 20% R9C audit | 0% | 0% |
| 8×40GB | 0% | 0% | 0% | 100% |

**Tightest**: Codex juggles 4 GPU experiments + R9B TikZ + R8 W2 P2. Priority: **R10A → R10D → R10E > R9B > R8 W2**. If contention, W2 pauses 1 week (W2 has months of buffer; paper-1 doesn't).

---

## 4. Sequencing (Day-by-Day)

```
Day 1:
  Codex: R10A multi-seed kicks off (3 seeds × 100 epochs train)
  Codex: R10B class-distribution analysis (4h, no GPU train)
  Kimi:  R10I 3-scenarios reframing (1h)
  Kimi:  R10F literature freshness audit start

Day 2-3:
  Codex: R10A 2 seeds finish; R10D NL=1.2/1.5 starts
  Codex: AIHWKit env setup (R10E prep)
  Kimi:  R10C OPECT distribution (with Codex stats assist)
  Kimi:  R10G novelty contrast paragraph draft

Day 4-5:
  Codex: R10A all 3 seeds fresh-eval
  Codex: R10D NL=1.8 + sweep figure
  Codex: R10E AIHWKit baseline training
  Kimi:  R10H energy provenance research
  Kimi:  R10B-text integration (after Codex R10B lands)

Day 6-7:
  Codex: R10E AIHWKit baseline lands
  Kimi:  R10G AIHWKit placeholder fill
  Claude: integration pass — all 11 concerns now have evidence/text
  Gemini: substantive audit (per-concern verification, not text pretty-pass)

Day 8-10 (buffer + R9 catch-up):
  Kimi: R9A length surgery (now uses R10-augmented headlines + new defenses)
  Codex: R9B TikZ rebuild (parallel)
  Claude: final read-through
```

---

## 5. R9 + R10 integration plan

R10 produces NEW content (~+400-500 words across § 5.5 mechanism, § 5.6 multi-seed headline reframe, § 5.7 NL sweep, § 5.8 OPECT stats, § 6 AIHWKit comparison, novelty paragraph).

R9A length surgery target shifts:
- Original: 7,332 → 5,500 words (-28%)
- **Revised**: 7,332 → 5,900 words (-19%, after R10 additions)

This still fits Nat Electronics envelope (5-6k words typical). Net: **stronger paper, similar length**.

R9 Track A (Kimi length surgery) waits for R10 to finish before starting cuts. Why: easier to cut once new content lands; otherwise we cut things that R10 will re-add.

R9 Track B (Codex TikZ) parallel-friendly with R10. No conflict.

R9 Track C (defense paragraphs) some folded into R10:
- D2 (5pp gap) — R10D evidence supersedes pure framing-only D2
- Other defenses (D1 Hardware fidelity, D3 ε_MAC, D4 OPECT, D5 ImageNet) — R9 written; R10 adds substance behind them

---

## 6. R10J — Venue strategy memo (decided here)

User asked about venue strategy. Honest assessment:

### Nat Electronics (current target)
- **Pros**: high-impact, perfect device-algorithm co-design fit, strong precedent for analog CIM
- **Cons**: device + circuit reviewer expertise; software-flavored ML may not impress; Tiny-ViT on CIFAR is below their typical model scale
- **Risk**: desk reject (lab-software focus, not enough silicon)
- **Estimated outcome**: 60% Major Revision, 30% Reject after revision, 10% Accept after revision

### Advanced Science (backup)
- **Pros**: cross-disciplinary, more software-flavored work accepted, IF 15-19
- **Cons**: less prestige than Nat Electronics, less analog CIM concentration
- **Risk**: lower bar, but reviewers less specialized → may not appreciate technical depth
- **Estimated outcome**: 40% Major Revision, 50% Accept after revision, 10% Reject

### Nature Communications Engineering (also backup)
- **Pros**: new journal hungry for content, IF ~8 (newer journal so still building citation base), Nature family
- **Cons**: less established, lower IF
- **Estimated outcome**: 30% Major Revision, 60% Accept, 10% Reject

### npj Computational Materials (alternative)
- **Pros**: framework-paper friendly, IF 12, computational community appreciates simulators
- **Cons**: less device-physics audience, may not fully appreciate organic CIM
- **Risk**: editor may bounce as "not enough materials science"

### Recommendation: Nat Electronics first, Adv Sci second

Even with R10 + R9, Nat Electronics is a stretch. But:
1. Submitting to Nat Electronics first is "free" — even rejection gives reviewer comments we can use for resubmission
2. R10 + R9 makes Nat Electronics outcome possible (without R10, it's hopeless)
3. If Nat Electronics rejects: directly resubmit to Adv Sci with reviewer-feedback-incorporated revision (faster than original submission)
4. If Adv Sci accepts: still good outcome (IF 15-19)

**Decision: Stay Nat Electronics first.** Adv Sci is the immediate fallback after rejection. Don't preemptively downgrade.

(User can override.)

---

## 7. Acceptance criteria for Round-10 closure

| Concern | Closes when |
|:--|:--|
| A1 | R10A delivers 3-seed canonical Ensemble HAT mean ± std |
| A2 | R10B delivers class-distribution figure + paragraph in §5.5 |
| A3 | R10C delivers OPECT QQ + AD test + statistical distance |
| B1 | R10I-prep footnote in §3 Methodology |
| C1 | R10G paragraph in §2.1 |
| C2 | R10I edits propagated across abstract+intro+discussion+cover letter |
| D1 | R10F audit complete; framing decision documented |
| D2 | R10E AIHWKit head-to-head numbers in §5 or Discussion |
| D3 | R10H provenance table in Supp Note S-Energy-Provenance |
| E3 | R10D NL sweep figure + paragraph supporting D2 defense |

**All 10 sub-tracks**: deliverables landed + manuscript integrated + Gemini hostile-v2 audit ≤ 2 unaddressed concerns.

---

## 8. Frozen decisions (still hold)

- NARRATIVE_PIVOT zone partition + Ensemble HAT diagnostic-treatment narrative
- PhD-graduation submission gate
- Wording bans
- Workspace doctrine
- Round-8 W2 launch
- 8×40GB cross-arch independent
- Git push strategy

**New (R10-specific)**:
- R10A multi-seed = headline replacement; reorders R9A length surgery
- R10E AIHWKit becomes "first head-to-head analog HAT comparison" — strengthens novelty claim
- R10I scenarios reframing changes paper's signature framing language permanently (was an honest-mistake before)

---

## 9. Escalation triggers

- R10A 3-seed mean diverges > 3pp from 86.37 → ESCALATE
- R10A any seed mean < 80% → MAJOR ESCALATION (reopen NARRATIVE_PIVOT)
- R10D non-monotonic with NL → ESCALATE
- R10E AIHWKit beats our Ensemble HAT → REASSESS novelty; honest reframe
- R10B Standard HAT NOT single-class collapse → revise mechanism story
- R10C OPECT data unavailable in paper SI → fallback honest framing
- R10F finds direct Ensemble HAT prior art → cite + reframe novelty (still publishable)

---

## 10. Submission timeline

```
Now → +5 days:    R9 + R10 parallel execution
+5 → +7 days:     R9 + R10 integration; Gemini hostile-v2 audit
+7 → +10 days:    Final read-through + cover letter polish
+10 days:         Submission-ready (pending PhD defense gate)
```

8×40GB return + PhD measured-D2D arrival can happen mid-window — auto-integrate. **R10 is the last substantive work; after R10 closes, we're paper-1-done waiting on PhD gate only.**

---

## 11. Agent-level instructions

### Codex (highest workload)
- Days 1-5: 4 experiments R10A/B/D/E
- Bandwidth: 50% R10 + 30% R8 W2 P2 + 20% R9B TikZ
- Priority order ABSOLUTE: R10A > R10D > R10E > R9B > W2
- All experiments document provenance (commit hash, code sha256, GPU device, env version)
- All numerical claims preserved + extended

### Kimi
- Days 1-3: characterization (R10C + R10F + R10H) + framing (R10I early)
- Days 4-5: framing (R10G + R10B-text after Codex evidence lands)
- Days 6-10: R9A length surgery (using R10-augmented content)
- Bandwidth: 50% R10 + 30% R9 + 20% R8 W2 paper-2 outline

### Gemini
- Days 1-5: STAND BY (no R10 task)
- Days 6-7: R10 substantive audit (per-concern verification)
- After all R10 + R9 close: G-HOSTILE-V2 trigger fires (final hostile reviewer simulation)
- Output: final hostile review report; if ≤ 2 unaddressed concerns → submission-ready

### Claude (me)
- Days 1-5: monitor + coordination + escalation handling
- Days 6-7: integration pass (merge R10 outputs into manuscript)
- Days 8-10: final read-through + cover letter polish
- Days 10+: submission package preparation pending PhD gate

### User
- Round-10 launched; agent work begins
- I'll surface escalations immediately
- Stay informed via AGENT_SYNC; intervene if you want to override venue strategy or specific decisions

---

## 12. One-line

Round-10 = 10-sub-track substantive completion (multi-seed headline / mechanism / OPECT stats / NL sweep / AIHWKit / freshness / novelty / energy / scenarios / venue) over 7-10 days, ~40 GPU-h local, parallel with R9 + R8 + 8×40GB. Pre-emptively closes 11 reviewer-attack vectors. Submission-ready in ~10 days pending PhD gate.
