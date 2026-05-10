# CLAUDE ROUND-10 — Substantive Completion (Option 3, all-in)
**Date:** 2026-04-25 23:00 CST
**From:** Claude (Chief Architect)
**Trigger:** User decision: "Option 3, 派发任务" — close 11 substantive concerns before submission, not in revision
**Authority:** This file
**Status:** ACTIVE — 10 sub-tracks, 7-10 days, ~40 GPU-h on local; parallel with R9 + R8 + 8×40GB

---

## 0. Strategic decision

User chose Option 3: complete every substantive gap **before** submission, not after Major Revision. Rationale:
- 1 week of R10 work saves potentially 2-3 months of revision cycle
- First-round Minor Revision (or Accept-with-Tweaks) becomes plausible at Nat Electronics
- All substantive concerns answered before reviewers even see paper

Round-10 sits between R9 (presentation polish, in flight) and submission. R10 + R9 + R8 W2 + 8×40GB cross-arch all run **in parallel** — no resource conflicts.

---

## 1. Eleven concerns mapped to ten dispatches

| # | Concern | Dispatch | Owner | Time | GPU |
|:--|:--|:--|:--|--:|--:|
| A1 | 86.37% headline single-seed | R10A multi-seed canonical Ensemble HAT | Codex | 1 day | ~20h |
| A2 | Standard HAT 10% mechanism | R10B class-distribution + gradient analysis | Codex | 4h | 0 |
| A3 | OPECT distribution missing | R10C OPECT statistical characterization | Codex+Kimi | 1 day | 0 |
| B1 | Standard vs Ensemble compute parity | R10D-prep / Discussion footnote | Kimi | 1h | 0 |
| B3 | Ensemble seed variance ±0.47% suspicious | folded into R10A (3 seeds) | — | — | — |
| C1 | Tobin novelty contrast missing | R10G novelty paragraph rewrite | Kimi | 4h | 0 |
| C2 | "1.5 scenarios not 3" | R10I honest reframing edit | Kimi | 1h | 0 |
| D1 | Framework framing too thin | R10F literature freshness + framing decision | Kimi | 1 day | 0 |
| D2 | AIHWKit baseline absent | R10E AIHWKit head-to-head | Codex | 2-3 days | ~10h |
| D3 | Energy ε provenance murky | R10H ε literature provenance table | Kimi+Codex | 4h | 0 |
| E3 | 5pp severe-NL "recipe not floor" no evidence | R10D intermediate NL sweep | Codex | 1-2 days | ~10h |

**Total**: ~7-10 days wall-clock, ~40 GPU-h on local, modest Kimi text load.

---

## 2. Dispatch grouping (4 dispatches, 10 sub-tracks)

| Dispatch | Contents | Owner |
|:--|:--|:--|
| **R10-CODEX-EXPERIMENTS** | R10A multi-seed Ensemble HAT + R10D intermediate NL sweep + R10E AIHWKit baseline + R10B class-distribution analysis | Codex |
| **R10-KIMI-CHARACTERIZATION** | R10C OPECT distribution + R10F literature freshness + R10H energy provenance | Kimi (with Codex assist on R10C numerical) |
| **R10-KIMI-FRAMING** | R10G novelty contrast + R10I scenarios reframing + R10B-text mechanism explanation | Kimi |
| **R10-CLAUDE-VENUE** | R10J venue strategy review (Nat Elec vs Adv Sci vs Nat Comm Eng cost-benefit) | Claude |

---

## 3. Sequencing (parallel-friendly)

```
Day 1:
  [Codex]  R10A multi-seed Ensemble HAT — kick off training (3 seeds, 24h compute)
  [Codex]  R10B class-distribution analysis — quick (4h, no GPU)
  [Codex]  R10D intermediate NL sweep — kick off (parallel with R10A)
  [Kimi]   R10C OPECT distribution analysis (parallel)
  [Kimi]   R10G novelty contrast paragraph
  [Kimi]   R10I 1.5-scenarios reframing (1 hour)
  [Kimi]   R10H energy ε provenance research

Day 2-3:
  [Codex]  R10A landing (3 seeds × 100 epochs)
  [Codex]  R10D landing (3 NL points)
  [Codex]  R10E AIHWKit baseline — start
  [Kimi]   R10F literature freshness audit (last 6 months)
  [Kimi]   D2 evidence integration (intermediate NL → defense paragraph)
  [Claude] R10J venue strategy memo

Day 4-5:
  [Codex]  R10E AIHWKit baseline landing
  [Kimi]   Integration of all R10 findings into manuscript
  [Codex]  R10A fresh-eval all 3 seeds (~3h)

Day 6-7:
  [Claude] Round-10 integration pass
  [Gemini] R10 hostile audit (substantive concerns, not just text)
  [Claude] Final compile + verify all 11 concerns addressed
```

Parallel:
- R8 Work 2 Phase 2 continues independently
- R9 Tracks A/B/C continue (Kimi/Codex split bandwidth carefully)
- 8×40GB cross-arch runs independently

---

## 4. Resource matrix

| Resource | R8 W2 | R9 (A+B+C) | R10 |
|:--|:--:|:--:|:--:|
| Local GPU | 50% | 0% | 50% (R10A + R10D + R10E) |
| Codex bandwidth | 30% | 20% (R9B TikZ) | 50% (R10 experiments + analysis) |
| Kimi bandwidth | 30% (Stream A+B) | 50% (R9A+C) | 20% (R10C/F/G/H/I text) |
| Gemini bandwidth | 0% | 20% (R9C audit) | 80% (R10 substantive audit at end) |
| 8×40GB | 0% | 0% | 0% (paper-1 cross-arch independent) |

Tightest: Codex juggles R8 W2, R9B TikZ, R10 experiments. **Priority order: R10A (highest, headline number) > R10D (close 5pp gap) > R10E (AIHWKit) > R9B TikZ > R8 W2 Phase 2**.

If Codex bandwidth maxed: R8 W2 Phase 2 can pause for 1 week (W2 has months of buffer; paper-1 doesn't).

---

## 5. Acceptance criteria for Round-10 closure

| Criterion | Threshold |
|:--|:--|
| R10A multi-seed Ensemble HAT canonical | 3 seeds, fresh-instance mean ± std published; replaces single-seed 86.37 |
| R10B 10% mechanism explained | Class distribution figure + 1-paragraph explanation in §5.5 |
| R10C OPECT distribution stats | QQ plot + Anderson-Darling + kurtosis in Supp Note S-OPECT |
| R10D intermediate NL evidence | Single figure showing monotonic gap shrinkage NL=1→2; supports D2 defense |
| R10E AIHWKit baseline | Direct comparison number; head-to-head paragraph in Discussion |
| R10F literature freshness | 1-page audit of 2025-2026 prior art; integrated into §2 if relevant findings |
| R10G novelty contrast | Single paragraph in §2.1 explicitly contrasting our method vs Tobin/AIHWKit |
| R10H energy ε provenance | Supp Note table with each ε value + citation source line |
| R10I scenarios reframing | "single training, two evaluation regimes + one independent training" replaces "three scenarios" |
| R10J venue strategy | Memo: Nat Elec vs Adv Sci comparison; user decides at end |

Manuscript compile RC 0; all numerical claims preserved + extended; zero broken refs.

---

## 6. Frozen decisions (still hold)

- NARRATIVE_PIVOT zone partition + Ensemble HAT diagnostic-treatment narrative
- PhD-graduation submission gate (R10 + R9 are pre-gate readiness work)
- Wording bans: no "post-fix"/"deployment-fidelity"/"bug-immune"/"post-fix"
- Workspace doctrine: clean dispatch per round, no stale files
- Round-8 W2 launch unchanged
- 8×40GB cross-arch unchanged
- Git push strategy (master clean, BFG'd, force-push capable)

**New (Round-10 specific)**:
- R10A multi-seed = HEADLINE replacement; reorders R9A length surgery to use new headline
- R10E AIHWKit becomes "first head-to-head analog HAT comparison" — strengthens novelty claim materially

---

## 7. What changes if R10A multi-seed goes badly

**R10A escalation triggers**:
- 3-seed mean ∈ 84-88%: normal, integrate as new headline
- 3-seed mean diverges by > 3pp from 86.37%: ESCALATE; investigate one-checkpoint anomaly
- 3-seed std > 3pp: ESCALATE; methodology question; possibly more seeds needed
- Seed-level mean below 80%: MAJOR ESCALATION; may invalidate paper claim; reopen NARRATIVE_PIVOT

If R10A gives clean ~86% across seeds → headline strengthens; submission probability goes up. If R10A gives messy variance → we learn before reviewer does, fix before submission.

**This is exactly the value of Option 3**: known-unknowns become tested before reviewers.

---

## 8. Coordination with R9 and R8

### R9 Track A (Kimi length surgery)
- Conflict: R9A cuts §5.5 §5.6 §5.8; R10B/R10C add to those sections
- **Solution**: Kimi does R10B/R10C/R10G/R10I/R10H **first** (Days 1-3), then R9A (Days 4-7)
- New length budget: 5,500 (R9A target) + 400 (R10 additions) = ~5,900 words. Within Nat Electronics envelope.

### R9 Track B (Codex TikZ)
- No conflict: R10 is GPU+code-analysis; R9B is TikZ. Separate surface area.
- Codex split: 60% R10 experiments + 30% R9B TikZ + 10% R8 W2 Phase 2 monitoring

### R9 Track C (defense paragraphs)
- R10D intermediate NL evidence DIRECTLY supports R9C-D2 (5pp gap defense)
- **Sequencing**: R10D fires first (Days 2-3), R9C-D2 paragraph written with new evidence (Days 4-5)

### R8 Work 2 Phase 2 (Pythia 410M Ensemble HAT training)
- ~50% local GPU; R10 takes other 50%
- Codex juggles two GPU streams via cron / nohup
- If contention: paper-1 R10 priority (submission-bound)

### 8×40GB paper-1 cross-arch
- Independent — Round-10 doesn't touch it

---

## 9. Submission timeline (Option 3)

```
Now → +5 days:    R9 + R10 parallel execution
+5 → +7 days:     R9 + R10 integration; Gemini hostile-v2 audit
+7 → +10 days:    Final read-through + cover letter polish
+10 days:         Submission-ready (pending PhD defense gate)

If 8×40GB cross-arch returns mid-window: integrate as new evidence.
If PhD measured-D2D arrives mid-window: integrate Supp Note S-HW.
If both arrive: this is the dream submission package.

Once PhD defense clearance: SUBMIT.
```

---

## 10. Dispatches issued

1. `DISPATCH_CODEX_R10_EXPERIMENTS_20260425.md` — A+B+D+E (multi-seed, mechanism, NL sweep, AIHWKit)
2. `DISPATCH_KIMI_R10_CHARACTERIZATION_20260425.md` — C+F+H (OPECT stats, freshness audit, energy provenance)
3. `DISPATCH_KIMI_R10_FRAMING_20260425.md` — G+I (novelty contrast, scenarios reframing)
4. `BROADCAST_ROUND10_LAUNCH_20260425.md` — master broadcast + venue memo

R10J venue strategy I do directly in the broadcast — not a separate dispatch.

---

## 11. One-line

Round-10 = 10-sub-track substantive completion (multi-seed canonical, mechanism, OPECT stats, NL sweep, AIHWKit baseline, freshness audit, novelty contrast, energy provenance, scenarios reframing, venue strategy) over 7-10 days, ~40 GPU-h local, in parallel with R9 presentation hardening + R8 W2 Phase 2 + 8×40GB cross-arch. Closes 11 reviewer attack vectors before submission.
