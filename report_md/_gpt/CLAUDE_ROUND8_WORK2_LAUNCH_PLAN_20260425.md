# CLAUDE ROUND-8 WORK 2 LAUNCH PLAN
**Date:** 2026-04-25 22:50 CST
**From:** Claude (Chief Architect)
**Trigger:** User directive "继续推进新工作 + 现在做 work2 实验的推进吗" + paper-1 data locked
**Authority:** This file (supersedes Work 2 deferral in NARRATIVE_PIVOT §8 — Work 2 was scheduled to start "after paper-1 submitted"; user's "继续推进新工作" advances it now)
**Status:** ACTIVE — Round-8 = Work 2 experimental launch

---

## 0. Decision

**Start Work 2 KV-cache experimental program NOW** in two-track discipline:
- **Track A (Work 2 main, this dispatch)**: Codex + Kimi build Phase W0+W1 over 2-3 weeks
- **Track B (paper-1 standby, unchanged)**: Kimi/Gemini reserve capacity to react to 8×40GB return + PhD data triggers. Work 2 must NOT cannibalize paper-1 finish-line readiness.

**What changes in NARRATIVE_PIVOT §8:** "Work 2 starts only after paper-1 submitted" → "Work 2 begins infrastructure phase NOW; experiments staged so the preview section in paper-1 §5.9 can be backfilled with real data when 8×40GB returns + R3-1 ch5 gates close."

---

## 1. Why now (revised from §8 deferral)

When NARRATIVE_PIVOT §8 was written, the assumption was paper-1 submission was weeks away. Reality is months (PhD-graduation-gated). The buffer changes the calculus:

- Local GPU is **idle** (paper-1 all local jobs done)
- 8×40GB remote on independent track (paper-1 cross-arch validation)
- Months of buffer means starting Work 2 now lets it be **substantive** by paper-1 submission, not just an outlook
- KV-cache is the hot 2025-2026 deployment problem — competitive timing matters
- Two papers stronger than one (lab signaling + venue diversification)

**What does NOT change**: paper-1 narrative, venue, gates, frozen decisions. Track B stays primary.

---

## 2. Work 2 scope (revised from CLAUDE_WORK2_DIRECTION_LOCK_20260423)

**Original scope** (CLAUDE_WORK2_DIRECTION_LOCK): full KV-cache analog CIM for long-context transformer decoding, multi-layer attention path, LLaMA-variant decode benchmark, energy/latency at 1024+ tokens.

**Round-8 staged scope** (this plan):

| Phase | What | Deliverable | Gates Phase |
|:--|:--|:--|:--|
| **W0** (Days 1-3) | Testbed pick + scope freeze | `WORK2_TESTBED_DECISION_20260425.md` + scoping spec | Phase W1 ready |
| **W1** (Days 4-14) | KV-cache analog mapping infrastructure | Code + smoke test passing | Phase W2 ready |
| **W2** (Days 15-28) | Baseline + Standard HAT + Ensemble HAT on small LLM testbed | First per-layer fresh-instance numbers on attention path | Paper-1 §5.9 preview backfill OR Work 2 Round-2 plan |
| W3+ | Long-context decode + energy + benchmarks | Paper-2 main results | Future rounds |

This dispatch fires W0 + W1 + W2 (~4 weeks total). W3+ planned in Round-9 after W2 lands.

---

## 3. Testbed candidates (W0 decision)

User picks; I recommend below.

| Candidate | Params | Why | Why not |
|:--|--:|:--|:--|
| **TinyLlama 1.1B** ⭐ recommended | 1.1B | Established baseline, fits comfortably on local 24GB GPU, decoder-only, clean attention | Smaller than "real" LLM |
| Pythia 410M / 1B / 1.4B | 0.4-1.4B | Open weights, good documented baselines, simpler architecture | Less attention to KV-cache optimization |
| GPT-2 small (124M) | 0.124B | Tiny, fits anywhere, fast iteration | Too small to be representative of "LLM deployment" |
| LLaMA-2 7B | 7B | Real LLM scale | Doesn't fit on local; needs 8×40GB |
| Mistral 7B | 7B | Modern attention (sliding window, GQA) | Same memory problem |

**My recommendation: TinyLlama 1.1B for W1+W2, then upgrade to LLaMA-2 7B for W3+ on 8×40GB if/when remote returns.**

Rationale:
- Local GPU compatibility (need to keep running)
- Established benchmark numbers (perplexity on WikiText, GSM8K, MMLU)
- Decoder-only with KV-cache (correct architectural target)
- 22 layers × hidden 2048 — enough to test multi-layer KV-cache analog mapping
- TinyLlama-Chat exists for instruction-following metrics
- Architecture similar enough to Llama-2/Mistral that scaling story is credible

---

## 4. Phase W0 deliverables (Day 1-3)

### 4.1 Testbed decision lock
- Pick + justify (TinyLlama 1.1B unless user signals otherwise)
- Document acceptance criteria (e.g., "preliminary success = Ensemble HAT recovers > 90% of baseline perplexity on attention-only-analog config under canonical 5%C2C/10%D2D/4-bit/NL=1.0")

### 4.2 Architectural mapping spec
- Diagram: which weights go analog vs digital
- Decision: analog the QKV projections, output projection, MLP up/down/gate? Or only QKV first?
- Decision: KV-cache itself (the stored K/V tensors during decode) — analog conductance bank or digital memory? **Critical question — this is the actual Work 2 novelty.**
- Decision: layernorm + rotary embedding stay digital (consistent with paper-1)
- Energy/latency target metrics

### 4.3 Benchmark suite pick
- Perplexity (WikiText-103) — baseline
- Long-context decode (1024 / 2048 / 4096 tokens) — KV-cache stress test
- (Optional) GSM8K accuracy — instruction-following degradation

---

## 5. Phase W1 deliverables (Day 4-14)

### 5.1 Codex infrastructure
- Extend `analog_layers.py` to support attention-path layers
  - QKV projection wrapper
  - Output projection wrapper
  - **NEW**: KV-cache analog wrapper (stored K/V as conductance, read with D2D+C2C noise per access)
- Write `train_llm_hybrid.py` (analogous to `train_tinyvit_ensemble.py`)
- Write `eval_llm_kv_cache.py` for perplexity + long-context eval
- Smoke test: TinyLlama loads, hybrid conversion runs, no NaN forward pass

### 5.2 Kimi paper-2 outline
- Adapt KIMI-THEORY-1/2 derivation to attention path
  - Does the implicit gradient-L2 regularizer change for QKV projections?
  - How does Ensemble HAT interact with softmax (nonlinear)?
- Draft paper-2 abstract + outline + section skeletons (`paper2/`)
- Identify novel claims unique to attention path (vs paper-1 MLP path)

---

## 6. Phase W2 deliverables (Day 15-28)

### 6.1 Codex experimentation
- Baseline TinyLlama fresh perplexity (FP32, no analog)
- Apply hybrid analog conversion to QKV (no KV-cache analog yet)
- Standard HAT vs Ensemble HAT, fresh-instance eval (10 instances × 5 MC, similar to paper-1)
- Add KV-cache analog and re-run
- Compare degradation patterns to paper-1 MLP findings

### 6.2 Kimi documentation
- Land first results into `paper2/results.tex.kimi_draft`
- Compare to paper-1 §5.5-5.6 patterns (does the diagnostic-treatment story extend?)

### 6.3 Decision point at end of W2
- If results align with paper-1 pattern → backfill paper-1 §5.9 preview with real numbers; continue Work 2 toward full paper
- If results diverge → publish as Work 2 standalone with the surprising finding; paper-1 §5.9 stays preview-only

---

## 7. Two-track discipline (CRITICAL)

| Trigger | Track A response | Track B response |
|:--|:--|:--|
| 8×40GB cross-arch returns | Pause W2 if collision; integrate cross-arch first | Kimi drafts cross-arch supplementary |
| PhD data lands | No effect | Codex runs R-D0 ingest pipeline ASAP |
| Codex W2 hits blocker | Document blocker, ask user | No effect |
| User says "submit paper-1 now" | Halt W2 immediately, Codex shifts to paper-1 polish | Kimi finalizes manuscript |
| W2 reveals paper-1 narrative issue | ESCALATE — possibly reopen NARRATIVE_PIVOT | — |

**Hard rule:** Paper-1 finish-line readiness comes first. Work 2 is opportunistic infrastructure investment.

---

## 8. Resource allocation

| Resource | Track A (Work 2) | Track B (paper-1 standby) |
|:--|:--|:--|
| Local GPU | ~70% (Codex W2 work) | ~30% (reserved for trigger response) |
| Codex bandwidth | ~80% Work 2 infrastructure | ~20% paper-1 trigger response |
| Kimi bandwidth | ~50% paper-2 outline + theory | ~50% paper-1 cross-arch / measured-D2D when triggers fire |
| Gemini bandwidth | 0% (Work 2) | 100% standby for G-HOSTILE-V2 + paper-1 escalations |
| Claude bandwidth | ~60% Work 2 architecting | ~40% paper-1 integration when triggers land |

---

## 9. What stays unchanged

- **NARRATIVE_PIVOT** for paper-1 (§1-§7 narrative spine intact; §8 Work 2 timing now revised to "infrastructure now, full results later")
- **Zone partition 3A/3B/3C**
- **Nature Electronics** as paper-1 venue
- **PhD-graduation gate** for paper-1 submission
- **No retraining** of paper-1 checkpoints
- **Git push strategy** (main repo local; handoff repo for GitHub mirror)
- **All 12 frozen decisions** in CLAUDE_FORWARD_ROADMAP §10

---

## 10. Other directions considered + why deferred

User asked which of the previously-discussed directions are suitable. Here's the triage:

| Direction | Decision | Reason |
|:--|:--|:--|
| **Work 2 KV-cache experimental** | ✅ START NOW | Highest-leverage; uses idle local GPU; competitive timing |
| Cross-arch ViT-Small/DeiT-Small | ✅ ALREADY RUNNING | 8×40GB remote independent track |
| Measured-D2D ingest | ⏳ GATED | PhD data trigger |
| Theory deepening v3 | ❌ DEFER | Diminishing returns after Phase 1 (Theory v2 done) |
| Energy modeling deepening (SPICE) | ❌ DEFER | Out-of-scope for paper-1; would take months |
| Cross-dataset extension | ❌ DEFER | Cross-arch on TinyImageNet already covers this concern |
| Hostile review v2 | ⏳ GATED | Needs full integrated paper |
| BFG GitHub history rewrite | ❌ DEFER | Paper-1 doesn't need it; user can request when ready |

---

## 11. Dispatches issued

1. `DISPATCH_CODEX_W2_PHASE0_INFRASTRUCTURE_20260425.md` — testbed pick + Phase W0/W1 infra
2. `DISPATCH_KIMI_W2_PAPER_OUTLINE_20260425.md` — paper-2 abstract + outline + theory adaptation
3. `BROADCAST_ROUND8_WORK2_LAUNCH_20260425.md` — master broadcast

---

## 12. Escalation triggers (for Round-8)

- **W0 testbed pick blocked** (e.g., TinyLlama license issue): user signal needed for alternative
- **W1 KV-cache analog wrapper has unsolvable issue** (e.g., gradient flow through cached tensor breaks): ESCALATE; possibly requires different architectural approach
- **W2 results show framework does NOT extend to attention** (Standard HAT collapses similarly to paper-1, but Ensemble HAT does NOT recover): MAJOR ESCALATION; paper-1 §5.9 preview claim wrong; reopen NARRATIVE_PIVOT
- **W2 results show framework extends in surprising new way** (e.g., new failure mode unique to KV-cache): GOOD NEWS; paper-2 narrative gains depth

---

## 13. Timeline

```
Week 1 (today → 2026-05-02):
  Codex: W0 testbed lock + W1 infrastructure scaffold
  Kimi:  W0 mapping spec + paper-2 outline draft
  
Week 2 (2026-05-03 → 2026-05-09):
  Codex: W1 finish (smoke test passing on TinyLlama hybrid)
  Kimi:  Paper-2 theory adaptation
  [Possible 8×40GB return mid-week — Track B activates]
  
Week 3 (2026-05-10 → 2026-05-16):
  Codex: W2 baseline + Standard HAT
  Kimi:  Paper-2 results.tex.kimi_draft skeleton
  
Week 4 (2026-05-17 → 2026-05-23):
  Codex: W2 Ensemble HAT + KV-cache analog
  Kimi:  Paper-2 first results landed
  [Decision point: pattern-aligns or pattern-diverges]
```

---

## 14. One-line

Work 2 KV-cache experimental program launches Round-8 in two-track discipline: Codex + Kimi build infrastructure + theory + first results over 4 weeks on TinyLlama 1.1B local testbed; paper-1 standby capacity reserved for trigger response; Work 2 cannot cannibalize paper-1 finish-line.
