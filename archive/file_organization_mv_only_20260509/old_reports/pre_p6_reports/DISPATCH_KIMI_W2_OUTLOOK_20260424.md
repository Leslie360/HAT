# DISPATCH KIMI-W2-OUTLOOK — Work 2 (KV-cache) Preview Section
**Date:** 2026-04-24
**Issued by:** Claude
**Assignee:** Kimi
**Priority:** MEDIUM (after KIMI-THEORY-1)
**Depends on:** NARRATIVE_PIVOT_20260424.md §8 (scope decision: medium as default)
**Time budget:** unconstrained

---

## 1. Objective

Write a 2-3 page preview section / subsection for paper-1 demonstrating that the framework extends from **inference-path (MLP)** to **attention-path (KV-cache) analog CIM**. Scope is "medium" per NARRATIVE_PIVOT §8: architecture diagram + energy estimate + one preliminary mapping experiment concept, not a full benchmark.

Purpose: give reviewers visible evidence that the paper-1 framework is a **platform**, not a one-off. This elevates the paper's contribution claim without requiring Work 2's full experimental program.

---

## 2. Content structure (2-3 pages, 2 figures, 1 table)

### 2.1 Opening framing (~0.5 page)

Motivation sentences:
- Inference-path (MLP projections) is what paper-1 measured. But attention itself — QKV projections and output projection — is also a matrix multiplication amenable to analog CIM.
- KV-cache during decode phase is particularly wasteful on digital hardware: quadratic memory access, low arithmetic intensity.
- Organic optoelectronic arrays are uniquely suited to KV-cache storage + read because of their non-volatile conductance, low read energy, and high integration density.

**Framing sentence**: "We preview an extension of the present framework to the attention pathway, showing that the hardware-instance overfitting diagnostic and Ensemble HAT treatment generalize mechanistically to this regime."

### 2.2 Architecture mapping (Figure 1 for this section)

One diagram showing:
- Transformer decoder block with Q, K, V projections
- KV-cache bank per layer
- Mapping: K and V matrices → separate analog CIM crossbars per layer, read-addressed by position index during attention
- Q projection → analog CIM (same as MLP path in paper-1)
- Attention softmax → kept digital (consistent with paper-1's hybrid stack)
- Output projection → analog

Label each subsystem with expected size (device count), read frequency (per-token vs per-sequence), and precision requirement (4-bit like paper-1, or higher for K cache).

### 2.3 Energy estimate table (~0.5 page)

Back-of-envelope order-of-magnitude table extending paper-1's energy section.

Columns:
- Component (Q-proj / K-proj / V-proj / KV-cache-read / Softmax / O-proj / LayerNorm)
- FP32 digital energy/token (J)
- Analog CIM energy/token (J, using paper-1's per-MAC energy constant ε_MAC)
- Speedup ratio

Rows for 1 decoder layer, context length 1024, hidden dim 512 (Tiny-ViT-sized example).

State clearly: "These are placeholder constants extrapolated from paper-1's energy model; not chip-predictive." Same discipline as paper-1 limitations.

Expected story: KV-cache-read becomes the dominant energy term in digital (fetching 1024 × d_model bytes from DRAM), analog replaces it with in-memory compute, massive reduction. Attention softmax remains in digital (small fraction).

### 2.4 Hardware-instance overfitting in attention path (~0.5 page)

Argue that the diagnostic extends. Key claim: attention is MORE sensitive to mismatch than MLP because:
- Softmax is nonlinear and exponentiates small perturbations in logits → small D2D errors get amplified to large attention-weight reallocations.
- KV-cache is used repeatedly across many decode steps → a single mismatch error compounds across tokens, unlike a single MLP forward pass.
- This motivates that Ensemble HAT is **more important**, not less, in the attention path.

Explicitly call out: "Standard HAT trained on a single K-matrix realization will overfit to that instance's mismatch profile. Fresh deployment on a fabricated KV-cache would collapse, as it did for Tiny-ViT MLP (paper-1 §5.5)."

### 2.5 Preliminary experiment sketch (~0.5 page)

One preliminary mapping experiment **concept**, not results. State what we will (or did, if Codex bandwidth allows) do:
- Take paper-1's Tiny-ViT, swap in analog CIM backing for attention Q, K, V projections only (keep softmax digital, keep MLP analog as in paper-1).
- Measure fresh-instance accuracy vs Standard HAT vs Ensemble HAT.
- Expected: same 10% vs ~80% pattern.

If Codex has run this by paper submission: cite the numbers. If not: cite as "Work-in-progress, full benchmark in companion paper."

**Design note**: leave placeholder `[PRELIMINARY_KV_ACCURACY]` + `[PRELIMINARY_KV_FRESH_STD]` for mechanical fill-in later.

### 2.6 Scope boundary

Close the section with explicit scope:
- "This preview establishes that the diagnostic and treatment generalize architecturally; full benchmarking of long-context decoding with multi-layer KV-cache analog mapping (including head-level, multi-query, and sparse attention variants) is the subject of a companion paper."
- State that paper-2 will use same framework, same audit infrastructure, same Ensemble HAT methodology.

---

## 3. Where in paper-1 this section lives

Two placement options; you choose:

**Option A**: Full subsection under Results (§5.9 "Extension to attention-path KV-cache"). Pros: visible to reviewers who skim. Cons: uses Results real estate for preliminary content.

**Option B**: Expanded Outlook in Discussion (§6.5 or §6.6). Pros: honest about scope (outlook ≠ result). Cons: less prominent.

**My recommendation**: Option B. Honesty about scope is a virtue, and the reviewer read time weighted toward Discussion conclusions means the reviewer still sees it.

Draft under Option B first. If Codex lands a real preliminary number, we can bump to Option A at integration time.

---

## 4. Deliverables

| File | Content |
|:--|:--|
| `paper/latex_gpt/sections/06_discussion_kv_outlook.tex.kimi_draft` | The 2-3 page subsection |
| `paper/figures/fig_kv_architecture.pdf` + `.png` | Architecture diagram (Kimi draws in tikz or delegates to Codex matplotlib) |
| `paper/figures/tab_kv_energy_estimate.tex` | The energy-estimate table as LaTeX |

---

## 5. Constraints

- **No claims beyond evidence**. Everything declared "preliminary" or "outlook" unless Codex delivers real number.
- **No overlap with paper-2 scope**. Do not preview paper-2's experimental matrix. Only architectural+mechanistic claims.
- **Cite Paper-1 Ensemble HAT theory (KIMI-THEORY-1 output)** as the method this section inherits.
- **Length firm at 2-3 pages**. Over = bad.

---

## 6. Interaction with NARRATIVE_PIVOT

Per §8 of NARRATIVE_PIVOT: this is the "medium scope" default. If months 2-4 allow upgrading to "maximum scope" (Codex runs a real LLaMA-variant decode benchmark), we escalate. Otherwise the medium draft is the submission version.

No time budget. Do it well.
