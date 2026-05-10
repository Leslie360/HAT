> Canonical coordination: `AGENT_SYNC_gpt.md` | Task ledger: `CLAUDE_TASK_gpt.md`

# Round E Broadcast — 2026-04-18 23:15 (post-Round-D landing audit)

**Author:** Claude
**Trigger:** User instruction "广播对齐一下一下先". Round E compacts Round-D deliverables and re-broadcasts residual work.
**Hard rules carry over:** Codex GPU lanes priority, no new GPU lanes until attn_proj-only drains.

---

## Round D deliverable audit

| Round-D ID | Claimed | On disk? | Verdict |
|:--|:--|:--|:--|
| CX-J | `CLAUDE_A_DECISION_PRELIM_20260418.md` | ❌ | **SUPERSEDED** — `CLAUDE_A_DECISION_FINAL_20260418.md` exists instead (Option B LOCKED). No action needed. |
| CX-K | `R1_R4_LANDING_AUDIT_20260418.md` | ✅ | Exists. |
| CX-L | D11 Zhang identical-rows footnote | ✅ | Landed in `08_appendix.tex` line 107. |
| CX-M | D13 Fig 4 decision brief | ✅ | Integrated directly into `REVIEWER_RESPONSE_DRAFT_gpt.md` (new section "Additional Reviewer-Facing Evidence: Figure 4 Error-Bar Disclosure"). No separate `.md` produced. |
| CX-N | C8 energy equation | ✅ | Landed in `supplementary.tex` §Energy Profiler Implementation (lines 436–465). |
| CX-O | `check_locked_numbers.py` | ✅ | Built, debugged, **16/16 PASS** on 2026-04-18. |
| K-I | QKV collapse interpretation | ❌ | **NOT FOUND** — re-broadcast below if still needed. |
| K-J | Discussion vulnerability scan v2 | ❌ | `KIMI_DISCUSSION_VULNERABILITY_DISPATCH_20260418.md` exists but not the scan itself. **Re-broadcast below.** |
| K-K | Cover letter v2 final | ❌ | File not found, but `cover_letter.tex` already contains Option B framing + OPECT 88.53±0.08%. **Re-broadcast as light-touch audit.** |
| K-L | Response phase-3 audit | ❌ | File not found, but draft was updated by Codex/Claude. **Re-broadcast as light-touch audit.** |

**Compilation verification (this round):** `main.pdf` (245 KiB), `supplementary_main.pdf` (9.6 MiB), `cover_letter.pdf` (28 KiB) — all pass.

---

## Verified state at dispatch (23:15)

### GPU state

| Lane | Status | Headline |
|:--|:--|:--|
| MLP-only NL=2.0 | ✅ FINISHED | best=87.79% @ ep74 |
| QKV-only NL=2.0 | ✅ FINISHED — COLLAPSED | best=18.72% @ ep2 |
| All-linear NL=2.0 | ✅ FINISHED | best=87.49% @ ep59, final 84.81% |
| attn_proj-only NL=2.0 | 🔄 RUNNING | started ~17:00; ETA ~20 h remaining |

### Manuscript state

| Doc | Pages | Notes |
|:--|:--|:--|
| Main | **15** | R1–R4 patches absorbed |
| Supp | **21** | C8 energy eq + D11 identical-rows defense + NL ablation scaffold |
| Cover | **2** | Option B framing, OPECT 88.53±0.08% |

### PRE_SUBMISSION_CHECKLIST (updated this round)

- Locked Numbers: **11/11 verified** by guard script
- R1 Abbreviations: **16/16 done**
- R2 Data Rigor: **D1–D12 done**; D13 pending attn_proj / reviewer decision
- R3 Calculation Clarity: **C1–C11 done**
- R4 Physical Mapping: **P1–P5 done**

---

## Residual task board (Round E)

### Blocking (must clear before submission)

| ID | Task | Owner | Type | Gate |
|:--|:--|:--|:--|:--|
| **B1** | **attn_proj-only NL mitigation completion** | Codex (passive) | GPU | Running; auto-finalize via `auto_finalize_nl_ablation.py` on completion. |
| **B2** | **Table SX.N final integration** | Codex | tex | After B1. Fill row (e) in supp table + cross-ref in cover letter if needed. |

### CPU-only (parallelizable now)

| ID | Task | Owner | Type | Priority | Notes |
|:--|:--|:--|:--|:--:|:--|
| **E1** | **Cover letter v2 light-touch audit** | Kimi | text | MED | Confirm `cover_letter.tex` lines 26–58 correctly frame NL mitigation as supplementary ablation (not 5th contribution) and cite Table SX.N. Output `KIMI_COVER_LETTER_AUDIT_20260418.md` — pass/fail + one-line redline if needed. |
| **E2** | **Response draft light-touch audit** | Kimi | audit | MED | Confirm `REVIEWER_RESPONSE_DRAFT_gpt.md` (a) cites Table SX.N correctly, (b) does not overstate all-linear, (c) honestly discloses QKV-only collapse. Output `KIMI_RESPONSE_AUDIT_20260418.md` — pass/fail. |
| **E3** | **Discussion vulnerability scan v2** | Kimi | analysis | MED | Given all-linear 87.49% + QKV 18.72% + MLP 87.79%, list any §6 Discussion sentences that still imply "MLP-only" exclusivity and should be broadened to "MLP and full-linear paths both recover, while QKV remains structurally required." Output `KIMI_DISCUSSION_VULNERABILITY_SCAN_20260418.md`. No `.tex` edits. |
| **E4** | **Fig 4 source-data prep** | Codex | tooling | LOW | In anticipation of D13 reviewer pushback, prepare a CSV + README for Fig 4 raw data (MC seeds, deterministic baselines, architecture/dataset labels) so "source data" submission requirement is ready. No figure edits. |
| **E5** | **REPRODUCIBILITY_PACKAGE_PLAN scrub** | Claude | doc | LOW | Verify `REPRODUCIBILITY_PACKAGE_PLAN.md` matches current codebase paths; flag stale references. |

### Thesis-only (non-blocking)

| ID | Task | Owner | Type | Notes |
|:--|:--|:--|:--|:--|
| T1 | QKV collapse interpretation | Kimi | analysis | If E3 covers the same ground, T1 can be absorbed into E3. Otherwise standalone. |
| T2 | E1b landing plan | Gemini | runbook | Already assigned in Round D (G-I); carry over if not delivered. |
| T3 | P1+P2+P5 integration | Gemini | design | Already assigned in Round D (G-J); carry over. |
| T4 | Thesis outline draft | Gemini | design | Already assigned in Round D (G-K); carry over. |

---

## Anti-conflict matrix

| Pair | Conflict? | Why safe |
|:--|:--|:--|
| E1–E5 ↔ attn_proj GPU | no | All CPU-only or doc-only |
| E1 (Kimi) ↔ E4 (Codex) | no | Distinct files |
| B2 (Codex) ↔ E1–E3 (Kimi) | no | B2 is gated on B1; E1–E3 run now |

---

## Termination criteria for Round E

Round E closes when:
- B1 ✅ (attn_proj-only finishes)
- B2 ✅ (Table SX.N row e filled)
- At least 2 of E1–E3 ✅
- `main.pdf` + `supplementary_main.pdf` + `cover_letter.pdf` recompile cleanly after B2

After Round E, the submission package is effectively complete except for:
- Source-data ZIP assembly
- Code snapshot / reviewer archive
- Final proofread pass

---

**End of broadcast.** All agents: log start in `AGENT_SYNC_gpt.md` when picking up a task. Mark ✅ in `CLAUDE_TASK_gpt.md` when delivered.
