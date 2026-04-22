# `_gpt/` Active Files Index — 2026-04-20

**Post-cleanup state**: 396 → 49 active files (rest archived under `archive/`).

---

## 🎛️ Live coordination (read every session)

| File | Purpose |
|:--|:--|
| `AGENT_SYNC_gpt.md` | Shared agent log — append status blocks here |
| `CLAUDE_TASK_gpt.md` | Task ledger with round-by-round tracking |
| `BROADCAST_ASSIGNMENT_20260421Q.md` | **CURRENT ROUND** (Round Q, 14-day, 2026-04-21 → 2026-05-05) |
| `BROADCAST_ASSIGNMENT_20260420P2.md` | Round P2 (superseded by Q) |
| `BROADCAST_FINAL_AUTONOMOUS_20260420.md` | Final Autonomous (fired early — J1d triple-report ambiguity) |
| `BROADCAST_GPU_DISPATCH_20260420.md` | GPU queue CX-J1b → J8 (updated by P2) |
| `BROADCAST_CLEANUP_20260420.md` | Cleanup broadcast (396→49 files) |
| `BROADCAST_ARBITRATION_20260420.md` | **Rule B enforcement**: defer "submit tonight" until CX-J1b/c/d close |
| `BROADCAST_MESSAGE_20260420.md` | External-review summary (10 perspectives) |
| `EXTERNAL_REVIEW_COMPILATION_20260420_FULL.md` | 10-reviewer compilation, 264 lines |
| `USER_METADATA_REQUEST_20260420.md` | Pending user-input form |

## 📈 GPU experiment landings (CX-J1 series)

| File | Status |
|:--|:--|
| `CODEX_JOINT_FULL_20260421.md` | CX-J1 joint warm-start (NEGATIVE: fresh-instance ~30.9%) |
| `CODEX_CX_J1_SUMMARY.md` – `CX_J8_SUMMARY.md` | Per-experiment Codex summaries |
| `CODEX_CX_J1d_SUMMARY.md` | Live summary scaffold for `CX-J1d-2` second-order STE |
| `CODEX_J1D_AMBIGUOUS_REPORT.md` | Branch-C scaffold if `J1d` lands in `35-50%` |
| `CODEX_J1D_CEILING_BROKEN_REPORT.md` | Branch-B scaffold if `J1d` exceeds `50%` |
| `CODEX_J1D_RECONCILIATION_20260421.md` | **Authoritative local audit** for the three conflicting `J1d` reports |

## 🧭 Claude audit + decision ledger (Round P2 active)

| File | Purpose |
|:--|:--|
| `CLAUDE_DA_RATIFICATION_20260420.md` | Day 1 rule ratification (language + no-rewrite) |
| `CLAUDE_DB_PHASE_A_AUDIT_20260420.md` | Day 3 phase-α audit (pending) |
| `CLAUDE_DC_PAPER_2_ROUTE_20260420.md` | Day 4 paper-2 route pick |
| `CLAUDE_DD_PHASE_B_AUDIT_20260420.md` | Day 7 phase-β audit (pending) |
| `CLAUDE_DE_PHASE_C_AUDIT_20260420.md` | Day 10 phase-γ audit (pending) |
| `CLAUDE_DF_REWRITE_TRIGGER_20260420.md` | Loop-closure single-shot rewrite trigger |
| `CLAUDE_DG_MONITOR_LOG_20260420.md` | Continuous monitor (enforces no paper-edit rule) |

## 📝 Kimi active deliverables (will roll into Round P2 Kimi K-Y* work)

Grouped by theme. All these are **frozen reference** during GPU loop.

**Thesis scaffolding (English reference for CN rewrite)**
- `KIMI_THESIS_CHAPTER_OUTLINE_20260420.md`
- `KIMI_THESIS_CONSISTENCY_20260420.md`
- `KIMI_THESIS_NARRATIVE_ARC_20260420.md`
- `KIMI_THESIS_SEVERE_NL_CHAPTER_20260419.md`

**NC submission (paper-1)**
- `KIMI_NC_FINAL_AUDIT_20260420.md`
- `KIMI_NC_SUBMISSION_CHECKLIST_20260420.md`
- `KIMI_REBUTTAL_MASTER_20260420.md` ⚠ NO EDITS during GPU loop
- `KIMI_CREDIT_STATEMENT_DRAFT_20260420.md`
- `KIMI_DATA_CODE_AVAIL_DRAFT_20260420.md`
- `KIMI_AUTHOR_BLURB_20260420.md`

**Paper-2 deep scope**
- `KIMI_PAPER_2_DEEP_SCOPE_20260420.md`
- `KIMI_LIT_LANDSCAPE_20260420.md`

**Community / outreach**
- `KIMI_BLOG_DRAFT_20260420.md`
- `KIMI_PRESS_RELEASE_20260420.md`
- `KIMI_PUBLIC_FAQ_20260420.md`
- `KIMI_SOCIAL_SHORTFORM_20260420.md`
- `KIMI_TALK_SCRIPT_15MIN_20260420.md`
- `KIMI_TALK_SCRIPT_5MIN_20260420.md`
- `KIMI_REPO_README_DRAFT_20260420.md`

**Defense**
- `KIMI_DEFENSE_QA_PREP_20260420.md`
- `KIMI_DEFENSE_SLIDES_OUTLINE_20260420.md`

**Theory notes**
- `KIMI_ENSEMBLE_FREQ_THEORY_NOTE_20260420.md`
- `KIMI_HAT_AS_REGULARIZER_NOTE_20260420.md`

## 🧠 Gemini active deliverables

- `GEMINI_GPU_STRATEGY_BRIEF_20260420.md` — GPU queue ordering rationale
- `GEMINI_ADC_FLOOR_THEORY_V2_20260420.md` — spec for CX-J7
- `GEMINI_IR_DROP_SPEC_V2_20260420.md` — spec for CX-J4
- `GEMINI_RETENTION_EXTENDED_SPEC_V2_20260420.md` — spec for CX-J6
- `GEMINI_TEMP_DRIFT_SPEC_V2_20260420.md` — spec for CX-J3

## 📁 Data directories

- `json_gpt/` — all JSON result files (was scattered at top-level)
- `csv_gpt/` — CSV summaries
- `images_gpt/` — PNG figures
- `json/` — legacy JSON (pre-refactor)
- `data_releases/` — Zenodo-ready bundle artifacts
- `reviewer_response/` — rebuttal assets
- `theory_memos/` — theory memo notebooks
- `visualizations/` — plotting outputs

---

## 📦 Archive map (`archive/` subdir)

| Subfolder | Count | Scope |
|:--|--:|:--|
| `dispatches_pre_round_k/` | 29 | Codex/Kimi/Gemini dispatches before Round K (04-15 to 04-18) |
| `broadcasts_rounds_a_to_o/` | 19 | Broadcasts A–O (now closed) |
| `round_p_rescinded/` | 61 | All K-X*, G-FF*, CLAUDE-C* files from Round P (rescinded by P2) + K-W* fold-ins (rescinded by no-rewrite rule) |
| `old_audits/` | 41 | Bibliography / citation / consistency audits from pre-Round-P rounds |
| `old_reviewer_prep/` | 89 | External review / figure audits / submission checklists pre-Round-P |
| `legacy_experiments/` | 73 | Smoke / pilot / ablation reports + pre-Round-P Gemini specs |

Total archived: **312 files**.

---

## 🚫 Forbidden during GPU loop (Rule B)

Do not edit these files until user declares loop closed:
- `paper/00_abstract.md`
- `paper/05_results.md`
- `paper/06_discussion.md`
- `paper/cover_letter*.md`
- `KIMI_REBUTTAL_MASTER_20260420.md`
- `paper/thesis/chapter_5_*.tex`

## ✅ Allowed during GPU loop

- New Round P2 deliverables (K-Y*, G-GG*) → create new files with `_20260420` or later date
- 中文 thesis work → `paper/thesis_cn/`
- Paper-2 skeleton → `paper/paper2/skeleton_v0/`
- Checklists (Phase δ Kimi work)
- Defense / community / grant materials

## 2026-04-22 authoritative local updates
- `CODEX_CX_K3_INTERPRETATION_20260422.md` — final local interpretation of completed `CX-K3` delta_g_eff sweep; best point `0.05 -> 36.21 ± 9.61%`, still below authoritative `K2 = 38.95 ± 9.85%`
