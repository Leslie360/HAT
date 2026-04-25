# DISPATCH KIMI-ROUND4 — EN Thesis Sidecars + Housekeeping
**Date:** 2026-04-25 00:55 CST
**Issued by:** Claude
**Assignee:** Kimi
**Priority:** HIGH (ID I1, I2, I5 — R4-1, R4-2, R4-5)
**Time budget:** ~2-3 days total

---

## 0. Context

Round-3 left 3 EN thesis chapters without sidecars, relying on WARNING headers to block ingestion. This is fragile. Create proper `.kimi_draft_v3` sidecars for each, zone-scrubbed per R3-1 methodology. Plus 2 small housekeeping items (root paper/thesis stubs, correlated-D2D zone-tag update).

---

## Part A (R4-1) — EN Chapter 1, 7, 8 sidecars

### A.1 Chapter 1 — HAT Instance Overfitting

**Current state:** `paper/thesis/chapter_1_hat_instance_overfitting.tex` has WARNING header. Contains zone 3B contamination: `87.79`, `~32` references.

**Target:** `paper/thesis/chapter_1_hat_instance_overfitting.tex.kimi_draft_v3`

**Content skeleton (aligned with NARRATIVE_PIVOT §1):**
- Opening: hardware-instance overfitting as pervasive failure mode, motivating narrative
- Formal setup: fixed-mask HAT vs distribution-matching HAT (cite KIMI-THEORY-1 Supp Note S-Theory)
- Empirical signature: 10% Standard HAT collapse vs 86.37% Ensemble HAT recovery (canonical NL=1.0, zone 3A)
- Cross-scenario evidence pillars (three scenarios from NARRATIVE_PIVOT §2)
- Chapter closing: framework overview

**Target length:** ~20-25 pages CN, ~15-20 pages EN.

**Strip from old original:**
- All references to `87.79`, `~32` severe-NL numbers
- Any "structural ceiling" / "structural limit" / "structural barrier" phrasing
- Any bug-retrospective language

### A.2 Chapter 7 — Deployment

**Current state:** `paper/thesis/chapter_7_deployment.tex` has WARNING header. Note: ADC wording already patched in original (per Kimi final audit F1 table), but no sidecar exists.

**Target:** `paper/thesis/chapter_7_deployment.tex.kimi_draft_v3`

**Content skeleton (mirror of paper Discussion + Methods for deployment):**
- 7.1 Deployment framework (iso-accuracy operating envelope + Sobol)
- 7.2 Mitigation methods taxonomy (Ensemble HAT + scale-masking + gamma + ADC precision)
- 7.3 Hardware calibration protocol ([LITERATURE_CALIBRATED] placeholders + DATA_INGEST_PROTOCOL reference)
- 7.4 Design rules summary (one-page quick reference)
- 7.5 Limitations and boundary conditions
- ADC Stage-2 numbers placeholder: `[PENDING_STAGE2_ADC_NUMBERS]` — will be filled from R4-3 output

**Target length:** ~30-35 pages.

**Use locked energy numbers:**
- `~23.9 μJ analog / ~273.94 μJ FP32 / 11.45× vs FP32 / ~2.86× vs assumed INT8`
- Source: `report_md/_gpt/json_gpt/energy_scale_recovery_sensitivity.json`
- NEVER `65 pJ` / `15.4×` / `energy_sensitivity_analysis.json` (deprecated BUGGY artifact)

### A.3 Chapter 8 — Outlook

**Current state:** `paper/thesis/chapter_8_outlook.tex` has WARNING header. Contains zone 3B contamination: `27.72`, `30.53`, `32.12`, `32.60`.

**Target:** `paper/thesis/chapter_8_outlook.tex.kimi_draft_v3`

**Content skeleton:**
- 8.1 Hardware-calibration trajectory (literature → measured → fabricated-device feedback loop)
- 8.2 Framework extension directions:
  - Attention pathway (KV-cache) — cite Work 2 preview (R4-6 will populate)
  - Cross-architecture breadth (cite 8×40GB remote results when back)
  - Measured-D2D integration (DATA_INGEST_PROTOCOL)
- 8.3 Open theoretical questions (beyond second-order Taylor, higher-moment corrections)
- 8.4 Industrial deployment considerations
- 8.5 Closing: from characterization simulator to chip-predictive emulator

**Target length:** ~15-20 pages.

**Strip from old original:**
- All 27.72 / 30.53 / 32.12 / 32.60 references (zone 3B)
- Any "ceiling" or "floor" severe-NL framing

### A.4 Cross-references

All three sidecars must:
- Cite KIMI-THEORY-1 Supp Note S-Theory for Ensemble HAT formalism
- Use placeholder tags per DATA_INGEST_PROTOCOL §5 for unfilled data
- Use zone tags per NARRATIVE_PIVOT §3
- No bug-retrospective language
- Use `hook-diagnostic` not `deployment-fidelity` for all ADC references

### A.5 Deliverable

| File | Target pages |
|:--|:--|
| `paper/thesis/chapter_1_hat_instance_overfitting.tex.kimi_draft_v3` | ~15-20 |
| `paper/thesis/chapter_7_deployment.tex.kimi_draft_v3` | ~30-35 |
| `paper/thesis/chapter_8_outlook.tex.kimi_draft_v3` | ~15-20 |

Append status to AGENT_SYNC per file landing.

---

## Part B (R4-2) — Root `paper/thesis/` README cleanup

### B.1 Action

In `/home/qiaosir/projects/paper/thesis/` (root level, NOT project level):
- Delete all stub `.tex` files
- Create `README.md`:

```markdown
# Thesis (Superseded Location)

**Canonical location:** `/home/qiaosir/projects/compute_vit/paper/thesis/` (EN) and `/home/qiaosir/projects/compute_vit/paper/thesis_cn/` (CN).

This directory historically held stub files. Do not edit here. All thesis work lives in `compute_vit/paper/`.
```

### B.2 Confirm

- `diff -rq /home/qiaosir/projects/paper/ /home/qiaosir/projects/compute_vit/paper/` should show only intentional divergences or none
- Commit-safe: do not commit the README unless user approves; leave as local file

### B.3 Time: ~5 min

---

## Part C (R4-5) — Correlated D2D zone tag propagation

### C.1 Action

Per R3-2 closure: Codex confirmed zone 3A bug-immune for correlated-D2D AR(1) numbers. Now propagate this zone tag across all 14 citation locations identified in `KIMI_CORRELATED_D2D_AUDIT_REPORT_20260424.md` §1.

### C.2 Specific changes

Add explicit zone-3A tag (as LaTeX comment or visible footnote per convention) at:
- `paper/latex_gpt/supplementary.tex` §S2 preamble: one sentence "All correlated-D2D numbers in this Note are zone-3A bug-immune canonical Ensemble HAT evaluations (NL=1.0, AMP disabled; see Supp Note S-Verification)."
- `paper/latex_gpt/sections/06_discussion.tex` Limitations paragraph: inline mention "zone-3A evaluation"
- `paper/latex_gpt/cover_letter_v5.tex.kimi_draft_v3`: inline mention
- Per-chapter thesis citations: brief parenthetical "(bug-immune canonical protocol)"

### C.3 Time: ~30 min

---

## Part D — Gates & signaling

- Part A chapters can be written in any order. Land sequentially to AGENT_SYNC.
- Part B can happen immediately (housekeeping).
- Part C can happen immediately.
- **Do NOT edit original `.tex` canonical files** for Part A — create `.kimi_draft_v3` sidecars only.

### D.1 Integration contract (reaffirm)

Per Kimi final audit §"Integration Ruling":
- Original `.tex` with SUPERSEDED header: **DO NOT INGEST**
- Original `.tex` with WARNING header: **DO NOT INGEST** until sidecar exists
- `.kimi_draft_v3` sidecars: **CANONICAL** for integration

This dispatch resolves the WARNING-blocked set so all thesis canonical files have safe targets.

---

## E. Success criteria

After Round-4 R4-1/R4-2/R4-5:
- Every original `.tex` has either (a) no contamination, (b) SUPERSEDED header + sidecar, or (c) WARNING header replaced by sidecar
- Zero reliance on headers for ingestion safety (belt + suspenders)
- All 14 correlated-D2D cite locations have explicit zone-3A tag
- Root `paper/thesis/` stops being a confusion risk

No deadline. Depth > speed. PhD-graduation buffer absorbs all of this.
