# DISPATCH CODEX R10 — Substantive Experiments (4 sub-tracks)
**Date:** 2026-04-25 23:00 CST
**Issued by:** Claude
**Assignee:** Codex
**Authority:** CLAUDE_ROUND10_SUBSTANTIVE_COMPLETION_PLAN_20260425
**Priority:** HIGHEST (closes reviewer-attack vectors before submission)
**Time budget:** ~5-7 days, ~40 GPU-h local
**Constraint:** Priority order — R10A > R10D > R10B > R10E > R9B TikZ > R8 W2 Phase 2

---

## 0. Mission

Run four substantive experiments on local GPU that close the most damaging reviewer concerns:
- R10A: 3-seed canonical Ensemble HAT (replaces single-seed 86.37% headline)
- R10B: Standard HAT 10% mechanism (class-distribution analysis)
- R10D: Intermediate NL sweep (closes 5pp severe-NL gap with evidence)
- R10E: AIHWKit head-to-head baseline (first comparison vs established analog HAT lib)

---

## 1. R10A — Multi-seed canonical Ensemble HAT (HIGHEST priority)

### Why
Current headline: `_ensemble/V4_hybrid_standard_noise_hat_best.pt` is **one seed**. The 86.37±1.54% std is across 10 fresh instances, NOT across training seeds. **Reviewer first attack vector.**

### Spec
- Train 2 additional seeds of canonical Ensemble HAT (existing seed 123 + new 456 + 789)
- Config: same as existing canonical (NL=1.0, σ_D2D=10%, σ_C2C=5%, 4-bit hybrid, batch=64, AdamW lr=5e-4, cosine, warmup=5, epochs=100, AMP on)
- Source: same training script `train_tinyvit_ensemble.py`
- Output: `checkpoints/_ensemble/V4_hybrid_seed{456,789}/best.pt`
- Then fresh-eval each new checkpoint: 10 fresh instances × 5 MC, eval_fresh_instances.py
- Final: aggregate 3-seed mean ± std across-seed; cross-instance ±std stays separate metric

### Time
- 3 seed × 100 epochs × ~3-4h/epoch on RTX 5070 Ti = ~10-12 GPU-h training
- Wait — actually 1 seed = ~10-12h, so 2 NEW seeds = ~20-25h. Use AMP + parallelism if VRAM allows.
- + 3 fresh-evals = ~3h
- Total: ~25-28 GPU-h, 2-3 days wall-clock if run sequentially

### Acceptance criteria
- 3 seeds trained, each best_acc within ±2% of original 91.13% (sanity)
- Fresh-eval per seed: 10 instances × 5 MC each
- Aggregate: 3-seed mean ± std
- Expected: 84-88% range across seeds. If outside: ESCALATE.

### Deliverable
- `checkpoints/_ensemble/V4_hybrid_seed456/best.pt` + `seed789/best.pt`
- `report_md/_gpt/json_gpt/r10a_seed{123,456,789}_fresh_eval.json`
- `CODEX_R10A_MULTI_SEED_REPORT_20260425.md`:
  - Provenance (commit hash, env, GPU)
  - Per-seed train_best + fresh mean ± std
  - Aggregate 3-seed mean ± std
  - Comparison to original single-seed 86.37±1.54
  - Paper-safe statement for Kimi to drop into §5.6: "Ensemble HAT canonical achieves [X.XX ± Y.YY%] across 3 training seeds (each evaluated on 10 fresh hardware instances), demonstrating training-seed robustness in addition to fresh-instance robustness."

### Constraints
- **Match existing protocol exactly** — no new hyperparameters, no new noise mode
- Same code commit (`33bed9c` post-fix); document in JSON provenance
- AMP enabled (matches existing); record exp_cfg
- No interactive monitoring — let it run, check next morning

---

## 2. R10B — Standard HAT 10% mechanism analysis (4 hours, no GPU training)

### Why
Standard HAT collapses to **exactly 10.00% on CIFAR-10** (10 classes). Reviewer immediate suspicion: single-class predictor, not "overfitting." We owe explicit mechanism evidence.

### Spec
Use existing Standard HAT canonical checkpoint (`V3_hybrid_standard_noise_standard_train_best.pt`):

1. **Load checkpoint, set eval mode**
2. **Sample fresh D2D instance** (one realization, σ=10%)
3. **Run inference on full CIFAR-10 test set** (10000 images)
4. **Per-class prediction frequency**: count predicted class for each test image
5. **Plot histogram**: predicted class (0-9) on x-axis, frequency on y-axis
6. **Statistics**: 
   - Argmax class concentration: what fraction of predictions are most-frequent class?
   - Entropy of prediction distribution: H = -Σ p_i log p_i (max for uniform = log(10) = 2.3)
   - Per-class accuracy on test images
7. **Repeat across 5 fresh D2D instances** to confirm pattern is consistent

### Expected finding
Standard HAT predicts ONE class (or 1-2 classes) for all test images → entropy ~0, single-class concentration ~100%. This confirms "single-class predictor" mechanism, not gradual degradation.

### Compare to Ensemble HAT
Run same analysis on canonical Ensemble HAT checkpoint at fresh D2D instance. Expected: prediction distribution close to uniform (or class-balanced), high entropy.

### Deliverable
- `report_md/_gpt/json_gpt/r10b_standard_hat_class_distribution.json`
- `paper/figures/figS_standard_hat_collapse_mechanism.{png,pdf}` — 3-panel:
  - (a) Standard HAT prediction histogram across 5 fresh instances (overlay)
  - (b) Ensemble HAT prediction histogram (control)
  - (c) Per-instance entropy bar chart
- `CODEX_R10B_MECHANISM_REPORT_20260425.md`:
  - Numerical findings + mechanism explanation
  - Paper-safe paragraph for §5.5 (after no-AMP confirmation): "Per-instance class-distribution analysis (Fig.~\ref{figS_standard_hat_collapse_mechanism}) reveals that Standard HAT under fresh hardware instances reduces to single-class prediction (mean entropy <0.1, vs Ensemble HAT entropy 2.3 ≈ uniform), confirming the 10.00% accuracy is mode-collapse to chance-level rather than gradual feature degradation."

### Time: 4 hours, NO new training, ~30 min GPU eval

---

## 3. R10D — Intermediate NL sweep (closes 5pp gap evidence)

### Why
Current paper says "5pp severe-NL gap reflects training-recipe constraints, not physical floor." NO EVIDENCE provided. Reviewer: handwaving.

### Spec
Train Ensemble HAT at 3 intermediate NL values to show monotonic gap closure as NL → 1:

| NL_LTP | NL_LTD | Status | Expected fresh |
|:--|:--|:--|:--|
| 1.0 | -1.0 | Already done (R10A canonical) | ~86% |
| 1.2 | -1.2 | NEW | ~85% |
| 1.5 | -1.5 | NEW | ~83% |
| 1.8 | -1.8 | NEW | ~82% |
| 2.0 | -2.0 | Already done (M-series) | ~80-82% |

Train Ensemble HAT at NL = 1.2, 1.5, 1.8 (3 new training runs, 1 seed each).
- Same recipe as R10A but with the NL flags overridden
- Each: ~10-12h training
- Fresh-eval each: 10 instances × 5 MC
- Plot: NL on x-axis, fresh-instance accuracy on y-axis

### Expected finding
Monotonic decrease in fresh-instance accuracy from NL=1.0 to 2.0. **This evidence supports D2 defense paragraph (5pp residual gap is monotonic with write nonlinearity, not a step at NL=2.0).**

### Time
3 training runs × ~10h = ~30 GPU-h. **Use overnight + parallel scheduling.**

### Deliverable
- 3 checkpoints + 3 fresh-eval JSONs
- `paper/figures/figS_nl_sweep_ensemble.{png,pdf}` — line plot: NL vs fresh-instance accuracy mean ± std
- `CODEX_R10D_NL_SWEEP_REPORT_20260425.md`:
  - Per-NL training + fresh-eval table
  - Monotonicity confirmation
  - Paper-safe paragraph for §5.7 / Discussion D2 defense:
    > "Ensemble HAT recovery degrades monotonically with write nonlinearity: from 86.37±1.54% at NL=1.0 to [X.XX±Y.YY%] at NL=1.5 to ~80-82% at NL=2.0 (Fig.~\ref{figS_nl_sweep_ensemble}). The 5-pp residual gap at NL=2.0 reflects continuous degradation of the gradient-scaling surrogate as nonlinearity increases, consistent with training-recipe constraints rather than a physical floor."

---

## 4. R10E — AIHWKit head-to-head baseline (~2-3 days, ~10 GPU-h)

### Why
**No head-to-head comparison vs established analog HAT library.** Reviewer at Nat Electronics: "How does your Ensemble HAT compare to AIHWKit's analog noise injection?"

### Spec

#### 4.1 Install AIHWKit
- `pip install aihwkit` in a separate conda env (avoid contaminating main env)
- Document version installed (Rasch et al. 2023 reference; latest is ~0.9)

#### 4.2 Build matching baseline
Replicate Tiny-ViT canonical eval setup using AIHWKit primitives:
- Same Tiny-ViT-5M architecture
- Same CIFAR-10 dataset
- AIHWKit's `InferenceRPU` config with parameters matching our literature priors:
  - σ_w_drift, σ_read_noise → match our σ_D2D/σ_C2C
  - inference_repeat = 10 (matches our 10 fresh instances)
  - 4-bit weight quantization
- Train AIHWKit's standard "noisy training" (analogous to Standard HAT)
- Optionally: AIHWKit's "robust training" if it has multi-mask resampling

#### 4.3 Comparison metrics
- Train AIHWKit baseline: report training best + fresh-instance equivalent metric
- Compare to:
  - Our Standard HAT: 10.00%
  - Our Ensemble HAT: 86.37±1.54% (or R10A new headline)

#### 4.4 Honest framing
Two outcomes:
- AIHWKit fresh ≈ our Ensemble HAT → minor improvement; reframe as "Ensemble HAT matches established analog HAT under our setting; differs in per-epoch resampling discipline"
- AIHWKit fresh ≈ our Standard HAT (i.e., collapses) → strong claim "Ensemble HAT is the first analog HAT to demonstrate cross-instance generalization"
- Either outcome: real evidence > speculation.

### Time
- AIHWKit setup + config: 1 day
- Training: ~1 day (~10 GPU-h depending on AIHWKit speed)
- Eval + analysis: 1 day

### Deliverable
- AIHWKit env + config in `paper2_aihwkit_baseline/` (separate dir)
- Comparison checkpoint + fresh-eval JSON
- `CODEX_R10E_AIHWKIT_BASELINE_REPORT_20260425.md`:
  - AIHWKit version + config details
  - Comparison table: Standard HAT (ours) / Ensemble HAT (ours) / AIHWKit baseline
  - Paper-safe paragraph for §5 or Discussion: "Direct comparison to AIHWKit \citep{rasch2021aihwkit} under matched canonical settings yields fresh-instance accuracy of [X.XX%], compared to [Y.YY%] for our Ensemble HAT. The gap reflects [interpretation depending on outcome]."

### Constraints
- Use SEPARATE python env (don't pollute main)
- Document AIHWKit version explicitly
- If AIHWKit baseline is impossible to install/run for technical reasons (CUDA mismatch etc.): ESCALATE; fallback is text-only comparison citing AIHWKit's published numbers

---

## 5. Sequencing within Codex

### Day 1 morning
- Kick off R10A multi-seed (parallel: seed 456 + seed 789, GPU may handle 2 simultaneously if VRAM allows)
- Codex starts R10B class-distribution analysis (CPU + brief GPU eval)

### Day 1 afternoon
- R10B finished (1-2h analysis)
- Document R10A progress in AGENT_SYNC

### Day 2
- R10A monitoring (training continuing)
- Codex starts R10D NL=1.2 training (if R10A finished or VRAM permits parallel)
- Codex starts AIHWKit env setup (R10E preparation, no GPU)

### Day 3
- R10A complete; fresh-eval 3 seeds
- R10D NL=1.2 done, start NL=1.5 + NL=1.8 in series
- AIHWKit baseline training starts

### Day 4
- All R10A/B/D landings reported
- AIHWKit baseline completes
- Final reports written

### Day 5 buffer
- Any reruns, debug, or final cleanup

---

## 6. Coordination with R8 W2 + R9 + 8×40GB

### R8 Work 2 Phase 2 (Pythia 410M training)
- W2 Phase 2 GPU work paused or reduced to 30% during R10 days 1-3
- W2 priority lower than paper-1 R10 (W2 has months of buffer; paper-1 doesn't)
- After R10 closes: full W2 GPU bandwidth resumes

### R9 Track B (TikZ rebuild)
- TikZ work is CPU-only — no conflict
- Codex can run R9B in parallel with R10 GPU jobs
- R9B target: 3 figures over 5-7 days. R10 takes priority for compute-attention.

### 8×40GB cross-arch
- Independent. No interaction.

---

## 7. Acceptance criteria

- All 4 sub-tracks complete with deliverables
- All experiments document provenance (commit hash, code sha256, GPU device, Python+pytorch version, git_worktree_dirty flag)
- Three new figures produced: figS_nl_sweep_ensemble, figS_standard_hat_collapse_mechanism, [optional figS_aihwkit_comparison if pretty]
- Paper-safe statements written for Kimi integration
- Manuscript wordcount budget preserves: + ~400-500 words across §5 R10A reframing + §5.5 mechanism para + §5.7 NL sweep para + Discussion AIHWKit paragraph

---

## 8. Escalation triggers

- R10A 3-seed mean diverges > 3pp from 86.37 → ESCALATE
- R10A 3-seed std > 3pp → ESCALATE (methodology check)
- R10A any seed mean < 80% → MAJOR ESCALATION (reopen NARRATIVE_PIVOT)
- R10D non-monotonic with NL → ESCALATE (recipe sensitivity question)
- R10E AIHWKit beats our Ensemble HAT → REASSESS novelty claim; honest reframe
- R10B Standard HAT NOT single-class collapse → revise mechanism story; new finding

---

## 9. What you do NOT do

- No new architectures
- No ImageNet
- No retraining paper-1 baseline canonical Ensemble HAT (use existing)
- No paper text edits (Kimi handles integration)
- No commits to canonical .tex (Kimi)
- No experiment beyond the 4 sub-tracks listed

---

## 10. Cold-start refs

- `CLAUDE_ROUND10_SUBSTANTIVE_COMPLETION_PLAN_20260425.md` — master plan
- `train_tinyvit_ensemble.py` — canonical training entry
- `eval_fresh_instances.py` / `eval_fresh_instances_postfix.py` — fresh eval
- `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt` — current canonical (DO NOT MODIFY)
- `checkpoints/_gpt/postfix_m_series/cx_m{1..6}/` — severe-NL M-series (use protocol as reference)
- `analog_layers.py` — at commit `33bed9c` (post-fix; NL guard active for `1<NL<2`)

**No deadline, but priority order is enforced: R10A first.**
