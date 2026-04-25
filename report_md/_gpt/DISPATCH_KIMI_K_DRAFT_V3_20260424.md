# DISPATCH KIMI-K-DRAFT-V3 — Paper-1 Main Text Rewrite Against NARRATIVE_PIVOT
**Date:** 2026-04-24
**Issued by:** Claude
**Assignee:** Kimi
**Priority:** HIGH (after KIMI-THEORY-1 derivation lands, which Methods paragraph depends on)
**Depends on:** NARRATIVE_PIVOT_20260424.md (spec), KIMI-THEORY-1 (derivation output), DATA_INGEST_PROTOCOL_20260424.md (placeholder tags)
**Time budget:** unconstrained — PhD-graduation-gated, months of buffer

---

## 1. Objective

Rewrite the four main paper-1 files as `*.kimi_draft_v3` against the NARRATIVE_PIVOT single-narrative spec. **Every number must be placed in a zone (3A bug-immune / 3B invalidated / 3C post-fix).** Every claim must derive from verified data or from KIMI-THEORY-1 derivation.

---

## 2. Files to rewrite

| Source | Output draft | Priority |
|:--|:--|:--|
| `paper/latex_gpt/sections/05_results.tex` | `05_results.tex.kimi_draft_v3` | HIGHEST |
| `paper/latex_gpt/sections/06_discussion.tex` | `06_discussion.tex.kimi_draft_v3` | HIGH |
| `paper/latex_gpt/sections/00_abstract.tex` | `00_abstract.tex.kimi_draft_v3` | HIGH |
| `paper/latex_gpt/cover_letter_v4.tex` | `cover_letter_v5.tex.kimi_draft_v3` | MEDIUM |

Also review (not necessarily rewrite) for internal consistency:
- `01_introduction.tex` — check for severe-NL ceiling references, flag to Claude
- `07_conclusion.tex` — needs to reflect new narrative, flag to Claude

---

## 3. Core narrative anchor (COPY from NARRATIVE_PIVOT §1)

> Hardware-instance overfitting is a pervasive failure mode of standard hardware-aware training for analog CIM deployment of transformers; Ensemble HAT, by resampling device-to-device mismatch maps during training, restores cross-instance generalization and generalizes across three independent deployment scenarios.

**Every section should advance this narrative.** If a paragraph doesn't contribute, flag for removal.

---

## 4. Three-scenario spine (COPY from NARRATIVE_PIVOT §2)

| Scenario | Ensemble HAT | Δ vs Standard | Placement |
|:--|--:|--:|:--|
| Canonical NL=1.0 fresh-instance | 86.37 ± 1.54% | +76pp | Results §5.5-5.6 (existing) |
| OPECT zero-shot | 88.53 ± 0.08% | +78pp | Results §5.8 (existing, strengthen) |
| Post-fix severe-NL | [PENDING_SEVERE_NL_ENSEMBLE] | [PENDING_DELTA] | Results §5.7 (new, with placeholders) |

Scenario 3 cell stays as `[PENDING_SEVERE_NL_ENSEMBLE]` placeholder until real-D2D data arrives or a decision on Option A/B/C from NARRATIVE_PIVOT §2.

---

## 5. Zone discipline per section

### 5.1 Results (05_results.tex.kimi_draft_v3) — most work here

**Keep verbatim (zone 3A bug-immune):**
- §5.1 Baseline digital
- §5.2 Quantization and noise resilience (keep V2 97.39 paragraph, keep Fig 4)
- §5.3 Retention (V8 corrected 79%)
- §5.4 Hardware-instance transferability (Standard HAT 10% collapse — bug-immune confirmation via no-AMP rerun)
- §5.5 Physical front-end (gamma +5.8pp)
- §5.6 Iso-accuracy envelope (63 points, Sobol) — this is a major bug-immune asset, consider promoting prominence
- §5.8 Zero-shot OPECT case study

**Rewrite (zone 3C post-fix):**
- §5.7 "Nonlinear Writing and Hardware-Aware Training":
  - **REMOVE** old bimodality / 30.53% / MLP-only joint-ablation / "attention pathway barrier" content
  - **REPLACE with**: post-fix severe-NL evidence. Structure:
    1. Opening: "Under severe write nonlinearity (NL=2.0), hardware-aware training is more demanding; we verify here that the framework still recovers deployable accuracy after implementation-level code verification (see Supp Note S-Verification)."
    2. Present the 3-arm comparison: Standard (83.64 ± 0.10% fresh, s123 remote), Proportional (84.80 ± 0.08% fresh, s123 remote), Ensemble [PENDING].
    3. Note the +1.15pp Proportional advantage; frame as regime-specific: proportional noise law offers implicit regularization when noise scales with state.
    4. Statement that all three arms preserve deployability (no ~30% ceiling exists under verified implementation). One sentence. Don't belabor.
    5. Defer to Supp Table S-post-fix for full cross-host parity numbers.

**Insert (new):**
- §5.9 "Extension to attention-path KV-cache" (per KIMI-W2-OUTLOOK — 2-3 pages, Option B=Discussion placement preferred, so maybe put it there instead; see KIMI-W2-OUTLOOK §3 for that choice)

### 5.2 Discussion (06_discussion.tex.kimi_draft_v3)

**Restructure around the three scenarios**. Current structure has separate subsections per bottleneck. New structure:

- §6.1 Hardware-instance overfitting as primary deployment risk
  - Subsume existing §6.1-6.2 content
  - Cite theoretical basis (KIMI-THEORY-1 Supp Note S-Theory)
  - State that Standard → Ensemble gap (76pp canonical, 78pp OPECT) is the paper's central empirical claim
- §6.2 Secondary bottlenecks: ADC and write nonlinearity
  - Keep 6-bit cliff discussion (bug-immune)
  - Keep Sobol two-phase structure (bug-immune)
  - Trim severe-NL discussion to one paragraph on post-fix recovery
- §6.3 Scale-masking regime (V2 mechanism) — keep as-is
- §6.4 Limitations — update:
  - Remove references to severe-NL ceiling
  - Add: "Hardware calibration uses literature priors; Supplementary Note S-HW will be populated once hardware partner delivers measured D2D/C2C distributions."
  - Keep front-end and energy caveats
- §6.5 Outlook — place KIMI-W2-OUTLOOK content here

### 5.3 Abstract (00_abstract.tex.kimi_draft_v3)

Rewrite to front-load the hardware-instance overfitting narrative. Structure (~200 words):

1. Problem: analog CIM deployment of transformers promises high energy efficiency, but hardware mismatch makes training-deployment transfer unreliable.
2. Contribution 1 (diagnostic): we identify **hardware-instance overfitting** as a pervasive failure mode of standard HAT — trained models collapse (10% accuracy) on fabricated arrays with fresh D2D realizations.
3. Contribution 2 (treatment): we propose **Ensemble HAT**, a per-epoch D2D resampling training objective, theoretically grounded as implicit regularization against mismatch sensitivity (analog of dropout-as-L2).
4. Evidence: Ensemble HAT restores 86.37 ± 1.54% fresh-instance accuracy on Tiny-ViT / CIFAR-10, 88.53% on a literature-calibrated reference array (OPECT), and recovers [POST_FIX_SEVERE_NL_NUMBER] under severe write nonlinearity.
5. Framework: system-level simulator with 63-point iso-accuracy operating envelope, 6-bit ADC deployment cliff, front-end gamma compensation, and hardware-calibration-ready data ingest for measured device statistics.
6. Impact: diagnostic and treatment generalize across three independent deployment scenarios, constituting design rules for organic optoelectronic CIM deployment.

Remove from abstract: bimodality, Hartigan dip, severe-NL ceiling, MLP-only ablation.

### 5.4 Cover letter (cover_letter_v5.tex.kimi_draft_v3)

Target Nature Electronics. One-paragraph version of abstract + "why Nature Electronics":
- Hardware-algorithm co-design is your scope
- Organic CIM is an emerging substrate with growing field interest
- Our hardware-instance overfitting concept names a failure mode not previously isolated in analog CIM literature
- Ensemble HAT is a principled training method with theoretical grounding (Supp Note S-Theory)
- Cross-scenario validation (3 scenarios) demonstrates framework generality
- Calibration against fabricated-array measurements (pending coauthor data release) is included

Suggest associate editors: whoever handles analog CIM / neuromorphic / organic electronics at Nat Electronics.

---

## 6. Placeholder tags (use EXACTLY these, they'll be sed-replaced at integration)

From DATA_INGEST_PROTOCOL §5:
- `[LITERATURE_CALIBRATED_D2D: σ=10%, Gaussian prior from ReRAM literature \citep{fastirdrop2025,iconniv2026}]`
- `[LITERATURE_CALIBRATED_C2C: σ=5%, Gaussian prior]`
- `[MEASURED_D2D_DISTRIBUTION: pending from coauthor data]`
- `[MEASURED_SIGMA_D2D_VALUE]`
- `[MEASURED_SIGMA_C2C_VALUE]`
- `[HARDWARE_CALIBRATION_SUPP_NOTE_REFERENCE]`

New placeholders for this dispatch:
- `[PENDING_SEVERE_NL_ENSEMBLE]` — single accuracy value
- `[PENDING_DELTA]` — one delta vs Standard
- `[POST_FIX_SEVERE_NL_NUMBER]` — use 84.80% or Ensemble number once decided

---

## 7. Hard constraints

- **Zone check**: every numerical claim must map to zone 3A / 3B / 3C from NARRATIVE_PIVOT §3. If you cannot place it, do NOT cite it. Flag to Claude.
- **No bug discussion in main text**. Methodological verification goes in Supp Note S-Verification (separate dispatch, not this one).
- **No ceiling language anywhere**. Not in abstract, results, discussion, cover letter, captions, anywhere.
- **Cite KIMI-THEORY-1 Supp Note S-Theory** in Methods and Discussion as the justification for Ensemble HAT.
- **Keep all figure references but update captions** where they're now about post-fix data (Fig 5, Fig S3-ensemble, new post-fix fig, new cross-host parity fig — see DISPATCH_CODEX_PLOT_REFRESH).
- **Keep all Supp Note references** but update S-theory / S-HW / S-verification / S-cross-host cross-references as they come online.
- **Word count discipline**: don't inflate. Where you remove content, don't "backfill" just to preserve length.

---

## 8. Deliverables

| File | What |
|:--|:--|
| `paper/latex_gpt/sections/05_results.tex.kimi_draft_v3` | Full results rewrite |
| `paper/latex_gpt/sections/06_discussion.tex.kimi_draft_v3` | Full discussion rewrite |
| `paper/latex_gpt/sections/00_abstract.tex.kimi_draft_v3` | Abstract rewrite |
| `paper/latex_gpt/cover_letter_v5.tex.kimi_draft_v3` | Cover letter (v5 = v4 + new narrative) |
| `report_md/_gpt/KIMI_K_DRAFT_V3_DELIVERY_20260424.md` | Summary: what changed per file, which placeholders used, flags for Claude on 01_intro / 07_conclusion inconsistencies |

---

## 9. Workflow discipline

- Do NOT edit the .tex files directly. Only write .kimi_draft_v3 siblings. Claude integrates later.
- Commit drafts incrementally; don't hold all four for a mega-PR.
- Append status block to AGENT_SYNC when each file lands.
- Flag cross-section inconsistencies immediately — don't patch them silently.

**No deadline.** Depth > speed.
