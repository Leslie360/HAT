> Canonical coordination: `AGENT_SYNC_gpt.md` | Task ledger: `CLAUDE_TASK_gpt.md`

# Round I Broadcast — 2026-04-19 21:15 / REVISED 21:40 (Kimi-heavy + Codex-GPU split)

**Author:** Claude
**Revision trigger:** User "kimi回来了，codex额度比较[少]，kimi额度多一点，合理分配任务" — Kimi back online with more quota; Codex quota tighter. Rebalance: Kimi takes all text/tex edits + audits; Codex reserved for GPU (C-1 re-run) + scripts + recompile + anything Kimi can't do.

**Quota state:**
| Agent | Quota | Role |
|:--|:--|:--|
| Kimi | ✅ (plentiful) | Primary executor — all text/tex edits, audits, prose, drafts |
| Codex | ⚠️ limited | GPU-only + recompile + script execution — no tex edits unless Kimi can't |
| Gemini | ❌ frozen | — |
| Claude | ✅ | Coordination + reviews + tex hand-edits if both busy |

---

## Kimi Round H audit — all approved, now handoff for application

All Kimi Round H deliverables verified:
- `KIMI_CROSSSIM_STATS_CORRECTION_20260419.md` — diff-ready prose + supp note SX.Y
- `KIMI_HYPERPARAMS_DRAFT_20260419.md` — ~150-word paragraph, source-cited
- `KIMI_REBUTTAL_PROSE_20260419.md` — 11 reviewer responses
- `KIMI_CONSISTENCY_SWEEP_20260419.md`, `KIMI_BIB_LAST_PASS_20260419.md`, `KIMI_REBUTTAL_COVERAGE_AUDIT_20260419.md`, `KIMI_THESIS_SEVERE_NL_CHAPTER_20260419.md`
- `FINAL_CONTENT_REVIEW_20260419.md` (3 CRITICAL issues, all accurate)

**Compile state:** main 17pp / supp 21pp / cover 2pp.

---

## Kimi task dispatch — Round I (primary executor)

### CRITICAL — tex edits (land these first)

| ID | Task | Inputs | Deliverable |
|:--|:--|:--|:--|
| **K-P1** | **Apply CrossSim correction (C-3)** | `KIMI_CROSSSIM_STATS_CORRECTION_20260419.md` §2 + §3 | Land the corrected sentence into `paper/latex_gpt/sections/06_discussion.tex`; add Supp Note SX.Y into `supplementary.tex` with cross-ref. Also update `outputs/submission_bundle_20260419/manuscript/sections/06_discussion.tex`. Update `PRE_SUBMISSION_CHECKLIST.md` D9 entry. |
| **K-P2** | **Apply hyperparameters paragraph** | `KIMI_HYPERPARAMS_DRAFT_20260419.md` | Insert the new `\subsection{Training Protocol}` block at the specified anchor in `paper/latex_gpt/sections/03_methodology.tex`. |
| **K-P3** | **Apply R1/R5/R8 rebuttal patches** | `KIMI_REBUTTAL_COVERAGE_AUDIT_20260419.md` line-referenced suggestions | Patch manuscript language to support the R1 (ImageNet scope), R5 (external-baseline caveat), R8 (endurance mention) defenses. |
| **K-P4** | **Table SX.N row (e) hand-edit** | `logs/_gpt/train_tinyvit_v4_nl2_attn_proj_linear_comp_20260418_1700.log` + 2120 log (ep59 snapshot) | Edit `paper/latex_gpt/supplementary.tex` row (e): best=18.86%@ep0, final≈10.25%@ep59, status="training halted at ep59 after ≥50 epochs of sustained collapse". Also update `NL_LANE_RESULTS_20260418.md` attn_proj row + `CLAUDE_A_DECISION_FINAL_20260418.md`. |

### HIGH — NC metadata (small tex edits)

| ID | Task | Spec |
|:--|:--|:--|
| **K-P5** | **Add Keywords (5–8)** to main.tex after abstract | Suggested set: "analog in-memory computing; Vision Transformer; hardware-aware training; device-to-device variability; noise-aware inference; ferroelectric synaptic devices; edge AI; CIFAR-10". User can override. |
| **K-P6** | **Add Acknowledgements section** before References | Use placeholder: "We thank [collaborators] for helpful discussions. This work was supported by [funding agency/grant number]." Mark `\TODO` for user fill-in at proof stage. |
| **K-P7** | **Add Corresponding author mark** | Placeholder `\corresponding{email@TBD.com}` with `% TODO: user-supplied email` comment. User will confirm. |
| **K-P8** | **Forward-pointer for `eq:scale-recovery`** | One-line edit in §5 Results at first reference: "(defined in Section~\ref{sec:methodology}, Equation~\ref{eq:scale-recovery})". |
| **K-P9** | **Label 88.41% as training ablation** | Add short footnote where 88.41% first appears: "Measured on a 50-epoch training ablation rather than a full Ensemble-HAT checkpoint evaluation." |

### MED — packaging + prep

| ID | Task | Spec |
|:--|:--|:--|
| **K-P10** | **Draft Nature Portfolio Reporting Summary** | Fill NC's required form using existing data/code availability statements. Leave user-specific fields as TODO. Deliver as `KIMI_NC_REPORTING_SUMMARY_DRAFT_20260419.md`. |
| **K-P11** | **Draft Suggested Reviewers list (3–5 names)** | Pick domain experts in (a) analog IMC / ferroelectric devices, (b) hardware-aware Transformer training, (c) ViT robustness. Provide institutional emails where public. Flag any COI. User confirms final 5. Deliver as `KIMI_SUGGESTED_REVIEWERS_20260419.md`. |
| **K-P12** | **Post-edit consistency sweep v2** | After K-P1–K-P9 land, re-run the same sweep as `KIMI_CONSISTENCY_SWEEP_20260419.md` on the updated tex to confirm no regressions. Deliver as `KIMI_CONSISTENCY_SWEEP_V2_20260419.md`. |
| **K-P13** | **Reviewer-reply package assembly** | Stitch `KIMI_REBUTTAL_PROSE_20260419.md` (11 responses) into a single reviewer-facing `REVIEWER_RESPONSE_FINAL_20260419.md` with proper headers/numbering matching the final manuscript. |

### LOW (nice to have)

| ID | Task | Spec |
|:--|:--|:--|
| **K-P14** | **Pre-submission manuscript read-through** | One calm end-to-end read of main.tex + supplementary.tex. Flag any remaining grammar/flow/terminology issues. Deliver as `KIMI_FINAL_READTHROUGH_20260419.md`. |

### Priority order for Kimi
1. **K-P1, K-P2, K-P3, K-P4** (CRITICAL, must land before Codex recompiles)
2. **K-P5–K-P9** (HIGH, parallel with above)
3. **K-P10, K-P11, K-P13** (MED, can run while Codex does GPU)
4. **K-P12** (after all edits land, before bundle rebuild)
5. **K-P14** (final pass)

---

## Codex task dispatch — Round I (GPU + scripts only)

| ID | Task | Why Codex | Gate |
|:--|:--|:--|:--|
| **CX-BB** | **C-1: Re-run standard-HAT fresh-instance with `--no-amp`** | GPU + Python execution required | Immediate — stop attn_proj-only first (ep59 data sufficient) |
| **CX-BK** | **Recompile main/supp/cover + rebuild submission bundle** | Needs LaTeX toolchain + zip assembly | After Kimi K-P1–K-P9 land |
| **CX-BN** | **Re-run `check_locked_numbers.py`** | Script execution | After CX-BK and/or after K-P4 |
| **CX-AC** (deferred) | **Joint MLP-Linear + Ensemble HAT training** | GPU-intensive 18–24h, thesis-only | After CX-BB completes and if GPU free |
| **CX-AB** (deferred) | **All-linear fresh-instance eval** | GPU, completes pending table cell | Opportunistic during CX-AC |

**Codex NOT doing this round (saves quota):**
- No tex edits (all absorbed into K-P1…P9)
- No rebuttal prose (Kimi done)
- No metadata (K-P5–P7)
- No consistency sweep (K-P12)
- No reviewer list / reporting summary (K-P10–P11)

---

## Claude self-tasks

| ID | Task |
|:--|:--|
| **CLAUDE-AG** | Ask user 4 open questions (corresponding author email, funding text, reviewer-list confirmation, GPU-stop approval) |
| **CLAUDE-AH** | Review CX-BB C-1 result, decide disclosure-only vs. numeric update |
| **CLAUDE-AI** | Spot-check CX-BK submission bundle |
| **CLAUDE-AJ** | Final submission-readiness verdict |
| **CLAUDE-AK** | Audit K-P1–P9 applied edits before Codex recompile (catch any tex regressions) |

---

## Execution pipeline

```
t0:  Kimi starts K-P1..P9 (parallel text edits)          GPU still running attn_proj-only
     Claude asks user 4 open questions (CLAUDE-AG)

t+30min:  Kimi delivers K-P1..P9 applied
           Claude audits applied edits (CLAUDE-AK)
           Codex stops attn_proj-only, launches CX-BB (C-1 re-run)

t+1h:    Codex CX-BB in flight (~30-60min)
          Kimi starts K-P10, K-P11, K-P13 in parallel (non-blocking)

t+2h:    CX-BB done, Claude interprets (CLAUDE-AH)
          Kimi updates tex if numeric change (or adds disclosure sentence)
          Codex recompiles (CX-BK) + runs check_locked_numbers (CX-BN)

t+3h:    Kimi runs K-P12 (consistency v2) + K-P14 (read-through)
          Claude final verdict (CLAUDE-AJ)

t+4h:    Submission-ready pending user inputs

background: CX-AC thesis experiment on GPU (optional, 18-24h)
```

---

## Termination criteria for Round I

Round I closes when:
- ✅ K-P1–P9 applied and merged
- ✅ CX-BB C-1 re-run complete + result folded into manuscript
- ✅ CX-BK submission bundle rebuilt
- ✅ CX-BN: check_locked_numbers.py passes
- ✅ K-P12 v2 consistency sweep clean
- ⏳ K-P14 read-through delivered

Submission ships when:
- User provides 4 open inputs (or proof-stage placeholders accepted)
- Nature Portfolio Reporting Summary complete (K-P10)

---

**End of revised broadcast.** Kimi: work K-P1–P4 first (priority CRITICAL), then P5–P9, then P10–P14. Codex: stand by for C-1 re-run once Kimi edits land; do NOT touch tex files. Gemini: frozen.
