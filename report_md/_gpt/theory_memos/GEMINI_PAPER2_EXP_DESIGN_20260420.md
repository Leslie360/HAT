# G-GG6: Paper-2 Experimental Design — Core Experiment Suite

**Date:** 2026-04-20  
**Author:** Gemini Phase β — Round P2  
**Scope:** Anchor Paper-2 in executable experiments within the current compute-ViT codebase. No unreported digits; all cited numbers reference locked thesis chapters, archived JSON logs, or pre-registered predictions from G-GG1–G-GG4.  
**Sources:** `train_tinyvit_ensemble.py`, `scripts/_gpt/run_tinyvit_groupwise_nl_comp.py`, `analog_layers.py`, `GEMINI_STRUCTURAL_LIMIT_FORMAL_20260420.md` (G-GG1), `GEMINI_HIGHER_ORDER_NL_DESIGN_20260420.md` (G-GG2), `GEMINI_PATHWAY_DECOMPOSITION_20260420.md` (G-GG3), `GEMINI_FIRST_ORDER_LIMIT_20260420.md` (G-GG4), Paper-2 skeleton (`paper/paper2/draft_v0/SKELETON.md`).

---

## 1. Preamble: Constraints on Experimental Design

Paper-2 is theory-first, but theory must be grounded in reproducible experiments. The following constraints govern the design:

1. **All experiments must run inside the existing PyTorch stack.** No new simulators, no new model families, no new dataset requirements beyond CIFAR-10/100.
2. **Group-wise NL manipulation is already implemented.** The `run_tinyvit_groupwise_nl_comp.py` wrapper provides `build_selector` and `make_groupwise_setter` for per-block surrogate assignment (`mlp`, `qkv`, `attn_proj`, `patch_embed`, `all`, `none`).
3. **Ensemble HAT cadence is already implemented.** `train_tinyvit_ensemble.py` provides per-epoch D2D resampling (`resample_all_d2d_noise`) and the canonical V1–V7 experiment matrix.
4. **Fresh-instance evaluation is already implemented.** The protocol `10 fresh instances × 5 MC forward passes` is codified in `diag_fresh_instance.py` and used for all locked numbers.
5. **Backward hooks in `analog_layers.py` must accommodate second-order STE.** This requires a minor extension (see G-GG2, §4.2), but the architecture is ready.

The experiment suite is therefore a **combinatorial design** over existing primitives, not a call for new infrastructure.

---

## 2. Experiment E1: CX-J1b — QKV-Only Linearization + Ensemble HAT

### 2.1 Research question
Is the `~30%` fresh-instance ceiling localized to the QKV projection specifically, or to the attention pathway as a whole? If QKV-only linearization breaks the ceiling, the structural bottleneck is the QKV-to-output-projection interaction described in G-GG3, §4.

### 2.2 Method
- **Selector:** `build_selector("qkv")` from `run_tinyvit_groupwise_nl_comp.py`.
- **Protected group:** `.attn.qkv` layers receive `NL_LTP = 1.0`, `NL_LTD = -1.0`.
- **Exposed group:** All other analog layers (`.attn.proj`, `.mlp.fc1`, `.mlp.fc2`, `patch_embed.*`) retain `NL_LTP = 2.0`, `NL_LTD = -2.0`.
- **Training recipe:** Ensemble HAT, per-epoch D2D resampling, 100 epochs, AdamW (`lr = 5e-4`, weight decay `0.05`), cosine annealing, batch size 64, CIFAR-10.
- **Warm-start:** None (cold start from ImageNet-pretrained Tiny-ViT-5M, as in canonical V4).
- **Evaluation:** Fresh-instance protocol (`10 instances × 5 MC`).

### 2.3 Expected result
Under the attention-pathway-dominance hypothesis (G-GG1, §3; G-GG3, §6.1), QKV-only linearization is predicted to **stay near the `~30%` ceiling**. The reasoning is that linearizing QKV in isolation creates a **decoupled optimization**: QKV receives clean gradients while the attention output projection receives distorted gradients. The optimizer adapts `W_V` and `W_O` to a distortion that `W_Q` and `W_K` do not sense, tearing the attention mechanism between incompatible objectives.

### 2.4 Relation to existing work
This is a strict follow-up to the CX-J1 joint-training result (`30.53 ± 7.07%`, `joint_mlp_linear_ensemble_hat_full_fresh.json`). It isolates whether the failure is specific to QKV or generic to the entire attention path.

### 2.5 Implementation notes
The group-wise wrapper already supports `"qkv"` as a selector. No code changes beyond command-line invocation:
```bash
python scripts/_gpt/run_tinyvit_groupwise_nl_comp.py \
  --protected-group qkv --protected-nl-ltp 1.0 --protected-nl-ltd -1.0 \
  --name-suffix _cxj1b_qkv_only -- --epochs 100 --dataset cifar10
```

---

## 3. Experiment E2: CX-J1c — Output-Projection-Only Linearization + Ensemble HAT

### 3.1 Research question
Symmetric to E1: is the bottleneck the attention output projection (`attn.proj`) rather than QKV? If output-projection-only linearization breaks the ceiling, the barrier is the inverse of value aggregation described in G-GG3, §5.

### 3.2 Method
- **Selector:** `build_selector("attn_proj")`.
- **Protected group:** `.attn.proj` layers receive `NL = 1.0`.
- **Exposed group:** QKV, MLP, and patch-embedding layers retain `NL = 2.0`.
- **Training recipe:** Identical to E1.

### 3.3 Expected result
Under the attention-pathway-dominance hypothesis, CX-J1c is also predicted to **stay near `~30%`**. The reasoning is symmetric: if QKV is distorted, the attention scores are computed from corrupted queries and keys, and linearizing the output projection cannot restore the corrupted score geometry (G-GG3, §6.2).

### 3.4 Unified falsification criterion
The structural hypothesis is supported if and only if:
```
FreshAcc(E1) ≈ FreshAcc(E2) ≈ FreshAcc(CX-J1) ≈ 30%.
```
If either E1 or E2 breaks the ceiling while the other does not, the hypothesis must be refined into a **sub-path hypothesis** identifying which specific matrix (Q, K, V, or O) is the bottleneck.

### 3.5 Implementation notes
```bash
python scripts/_gpt/run_tinyvit_groupwise_nl_comp.py \
  --protected-group attn_proj --protected-nl-ltp 1.0 --protected-nl-ltd -1.0 \
  --name-suffix _cxj1c_attn_proj_only -- --epochs 100 --dataset cifar10
```

---

## 4. Experiment E3: CX-J1d-2 — Second-Order STE in Attention Blocks

### 4.1 Research question
Is the `~30%` ceiling a **first-order artifact** (truncated Taylor expansion of the write dynamics) or a **deeper structural property** of the attention pathway? If the second-order Taylor-corrected STE (G-GG2, §2) breaks the ceiling, the barrier is surrogate-dependent, not architecture-dependent.

### 4.2 Method
- **Architecture:** All analog layers at `NL = 2.0` globally.
- **Surrogate modification:** In `AnalogLinear` / `AnalogConv2d` backward hooks, replace the first-order STE with the second-order STE:
  ```
  grad_input = grad_output * (phi_prime + 0.5 * phi_double_prime * delta_g_eff)
  ```
  where `phi_prime = NL * |G|^(NL-1)` and `phi_double_prime = NL*(NL-1)*|G|^(NL-2)`.
- **`delta_g_eff`:** Set to `sigma_d2d * (G_max - G_min) + sigma_c2c * |G|`, auto-populated from the experiment config.
- **Group-wise override:** Apply second-order STE *only* to attention blocks (QKV + proj); keep MLP blocks on first-order STE to isolate the attention-pathway effect. This can be implemented by checking `classify_tinyvit_layer(name)` in the backward hook.
- **Training recipe:** Ensemble HAT, 100 epochs, identical hyperparameters to E1/E2.

### 4.3 Expected result
Under the structural-limit hypothesis (G-GG1, §3), the second-order correction is predicted **not to exceed 50% fresh-instance accuracy**. The reasoning is that the barrier arises from the *interaction* between the attention pathway's bilinear QK^T geometry and the state-dependent conductance mapping, not merely from gradient-approximation error. Even a perfect gradient would still face the rank-collapse and scale-recovery-mismatch mechanisms.

Under the first-order-insufficiency hypothesis (G-GG4, §5.1), the second-order correction should show a measurable lift (> 10 percentage points) relative to the first-order baseline.

### 4.4 Relation to existing work
This is the most important diagnostic in the suite. It directly adjudicates between the two dominant theoretical interpretations of the ceiling. The implementation path is described in G-GG2, §4.2.

### 4.5 Implementation notes
Requires a minor patch to `analog_layers.py`:
1. Add `use_second_order_ste: bool = False` and `delta_g_eff: float = 0.0` to `AnalogLinearConfig`.
2. In the backward hook (implied by STE usage), branch on `config.use_second_order_ste`.
3. In `run_tinyvit_groupwise_nl_comp.py` or a new wrapper, set `use_second_order_ste = True` for modules matching `"attn"`.
4. Add `torch.clamp(|G|, min=1e-4)` to avoid divergence at `G ≈ 0` for `NL = 2.0` (G-GG2, §6, Risk 1).

Compute cost: `~1.1×` backward-pass overhead, negligible versus attention forward cost. Estimated wall time: ~7 hours on RTX 4090.

---

## 5. Experiment E4: CX-J1d-3 — Cumulant Expansion (Third-Order) in Attention Blocks

### 5.1 Research question
Does propagating variance sensitivity (second cumulant) and skewness sensitivity (third cumulant) into the backward pass further improve generalization? This tests whether stochastic programming dynamics, not just deterministic curvature, are responsible for the ceiling.

### 5.2 Method
- **Architecture:** All analog layers at `NL = 2.0` globally.
- **Surrogate modification:** Use the cumulant-corrected STE (G-GG2, §3.2):
  ```
  ∂L/∂G = (∂L/∂Ĝ)·μ₁'(G) + ½ (∂²L/∂Ĝ²)·μ₂'(G) + ⅙ (∂³L/∂Ĝ³)·μ₃(G)
  ```
  The second derivative of the loss is obtained via PyTorch double-backward.
- **Scope:** Applied to attention blocks only, as in E3.
- **Training recipe:** Ensemble HAT, 100 epochs.
- **Memory mitigation:** Enable activation checkpointing for analog linear layers if OOM occurs (G-GG2, §4.3).

### 5.3 Expected result
If the barrier is purely a deterministic gradient-approximation error, the cumulant expansion should show incremental improvement over the second-order STE. If the barrier is structural, the cumulant expansion will not escape the `~30%` ceiling. The structural-limit hypothesis predicts **no significant lift beyond E3**.

### 5.4 Implementation notes
Requires double-backward:
```python
grad_hat = torch.autograd.grad(loss, hat_G, create_graph=True)[0]
hessian_term = torch.autograd.grad(grad_hat.sum(), hat_G, retain_graph=True)[0]
```
Memory cost: `~1.5×` versus first-order. Feasible on 24 GB VRAM with batch size 64. Estimated wall time: ~9 hours.

---

## 6. Experiment E5: Mixed Digital-Analog Partition (Attention Digital, MLP Analog)

### 6.1 Research question
If the attention pathway is indeed the structural bottleneck under severe NL, can we **bypass the barrier entirely** by keeping attention weights in digital memory while mapping only the MLP and patch-embedding layers to analog arrays? This tests the most radical architectural implication of the structural-limit hypothesis.

### 6.2 Method
- **Architecture modification:** In `convert_to_hybrid` (from `analog_layers.py`), skip conversion for layers matching `"attn.qkv"`, `"attn.proj"`, and `"attn"` generally. These layers remain standard `nn.Linear`/`nn.Conv2d` in FP16/FP32.
- **Analog scope:** `patch_embed.*`, `.mlp.fc1`, `.mlp.fc2` only.
- **NL regime:** `NL = 2.0` for all analog layers; digital layers are ideal.
- **Training recipe:** Ensemble HAT, 100 epochs, CIFAR-10.
- **Energy note:** Do not report absolute energy numbers (placeholders only). Report the *relative* energy cost of digital attention versus the baseline hybrid model.

### 6.3 Expected result
If the structural-limit hypothesis is correct, this partition is predicted to **restore deployment-grade accuracy** (> 80% fresh-instance) because the bottleneck pathway is removed from the analog domain. The cost is increased digital memory bandwidth and area.

If accuracy remains near `~30%`, the hypothesis is falsified: either the MLP path is also severely affected under global `NL = 2.0` (contradicting G-GG3), or the patch-embedding layer is the hidden bottleneck (contradicting the all-linear control, `32.60 ± 9.18%`).

### 6.4 Relation to existing work
This implements **Direction C** from G-GG4, §5.3, and validates the industrial trade-off discussed in Paper-1 Discussion ("digital attention still dominates total energy, roughly 60%"). It is also the strongest positive-control experiment: if *anything* can break the ceiling, removing attention from analog should.

### 6.5 Implementation notes
Requires a one-line patch to `convert_to_hybrid` or a post-conversion filter:
```python
def deconvert_attention_layers(model):
    for name, module in model.named_modules():
        if "attn" in name and isinstance(module, (AnalogLinear, AnalogConv2d)):
            # Replace with equivalent nn.Linear / nn.Conv2d
            # preserving weight shape and initialization
            pass
```
Alternatively, modify the `convert_to_hybrid` call site in `train_tinyvit_ensemble.py` to accept an exclusion regex.

---

## 7. Experiment E6: Rank-Collapse Diagnostic (Training-Time SVD Trajectory)

### 7.1 Research question
Does severe NL induce **rank collapse in Q/K projections**, as predicted by Pillar I of G-GG1? This is a pure diagnostic with no mitigation intent; it provides mechanistic evidence for the structural hypothesis.

### 7.2 Method
- **Training runs:** Two checkpoints trained under identical conditions except NL regime:
  - Baseline: `NL = 1.0` globally, Ensemble HAT.
  - Severe: `NL = 2.0` globally, Ensemble HAT.
- **Metric:** Every 10 epochs, compute the effective rank of `W_Q` and `W_K` for each transformer stage:
  ```
  r_eff = number of singular values > 0.01 × σ_max
  ```
- **Logging:** Write to JSON/WandB. Track the sum `r_Q + r_K` per layer.

### 7.3 Expected result
Under Pillar I (G-GG1, §3.1), we predict:
```
r_Q(NL=2.0) + r_K(NL=2.0) < r_Q(NL=1.0) + r_K(NL=1.0)
```
specifically a rank deficit of at least 25% relative to the `NL = 1.0` baseline (Condition F1). If no rank deficit is observed, Pillar I is falsified.

### 7.4 Relation to existing work
This is the first empirical test of Condition F1. It transforms a theoretical prediction into an observable training dynamic. The rank-collapse mechanism connects to broader literature on transformer rank degeneration (e.g., low-rank bias in deep linear networks).

### 7.5 Implementation notes
Add a callback in `train_tinyvit_ensemble.py`:
```python
if epoch % 10 == 0:
    with torch.no_grad():
        for name, module in model.named_modules():
            if ".attn.qkv" in name:
                w = module.weight  # or reconstructed effective weight
                u, s, v = torch.linalg.svd(w, full_matrices=False)
                rank = (s > 0.01 * s[0]).sum().item()
                log_dict[f"{name}/rank_qk"] = rank
```
Note: `module.weight` for QKV is a concatenated `[W_Q, W_K, W_V]` tensor in most timm implementations; slice appropriately.

---

## 8. Experiment Summary Table

| ID | Experiment | Protected / Modified | NL (protected) | NL (exposed) | STE order | Predicted fresh-instance | Falsifies if |
|---|---|---|---|---|---|---|---|
| E1 | CX-J1b | QKV only | 1.0 | 2.0 | 1st | `~30%` | > 50% |
| E2 | CX-J1c | Attn proj only | 1.0 | 2.0 | 1st | `~30%` | > 50% |
| E3 | CX-J1d-2 | Attn blocks | — | 2.0 | 2nd (attn) | `~30%` (structural) or > 40% (surrogate) | > 50% |
| E4 | CX-J1d-3 | Attn blocks | — | 2.0 | 3rd (cumulant) | `~30%` or slight lift | > 50% |
| E5 | Mixed dig/ana | Attention digital | N/A (digital) | 2.0 (MLP/emb) | 1st | > 80% | < 50% |
| E6 | Rank diagnostic | None | 1.0 vs 2.0 | — | — | Rank deficit ≥ 25% | No deficit |

---

## 9. Compute Budget and Scheduling

| Experiment | GPU-hours (RTX 4090) | Wall time | Dependencies |
|---|---|---|---|
| E1 (CX-J1b) | ~6 | 1 day | None |
| E2 (CX-J1c) | ~6 | 1 day | None |
| E3 (CX-J1d-2) | ~7 | 1 day | Minor `analog_layers.py` patch |
| E4 (CX-J1d-3) | ~9 | 1 day | E3 patch + double-backward |
| E5 (Mixed dig/ana) | ~6 | 1 day | `convert_to_hybrid` exclusion logic |
| E6 (Rank diagnostic) | ~6 | 1 day | SVD callback |
| **Total** | **~40** | **1 week (parallelizable)** | — |

All six experiments can execute in parallel on a 4-GPU node. The critical path is the code patches for E3/E4/E5, which require at most 2 hours of development each.

---

## 10. Fallbacks and Risk Mitigation

| Risk | Mitigation |
|---|---|
| E3/E4 code patch introduces bugs | Run the `NL = 1.0` baseline through the patched hook; verify identical accuracy to unpatched run. |
| E5 digital attention exceeds GPU memory | Reduce batch size to 32; use gradient accumulation. Accuracy trend is the metric, not absolute throughput. |
| E6 SVD too slow on CPU | Run SVD asynchronously in a background process every 10 epochs; skip if training is paused. |
| Fresh-instance variance too high (σ > 12 pp) | Increase to `n = 15` instances; recompute SEM and Cohen's d. |
| Any experiment yields ambiguous result (e.g., 42%) | Report the number honestly; discuss whether it supports a *weak* structural limit or a *partial* surrogate improvement. Do not force interpretation. |

---

## 11. Statistical Treatment

All fresh-instance comparisons use the protocol from Paper-1 (see `paper/paper2/draft_v0/03_methods.md`, §Statistical Treatment):
- `n = 10` independent D2D realizations per lane
- Primary metric: mean ± standard deviation across instance means
- Effect size: Cohen's `d` between lane means
- Significance: Welch's two-sample t-test, two-tailed, `α = 0.05`
- Power: `n = 10` is sufficient to detect a 7 pp difference at observed `σ ≈ 7–9` pp with power `1 – β = 0.80`

The ceiling-convergence claim (R-A narrative) requires not merely overlapping confidence intervals but also a **small effect size** (`d < 0.3`) between the three severe-NL lanes (E1, E2, CX-J1 joint baseline).

---

## 12. Summary

Six core experiments are proposed, all executable within the existing compute-ViT codebase. E1 and E2 isolate the attention bottleneck to sub-paths. E3 and E4 test the surrogate-order hypothesis. E5 tests the architectural-partition hypothesis. E6 provides mechanistic diagnostics. Together they form a **falsification lattice**: if the structural-limit hypothesis is correct, E1–E4 should converge on `~30%`, E5 should escape to `> 80%`, and E6 should reveal rank collapse. If any experiment violates its prediction, the hypothesis is refined in a direction specified in advance. This design maximizes epistemic value while minimizing implementation risk.
