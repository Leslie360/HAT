# CLAUDE FORWARD ROADMAP — All Remaining Directions Until Submission
**Date:** 2026-04-25 01:15 CST
**Author:** Claude (Chief Architect)
**Purpose:** Complete forward-path map for the project, so any successor Claude session or user can pick up without information loss. All remaining phases, items, decisions, gates, triggers, and fallbacks captured in one place.

---

## 0. Context snapshot (hand-off to future-you)

- **Project:** `/home/qiaosir/projects/compute_vit/` — organic optoelectronic CIM analog deployment of Tiny-ViT
- **Core narrative:** NARRATIVE_PIVOT_20260424.md — "Hardware-instance overfitting as diagnostic, Ensemble HAT as treatment"
- **Venue target:** Nature Electronics (primary) → Adv Sci / Nat Comm Eng (fallback)
- **Submission gate:** PhD student's defense clearance (months, not weeks)
- **Current phase:** Round-4 active (post-cross-review closure, Stage-2 ADC re-eval gate open)
- **Active remote:** 8×40GB GPU server running cross-arch ViT-Small/DeiT-Small on TinyImageNet (18-config matrix)
- **Active agents:** Kimi (text/theory), Codex (GPU/code), Gemini (error-find standby)
- **Active bug-fix commit:** `9cdbe77` (dual-bug fix) + `analog_layers.py` NL-guard + AMP decorator patches

---

## 1. The phase map

```
┌─────────────────────────────────────────────────────────┐
│ ROUND-4 (NOW) — Finish-line items                        │
│   R4-1 EN sidecars  R4-3 Stage-2 ADC  R4-4 cover letter  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ 8×40GB REMOTE RETURN — Cross-arch matrix landing         │
│   18 configs × 2 arch × 3 HAT × 3 seeds                  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ ROUND-5 — Work 2 KV-cache preliminary + batch integrate  │
│   R4-6 fires after remote return                         │
│   Claude one-pass integration                            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ ROUND-6 — Measured-D2D integration (when PhD data lands) │
│   R-D0..R-D4 ingest pipeline triggers                    │
│   Supp Note S-HW populates                               │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ ROUND-7 — Pre-submission polish + hostile review         │
│   Full manuscript compile, figure QA, supp note final    │
│   Gemini G-HOSTILE v2 reviewer simulation                │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ SUBMISSION — Nature Electronics                          │
│   Gate: PhD defense clearance                            │
│   Optional: arxiv preprint 2-4 weeks before              │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ REVIEW / REVISION → ACCEPTANCE → WORK 2 PAPER            │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Round-4 (active now)

Reference: `CLAUDE_ROUND3_CLOSURE_RULING_20260425.md`, `BROADCAST_ROUND4_20260425.md`

### Items in flight
- **R4-1**: Kimi creating EN Ch1/Ch7/Ch8 `.kimi_draft_v3` sidecars (~2-3 days)
- **R4-2**: Kimi root `paper/thesis/` README cleanup (~5 min)
- **R4-3**: Codex ADC Stage-2 per-instance recal re-eval (~3-4 GPU-h). **Gate OPEN.** Fire when GPU idle.
- **R4-4**: Kimi cover letter v6 for Nature Electronics (~1 day)
- **R4-5**: Kimi correlated-D2D zone-3A tag propagation at 14 cite locations (~30 min)

### Gated
- **R4-6**: Work 2 KV-cache preliminary — waits on 8×40GB return

### Escalation triggers
| Signal | Action |
|:--|:--|
| R4-3 Δ > 2pp | Reopen §5.7 narrative. D4 finding severity underestimated. |
| R4-3 Δ < 0pp | Halt integration. Debug per-instance cal code. |
| R4-1 finds new zone 3B contamination | Extend scrub, rerun expanded grep |

---

## 3. After R4 lands — triggers and handoffs

### Trigger T1: 8×40GB remote returns
- **What lands**: 18 fresh-eval JSONs (`cross_arch_<arch>_<hat>_seed<S>_fresh.json`) + master report
- **First action**: Claude reviews cross-host parity + Ensemble HAT pattern reproduction on ViT-Small/DeiT-Small
- **Decision rule** (from REMOTE_DISPATCH_8X40GB_CROSS_ARCH §11):
  - Ensemble ≥ Standard + 50pp → diagnostic-treatment generalizes; Kimi may promote §5.7 to include cross-arch
  - Ensemble ≥ Standard + 20-50pp → partial generalization, still paper-grade
  - Ensemble ≈ Standard → scope-limiting finding, honest write-up as "CIFAR-Tiny-ViT-specific amplification"
  - Ensemble < Standard → ESCALATE, implementation verification
- **Who writes up**: Kimi drafts `paper/latex_gpt/supplementary/S_cross_arch.tex.kimi_draft`; Claude integrates in Round-5

### Trigger T2: R4-6 fires (after T1)
- Work 2 KV-cache preliminary launches (see `DISPATCH_KIMI_CODEX_W2_KV_CACHE_PRELIM_20260424.md`)
- Codex extends `analog_layers.py` to include QKV analog path
- Warm-start from canonical V4 Ensemble HAT checkpoint, finetune 5-10 epochs
- Fresh-instance eval: Standard HAT vs Ensemble HAT on attention pathway
- Expected wall-clock: ~3-4 days
- Outcomes A (reinforcing) or B (scope-limiting) both paper-grade
- Kimi writes `paper/latex_gpt/sections/05_results_kv_preview.tex.kimi_draft_v3`

### Trigger T3: PhD measured D2D/C2C data delivered
- Activate DATA_INGEST_PROTOCOL_20260424.md
- Codex runs `scripts/ingest_measured_conductance.py` → QQ plot + stats summary
- **R-D0** (10 min): QQ plot, report whether measured is Gaussian or heavy-tailed
- **R-D1** (~6-8 GPU-h): Ensemble HAT canonical at measured D2D, 10×5 MC
- **R-D2** (~12-20 GPU-h): 63-point iso-accuracy map re-run with measured distribution
- **R-D3** (~20-30 GPU-h): Scenario 3 (severe-NL Ensemble HAT) at measured D2D, 3 seeds. Fills the [PENDING_SEVERE_NL_ENSEMBLE] cell.
- **R-D4** (~5 GPU-h, if measured is heavy-tailed): AR(1) spatial correlation study extended to measured spatial map
- Kimi populates Supp Note S-HW template with measured stats + figures
- Find-and-replace all `[LITERATURE_CALIBRATED_*]` / `[MEASURED_*]` placeholders in manuscript

---

## 4. Round-5 — Batch integration pass (Claude-owned)

**Trigger:** All of (R4-1, R4-3, R4-4, R4-6 decision, T1 cross-arch results) landed.

### Claude tasks
1. **Integrate sidecars into canonical `.tex`** — per Kimi's "Integration Ruling" in BROADCAST_KIMI_FINAL_SELF_AUDIT_20260425
   - Replace `paper/thesis/chapter_1_hat_instance_overfitting.tex` content with sidecar
   - Same for Ch4/5/7/8 EN; Ch1/5/6/7 CN
   - Delete WARNING/SUPERSEDED headers after content replaced
2. **Strip `\documentclass` wrapper from Supp Note S-Theory** (Kimi's THEORY-1 output) and `\input` it into main supplementary
3. **Integrate Methods paragraph (KIMI-THEORY-1 #2) into `03_methodology.tex`**
4. **Update §5.7 with Stage-2 per-instance cal numbers**
5. **Add cross-arch supplementary section** (if T1 landed strong)
6. **Add §5.9 Work 2 preview** (if T2 landed)
7. **Lock cover letter v6 with all final numbers**
8. **Update bib** — add Wager 2013, Tobin 2017, Kirkpatrick 2017, Hochreiter 1997 (KIMI-THEORY-1 citations)
9. **Full compile test**: `cd paper/latex_gpt && pdflatex main.tex` — verify no LaTeX errors, all refs resolve
10. **Figure checklist**: every figure in `paper/figures/` is referenced; no orphaned figures in `deprecated_20260424/`
11. **Grep gate (final)**: zero matches for zone-3B numbers, zero bug-retrospective phrasing, zero unzoned claims
12. **Append to `KIMI_PRE_SUBMISSION_CHECKLIST_20260423.md`** — final submission checklist

### Round-5 output
- `paper/latex_gpt/main.pdf` (compiled, full manuscript)
- `paper/latex_gpt/supplementary/` full
- `paper/latex_gpt/cover_letter_v6.tex` final
- `paper/thesis/` and `paper/thesis_cn/` canonical files updated
- `release_artifacts/` bundle for Zenodo ready

**Estimated Claude integration time: 2-3 days**

---

## 5. Round-6 — Measured-D2D integration (triggered by PhD data)

Could land before or after Round-5 depending on PhD timeline. Independent track.

### Tasks (if data lands)
1. Codex runs R-D0 ingest (10 min)
2. Claude reviews QQ plot, decides whether measured distribution requires downstream re-runs
3. If Gaussian-like: R-D1 sanity, fill Supp Note S-HW with statistics summary, done
4. If heavy-tailed: R-D1 + R-D2 + possibly R-D3/R-D4, larger integration
5. Kimi populates Supp Note S-HW template, updates Methods paragraph to cite measured-calibrated framework
6. Claude does surgical re-integration of measured numbers (find-and-replace placeholders)

**Upgrade impact**: "literature-calibrated simulator" → "hardware-calibrated framework against fabricated organic optoelectronic array" — big step for Nat Electronics venue.

---

## 6. Round-7 — Pre-submission polish

Trigger: Round-5 integration clean + (Round-6 measured data done OR PhD about to defend with data incoming)

### Tasks
1. **Full manuscript compile pass** — LaTeX warnings to zero
2. **Figure QA** — all figures PDF+PNG at consistent resolution, captions complete, no orphans
3. **Supp Note final review** — Claude reads top-to-bottom, consistency pass
4. **Gemini G-HOSTILE v2** — dispatch hostile reviewer simulation on final manuscript (`GEMINI_HOSTILE_REVIEW_POST_FIX_20260513.md` is the template — update date)
5. **Patch any hostile-review findings** that land in "defensible" severity; ignore "reviewer might quibble but not block" findings
6. **Claude final read-through** — single editor pass top-to-bottom of paper + supp + cover letter
7. **Prepare Zenodo bundle**: code commit hash pinned, release artifacts finalized, README in code/ directory
8. **Reviewer suggestions**: identify 3-5 suggested reviewers (avoid direct competitors, include field experts for organic CIM + analog HAT)
9. **Editor selection**: choose Nature Electronics AE with analog CIM / neuromorphic background

### Round-7 output
- Ready-to-submit manuscript
- Zenodo DOI placeholder
- Cover letter final
- Reviewer/editor suggestion list

**Estimated time: 1-2 weeks**

---

## 7. Submission and beyond

### Submission stage
- **Gate**: PhD student has defended (or has clearance to publish)
- **Primary target**: Nature Electronics
- **Action**: Claude drafts submission message, user executes submission
- **Optional**: arxiv preprint 2-4 weeks before formal submission (for DOI and community visibility) — ONLY if user approves and measured-D2D can be redacted if under embargo

### Review period (typical 4-8 weeks)
- Reviewer comments land
- Kimi drafts response letter
- Codex runs any reviewer-requested additional experiments (budget ~1-2 GPU-weeks)
- Claude coordinates revision

### If rejected at Nat Electronics
**Fallback order** (per NARRATIVE_PIVOT §5):
1. Advanced Science / Advanced Functional Materials / Advanced Electronic Materials (IF 15-19)
2. npj Computational Materials (IF 12)
3. Nature Communications Engineering (IF ~8)
4. IEEE TED / JSSC (IF 3-4) — safe floor

Each rejection triggers:
- 1-week pause, revise cover letter for new venue
- Assess whether substantive content changes needed
- Resubmit

---

## 8. After paper-1 accepted → Work 2 full paper

Work 2 is **already scoped** as a separate paper. Paper-1 carries only the 1-2 page KV-cache preview. Full Work 2 becomes its own campaign:

### Work 2 scope (from CLAUDE_WORK2_DIRECTION_LOCK_20260423)
- Full KV-cache analog CIM for long-context transformer decoding
- Multi-layer attention path analog mapping
- Long-context benchmark (1024+ tokens, LLaMA-variant or equivalent)
- Energy/latency measurement at decode phase
- Same framework + Ensemble HAT, new substrate (attention vs MLP)
- Target venue: Nature Communications (the ambition goes back up after paper-1 establishes credibility)

### When to start
- **Launch trigger**: paper-1 accepted OR paper-1 submitted with 2+ months to first reviewer response
- Claude re-activates CLAUDE_WORK2_DIRECTION_LOCK as active spec
- New Round-1 Work-2 dispatch cycle begins

---

## 9. Perennial standing items (all phases)

These are always-on, always-watch:

### S1 — AGENT_SYNC curation
- Claude monitors AGENT_SYNC_gpt.md for drift back to old narrative
- Catch any "severe-NL ceiling" language reintroduction
- Catch any unzoned number citations
- Catch any "deployment-fidelity" wording creep before Stage-2 per-instance cal locks

### S2 — Zone partition enforcement
- Every new number must map to 3A / 3B / 3C
- Every paper edit reviewed against NARRATIVE_PIVOT §3
- New findings → classify immediately

### S3 — PhD data status ping
- Monthly check-in on PhD team's measured-D2D/C2C delivery timeline
- When data lands: trigger Round-6 within 24 hours

### S4 — Remote monitoring
- 8×40GB remote run progress
- When 18-config matrix completes: review per BROADCAST_ROUND4 §1 outcome rules
- Signal R4-6 GO if appropriate

### S5 — Code hygiene
- Any new code → unit tests
- `test_dual_bug_fix.py` + `test_groupwise_nl_wrapper.py` + `test_adc_perinstance_calibration.py` must stay green
- Any new `1<NL<2` work → the NL guard (analog_layers.py:263) must cover it

---

## 10. Decisions frozen (do not reopen unless data forces it)

These are locked; reopening requires new evidence:

1. **Narrative**: "Hardware-instance overfitting as diagnostic, Ensemble HAT as treatment" (NARRATIVE_PIVOT §1)
2. **Venue target**: Nature Electronics primary, Adv Sci fallback
3. **Training path**: ADC-off differentiable surrogate (D1)
4. **Evaluation path**: ADC-on hook-based + per-instance calibration (D1 + R4-3 outcome)
5. **Severe-NL headline**: ~80-82% band (post-fix, Stage-2-adjusted)
6. **Canonical 86.37% Ensemble HAT fresh-instance**: zone 3A bug-immune (unchanged from Day 1)
7. **OPECT zero-shot 88.53%**: zone 3A (unchanged)
8. **6-bit ADC cliff**: zone 3A (unchanged)
9. **Work 2 deferred** as separate paper; paper-1 only carries preview
10. **Bug discussion**: NOT in paper body; verification goes in Supp Note S-Verification
11. **Submission gate**: PhD defense clearance ONLY
12. **Integration strategy**: batch, not incremental

---

## 11. Things that could force reopening

If any of these happen, I may need to reopen frozen decisions:

| Signal | Potentially reopens |
|:--|:--|
| Stage-2 ADC re-eval Δ > 2pp | D1 ADC protocol (maybe redo training) |
| 8×40GB cross-arch: Ensemble < Standard | NARRATIVE_PIVOT §2 scenarios, venue target |
| Measured D2D is extreme heavy-tailed | Theory derivation (KIMI-THEORY-1 second-order assumption) |
| Gemini G-HOSTILE v2 finds killer issue | Depending on issue, various decisions |
| Nat Electronics desk-rejects | Venue list, not core decisions |
| PhD data doesn't materialize | Submission without measured-D2D (honest limitation note) |
| New bug found by any agent | Scope assessment, possible rerun of affected zone |

---

## 12. Files to consult (ordered by importance for a cold start)

For future-you / future-user continuity:

1. `NARRATIVE_PIVOT_20260424.md` — narrative source of truth, zone partition
2. `CLAUDE_FORWARD_ROADMAP_20260425.md` — **this document**
3. `BROADCAST_ROUND4_20260425.md` — current active broadcast
4. `INDEX.md` — all active files with one-line descriptions
5. `AGENT_SYNC_gpt.md` — the ledger (tail it: `tail -100 AGENT_SYNC_gpt.md`)
6. `CLAUDE_ROUND3_CLOSURE_RULING_20260425.md` — most recent ruling
7. `DATA_INGEST_PROTOCOL_20260424.md` — PhD data pipeline
8. `REMOTE_DISPATCH_8X40GB_CROSS_ARCH_20260424.md` — remote task spec
9. `CLAUDE_DECISIONS_D1_D5_20260424.md` — ADC / NL-guard / theory decisions
10. `CODEX_MSERIES_ADC_DUAL_REPORT_20260424.md` — current severe-NL numbers
11. `KIMI_THEORY_1_COMPLETE_20260424.md` — Ensemble HAT theory deliverable
12. `BROADCAST_KIMI_FINAL_SELF_AUDIT_20260425.md` — last clean-state audit

---

## 13. Open questions requiring user signal (no default action)

1. **arxiv preprint before submission?** Not urgent. Decide closer to Round-7.
2. **Suggested reviewers list?** User probably has field contacts. Claude can draft, user confirms.
3. **If PhD data doesn't come**: submit with literature-prior only, honest limitation note? User call.
4. **Work 2 maximum scope escalation** (full Work 2 section in paper-1 vs keeping it as preview)? Decide after R4-6 lands.
5. **Chinese thesis defense timeline**: affects when Claude does CN-specific integration pass.
6. **If cross-arch returns weak** (Ensemble ≈ Standard on ViT-Small): downgrade venue to Adv Sci, or reframe as "Tiny-ViT-specific amplification effect"?

---

## 14. One-paragraph "if I lost context" briefing

> We're writing a paper on organic optoelectronic CIM analog deployment of Tiny-ViT transformers, target Nature Electronics, submission gated by PhD student's defense (months away). The central contribution is Ensemble HAT — a per-epoch D2D resampling training objective that fixes "hardware-instance overfitting" (Standard HAT collapses to 10% on fresh arrays, Ensemble recovers 86.37%). We have canonical results at NL=1.0 (bug-immune), post-fix severe-NL at NL=2.0 (~80-82% band), an OPECT zero-shot case study (88.53%), and a 63-point ADC×D2D iso-accuracy operating envelope. Theory is formalized as distribution-matching objective with implicit gradient-L2 regularization. A new 8×40GB remote is running cross-architecture validation on ViT-Small/DeiT-Small/TinyImageNet. Real D2D/C2C measurements from PhD collaborator are incoming. Current phase is Round-4 (finish-line items): EN thesis sidecars for 3 chapters, ADC Stage-2 per-instance recal re-eval, cover letter v6. Claude does batch integration in Round-5 after these land. No retraining needed anywhere. All zones partitioned (3A bug-immune, 3B invalidated, 3C post-fix verified). No bug-retrospection in paper body; verification discipline in Supp Note S-Verification.

---

## 15. Closing

This roadmap is the complete forward plan. Every future decision point, gate, trigger, and fallback is documented. If Claude goes offline, a successor session plus the user can execute this plan with zero information loss.

The work is in a **stable, honest, defensible state**. No hidden emergencies. No gambles riding on unfired experiments. The remaining ~1-3 months of work is polish + depth + waiting-on-data + integration — not high-risk exploration.

**Good luck to future-me.**
