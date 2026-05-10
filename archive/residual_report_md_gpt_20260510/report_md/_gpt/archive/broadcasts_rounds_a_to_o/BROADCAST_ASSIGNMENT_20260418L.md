> Canonical coordination: `AGENT_SYNC_gpt.md` | Task ledger: `CLAUDE_TASK_gpt.md`

# Round L Broadcast — 2026-04-19 03:30 (post-Round-K closure; pre-submission red team + thesis fork)

**Author:** Claude (Chief Architect)
**Trigger:** All Round-K work landed. Reviewer-blocking text closed; correlated-D2D experiment locked (iid 86.33±1.61 / ρ=0.3 84.57±2.39 / ρ=0.5 82.12±3.95, ranking preserved); bundle rebuilt; 16/16 locked-numbers pass. Only user metadata blocks formal submission.
**Quota policy (unchanged):** Kimi ✅ heavy · Gemini 🟡 medium · Codex 🔴 tight (preserve for matplotlib + final bundle).
**Round L theme:** This is the **adversarial / hardening round**. Assume the package will be desk-rejected unless we red-team it ourselves first; in parallel, open the thesis-only fork and reproducibility archive.

---

## Where we stand on disk

| Pillar | Status |
|:--|:--|
| Main + supp + cover | ✅ recompile clean, no warnings |
| Bundle `outputs/submission_bundle_20260419/` | ✅ rebuilt (main 17pp 265 KiB, supp 22pp 2.16 MiB) |
| Locked numbers | ✅ 16/16 pass via `check_locked_numbers.py` |
| 5 reviewer items | ✅ B-1/B-2/B-3 closed; 6 should-fix landed; nice-to-have folded |
| CX-CA correlated-D2D | ✅ full 10×5 sweep folded into §6.5 + Supp SX.Z |
| Gemini design briefs G-Z1–Z4 | ✅ available for thesis fork + future figure |
| Response letter | ✅ `RESPONSE_LETTER_FINAL_20260419.md` updated |
| User metadata | ⛔ still pending (user-owned: acknowledgements, corresponding author/email, suggested reviewers) |

---

## Strategic frame for Round L

Three parallel tracks:

1. **Red team the submission package** — assume an editor will spend 8 minutes on desk review; find the things that would kill us in those 8 minutes. (Kimi heavy, Gemini one design brief)
2. **Reproducibility & archive hardening** — Zenodo-ready archive, source-data manifest, code snapshot integrity. (Codex tight)
3. **Open thesis-only fork** — joint MLP-Linear + Ensemble HAT training spec; ImageNet pilot scoping; thesis chapter draft. (Gemini design, Kimi outline)

These three tracks are **independent** and can run in parallel.

---

## KIMI — Round L (HEAVIEST; 8 tasks)

### 🔴 Track 1: Red-team pre-submission audit

| ID | Item | Deliverable | Spec |
|:--|:--|:--|:--|
| **K-S1** | **Hostile-reviewer end-to-end pass** on `outputs/submission_bundle_20260419/manuscript.pdf` + `supplementary.pdf` + `cover_letter.pdf` | `KIMI_RED_TEAM_AUDIT_20260419.md` (≤2 pages) | Read as if you were a hostile NeurIPS area chair with 8 min to decide desk-reject vs send-out. List CRITICAL (would kill us) / SHOULD-FIX (cosmetic but visible) / NICE (style). For each CRITICAL item, propose a one-line patch. |
| **K-S2** | **Figure caption audit** | `KIMI_FIGURE_CAPTION_AUDIT_20260419.md` | For every figure in main + supp: (a) does the caption stand alone if the figure is read out of context? (b) does it cite the table/equation it depends on? (c) does it explicitly state error-bar protocol where applicable? Flag any where the answer is no with a one-line patch. |
| **K-S3** | **Notation / glossary sweep** | `KIMI_NOTATION_AUDIT_20260419.md` | Grep main + supp for every Greek symbol, every subscripted variable, every acronym (CIM, HAT, D2D, MC, AR(1), NL, QKᵀ, ADC, MLP, etc.). Confirm each is defined at first use; produce a list of exceptions with the line numbers needing a one-word patch. |
| **K-S4** | **Citation completeness** | `KIMI_CITATION_AUDIT_20260419.md` | Grep `paper/latex_gpt/` for `[?]`, `XXX`, `TODO`, `FIXME`, `\cite{}` (empty), or any reference that points to a placeholder. Confirm `references.bib` has no duplicate keys and all `\cite` keys resolve. Report PASS/FAIL with line numbers for any FAIL. |

### 🟡 Track 2: Cover letter & response letter final pass

| ID | Item | Deliverable | Spec |
|:--|:--|:--|:--|
| **K-S5** | **Cover letter final polish** | edits to `paper/latex_gpt/cover_letter.tex` (or its source) | After K-S1 lands, fold any CRITICAL items into the cover letter framing. Ensure cover letter explicitly mentions the four reviewer-strengthening additions (correlated-D2D ablation, two-level MC disclosure, all-linear upper-bound control, collapsed-predictor framing). Recompile cover_letter.pdf. |
| **K-S6** | **Editor's-eye 100-word abstract variant** | `KIMI_EDITOR_ABSTRACT_VARIANT_20260419.md` | Compose a 100-word "if the editor only reads one paragraph" version. Different rhetorical center from the existing abstract: lead with **what the framework reveals** (instance-overfitting failure mode + Ensemble HAT mitigation + bounded spatial-correlation degradation) rather than what we built. For Editor consideration; not a manuscript edit. |

### 🟢 Track 3: Thesis fork

| ID | Item | Deliverable | Spec |
|:--|:--|:--|:--|
| **K-S7** | **Thesis chapter outline** absorbing Gemini's G-Z3 brief | `KIMI_THESIS_CHAPTER_OUTLINE_20260420.md` (≤3 pages) | Translate Gemini's narrative ordering (collapse → linearization-bound → spatial robustness → joint-training upgrade) into a concrete chapter skeleton: section/subsection headers, what figure goes where, what experimental result anchors each subsection. Identify which sections share content with the NC manuscript (cite + don't repeat) vs which are thesis-only. |
| **K-S8** | **Source-data README readability pass** | edits to `outputs/submission_bundle_20260419/README_SUBMISSION.txt` (or upstream source) | Read as a downstream user who wants to reproduce Fig 4 from the bundled source_data zip. Fix any path that's wrong, any column that's undocumented, any reference to a script that's not in the bundle. |

**Kimi NOT doing this round:** any new GPU experiments; any new figure generation (Codex track).

---

## GEMINI — Round L (medium; 5 stateless design briefs)

### 🔴 Track 1: Adversarial editor view

| ID | Item | Deliverable | Spec |
|:--|:--|:--|:--|
| **G-AA1** | **Top-3 plausible desk-reject reasons** + neutralization for each | `GEMINI_DESK_REJECT_DEFENSE_20260419.md` (≤300 words) | Steelman the case for desk-reject from a Nature-Communications editor's perspective. List 3 most-likely killshots (e.g., "scope too narrow for NC", "framework not validated against fabricated arrays", "ImageNet missing"). For each, write a 2-sentence rebuttal pointing to the exact place in current source where we already address it. Tone: editor-facing, not defensive. |

### 🟢 Track 3: Thesis fork & forward experiments

| ID | Item | Deliverable | Spec |
|:--|:--|:--|:--|
| **G-AA2** | **ImageNet pilot scoping doc** | `GEMINI_IMAGENET_PILOT_SCOPE_20260420.md` (≤500 words) | Cover letter promises ImageNet as future work. Spec: (a) which subset (ImageNet-100 vs full 1k); (b) which Tiny-ViT variant + scaling; (c) D2D protocol (per-epoch vs per-batch); (d) compute budget estimate (GPU-hours); (e) decision points (when do we pivot to a smaller model); (f) what success looks like (accuracy floor + ranking preservation criterion). |
| **G-AA3** | **MLP-Linear + Ensemble HAT joint training spec** (thesis punchline) | `GEMINI_JOINT_TRAINING_SPEC_20260420.md` (≤500 words) | Per Gemini's own G-Z3: this is the thesis-only "solution" beyond NC paper's "diagnostic". Spec: (a) loss formulation; (b) initialization (warm-start from Ensemble HAT vs from MLP-Linear vs joint cold); (c) D2D resampling cadence under joint regime; (d) target metric (recover ≥80% fresh-instance from current 32%); (e) ablation matrix; (f) GPU-hour budget. |
| **G-AA4** | **Fig CORR_D2D production refinement** | `GEMINI_FIG_CORR_D2D_FINAL_SPEC_20260420.md` (≤200 words + ASCII sketch) | Now that full CX-CA data exists (iid 86.33 / ρ=0.3 84.57 / ρ=0.5 82.12), refine your G-Z4 sketch with actual numerical bounds. Decide: main figure vs supplementary figure? Caption draft. Specify exact matplotlib parameters Codex will use (axis limits, error-bar style, color palette consistent with Fig 1/4). |
| **G-AA5** | **100-word press / Nature-Briefing variant** | `GEMINI_PRESS_BLURB_20260420.md` | A non-technical 100-word version suitable for Nature Briefing or institutional press release. Audience: scientifically literate but not in CIM. Tone: declarative, no hedging. (For user to review; not a manuscript edit.) |

**Gemini NOT doing this round:** any source-tex edits, any GPU work, any bundle work.

---

## CODEX — Round L (TIGHT quota; matplotlib + final bundle only)

| ID | Item | Type | Priority | Gate |
|:--|:--|:--|:--:|:--|
| **CX-EA** | **Generate Fig CORR_D2D** from Gemini's G-AA4 spec | matplotlib | MED | After G-AA4 lands. Place output at `paper/figures/figS_corr_d2d.png` + integrate into `supplementary.tex` (or main if Gemini decides main). Recompile clean. |
| **CX-EB** | **Zenodo-ready archive** | bundle | MED | Anytime CPU. Build `release_artifacts/zenodo_archive_v0/` containing: (a) `source_data_v1.zip` (or current); (b) `code_snapshot/` (frozen pointer to current commit); (c) `CITATION.cff`; (d) `README.md` with reproducibility instructions; (e) hash manifest. Do NOT actually upload — produce the archive ready for user to push to Zenodo. |
| **CX-EC** | **Pre-flight bundle integrity check** | script | HIGH | After K-S1–S5 land + after CX-EA recompile. Verify: (a) main.pdf + supp.pdf + cover.pdf exist + open + page counts match expected (17/22/2); (b) hyperref links live (no broken cross-refs); (c) source_data zip extracts cleanly; (d) README path references all valid. Report `CODEX_PREFLIGHT_20260420.md` PASS/FAIL. |
| **CX-ED** | **Final bundle rebuild on user-metadata landing** | bundle | HIGH | TRIGGER: when user supplies acknowledgements + corresponding author + suggested reviewers. Insert into source, recompile, refresh bundle, run `check_locked_numbers.py`, hand off to CLAUDE-AY for final go/no-go. |

**Codex DEFERRED:** CX-AC joint MLP-Linear + Ensemble HAT training (now spec'd by Gemini G-AA3 — execution moves to a future round once spec approved).

---

## CLAUDE self

| ID | Task |
|:--|:--|
| **CLAUDE-AV** | After K-S1 lands: read the red-team audit and personally classify each CRITICAL item — accept/reject/escalate. |
| **CLAUDE-AW** | Decide Fig CORR_D2D main-vs-supp placement after G-AA4 (default: supp; promote to main only if it strengthens §6.5). |
| **CLAUDE-AX** | Compose `USER_METADATA_REQUEST_20260420.md` — exact field-by-field template the user fills in (one form, 5 minutes), so user metadata stops being the bottleneck. |
| **CLAUDE-AY** | After CX-ED: final bundle spot-check, locked-numbers re-pass, declare submission-ready. |
| **CLAUDE-AZ** | Pre-emptive rebuttal-prep notes file `CLAUDE_REBUTTAL_PREP_20260420.md` — anticipate top-5 reviewer objections we have NOT pre-empted yet, with answer outlines. (For our own use after submission.) |

---

## USER (still blocking; one form will unblock all of CX-ED)

Use the form Claude will produce in CLAUDE-AX (`USER_METADATA_REQUEST_20260420.md`):

- Acknowledgements text (funding/grant line) — *user previously said: "123，是学校单位，我自己写"*
- Corresponding author + email
- Suggested reviewers (3–5 with affiliation + email)

---

## Execution pipeline

```
t0 (now):
  Kimi launches K-S1, K-S2, K-S3, K-S4 in parallel (red team + audits)
  Kimi launches K-S6, K-S7, K-S8 in parallel (no source dependencies)
  Gemini launches G-AA1, G-AA2, G-AA3, G-AA4, G-AA5 in parallel (all stateless)
  Codex starts CX-EB Zenodo archive (CPU, no dependencies)
  Claude starts CLAUDE-AX user-metadata form

t+1h:
  K-S1–S4 audits land → CLAUDE-AV triage
  G-AA1 desk-reject defense in (informs K-S5 cover letter polish)
  G-AA4 Fig spec in → CX-EA can start
  Gemini design briefs all in

t+2h:
  Kimi K-S5 cover letter polish using K-S1 + G-AA1
  Codex CX-EA Fig CORR_D2D land + recompile
  Claude CLAUDE-AW placement decision

t+3h:
  Codex CX-EC pre-flight integrity check
  Claude CLAUDE-AZ rebuttal-prep notes

[blocked on USER METADATA]:
  Codex CX-ED final bundle rebuild
  Claude CLAUDE-AY submission-ready declaration
```

---

## Termination criteria for Round L

- ✅ K-S1 red-team audit; all CRITICAL items either patched or escalated to Claude with rejection rationale
- ✅ K-S2 / K-S3 / K-S4 audits PASS (or any FAIL fixed)
- ✅ K-S5 cover letter polish landed
- ✅ K-S6 alternate abstract variant available for user
- ✅ K-S7 thesis chapter outline available for thesis fork
- ✅ K-S8 source-data README readable
- ✅ G-AA1–G-AA5 design briefs landed
- ✅ CX-EA Fig CORR_D2D landed + recompile clean
- ✅ CX-EB Zenodo archive packaged
- ✅ CX-EC pre-flight PASS
- ⛔ CX-ED gated on user metadata
- ✅ CLAUDE-AV/AW/AX/AZ self-tasks done

---

## Deferred to Round M (post-submission)

- Joint MLP-Linear + Ensemble HAT training execution (after G-AA3 spec approval)
- ImageNet pilot kickoff (after G-AA2 scoping approval + GPU window)
- Full CrossSim 10000-image re-run (resource-permitting)
- Thesis chapter drafting (after K-S7 outline approval)
- Press / outreach materials finalization

---

**End of Round L broadcast.** Three parallel tracks (red team / archive hardening / thesis fork). Kimi 8 tasks, Gemini 5 design briefs, Codex 4 (3 active + 1 gated). Single user form unblocks the final-bundle path. After Round L closes we are submission-ready pending only metadata.
