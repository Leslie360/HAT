# Kimi P5 Track F Report: Repo Hygiene and Commit Plan

**Date:** 2026-05-09
**Dispatch:** `DISPATCH_SUPERPHASE_P5_POST_AUDIT_REMOTE_AND_EXPERIMENT_GOVERNANCE_20260509.md`
**Executor:** kimi

---

## 1. Git Status Summary

```bash
git status --short
```

- **Modified files:** 96
- **Untracked files:** 303

---

## 2. Modified Files Classification

### Should Commit (Scientific / Source)

| File | Reason |
|------|--------|
| `paper/latex_gpt/main.tex` | Main manuscript updates |
| `paper/latex_gpt/main.pdf` | Rebuilt PDF |
| `paper/latex_gpt/sections/*.tex` | Section updates |
| `paper/latex_gpt/supplementary.tex` | Supplementary updates |
| `paper/latex_gpt/cover_letter.tex` | Cover letter updates |
| `paper/latex_gpt/refs_gpt.bib` | Bibliography updates |
| `paper/latex_gpt/figures/*.png` | Updated figures |
| `paper/latex_gpt/figures/tikz/*.tex` | TikZ source updates |

### Should NOT Commit (Draft / Backup)

| File | Reason |
|------|--------|
| `*.kimi_draft*` (37 files across project) | Draft files containing stale values (e.g. 86.37%); **DELETED in cleanup** |

---

## 3. Untracked Files Classification

### Should Commit

| Pattern | Count | Examples |
|---------|-------|----------|
| `report_md/_gpt/*.md` | ~130 | All agent reports, broadcasts, audits |
| `release_artifacts/paper1_submission_bundle_20260509_final/` | 1 | Final submission bundle |
| `release_artifacts/paper1_provenance_archive_20260509/` | 1 | Provenance archive |
| `release_artifacts/paper1_release_candidate_20260509_clean/` | 1 | Clean release candidate |

### Should Archive Locally (Not in Git)

| Pattern | Count | Examples |
|---------|-------|----------|
| `*.tar.gz` | 3 | `paper1_submission_bundle_20260509_final.tar.gz`, `paper1_provenance_archive_20260509.tar.gz`, `paper1_reviewer_bundle_20260501_1645.tar.gz` |
| `release_artifacts/paper1_reviewer_bundle_20260501_1645/` | 1 | Old reviewer bundle |

### Should Ignore (Add to .gitignore)

| Pattern | Count | Examples |
|---------|-------|----------|
| `.claude/` | ~50 | Agent workspace, memory, temp files |
| `paper/latex_gpt/ChatGPT Image*.png` | 4 | ChatGPT image prompts |
| `paper/latex_gpt/BROADCAST_EOF` | 1 | Temporary broadcast marker |
| `paper/latex_gpt/CLEAN_DRAFT_V3_FIXED.pdf` | 1 | Temporary PDF |
| `paper/latex_gpt/cover_letter_v6.tex.pdf` | 1 | Temporary PDF |
| `paper/latex_gpt/1` | 1 | Accidental file |
| `paper/latex_gpt/deprecated/` | ~20 | Deprecated LaTeX files |
| `AGENT_INTERCOM_HUB_*.md` | 3 | Root-level temp intercoms |
| `broadcast.md` | 1 | Root-level temp broadcast |
| `output.md` | 1 | Root-level temp output |
| `gpu_watcher.sh` | 1 | Root-level temp script |

### Needs User Decision

| Pattern | Count | Question |
|---------|-------|----------|
| `REMOTE_105_MULTIDATASET_TASKLIST_20260429.md` | 1 | Keep as historical or archive? |
| `REMOTE_HANDOFF_README_20260429.md` | 1 | Keep as historical or archive? |
| `REMOTE_NO_PUSH_RETURN_PROTOCOL_20260429.md` | 1 | Keep as historical or archive? |
| `GPU_SCHEDULE_20260428.md` | 1 | Keep as historical or archive? |

---

## 4. Tar.gz Tracking Policy

| File | Recommendation |
|------|----------------|
| `paper1_submission_bundle_20260509_final.tar.gz` | **Add to .gitignore** — binary artifact; bundle directory is already tracked if needed |
| `paper1_provenance_archive_20260509.tar.gz` | **Add to .gitignore** — binary artifact; archive directory is already tracked if needed |
| `paper1_reviewer_bundle_20260501_1645.tar.gz` | **Add to .gitignore** — old binary artifact |

Rationale: Git is not designed for large binary archives. The unpacked directories contain the actual source files and are preferred for version control.

---

## 5. Proposed .gitignore Additions

```gitignore
# Agent workspaces
.claude/

# Temporary files
paper/latex_gpt/BROADCAST_EOF
paper/latex_gpt/1
paper/latex_gpt/*.pdf
!paper/latex_gpt/main.pdf
!paper/latex_gpt/supplementary_main.pdf

# ChatGPT image prompts
paper/latex_gpt/ChatGPT Image*.png

# Draft files (glob covers all 37 deleted files)
*.kimi_draft*

# Deprecated LaTeX
paper/latex_gpt/deprecated/

# Root temp files
broadcast.md
output.md
gpu_watcher.sh
AGENT_INTERCOM_HUB_*.md

# Binary archives
release_artifacts/*.tar.gz
```

---

## 6. Conservative Commit Plan

### Phase 1: Safe Commit (Recommended Now)

```bash
git add paper/latex_gpt/main.tex paper/latex_gpt/main.pdf
git add paper/latex_gpt/sections/*.tex
git add paper/latex_gpt/supplementary.tex paper/latex_gpt/supplementary_main.tex
git add paper/latex_gpt/cover_letter.tex
git add paper/latex_gpt/refs_gpt.bib
git add paper/latex_gpt/figures/*.png
git add paper/latex_gpt/figures/tikz/*.tex
git add report_md/_gpt/*.md
git add release_artifacts/paper1_submission_bundle_20260509_final/
git add release_artifacts/paper1_provenance_archive_20260509/
git add release_artifacts/paper1_release_candidate_20260509_clean/
```

### Phase 2: Add .gitignore (Recommended Now)

Add the `.gitignore` entries above.

### Phase 3: User Decision Required

- Delete or archive `REMOTE_*_20260429.md` files at root?
- Delete old reviewer bundle directory (`release_artifacts/paper1_reviewer_bundle_20260501_1645/`)?
- **Done**: All 37 `.kimi_draft*` files deleted (11 in working tree, 26 in old release artifacts).

### Phase 4: Do NOT Push

Wait for user explicit approval before pushing. The repo may contain user-private material.

---

## 7. Verdict

Commit plan is conservative and safe. All 37 `.kimi_draft*` files containing stale values have been batch-deleted per DS/Mimo audit. Remaining deletions (old REMOTE files, reviewer bundle) require user approval. Binary archives should be `.gitignore`d, not committed.

---

*Report by kimi. Hygiene plan prepared on 2026-05-09.*
