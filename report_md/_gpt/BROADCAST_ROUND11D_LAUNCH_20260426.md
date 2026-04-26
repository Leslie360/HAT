# BROADCAST ROUND-11D — Path C Exploration Launch
**Date:** 2026-04-26 16:50 CST
**From:** Claude (Chief Architect)
**To:** DeepSeek, Kimi, Gemini, User
**Authority:** CLAUDE_ROUND11D_PATH_C_EXPLORATION_PLAN
**Status:** ACTIVE — running parallel with R11A/B/C role-reassignment

---

## 0. User decision: Path C 比较好，我们应该更多探索

R10E AIHWKit baseline: **87.34 ± 0.14%** > our Ensemble HAT: 86.16 ± 0.19%. User chose to explore — search for regime where Ensemble HAT > AIHWKit (or honestly accept Path A reframing if no such regime exists).

---

## 1. Round-11D — multi-track exploration

### Experiments (DeepSeek, ~5-7 days, 50-60 GPU-h)
| Track | Stress regime | Hypothesis |
|:--|:--|:--|
| R11D-1 | AIHWKit at 4-bit precision | AIHWKit may collapse at our paper's 4-bit cliff while Ensemble HAT survives |
| R11D-2 | AIHWKit at σ=0.20 | AIHWKit per-batch noise saturates at high σ |
| R11D-3 | AIHWKit at σ=0.30 (cond.) | Confirm collapse pattern |
| R11D-4 | AIHWKit with PCM device model | Realistic non-linear pulse update closer to NL=2.0 |
| R11D-6 | Ensemble HAT @ AIHWKit-matched cadence (cond.) | Test if cadence is the lever, not the architecture |

### Theory + text (Kimi, ~2 days)
| Track | Output |
|:--|:--|
| R11D-5 | Cadence operational comparison (memo) |
| R11D-T1 | Theoretical addendum to KIMI-THEORY-2 (per-batch vs per-epoch) |
| Discussion text | AIHWKit comparison paragraph (3 outcome branches ready) |

### Figures (Gemini, ~1-2 days, after experiments land)
| Track | Output |
|:--|:--|
| R11D-T2 | Method operating-envelope plot (4 methods × stress regimes) |
| Side | AIHWKit comparison bar chart |

---

## 2. Decision rules (after R11D lands)

| Outcome | Story |
|:--|:--|
| AIHWKit collapses at high σ / 4-bit / PCM, Ensemble HAT survives | **Method-superiority restored** — novelty strong |
| AIHWKit survives everywhere | **Path A reframing** — diagnosis + theory + substrate (NOT method-superiority) |
| Mixed | **Targeted method-superiority** in specific regimes |

My prediction: ~70% chance AIHWKit breaks at 4-bit OR PCM. Worth the experiment.

---

## 3. Resource budget

- DS GPU: ~50-60 GPU-h over 5-7 days (puts ~50% pressure on local GPU; W2 P2 reduced to ~20% during this window)
- Kimi text: ~2 days theory + 4-6 hours integration; interleaves with R11C paper fix-it
- Gemini figs: ~1-2 days after data lands
- Submission timeline: extends ~1 week (was 3-5 days, now ~10-14 days)

User accepted this trade-off in choosing Path C.

---

## 4. Sequencing with Round-11A/B/C

```
NOW:
  DS:    starts R11D-1 (AIHWKit 4-bit) — also takes over Codex GPU role per R11A
  Kimi:  starts R11D-5 cadence comparison — interleaves with R11C paper fix-it
  Gemini: starts R11B-1 figure inventory + R11D-T2 envelope plot prep

Day 2-3:
  DS:    R11D-2 σ=0.20 + R11D-3 σ=0.30 if conditional fires
  Kimi:  R11D-T1 theory addendum + R11C continues
  Gemini: figure inventory + plot iteration

Day 4-5:
  DS:    R11D-4 PCM + R11D-6 conditional
  Kimi:  Discussion AIHWKit paragraph (post-data)
  Gemini: envelope plot finalization

Day 6-7:
  Claude: Round-11 integration pass (R11A+B+C+D)
  Decision: Path A vs B based on R11D outcome

Day 8-10:
  Final compile + Gemini hostile-v2
  Submission-ready
```

---

## 5. Dispatches

| File | Owner |
|:--|:--|
| `CLAUDE_ROUND11D_PATH_C_EXPLORATION_PLAN_20260426.md` | Claude (master) |
| `DISPATCH_DS_R11D_AIHWKIT_EXPLORATION_20260426.md` | DeepSeek |
| `DISPATCH_KIMI_R11D_THEORY_TEXT_20260426.md` | Kimi |
| `DISPATCH_GEMINI_R11D_ENVELOPE_PLOT_20260426.md` | Gemini |
| `BROADCAST_ROUND11D_LAUNCH_20260426.md` | This file |

Plus existing R11A/B/C dispatches still in flight:
- `DISPATCH_DS_R11A_GPU_TAKEOVER_20260426.md`
- `DISPATCH_GEMINI_R11B_FIGURE_PIPELINE_20260426.md`
- `DISPATCH_KIMI_R11C_PAPER_FIXIT_20260426.md`

---

## 6. Frozen decisions

All 12 frozen decisions in `CLAUDE_FORWARD_ROADMAP §10` still hold.

**New (R11D-specific)**:
- Discussion will include AIHWKit comparison (no longer optional)
- Novelty framing depends on R11D outcome
- Operating envelope plot becomes paper figure
- Submission timeline extends ~1 week — accepted in exchange for stronger evidence

---

## 7. Agent-level instructions

### DeepSeek
- **Now**: start R11D-1 (4-bit AIHWKit) ASAP
- **Bandwidth**: ~80% R11D + ~20% R11A residual (V3/V4 ablation resume + R10E monitoring)
- **GPU contention**: pause Round-8 W2 P2 until R11D closes (W2 has months of buffer)

### Kimi
- **Now**: R11D-5 cadence code comparison (4-6 hours)
- **Day 2-3**: R11D-T1 theory addendum
- **Days 4-5**: AIHWKit Discussion paragraph (post-data)
- **Bandwidth split**: ~40% R11D + ~60% R11C paper fix-it (still highest priority)

### Gemini
- **Now**: R11B-1 figure inventory + R11D-T2 plot prep (data not yet available)
- **Days 4-5**: actual plot rendering once data lands
- **Hostile review v2**: still gated on R11C + R11D both closing

### Claude (me)
- **Days 1-5**: monitor + escalation handling
- **Days 6-7**: integration pass
- **Days 8-10**: final read + submission prep
- **Days 10+**: pending PhD defense gate

---

## 8. One-line

Round-11D = Path C exploration: 5 AIHWKit stress experiments + cadence theory + operating envelope plot, ~7-10 days, may restore method-superiority story OR honestly reframe Path A. Either outcome is publishable and stronger than not-asking. Submission timeline extends ~1 week.
