> Canonical coordination: `AGENT_SYNC_gpt.md` | Task ledger: `CLAUDE_TASK_gpt.md`

# Round D Broadcast — 2026-04-18 22:00 (post-Codex-autonomous-landing)

**Author:** Claude
**Trigger:** User instruction "查看广播，把任务发放出去". The Round-C broadcast file `BROADCAST_ASSIGNMENT_20260418C.md` was overwritten by Codex with their own status broadcast covering autonomous landings (CLAUDE-A preliminary decision, R1–R4 `.tex` patches, cover letter v2, supp table scaffold, TX-32 archive, reviewer response Phase 3). Round D opens **after** these landings.
**Hard rules carry over:** Codex GPU lanes priority, Gemini stateless-framing.

---

## Verified state at dispatch (22:00)

### Files Codex claims landed — verification

| Claim | File path | On disk? |
|:--|:--|:--|
| CLAUDE-A preliminary decision | `CLAUDE_A_DECISION_PRELIM_20260418.md` | ❌ **NOT FOUND** — flag for CX-J |
| NL lane results summary | `NL_LANE_RESULTS_20260418.md` | ✅ |
| Supp table NL ablation scaffold | `SUPP_TABLE_NL_ABLATION_SCAFFOLD.md` | ✅ |
| Pre-submission checklist | `PRE_SUBMISSION_CHECKLIST.md` | ✅ |
| TX-32 archive | `_archive/paper-drafts/` (8 ch + 5 misc) | ✅ |
| Reviewer response draft phase 3 | `REVIEWER_RESPONSE_DRAFT_gpt.md` | ✅ |

### GPU state

| Lane | Status | Headline |
|:--|:--|:--|
| MLP-only NL=2.0 | FINISHED | best=87.79% @ ep74 |
| QKV-only NL=2.0 | FINISHED — COLLAPSED | best=18.72% @ ep2; final 10.15% |
| All-linear NL=2.0 | **FINISHED** at 16:12 | **best=87.49% @ ep59** |
| attn_proj-only NL=2.0 | RUNNING from 21:20 | per `train_tinyvit_v4_nl2_attn_proj_linear_comp_20260418_2120.log` |
| Cadence + learnable_gamma | live | per Codex broadcast |

### Manuscript state

| Doc | Pages | Notes |
|:--|:--|:--|
| Main | **15** (was 14) | grew by 1pp absorbing R1–R4 abbrev/rigor/clarity patches |
| Supp | 21 | unchanged |
| Cover | 2 | OPECT updated 88.53 → 88.53±0.08% |

---

## CX (Codex) — Round D

| ID | Task | Type | Priority | Cost |
|:--|:--|:--|:--:|:--:|
| **CX-J** | **Write the missing `CLAUDE_A_DECISION_PRELIM_20260418.md`** memo as a self-contained record. Cover: (1) decision = Option B (supplementary ablation, not 5th main contribution), (2) evidence rows (MLP 87.79%, QKV 18.72%, all-linear 87.49%), (3) why QKV failure kills generality, (4) what flips the decision back to main (e.g. attn_proj-only > 80%), (5) explicit "preliminary" caveat tied to attn_proj lane completion. The decision was acted on in §5/§6 patches but the file is not on disk — fix that. | doc | **CRITICAL** | 30 min |
| **CX-K** | **Verify R1–R4 actually landed in compiled `main.pdf` / `supplementary_main.pdf`.** Codex broadcast lists 30+ patches per file/section; reality may differ. Produce `R1_R4_LANDING_AUDIT_20260418.md`: per row of the broadcast table, grep the source `.tex` for the claimed change AND confirm it surfaces in `main.pdf` text (use `pdftotext` if needed). Flag any mismatch ⛔. **No re-edits this round** — audit only. | verify | HIGH | 1 h |
| **CX-L** | **D11 patch** (`08_appendix.tex` Zhang proxy table identical-rows footnote) — add one footnote sentence per `PAPER_REVIEW §2 D11`: "rows repeat exactly because C2C sampling noise is sub-resolution under the MC precision used". Single-file edit, recompile supp, verify still 21pp. | tex | MED | 30 min |
| **CX-M** | **D13 decision support** (Fig 4 mixed error-bar bars) — produce `D13_FIG4_DECISION_BRIEF_20260418.md`: enumerate which Fig 4 cells have MC error bars vs which don't, estimate cost of MC-completion vs cost of split-panel restructuring, recommend one. **No figure edits.** | analysis | MED | 45 min |
| **CX-N** | **C8 energy equation** (`PAPER_REVIEW §3 C8`) — add the energy-model equation `E_total = Σ_layer (N_MAC^analog · e_analog + N_MAC^digital · e_digital) + α · interconnect` to `08_appendix.tex` (or a new supp section), with e_analog / e_digital / α stated as placeholder constants. Single-file edit, recompile supp. | tex | LOW | 30 min |
| **CX-O** | **Build `scripts/_gpt/check_locked_numbers.py`** (was CX-I in Round C; bumped after `check`-skeleton remained undone). Read `paper/CANONICAL_RESULT_LOCK_gpt.md` table → grep matching numbers in `paper/latex_gpt/sections/*.tex` → emit `(claim, expected, found, match?)` per row. Skeleton only, no CI hook. | tooling | MED | 1 h |
| **CX-P** | **NO new GPU lanes.** Wait for attn_proj-only to finish; on completion, append a row to `NL_LANE_RESULTS_20260418.md` and update `SUPP_TABLE_NL_ABLATION_SCAFFOLD.md` row (e). | passive | — | gated on GPU |

**Codex must NOT** start any of CX-J..CX-O if currently mid-launch on attn_proj — these are CPU-only and parallelizable, but priority order is J → K → L → M → N → O.

---

## K (Kimi) — Round D

| ID | Task | Type | Priority | Cost |
|:--|:--|:--|:--:|:--:|
| **K-I** | **`KIMI_QKV_COLLAPSE_INTERPRETATION_20260418.md`** — was K-F in Round C; verify file exists, otherwise produce. ~600-word mechanistic interpretation of QKV-only NL=2.0 collapse (18.72%) vs MLP/all-linear (~87%). Cover: (a) why query/key projections under severe NL destroy softmax attention geometry, (b) prior literature on attention noise sensitivity (cite if found), (c) one-paragraph framing for §6 Discussion. **No `.tex` edits.** | analysis | HIGH | 1 h (or skip if exists) |
| **K-J** | **Discussion vulnerability scan v2** — given all-linear has FINISHED at 87.49% (climbing was real), update `KIMI_DISCUSSION_VULNERABILITY_SCAN_20260418.md` (or write fresh) listing §6 Discussion claims that NOW require softening. Flag specifically: any "MLP-only" wording in §6 should reference "MLP and full-linear paths both recover" — but stay reviewer-honest about QKV-only failure. | analysis | HIGH | 1 h |
| **K-K** | **Cover letter v2 final pass** — was K-B (🛑 hold). Now UNBLOCKED since CLAUDE-A landed (Option B = supp-only). Produce `KIMI_COVER_LETTER_V2_FINAL_20260418.md` with redlines vs current `cover_letter.tex`: (1) ensure NL mitigation framed as "supplementary ablation, not main claim", (2) confirm OPECT 88.53±0.08% wording matches main, (3) one-line on QKV-only collapse honesty disclosure (or argue it stays in supp only). | text | HIGH | 1 h |
| **K-L** | **Reviewer-response phase-3 audit** — Codex appended new sections (Group-wise NL Mitigation Ablation + Learnable Inverse-Gamma E3) to `REVIEWER_RESPONSE_DRAFT_gpt.md`. Audit the prose: (a) does it correctly cite the supp table scaffold, (b) does the QKV failure get an honest disclosure, (c) does it overstate the all-linear result. Output `KIMI_RESPONSE_PHASE3_AUDIT_20260418.md`. **No edits to `REVIEWER_RESPONSE_DRAFT_gpt.md` directly.** | audit | MED | 45 min |

---

## G (Gemini) — Round D

> **Stateless-agent reminder (per project policy):** Gemini has no memory of prior conversation. Each task below is self-contained and re-cites canonical files. Re-read the cited files in full before producing output. Each output should re-state working assumptions in a "Reread of canonical state" header.
>
> Round-C confirmed Gemini delivered G-D / G-E / G-F / G-G / G-H ✅ — re-onboarding worked. Round D now leans on that throughput.

### G-I — `GEMINI_E1B_LANDING_PLAN_20260418.md` (NEW)

**Self-contained brief:** `GEMINI_E1B_EXECUTION_REFINEMENT_20260418.md` (Round-C deliverable, exists on disk) gave the runbook. The next step is a **landing plan** for when Codex actually launches it. Re-read your own `E1B_EXECUTION_REFINEMENT` first, then produce:

1. **Pre-launch smoke test sequence** — three 1-epoch dry runs (one per architecture) with assertion pass/fail criteria.
2. **Failure-mode catalog** — five most-likely failure modes with diagnostic + recovery action.
3. **Mid-run check-in cadence** — when should Codex pause and report (e.g. "after architecture 1 cell 3 finishes").
4. **Output schema** — JSON keys per cell so downstream Sobol-style analysis can ingest cleanly.
5. **Hand-off checklist** — what Codex must verify before declaring E1b complete.

Design only. No code.

### G-J — `GEMINI_P1_P2_P5_INTEGRATION_20260418.md` (NEW)

**Self-contained brief:** Round-C delivered three separate chapter outlines (`GEMINI_P1_P2_IRDROP_SNEAK_THESIS_OUTLINE`, `GEMINI_P5_THERMAL_THESIS_OUTLINE`, `GEMINI_E6_THESIS_CHAPTER_OUTLINE`). The thesis-scope question is now: **how do these three live together as one coherent chapter (or three sub-chapters)?** Re-read all three before producing:

1. **Recommended structure** — single chapter "Toward Circuit-Aware Simulation" with three subsections, OR three independent chapters? Argue both sides, recommend one.
2. **Shared mathematical scaffolding** — what equations / definitions / profile-interface entries are common to all three.
3. **Cross-experiment dependencies** — which experiments need to run before others (e.g. P5 thermal sweep needs P1 IR-drop spatial baseline first?).
4. **Total cost estimate** — wall-clock, GPU-hours, calendar time for the integrated chapter(s).
5. **Risk register** — three biggest risks with mitigation.

Design only.

### G-K — `GEMINI_THESIS_OUTLINE_DRAFT_20260418.md` (NEW)

**Self-contained brief:** Re-read `report_md/_gpt/THESIS_VS_PAPER_SCOPE_20260418.md` in full. Produce a top-level thesis-outline draft (chapter list with one-paragraph each):

1. Chapter 1 — Introduction & motivation (organic optoelectronic CIM landscape).
2. Chapter 2 — Background & related work (extends NC §2; thesis-only literature deep dives).
3. Chapter 3 — The compute_vit framework (NC §3 + extended methodology).
4. Chapter 4 — Profile-driven NC submission core (NC §5 results condensed).
5. Chapter 5 — Hardware-aware training (NC §5 + thesis-only HAT depth).
6. Chapter 6 — Toward circuit-aware simulation (G-J integrated chapter, P1+P2+P5+E6).
7. Chapter 7 — Reproducibility, datasets, & open-source release (REPRODUCIBILITY_PACKAGE_PLAN extension).
8. Chapter 8 — Conclusion & future work.

Each chapter paragraph: scope, what's shared with NC paper, what's thesis-only.

Design only. ~3 pages markdown.

### G-L — `GEMINI_FIG4_REDESIGN_BRIEF_20260418.md` (NEW)

**Self-contained brief:** `paper/latex_gpt/sections/05_results.tex` Fig 4 mixes cells with and without MC error bars (PAPER_REVIEW D13). Codex CX-M will recommend a path (split-panel vs MC-complete). In parallel, produce a **figure-redesign brief** in case the recommendation is split-panel:

1. **Current Fig 4 panel inventory** — re-read `paper/latex_gpt/sections/05_results.tex` and the Fig 4 caption; list which subpanels exist and which cells have / lack error bars.
2. **Two redesign options** with pros/cons:
   - Option A: split into Fig 4a (MC-quantified cells) + Fig 4b (deterministic cells).
   - Option B: keep single panel, mark deterministic cells with hollow markers + caption disclosure.
3. **Recommend one.**
4. **Implementation cost** — re-running which scripts? regenerating which CSV inputs?

Design only. **Do not edit the figure or the script.**

### Gemini summary table

| Task | File | Cost | Type |
|:--|:--|:--:|:--|
| G-I | `GEMINI_E1B_LANDING_PLAN_20260418.md` | 1 h | runbook extension |
| G-J | `GEMINI_P1_P2_P5_INTEGRATION_20260418.md` | 1.5 h | thesis structure |
| G-K | `GEMINI_THESIS_OUTLINE_DRAFT_20260418.md` | 1.5 h | thesis outline |
| G-L | `GEMINI_FIG4_REDESIGN_BRIEF_20260418.md` | 1 h | figure redesign |

**Order:** Independent, any order. Recommended G-K → G-J → G-I → G-L.

---

## Claude (own followups, scheduled)

| ID | Task | Gate |
|:--|:--|:--|
| CLAUDE-I | Read CX-J memo when delivered; confirm CLAUDE-A decision is now formally documented | after CX-J |
| CLAUDE-J | Read CX-K audit; if mismatch found, plan corrective `.tex` patch round | after CX-K |
| CLAUDE-K | Read K-J vulnerability scan v2 + K-K cover letter redlines; reconcile with §6/cover-letter | after K-J + K-K |
| CLAUDE-L | When attn_proj-only finishes, run final CLAUDE-A decision (escalate if attn_proj > 80%, hold Option B otherwise) | after attn_proj GPU drain |
| CLAUDE-M | Triage `CHECKPOINT_INVENTORY_20260418.md` `?` rows into final A/B/C tiers | independent — fit when slot opens |

---

## Anti-conflict matrix

| Pair | Conflict? | Why safe |
|:--|:--|:--|
| CX-J/K (doc/audit) ↔ attn_proj GPU | no | CPU-only |
| CX-L/M/N (`.tex` edits) ↔ Kimi K-J/K (text drafts) | partial | Kimi outputs are draft memos; only Claude lands them |
| CX-O (`check_locked_numbers.py`) ↔ everything | no | new file |
| Gemini all 4 ↔ Codex all 7 ↔ Kimi all 4 | no | distinct files |
| K-K cover letter v2 redlines ↔ CX-J CLAUDE-A memo | partial | both reflect Option B framing; K-K should cite CX-J once it lands |

---

## Termination criteria

Round D closes when:
- CX-J ✅ (the missing memo is the bookkeeping debt that has to clear)
- CX-K ✅ (audit confirms or refutes Codex's broadcast — non-negotiable for trust)
- At least 2 of CX-L/M/N/O ✅
- K-J + K-K ✅
- Gemini at least G-K + one other ✅
- attn_proj-only finishes; CLAUDE-L lands

After Round D, decision point: submit, or run E5 layer-wise gamma sensitivity (Codex Option A in their broadcast).

---

**End of broadcast.** All agents: log start in `AGENT_SYNC_gpt.md` when picking up a task. Mark ✅ in `CLAUDE_TASK_gpt.md` when delivered.
