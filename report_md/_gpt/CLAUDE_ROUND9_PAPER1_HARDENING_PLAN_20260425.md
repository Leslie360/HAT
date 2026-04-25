# CLAUDE ROUND-9 — Paper-1 Hardening Plan
**Date:** 2026-04-25 22:30 CST
**From:** Claude (Chief Architect)
**Trigger:** User audit: "示意图丑陋 / 数据示例不清晰 / 审批意见也没底 / 废话过多 / 工作量不多确篇幅过长"
**Authority:** This file
**Status:** ACTIVE — three parallel hardening tracks

---

## 0. Diagnosis (data, not opinion)

| Concern | Evidence | Root cause |
|:--|:--|:--|
| 篇幅过长 | Body 7,332 words; target 5,000-5,500 for Nat Electronics | Intro repeats 70% of Related Work; contribution stated 2× |
| 示意图丑陋 | fig1/fig2/figS3 are 24-34KB matplotlib auto-output | No TikZ/Inkscape sources; mid-April quick-draws never replaced |
| 审批信心不足 | 5 attack vectors only partially defended | Hardware validation, ε_MAC placeholder, OPECT single-source, residual 5pp gap, ImageNet absence |
| 数据示例不清晰 | Tables in §5.7 + appendix scan poorly | Stage-2 ADC numbers spread across 3 tables; iso-accuracy contour lacks call-out |

**Verdict**: paper is technically solid (post-Round-7 sprint), but **presentation quality lags content quality**. Round-9 closes that gap.

---

## 1. Three parallel tracks

### Track A — Length surgery (Kimi)
- 7,332 → ~5,200 words (-28%)
- Specific section caps + line-level cut targets
- Removes intro/related-work redundancy + results/discussion bloat
- **Time**: 3-4 days
- **Risk**: very low (cuts only, no new content)

### Track B — TikZ schematic rebuild (Codex)
- fig1 system architecture, fig2 weight mapping, figS3 Ensemble HAT concept
- Clean TikZ source (git-friendly, reproducible)
- 3-panel system architecture, flow diagram for weight mapping, side-by-side concept for Ensemble HAT
- **Time**: 5-7 days
- **Risk**: medium (TikZ aesthetics need iteration); fallback to better matplotlib if TikZ takes too long

### Track C — Reviewer-confidence hardening (Kimi + Gemini)
- 5 short defense paragraphs (Hardware fidelity / 5pp gap / ε_MAC / OPECT single-source / ImageNet absence)
- Pre-rebuttal honest framing, not new science
- Gemini cross-reviews each defense for hostile-reviewer simulation
- **Time**: 2-3 days
- **Risk**: very low

---

## 2. Parallel resource allocation

| Resource | Track A | Track B | Track C | Track D (W2 ongoing) | Track E (8×40GB) |
|:--|:--:|:--:|:--:|:--:|:--:|
| Kimi bandwidth | 70% | 0% | 30% (with Gemini review) | 0% | 0% |
| Codex bandwidth | 0% | 80% TikZ | 0% | 20% (W2 Phase 2 cont.) | 0% |
| Gemini bandwidth | 0% | 20% (figure aesthetic review) | 80% (defense review + hostile-v2 trigger watch) | 0% | 0% |
| Local GPU | 0% | 0% | 0% | 100% (W2 already running) | 0% |
| 8×40GB | 0% | 0% | 0% | 0% | 100% (paper-1 cross-arch) |

No resource conflicts. All five tracks parallel.

---

## 3. Dependencies + sequencing

```
Day 1-2:
  Track A: Kimi cuts intro + related work first (highest redundancy)
  Track B: Codex starts fig1 TikZ design
  Track C: Kimi drafts 5 defense paragraphs in parallel (low cognitive switching cost)

Day 3-4:
  Track A: Kimi cuts results + discussion + appendix
  Track B: Codex iterates fig1 + starts fig2
  Track C: Gemini cross-reviews defense paragraphs

Day 5-7:
  Track A: Final compile test, word-count verification
  Track B: Codex finishes figS3, all 3 figures integrated
  Track C: Final defense integration into manuscript

Day 7+:
  Claude integration pass: A + B + C output → manuscript
  Recompile main.tex; verify <5,500 words; figures embed cleanly
  Commit + push
```

Critical path: Track A drives total timeline (writing prose is sequential). Track B/C can land out of order.

---

## 4. Acceptance criteria for Round-9 closure

| Criterion | Threshold |
|:--|:--|
| Body word count | ≤ 5,500 |
| Figure quality | fig1/fig2/figS3 are vector TikZ, ≥150KB each (vs current 24-34KB matplotlib) |
| Defense paragraphs | 5 deployed; Gemini hostile-review v2 simulates reviewer; <2 unaddressed attack vectors |
| Manuscript compile | RC 0, zero warnings, zero undefined refs |
| Reviewer-readiness | Claude final read-through declares submission-ready |

If any criterion fails: pause integration, dispatch fix, re-converge.

---

## 5. What stays unchanged

- NARRATIVE_PIVOT (zone partition + 3-scenario evidence spine)
- All numerical claims (no number changes; only presentation polish)
- Venue: Nature Electronics
- PhD-graduation submission gate
- Round-8 Work 2 launch unchanged (Codex Track B is small; W2 Phase 2 GPU work continues)
- 8×40GB cross-arch paper-1 work unchanged

---

## 6. Dispatches

1. `DISPATCH_KIMI_R9A_LENGTH_SURGERY_20260425.md` — line-level cut targets
2. `DISPATCH_CODEX_R9B_TIKZ_SCHEMATICS_20260425.md` — 3 TikZ figures with design specs
3. `DISPATCH_KIMI_GEMINI_R9C_DEFENSE_20260425.md` — 5 defense paragraphs + hostile-review v2 trigger
4. `BROADCAST_ROUND9_HARDENING_20260425.md` — master broadcast

---

## 7. Escalation triggers

- Track A: Kimi cuts kill important content → ESCALATE; Claude re-establishes minimum viable version
- Track B: Codex TikZ takes >10 days → fallback to high-quality matplotlib (decent fallback exists)
- Track C: Gemini hostile review finds NEW attack vector → ESCALATE; possibly new experiments
- Compile breaks at integration → halt; trace per-track

---

## 8. One-line

Round-9 = parallel paper-1 hardening (length surgery + TikZ rebuild + reviewer defense) over 5-7 days; no resource conflicts with Round-8 Work 2 or 8×40GB cross-arch tracks.
