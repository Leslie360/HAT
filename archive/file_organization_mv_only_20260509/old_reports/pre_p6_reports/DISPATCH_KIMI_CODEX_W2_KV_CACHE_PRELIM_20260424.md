# DISPATCH KIMI+CODEX — Work 2 KV-Cache Preliminary Experiment
**Date:** 2026-04-24 22:30 CST
**Issued by:** Claude
**Assignees:** Kimi (design spec + integration) + Codex (code + run)
**Depends on:** CLAUDE_ROUND2_CLOSURE_RULING §2 R3-6; KIMI-W2-OUTLOOK already sent
**Priority:** MEDIUM
**Time budget:** ~1 week
**GATED ON:** R3-1 thesis chapter 5 (CN) first draft + 8×40GB remote cross-arch returning

---

## 1. Objective

Upgrade the Work 2 Outlook section (per DISPATCH_KIMI_W2_OUTLOOK §2.5) from "Option B: Discussion Outlook" to "Option A: Full Results subsection" by landing ONE real preliminary measurement on KV-cache analog mapping.

Purpose: give reviewers visible experimental evidence that the paper-1 framework extends to attention-path analog CIM, not just mechanistic argument.

---

## 2. Scope (one measurement, not a full benchmark)

Single preliminary config:
- **Model**: Tiny-ViT-5M (paper-1's existing model — no new architecture) OR ViT-Small (if 8×40GB remote delivers it first, use ViT-Small for scale continuity)
- **Task**: CIFAR-10 or TinyImageNet (match whichever has existing checkpoint)
- **Mapping**:
  - **Keep** MLP projections analog (paper-1 hybrid)
  - **Add**: QKV projections analog (new for Work 2 preview)
  - **Keep**: attention softmax + LayerNorm digital
  - **Keep**: output projection analog (per paper-1)
- **Training**: from an existing analog-hybrid checkpoint with Ensemble HAT, add QKV path analog, short finetune (~5-10 epochs)
- **Evaluation**:
  - Standard accuracy (should stay close to baseline if the QKV analog path works)
  - Fresh-instance eval (10 D2D × 5 MC) — the diagnostic question: does Standard HAT → 10% collapse also happen on attention path?
  - Ensemble HAT fresh: does it recover similarly to MLP?

---

## 3. What success looks like

Two outcomes are both paper-grade:

**Outcome A (reinforcing)**: Ensemble HAT recovers attention-path analog deployment to similar accuracy as MLP-only. Shows the diagnostic-treatment framework is architecture-pathway-general.

**Outcome B (scope-limiting)**: Attention path shows different failure pattern (e.g., larger fresh-collapse, lower Ensemble recovery). This is a NEW finding, still Nature-Electronics-worthy — identifies attention path as a harder mitigation target.

Either outcome lands in paper as "§5.9 Preliminary: Extension to attention pathway" (upgrade from Outlook).

---

## 4. Codex side

### 4.1 Code

- Extend `analog_layers.py` hybrid conversion rule to include QKV projection classification
- Check `tinyvit_hybrid_utils.py:classify_tinyvit_layer` — add a `qkv` group if not already present
- Wire into `train_tinyvit.py` or `train_tinyvit_ensemble.py` as a new config flag `--include-qkv-analog`

### 4.2 Training

- Warm-start from `V4_hybrid_ensemble_hat_canonical` checkpoint
- Add QKV analog, short Ensemble HAT finetune (~5-10 epochs, lr=1e-4)
- Save checkpoint as `checkpoints/_gpt/work2_preview/V4_qkv_analog_ensemble_hat.pt`

### 4.3 Eval

- Standard test-set accuracy
- Fresh-instance: 10 D2D × 5 MC with `eval_fresh_instances_postfix.py`
- Also run Standard HAT control (fixed mask) for comparison
- Output: `work2_preview_qkv_fresh_ensemble.json`, `work2_preview_qkv_fresh_standard.json`

### 4.4 Deliverable

`CODEX_W2_KV_PRELIM_REPORT_20260424.md`:
- Training log summary (convergence, test acc)
- Fresh-instance table: Standard HAT vs Ensemble HAT
- Any surprises / failure modes
- JSON paths

### 4.5 Time budget

- Code extension: 1-2 days
- Training: 1-2 GPU-days
- Fresh-eval: few hours
- Total: 3-4 days wall-clock

---

## 5. Kimi side

### 5.1 Wait for Codex report

Do not start §5 writing until Codex delivers §4.4 report.

### 5.2 Write §5.9 draft

Replace current `06_discussion_kv_outlook.tex.kimi_draft` (from DISPATCH_KIMI_W2_OUTLOOK) with a full Results subsection:

`paper/latex_gpt/sections/05_results_kv_preview.tex.kimi_draft_v3`

Structure:
- Opening: "To test whether the hardware-instance overfitting diagnostic and Ensemble HAT treatment generalize to the attention pathway, we conduct a preliminary experiment extending the framework to QKV projections."
- Methodology (brief): warm-start, QKV added to analog, fine-tune protocol
- Results table: Standard HAT vs Ensemble HAT fresh-instance accuracy on attention+MLP configuration
- Discussion: pattern relative to MLP-only paper-1 §5.5-5.6
- Scope: "Full attention-path analog deployment (multi-head, multi-query, KV-cache decoding) remains the subject of a companion paper."

Target length: 2 pages.

### 5.3 Update CN thesis chapter 6 (Work 2 scope)

Fold the preliminary result into `paper/thesis_cn/chapter_6_work2_scope.tex.kimi_draft_v3` as concrete experimental evidence (was preliminary sketch).

### 5.4 Deliverable

- `paper/latex_gpt/sections/05_results_kv_preview.tex.kimi_draft_v3` (new)
- Updated `paper/thesis_cn/chapter_6_work2_scope.tex.kimi_draft_v3`
- `KIMI_W2_PRELIM_INTEGRATION_REPORT_<date>.md`

---

## 6. Gating

**Do NOT start this dispatch until:**
1. Kimi R3-1 thesis chapter 5 (CN failure modes) first draft is complete (keeps Kimi's failure-mode framing current in memory)
2. 8×40GB remote cross-arch returns (to avoid GPU contention with local Codex)

Claude signals "R3-6 GO" via AGENT_SYNC when both conditions met.

---

## 7. Constraints

- **One preliminary config only.** Do not expand to multi-arch / multi-dataset.
- **Warm-start from existing checkpoint** — no full retrain.
- **Stay on local GPU.** Do not dispatch to 8×40GB remote (it has its own task).
- **No paper-1 main narrative changes** — §5.9 is additive.
- **No Work 2 full paper content.** This is a preview; the full Work 2 is a follow-up paper.

---

## 8. Success criteria

Paper-1 §5.9 has a 2-page Results subsection with one concrete attention-path analog experiment, showing either (A) diagnostic-treatment generalizes, or (B) attention path has distinct failure characteristic. Either way, paper-1 claim strengthens from "framework conceptually extends" to "framework extends with preliminary evidence".

---

## 9. Escalation

If preliminary experiment reveals the framework does NOT extend (Standard HAT on QKV doesn't even collapse to 10% — or Ensemble HAT doesn't help): halt integration, flag to Claude. This is scientifically interesting but needs narrative rework.
