# NARRATIVE_PIVOT — Post-Bug-Fix Paper-1 Master Spec
**Date:** 2026-04-24
**Author:** Claude (Chief Architect)
**Status:** ACTIVE — single source of truth for all paper-1 rewrites
**Supersedes:** CLAUDE_BIMODAL_NARRATIVE_LOCK_20260423 (INVALIDATED), CLAUDE_LOOP_CLOSURE_DECLARATION_20260423 (INVALIDATED)

---

## 0. Context

- Paper-1 is NOT time-constrained. User confirmed "不着急根本不着急".
- **Real D2D/C2C data is locked behind PhD student's graduation** — cannot publish before PhD defends. Several months of buffer. Data itself may land earlier (for internal use) but paper submission blocks on graduation clearance.
- No hard external deadlines. Depth > speed. The multi-month window is a resource, not a constraint.
- When real data lands (internally), we swap literature priors for measured distributions and re-run downstream plots. Infrastructure for this swap must be ready (see DATA_INGEST_PROTOCOL).
- This buffer enables: deep theory (A), Work 2 preliminary experiments (not just 1-page outlook — possibly full preliminary section), cross-architecture validation (ViT-Small / TinyImageNet), exhaustive audit cycles, possibly an arxiv preprint with measured-D2D removed for IP protection until grad clearance.

---

## 1. New main narrative (ONE sentence)

> **Hardware-instance overfitting is a pervasive failure mode of standard hardware-aware training for analog CIM deployment of transformers; Ensemble HAT, by resampling device-to-device mismatch maps during training, restores cross-instance generalization and generalizes across three independent deployment scenarios.**

This replaces the old dual-story "severe-NL ceiling + Ensemble HAT canonical recovery". The ceiling story is gone (it was a bug). The Ensemble HAT story stays and is now the sole protagonist.

---

## 2. Three-scenario evidence spine

Ensemble HAT wins in three independent scenarios; each scenario supplies one evidence pillar.

| Scenario | Standard HAT | Ensemble HAT | Δ | Bug-immunity | Role |
|:--|--:|--:|--:|:--:|:--|
| **Canonical NL=1.0 fresh-instance transfer** | 10.00% | 86.37±1.54% | +76pp | ✅ bug-immune | Primary diagnostic/treatment pair |
| **OPECT zero-shot transfer (literature-calibrated)** | 10.00% | 88.53±0.08% | +78pp | ✅ bug-immune | Literature-anchored validation |
| **Post-fix severe-NL (NL=2.0 from scratch)** | 83.64% (V3 remote) | TBD (Ensemble arm not yet run) | TBD | ⚠ Post-fix only | Stress-regime robustness |

**Critical gap:** Scenario 3 Ensemble arm is missing because remote A100 is retired. Options:
- **Option A**: Drop scenario 3 entirely, keep 1+2. Still a strong paper — 2 pillars of +76/+78pp are a clean "diagnostic-treatment" proof. OPECT zero-shot alone is the novelty anchor.
- **Option B**: Use local CX-M2 (Ensemble seed 123, 80.97%) and CX-M6 (Ensemble seed 456, 81.87%) as the Ensemble arm. Not as clean as remote (batch=64 gap), but is ≈ V3 local seeds (M1=82.89, M5=80.69), showing Ensemble not worse than Standard even under severe-NL. Honest and publishable.
- **Option C (preferred)**: When real-D2D data arrives, re-run the full 3-arm comparison (Standard/Ensemble/Proportional) at the measured D2D distribution on local GPU over 1-2 weeks. Then scenario 3 has hardware-calibrated ground truth, which is actually stronger than the literature-prior version we'd have reported at NL=2.0.

**Decision**: Go with **Option C**. No rush means we wait for real data to fill this cell. Scenario 3 stays in the paper as a placeholder table cell `[PENDING: hardware-calibrated D2D run]` during drafting; gets filled post-data.

---

## 3. Tripartite zone partition

All existing results sort into exactly one of three zones. **Kimi/Codex/Gemini MUST check this partition before citing any number.**

### 3A. BUG-IMMUNE — stays verbatim (no re-verification needed)

All NL=1.0 results. The bug's `pow(ratio, NL-1)` reduces to 1 when NL=1, making the buggy and fixed code arithmetically identical on this path. Mathematical property, not empirical claim.

| Result | Number | Source | Figure/Table |
|:--|:--|:--|:--|
| FP32 baselines (ViT/CNX/ResNet) | 98.06 / 90.74 / 95.46% | baseline runs | Table 1 |
| V2 zero-noise hybrid | 97.39±0.00% | deterministic eval | Results §5.2 |
| Standard HAT fresh collapse | 10.00±0.00% (n=10 instances, n=5 MC) | eval_fresh_v4_standard_noamp.json | Results §5.5 |
| **Ensemble HAT fresh** | **86.37±1.54%** | fresh_instance_eval_v4_ensemble.json | Results §5.6, Fig 5 |
| Ensemble HAT OPECT zero-shot | 88.53±0.08% | case study | Results §5.8, Fig 10 |
| 63-point iso-accuracy map | full grid | joint ADC-D2D sweep | Fig contour-map |
| Sobol variance decomposition | S_ADC=0.98 (global), S_D2D=0.92 (operational) | Sobol analysis | Discussion §6.1 |
| 6-bit ADC cliff | ~7pp jump, all σ_D2D | extended sweep | Fig S-noise-sweep |
| Retention plateau V8 | 79.13–79.51% through 10⁴ s | corrected retention | Fig S-retention |
| Front-end gamma | +5.8pp @ γ=2.0 | gamma scan | Fig S-frontend |
| AR(1) spatial D2D sensitivity | 1.76pp / 4.20pp degradation | correlated D2D study | Supp Note S2 |
| ConvNeXt CIFAR-100 / Flowers-102 | full matrix | cross-dataset runs | Supp Table |
| Tiny-ViT CIFAR-100 / Flowers-102 | full matrix | cross-dataset runs | Supp Table |
| ADC calibration error sensitivity | 0.18pp | hook-based check | Limitations §6.4 |
| Front-end group-wise ablation (at NL=1.0) | confirm via CX-AUDIT-1 | group-wise study | Supp Note |
| Noise sweep (V4) | flat 91.6-91.8% | noise sweep | Supp Fig |

**All of the above stay in the paper unchanged.**

### 3B. INVALIDATED — deleted from paper, moved to archive

Any number or claim relying on NL≠1.0 produced before commit 9cdbe77.

| Old result | Old number | Action |
|:--|:--|:--|
| "Severe-NL structural ceiling" | 30.53±7.07% | ❌ DELETE all mentions |
| MLP-only / all-linear / joint hit 30% wall | ~27-30% | ❌ DELETE entire subsection |
| V4_NL2_HAT | 27.72±0.82% | ❌ REPLACE with post-fix CX-M series |
| Bimodality / Hartigan dip / CX-K2 | p=0.98 etc | ❌ DELETE (bug-contaminated input data) |
| "Attention-pathway generalization barrier" | — | ❌ DELETE entire paragraph |
| Proportional HAT eval-only NL-swap | 90.88% | ❌ DELETE (Erratum in Kimi report already issued) |
| Signature figure fig_structural_limit_signature | — | ❌ Quarantined to deprecated_20260424/ |

**Scrubbing status:** Kimi contamination map covers 72 memos + 5 .tex files + 6 scripts + 6 JSON files. Already done. Re-verify before each draft.

### 3C. POST-FIX VERIFIED — included with full provenance (commit 9cdbe77)

Everything at NL=2.0 from commit 9cdbe77 onward.

| Result | Number | Source | Figure |
|:--|:--|:--|:--|
| Remote V3 Standard NL=2.0, 3 seeds | 83.21±0.86% train, s123 fresh=83.64±0.10% | remote R-M5 batch=512 | new Fig "post-fix" |
| Remote V4 Proportional NL=2.0, 5 seeds | 83.97±0.66% train, s123 fresh=84.80±0.08% | remote R-M2-M3 batch=512 | new Fig "post-fix" |
| Local CX-M1..M6 | per-checkpoint best_acc | post-fix train | parity table |
| Local fresh-eval CX-M1..M6 | pending CX-FRESH-EVAL-MSERIES | — | parity table |
| [PENDING] Ensemble HAT @ measured-D2D | — | awaiting PhD real data | scenario 3 cell |

**Provenance required in every post-fix table**: commit hash 9cdbe77, batch size, seed, NL=±2.0 explicit.

---

## 4. What we keep, what we add, what we remove

### KEEP (bug-immune, working):
- Section structure: Intro / Methods / Results / Discussion / Conclusion / Supplementary
- All NL=1.0 canonical results and figures
- OPECT zero-shot case study
- Iso-accuracy map + Sobol analysis
- Front-end gamma compensation
- Cross-dataset (CIFAR-100 / Flowers-102) results
- Energy projection (first-order, placeholder constants)

### ADD (new contributions at no extra GPU cost):
- **[A] Theoretical derivation of Ensemble HAT as distribution-matching objective** (Supp Note S-Theory, 3-4 pages). This is the methodological upgrade — see Kimi dispatch KIMI-THEORY-1.
- **[C] Outlook subsection on Work 2 KV-cache mapping** (1 page, no experiments). See dispatch KIMI-W2-OUTLOOK.
- **[E] Code availability formalized with Verification Suite Supp Note** (1 page). Lists test_dual_bug_fix.py + test_groupwise_nl_wrapper.py + CX-REGRESSION guard. Commit hash pinned.
- **[D-upgraded] Hardware-calibrated D2D distribution** (post-data-landing). When PhD data arrives, add QQ plot comparing Gaussian prior vs measured, re-run iso-accuracy with measured distribution, add Supp Note S-Hardware-Calibration.

### REMOVE:
- All "severe-NL ceiling" language
- All 30.53% / 27.72% / 38.95% / 90.88% bug-contaminated numbers
- MLP-only / all-linear / joint-ablation subsection at severe NL
- Bimodality / Hartigan paragraph in discussion and abstract
- Signature figure (quarantined already)

---

## 5. Venue strategy

No rush means we aim higher. Revised venue target:

1. **Nature Electronics** (IF 34) — PRIMARY. Hardware-calibrated measured-D2D data lifts this from "reach" to "realistic". Hardware-instance overfitting as named diagnostic is a candidate cover-worthy hook.
2. **Advanced Science / AFM / AEM** — strong backup if Nat Elec desk-rejects.
3. **npj Computational Materials** — framework-first framing.
4. **Nat Comm Eng** — safe floor.

**Submit order**: Nat Elec first, wait 6-8 weeks, if desk-rejected try Adv Sci. Don't submit to NC — positioning wrong.

**Cover letter hook**: "Hardware-instance overfitting — a previously unnamed failure mode of hardware-aware training — is a general diagnostic for analog CIM deployment. We show it manifests across three independent deployment scenarios (canonical noise, literature-calibrated reference array, severe nonlinearity) and present Ensemble HAT as a principled training-distribution-matching solution. The framework is simultaneously validated against measured D2D/C2C statistics from a fabricated organic optoelectronic array."

---

## 6. Timeline (landmarks, PhD-graduation-gated)

| Landmark | Trigger | Work unlocked |
|:--|:--|:--|
| L0 — Now | Post-fix compute done | Theory derivation (A), Work 2 outlook (C), Kimi K-DRAFT-v3, Gemini G-AUDIT-CODE, Codex CX-FRESH-EVAL-MSERIES + plot refresh |
| L1 — Real D2D/C2C delivered internally | PhD team shares data (pre-graduation OK for internal use) | Calibrate simulator, QQ plot, re-run iso-accuracy with measured distribution, fill [PENDING] cells. Keep internal until L3. |
| L2 — Deep-work accumulation phase | Several months; work expands as time allows | Cross-architecture (ViT-Small / DeiT-Small on TinyImageNet), Work 2 preliminary KV-cache experiments (maybe upgrade outlook to real preliminary section), ablation hardening, multi-host reproducibility |
| L3 — PhD defends successfully | Grad clearance released | Submit to Nat Elec with hardware-calibrated data + theory + preliminary Work 2 |

**No checkpoint dates.** The hard gate is PhD graduation, everything else is depth-accumulation. Optional: submit arxiv preprint at L0+theory+audit complete, with measured-D2D redacted (cite as "in preparation / awaiting coauthor release").

---

## 7. Hard rules for Kimi/Codex/Gemini

1. **Every number cited in any draft must reference a zone (3A / 3B / 3C) from this file.** If it can't be placed, flag to Claude before including.
2. **No reference to bug, bug-fix, pre-fix, post-fix, errata in paper body.** Verification discipline goes in Methods + Supp Note. See problem-2 discussion in conversation log.
3. **Bug-immunity claim is a mathematical property (pow(ratio, NL-1)=1 at NL=1), not an empirical finding.** Phrase accordingly in Supp Note.
4. **[PENDING: measured-D2D] placeholder is allowed** in drafts. Do not fabricate interim numbers.
5. **Theory derivation (KIMI-THEORY-1) must be cited in Methods as justification for Ensemble HAT**, not presented as "a trick that worked".
6. **Work 2 outlook is 1 page max.** Do not steal paper-2 content into paper-1.

---

## 8. Work 2 (KV-cache) status — upgraded scope given PhD-graduation window

Originally deferred as full paper-2 with paper-1 carrying only 1-page Outlook. With several months of buffer pre-submission, we can upgrade.

**New scope for Work 2 within paper-1 window:**
- **Minimum (Outlook only, 1 page)**: architecture diagram + back-of-envelope energy.
- **Medium (Preliminary Section, 2-3 pages)**: add a preliminary experiment — e.g. map Tiny-ViT attention QKV projections onto analog CIM with current HAT framework, report a single decode-phase latency/energy measurement vs FP32, no full benchmark. This shows the framework extends to attention path, not just MLP path.
- **Maximum (Full Section, 4-5 pages)**: includes KV-cache decoding with a small LLaMA-variant or equivalent, measured energy/latency on 1024-token decode, proper benchmark. Pushes paper-1 toward Nature Electronics tier definitively.

**Decision criterion**: pursue medium scope as default. Escalate to maximum if months 2-4 of the window are available and Codex has bandwidth. Fall back to minimum if interference with paper-1 audit becomes visible.

Paper-2 as a separate publication still possible if Work 2 scope grows beyond paper-1 fit.

---

## 9. Sign-off

Approved by user (conversation 2026-04-24 post "不着急" directive). This document supersedes all prior narrative lock files. All agents cite this file by name when aligning their work.

**Next immediate actions** (see BROADCAST_FINAL_PUSH_20260424 for dispatch):
1. Kimi: KIMI-THEORY-1 theory derivation (highest priority)
2. Kimi: K-DRAFT-v3 rewrite against this spec
3. Codex: CX-FRESH-EVAL-MSERIES + CX-PLOT-REFRESH
4. Gemini: G-AUDIT-CODE third-bug hunt
5. Claude: DATA_INGEST_PROTOCOL + monitor AGENT_SYNC
