# DISPATCH KIMI-ROUND3-THESIS — Full Thesis Chapters 5-7 Drafting
**Date:** 2026-04-24 22:30 CST
**Issued by:** Claude
**Assignee:** Kimi
**Depends on:** CLAUDE_ROUND2_CLOSURE_RULING §2 R3-1; NARRATIVE_PIVOT_20260424.md
**Priority:** HIGH (largest single writing deliverable)
**Time budget:** ~1-2 weeks, no hard deadline

---

## 1. Objective

Complete the Chinese PhD thesis chapters 5-7 from current stubs / drafts to full submission-quality prose, aligned with NARRATIVE_PIVOT_20260424.md. CN thesis is the primary PhD defense artifact; English paper-1 feeds into the thesis but doesn't substitute.

Current state per `paper/thesis_cn/`:
- `chapter_5_failure_modes.tex` — exists but `chapter_5_failure_modes.tex.kimi_draft_v2` sidecar suggests out-of-date content
- `chapter_6_work2_scope.tex` — exists, needs alignment with new KIMI-W2-OUTLOOK
- `chapter_7_deployment.tex` — exists but has `.kimi_draft_v2` sidecar
- `chapter_8_outlook.md` — markdown, not converted

English side `paper/thesis/`:
- Already has chapters 1-8 in `.tex`, but some drifted from NARRATIVE_PIVOT

---

## 2. Scope per chapter

### 2.1 Chapter 5 — Failure Modes (both CN and EN)

**Target:** ~30-40 pages CN, ~25 pages EN.

**Narrative anchor (from NARRATIVE_PIVOT §1):** Hardware-instance overfitting as primary failure mode.

**Structure:**
- 5.1 Taxonomy of failure modes for analog CIM transformer deployment (diagnostic framing)
  - Hardware-instance overfitting (primary focus — subsumes 76pp / 78pp / severe-NL evidence)
  - Scale-masking regime (V2 analysis)
  - ADC precision cliff (6-bit threshold)
  - Spatial correlation degradation (AR(1))
  - Retention drift
  - Write nonlinearity (NL=2.0 severe-NL)
- 5.2 Diagnostic protocols — how to detect each failure mode
- 5.3 Case studies from the experimental matrix
  - Canonical NL=1.0 fresh-instance (10 → 86.37)
  - OPECT zero-shot (10 → 88.53)
  - Post-fix severe-NL NL=2.0 (train-surrogate vs ADC-on)
  - Proportional-noise regime-specific robustness
- 5.4 Chapter summary + bridge to Chapter 6 (mitigation)

### 2.2 Chapter 6 — Physical Realism + Work 2 Scope

**Note:** Current structure has Chapter 6 as "work2_scope" (CN) / "physical_realism" (EN). Reconcile:
- EN Chapter 6 = Physical Realism (IR drop, sneak paths, retention, correlated D2D, front-end gamma, energy model, ADC hook validity)
- CN Chapter 6 = Work 2 scope (KV-cache mapping preview)

**Decision:** Keep this asymmetry. EN thesis is paper-1-mirror. CN thesis has PhD-defense-specific Work 2 framing. Each serves its purpose.

**EN Chapter 6 target:** ~25 pages. Physical realism deep dive, cites all Supp Notes.

**CN Chapter 6 target:** ~15 pages. Work 2 framing — KV-cache opportunity, architecture mapping, preliminary energy estimate, roadmap.

### 2.3 Chapter 7 — Deployment (both CN and EN)

**Target:** ~30-35 pages.

**Structure:**
- 7.1 Deployment framework (iso-accuracy operating envelope + Sobol)
- 7.2 Mitigation methods taxonomy
  - Ensemble HAT (central — cite theory derivation Supp Note S-Theory)
  - Scale-masking calibration
  - Front-end gamma compensation
  - ADC precision selection (6-bit cliff as design rule)
- 7.3 Hardware-calibration protocol (reference DATA_INGEST_PROTOCOL; [LITERATURE_CALIBRATED] placeholders for where measured-D2D data will land)
- 7.4 Design rules summary (one-page quick reference for device engineers)
- 7.5 Limitations and boundary conditions

---

## 3. Hard constraints

- **Zone discipline**: every numerical claim cited in thesis maps to NARRATIVE_PIVOT §3 zone 3A / 3B / 3C. No unzoned numbers. Use placeholders where data not yet available (`[LITERATURE_CALIBRATED_D2D]`, etc. per DATA_INGEST_PROTOCOL §5).
- **No bug-retrospective language** in any chapter body. Same rule as paper: verification discipline lives in dedicated "Implementation Verification" appendix, not scattered through narrative.
- **CN and EN parity on core claims**: if chapter 5 EN says "76pp gap", chapter 5 CN says "76 个百分点" — no story-drift between the two.
- **Cite KIMI-THEORY-1 Supp Note S-Theory** in Chapter 7 as justification for Ensemble HAT (not "a trick that worked").
- **Placeholders are allowed**: `[PENDING_MEASURED_D2D]`, `[PENDING_WORK2_KV_PRELIM]` as noted in NARRATIVE_PIVOT. Use the exact tag strings for mechanical find-and-replace at integration.

---

## 4. Process

Work in this order (dependencies exist):

1. **Chapter 5 first** (failure modes) — sets diagnostic framing
2. **Chapter 7 second** (deployment / mitigation) — cites chapter 5 diagnostics
3. **EN Chapter 6** (physical realism) — cites chapters 5+7 for context
4. **CN Chapter 6** (Work 2 scope) — last, aligned with KIMI-W2-OUTLOOK + any preliminary experiments if R3-6 lands

Produce each as `chapter_N_*.tex.kimi_draft_v3` sidecar. Do not overwrite canonical `.tex` files. Claude integrates at batch end.

---

## 5. Coordination points

- **With KIMI-THEORY-1**: Chapter 7 deployment section needs the implicit-regularizer formalism. Kimi already has this content. Drop in with edits for thesis audience.
- **With DATA_INGEST_PROTOCOL**: Chapter 7 calibration section + S-HW supplementary hookup.
- **With KIMI-W2-OUTLOOK**: CN Chapter 6 inherits Work 2 framing. Upgrade if R3-6 lands with preliminary experiment.
- **With DISPATCH_KIMI_CODEX_CORRELATED_D2D_AUDIT (R3-2)**: Chapter 5 AR(1) citation depends on R3-2 provenance confirmation.

---

## 6. Deliverables

| File | Content | Status |
|:--|:--|:--|
| `paper/thesis_cn/chapter_5_failure_modes.tex.kimi_draft_v3` | Full CN chapter 5 | ~30-40 pages |
| `paper/thesis/chapter_4_failure_modes.tex.kimi_draft_v3` (or 5) | Full EN chapter 5 equivalent | ~25 pages |
| `paper/thesis_cn/chapter_7_deployment.tex.kimi_draft_v3` | Full CN chapter 7 | ~30-35 pages |
| `paper/thesis/chapter_7_deployment.tex.kimi_draft_v3` | Full EN chapter 7 | ~30-35 pages |
| `paper/thesis/chapter_6_physical_realism.tex.kimi_draft_v3` | Full EN chapter 6 | ~25 pages |
| `paper/thesis_cn/chapter_6_work2_scope.tex.kimi_draft_v3` | Full CN chapter 6 | ~15 pages |
| `KIMI_ROUND3_THESIS_DELIVERY_<date>.md` | Per-chapter change summary, zone map, placeholders list | Status report |

---

## 7. Progress signaling

Append to AGENT_SYNC_gpt.md per chapter landing:
```
[Kimi] Thesis chapter <N> (<CN/EN>) first draft complete; <pages> pages; zone-mapped; placeholders [<tag1>, <tag2>] for post-data swap.
```

No need to wait for all 6 chapters before signaling — land them as they complete.

---

## 8. Success criteria

- 6 chapter drafts in `.kimi_draft_v3` sidecars
- All numeric claims zone-mapped
- CN and EN parity on core narrative
- KIMI-THEORY-1 formalism cited in mitigation discussion
- Placeholders mechanical for post-data integration
- Claude can do a final integration pass without major rewrites

**No deadline. Depth > speed.**
