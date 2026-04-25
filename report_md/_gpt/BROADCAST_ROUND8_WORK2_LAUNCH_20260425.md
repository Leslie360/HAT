# BROADCAST ROUND-8 — WORK 2 KV-CACHE EXPERIMENTAL LAUNCH
**Date:** 2026-04-25 23:00 CST
**From:** Claude (Chief Architect)
**To:** Kimi, Codex, Gemini, User
**Authority:** CLAUDE_ROUND8_WORK2_LAUNCH_PLAN_20260425
**Status:** ACTIVE — Round-7 (paper-1 sprint) closed → Round-8 (Work 2 launch) opened

---

## 0. Headline

User directive: paper-1 data locked + continue with new work + asked whether to push Work 2 experiments.

**Decision: YES start Work 2 NOW** in two-track discipline:
- **Track A (Work 2 main, NEW)**: Codex builds KV-cache analog infrastructure on Pythia 410M local testbed; Kimi drafts paper-2 outline + theory adaptation. 2-track 4-week launch (W0+W1+W2).
- **Track B (paper-1 standby, unchanged)**: All paper-1 trigger response capacity reserved. Paper-1 finish-line readiness comes first if 8×40GB return / PhD data / submit-now signals fire.

---

## 1. Why Work 2 now (revised from NARRATIVE_PIVOT §8)

When NARRATIVE_PIVOT §8 was written, it deferred Work 2 to "after paper-1 submitted". Reality is: paper-1 submission is months away (PhD-graduation-gated), local GPU is idle, 8×40GB is on independent track. Sitting on idle local GPU for months wastes the buffer.

Starting Work 2 NOW:
- Local GPU productively used during paper-1 wait
- Substantive Work 2 results by paper-1 submission, not just outlook
- Competitive timing — KV-cache is hot 2025-2026 LLM deployment problem
- Two papers stronger than one (lab signaling + venue diversification)

What does NOT change: paper-1 narrative, venue, gates, all 12 frozen decisions in CLAUDE_FORWARD_ROADMAP §10.

---

## 2. Work 2 staged scope

| Phase | What | Time | Deliverable |
|:--|:--|:--|:--|
| W0 | Testbed pick + scope freeze + benchmark suite | 3 days | 3 spec docs |
| W1 | KV-cache analog infrastructure + smoke tests | 10 days | `paper2/src/` package + 3 passing tests |
| W2 | Baseline + Standard HAT + Ensemble HAT first results | 14 days | First fresh-instance numbers on attention path |
| W3+ | Long-context decode + energy + benchmarks | future rounds | Paper-2 main results |

**Round-8 scope = W0 + W1 + W2 (~4 weeks).** W3+ planned in Round-9 after W2 lands.

---

## 3. Testbed: Pythia 410M

Default pick (user can override):
- **Model**: `EleutherAI/pythia-410m-deduped` (HuggingFace, Apache 2.0; fits 16GB local with ~5GB peak training)
- **Why**: 24 layers × 16 heads × 1024 hidden, fits local 16GB GPU with AMP, established baselines, decoder-only KV-cache architecture, scaling to LLaMA-2/Mistral credible
- **Fallback**: `EleutherAI/pythia-1b-deduped`

---

## 4. Architectural mapping (Work 2 signature contribution)

What goes analog vs digital in Work 2:

| Component | Analog/Digital | Notes |
|:--|:--|:--|
| Embedding, RMSNorm, Softmax, Rotary | Digital | Same as paper-1 |
| **W_q / W_k / W_v / W_o (QKV+output projections)** | **Analog** | Same as paper-1 MLP-path discipline |
| **MLP gate/up/down** | **Analog** | Same as paper-1 |
| **🔥 KV-cache storage (persistent K/V for decode)** | **🔥 Analog (NEW)** | The Work 2 signature: stored as conductance, read with D2D persistent + C2C fresh-per-read noise |
| LM head | Digital initially | Tied to embedding |

The KV-cache analog wrapper is the actual Work 2 novelty (paper-1 only did inference-path MLP).

---

## 5. Benchmark suite

- Primary: WikiText-103 perplexity (single-pass)
- Secondary: WikiText-103 sliding-window decode at {128, 512, 1024, 2048} tokens (KV-cache stress test)
- Tertiary (optional): MMLU 5-shot (instruction-following degradation)

Same noise discipline as paper-1: σ_C2C = 5%, σ_D2D = 10%, NL = 1.0 canonical, 4-bit weights, 10 fresh × 5 MC.

---

## 6. Dispatches issued

| Dispatch | Owner | Phase | File |
|:--|:--|:--|:--|
| W2 Phase 0+1 Infrastructure | Codex | W0+W1 | `DISPATCH_CODEX_W2_PHASE0_INFRASTRUCTURE_20260425.md` |
| W2 Paper-2 Outline + Theory | Kimi | parallel to W0+W1 | `DISPATCH_KIMI_W2_PAPER_OUTLINE_20260425.md` |

W2 Phase 2 dispatch (Days 15-28) issues separately after W1 lands.

---

## 7. Two-track discipline (CRITICAL)

| Trigger | Track A (W2) action | Track B (paper-1) action |
|:--|:--|:--|
| 8×40GB cross-arch returns | Pause W2 if Codex collision; Kimi prioritizes integration | Kimi drafts cross-arch supplementary |
| PhD data lands | PAUSE W2; Codex runs R-D0 ingest pipeline ASAP | Resume after R-D0 |
| User signals "submit paper-1 now" | HALT W2 immediately | Codex shifts to paper-1 polish |
| W2 hits unsolvable blocker | Document + escalate to Claude | No effect |
| W2 reveals paper-1 narrative issue | ESCALATE — possibly reopen NARRATIVE_PIVOT | — |

**Hard rule**: Paper-1 finish-line readiness > Work 2 momentum.

---

## 8. Resource allocation

| Resource | Track A (Work 2) | Track B (paper-1) |
|:--|:--|:--|
| Local GPU | ~70% | ~30% reserved |
| Codex bandwidth | ~80% W2 infrastructure | ~20% paper-1 trigger response |
| Kimi bandwidth | ~50% paper-2 outline + theory | ~50% paper-1 cross-arch / measured-D2D when triggers fire |
| Gemini bandwidth | 0% (Work 2) | 100% standby for G-HOSTILE-V2 + paper-1 escalations |

---

## 9. Other directions previously discussed (triage decisions)

User asked me to pick suitable ones. Here's the full triage:

| Direction | Decision | Why |
|:--|:--|:--|
| **Work 2 KV-cache** | ✅ START NOW (this round) | Highest-leverage; idle GPU; competitive timing |
| Cross-arch ViT-Small/DeiT-Small | ✅ ALREADY RUNNING | 8×40GB independent track |
| Measured-D2D ingest | ⏳ GATED on PhD trigger | DATA_INGEST_PROTOCOL ready |
| Theory deepening v3 | ❌ DEFER | Diminishing returns after Theory v2 (Phase 1) |
| Energy modeling SPICE-deepening | ❌ DEFER | Out-of-scope for paper-1; months of work |
| Cross-dataset extension | ❌ DEFER | Cross-arch already covers this concern |
| Hostile review v2 | ⏳ GATED on full integration | Spec written; awaits trigger |
| BFG GitHub history rewrite | ❌ DEFER | Paper-1 doesn't need it; user-trigger only |

Work 2 is the natural next high-value direction; the rest are gated or deferred.

---

## 10. What stays unchanged

- NARRATIVE_PIVOT §1-§7 (paper-1 narrative spine intact)
- §8 Work 2 timing revised: "infrastructure now, full results before paper-1 submission"
- All 12 frozen decisions in CLAUDE_FORWARD_ROADMAP §10
- Zone partition 3A/3B/3C (+3W new for Work 2)
- Wording bans: no "post-fix"/"pre-fix"/"deployment-fidelity"/"bug-immune"
- Manuscript canonical files in `paper/` UNTOUCHED unless paper-1 trigger fires
- Work 2 work isolated in `paper2/` subdir — clean separation

---

## 11. Agent-level instructions

### Codex
- **NOW**: Phase W0 testbed lock + mapping spec + benchmark suite (3 days, ~0 GPU)
- **Then**: Phase W1 KV-cache analog wrapper + smoke tests (10 days, ~6 GPU-h)
- **Constraint**: Pause if 8×40GB cross-arch needs Codex bandwidth, PhD data lands, or user halts W2
- **Code lives in**: `paper2/src/` (clean separation from paper-1 root)

### Kimi
- **Stream A (Days 1-7)**: Theory adaptation for attention path (`paper2/supplementary/S_attention_theory.tex.kimi_draft`)
- **Stream B (Days 1-14)**: Paper-2 sections skeleton + abstract + intro + cover letter
- **Constraint**: Wait for Codex W0 mapping spec before finalizing Methodology section
- **Constraint**: No fake placeholder numbers; use vague "demonstrates" language until W2 lands

### Gemini
- **STAND BY**. No Work 2 audit task in Round-8.
- **Reactive role**: G-HOSTILE-V2 spec still holds; activates only when paper-1 fully integrates + cross-arch + measured-D2D land.
- **Optional cross-review**: if Kimi/Codex requests independent W2 architecture audit, Gemini can review. Otherwise hands off.

---

## 12. Timeline (no hard dates, milestones only)

```
Week 1 (today → 2026-05-02):
  Codex: W0 testbed lock + W1 infrastructure scaffold
  Kimi:  W0 mapping spec + paper-2 outline draft
  
Week 2 (2026-05-03 → 2026-05-09):
  Codex: W1 finish (smoke tests passing on Pythia hybrid)
  Kimi:  Paper-2 theory adaptation
  [Possible 8×40GB return mid-week → Track B activates]
  
Week 3 (2026-05-10 → 2026-05-16):
  Codex: W2 baseline + Standard HAT
  Kimi:  Paper-2 results.tex.kimi_draft skeleton
  
Week 4 (2026-05-17 → 2026-05-23):
  Codex: W2 Ensemble HAT + KV-cache analog
  Kimi:  Paper-2 first results landed
  → Decision point: pattern-aligns or pattern-diverges
```

---

## 13. Escalation triggers (Round-8 specific)

- **W0 testbed pick blocked**: user signal needed for alternative
- **W1 KV-cache wrapper has unsolvable issue** (e.g., gradient flow through cached tensor breaks): ESCALATE to Claude
- **W2 results show framework does NOT extend to attention** (Standard HAT collapses but Ensemble HAT also collapses): MAJOR ESCALATION; reopen NARRATIVE_PIVOT
- **W2 results show new failure mode unique to KV-cache**: GOOD NEWS; paper-2 narrative gains depth

---

## 14. Note on git push

Earlier attempt to push 6 paper-1 cleanup commits to `Leslie360/HAT.git master` was REJECTED (pack > 2GB; historical 445MB checkpoint blobs). Decision: keep main repo LOCAL-only as designed. Public mirror via existing handoff repo. Work 2 code in `paper2/` will need its own export path when ready (lightweight). Defer until W1 finishes.

---

## 15. One-line

"Round-7 paper-1 sprint closed; Round-8 Work 2 KV-cache experimental launch starts in two-track discipline; Codex builds infrastructure on Pythia 410M local while Kimi drafts paper-2 + theory; paper-1 finish-line readiness preserved as Track B priority."
