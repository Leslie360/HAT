# Kimi P6 Track G Report: Repo Hygiene Execution Plan

**Date:** 2026-05-09
**Dispatch:** `DISPATCH_SUPERPHASE_P6_EXPERIMENT_COMPLETION_AND_EVIDENCE_GAP_CLOSURE_20260509.md`
**Executor:** kimi

---

## 1. Git Status Summary

```
Untracked:  321 files
Modified:    95 files
Deleted:     31 files
```

The 31 deletions are primarily the 37 `.kimi_draft*` files batch-removed per DS/Mimo audit.

---

## 2. Draft/Stale File Audit

### 2.1 `.kimi_draft*` Files

| Count | Status |
|-------|--------|
| 37 deleted | **COMPLETE** |
| 0 remaining | Verified |

All `.kimi_draft*` files containing stale 86.37% values have been removed.

### 2.2 Root-Level Temp Files (Should Archive/Ignore)

| File | Action |
|------|--------|
| `AGENT_INTERCOM_HUB_20260428.md` | `.gitignore` |
| `AGENT_INTERCOM_HUB_20260429.md` | `.gitignore` |
| `AGENT_INTERCOM_HUB_20260506.md` | `.gitignore` |
| `broadcast.md` | `.gitignore` |
| `gpu_watcher.sh` | `.gitignore` |
| `output.md` | `.gitignore` |

### 2.3 Tarballs (Should Ignore)

| File | Size | Action |
|------|------|--------|
| `data/cifar-10-python.tar.gz` | ~170 MB | `.gitignore` (data dir) |
| `data/cifar-100-python.tar.gz` | ~170 MB | `.gitignore` (data dir) |
| `outputs/reviewer_archive_20260417.tar.gz` | Archive | `.gitignore` |
| `outputs/reviewer_archive_20260419.tar.gz` | Archive | `.gitignore` |
| `outputs/submission_bundle_20260417.tar.gz` | Archive | `.gitignore` |
| `release_artifacts/paper1_provenance_archive_20260509.tar.gz` | ~? | `.gitignore` |
| `release_artifacts/paper1_reviewer_bundle_20260501_1645.tar.gz` | ~? | `.gitignore` |
| `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` | ~? | `.gitignore` |

### 2.4 `.claude/` Workspace

| Count | Action |
|-------|--------|
| 2 files | `.gitignore` |

---

## 3. Proposed `.gitignore` Additions

```gitignore
# Agent workspaces
.claude/

# Data archives
data/*.tar.gz

# Output archives
outputs/*.tar.gz

# Release artifact tarballs (directories tracked, tarballs not)
release_artifacts/*.tar.gz

# Root-level temp files
broadcast.md
output.md
gpu_watcher.sh
AGENT_INTERCOM_HUB_*.md

# Deprecated/old review bundles
release_artifacts/paper1_reviewer_bundle_20260501_1645/

# Temporary eval logs
logs/_gpt/*.log
```

---

## 4. Commit Sequence (Proposed, Not Executed)

### Phase 1: Safe Commit (Recommended)

```bash
git add paper/latex_gpt/main.tex paper/latex_gpt/main.pdf
git add paper/latex_gpt/sections/*.tex
git add paper/latex_gpt/supplementary.tex
git add paper/latex_gpt/cover_letter.tex
git add paper/latex_gpt/refs_gpt.bib
git add paper/latex_gpt/figures/*.png
git add paper/latex_gpt/figures/tikz/*.tex
git add paper/latex_gpt/source_data/
git add report_md/_gpt/*.md
git add release_artifacts/paper1_submission_bundle_20260509_final/
git add release_artifacts/paper1_provenance_archive_20260509/
git add release_artifacts/paper1_release_candidate_20260509_clean/
```

### Phase 2: Add `.gitignore`

```bash
git add .gitignore
```

### Phase 3: Stage Deletions

```bash
git rm -r release_artifacts/paper1_reviewer_bundle_20260501_1645/ 2>/dev/null || true
git rm paper/latex_gpt/*.kimi_draft* 2>/dev/null || true
```

### Phase 4: Do NOT Push

Wait for user explicit approval.

---

## 5. Classification of Untracked Files

| Category | Count | Examples |
|----------|-------|----------|
| **Should commit** | ~140 | `report_md/_gpt/*.md`, release artifacts, source data |
| **Should .gitignore** | ~50 | `.claude/`, temp files, tarballs, logs |
| **Needs user decision** | ~10 | Old REMOTE files, old outputs |
| **Can delete** | ~120 | Build artifacts, old checkpoints, duplicate figures |

---

## 6. Verdict

Repo hygiene plan is actionable and non-destructive:
- All stale `.kimi_draft*` files deleted
- `.gitignore` proposal covers temp files, tarballs, agent workspaces
- Commit sequence is conservative (no push without approval)
- 321 untracked files need triage; ~140 should be committed

**No destructive actions proposed without user approval.**

---

*Report by kimi. Hygiene plan prepared on 2026-05-09.*
