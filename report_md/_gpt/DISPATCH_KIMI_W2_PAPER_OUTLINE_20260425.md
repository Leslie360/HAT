# DISPATCH KIMI W2 — Paper-2 Outline + Theory Adaptation
**Date:** 2026-04-25 22:55 CST
**Issued by:** Claude
**Assignee:** Kimi
**Authority:** CLAUDE_ROUND8_WORK2_LAUNCH_PLAN_20260425 §5.2
**Priority:** MEDIUM (parallel to Codex W0/W1 infrastructure)
**Time budget:** ~2 weeks

---

## 0. Mission

Lay the textual foundation of Work 2 paper while Codex builds infrastructure. Two streams: (1) adapt paper-1's Ensemble HAT theory to attention path; (2) draft paper-2 abstract + outline + section skeletons.

---

## 1. Stream A — Theory adaptation (Days 1-7)

Paper-1's KIMI-THEORY-1/2 derives Ensemble HAT for MLP-path analog under uniform additive noise. Work 2 needs to extend or adapt for:
- Attention path (QKV projections + KV-cache reads)
- Softmax nonlinearity in attention
- Sequential reads from analog KV-cache (noise accumulates across decode tokens)

### 1.1 Question 1: Does the implicit gradient-L2 regularizer change for QKV?

QKV projections are mathematically identical to MLP projections (linear maps). At first order, the same Ensemble HAT analysis applies:
$$\mathcal{L}_{\text{Ens}}^{\text{QKV}} \approx \mathcal{L}_0 + \frac{\sigma_{\text{D2D}}^2}{2}\sum_i W_i^2 \mathbb{E}[(\partial \ell / \partial W_i)^2]$$

Subtle difference: $\partial \ell / \partial W_i$ for Q, K, V flows back through softmax. The Hessian-vector product structure changes. Sketch: softmax is contractive on logits, so the gradient norm is bounded by entropy/sharpness of attention. Implication: high-entropy attention (broad attention, uncertain) → larger implicit regularization weight on Q/K than low-entropy (sharp attention).

**Deliverable**: §S.attention-theory in paper-2 supplementary draft. ~1 page. Cite paper-1 §S.7-S.10 for the base derivation.

### 1.2 Question 2: How does Ensemble HAT interact with softmax?

Softmax exponentiates logits. Small noise in logits → potentially large changes in attention weights (nonlinear amplification). But softmax also contracts (output sums to 1, bounded). Trade-off:
- For peaked attention (one logit dominates): noise has small effect (output is mostly determined)
- For broad attention (logits similar): noise has large effect on attention weights, but small effect on average

Theory sketch needed: bound the attention-output noise as a function of input logit noise. Use fact that Jacobian of softmax has spectrum bounded by entropy of the output. Cite Vaswani et al. 2017 attention paper, plus any softmax sensitivity literature.

**Deliverable**: paragraph in §S.attention-theory.

### 1.3 Question 3: Sequential decode noise accumulation

Analog KV-cache: token $t$'s K is stored at decode step $t$; read at decode steps $t+1, t+2, \ldots$. Each read adds fresh C2C noise. After $T$ reads, the effective K seen by attention is:
$$\tilde{K}_t = K_t (1 + M_{D2D,t}) + \frac{1}{T}\sum_{r=1}^{T} \xi_{C2C,t,r}$$

C2C noise averages out over reads (good!). D2D mismatch is persistent (no averaging across reads, only across instances).

Implication: long-context decode is **less sensitive to C2C** than short context (averaging effect), but **equally sensitive to D2D**. This is a Work-2-specific finding that doesn't appear in paper-1.

**Deliverable**: this is the key Work 2 theoretical contribution. Write as §S.kv-cache-noise-analysis in paper-2 supplementary. ~1.5 pages with derivation.

### 1.4 Stream A acceptance

`paper2/supplementary/S_attention_theory.tex.kimi_draft` (Kimi writes; Claude integrates later)
- §S.attention-theory.1 QKV regularizer adaptation
- §S.attention-theory.2 Softmax interaction
- §S.attention-theory.3 KV-cache decode noise accumulation
- ~3-4 pages

---

## 2. Stream B — Paper-2 outline (Days 1-14)

Draft `paper2/` directory with paper-2 structure mirroring paper-1.

### 2.1 Files to create

`paper2/sections/` skeleton:
- `00_abstract.tex.kimi_draft` — Work 2 abstract
- `01_introduction.tex.kimi_draft` — KV-cache problem + paper-1 reference + Work 2 contribution claim
- `02_related_work.tex.kimi_draft` — analog CIM literature + LLM compression literature + KV-cache compression literature
- `03_methodology.tex.kimi_draft` — analog mapping + KV-cache analog wrapper + Ensemble HAT for attention
- `04_experimental_setup.tex.kimi_draft` — TinyLlama testbed + WikiText-103 + benchmarks + sliding-window decode
- `05_results.tex.kimi_draft` — placeholder pending W2 results
- `06_discussion.tex.kimi_draft` — placeholder
- `07_conclusion.tex.kimi_draft` — placeholder

`paper2/supplementary/` skeleton:
- `S_attention_theory.tex.kimi_draft` — Stream A output
- `S_kv_cache_implementation.tex.kimi_draft` — placeholder
- `S_decode_benchmark_protocol.tex.kimi_draft` — placeholder

`paper2/cover_letter.tex.kimi_draft` — Work 2 cover letter (target Nature Communications, given paper-1 takes Nature Electronics)

### 2.2 Abstract draft

~200 words. Hook: KV-cache is the dominant inference-time bottleneck for long-context LLM decoding; analog CIM offers compute-in-memory but has been deployed only for inference-path (paper-1). Work 2 extends the framework to the attention path, including persistent KV-cache stored as analog conductance. Three contributions:
1. Architectural: first analog mapping of LLM KV-cache (signature novelty)
2. Theoretical: extends Ensemble HAT to attention path with sequential-decode noise analysis (Work-2-specific finding)
3. Empirical: [PENDING W2 RESULTS — placeholder for actual numbers]

Use NARRATIVE_PIVOT zone discipline. No `[PENDING_*]` allowed in abstract for placeholder claims; use vague "demonstrates" language until W2 numbers land.

### 2.3 Introduction outline

- Para 1: Motivation — long-context LLM inference is limited by KV-cache memory bandwidth
- Para 2: Related work — paper-1 inference-path analog; gap = attention path + KV-cache
- Para 3: Contribution sketch — analog KV-cache + Ensemble HAT extension + first benchmark
- Para 4: Paper structure
- Cite paper-1 explicitly (and as soon as paper-1 has DOI/arxiv, update)

### 2.4 Related work outline

Three pillars:
- Analog CIM for transformers (paper-1 + Sebastian, Burr, Eleftheriou, Rasch AIHWKit)
- LLM compression (KV-cache quantization papers like KVQuant, FlexGen — survey 2024-2025)
- KV-cache for long-context (StreamingLLM, scissorhands, H2O, etc.)

This is where Work 2 differentiates: most KV-cache work compresses for digital memory; we re-imagine it as analog conductance with mismatch tolerance via Ensemble HAT.

### 2.5 Stream B acceptance

`paper2/sections/*.tex.kimi_draft` skeleton with abstract drafted, intro structured, related work outlined; results/discussion/conclusion placeholders; cover letter draft. ~10 short files.

---

## 3. Hard constraints

### 3.1 Two-track discipline

- Track B (paper-1 standby) takes priority over Stream A/B if 8×40GB returns or PhD data lands
- Work 2 paper-2 work must NOT pull resources from paper-1 §5.9 cross-arch integration when that fires

### 3.2 Numerical/zone discipline (carry over from paper-1)

- All numbers in paper-2 must zone-map: 3A bug-immune, 3B invalidated, 3C post-fix verified, **3W new Work 2 zone for W2 results when they land**
- Same wording bans (no "post-fix", no "deployment-fidelity" without hook qualification, etc.)
- Cite Wager 2013, Foret 2021, paper-1 self-citation when appropriate

### 3.3 Don't do

- Don't write fake/placeholder numbers in any draft
- Don't preview Work 2 results that don't yet exist
- Don't pull paper-1 narrative content into paper-2 (paper-2 inherits framework, not narrative)
- Don't decide Work 2 venue strategy yet — that's a Round-9+ decision

---

## 4. Coordination

- Wait for Codex W0 testbed lock (Day 3) before finalizing Methodology + Experimental Setup
- Wait for Codex W1 baseline FP32 perplexity number before mentioning specific numbers
- Coordinate with Codex on architectural mapping spec (Codex's `WORK2_ARCHITECTURAL_MAPPING_SPEC` is the source of truth for §3 Methodology)

---

## 5. Deliverables summary

| Stream | File | Status |
|:--|:--|:--|
| A | `paper2/supplementary/S_attention_theory.tex.kimi_draft` | NEW (~3-4 pages) |
| B | `paper2/sections/{00..07}*.tex.kimi_draft` | NEW (~10 files; abstract + intro complete, others skeleton) |
| B | `paper2/cover_letter.tex.kimi_draft` | NEW (~1 page draft) |
| Status | `KIMI_W2_PAPER_OUTLINE_REPORT_20260425.md` | Status + change summary |

---

## 6. Success criteria

After 2 weeks:
- Paper-2 has a structured skeleton ready to absorb W2 results
- Theory adaptation (Stream A) is publishable supplementary material
- When Codex W2 results land in 4 weeks, integration is mechanical (no major rewrites needed)
- Paper-1 work is unaffected

---

## 7. Cold-start refs

- `CLAUDE_ROUND8_WORK2_LAUNCH_PLAN_20260425.md` — master plan
- `KIMI_THEORY_1_COMPLETE_20260424.md` + `KIMI_THEORY_2_COMPLETE_20260425.md` — paper-1 theory base
- `paper/latex_gpt/supplementary/S_theory_ensemble_hat.tex` — paper-1 theory canonical
- `DISPATCH_CODEX_W2_PHASE0_INFRASTRUCTURE_20260425.md` — companion Codex dispatch

**Time budget: 2 weeks. No deadline.**
