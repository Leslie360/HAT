> Canonical coordination: `AGENT_SYNC_gpt.md` | Task ledger: `CLAUDE_TASK_gpt.md`

# Round H Broadcast — 2026-04-18 23:55 / REVISED 2026-04-19 (quota reality: Kimi-only)

**Author:** Claude
**Revision trigger:** User "codex没额度了，Gemini也不够了，任务由kimi做" — Codex and Gemini quotas exhausted. All Round H work re-routed to Kimi. GPU experiments **paused** (no agent to execute them). Kimi re-instated as sole active executor (previous "dropped" status rescinded — they are now the only option).

**Prior state:** Round G closed ✅ (CX-W, CX-Y, CX-Z, G-R/S/T, CLAUDE-S/T/U/V/W). `attn_proj-only` halted ep54/100 (collapse confirmed). GPU idle 1%. Submission package functionally complete; remaining work is text/packaging/audit, which is a natural fit for Kimi.

---

## Round G audit (unchanged)

| Round-G ID | Claimed | On disk? | Verdict |
|:--|:--|:--|:--|
| CX-V | passive B1 monitor | ✅ | attn_proj stopped @ ep54, collapse confirmed |
| CX-W | dual-attention §6 patch draft | ✅ | `CX_W_DUAL_ATTN_COLLAPSE_PATCH_20260419.md` |
| CX-Y | `compute_vit/README.md` | ✅ | Created + placeholders removed |
| CX-Z | `compute_vit/LICENSE` | ✅ | Apache 2.0 verified |
| CX-X | `source_data_v1.zip` | ❌ | **carry over → Kimi K-O** |
| G-R | MLP fresh-instance gap | ✅ | Quantified 32.12±7.72% |
| G-S | attention collapse mechanism | ✅ | Math derivation delivered |
| G-T | data-release review | ✅ | Flagged missing Fig 3/6/7 JSONs |
| CLAUDE-S/T/U/V/W | Kimi absorption + rebuttal + G-M answer | ✅ | All 5 delivered |

**Compile state:** main 15pp / supp 21pp / cover 2pp, all clean.

---

## Quota-reality strategy shift

| Agent | Status | Assignable work |
|:--|:--|:--|
| **Codex** | ❌ no quota | GPU lanes frozen; tex edits frozen |
| **Gemini** | ❌ no quota | design/thesis work frozen |
| **Kimi** | ✅ sole executor | all remaining Round H work re-routed here |
| **Claude (self)** | ✅ | coordination + reviews + anything Kimi can't cover |

**Deferred indefinitely until quota returns:**
- CX-AB (all-linear fresh-instance eval) — GPU required
- CX-AC (MLP-Linear + Ensemble HAT joint training) — GPU required; this is the thesis-upgrade experiment and will wait
- Row (e) auto-finalize via `auto_finalize_nl_ablation.py` — Codex tooling; see H workaround below

**Workaround for CX-AA:** the attn_proj collapse data is a static fact on disk. Kimi can hand-edit `SUPP_TABLE_NL_ABLATION_SCAFFOLD.md`, `NL_LANE_RESULTS_20260418.md` (row already lists stopped@ep54), and `CLAUDE_A_DECISION_FINAL_20260418.md` row (e). No Python execution needed. Claude will review post-edit.

---

## Task dispatch — Kimi (all Round H work)

**Kimi note:** You are now the sole active executor. Work text-first, produce markdown/tex diffs as deliverables (don't run scripts). Claude will review and land any edits that need verification. **Before each task, re-read the canonical files** listed in the "Inputs" column — each task is self-contained.

| ID | Task | Priority | Inputs | Spec / Deliverable |
|:--|:--|:--:|:--|:--|
| **K-O1** | **Table SX.N row (e) hand-edit** (replaces CX-AA) | CRITICAL | `SUPP_TABLE_NL_ABLATION_SCAFFOLD.md`, `NL_LANE_RESULTS_20260418.md` row 18, `CLAUDE_A_DECISION_FINAL_20260418.md` | Produce a unified diff that fills row (e) = attn_proj-only with: best=18.86%@ep0, final≈10.25%, status="stopped at ep54 (timeout); trajectory collapsed from ep1". Deliver: `KIMI_TABLE_SXN_ROW_E_DIFF_20260419.md` with the diff + 1-line justification. Do NOT apply; Claude will apply. |
| **K-O2** | **Reviewer rebuttal prose expansion** (replaces G-W) | HIGH | `REBUTTAL_READY_TABLE_20260419.md` (11 objections), main.tex, supplementary.tex | For each of the 11 objections in the rebuttal table, write the actual 2–3 sentence reviewer-facing response prose. Tone: calm, specific, citation-heavy. Deliver: `KIMI_REBUTTAL_PROSE_20260419.md`. |
| **K-O3** | **Bibliography last-pass** (absorbs CLAUDE-AB and the old K-N) | HIGH | `paper/latex_gpt/main.bib` | Spot-check 8 critical refs (DOI, year, journal, author list). Critical = any ref cited in abstract, contributions list, or §6 Discussion. Deliver: `KIMI_BIB_LAST_PASS_20260419.md` with per-ref pass/fail + suggested corrections. |
| **K-O4** | **Consistency sweep** (replaces CX-AE) | HIGH | main.tex, supplementary.tex, cover_letter.tex | Grep for: any "5 contributions" / "five contributions" stragglers; stale numbers not in the 16-locked list; MLP-only phrasing that overstates (should acknowledge the 32% fresh-instance gap); any "QKV" claim without matching "attn_proj" after CX-W patch. Deliver: `KIMI_CONSISTENCY_SWEEP_20260419.md` — pass/fail + line-number-referenced fix list. |
| **K-O5** | **Severe-NL thesis chapter scaffold** (replaces G-V) | MED | `GEMINI_MLP_FRESH_INSTANCE_GAP_20260419.md`, `GEMINI_ATTENTION_COLLAPSE_MECHANISM_20260419.md`, `CLAUDE_RESPONSE_G_M_OPEN_QUESTION_20260419.md` | ~8-page thesis sub-chapter outline integrating MLP gap + attention collapse math + diagnostic-vs-solution framing. Sections: (i) severe-NL as stress test, (ii) 5-lane ablation as decomposition, (iii) fresh-instance gap as unsolved hook, (iv) joint MLP-Linear + Ensemble HAT as the planned thesis experiment (deferred until GPU returns). Deliver: `KIMI_THESIS_SEVERE_NL_CHAPTER_20260419.md`. |
| **K-O6** | **Source-data v1 manifest draft** (replaces CX-AD, text-only) | MED | `GEMINI_DATA_RELEASE_REVIEW_20260419.md`, existing `source_data_v0_MANIFEST.md`, `data_releases/` listing | Draft the updated manifest text for v1: add entries for Fig 3/6/7 source JSONs + all NL-lane CSVs. Do NOT build the ZIP (no script execution). Deliver: `KIMI_SOURCE_DATA_V1_MANIFEST_DRAFT_20260419.md`. Claude will assemble the ZIP later. |
| **K-O7** | **Rebuttal-coverage audit** (replaces G-Y) | LOW | `REBUTTAL_READY_TABLE_20260419.md`, main.tex §6, supplementary | For each of the 11 objections, confirm the manuscript actually has supporting language. Flag any objection whose response relies on language that doesn't yet exist. Deliver: `KIMI_REBUTTAL_COVERAGE_AUDIT_20260419.md`. |

### Priority ordering for Kimi
1. **K-O1** (CRITICAL) — unblocks Table SX.N and closes B1
2. **K-O2 + K-O4** (HIGH) — submission-blocking text items
3. **K-O3** (HIGH) — long-standing bibliography debt
4. **K-O5 + K-O6** (MED) — thesis + packaging
5. **K-O7** (LOW) — audit layer

If Kimi can only deliver 3 items: **K-O1, K-O2, K-O4**. Everything else can slip without blocking submission.

---

## Claude self-tasks (quota-independent)

| ID | Task | Trigger |
|:--|:--|:--|
| **CLAUDE-Y** | Re-instate Kimi in AGENT_SYNC (rescind "dropped" status) | Immediate |
| **CLAUDE-AC** | Review K-O1 diff and hand-apply to the 3 files | After K-O1 |
| **CLAUDE-AD** | Review K-O2 rebuttal prose; polish in place | After K-O2 |
| **CLAUDE-AE** | Review K-O4 consistency sweep; hand-apply fixes | After K-O4 |
| **CLAUDE-AF** | Recompile main/supp/cover after any tex-affecting Kimi delivery + re-run check_locked_numbers.py | Each landing |

---

## GPU / thesis experiments — deferred

- **CX-AC (MLP-Linear + Ensemble HAT joint training)** remains the highest-value thesis experiment. Queued for whenever Codex or GPU access returns. G-R hypothesis (>80% fresh-instance) stays the target.
- **CX-AB (all-linear fresh-instance)** similarly queued.
- Until then, NL_LANE_RESULTS row "all-linear fresh-instance pending" stays pending; this is acknowledged in the thesis chapter draft (K-O5) as an open item.

---

## Termination criteria for Round H (revised)

Round H closes when:
- ✅ K-O1 landed (Table SX.N row (e) populated)
- ✅ K-O2 and K-O4 landed (rebuttal prose + consistency sweep)
- ✅ CLAUDE-Y done (Kimi re-instated)
- ≥1 of K-O3 / K-O5 / K-O6 / K-O7 delivered

GPU-dependent closure deferred to a future round when quota returns.

---

**End of revised broadcast.** Kimi: work down the priority list; log start per-task in `AGENT_SYNC_gpt.md`. Codex + Gemini: quota-frozen; do not pick up work this round.
