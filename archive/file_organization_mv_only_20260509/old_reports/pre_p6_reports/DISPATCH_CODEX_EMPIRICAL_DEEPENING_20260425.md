# DISPATCH CODEX — Empirical Mechanism Analyses (Phase 2)
**Date:** 2026-04-25 01:50 CST
**Issued by:** Claude
**Assignee:** Codex
**Authority:** CLAUDE_PROACTIVE_SPRINT_PLAN_20260425.md Phase 2
**Priority:** HIGH (sprint anchor)
**Time budget:** ~6-8 GPU-h total, 5 jobs, all on existing checkpoints

---

## 0. Mission

Run lightweight analyses on existing checkpoints to expose the **mechanism** behind Ensemble HAT's effectiveness. Each analysis is a standalone job. NO new training. All complete on local GPU within ~1 day if run sequentially; faster if parallelized.

These analyses become the empirical backbone of Supp Note S-Mechanism, which complements Kimi's KIMI-THEORY-2 theoretical Supp Note S-Theory.

---

## 1. Checkpoints in scope (all existing)

| Checkpoint | Path | Used in |
|:--|:--|:--|
| Canonical Ensemble HAT (NL=1.0) | `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt` | E1, E2, E3, E4, E5 |
| Canonical Standard HAT (V4 fixed-mask, NL=1.0) | best canonical Standard HAT checkpoint (find via grep) | E1, E2, E3 |
| CX-M1..M6 (severe-NL post-fix) | `checkpoints/_gpt/postfix_m_series/cx_m{N}/...` | E1, E3 |

If exact paths uncertain, Codex inspects `checkpoints/_gpt/` and reports.

---

## 2. Job E1 — Hessian eigenspectrum (~2 GPU-h)

### Goal
Compare loss-landscape sharpness across HAT variants. Hypothesis: Ensemble HAT lands in flatter minima (smaller top eigenvalues) than Standard HAT.

### Method
- Use **Hutchinson trace estimator** for trace, **Lanczos** or **power iteration** for top-k eigenvalues
- Library suggestion: `pyhessian` (Yao 2020) or roll your own
- Top-k = 50 eigenvalues per checkpoint
- Use a fixed eval batch (~256 samples from CIFAR-10 test set) for Hessian computation
- Disable analog noise during Hessian computation (we want clean loss landscape)

### Checkpoints
- Canonical Ensemble HAT (NL=1.0)
- Canonical Standard HAT (NL=1.0) — control
- CX-M1, M3, M2 (severe-NL Standard / Proportional / Ensemble at NL=2.0) — extension

### Outputs
- `report_md/_gpt/json_gpt/hessian_eigenspectrum_<checkpoint_id>.json` per checkpoint
- One figure: `paper/figures/figS_hessian_spectrum.{png,pdf}`
  - Y-axis: eigenvalue magnitude (log scale)
  - X-axis: eigenvalue index (1 to 50)
  - Lines: one per checkpoint, color-coded by HAT type
  - Caption-ready: "Top-50 Hessian eigenvalues at canonical Ensemble HAT (NL=1.0), canonical Standard HAT (NL=1.0), and severe-NL post-fix M-series checkpoints. Smaller eigenvalues indicate flatter minima."

### Decision rule
- If Ensemble HAT has 2-5× smaller top-1 eigenvalue than Standard HAT (NL=1.0): theory CONFIRMED. Headline finding.
- If similar: weaker support for flat-minima hypothesis. Honest reporting.
- If Ensemble HAT has LARGER eigenvalues: surprising negative result. ESCALATE to Claude.

---

## 3. Job E2 — Loss landscape along D2D direction (~1 GPU-h)

### Goal
Visualize that Ensemble HAT loss is flatter as D2D mismatch grows. Concrete picture of the "flatness in mismatch direction" claim.

### Method
- For canonical Ensemble HAT and canonical Standard HAT:
- Sample one D2D mask $M_0$ at $\sigma_{\text{D2D}} = 0.10$
- Vary perturbation magnitude $\alpha \in \{0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0\}$
- Compute test loss + accuracy at perturbed weights $W \odot (1 + \alpha M_0)$
- Repeat for 3-5 different $M_0$ samples to average

### Outputs
- `report_md/_gpt/json_gpt/d2d_loss_landscape.json`
- Figure: `paper/figures/figS_d2d_loss_landscape.{png,pdf}`
  - Y-axis (left): test accuracy
  - Y-axis (right, optional): test loss
  - X-axis: perturbation magnitude $\alpha$
  - Lines: Ensemble HAT (solid) vs Standard HAT (dashed); shaded region for ±std across $M_0$ samples
  - Caption-ready: "Loss landscape along the D2D mismatch direction at $\sigma_{\text{D2D}}=0.10$. Ensemble HAT degrades gracefully; Standard HAT collapses near $\alpha \geq 1$, consistent with the cross-instance generalization gap."

---

## 4. Job E3 — CKA similarity across M-series (~30 min)

### Goal
Assess whether different HAT methods learn similar internal representations under severe NL, or diverge. Useful diagnostic for "all routes recover ~80-82%" — do they recover the SAME way?

### Method
- Use **linear CKA** (Kornblith et al. 2019) on layer activations
- For each pair of CX-M{N} checkpoints, compute per-layer CKA on a fixed eval batch
- Build 6×6 similarity matrix per layer; aggregate to per-layer mean similarity
- Plot heatmap

### Outputs
- `report_md/_gpt/json_gpt/cka_mseries.json`
- Figure: `paper/figures/figS_cka_mseries.{png,pdf}`
  - 6×6 heatmap, average over layers (or per-layer subplot if richer)
  - Caption-ready: "Centered Kernel Alignment between M-series checkpoints across all transformer layers. High off-diagonal CKA indicates representational convergence despite differing training protocols."

### Decision rule
- High off-diagonal CKA (>0.8): "all routes converge" supports recipe-insensitivity claim
- Low off-diagonal CKA (<0.5): "different routes, similar accuracy by accident" — interesting and honest finding
- Mixed: per-layer breakdown explains where convergence happens

---

## 5. Job E4 — Per-layer mismatch sensitivity (~2 GPU-h)

### Goal
Identify which layers in canonical Ensemble HAT are most sensitive to D2D mismatch. Inform the "MLP path is bottleneck" claim with quantitative attribution.

### Method
- For canonical Ensemble HAT (NL=1.0):
- For each `AnalogLinear` / `AnalogConv2d` layer: perturb only that layer's D2D mask at $\sigma=0.10$, leave others zero
- Eval test accuracy
- Drop = baseline accuracy − single-layer-perturbed accuracy

### Outputs
- `report_md/_gpt/json_gpt/per_layer_d2d_sensitivity.json`
- Table: per-layer name, accuracy drop, ranked
- Figure: `paper/figures/figS_per_layer_sensitivity.{png,pdf}`
  - X-axis: layer index (in network order)
  - Y-axis: accuracy drop (pp)
  - Color bars by group (MLP / QKV / proj / patch_embed / head)
  - Caption-ready: "Per-layer D2D mismatch sensitivity in canonical Ensemble HAT. Bars show accuracy drop when only the indicated layer's D2D mask is perturbed at $\sigma_{\text{D2D}}=0.10$."

### Decision rule
- MLP layers dominate top-5 sensitivity: confirms paper's MLP-path-bottleneck claim with new evidence (and replaces the contaminated supplementary groupwise table)
- QKV / attention dominate: news, possibly reframe Discussion

---

## 6. Job E5 — Checkpoint averaging (~30 min, optional)

### Goal
Test whether seed averaging recovers Ensemble HAT generalization without per-epoch resampling. If yes: cheaper alternative; if no: emphasizes per-epoch resampling necessity.

### Method
- Take Standard HAT seed 123 + seed 456 weights, average parameter-by-parameter
- Eval on fresh instances (10 D2D × 5 MC)
- Compare against:
  - Standard HAT seed 123 alone (~10%)
  - Standard HAT seed 456 alone (~10%)
  - Ensemble HAT (~86.37%)

### Outputs
- `report_md/_gpt/json_gpt/checkpoint_average_eval.json`
- Either standalone Figure or annotation in figS_d2d_loss_landscape

### Decision rule
- If averaging recovers >50%: surprising result, makes Ensemble HAT slightly less special. Honest reporting.
- If averaging stays at ~10%: confirms per-epoch resampling is the load-bearing mechanism, not just averaging.

---

## 7. Constraints

- **No new training.** All jobs evaluate or analyze existing checkpoints.
- **No changes to canonical analog_layers.py code.** Use as-is at current commit.
- **Figures at 300dpi PNG + vector PDF**, consistent with existing paper figure style
- **JSON provenance fields**: commit hash, code sha256, CUDA device, PyTorch version, checkpoint paths
- **No new bug-fix work** unless an analysis surfaces something
- **Save logs**: `logs/_gpt/empirical_E{N}_<ts>.log` per auto-memory

---

## 8. Deliverables

| File | Source job |
|:--|:--|
| `paper/figures/figS_hessian_spectrum.{png,pdf}` + JSONs | E1 |
| `paper/figures/figS_d2d_loss_landscape.{png,pdf}` + JSON | E2 |
| `paper/figures/figS_cka_mseries.{png,pdf}` + JSON | E3 |
| `paper/figures/figS_per_layer_sensitivity.{png,pdf}` + JSON | E4 |
| `paper/figures/figS_checkpoint_avg.{png,pdf}` + JSON | E5 (optional) |
| `report_md/_gpt/CODEX_EMPIRICAL_MECHANISM_REPORT_20260425.md` | Master summary |

Master summary structure:
- §1 Provenance (one block)
- §2 Per-job results (E1..E5)
- §3 Cross-job synthesis: do the empirical findings support the theoretical predictions in KIMI-THEORY-2 (flat minima + implicit regularization)?
- §4 Paper-safe statements for Kimi to drop into Supp Note S-Mechanism

---

## 9. Sequencing

Days 1-2: E1 (Hessian) + E2 (loss landscape) in parallel where GPU permits
Days 2-3: E3 (CKA) + E4 (per-layer sensitivity)
Days 4-5: E5 (optional) + master report

Signal AGENT_SYNC per job landing.

---

## 10. Escalation

- E1 finds Ensemble HAT NOT in flatter minima: ESCALATE. Reopens NARRATIVE_PIVOT mechanism claim.
- E4 finds attention path more sensitive than MLP: news, possibly reframe Discussion §6
- E5 averaging recovers >50%: makes per-epoch resampling less special; Kimi reframes §5.7 ablation discussion

All other outcomes: normal completion, integrate per Phase 5.

---

## 11. Why this matters

The KIMI-THEORY-2 theoretical Supp Note + this Phase 2 empirical Supp Note (S-Mechanism) together form the "mechanism" subsection of Discussion. Reviewer who reads §6 sees:
- Diagnosis (hardware-instance overfitting, paper §5.5)
- Treatment (Ensemble HAT, paper §5.6)
- **Mechanism (theory + empirical, Supp Notes S-Theory + S-Mechanism)** ← this sprint
- Implications (design rules, energy)

This four-part structure is what makes a Nat Electronics paper feel complete instead of incremental.
