# CLAUDE — Work 2 Direction Lock
**Date:** 2026-04-23
**Architect:** Claude (Opus 4.7)
**Inputs read:**
- `THESIS_WORK2_RESEARCH_PLAN_20260423.md`
- `WORK2_DIRA_MULTITILE_SURVEY_20260423.md`
- `WORK2_DIRB_CONTINUAL_LEARNING_SURVEY_20260423.md`
- `WORK2_DIRC_KVCACHE_SURVEY_20260423.md`
- `WORK2_DIRD_OPTOELECTRONIC_SURVEY_20260423.md`
**Scope:** Select the single big direction for Work 2 (thesis 第二工作 + paper-2).
**Decision authority:** Architect, pending user veto.

---

## 1. Evaluation matrix

| Criterion (weight) | A Multi-Tile | B Continual Learning | **C KV-Cache** | D Opto-Electronic |
|:--|:-:|:-:|:-:|:-:|
| Scientific novelty (0.25) | ★★ | ★★★★ | **★★★★★** | ★★★★ |
| Topical relevance 2026 (0.20) | ★★★ | ★★★ | **★★★★★** | ★★★ |
| Distinct from Work 1 (0.15) | ★★ | ★★★★ | **★★★★★** | ★★★ |
| Organic-specific moat (0.15) | ★ | ★★★ | **★★★★★** (retention match) | ★★★★★ |
| Work 1 infra reuse (0.10) | ★★★★★ | ★★★ | **★★★★** | ★★★★ |
| Master's-scope feasibility (0.10) | ★★★★ | ★★★ | **★★★★** | ★★★★ |
| Defense-committee sellability (0.05) | ★★ | ★★★ | **★★★★★** | ★★★ |
| **Weighted total** | 2.7 | 3.4 | **4.5** | 3.7 |

**Pick: Direction C — LLM KV-Cache Mapping to Organic Optoelectronic CIM.**

## 2. Why C wins (in one argument)

Work 1 told a story about **where organic CIM fails**: attention + severe NL + inference = structural ceiling. Work 2 must tell a complementary story about **where organic CIM uniquely wins**. KV-cache is the only one of the four candidates where organic optoelectronic CIM has a *physics-level* advantage that oxide-RRAM/PCM/FeFET cannot copy:

- **Retention match**: organic OEC-RAM ~10³ s retention aligns naturally with KV-cache residence time (seconds-to-minutes per session). Oxide RRAM is over-specced (years) and over-priced in endurance; SRAM under-specced (ms-scale standby). Organic lands in the Goldilocks zone.
- **Optical refresh**: the photon-modulated conductance that hurt us in Work 1 (Chen 2023) becomes a **feature** here — write refreshes via light rather than voltage, dodging endurance cost.
- **Write-once-per-prefill pattern**: KV entries are appended, read often, rarely re-written. This fits organic's *bad* write endurance (10³-10⁴ cycles) without penalty, which kills Direction B.
- **2026 topicality**: LLM inference memory is the most-funded system problem. Any viable organic-CIM story for KV-cache publishes well and sells hard on defense / grant / industry calls.

The other three directions lose on at least one axis:
- **A (Multi-Tile)** is an engineering contribution, not a scientific one. Hemlet / CLSA-CIM / LionHeart already occupied the framework slot. A student retracing this on organic tiles is a systems paper, not a thesis punchline.
- **B (Continual Learning)** has the right novelty but the wrong device. 10³-10⁴ cycle endurance is a soft ceiling that kills a convincing long-task-sequence demo. Salvageable as a side-memo, not a thesis anchor.
- **D (Opto-Electronic Co-Design)** has the strongest organic-optical moat, but the contribution ("jointly train photodiode + CIM weights") is a local engineering win, not a structural result. Retained as **Work 2 secondary axis** — co-design ideas fold into §3 methodology of Work 2.

## 3. Work 2 one-paragraph pitch (paper-2 abstract seed)

> Large language model inference is bottlenecked by the KV-cache, not model weights. We propose mapping the KV-cache onto organic optoelectronic analog CIM arrays and computing attention scores in-place. Unlike oxide-RRAM (over-endured, over-retained, under-dense) and SRAM (volatile, area-hungry), organic OEC-RAM sits at the retention-endurance working point natively demanded by generative LLM decoding: ~10³ s residence, low per-cell write frequency, and optical refresh that sidesteps the cycling budget. Using the behavioural simulator from [Work 1 ref], we characterize attention degradation under organic device noise, retention drift, and quantization, derive the minimum analog-state count for lossless perplexity on a 1-3B edge LLM, and propose an organic-CIM KV-cache architecture with hybrid digital fallback. The contribution is the first physics-grounded argument for which LLM sub-problem organic CIM actually solves — and the first benchmark suite that measures it.

## 4. Scope commitment (what we will and will NOT do)

### We will
- Target 1-3B edge LLM (TinyLlama-1.1B primary; LLaMA-2-7B GQA secondary).
- Context 4k-8k tokens (covers single-turn + short multi-turn).
- Simulation-only thesis acceptable for Master's; one small-array experimental validation is a stretch goal.
- Metrics: perplexity (WikiText-103), downstream task (LongBench subset, GSM8K), energy per token, area.
- Benchmarks against: FP16 baseline, KIVI 2-bit baseline, SRAM-CIM baseline.

### We will NOT
- Chase > 7B models (infeasible on organic density 2026).
- Chase 128k context (Qwen2.5-7B scale — needs 3D stacking, not organic).
- Attempt organic on-device *training* for KV cache (that's Direction B's problem).
- Claim production deployment — simulation results support a prototype claim only.

## 5. Where this leaves Work 1

Unchanged. Round Q GPU queue (CX-K1-K5 + J-series) continues to close the structural-limit / bimodal-basin question. Work 1 = paper-1 (NC submission under Rule B discipline). Work 2 = paper-2 + thesis second contribution. They are decoupled experimentally; they share only the simulator.

**Narrative arc for thesis defense:**
1. Chapter 3-5 (Work 1): Organic CIM inference of ViTs under severe NL — falsification, structural limit, mitigations tested and rejected.
2. Chapter 6-7 (Work 2): Organic CIM storage of KV-cache for LLM inference — structural fit, retention match, simulation demonstration, architecture proposal.
3. Chapter 8 (Outlook): joint opto-electronic co-design frontend (Direction D as future work), CL on rewritable organic arrays (Direction B as future work).

This arc is defensible, cohesive, and non-redundant with the paper-1 scope.

## 6. Immediate next-step tasks (folded into Round Q §11)

Issued as extensions to the current Round Q broadcast. No new round.

### Kimi (K-Z31-Z35, Phase α addition)
- **K-Z31** `KIMI_WORK2_SCOPE_LOCK_20260423.md` — turn §3 pitch into a 2-page scope document with exact benchmark list, target models, metrics, baselines. Chinese 对应: `paper/thesis_cn/chapter_6_work2_scope.tex` stub.
- **K-Z32** `KIMI_WORK2_EXPERIMENT_PLAN_20260423.md` — experiment plan adapted from Direction C §5 with exact model / dataset / config choices. Drop Experiments to ≤ 4; prioritize Exp 1 (noise-robustness) + Exp 4 (architecture exploration).
- **K-Z33** `paper/paper2/skeleton_v1/SKELETON.md` — REWRITE from the falsification-study skeleton to the KV-cache skeleton. Number-agnostic placeholders still apply.
- **K-Z34** `paper/paper2/skeleton_v1/00_abstract.md` — abstract based on §3 pitch, `[TBD]` for all numbers.
- **K-Z35** `KIMI_WORK2_CITATION_CONSOLIDATION_20260423.md` — merge citation lists from DIRC (33 refs) + DIRD retained refs (for co-design §3.x subsection).

### Gemini (G-HH21-HH25)
- **G-HH21** `GEMINI_WORK2_RETENTION_THEORY_20260423.md` — formal statement: relate organic OEC-RAM retention distribution to KV-cache session-length distribution; derive break-even retention spec.
- **G-HH22** `GEMINI_WORK2_QUANTIZATION_FLOOR_20260423.md` — theoretical floor on analog-state count N such that attention softmax preserves top-k ranking under device noise σ. Number-agnostic until CX-L1 lands.
- **G-HH23** `GEMINI_WORK2_BASELINE_COMPARISON_20260423.md` — matrix of baselines (FP16, KIVI, SRAM-CIM, oxide-RRAM-CIM) with fair-comparison criteria and pitfalls.
- **G-HH24** `GEMINI_WORK2_HOSTILE_REVIEW_20260423.md` — 10 hostile reviewer angles against the KV-cache pitch + response paths.
- **G-HH25** `GEMINI_WORK2_CONFERENCE_FIT_20260423.md` — where Work 2 publishes best (MICRO / ASPLOS / DATE / HPCA / NC follow-up).

### Codex (CX-L series, new sub-queue, non-blocking to CX-K)
Run **only after** CX-K2 closes (no GPU contention). Each experiment is ≤ 15 GPU-h.
- **CX-L1** — LLM infrastructure bring-up: HuggingFace TinyLlama-1.1B local inference; instrument KV cache with quantization + noise hooks; validate WikiText-103 perplexity baseline.
- **CX-L2** — KV-cache noise sweep: inject Gaussian conductance noise (σ = 0.01 → 0.10 of LSB) on K and V tensors independently; measure perplexity degradation. This is Experiment 1 from Direction C §5.
- **CX-L3** — analog-state sweep: quantize KV to N ∈ {2, 3, 4, 5, 6} levels with uniform and non-uniform (learned) codebook; measure perplexity + LongBench subset.
- **CX-L4** — retention drift sweep: simulate exponential conductance decay with τ ∈ {1 s, 10 s, 100 s, 1000 s} across 32-token decode; measure attention-score rank-preservation.
- **CX-L5** — combined-effect ablation: noise + quantization + retention in one run, identify Pareto front.

### Claude (CLAUDE-EG)
- **CLAUDE-EG** (Day 4, 2026-04-26) — audit K-Z31-Z35 + G-HH21-HH25 + CX-L1 landing; ratify Work 2 experimental design v1. If any of K-Z32 experiment plan contradicts G-HH23 baseline matrix, arbitrate.

## 7. Decision rules agents may apply without Claude

- If CX-L1 cannot reach baseline WikiText-103 perplexity within 2 GPU-h → Codex falls back to GPT-2-medium (smaller, known-good). Alert Claude.
- If CX-L2 shows perplexity catastrophically breaks at any σ > 0.01 → Gemini writes an addendum memo explaining; Kimi does NOT scrap the direction — this is a scientific finding, not a project killer.
- If Gemini theory (G-HH22) predicts N ≥ 6 analog states required but experimentally we can only get 4-5 → accept and report; Work 2 pitch becomes "organic CIM is feasible for 4-bit-equivalent KV with graceful degradation" rather than lossless.
- If any agent claims infeasibility: write `WORK2_BLOCKER_<topic>.md` with reproduction steps. Do not silently abandon.

## 8. User-visible one-paragraph summary

Work 2 locks to **LLM KV-cache on organic optoelectronic CIM**. Rationale: it is the only one of the four candidates where organic retention / endurance / optical properties *match* the problem intrinsically, rather than being worked around. Kimi rewrites paper-2 skeleton to the KV-cache pitch; Gemini writes retention-vs-session theory + quantization floor + hostile-review memo; Codex brings up TinyLlama-1.1B baseline and runs noise / quantization / retention sweeps (CX-L1 → L5, ≤ 60 GPU-h total, queued after CX-K2). Directions A and B are shelved to thesis Chapter 8 outlook; Direction D (opto-electronic co-design) folds into Work 2 §3 as the frontend subsection. Work 1 (paper-1, NC) continues untouched under Rule B.

---

## 9. Supersede notice

- `THESIS_WORK2_RESEARCH_PLAN_20260423.md` — superseded; kept as history.
- All four WORK2_DIR* surveys — kept as reference material; DIRC becomes primary citation source, DIRD subset folds in as §3 subsection support, DIRA/DIRB become Chapter 8 outlook references.
- Any agent asked to "pick between A/B/C/D" defaults to **C**. Other directions appear only as comparison rows in tables or as future-work paragraphs.
