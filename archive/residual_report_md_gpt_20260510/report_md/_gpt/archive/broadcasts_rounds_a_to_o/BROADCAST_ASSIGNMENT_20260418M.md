> Canonical coordination: `AGENT_SYNC_gpt.md` | Task ledger: `CLAUDE_TASK_gpt.md`

# Round M Broadcast — 2026-04-19 10:50 (post-Round-L; rebuttal arsenal + thesis fork ignition + housekeeping)

**Author:** Claude (Chief Architect)
**Trigger:** Round L closed. Red-team audit (`KIMI_RED_TEAM_AUDIT_20260419.md`) verdict = *send out, not desk-reject*; sole CRITICAL is user metadata (out of our hands). Codex pre-flight PASS (`CODEX_PREFLIGHT_20260420.md`); supp now 23 pp after Fig CORR_D2D integration; Zenodo archive built; locked-numbers 16/16. GPU is fully idle (Codex confirmed all training quiesced).
**Quota policy:** Kimi ✅ heavy · Gemini 🟡 medium · Codex 🟢 medium (now that GPU is free we can spend a small Codex budget on a pilot run + housekeeping edits).
**Round M theme:** Stop polishing the submitted artifact (it's done). Pivot the spare bandwidth into three forward-looking workstreams:

1. **Rebuttal arsenal pre-loading** — anticipate the editor/reviewer counter-questions that *will* come, prepare answers before the clock starts.
2. **Submission-completeness housekeeping** — Nature Communications-aligned author contributions / data availability / code availability / ethics statements, plus the SHOULD-FIX items from the red-team audit.
3. **Thesis fork ignition** — actually start the joint-training pilot (G-AA3 spec) on the now-idle GPU, and seed the first thesis chapter from K-S7 outline.

---

## State on disk (pinned)

| Item | State |
|:--|:--|
| Bundle PDFs | main 17pp · supp **23pp** · cover 2pp ✅ |
| Locked numbers | 16/16 PASS ✅ |
| Pre-flight | PASS ✅ (`CODEX_PREFLIGHT_20260420.md`) |
| Zenodo archive | built at `release_artifacts/zenodo_archive_v0/` ✅ |
| Red-team verdict | send out, 1 CRITICAL = user metadata only ✅ |
| GPU | idle, no live training/eval workers ✅ |
| User metadata form | drafted at `USER_METADATA_REQUEST_20260420.md` ⛔ awaiting fill |

---

## KIMI — Round M (HEAVIEST; 8 tasks across 3 tracks)

### 🟡 Track A: Submission-completeness housekeeping (NC-aligned)

| ID | Item | Deliverable | Spec |
|:--|:--|:--|:--|
| **K-T1** | **SHOULD-FIX patch SF-1**: page-count normalization | edits across `paper/latex_gpt/` + `outputs/submission_bundle_20260419/README_SUBMISSION.txt` + cover letter if relevant | grep for any text mentioning "22 pages" / "22 pp" / "22-page" referring to supplementary; replace with `23 pages` to match `CODEX_PREFLIGHT_20260420.md`. Recompile clean. |
| **K-T2** | **SHOULD-FIX patch SF-2**: Zenodo archive mention | edit to `outputs/submission_bundle_20260419/README_SUBMISSION.txt` + `paper/latex_gpt/sections/04_data_code_availability.tex` (or wherever Data/Code Availability lives) | One sentence: *"A reproducibility archive (code snapshot + source data + SHA-256 manifest + CITATION.cff) is staged at `release_artifacts/zenodo_archive_v0/` and will be deposited to Zenodo with a DOI assigned at acceptance."* |
| **K-T3** | **CRediT Author Contributions statement** | new `KIMI_CREDIT_STATEMENT_DRAFT_20260420.md` | Draft a CRediT-format author contributions paragraph using placeholder roles (Conceptualization, Methodology, Software, Validation, etc.) with empty author initials. User will fill in initials. Land in `paper/latex_gpt/` after user input. |
| **K-T4** | **Data Availability + Code Availability statements** | `KIMI_DATA_CODE_AVAIL_DRAFT_20260420.md` + edits to `paper/latex_gpt/` | Draft NC-style statements: (a) data: which datasets, where, license, generated source data location; (b) code: GitHub URL placeholder, license (MIT/Apache?), Zenodo DOI placeholder. Insert into manuscript per NC submission template. |

### 🟢 Track B: Rebuttal arsenal pre-loading

| ID | Item | Deliverable | Spec |
|:--|:--|:--|:--|
| **K-T5** | **Top-10 anticipated reviewer objections** + canned responses | `KIMI_REBUTTAL_ARSENAL_V1_20260420.md` (≤4 pages) | Beyond the 5 we've already seen externally, anticipate what NC peer review will ask. For each objection list: (a) the objection in reviewer voice; (b) where in current source we already address it (or "currently unaddressed"); (c) a 3-sentence ready-to-fire response; (d) whether it would require a new experiment to fully resolve and which one. Cover at minimum: heavy-tailed conductance, IR drop, temperature drift, ADC choice rationale (6-bit), ensemble-frequency selection, attention-head specialization, NL gradient scaling justification, why CIFAR-10 over CIFAR-100 as headline, retention beyond 79%, and statistical-power objections to n=10 fresh instances. |

### 🟢 Track C: Thesis fork ignition

| ID | Item | Deliverable | Spec |
|:--|:--|:--|:--|
| **K-T6** | **Thesis Chapter 1 actual draft** (HAT + instance overfitting) | `paper/thesis/chapter_1_hat_instance_overfitting.tex` (≤25 pages LaTeX skeleton with prose for §1, §2; bullet outlines for §3–§5) | Convert K-S7 outline into an actual LaTeX skeleton. §1 introduction prose + §2 the 10.00% collapse story (with figure ref) + §3–§5 outline-only. Reuse manuscript figures by `\includegraphics` reference, do not duplicate. |
| **K-T7** | **NC Submission Checklist verification** | `KIMI_NC_SUBMISSION_CHECKLIST_20260420.md` | Walk the live Nature Communications submission checklist (article type, abstract length, main-text word count, figure count, supplementary policy, declarations required, ORCID, etc.). For each line, mark PASS / FAIL / N/A with evidence file. Catch anything we'd have to fix at submission portal time. |
| **K-T8** | **Reviewer-suggester prep brief** | `KIMI_REVIEWER_SUGGESTER_BRIEF_20260420.md` (≤200 words) | Help the user pick 5 suggested reviewers: list 3–5 *types of expertise* needed (organic-RRAM device physicist, ViT-quantization expert, CIM hardware-aware-training expert, simulation-framework methodologist, edge-AI systems person), with example venues (IEDM, ISSCC, NeurIPS-Hardware, ACM TODAES, etc.) where such people publish. Do NOT propose specific names. |

**Kimi NOT doing this round:** any GPU work; any new red-team passes (Round L did one).

---

## GEMINI — Round M (medium; 5 stateless design briefs)

### 🟢 Track B: Forward-looking experimental specs (rebuttal-defensive)

| ID | Item | Deliverable | Spec |
|:--|:--|:--|:--|
| **G-BB1** | **Heavy-tailed conductance distribution stress-test spec** | `GEMINI_HEAVY_TAILED_SPEC_20260420.md` (≤500 words) | Reviewer-anticipated: §6.5 already disclaims heavy tails; spec out the experiment that would actually answer it. Choices: (a) distribution family (log-normal vs t-distribution vs Pareto-truncated); (b) tail-index sweep range; (c) mapping from organic-RRAM literature (cite which papers report tail behavior); (d) compute budget; (e) success criterion (does Ensemble HAT still preserve ranking under 5% heavy-tail probability?). |
| **G-BB2** | **IR-drop preliminary modeling spec** | `GEMINI_IR_DROP_SPEC_20260420.md` (≤500 words) | §6.6 defers a "circuit-aware layer that models spatial IR drop". Spec the minimal-effort version: (a) array geometry (16×16 tile? 32×32?); (b) conductance-load assumption; (c) wire-resistance from organic-array literature; (d) coupling into existing fresh-instance harness; (e) compute estimate. Goal: show we *can* implement it during rebuttal if asked. |
| **G-BB3** | **Per-batch vs per-epoch HAT visualization design** | `GEMINI_PER_BATCH_VIZ_SPEC_20260420.md` (≤300 words) | K-Q9 disclosed per-batch HAT = 86.16% vs paper-locked 86.37% (ours = per-epoch). Reviewers will ask "why epoch?" — we need a figure that visualizes the variance/wallclock/accuracy trade-off across cadences. ASCII sketch + matplotlib parameter list for Codex to execute later if requested. |

### 🟡 Track A: Submission-completeness

| ID | Item | Deliverable | Spec |
|:--|:--|:--|:--|
| **G-BB4** | **Ethics + reproducibility statement design** | `GEMINI_ETHICS_REPRO_DRAFT_20260420.md` (≤300 words) | Draft NC-aligned: (a) ethics statement (no human/animal subjects, no dual-use concern); (b) reproducibility statement covering: deterministic seeds disclosed, hardware specs disclosed, software versions, hyperparameter table location, source-data extraction instructions. |

### 🟢 Track C: Thesis fork strategic decision

| ID | Item | Deliverable | Spec |
|:--|:--|:--|:--|
| **G-BB5** | **GPU-window strategy: joint training vs ImageNet pilot** | `GEMINI_GPU_STRATEGY_BRIEF_20260420.md` (≤300 words) | GPU is idle. Two candidates compete for first window: (i) G-AA3 joint MLP-Linear + Ensemble HAT (thesis punchline, ~60 GPU-h); (ii) G-AA2 ImageNet-100 pilot (cover-letter-promised, ~120 GPU-h). Recommend a sequencing with rationale. Consider: (a) which yields a stronger rebuttal artifact if reviewers come back fast; (b) which has higher technical risk; (c) which is more compute-efficient as a first-pilot. |

**Gemini NOT doing this round:** any source-tex edits, any GPU execution, any bundle work.

---

## CODEX — Round M (MEDIUM quota; GPU idle window enables a pilot + housekeeping)

| ID | Item | Type | Priority | Gate |
|:--|:--|:--|:--:|:--|
| **CX-FA** | **Joint MLP-Linear + Ensemble HAT pilot smoke** | GPU | MED | After G-AA3 spec re-read + G-BB5 sequencing brief lands. **Pilot only**: 3 epochs, single config, just to verify the loss/optimizer wiring runs and doesn't NaN. Output: `report_md/_gpt/json_gpt/joint_mlp_linear_ensemble_hat_smoke.json` + `CODEX_JOINT_TRAINING_SMOKE_20260420.md` (≤1 page). Do NOT launch full run; that's a Round-N decision. |
| **CX-FB** | **Land K-T1 + K-T2 housekeeping edits** if Kimi only drafts and doesn't land | tex | MED | After K-T1 + K-T2 deliverables exist. If Kimi already landed (verify), skip. If only drafts in `KIMI_*_DRAFT_*.md`, Codex applies the edits to `paper/latex_gpt/` + bundle README and recompiles. |
| **CX-FC** | **Heavy-tailed evaluator stub script** | code (no execution) | LOW | After G-BB1 spec lands. Write `scripts/_gpt/eval_heavy_tailed_d2d.py` as a STUB matching the existing fresh-instance harness signature, but with sampling fn TODO-marked. Do not run. Provides a "yes we are ready" proof point if reviewers ask. |
| **CX-FD** | **Final bundle rebuild** (CX-ED carry-over) | bundle | HIGH | TRIGGER: when user fills `USER_METADATA_REQUEST_20260420.md`. Insert metadata, recompile, refresh bundle, run `check_locked_numbers.py`, hand to CLAUDE-BD. |
| **CX-FE** | **Pre-flight v2** post-CX-FB landings | script | MED | After CX-FB. Re-run the `CODEX_PREFLIGHT_20260420.md` checks; produce `CODEX_PREFLIGHT_V2_20260420.md`. |

**Codex DEFERRED:** full joint-training run (Round N decision); ImageNet pilot (Round N decision); heavy-tailed full sweep (gated on stub + spec approval).

---

## CLAUDE self

| ID | Task |
|:--|:--|
| **CLAUDE-BA** | After K-T5: read rebuttal arsenal end-to-end, classify each anticipated objection as covered / partial / uncovered; flag any "uncovered" objection that would actually justify a Round-N experiment. |
| **CLAUDE-BB** | After G-BB5: make the GPU-window decision (joint-training pilot vs ImageNet pilot) and authorize CX-FA accordingly. |
| **CLAUDE-BC** | Compose `CLAUDE_USER_DECISION_REQUEST_20260420.md` consolidating: (i) metadata fill (existing form); (ii) joint-training-vs-ImageNet GPU-window choice; (iii) suggested-reviewer types from K-T8; (iv) GitHub repo URL + license decision for K-T4. One single ask, not five separate ones. |
| **CLAUDE-BD** | After CX-FD: final spot-check; declare submission-ready. |
| **CLAUDE-BE** | After CX-FA pilot smoke result: decide go/no-go on full joint training in Round N. |
| **CLAUDE-BF** | Audit K-T7 NC checklist; any FAIL becomes a CRITICAL Round-M-residual task. |

---

## USER (consolidated single ask via CLAUDE-BC)

The current `USER_METADATA_REQUEST_20260420.md` will be superseded by a single consolidated form covering:

- Acknowledgements text (funding/grant)
- Corresponding author + email + affiliation
- Suggested reviewers — **types** confirmed via K-T8 brief; user provides specific names
- GitHub repo URL + license choice (MIT / Apache-2 / BSD-3?)
- GPU-window decision: joint-training pilot first, OR ImageNet pilot first?
- CRediT author roles (initials per role from K-T3 template)

User can fill in one sitting (≤15 minutes).

---

## Execution pipeline

```
t0 (now):
  Kimi launches K-T1, K-T2, K-T3, K-T4, K-T5, K-T7, K-T8 in parallel (all independent)
  Kimi launches K-T6 in parallel (thesis chapter draft, longest)
  Gemini launches G-BB1, G-BB2, G-BB3, G-BB4, G-BB5 in parallel
  Claude starts CLAUDE-BC consolidated user form

t+1h:
  K-T1/T2 land → Codex CX-FB if needed
  G-BB5 in → Claude CLAUDE-BB GPU-window decision
  K-T5 in → Claude CLAUDE-BA arsenal classification
  K-T7 in → Claude CLAUDE-BF checklist audit

t+2h:
  Codex CX-FA joint-training pilot smoke (3 epochs)
  Codex CX-FE pre-flight v2
  Codex CX-FC heavy-tailed stub

t+3h (or after CX-FA):
  CX-FA result → Claude CLAUDE-BE Round-N go/no-go on full joint training
  K-T6 thesis chapter §1+§2 prose drafted

[gated on USER decision form]:
  Codex CX-FD final bundle rebuild
  Claude CLAUDE-BD submission-ready declaration
  Round N kickoff (full joint training OR ImageNet pilot, per user)
```

---

## Termination criteria for Round M

- ✅ K-T1, K-T2 housekeeping landed; supp page count, Zenodo mention consistent
- ✅ K-T3, K-T4 NC-aligned statements drafted (placeholders OK pending user)
- ✅ K-T5 rebuttal arsenal v1 — 10 anticipated objections covered; CLAUDE-BA classified
- ✅ K-T6 thesis Chapter 1 LaTeX skeleton with §1+§2 prose
- ✅ K-T7 NC checklist PASS or any FAIL fixed
- ✅ K-T8 reviewer-suggester brief available for user
- ✅ G-BB1–G-BB4 design briefs landed
- ✅ G-BB5 GPU-window sequencing decision made via CLAUDE-BB
- ✅ CX-FA joint-training pilot smoke completed (NaN-free)
- ✅ CX-FB housekeeping edits landed in source if needed; CX-FE pre-flight v2 PASS
- ✅ CX-FC heavy-tailed stub committed
- ✅ CLAUDE-BC consolidated user form composed
- ⛔ CX-FD final bundle gated on user metadata
- ⛔ Round N kickoff gated on user GPU-window decision

---

## Deferred to Round N (post-user-decision)

- Full joint MLP-Linear + Ensemble HAT training (per G-AA3 spec, after CX-FA smoke pass + user authorization)
- ImageNet-100 pilot kickoff (per G-AA2 spec, alternative or sequenced)
- Heavy-tailed D2D full sweep (per G-BB1 spec, post-stub validation)
- IR-drop preliminary modeling (per G-BB2 spec)
- Thesis Chapters 2–N drafting
- Per-batch HAT figure if reviewers actually ask (G-BB3 spec ready)

---

**End of Round M broadcast.** Three forward tracks: NC-housekeeping (Kimi A) · rebuttal pre-loading (Kimi B + Gemini B) · thesis ignition (Kimi C + Gemini C + Codex pilot). Kimi 8 · Gemini 5 · Codex 5 (1 GPU pilot + 4 housekeeping/staging). One consolidated user form unblocks both submission and Round N. Submission can ship the moment user metadata lands; everything else is positioning for what comes after.
