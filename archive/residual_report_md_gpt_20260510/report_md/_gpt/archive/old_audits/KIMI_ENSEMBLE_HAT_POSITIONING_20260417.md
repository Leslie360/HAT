<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# Ensemble HAT Novelty Boundary Audit
**Date:** 2026-04-17
**Scope:** Tight literature-and-positioning memo for reviewer-facing manuscript support.
**Constraint:** No code edits, no result fabrication, no unpublished-source disclosure.

---

## 1. Closest Prior Ideas

These are the 3–6 concepts or papers that reviewers are most likely to argue overlap with Ensemble HAT.

### 1.1 Standard fixed-mask HAT (Joshi et al. 2020; Rasch et al. 2021)
- **What it does:** Injects device noise into the forward training path and keeps one fixed D2D realization for the entire training run.
- **Why it is close:** It is the direct baseline that Ensemble HAT modifies. The manuscript shows that this baseline collapses to 10.00% on fresh hardware instances.
- **Gap:** Standard HAT does not resample the spatial D2D mask during training; it therefore optimizes against a single instance rather than a distribution of instances.

### 1.2 AIHWKIT `InjectAnalogNoise` with optional per-batch resampling (Rasch et al. 2021)
- **What it does:** Allows i.i.d. Gaussian noise to be resampled every batch.
- **Why it is close:** It is the nearest implementation in an existing open-source analog-training toolkit.
- **Gap:** The resampled noise is **i.i.d. and weight-independent**, not a spatially structured mismatch map. The fresh-instance ablation in the supplementary material shows that i.i.d. perturbation does not achieve the same transfer robustness as epoch-level structured D2D resampling.

### 1.3 Domain randomization / sim-to-real (Tobin et al. 2017)
- **What it does:** Randomizes global simulation parameters (textures, lighting, physics) during training so that the real world looks like just another variation.
- **Why it is close:** The high-level intuition—"train on a distribution of simulated conditions to improve real-world transfer"—is conceptually similar.
- **Gap:** Domain randomization varies **global environmental parameters**, not fixed spatial hardware-instance maps. D2D mismatch is tied to a specific fabricated array layout; it is static per instance and spatially correlated, unlike rendering randomization.

### 1.4 Variation-aware training (VAT) for memristor crossbars (Zhu et al. 2020 / Liu et al. 2015)
- **What it does:** Models process variation and noise statistically during training, sometimes via Monte Carlo sampling of device parameters.
- **Why it is close:** It explicitly considers fabrication variability.
- **Gap:** Existing VAT literature typically treats variation as a **statistical parameter distribution** sampled independently per weight or per layer, not as a fixed spatial map that must be jointly compensated across an entire instance.

### 1.5 Meta-learning / MAML (Finn et al. 2017)
- **What it does:** Learns an initialization that can adapt to new tasks (or new device instances) with a small number of gradient steps.
- **Why it is close:** It targets zero- or few-shot transfer to unseen conditions.
- **Gap:** MAML requires **retraining/adaptation at deployment time**. Ensemble HAT aims for zero-shot transfer without any additional updates on the target hardware instance.

---

## 2. What Is Genuinely New Here

In 3–5 bullets, the defensible novelty boundary:

- **Structured spatial-map resampling:** Ensemble HAT is, to the best of our knowledge, the first training method for analog CIM vision models that explicitly resamples **spatially structured D2D mismatch maps** at each epoch, rather than injecting i.i.d. noise or varying global scalar parameters.

- **Fresh-instance zero-shot transfer validation:** The manuscript validates the benefit on **10 unseen fixed D2D realizations** with 5 MC evaluations each, yielding 86.37 ± 1.54%. Prior HAT literature (Joshi 2020, Rasch 2021) does not report cross-instance transfer for modern vision transformers under fixed-array semantics.

- **Frequency ablation distinguishing structure from generic noise:** The supplementary ablation shows that per-epoch resampling (88.41%) outperforms fixed-mask (87.18%), per-5-epoch (87.31%), per-20-epoch (87.76%), and **per-batch i.i.d. perturbation (86.16%)**. The fact that per-batch perturbation performs *worst* among the resampling schedules is direct evidence that the benefit is not merely stronger noise regularization.

- **Instance-overfitting as a distinct failure mode:** The manuscript identifies and measures a specific failure mode—hardware-instance overfitting to a single fixed mismatch map—that causes standard HAT to collapse to 10.00% on fresh arrays, and it proposes a training-objective fix (Eq. hat-ensemble) targeted at that exact mode.

---

## 3. What Should Not Be Claimed

To avoid overclaiming, the manuscript and response should **avoid** the following phrasing:

- ❌ Do **not** claim "first-ever hardware-aware training for CIM." Fixed-mask HAT predates this work (Joshi 2020; Rasch 2021).
- ❌ Do **not** claim that Ensemble HAT is the first application of "domain randomization" to analog hardware. The term already belongs to robotics (Tobin 2017); borrowing the term without qualification invites scope critique.
- ❌ Do **not** assert that i.i.d. noise regularization has no effect. The per-batch i.i.d. control still yields ~86%, so generic noise regularization provides *some* benefit, just less than structured epoch-level resampling.
- ❌ Do **not** claim that Ensemble HAT solves *all* analog non-idealities. It specifically targets D2D instance transfer; it does not address severe nonlinear write (NL=2.0 remains at 27.72%) or sub-6-bit ADC collapse.
- ❌ Do **not** claim the per-epoch schedule is provably optimal. The frequency ablation shows it is empirically best *among the tested schedules*; the optimal cadence remains an open problem.

---

## 4. Safe Wording for Introduction

**Option A (concise):**
> Standard hardware-aware training keeps one fixed device-to-device mismatch map throughout optimization, which we show causes the model to overfit a particular hardware instance. Ensemble HAT mitigates this by resampling the spatial mismatch map at each training epoch, improving zero-shot transfer to unseen arrays from chance level to 86.37 ± 1.54%.

**Option B (with boundary):**
> Although related in spirit to domain randomization and to quantization-aware training, hardware-aware training for CIM faces an additional difficulty: device-to-device mismatch is spatially structured and fixed per instance. We therefore introduce Ensemble HAT, which resamples the mismatch map each epoch and raises fresh-instance accuracy to 86.37 ± 1.54%.

**Option C (most conservative):**
> We find that standard HAT, which holds the D2D mask fixed, collapses to 10.00% on fresh hardware instances. By resampling the spatial mismatch map at each epoch—a schedule we term Ensemble HAT—fresh-instance accuracy recovers to 86.37 ± 1.54% on Tiny-ViT.

---

## 5. Safe Wording for Discussion / Response to Reviewers

**If reviewers ask whether this is just stronger noise regularization:**
> The supplementary ablation directly compares structured D2D resampling against per-batch i.i.d. perturbation. Per-batch i.i.d. noise yields 86.16%, whereas per-epoch structured resampling yields 88.41%. Because the i.i.d. schedule actually resamples *more frequently* yet performs worse, the benefit is not attributable to noise regularization alone; the spatial structure and epoch-level cadence of the mismatch-map exposure matter.

**If reviewers ask about domain-randomization overlap:**
> Domain randomization (Tobin et al., 2017) randomizes global simulation parameters such as lighting and textures. Ensemble HAT does not vary global parameters; it resamples the fixed spatial mismatch map that characterizes a specific fabricated array. The two techniques address different transfer problems—environmental vs. instance-specific spatial mismatch—and are complementary rather than equivalent.

**If reviewers ask for a direct comparison with MI-HAT or SDR-HAT:**
> The fairest narrative is that existing multi-instance HAT formulations in the literature (e.g., Zhu et al. 2020 statistical training, Liu et al. 2015 Vortex) typically sample device parameters independently per weight or per layer rather than resampling full spatial mismatch maps. To our knowledge, no publicly available baseline implements exactly the same epoch-level spatial-map resampling protocol. Where direct apples-to-apples baselines are unavailable, the manuscript relies on internal ablations (fixed vs. i.i.d. vs. epoch-level structured) to isolate the causal contribution of the mismatch-map resampling schedule.

---

## 6. If Reviewers Ask for MI-HAT / SDR-HAT Comparisons

**Fairest narrative response (short version):**
> We are not aware of an open-source implementation of multi-instance HAT that resamples full spatial D2D maps at the epoch level. The closest available toolkit, AIHWKIT, supports only i.i.d. noise resampling, which our ablation shows is insufficient. We therefore report internal controls (fixed-mask, i.i.d. per-batch, and per-epoch structured) to bound the contribution of the resampling strategy itself.

**Fairest narrative response (long version):**
> The literature contains several variation-aware training methods (Zhu et al. 2020; Liu et al. 2015) that model device variability statistically, but these generally treat variation as a parameter distribution sampled independently per weight, not as a fixed spatial map per hardware instance. Because no existing open baseline implements the exact epoch-level spatial-map resampling protocol used here, we cannot provide an external apples-to-apples comparison. Instead, the manuscript provides three internal ablations that isolate the effect: (1) fixed-mask standard HAT, which collapses on fresh instances; (2) per-batch i.i.d. perturbation, which partially recovers but underperforms structured resampling; and (3) per-epoch structured D2D resampling (Ensemble HAT), which yields the highest fresh-instance accuracy. These internal controls constitute the strongest available evidence for the specific value of spatial-map resampling in this regime.

---

## 7. Quick-Reference Comparison Matrix

| Concept | Spatial structure | Instance transfer | Zero-shot | Training-time resampling |
|:--------|:-----------------:|:-----------------:|:---------:|:------------------------:|
| Standard HAT (Joshi 2020) | ✅ Fixed static map | ❌ Overfits single instance | ❌ 10.00% | ❌ None |
| AIHWKIT i.i.d. (Rasch 2021) | ❌ None | ⚠️ Partial | ⚠️ ~86% | ✅ Per-batch i.i.d. |
| Domain randomization (Tobin 2017) | ❌ Global params | ✅ Environments | ✅ Robotics | ✅ Global variation |
| Ensemble HAT (This work) | ✅ Epoch-level maps | ✅ Distribution | ✅ 86.37% | ✅ Per-epoch structured |

---

*End of memo.*
