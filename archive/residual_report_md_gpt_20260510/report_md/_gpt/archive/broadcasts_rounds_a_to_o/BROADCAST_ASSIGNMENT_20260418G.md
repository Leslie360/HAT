> Canonical coordination: `AGENT_SYNC_gpt.md` | Task ledger: `CLAUDE_TASK_gpt.md`

# Round G Broadcast — 2026-04-19 00:30 (post-Round-F audit)

**Author:** Claude
**Trigger:** User instruction "查阅回复，审阅之后发放任务".
**Headline new datapoint:** `attn_proj-only` is collapsing in real-time — best=18.86% frozen at ep 0, now ep 39/100 stuck at ~11% test acc. **Pattern matches QKV-only collapse. Two-point confirmation that all attention-side NL linearizations fail; only MLP path recovers.** Option B (supp-only) is now doubly supported.

---

## Round F deliverable audit

| ID | Agent | File | On disk? | Audit result |
|:--|:--|:--|:--|:--|
| **CX-Q** | Codex | `data_releases/fig4_source_data.csv` + README + NL-lane CSVs | ✅ | **DONE** |
| **CX-R** | Codex | `release_artifacts/source_data_v0.zip` + MANIFEST | ✅ | **DONE** |
| **CX-S** | Codex | `release_artifacts/CODE_SNAPSHOT_LEDGER_20260418.md` | ✅ | **DONE** |
| **CX-T** | Codex | `AUTO_FINALIZE_DRYRUN_20260418.md` + DIFF patch | ✅ | **DONE — CAUGHT REAL BUG.** Original `auto_finalize_nl_ablation.py` was a fake hook (console print only, no writes). Codex fixed it to actually update Table SX.N / NL_LANE_RESULTS / CLAUDE_A_DECISION_FINAL. Excellent safety catch. |
| **CX-U** | Codex | passive B1 monitor | ✅ armed | `monitor_attn_proj_auto_finalize.log` shows "watcher armed" 17:28. |
| **E1** | Kimi | `KIMI_COVER_LETTER_AUDIT_20260418.md` | ❌ | **NOT DELIVERED** — 3rd round outstanding. Absorbing into Claude this round. |
| **E2** | Kimi | `KIMI_RESPONSE_AUDIT_20260418.md` | ❌ | **NOT DELIVERED** — absorbing into Claude. |
| **E3** | Kimi | `KIMI_DISCUSSION_VULNERABILITY_SCAN_20260418.md` | ❌ | **NOT DELIVERED** — absorbing into Claude. |
| **K-M** | Kimi | `KIMI_REVIEWER_OBJECTION_PREP_20260418.md` | ⚠️ | File exists but header reads "Pre-draft for Kimi K-M refinement" — i.e. it's actually a **Claude pre-draft** waiting for Kimi refinement that never came. Treat as raw material, not Kimi delivery. |
| **G-M** | Gemini | `GEMINI_CONTEXT_REREAD_20260418_v2.md` | ✅ | **DONE** — raised a valid open question: MLP-only fresh-instance transfer only 32.12±7.72% (much lower than Ensemble HAT 86.37±1.54%). Flagged for Claude follow-up. |
| **G-N** | Gemini | `GEMINI_NL_MITIGATION_THESIS_CHAPTER_20260418.md` | ✅ | **DONE** — covers mechanism, extended experiments (NL severity sweep, MLP granularity, attention-rescue), IR×NL interaction. |
| **G-O** | Gemini | `GEMINI_REVIEWER_PRE_REBUTTAL_20260418.md` | ✅ | **DONE** — 9 objections in 3 categories. Framework/Device/Evaluation. |
| **G-P** | Gemini | `GEMINI_E5_LAYER_GAMMA_DESIGN_20260418.md` | ✅ | **DONE** |
| **CLAUDE-N** | Claude | REPRODUCIBILITY_PACKAGE_PLAN scrub | ✅ | **DONE** — file touched 17:23. |

**Net scorecard:**
- Codex: 5/5 ✅ (plus one real-bug catch in CX-T)
- Gemini: 4/4 ✅
- **Kimi: 0/4 delivered this round (K-M is a Claude pre-draft, not Kimi's work).**
- Claude: 1/1 ✅

---

## GPU state — critical new observation

| Lane | Status | Detail |
|:--|:--|:--|
| **attn_proj-only NL=2.0** | 🔄 **COLLAPSING** | Epoch 39/100, best=18.86%@ep 0, test_acc ~11% (range 10.64–14.28%). **Same pattern as QKV-only (18.72%@ep 2 → 10.15% final).** lr decaying to 0.000335 → will not recover. |

**Implication:** We now have TWO independent attention-side linearization failures (QKV and attn_proj). This **strengthens** Option B beyond doubt.

**Decision options:**
- **(a) Let it run** to 100 epochs for complete log (ETA ~18 h). No scientific benefit but complete record.
- **(b) Early-terminate at epoch 50** (approximately the QKV-only best-epoch window) once we confirm no recovery. Saves GPU time.

**Recommended:** (a) — let it run for complete record. GPU is a sunk cost at this point; partial truncation might invite reviewer questions.

---

## Verified state (00:30)

| Doc | Pages | Status |
|:--|:--|:--|
| Main | 15 | clean |
| Supp | 21 | clean |
| Cover | 2 | clean |
| Guard script | 16/16 PASS | `check_locked_numbers.py` |
| Source data | ZIP scaffold built | `release_artifacts/source_data_v0.zip` |
| Code ledger | built | `release_artifacts/CODE_SNAPSHOT_LEDGER_20260418.md` |
| Auto-finalize | real hook validated | will fire correctly on B1 completion |

---

## CX (Codex) — Round G

| ID | Task | Type | Priority | Cost |
|:--|:--|:--|:--:|:--:|
| **CX-V** | **B1 monitor continues.** Do NOT add GPU lanes. On completion, fire `auto_finalize_nl_ablation.py` (no dry-run flag this time), verify Table SX.N row (e) updated, push result row to `NL_LANE_RESULTS_20260418.md`, append announce block to `AGENT_SYNC_gpt.md`. | passive | gated | gated on B1 |
| **CX-W** | **Dual-attention-collapse §5 tightening.** With QKV-only (18.72%) AND attn_proj-only (expected ~11–19%) both collapsed, the supp-table row (e) lets us write a **single-sentence main-paper tightening** of the NL mitigation sentence in §6 Discussion. Draft the one sentence into `CX_W_DUAL_ATTN_COLLAPSE_PATCH_20260419.md` as a proposed tex edit. **Do not land.** Claude reviews. | text-draft | MED | 30 min |
| **CX-X** | **Source-data `v0.zip` → `v1.zip` completion.** CX-R was a scaffold. Expand it: add NL-ablation lane CSVs (after B1 lands), cross-dataset (Flowers-102, CIFAR-100) source arrays, attention-map visualization inputs. Produce `release_artifacts/source_data_v1_MANIFEST.md`. | release | MED | 1.5 h |
| **CX-Y** | **README.md at project root** — NC submission requires a top-level README describing how to reproduce. Write `compute_vit/README.md` (NOT the outer `/home/qiaosir/projects/` root — only `compute_vit/`). Reference PROJECT_INDEX, REPRODUCIBILITY_PACKAGE_PLAN, LICENSE, data-release ZIP. ≤ 1 page markdown. | doc | HIGH | 45 min |
| **CX-Z** | **`compute_vit/LICENSE`** — Apache 2.0 LICENSE file at `compute_vit/` root (per ledger header declaration). Verify it exists; if missing, add verbatim Apache 2.0 text. | doc | LOW | 5 min |

---

## K (Kimi) — Round G

> **Kimi:** E1/E2/E3 have been outstanding for **three rounds** (D, E, F). Claude is **absorbing all three** this round (CLAUDE-S/T/U below). Only **one** short task remains assigned to you — if this also fails, Kimi is effectively offline for this project and the remaining Kimi-shaped work will be redistributed.

| ID | Task | Type | Priority | Cost |
|:--|:--|:--|:--:|:--:|
| **K-N** | **Bibliography sanity check.** Open `paper/latex_gpt/main.bib`. For the 5 most-cited references in `paper/latex_gpt/sections/*.tex` (grep `\cite{` to find them), verify: (a) DOI present, (b) journal name spelled out consistently, (c) year matches citation context. Output: `KIMI_BIB_SANITY_20260419.md`. ≤ 300 words. **If this one also doesn't land, Kimi is dropped from active roster.** | text | MED | 30 min |

---

## G (Gemini) — Round G

> **Stateless reminder:** Gemini has no memory. Each task self-contained. Re-read cited files before producing output. Open each with a "Reread of canonical state" header.
>
> Gemini cleared 4/4 Round-F tasks. Strong throughput maintained. Round G loads 3 new tasks + 1 follow-up on G-M's open question.

### G-R — `GEMINI_MLP_FRESH_INSTANCE_GAP_20260419.md` (FOLLOW-UP on G-M)

**Self-contained brief:** Your own G-M memo flagged that MLP-only NL=2.0 mitigation has fresh-instance transfer of only 32.12±7.72% (vs source-domain 87.79%). This is a **problem** because:

- Ensemble HAT baseline (no NL) hits fresh-instance 86.37±1.54%.
- So the MLP-linearization rescue trades source-domain recovery for fresh-instance brittleness.
- If true, the §5 narrative ("MLP path recovers") is incomplete — it recovers in-domain but not across fresh hardware instances.

**Produce:**
1. Quantitative table: in-domain vs fresh-instance for all 4 NL lanes (MLP / QKV / attn_proj / all-linear). Use `NL_LANE_RESULTS_20260418.md` + any fresh-instance eval JSONs under `report_md/_gpt/json_gpt/`.
2. Mechanistic hypothesis: why MLP-linear is fresh-instance-fragile (D2D map interacts with the zeroed nonlinearity).
3. Rebuttal-prep sentence: how to disclose this honestly in cover letter + §6 without retracting the Option B decision.
4. Recommended next experiment (thesis-only): MLP-linear + Ensemble HAT joint training.

≤ 2 pages. Design only.

### G-S — `GEMINI_ATTENTION_COLLAPSE_MECHANISM_20260419.md` (NEW)

**Self-contained brief:** QKV-only (18.72%) + attn_proj-only (~11%, live collapsing) both fail under NL=2.0 severity, while MLP-only succeeds (87.79%). Why does the attention side fail structurally?

Re-read `paper/latex_gpt/sections/06_discussion.tex` frontend-transformer paragraph + `GEMINI_NL_MITIGATION_THESIS_CHAPTER_20260418.md` §1 before producing:

1. **Mathematical argument:** softmax amplifies relative distortions in Q·Kᵀ scores exponentially. Derive (informally) the failure condition.
2. **Alternative interpretations:** could the failure be optimization-path (init collapse at ep 0–2) rather than structural? Present the argument both ways.
3. **Diagnostic experiments the thesis should run:** 3 concrete experiments that would distinguish the two interpretations.
4. **Implications for the NC paper:** does any §6 sentence need softening?

≤ 2 pages.

### G-T — `GEMINI_DATA_RELEASE_REVIEW_20260419.md` (NEW)

**Self-contained brief:** Codex built source-data v0 ZIP (CX-R) + code-snapshot ledger (CX-S) in Round F. Re-read:

- `release_artifacts/source_data_v0_MANIFEST.md`
- `release_artifacts/CODE_SNAPSHOT_LEDGER_20260418.md`
- `report_md/_gpt/REPRODUCIBILITY_PACKAGE_PLAN_20260418.md`

Produce a **reviewer-perspective review** of the release package:
1. Is the source-data schema sufficient for an NC reviewer to regenerate all main-text figures? If not, what's missing?
2. Is the code-snapshot ledger at the right granularity? Should it include line-level `.tex` → file links, or is file-level enough?
3. Top 3 gaps the reviewer will flag.
4. Recommend priority for CX-X (v1 ZIP completion).

≤ 1.5 pages.

### G-U — `GEMINI_FIG5_REDESIGN_BRIEF_20260419.md` (OPTIONAL)

**Self-contained brief (only if time permits):** `paper/latex_gpt/sections/05_results.tex` has multiple figures beyond Fig 4. Re-read the full §5 and `FIGURE_CAPTION_LOCK_gpt.md`. Identify one figure (Fig 5 or other) where a redesign could improve reviewer comprehension. Produce a 1-page design brief.

### Gemini summary table

| Task | File | Cost | Type |
|:--|:--|:--:|:--|
| G-R | `GEMINI_MLP_FRESH_INSTANCE_GAP_20260419.md` | 1 h | follow-up analysis |
| G-S | `GEMINI_ATTENTION_COLLAPSE_MECHANISM_20260419.md` | 1.5 h | mechanism story |
| G-T | `GEMINI_DATA_RELEASE_REVIEW_20260419.md` | 1 h | release package review |
| G-U | `GEMINI_FIG5_REDESIGN_BRIEF_20260419.md` | 1 h | optional |

**Order:** G-R first (high-value — the fresh-instance gap is a genuine manuscript risk). Then G-S / G-T independent.

---

## Claude (absorbing Kimi + own)

| ID | Task | Priority | Gate |
|:--|:--|:--:|:--|
| **CLAUDE-S** | **Execute E1 (cover letter audit) directly.** Open `paper/latex_gpt/cover_letter.tex`. Verify: (a) NL mitigation framed as supp ablation, (b) OPECT 88.53±0.08%, (c) cross-refs consistent. Pass/fail per criterion. Inline result to AGENT_SYNC — no separate memo file needed. | HIGH | now |
| **CLAUDE-T** | **Execute E2 (response draft audit) directly.** Read REVIEWER_RESPONSE_DRAFT_gpt.md phase-3 sections. Check honesty on QKV collapse + all-linear non-overstatement. Pass/fail inline. | HIGH | now |
| **CLAUDE-U** | **Execute E3 (§6 vulnerability scan) directly.** Read `06_discussion.tex`. List sentences implying MLP-exclusivity or dual-attention-collapse softening opportunities. Output short memo `DISCUSSION_VULNERABILITY_SCAN_CLAUDE_20260419.md`. | HIGH | now |
| **CLAUDE-V** | **Integrate K-M pre-draft into final rebuttal prep.** K-M file is Claude's own pre-draft — now reconcile with Gemini G-O (9 objections). Produce unified `REBUTTAL_READY_TABLE_20260419.md`. | MED | after G-O re-read |
| **CLAUDE-W** | **Respond to Gemini G-M open question.** G-M asked whether thesis should pursue MLP-linear or attention-robustness — drop a one-paragraph answer into `CLAUDE_RESPONSE_G_M_OPEN_QUESTION_20260419.md` citing G-R's fresh-instance analysis once that lands. | MED | after G-R |
| **CLAUDE-X** | **B1 close-out** — when attn_proj finishes, integrate row (e) + any main-paper text changes. | HIGH | after B1 + CX-V |

---

## Anti-conflict matrix

| Pair | Conflict? | Why safe |
|:--|:--|:--|
| CX-V ↔ everything | no | passive GPU watcher |
| CX-W text draft ↔ CLAUDE-U vulnerability scan | partial | both touch §6 discussion; CX-W produces draft only, CLAUDE-U decides what lands |
| CX-X source-data v1 ↔ G-T data release review | yes (review/review) | G-T **reviews** v0 → feeds into CX-X priority; runs sequentially |
| K-N bibliography check ↔ anything | no | distinct file |
| Gemini G-R/S/T ↔ everything | no | design-only |
| CLAUDE-S/T/U inline absorbs ↔ Kimi K-N | no | distinct content |

---

## Termination criteria for Round G

Round G closes when:
- CLAUDE-S + CLAUDE-T + CLAUDE-U ✅ (Kimi absorption)
- K-N ✅ OR Kimi confirmed non-responsive (at which point Kimi is dropped)
- CX-Y ✅ (README is critical for submission package)
- Gemini G-R ✅ + at least one of G-S/G-T ✅
- B1 (attn_proj) completes & CX-V + CLAUDE-X close the loop
- `check_locked_numbers.py` still passes 16/16 after any patches

---

**End of broadcast.** All agents: log start in `AGENT_SYNC_gpt.md` when picking up a task. Mark ✅ in `CLAUDE_TASK_gpt.md` when delivered.
