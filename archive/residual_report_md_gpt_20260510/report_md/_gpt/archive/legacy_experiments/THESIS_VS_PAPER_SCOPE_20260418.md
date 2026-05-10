# Thesis vs. Paper Scope Decision Document

**Date:** 2026-04-18
**Purpose:** Explicit partition of work products into three tiers:
- **NC-main:** Nature Communications main text (currently 14 pp)
- **NC-supp:** Nature Communications supplementary (currently 21 pp)
- **Thesis-only:** Doctoral dissertation material, not submitted with NC paper

**Bias:** Inclusion. Thesis gets everything the paper does not take. Nothing is deleted.

---

## 1. Current NC Paper Scope (Locked)

### 1.1 NC-Main (14 pages, verified `pdfinfo main.pdf`)

Actual section order in `paper/latex_gpt/sections/`:

| § | File | Content | Contribution tier |
|:--|:--|:--|:--|
| §0 | `00_abstract.tex` | Abstract | — |
| §1 | `01_introduction.tex` | 4-contribution structure; inverse-gamma elevated to #2 | Core |
| §2 | `02_related_work.tex` | OECT/OPECT prior work, AIHWKIT/CrossSim positioning | Supporting |
| §3 | `03_methodology.tex` | Hybrid mapping, physical non-idealities, profile interface, Sobol | Supporting |
| §4 | `04_experimental_setup.tex` | Training recipe, datasets, evaluation protocol | Supporting |
| §5 | `05_results.tex` | Baseline / quantization / retention / transferability / frontend / iso-accuracy / NL+HAT / case study | Core |
| §6 | `06_discussion.tex` | Bottlenecks, transformer sensitivity, task complexity, energy, limitations, outlook | Core |
| §7 | `07_conclusion.tex` | Summary + forward look | Supporting |
| §8 | `08_appendix.tex` | Regen target — currently empty stub, see CLAUDE_TASK ledger | — |

**Figures in main:** Fig 1 (accuracy comparison), Fig 2 (HAT recovery), Fig 3 (contour map), Fig 4 (ensemble HAT concept), Fig 5 (zero-shot transfer). **System-architecture figure moved to supplementary.**

**Tables in main:** None (FP32 baselines and result-summary moved to supplementary).

### 1.2 NC-Supplementary (21 pages)

| Category | Content |
|:--|:--|
| Extended Methods | Operator mapping rationale, weight-to-conductance pipeline, system architecture tikz, NL surrogate equation, energy model |
| Experiment Details | Detailed experiment matrix (V1–V8), evaluation protocol, 3-seed summary |
| Parameter Provenance | Canonical profile parameter table, provenance notes, sensitivity checks |
| Supplementary Figures | Noise sensitivity sweep, fresh-instance ablation, attention maps, frontend compensation, SNR curves, Pareto energy, zero-shot transfer |
| Supplementary Tables | FP32 baselines, result summary, frontend γ-scan (Table S5), operator mapping, profile schema |
| Theory Notes | T1 (ISP distinction), T2 (optimal γ), T3 (attention sensitivity) |

---

## 2. Thesis-Only Material (Not in NC Submission)

### 2.1 Extended Experiments (Gemini Design Lane E1–E6)

| ID | Experiment | Scope | GPU Hours | Thesis Chapter | Priority |
|:--|:--|:--|:--|:--|:--|
| **E1** | Cross-architecture γ scan (ResNet, ConvNeXt, DeiT-Tiny) | γ_phys = 0.5–2.0 across 3+ architectures | ~40 | Frontend compensation depth | Medium |
| **E1b** | γ × HAT joint retraining (not inference-only) | Train with frontend on, vary γ | ~60 | Frontend compensation depth | Medium |
| **E2** | Cross-dataset γ robustness | CIFAR-100, Tiny-ImageNet under γ = 0.5, 1.0, 2.0 | ~80 | Generalization | Medium |
| **E2b** | + SVHN, + Flowers-102 full 3-seed | Low-data + domain-shift stress tests | ~40 | Generalization | Low |
| **E3** | Learnable compensation exponent | γ_comp as trainable parameter; validates T2 | ~30 | Theory validation | **High** (running now) |
| **E4** | AIHWKIT/CrossSim frontend sanity check | Shared-regime comparison with/without inverse-gamma | ~20 | Simulator validation | Low |
| **E5** | Tiny-ViT layer-wise γ sensitivity | Patch-embed / MLP / attention / head sensitivity | ~50 | Architecture analysis | Medium |
| **E6** | γ × NL joint sweep (16 cells × 3 seeds) | Does inverse-gamma also rescue NL=2.0? | ~200 | Interaction effects | **High** |

**Notes:**
- E3 (`run_learnable_gamma_compensation_gpt.py`) was launched earlier; treat status as "ran in this round" — verify against latest log before citing the value.
- E6 is explicitly flagged by Gemini as **high-value thesis experiment** (~200 GPU hours; 16 cells × 3 seeds).
- E1b/E2b are extensions that go beyond the paper's inference-only frontend evaluation.
- Authoritative design memo is `GEMINI_E1_E2_DESIGN_20260418.md` (now contains E1, E1b, E2, E2b, E5, E6 + Evidence Matrix).

### 2.2 NL Mitigation Queue (Codex CX-A)

| Stage | Status | Target | Thesis Value |
|:--|:--|:--|:--|
| MLP-only retraining | Running (ep 49/100) | Recover from 27.72% to ~87% | **High** — if successful, becomes a thesis chapter on surrogate-gradient design |
| QKV-only control | Queued | Isolate attention-path NL sensitivity | Medium |
| All-linear upper bound | Queued | Ceiling under perfect linearity | Medium |
| Cadence reinstated | Queued | Confirm per-epoch remains optimal | Low |

**Decision gate:** If MLP-only reaches ~87%, three placement options:
1. **NC-main §5 5th bullet** — elevates NL mitigation to core contribution (would require page expansion).
2. **NC-supp new section** — "NL Mitigation Supplementary Study" (keeps main at 14 pp).
3. **Thesis-only** — full chapter on NL surrogate design with all ablations.

*Current recommendation:* Option 2 (NC-supp) if result is clean; Option 3 if result is messy or requires extensive explanation. Main text stays 14 pp.

### 2.3 Additional Ablations & Controls (Experiment Protocol)

| Experiment | Status | Thesis Value |
|:--|:--|:--|
| ResNet-18 controlled study (W6: BN drift, noise intensity sweep, architecture comparison) | Not started | Medium — explains why ResNet-18 collapses on CIFAR-100 |
| Statistical standardization (n=5 seeds for all core claims) | Partial | Low — rigor, not novelty |
| C2C robustness trade-off (Exp 2D) | Not started | Low — completeness check |
| Spatial correlation ablation (Exp 2B) | Not started | Low — mechanism validation |
| Literature baseline comparison (Exp 2C: multi-instance HAT, domain rand, adversarial) | Not started | Medium — positions Ensemble HAT in broader landscape |

### 2.4 Measured-Device Profile Pipeline

| Asset | Status | Thesis Value |
|:--|:--|:--|
| `数据_博士/` raw measurement data (PPT-origin exports) | Live, private | **High** — thesis can show full measured-device fitting pipeline |
| Private raw-data tree (not in public repo) | Excluded from NC | **High** — device characterization chapter |
| Profile-fitting notebooks & diagnostic plots | Internal | Medium — methodology transparency |

**NC paper** only uses literature-anchored profiles (Zhang 2025 OPECT). **Thesis** can include measured-device profiles from the user's own fabricated devices, with full fitting diagnostics.

### 2.5 Additional Datasets & Evaluations

| Dataset | NC Paper | Thesis |
|:--|:--|:--|
| CIFAR-10 | ✅ Main + supp | ✅ |
| CIFAR-100 | ✅ Mentioned, limited results | ✅ Full chapter on task-complexity scaling |
| Flowers-102 | ✅ Mentioned, single-run estimate | ✅ Full 3-seed evaluation |
| ImageNet-1k | ❌ Not in paper | ✅ Evaluated (`eval_imagenet_analog.py` exists) |
| SVHN | ❌ Not in paper | ✅ Proposed in E2b |
| TinyImageNet | ❌ Not in paper | ✅ Proposed in E2b |

### 2.6 Code & Infrastructure Depth

| Component | NC Paper | Thesis |
|:--|:--|:--|
| Framework architecture diagram | ✅ High-level (supplementary) | ✅ Detailed module diagram + API docs |
| Profile JSON schema | ✅ Listed parameters | ✅ Full schema + validation + examples |
| Unit test suite | ❌ Not mentioned | ✅ `test_*.py` coverage report |
| Cross-framework comparison code | ✅ Results cited | ✅ Full pipeline + discrepancy analysis |
| Energy model derivation | ✅ Eq. referenced | ✅ Full derivation + placeholder sensitivity |

---

## 3. Cross-Tier Flow Diagram

```
Raw experiments & data
        │
        ▼
┌─────────────────────────────────────┐
│  NC-Main (14 pp)                    │
│  ─ 4 core contributions             │
│  ─ 5 figures, 0 tables              │
│  ─ Compressed methodology           │
└─────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────┐
│  NC-Supplementary (21 pp)           │
│  ─ Extended methods                 │
│  ─ Full tables (S5, etc.)           │
│  ─ Theory notes (T1/T2/T3)          │
│  ─ Additional figures               │
└─────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────┐
│  Thesis-Only Archive                │
│  ─ Extended experiments (E1–E6)     │
│  ─ NL mitigation ablations          │
│  ─ Measured-device fitting          │
│  ─ Additional datasets (IN/SVHN/..) │
│  ─ Full code documentation          │
│  ─ Statistical n=5 reruns           │
└─────────────────────────────────────┘
```

**Rule:** Data flows downward. Thesis gets everything NC takes, plus its own exclusive material. Nothing is deleted when moving between tiers.

---

## 4. Open Decision Gates

| Gate | Blocks | Decision Criteria |
|:--|:--|:--|
| **G1: NL mitigation success?** | CX-A completion, CLAUDE-A narrative decision | MLP-only ≥ 80% → promotes to NC-supp; ≥ 87% → consider NC-main 5th bullet |
| **G2: E3 learnable γ result?** | T2 theory validation | If learnable γ deviates from 1/γ_phys → strengthens T2; if not → T2 remains theoretical |
| **G3: E6 γ×NL interaction?** | Gemini G-B design, GPU allocation | If γ rescues NL=2.0 → thesis chapter + possible NC-rebuttal evidence |
| **G4: Cover letter v2** | K-B unblocking | Must wait for G1; narrative changes if NL mitigation succeeds |

---

## 5. Storage & Archive Plan

| Tier | Location | Retention |
|:--|:--|:--|
| NC-main source | `paper/latex_gpt/sections/*.tex` | Git-tracked, frozen at submission |
| NC-supp source | `paper/latex_gpt/supplementary*.tex` | Git-tracked, frozen at submission |
| Thesis-only experiments | `report_md/_gpt/GEMINI_E1_E2_DESIGN_20260418.md` (covers E1–E6) + `logs/` + `checkpoints/` | Git-tracked designs; gitignored data |
| Measured-device data | `数据_博士/`, private raw-data tree | Never in public repo; thesis appendix |
| Superseded drafts | `_archive/paper-drafts/`, `_archive/scripts-versions/` | Append-only, do not delete |

---

## 6. Action Items

| # | Action | Owner | Deadline | Depends on |
|:--|:--|:--|:--|:--|
| 1 | Finish CX-A NL queue (MLP → QKV → all-linear → cadence) | Codex | Live; MLP at Epoch 49/100 | — |
| 2 | Write NL narrative decision doc (CLAUDE-A) | Claude | After CX-A MLP completion | G1 |
| 3 | Finalize cover letter v2 (K-B) | Kimi | After CLAUDE-A lands | G4 |
| 4 | Design E1–E6 experiment matrix (G-B) | Gemini | ✅ Delivered in `GEMINI_E1_E2_DESIGN_20260418.md` | — |
| 5 | Provenance audit (CLAUDE-C) — every Locked Number → claim → script/log/JSON → blast-radius | Claude | Today | — |
| 6 | Reproducibility-package plan (outer repo / checkpoints mirror / `数据_博士` substitution) | Claude | This week | — |
| 7 | Archive thesis-only experiments to `_archive/thesis-experiments/` | Claude | After NC submission | — |
| 8 | Update `PROJECT_INDEX.md` with thesis-only paths | Claude | After scope settles | G1, G2 |

---

*This document is a living scope boundary. Update when G1–G4 resolve.*
