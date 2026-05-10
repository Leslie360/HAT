> Canonical coordination: `AGENT_SYNC_gpt.md` | Task ledger: `CLAUDE_TASK_gpt.md`

# Round F Broadcast — 2026-04-18 23:50 (post-Round-E)

**Author:** Claude
**Trigger:** User instruction "查看广播，继续发布任务".
**Round-E status:** Codex landings audited (CX-J/K/L/M/N/O all ✅), Round E broadcast file (`BROADCAST_ASSIGNMENT_20260418E.md`) and ledger entries are aligned. Round F adds new work for the agents whose throughput slot is open.
**Hard rules carry over:** Codex GPU lanes priority, no new GPU lanes until attn_proj-only drains.

---

## Round D/E deliverable verification (one more pass)

| ID | Agent | File | On disk? | Verdict |
|:--|:--|:--|:--|:--|
| G-I | Gemini | `GEMINI_E1B_LANDING_PLAN_20260418.md` | ✅ | **DONE** — was ⏳ in ledger; mark ✅ this round. |
| G-J | Gemini | `GEMINI_P1_P2_P5_INTEGRATION_20260418.md` | ✅ | **DONE** — was ⏳; mark ✅. |
| G-K | Gemini | `GEMINI_THESIS_OUTLINE_DRAFT_20260418.md` | ✅ | **DONE** — was ⏳; mark ✅. |
| G-L | Gemini | `GEMINI_FIG4_REDESIGN_BRIEF_20260418.md` | ✅ | **DONE** — was ⏳; mark ✅. |
| E1 / E2 / E3 | Kimi | `KIMI_COVER_LETTER_AUDIT` / `KIMI_RESPONSE_AUDIT` / `KIMI_DISCUSSION_VULNERABILITY_SCAN` | ❌ | Still **NOT FOUND** — re-emphasize this round. |
| E4 | Codex | Fig 4 source-data CSV + README | not yet | Still ⏳. |
| E5 | Claude | REPRODUCIBILITY_PACKAGE_PLAN scrub | not yet | Still ⏳ — Claude self-task. |

**Net:** Gemini cleared 4/4 Round-D backlog. Kimi 0/3 outstanding. Codex GPU-blocked on B1.

---

## Verified state at dispatch (23:50)

| Lane | Status | Headline |
|:--|:--|:--|
| MLP / QKV / all-linear NL=2.0 | ✅ FINISHED | locked into `CLAUDE_A_DECISION_FINAL` |
| attn_proj-only NL=2.0 | 🔄 RUNNING | startup logs only at last check; auto-finalize hook armed |
| Manuscript | 15/21/2 pp | clean compile |
| Locked-numbers guard | 16/16 PASS | `check_locked_numbers.py` |

---

## CX (Codex) — Round F

| ID | Task | Type | Priority | Cost |
|:--|:--|:--|:--:|:--:|
| **CX-Q** | **Execute E4 (Fig 4 source-data prep)** — produce `report_md/_gpt/data_releases/fig4_source_data.csv` + `fig4_source_data_README.md`. Columns: experiment_id, architecture, dataset, condition, MC_seed, accuracy, error_bar (or `null` for deterministic cells). README explains schema + cell-by-cell provenance. **No figure / `.tex` edits.** | tooling | MED | 1 h |
| **CX-R** | **Source-data ZIP scaffold** — extend CX-Q. Produce `release_artifacts/source_data_v0.zip` containing: fig4 CSV + README, locked-numbers JSON snapshots from `report_md/_gpt/json_gpt/`, NL ablation lane CSVs from CSV exports of `NL_LANE_RESULTS_20260418.md`. Manifest = `release_artifacts/source_data_v0_MANIFEST.md`. NC requires source data per figure; this is the scaffold. | release | MED | 1 h |
| **CX-S** | **Code snapshot ledger** — `release_artifacts/CODE_SNAPSHOT_LEDGER_20260418.md`: list every file in `compute_vit/` that the manuscript references (scripts, configs, profile JSONs). For each, cite the `.tex` line that uses it. This is the predecessor to a reviewer-facing code archive. **Read-only, no archive build yet.** | release | MED | 1 h |
| **CX-T** | **Auto-finalize hook health-check** — verify `auto_finalize_nl_ablation.py` (or whichever script Codex wired up) actually triggers on attn_proj-only completion: dry-run on a synthetic completion event, log expected outputs (Table SX.N row, NL_LANE_RESULTS row, SUPP_TABLE_NL_ABLATION_SCAFFOLD row). Output `AUTO_FINALIZE_DRYRUN_20260418.md`. | safety | HIGH | 30 min |
| **CX-U** | **Passive: B1 monitor** — watch attn_proj-only; on completion, fire auto-finalize, then announce in `AGENT_SYNC_gpt.md`. | passive | — | gated on GPU |

Codex priority order: CX-T (safety) → CX-Q → CX-S → CX-R → CX-U.

---

## K (Kimi) — Round F (re-push of unfinished Round-E)

> **Kimi:** Round E E1/E2/E3 are still outstanding. These are short audit memos, not new analysis — the manuscript and cover letter already exist on disk; you only need to read and pass/fail them. **Each audit ≤ 400 words.**

| ID | Task | Type | Priority | Cost |
|:--|:--|:--|:--:|:--:|
| **E1 (re-push)** | **Cover letter v2 light-touch audit.** Read `paper/latex_gpt/cover_letter.tex`. Confirm: (a) NL mitigation framed as supplementary ablation (NOT 5th main contribution), (b) OPECT zero-shot cited as `88.53±0.08%` (not bare 88.53%), (c) cross-ref to Supp Table SX.N is consistent. Output: `KIMI_COVER_LETTER_AUDIT_20260418.md` — pass/fail per criterion + ≤2 redline suggestions if needed. | text | HIGH | 30 min |
| **E2 (re-push)** | **Response draft light-touch audit.** Read `report_md/_gpt/REVIEWER_RESPONSE_DRAFT_gpt.md` "Group-wise NL Mitigation Ablation" + "Learnable Inverse-Gamma Compensation" sections (added by Codex Phase 3). Confirm: (a) Table SX.N cited correctly, (b) all-linear 87.49% NOT overclaimed as success of QKV path, (c) QKV-only collapse honestly disclosed in the same paragraph. Output: `KIMI_RESPONSE_AUDIT_20260418.md` — pass/fail + ≤2 redline suggestions. | audit | HIGH | 30 min |
| **E3 (re-push)** | **§6 Discussion vulnerability scan v2.** Read `paper/latex_gpt/sections/06_discussion.tex`. List any sentence still implying "MLP-only" exclusivity that should now read "MLP and full-linear paths both recover, while QKV-only collapses." Honest disclosure of QKV failure must remain. Output: `KIMI_DISCUSSION_VULNERABILITY_SCAN_20260418.md` — bullet list, no `.tex` edits. | analysis | HIGH | 45 min |
| **K-M (NEW)** | **Reviewer-objection prep — top 5.** Given the locked manuscript (15pp main, 21pp supp), what are the top 5 reviewer objections still likely? For each: objection / strongest counter-evidence already in manuscript / residual exposure / mitigation if reviewer pushes. Output: `KIMI_REVIEWER_OBJECTION_PREP_20260418.md`, ≤ 1 page. | strategy | MED | 1 h |

---

## G (Gemini) — Round F

> **Stateless-agent reminder:** Gemini has no memory of prior conversation. Each task below is self-contained and re-cites canonical files. Re-read the cited files in full before producing output. Each output should re-state working assumptions in a "Reread of canonical state" header.
>
> **Gemini cleared all 4 Round-D backlog tasks (G-I/J/K/L) — strong throughput, slot is open.** Round F adds 4 new design/research tasks. **Pick them up one at a time, one file per task.** No bundling.

### G-M — `GEMINI_CONTEXT_REREAD_20260418_v2.md` (mandatory first)

Re-read these files in full **before any new work**:
1. `report_md/_gpt/CLAUDE_A_DECISION_FINAL_20260418.md` (Option B locked, NL mitigation = supp only)
2. `report_md/_gpt/PRE_SUBMISSION_CHECKLIST.md` (R1–R4 status)
3. `report_md/_gpt/R1_R4_LANDING_AUDIT_20260418.md` (what was actually patched)
4. `report_md/_gpt/NL_LANE_RESULTS_20260418.md` (the four NL=2.0 mitigation lanes)

Output: 200-word self-summary covering (a) what Option B means for §6 and §7, (b) what's still pending (B1, B2, D13), (c) one open question Gemini wants Claude to clarify. This refreshes the stateless-agent context and gives the team a checkpoint.

### G-N — `GEMINI_NL_MITIGATION_THESIS_CHAPTER_20260418.md` (NEW)

**Self-contained brief:** With NL mitigation locked as supp-only in the NC paper, the **thesis** can give it a full chapter. Re-read `NL_LANE_RESULTS_20260418.md` + `CLAUDE_A_DECISION_FINAL_20260418.md` before producing:

1. **Chapter scope** — full mechanistic story of NL=2.0 mitigation: why MLP path recovers (87.79%), why QKV path collapses (18.72%), why all-linear (87.49%) ≈ MLP-only. Cite attention-noise literature.
2. **Extended experiments not in NC paper** — propose 3 thesis-only experiments: (a) NL severity sweep (1.5/1.7/2.0/2.5), (b) MLP-linearization granularity (which sub-MLP layers matter most), (c) attention-rescue strategies (low-rank, structured noise, etc.).
3. **Tie-back to circuit-aware (G-J integration)** — does NL=2.0 mitigation interact with IR drop / thermal / sneak path?
4. **Estimated cost** — wall-clock + GPU-hours.

Design only. No code. ~3 pages markdown.

### G-O — `GEMINI_REVIEWER_PRE_REBUTTAL_20260418.md` (NEW)

**Self-contained brief:** Re-read `paper/latex_gpt/main.pdf` (or `paper/latex_gpt/sections/00_abstract..07_conclusion.tex`) and `cover_letter.tex` in full. Produce a **pre-rebuttal anticipation memo** that complements Kimi's K-M (reviewer objection prep — different angle, design-side rather than text-side):

1. **Three "framework" objections** a reviewer might raise about the simulator architecture itself (not the results), e.g. "why fixed Gaussian C2C/D2D" / "why STE backward" / "why hybrid analog/digital split as drawn". Counter each with what the cover letter / methods already says.
2. **Three "device" objections** about the OPECT case study, e.g. "why these calibration constants" / "what about cycle endurance" / "what about T-dependence". Counter from manuscript or flag as future work.
3. **Three "evaluation" objections** — e.g. "why CIFAR-100 and not ImageNet" / "why three datasets" / "why best-checkpoint reporting". Counter or concede with work-around.

Output: 9 objections in 3 sections, 1 paragraph each. ≤ 2 pages.

### G-P — `GEMINI_E5_LAYER_GAMMA_DESIGN_20260418.md` (NEW)

**Self-contained brief:** Codex previously offered "E5 layer-wise gamma sensitivity" as Option A in their broadcast. Produce a runnable design (not code):

1. **Goal** — for Tiny-ViT V4, identify which transformer block depths are most sensitive to γ_phys (the inverse-gamma frontend). Hypothesis: early patch-embedding-adjacent layers dominate.
2. **Experimental matrix** — 4 γ values × N transformer block depths × 1 architecture = grid.
3. **Required code modifications** — describe in pseudo-code what `analog_layers.py` needs to expose so per-block γ can be set.
4. **Estimated GPU-hours.**
5. **Decision criteria** — what result pattern would justify a follow-on supp section in the NC submission revision (vs thesis-only).

Design only. No code.

### G-Q — `GEMINI_E1B_LANDING_PLAN_REVIEW_20260418.md` (OPTIONAL — only if time permits)

If after G-M/N/O/P, Gemini still has bandwidth: **re-read** `GEMINI_E1B_LANDING_PLAN_20260418.md` (own prior delivery) + `GEMINI_E1B_EXECUTION_REFINEMENT_20260418.md`. Produce a **self-critique**: what's missing, what a smart reviewer would push back on, three concrete improvements.

### Gemini summary table

| Task | File | Cost | Type |
|:--|:--|:--:|:--|
| G-M | `GEMINI_CONTEXT_REREAD_20260418_v2.md` | 30 min | re-onboarding (mandatory first) |
| G-N | `GEMINI_NL_MITIGATION_THESIS_CHAPTER_20260418.md` | 1.5 h | thesis chapter |
| G-O | `GEMINI_REVIEWER_PRE_REBUTTAL_20260418.md` | 1.5 h | pre-rebuttal |
| G-P | `GEMINI_E5_LAYER_GAMMA_DESIGN_20260418.md` | 1 h | experiment design |
| G-Q | `GEMINI_E1B_LANDING_PLAN_REVIEW_20260418.md` | 45 min | self-critique (optional) |

**Order:** G-M first (mandatory). Then G-N / G-O / G-P independent — any order. G-Q only if bandwidth.

---

## Claude (own followups)

| ID | Task | Gate |
|:--|:--|:--|
| **CLAUDE-N** | Execute E5 (REPRODUCIBILITY_PACKAGE_PLAN scrub) — verify all paths + 数据_博士 / checkpoint references match current state. | now |
| **CLAUDE-O** | Read CX-T auto-finalize dry-run report when delivered; sign off or redirect. | after CX-T |
| **CLAUDE-P** | Read Kimi E1/E2/E3 audits and apply micro-patches to manuscript if needed. | after Kimi delivers |
| **CLAUDE-Q** | Read Gemini G-O pre-rebuttal; reconcile with K-M reviewer objection prep — produce single unified rebuttal-ready table. | after G-O + K-M |
| **CLAUDE-R** | When B1 (attn_proj) completes + CX-T verifies hook, integrate row (e) into all downstream tables. | after B1 + CX-T |

---

## Anti-conflict matrix

| Pair | Conflict? | Why safe |
|:--|:--|:--|
| CX-Q/R/S/T (Codex CPU work) ↔ attn_proj GPU | no | All CPU-only |
| CX-Q (fig4 CSV) ↔ G-L (Gemini Fig 4 redesign brief, already delivered) | no | CX-Q is data prep; G-L was design |
| Kimi E1/E2/E3 ↔ Codex CX-Q/R/S/T | no | Distinct files |
| Gemini G-M..Q ↔ everything | no | Design-only, all under `report_md/_gpt/` |
| K-M (Kimi reviewer objection) ↔ G-O (Gemini pre-rebuttal) | partial | Different angles by design (text vs framework); reconciled by CLAUDE-Q |

---

## Termination criteria

Round F closes when:
- Kimi E1 + E2 + E3 ✅ (the long-overdue audits)
- CX-T ✅ (auto-finalize verified before B1 fires)
- CX-Q + at least one of CX-R/S ✅
- Gemini G-M + at least 2 of G-N/O/P ✅
- B1 (attn_proj) eventually completes; CX-U auto-fires; B2 lands; CLAUDE-R closes loop

After Round F, the submission is in final-pass territory.

---

**End of broadcast.** All agents: log start in `AGENT_SYNC_gpt.md` when picking up a task. Mark ✅ in `CLAUDE_TASK_gpt.md` when delivered.
