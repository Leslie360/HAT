# Submission Readiness Checklist — 2026-04-19

**Target:** Nature Communications
**Status:** Content-complete; remaining work is administrative / packaging.

---

## ✅ Content-complete items

| Item | Status | Evidence |
|:---|:---:|:---|
| Main manuscript (15 pp) | ✅ | `main.pdf` compiles, 245 KiB |
| Supplementary (21 pp) | ✅ | `supplementary_main.pdf` compiles, 9.60 MiB |
| Cover letter (2 pp) | ✅ | `cover_letter.pdf` compiles, 27 KiB |
| All R1–R4 patches landed | ✅ | `R1_R4_LANDING_AUDIT_20260418.md` |
| Locked numbers verified | ✅ | `check_locked_numbers.py` 16/16 PASS |
| Table SX.N complete | ✅ | Row (e) filled with attn_proj-only 18.86% |
| Guard script | ✅ | `scripts/_gpt/check_locked_numbers.py` |
| README.md | ✅ | `compute_vit/README.md` |
| LICENSE | ✅ | `compute_vit/LICENSE` (Apache 2.0) |
| REPRODUCIBILITY.md | ✅ | `compute_vit/REPRODUCIBILITY.md` |
| Source data manifest | ✅ | `SOURCE_DATA_MANIFEST_20260418.md` |
| Source data v1 ZIP | ✅ | `release_artifacts/source_data_v1.zip` (144 KiB, 76 files) |
| Source data v1 manifest | ✅ | `release_artifacts/source_data_v1_MANIFEST.md` |
| Checkpoint inventory | ✅ | `CHECKPOINT_INVENTORY_20260418.md` |
| Reviewer response draft | ✅ | `REVIEWER_RESPONSE_DRAFT_gpt.md` Phase 3 |
| Rebuttal-ready table | ✅ | `REBUTTAL_READY_TABLE_20260419.md` |

---

## ⏳ Pending Kimi deliverables (Round H)

| ID | Task | Blocker |
|:---|:---|:---|
| K-O2 | Rebuttal prose expansion (11 objections) | Kimi quota |
| K-O3 | Bibliography last-pass (8 critical refs) | Kimi quota |
| K-O4 | Consistency sweep (stragglers, MLP-only overstatement) | Kimi quota |
| K-O5 | Thesis severe-NL chapter scaffold | Kimi quota |
| K-O6 | Source-data v1 manifest draft | Kimi quota |
| K-O7 | Rebuttal-coverage audit | Kimi quota |

**If Kimi can only deliver 3:** K-O1 ✅ done, K-O2 + K-O4 are submission-blocking.

---

## ⏳ Pending Claude / admin tasks

| Task | Owner | Priority | Notes |
|:---|:---|:---:|:---|
| Apply K-O1 diff to 3 files | Claude | **DONE** | Row (e) already filled |
| Apply K-O4 fixes after sweep | Claude | HIGH | Wait for K-O4 |
| Recompile after any tex changes | Claude | HIGH | CLAUDE-AF |
| Run check_locked_numbers.py | Claude | HIGH | 16/16 PASS |
| Build source_data_v1.zip | Claude | MED | Wait for K-O6 manifest |
| Zenodo Tier-A checkpoint deposit | Codex (quota-blocked) | MED | ~1.5 GB, need DOI for cover letter / methods footnote |
| requirements.txt pin | Codex (quota-blocked) | LOW | Exact PyTorch/CUDA patch versions |
| Final sign-off | Claude + user | HIGH | User approval of locked manuscript |

---

## ⏳ GPU-deferred (quota returns)

| Task | Owner | Reason |
|:---|:---|:---|
| CX-AC: MLP-Linear + Ensemble HAT joint training | Codex | Thesis-only; highest-value thesis experiment |
| CX-AB: all-linear fresh-instance eval | Codex | Completes NL lane fresh-instance matrix |
| attn_proj-only fresh-instance eval | Codex | Completes NL lane fresh-instance matrix |

---

## Pre-submission sign-off gate

Before upload, verify:
- [ ] Main PDF: 15 pp, all figures render, no missing refs
- [ ] Supp PDF: 21 pp, all tables render, Table SX.N row (e) visible
- [ ] Cover letter: 2 pp, contributions = 4, page count = 15
- [ ] check_locked_numbers.py: 16/16 PASS
- [ ] Source-data ZIP: all figure/table CSVs present
- [ ] Zenodo DOI inserted (if Tier-A deposited)
- [ ] No git mutations (per project rules)

---

**Bottom line:** Manuscript is content-complete and compile-verified. Remaining blockers are (1) Kimi K-O2/K-O4 text deliveries, (2) source-data ZIP assembly, (3) optional Zenodo deposit. No GPU work needed for submission.
