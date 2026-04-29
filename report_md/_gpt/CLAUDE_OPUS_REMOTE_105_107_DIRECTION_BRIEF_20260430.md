# Claude Opus — Remote 105 & 107 Future Direction Brief

**Date:** 2026-04-30 CST
**From:** Claude (Chief Architect)
**To:** User / Kimi / DS / Codex / Gemini / Remote 105 agent / Remote 107 agent / future Claude
**Status:** Architectural ruling. Companion to `CLAUDE_OPUS_FINAL_DIRECTION_BRIEF_20260430.md` (the local/paper-1 brief). This file governs the two remote research lines.
**Project root:** `/home/qiaosir/projects/compute_vit`

---

## Preamble

The local paper-1 brief (`CLAUDE_OPUS_FINAL_DIRECTION_BRIEF_20260430.md`) sets the spine for the Tiny-ViT analog HAT submission. That paper does NOT depend on 105 or 107 closing — it stands alone on local R10E + R11D evidence. **105 and 107 are independent research lines with their own narrative arcs and their own publication trajectories.** This brief treats them as such.

What this brief is for:
1. State the strategic position of each line (where the science is, what's missing).
2. Decide whether 105/107 are paper-1 supplements, paper-2/paper-3 spines, or thesis-only.
3. Rank-order the next experiments at each line (validation gate first; novelty experiments second).
4. Lock the narrative axis for each (proportional HAT regularization for 105; retention-driven rank inversion for 107).
5. Provide kill criteria and anti-patterns.

If you are an agent on 105 or 107: §6 (105) and §7 (107) are your direct task queues. Read those plus the validation gates in §4. Skip everything else.

---

## 1. One-paragraph north stars

### 1.1 Remote 105 — multi-architecture HAT validation

**The claim worth chasing.** Proportional HAT (continuous noise-aware training with magnitude-proportional D2D injection) is a robust drop-in alternative to digital training that preserves accuracy AND eliminates fresh-instance degradation, across at least two transformer architectures (deit, vit). Standard HAT collapses on fresh-instance transfer; ensemble HAT partially recovers; proportional HAT survives. **The novel contribution is not the proportional injection itself — that is a known scheme — it is the head-to-head head architectural comparison + cross-instance protocol that demonstrates the robustness story is architecture-general, not Tiny-ViT-specific.** This is a paper-1 supplement (one Discussion paragraph + one SI table) IF same-architecture digital baseline + multi-seed close cleanly. Otherwise it is thesis Chapter material.

### 1.2 Remote 107 — LLM analog KV-cache

**The claim worth chasing.** Analog KV-cache viability is governed by **temporal memory stability**, not static write precision alone. PCM at 32 states is best as a static analog cache (PPL 107.27), but under realistic cache-lifetime retention it collapses harder than organic-like profiles (PPL 751.28 vs 683.74) — a **retention-driven rank inversion**. The deployable architecture is **selective terminal-layer analog KV** (last-layer-only 8-bit passes the 10% PPL gate at 15.82/16.72 zero-noise/realistic) with HAT adaptation potentially expanding the feasible scope. This is **Work-2, separate from paper-1**, with paper-2 potential conditional on validation.

---

## 2. Current state — what we have, what's missing

### 2.1 Remote 105 inventory (as of 2026-04-29)

**Have (seed=123 single delivery):**

| Architecture | HAT mode | Source/test | Fresh mean | Fresh std |
|:--|:--|--:|--:|--:|
| deit | proportional | 50.24% | 50.20% | 0.10% |
| vit | proportional | 49.03% | 49.00% | 0.09% |
| vit | digital | 48.83% | 48.83% | 0.00% |
| deit | ensemble | 45.26% | 40.44% | 0.43% |
| vit | ensemble | 43.64% | 40.24% | 0.36% |
| deit | standard | 40.61% | 6.38% | 0.85% |
| vit | standard | 39.22% | 5.22% | 0.51% |

**Missing — required before any paper-grade claim:**
- `deit_digital` (cell that disambiguates the architecture-confounded comparison)
- Multi-seed (456, 789) on at least 4 priority cells
- Reproducibility packet (git SHA, env, exact commands, dataset/preprocessing)
- Fresh protocol audit (n_instances, MC repeats, D2D/C2C resampling policy)
- Naming clarification: "Best Train Acc" — is it training-set accuracy or source/test? The ~50% ceiling and near-equality to fresh is suspicious.
- Dataset identity confirmation (the ~50% ceiling implies a specific dataset/regime; could be a 100-class ImageNet subset, Tiny-ImageNet, or a short-training schedule)

**Promised but not yet archived locally:**
- User reports tomorrow's return may include 12-row two-seed table on a new dataset with order P > S > E. Not yet a result.

### 2.2 Remote 107 inventory (as of 2026-04-29)

**Have:**

*Selective-layer routing (the locked finding):*
- Digital baseline PPL: 15.68
- 8-bit all-layer zero-noise: 17.48 = 1.115× (fails 10% gate)
- 6-bit all-layer zero-noise: 32.41 (fails by 2×)
- Last-layer 8-bit zero-noise: 15.82 = 1.009× (PASS)
- Last-layer 8-bit realistic: 16.72 = 1.066× (PASS)
- HAT all-layer 8-bit C2C=0.01: 579.52 → 142.27 after 50 steps (still 9× baseline)

*Material/profile/retention frontier (separate sweep, possibly different model):*
- PCM 32-state, retention=0: PPL 107.27 (best static)
- Organic, retention=0: PPL 429.05
- Organic, retention=on (0.1s): PPL 683.74 (+60%)
- PCM 32-state, retention=on (0.1s): PPL 751.28 (collapse, +600%)

**Missing — required before any paper-grade claim:**
- Reproducibility packet (model id, tokenizer, transformers version, evaluator details)
- Digital-baseline + analog-no-noise parity gate (must match within 1% PPL)
- Multi-seed (3 seeds for the 4 retention cells)
- Retention-time sweep: 0 / 0.01 / 0.03 / 0.1 / 0.3 / 1.0s
- Noise-source ablation: quantization only / static programming only / read/cycle only / retention only / full
- KV scope ablation: K only / V only / K+V; last 25% layers / all layers
- HAT rescue full curve: steps 0/50/100/200/500 for all-layer + last1/2/4 selective
- Per-position NLL buckets (does failure manifest as late-context avalanche?)

**Note:** the two sweeps (selective-layer kill criterion AND material/retention) appear to be on different evaluators or different models. The selective-layer baseline is 15.68 PPL while the material sweep starts from PCM 32-state at 107.27 — likely a different model or evaluator. **This must be reconciled before either result enters a paper.**

---

## 3. Strategic position — where each line should be heading

### 3.1 Remote 105 — three plausible publication trajectories

| Trajectory | When justified | Estimated effort | Expected outcome |
|:--|:--|:--|:--|
| **A. Paper-1 supplement** | If T105-A (same-arch closure) + T105-B (multi-seed) close in 2 weeks | Low (~5 days remote) | One Discussion paragraph + one SI table; "cross-architecture validation" framing |
| **B. Paper-2 standalone (multi-arch HAT)** | If T105-C (multi-dataset) also closes cleanly + 3+ datasets show consistent P > S > E ordering | Medium (~6 weeks) | Standalone short paper for Transactions on Computers / NEMS / IEEE-TVLSI; "cross-architecture, cross-dataset robustness of proportional HAT" |
| **C. Thesis-only chapter** | If reproducibility packet doesn't return clean OR multi-seed shows std > 1pp OR multi-dataset doesn't generalize | Already paid (data exists) | Thesis Chapter on architectural generality; not for external publication |

**Claude's ruling.** Default to **(A) paper-1 supplement** as the working hypothesis. Trajectory (B) is on the table only if remote returns are clean AND user has bandwidth post-defense. Do NOT commit to (B) before defense.

### 3.2 Remote 107 — three plausible trajectories for Work-2

| Trajectory | When justified | Estimated effort | Expected outcome |
|:--|:--|:--|:--|
| **A. Paper-2 spine: selective KV + HAT** | If T107-2/T107-4 close: last1/last2 8-bit realistic stable across 3 seeds; HAT extends scope to last4 or beyond | High (~3 months) | Standalone Work-2 paper. NeurIPS/ICLR ML-systems track or HPCA/MICRO. "Selective terminal-layer analog KV-cache + HAT" |
| **B. Paper-3 spine: retention-driven rank inversion** | If T107-C (retention sweep) + T107-D (noise-source ablation) close: rank inversion is reproducible and mechanism-attributable to retention specifically | High (~4 months, requires careful provenance) | Standalone material-systems paper. Nature Electronics OR IEDM. "Static precision is not the right axis: temporal stability inverts material ranking for analog KV-cache" |
| **C. Combined Work-2 paper** | If both close, weave them into one: "Selective architecture + temporal-stability axis define the analog-KV-cache design space" | Highest | Strongest single-paper outcome; Nature Electronics or IEDM headliner |

**Claude's ruling.** Pursue (C) as the long-term goal but execute as **(A) first, (B) second**. The selective-layer story is closer to closure (kill criterion already passed at last1) and provides a deployable architecture. The retention-rank-inversion story is the more striking scientific finding but requires more validation. They unify naturally: selective-layer is WHERE to put the cache; retention-rank is WHAT material to use there.

---

## 4. Validation gates (HARD — must close before any paper claim)

### 4.1 105 validation gate

Three claims must close, in order:

| Gate | Test | Pass criterion | If fails |
|:--|:--|:--|:--|
| G105-1: Naming | Confirm "Best Train Acc" semantics | If train-set: surprising → debug. If source/test: rename column. | Stop and clarify before any other run |
| G105-2: Same-arch | `deit_digital` lands cleanly | Reports source/fresh as a clean cell | Cannot claim proportional > digital |
| G105-3: Multi-seed | seeds 123/456/789 across 4 priority cells | std < 1pp on fresh; ordering preserved | Demote to "matches digital" instead of "exceeds" |
| G105-4: Protocol | Fresh-eval protocol audit | n_instances, MC repeats, D2D/C2C policy archived | Cannot claim cross-instance robustness without this |
| G105-5: Reproducibility | Git SHA + env + commands packet | Local Codex reproduces on a smoke run | Numbers are not citable |

**No 105 paper claim ships unless G105-1 through G105-5 pass.**

### 4.2 107 validation gate

| Gate | Test | Pass criterion | If fails |
|:--|:--|:--|:--|
| G107-1: Parity | Analog-no-noise PPL vs digital baseline | within 1% | Stop; injection is buggy |
| G107-2: Baseline reconciliation | Selective-route baseline (15.68) vs material-route baseline (~107?) | Same model, same evaluator, OR explicit documentation of difference | Cannot mix the two narratives in one paper |
| G107-3: Multi-seed retention cells | seeds 42/123/456 for 4 retention cells | rank inversion preserved across seeds | Demote retention-rank-inversion claim |
| G107-4: Selective scope | last1/last2/last4 8-bit zero+realistic, multi-seed | stable PPL ratios across seeds | Selective claim limited to last1 only |
| G107-5: HAT step curve | all-layer + last1/2/4 at steps 0/50/100/200/500 | steady-state PPL recorded | Cannot make HAT-rescue claim |
| G107-6: Reproducibility | Full env + sliding-window evaluator details | Local Codex understands & could reproduce | Numbers are not citable |

**No 107 paper claim ships unless G107-1 through G107-6 pass.**

---

## 5. Risk register + reviewer attack patterns

### 5.1 Remote 105 risks

| # | Attack | Likelihood | Severity | Defense |
|:-:|:--|:-:|:-:|:--|
| R105-1 | "Architecture-confounded comparison" (deit_proportional vs vit_digital) | Certain | Critical | G105-2: deit_digital must close |
| R105-2 | "Single seed is not statistically meaningful" | Certain | High | G105-3: 3-seed minimum on priority cells |
| R105-3 | "Why does proportional exceed digital? Magic?" | High | Med | T105-E ablation: train-noise-on/eval-noise-off vs eval-fresh-on separates regularization from cross-instance robustness |
| R105-4 | "Dataset is suspiciously hard (~50% ceiling)" | High | Med | Document dataset, class count, training schedule. If short-schedule artifact, run longer schedule for a key cell. |
| R105-5 | "Fresh protocol underspecified" | Med | High | G105-4: archive n_instances/MC/D2D-C2C policy |
| R105-6 | "Cross-architecture means cross-attention; what about CNN?" | Med | Low | Honest answer: this paper is transformer-focused; CNN cross-arch is future work |
| R105-7 | "Why not include this in paper-1?" | Med | Low | Honest answer: paper-1 is Tiny-ViT-specific because PCM substrate calibration is per-architecture; 105 supplements with a transformer-family generalization |

### 5.2 Remote 107 risks

| # | Attack | Likelihood | Severity | Defense |
|:-:|:--|:-:|:-:|:--|
| R107-1 | "Two evaluators / two baselines — which is real?" | Certain | Critical | G107-2: reconcile baselines |
| R107-2 | "10% PPL gate is arbitrary" | High | Med | Cite literature on KV-cache compression PPL tolerance. Show it's a community-standard threshold (e.g. SmoothQuant, AWQ benchmarks). |
| R107-3 | "Selective-layer is a quantization trick, not material physics" | High | High | Run selective with PCM-32-state and Organic profiles; show material ranking inverts under retention even at last-layer-only |
| R107-4 | "Pythia 410M is small; doesn't generalize to 7B/70B" | Certain | Med | Honest answer: 410M is the testbed; size scaling is future work. Cite KV-cache literature showing trends extend. |
| R107-5 | "WikiText-2 is a weak benchmark; try The Pile / GSM8K" | High | Med | If validation closes on WikiText-2, expand to one additional benchmark (e.g. C4 or Lambada) before submission |
| R107-6 | "Retention=0.1s is arbitrary" | High | High | Run full retention sweep 0/0.01/0.03/0.1/0.3/1.0s; show monotonic vs threshold-like behavior |
| R107-7 | "K-only, V-only, both — does scope matter?" | Med | Med | T107-E scope ablation must close |
| R107-8 | "HAT helps but doesn't rescue all-layer; isn't HAT useless here?" | Med | Med | Honest answer: HAT extends selective scope from last1 to last2/4; it is a scope-expander, not an all-layer rescuer |
| R107-9 | "Material profiles are simulator-specific — would PCM/Organic devices behave like this in fab?" | Med | High | Cite measured profiles; document profile-equation provenance; treat as "simulator-derived predictions, not measured device behavior" |
| R107-10 | "PPL is a weak quality metric for downstream tasks" | High | Med | Add at least one downstream eval (lambada accuracy or ARC-easy) before paper |

---

## 6. Remote 105 task queue (priority-ordered)

### 6.1 P0 — must close before any paper use

| # | Task | Owner | Effort | Trigger | Done definition |
|:-:|:--|:--|:--|:--|:--|
| 1 | **Reproducibility packet return** | 105 agent | 1h | Now | Git SHA + env + commands + dataset/epoch/lr/batch/optimizer all archived in one MD chunk |
| 2 | **Naming clarification** | 105 agent | 0.5h | Now | "Best Train Acc" column renamed if it's source/test, OR explained why train-acc is reported |
| 3 | **deit_digital cell, seed=123** | 105 agent | 2-4 GPU-h | After #1 | One row appended; same-arch comparison now possible |
| 4 | **Multi-seed (456, 789) on 4 priority cells** | 105 agent | ~16-24 GPU-h | After #3 | 8 cells (4 modes × 2 architectures) × 3 seeds with mean ± std |
| 5 | **Fresh protocol audit** | 105 agent | 1h | After #1 | Per-instance fresh list + n_instances + MC + D2D/C2C policy documented |

### 6.2 P1 — strengthens if P0 closes cleanly

| # | Task | Owner | Effort | Trigger | Done definition |
|:-:|:--|:--|:--|:--|:--|
| 6 | **Proportional regularization ablation** | 105 agent | ~6-12 GPU-h | If P > D after multi-seed | train-noise-on/eval-noise-off vs eval-fresh-on for both architectures |
| 7 | **Multi-dataset validation** | 105 agent | ~24-48 GPU-h | After P0 | Run on 1-2 additional datasets (CIFAR-100 if cached, Tiny-ImageNet if cached); same matrix |
| 8 | **Pipeline task: 105 → paper-1 supplement integration** | Local Claude → pipeline | ~4h | After P0 + P1 #6 | tasks/r11_105_proportional_validation.md fired; Discussion paragraph + SI table in paper-1 |

### 6.3 P2 — opportunistic / thesis-only

| # | Task | Effort | Purpose |
|:-:|:--|:--|:--|
| 9 | Architecture extension: convnext, swin | High | Thesis chapter only |
| 10 | Larger model: vit-base/deit-base | High | Future paper-2-B if pursued |
| 11 | Training-schedule ablation (longer training) | Med | Resolves "50% ceiling" question |
| 12 | LR/optimizer sensitivity for proportional HAT | Med | Defense Q&A material |

### 6.4 KILLED / FROZEN

- ~~Mixed-NL / MLP-protected route reruns~~ (per main brief D7)
- ~~Cross-architecture into CNN families~~ (premature scope)
- ~~ImageNet-1k full~~ (compute prohibitive; not needed for paper-1 supplement)

---

## 7. Remote 107 task queue (priority-ordered)

### 7.1 P0 — must close before any paper use

| # | Task | Owner | Effort | Trigger | Done definition |
|:-:|:--|:--|:--|:--|:--|
| 1 | **Reproducibility packet** | 107 agent | 1h | Now | Git SHA + transformers version + sliding-window evaluator details + model/tokenizer/dataset preprocessing |
| 2 | **Baseline reconciliation** | 107 agent | 2-3 GPU-h | After #1 | Determine why selective baseline is 15.68 and material baseline is 107.27; document explicitly OR rerun on a single evaluator |
| 3 | **Parity gate G107-1** | 107 agent | 1-2 GPU-h | After #2 | Analog-no-noise PPL within 1% of digital baseline on the unified evaluator |
| 4 | **8-bit selective depth sweep** | 107 agent | ~8-12 GPU-h | After #3 | last1/2/4/6/8 at zero/realistic/D2D-only/C2C-only |
| 5 | **HAT step curves** | 107 agent | ~12-20 GPU-h | After #4 | all-layer + last1/2/4 at steps 0/50/100/200/500 |

### 7.2 P1 — strengthens once P0 closes

| # | Task | Owner | Effort | Trigger | Done definition |
|:-:|:--|:--|:--|:--|:--|
| 6 | **3-seed retention cells** | 107 agent | ~12 GPU-h | After P0 | seeds 42/123/456 × 4 retention cells; rank inversion preserved |
| 7 | **Retention-time sweep** | 107 agent | ~12 GPU-h | After P0 | PCM + Organic at retention {0, 0.01, 0.03, 0.1, 0.3, 1.0}s |
| 8 | **Noise-source ablation** | 107 agent | ~10 GPU-h | After P0 | Quant-only / static-only / cycle-only / retention-only / full for PCM and Organic |
| 9 | **Scope ablation** | 107 agent | ~6 GPU-h | After P0 | K-only / V-only / K+V; last 25% / all layers |
| 10 | **Selective + material fusion** | 107 agent | ~8 GPU-h | After #4 + #6 | Last1 / last2 with PCM-32-state and Organic profiles; show whether retention-rank-inversion still holds at selective scope |

### 7.3 P2 — for paper-2 / paper-3 readiness

| # | Task | Effort | Purpose |
|:-:|:--|:--|:--|
| 11 | Per-position NLL buckets | Med | Mechanism evidence: late-context avalanche vs uniform degradation |
| 12 | Larger model (Pythia 1.4B if cached) | High | Size scaling claim |
| 13 | One downstream eval (Lambada or ARC-easy) | Med | Counter-attack R107-10 |
| 14 | One additional benchmark (C4) | Med | Counter-attack R107-5 |
| 15 | 6-bit selective pilot | Med | Pareto extension if 8-bit closes |

### 7.4 KILLED / FROZEN

- ~~All-layer 6-bit noisy sweeps~~ (PPL already > 32 at zero noise; futile)
- ~~All-layer HAT beyond 200 steps~~ (if not at gate by then, abandoned)
- ~~Retention/material sweeps on all-layer scopes~~ (spend on selective)
- ~~Full noisy training of all-module Pythia~~ (cost vs scientific yield unfavorable)
- ~~Large model end-to-end training~~ (inference-only is the right testbed)
- ~~Retention extrapolation beyond 1s~~ (no physical mechanism for longer cache lifetimes in inference workloads)

---

## 8. Cross-line interactions — what 105 and 107 can borrow from each other (and from local R11D)

### 8.1 What 105 should borrow from local R11D

- **Proportional HAT framing.** The local R11D PCM result demonstrates that PCM physics enable 4-bit training. 105's proportional HAT result is the **algorithm-side analogue**: a noise-injection cadence that achieves cross-instance robustness. If both close, paper-1's contribution becomes "method (Ensemble HAT) + substrate (PCM) + cadence (proportional)" — a three-axis design space.
- **3-seed protocol.** R11D-7 PCM 3-seed showed seed std ~ 0.4pp; 105 should replicate this discipline, not single-seed.
- **Locked-number guard.** 105's headline numbers (deit_proportional, deit_digital, vit_proportional, vit_digital) should be added to `scripts/_gpt/check_locked_numbers.py` before they enter the paper.

### 8.2 What 107 should borrow from local R11D

- **Drift framing.** Local R11D 4-bit PCM shows 4.78pp/3d drift; 8-bit is flat. **107's retention-rank-inversion is the LLM-cache analogue of this same physics.** Both stories are "temporal stability matters more than static precision." Use this language in 107's paper to anchor in established physical evidence.
- **3-seed minimum.** Same as 105.
- **Profile equation provenance.** Document PCM-32-state and Organic profile equations the same way R11D documents UnitCell vs Device.
- **Fresh-instance protocol.** 107 should adopt the same n_instances × MC_repeats × D2D/C2C resampling discipline as local R11D.

### 8.3 What 105 and 107 should NOT share

- **Datasets.** 105 is image classification (CIFAR-family); 107 is language modeling (Pythia/WikiText-2). Do not try to unify the dataset; the work is in different domains by design.
- **Architecture story.** 105's "deit vs vit" comparison is a paper-1 supplement angle. 107's "selective vs all-layer" is a Work-2 architecture angle. They should not be blended.
- **GPU scheduling.** 105 and 107 are independent execution nodes. Their queues should not interleave.

---

## 9. Multi-paper structure — what gets published where

| Vehicle | Spine | Status | Estimated submission |
|:--|:--|:--|:--|
| **Paper-1: Nature Electronics** | Tiny-ViT analog HAT (Ensemble + PCM substrate) | In writing; gates on PhD defense | 2026-Q2/Q3 |
| **Paper-1 supplement (one Discussion para + SI table)** | 105 cross-architecture validation | Conditional on G105-1 through G105-5 | Same as paper-1 |
| **Paper-2: ML systems venue (NeurIPS / ICLR / HPCA / MICRO)** | Selective terminal-layer analog KV + HAT | Conditional on G107-1 through G107-6 + selective scope closure | 2026-Q4 |
| **Paper-3: Nature Electronics OR IEDM (alt. material/devices venue)** | Retention-driven rank inversion in analog KV-cache | Conditional on retention sweep + multi-seed + noise-source ablation | 2027-Q1/Q2 |
| **Combined Work-2 paper (instead of 2+3)** | Selective architecture × material temporal stability | If both #2 and #3 close cleanly together | 2027-Q1 |
| **arXiv preprint companion** | Thesis-only data (full ablation matrix, cross-arch, cross-dataset) | Post-defense | 2026-Q3 |
| **Thesis** | All of the above as chapters | At PhD defense | per defense schedule |

**Claude's ruling.** Treat the publication tree as **paper-1 first, alone**. Paper-2 and beyond are post-defense work. Do NOT delay paper-1 for 105 supplement closure or 107 results. If 105 closes in time, supplement; if not, ship paper-1 alone. 107 is decoupled — it has its own timeline.

---

## 10. Decision rules (for autonomous operation)

### 10.1 105 decision rules

| Condition | Action |
|:--|:--|
| G105-1 fails (naming unclear) | Stop until clarified; do not run more cells |
| G105-2 (deit_digital) shows P > D by ≥ 0.5pp + std < 1pp | Promote to paper-1 supplement |
| G105-2 shows P ≈ D within ±0.3pp | Demote claim to "matches digital with cross-instance robustness" |
| G105-2 shows P < D by ≥ 0.5pp | Demote further; claim is "trades small accuracy for deployment robustness" |
| G105-5 (reproducibility) doesn't close in 2 weeks | Demote to thesis-only; do NOT cite numbers in paper-1 |
| Multi-dataset shows inconsistent ordering | Frame as "architecture-dependent" in supplement; do not claim universal |
| Standard collapse fails to reproduce | Critical bug; halt all 105 work, debug protocol |

### 10.2 107 decision rules

| Condition | Action |
|:--|:--|
| G107-1 (parity) fails (>1% PPL diff) | Halt; injection is buggy |
| G107-2 (baseline reconciliation) reveals two evaluators | Choose unified evaluator; rerun headline numbers |
| Selective last1 stable across seeds + HAT extends to last2 | Lock paper-2 selective spine |
| HAT all-layer reaches PPL ≤ 1.10× by step 500 | Reopen all-layer route as HAT-dependent; expand scope |
| HAT all-layer remains > 1.20× at step 500 | Permanently close all-layer; selective is the route |
| Retention rank inversion preserved across 3 seeds | Lock paper-3 retention spine |
| Retention rank inversion vanishes under multi-seed | Demote to "single-run observation"; do not paperize |
| PCM/Organic profiles can't be defended | Treat as "simulator-derived predictions"; cite explicitly |

---

## 11. Anti-patterns (do NOT do)

For both lines:
- Do NOT push from remote (per `REMOTE_NO_PUSH_RETURN_PROTOCOL_20260429.md`).
- Do NOT send checkpoints back; only compact MD + small JSON.
- Do NOT run experiments before the validation gate closes for that line.
- Do NOT use single-seed numbers as paper claims.
- Do NOT mix 105 and 107 in the same task file.
- Do NOT skip reproducibility packet to "save time."

For 105 specifically:
- Do NOT compare across architectures without a same-architecture digital baseline.
- Do NOT run more datasets before multi-seed closes on the current dataset.
- Do NOT add new HAT modes (e.g. "annealed proportional") before the four base modes close cleanly.
- Do NOT combine 105 result with R11D PCM in a single paragraph (different layers of contribution; keep separate).

For 107 specifically:
- Do NOT run more all-layer experiments beyond the kill criterion.
- Do NOT downsize models without recording it (Pythia 410M → 160M must be flagged).
- Do NOT extrapolate retention beyond physically motivated time scales.
- Do NOT claim PCM/Organic are universally ranked one way or another. The story is rank-inversion-under-retention.
- Do NOT mix kill-criterion baseline (15.68) with material-retention baseline (107.27) without explicit reconciliation.

---

## 12. Provenance and locked numbers (CANONICAL)

### 12.1 Remote 105 — locked headline numbers (single seed, must be replaced by 3-seed)

**WARNING: these are PROVISIONAL — do not cite in any paper draft until 3-seed multi-seed closes.**

| Cell | Source/best | Fresh mean | Fresh std (single seed → instance) |
|:--|--:|--:|--:|
| deit_proportional | 50.24% | 50.20% | 0.10% |
| vit_proportional | 49.03% | 49.00% | 0.09% |
| vit_digital | 48.83% | 48.83% | 0.00% |
| deit_ensemble | 45.26% | 40.44% | 0.43% |
| vit_ensemble | 43.64% | 40.24% | 0.36% |
| deit_standard | 40.61% | 6.38% | 0.85% |
| vit_standard | 39.22% | 5.22% | 0.51% |
| deit_digital | — | — | MISSING |

Source: Remote 105 seed=123 delivery, archived in `report_md/_gpt/REMOTE_105_SEED123_DELIVERY_REVIEW_20260429.md`.

### 12.2 Remote 107 — locked headline numbers (single seed; must be 3-seed)

**WARNING: these are PROVISIONAL — do not cite in any paper draft until G107-1 through G107-6 close.**

Selective-layer route (one evaluator, baseline 15.68):
| Config | PPL | Ratio | Status |
|:--|--:|--:|:--|
| Digital baseline | 15.68 | 1.000× | reference |
| Last1 8-bit zero-noise | 15.82 | 1.009× | PASS |
| Last1 8-bit realistic | 16.72 | 1.066× | PASS |
| All-layer 8-bit zero-noise | 17.48 | 1.115× | FAIL |
| All-layer 6-bit zero-noise | 32.41 | 2.067× | FAIL |
| All-layer HAT 50 steps (8-bit, C2C=0.01) | 142.27 | 9.07× | FAIL |

Material/retention route (separate evaluator, baseline ~?):
| Config | PPL | Status |
|:--|--:|:--|
| PCM 32-state, retention=0 | 107.27 | best static |
| Organic, retention=0 | 429.05 | reference |
| Organic, retention=0.1s | 683.74 | +60% |
| PCM 32-state, retention=0.1s | 751.28 | rank-inverted to last |

Source: Remote 107 deliveries, archived in `report_md/_gpt/REMOTE_107_KV_RESULTS_REVIEW_20260429.md` and `REMOTE_107_KV_DELIVERY_REVIEW_20260429.md`.

**CRITICAL:** the two routes have different baselines (15.68 vs implicit). They cannot be cited side-by-side until G107-2 reconciles them.

---

## 13. 4-week execution path

Today: 2026-04-30 (Wed).

### Week 1 (May 1–7)
- 105: P0 #1 (reproducibility), #2 (naming), #3 (deit_digital seed=123), #5 (protocol audit)
- 107: P0 #1 (reproducibility), #2 (baseline reconciliation), #3 (parity gate)
- Paper-1: defense gate alignment + R11C + R11D narrative integration (per main brief)

### Week 2 (May 8–14)
- 105: P0 #4 (multi-seed); writeup of 105 status memo
- 107: P0 #4 (selective sweep), #5 (HAT curves)
- Paper-1: G-HOSTILE-V2; final compile

### Week 3 (May 15–21)
- 105: P1 #6 (regularization ablation) IF P > D persists; P1 #7 (multi-dataset)
- 107: P1 #6 (3-seed retention), #7 (retention sweep)
- Paper-1: submission prep / co-author distribution

### Week 4 (May 22–28)
- 105: P1 #8 (paper-1 supplement integration via pipeline) IF gates closed
- 107: P1 #8-#10 (noise-source / scope / selective+material fusion)
- Paper-2 outline draft if 107 selective spine locked

After Week 4: defense-gated for paper-1 submission. 107 paper-2 trajectory clarifies based on which gates closed. 105 either ships as supplement with paper-1 or rolls into thesis chapter.

---

## 14. Summary table — "what to do, what to ship, what to drop"

| Line | Do (next 2 weeks) | Ship (paper) | Drop |
|:--|:--|:--|:--|
| **105** | reproducibility packet + deit_digital + 3-seed; protocol audit | paper-1 supplement (1 para + SI table) IF gates close | mixed-NL reruns; ImageNet-1k; CNN-family extension |
| **107** | reproducibility packet + baseline reconciliation + parity gate + selective sweep + HAT curves | paper-2 spine (selective+HAT) IF gates close | all-layer beyond kill; 6-bit all-layer; retention sweeps on all-layer |
| **Local R11D** | Batch B/C; 6-bit pilot; R11C narrative integration | paper-1 (P1+P2+P3 spine) | R11D-T1 theory addendum; R11D-6 cadence-matched Ensemble |

---

## 15. Final words

Two parallel research lines like 105 and 107 routinely tempt projects into scope sprawl. The discipline that keeps them publishable is **gating each on its own validation matrix** before integration into any paper. We have the matrices. We have the kill criteria. We have provisional headline numbers that suggest both lines are real and substantive. What remains is to execute the gates, then choose where each line goes — paper-1 supplement, paper-2 spine, paper-3 spine, or thesis chapter.

If only 105 closes in time: paper-1 supplement, thesis chapter on cross-architecture.
If only 107 closes in time: post-defense paper-2.
If both close: post-defense paper-2 + paper-3 (or one combined Work-2 paper, which is stronger).
If neither: paper-1 stands alone on local evidence. The thesis still gets both as chapters.

In all four scenarios, **paper-1 ships first, alone, on local evidence**. 105 and 107 are upside, not requirements.

— Claude (Opus 4.7)
2026-04-30 CST
