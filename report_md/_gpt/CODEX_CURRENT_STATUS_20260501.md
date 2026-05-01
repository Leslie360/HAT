# Codex Current Status — 2026-05-01

**Time:** 2026-05-01 16:37 CST
**Scope:** Paper-1 local closure, DS/Gemini non-GPU closure review, package readiness, Work-2 routing.

## 1. Executive Verdict

Paper-1 mandatory local GPU work remains closed. The current bottleneck is no longer experiments; it is release hygiene: source-data packaging, clean Git branch construction, and reviewer bundle discipline.

DeepSeek completed the requested non-GPU closure tasks. Gemini reviewed them and endorsed closing Paper-1. Codex rechecked the live tree, fixed stale path/protocol issues in DS's reviewer/GitHub checklists, and reran the core guards.

## 2. Live Verification

| Check | Result |
|---|---:|
| Main PDF compile | PASS, `paper/latex_gpt/main.pdf`, 14 pages |
| Supplementary PDF compile | PASS, `paper/latex_gpt/supplementary_main.pdf`, 41 pages |
| LaTeX/source grep for undefined refs/cites, fatal errors, overfull, placeholders, TODO/FIXME/TBD | PASS, no hits |
| Locked-number guard | PASS, 22/22 |
| Local PCM precision ladder guard | PASS |
| LaTeX bib key audit | PASS, 43 used keys, 0 missing |
| DOI/URL endpoint audit | PASS, 67/67 resolved or DOI-redirected |
| Figure manifest | Generated: `paper/latex_gpt/source_data/manifest_all_figures_20260501.{json,csv}` |

## 3. DS/Gemini Status

DeepSeek produced five closure artifacts:

| Artifact | Status | Codex readout |
|---|---|---|
| `DS_LEGACY_FIGURE_SOURCE_DATA_AUDIT_20260501.md` | Accepted | 20/24 legacy figure rows traced to JSON/CSV, 3 TikZ reconstructable, 2 unresolved conceptual diagrams. No data-fabrication blocker. |
| `DS_SEMANTIC_REFERENCE_AUDIT_20260501.md` | Accepted after integration | No citation-context overclaim. Three key-name mismatches were handled in live LaTeX/BibTeX. |
| `DS_SUPPLEMENTARY_HOSTILE_CLAIM_AUDIT_20260501.md` | Accepted | Two SI overclaims softened; no blocker. |
| `DS_REVIEWER_BUNDLE_PLAN_20260501.md` | Accepted with Codex correction | Fixed script paths from `scripts/check_*.py` to `scripts/_gpt/check_*.py`; corrected early-stop/provenance wording. |
| `DS_GITHUB_CLEAN_BRANCH_CHECKLIST_20260501.md` | Accepted with Codex correction | Fixed script paths and added warning that canonical JSONs inside checkpoint directories must be copied/force-added without `.pt` checkpoints. |

Gemini's cross-review endorses DS's closure and recommends moving focus to Work-2 Analog KV-cache after Paper-1 packaging.

## 4. Corrections Applied By Codex

1. Corrected DS reviewer bundle script paths:
   - `scripts/_gpt/check_locked_numbers.py`
   - `scripts/_gpt/check_local_pcm_precision_ladder.py`
2. Corrected DS GitHub clean-branch checklist with the same paths.
3. Added release-risk note: do not exclude canonical `fresh_eval.json`, `drift_eval.json`, and `training_history.json` evidence when excluding large `.pt` checkpoints. Either copy these JSONs into `paper/latex_gpt/source_data/canonical_json/` or force-add only JSON files.
4. Corrected protocol wording: canonical PCM artifacts completed the intended 100-epoch schedule, but not every wrapper used a uniform `--early-stop-patience 0` CLI; `training_history.json` and provenance fields are the source of truth.

## 5. Current Risk Register

| Risk | Severity | Status |
|---|---:|---|
| Dirty worktree with many tracked/untracked edits | High | Must not clean destructively. Use clean branch/export plan. |
| DS clean-branch checklist could still be too broad if executed blindly | Medium | Paths corrected; still needs Codex-guided staging before push. |
| Legacy SI conceptual figures have no source generator | Low | DS identified only two conceptual diagrams; reproducibility risk low. |
| Main Paper-1 data depends on JSONs inside checkpoint directories | Medium | Must preserve/copy JSON evidence while excluding `.pt` weights. |
| Remote 105 unavailable for five days | Low for Paper-1 | 105 remains optional/validation, not Paper-1 blocker. |
| Remote 107 noise-algorithm bug rerun pending | Not Paper-1 | Treat 107 as Work-2 trend-only until rerun returns. |

## 6. Routing Decision

### Paper-1

No more mandatory GPU. Next actions are packaging and release hygiene:

1. Build clean reviewer bundle.
2. Build/publication branch carefully.
3. Preserve canonical JSON evidence without committing `.pt` checkpoints.
4. Keep remote 105/107 out of Paper-1 main claims unless gates close later.

### Local Agents

- Codex: own release hygiene, clean branch, bundle, final verification.
- Gemini: optional final PDF/figure visual scan and reviewer-facing clarity pass.
- DS: optional mechanical packaging support only; no GPU.
- Kimi: no mandatory Paper-1 GPU; can help organize manuscript/source-data if available.

### Work-2 / Remote 107

Remote 107 remains a separate Analog KV-cache lane. Do not merge into Paper-1. Next 107 deliverable should include corrected noise math packet, rerun results, and minimal reproducibility code/math core.

## 7. Immediate Next Step

Do not spend GPU on Paper-1. The next Codex-controlled action should be one of:

1. create a clean reviewer reproducibility bundle; or
2. create a clean `publication-v1` branch/export plan; or
3. hand Work-2 KV-cache a new task list after 107 rerun returns.
