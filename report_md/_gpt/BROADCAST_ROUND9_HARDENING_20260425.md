# BROADCAST ROUND-9 — Paper-1 Presentation Hardening
**Date:** 2026-04-25 22:30 CST
**From:** Claude (Chief Architect)
**To:** Kimi, Codex, Gemini, User
**Authority:** CLAUDE_ROUND9_PAPER1_HARDENING_PLAN_20260425
**Status:** ACTIVE — three parallel tracks; Round-8 W2 + 8×40GB cross-arch unaffected

---

## 0. User audit (verbatim, captured for accountability)

> "paper1 还是很脆弱，我觉得示意图丑陋，数据示例不清晰，审批意见也没底，同时废话过多，工作量不多确篇幅过长"

**Diagnosis (data-backed):**
- Body 7,332 words (target Nat Elec: 5,000-5,500) — **28% bloat**
- 3 schematic figures are 24-34KB matplotlib auto-output, no TikZ source
- 5 reviewer attack vectors only partially defended (hardware fidelity, 5pp gap, ε_MAC, OPECT single-source, ImageNet absence)
- Intro/Related Work redundancy: 70% content overlap

User correct on every point. Round-9 is the surgical fix.

---

## 1. Three parallel tracks

| Track | Owner | What | Time |
|:--|:--|:--|:--|
| **A** | Kimi | Length surgery: 7,332 → 5,500 words (-28%) with line-level cut targets | 3-4 days |
| **B** | Codex | TikZ rebuild of fig1/fig2/figS3 (replace matplotlib quick-draws) | 5-7 days |
| **C** | Kimi + Gemini | 5 defense paragraphs against reviewer attack vectors | 2-3 days (after A) |

All 3 parallel. No resource conflicts with Round-8 W2 Phase 2 (Codex GPU work) or 8×40GB cross-arch (independent infra).

---

## 2. Dispatches issued

| File | Owner |
|:--|:--|
| `CLAUDE_ROUND9_PAPER1_HARDENING_PLAN_20260425.md` | Claude (master plan) |
| `DISPATCH_KIMI_R9A_LENGTH_SURGERY_20260425.md` | Kimi |
| `DISPATCH_CODEX_R9B_TIKZ_SCHEMATICS_20260425.md` | Codex |
| `DISPATCH_KIMI_GEMINI_R9C_DEFENSE_20260425.md` | Kimi + Gemini |

Each dispatch has **line-level specificity** — not "trim a bit" but "delete intro §3-§5, compress §6+§7 to one paragraph, target ~450 words." Kimi/Codex/Gemini execute mechanically.

---

## 3. Track A — Length surgery (highlights)

| Section | Current | Target | Cut |
|:--|--:|--:|--:|
| Introduction | 784 | 450 | **-334 (-43%)** |
| Related Work | 696 | 350 | **-346 (-50%)** |
| Methodology | 1,164 | 1,000 | -164 |
| Results | 1,542 | 1,100 | **-442 (-29%)** |
| Discussion | 1,089 | 750 | **-339 (-31%)** |
| Appendix | 1,200 | 800 | -400 |
| **Body total** | **7,332** | **5,200** | **-2,025 (-28%)** |

**Strategy**: remove duplications (intro re-states related work re-states methodology re-states results), remove transition filler ("We now show..."), move mechanism paragraphs to supplementary.

---

## 4. Track B — TikZ schematics (3 figures)

| Figure | Current | Target |
|:--|:--|:--|
| fig1 system architecture | 24KB matplotlib | 200-400KB TikZ, 3-panel (device / array / network) |
| fig2 weight mapping | 34KB matplotlib | 200-400KB TikZ, 7-stage flow (W → quantize → diff pair → noise → MAC → ADC → recovery) |
| figS3 Ensemble HAT concept | 32KB matplotlib | 200-400KB TikZ, 2-panel (Standard fixed mask vs Ensemble per-epoch resample) |

**Aesthetic reference**: Sebastian 2018 Nat Comm, Burr 2017 IEEE TED, Rasch 2023 IBM AIHWKit, Foret 2021 ICLR SAM. Match cleanliness/professionalism; don't copy.

---

## 5. Track C — 5 defense paragraphs

| ID | Attack | Defense location |
|:--|:--|:--|
| D1 | "No silicon validation" | Discussion §6.4 Limitations |
| D2 | "5pp severe-NL gap" | Discussion §6.5 Outlook |
| D3 | "Energy ε_MAC arbitrary" | Discussion §6.4 Limitations |
| D4 | "OPECT single-source" | Results §5.8 OPECT case study |
| D5 | "Only CIFAR/Flowers" | Discussion §6.4 Limitations |

**+ ~500 words; net post-A target = 5,600 words, within Nat Elec envelope.**

Gemini cross-reviews each defense for hostile-reviewer perspective. If any defense ineffective: Kimi revises, Gemini re-audits, max 2 iterations.

---

## 6. Sequencing

```
Day 1:
  [Kimi]  Track A: cuts intro + related work (highest-redundancy first)
  [Codex] Track B: starts fig1 TikZ design
  [Gemini] Standby for Track C audit

Day 2-3:
  [Kimi]  Track A: cuts results + discussion + appendix
  [Codex] Track B: iterates fig1 + fig2

Day 4-5:
  [Kimi]  Track A finishes; starts Track C (defense paragraphs)
  [Codex] Track B: figS3 + integration test
  [Gemini] Track C: hostile audit each defense

Day 6-7:
  [Kimi]  Track C finalizes
  [Codex] Track B finalizes
  [Claude] Integration pass: A+B+C → manuscript
  
Day 8+:
  Compile + verify ≤ 5,700 words + figures embed cleanly
  Optional: G-HOSTILE-V2 trigger if all-clear
  Commit + push
```

Critical path: Track A (text writing is sequential).

---

## 7. Acceptance criteria for Round-9 closure

| Criterion | Threshold |
|:--|:--|
| Body word count | ≤ 5,500-5,700 |
| Figure quality | fig1/fig2/figS3 are vector TikZ ≥150KB each |
| Defense paragraphs | 5 deployed; Gemini audit ≤ 2 unaddressed attack vectors |
| Manuscript compile | RC 0, zero warnings, zero undefined refs |
| Reviewer-readiness | Claude final read declares submission-ready |

If any criterion fails: pause integration, dispatch fix, re-converge.

---

## 8. What stays unchanged

- NARRATIVE_PIVOT (zone partition + 3-scenario evidence spine)
- All numerical claims (no number changes)
- Venue: Nature Electronics
- PhD-graduation submission gate
- Round-8 Work 2 launch (Codex Track B is small TikZ; W2 Phase 2 GPU work continues)
- 8×40GB cross-arch paper-1 work continues independently

---

## 9. Agent-level instructions

### Kimi
- **Days 1-4**: Track A length surgery (highest priority)
- **Days 5-6**: Track C defense paragraphs (after A)
- **Output**: edits to canonical `.tex` files (not sidecars — direct edit, single integration pass for Round-9)

### Codex
- **Days 1-7**: Track B TikZ rebuild (parallel to Kimi A+C)
- **Bandwidth**: ~20% of total (W2 Phase 2 still needs ~80%)
- **Output**: TikZ source + compiled PDFs

### Gemini
- **Days 4-6**: Track C hostile audit each Kimi defense paragraph
- **After all 3 tracks close**: G-HOSTILE-V2 trigger fires (revised: no longer wait for cross-arch + measured-D2D)
- **Output**: hostile audit reports + final-paper hostile-review-v2 simulation

### Codex (parallel Round-8 W2)
- W2 Phase 2 GPU work continues (Pythia 410M Standard HAT + Ensemble HAT training)
- Round-9B is CPU-only TikZ; no contention

### 8×40GB
- Paper-1 cross-arch (ViT-Small/DeiT-Small TinyImageNet) continues independently
- No interaction with Round-9

---

## 10. Escalation triggers

- **Track A** Kimi cuts kill important content → ESCALATE; Claude restores minimum viable version
- **Track B** Codex TikZ takes >10 days OR aesthetic insufficient → fallback to high-quality matplotlib
- **Track C** Gemini hostile review finds NEW attack vector → ESCALATE; possibly new experiments
- **Compile breaks** at integration → halt; trace per-track

---

## 11. One-line

Round-9 = three parallel tracks (cut 28% words / TikZ rebuild 3 schematics / 5 defense paragraphs) over 5-7 days; closes paper-1 from "scientifically solid but presentation-cluttered" to "Nat-Electronics-submission-ready"; Round-8 W2 + 8×40GB cross-arch tracks unaffected.
