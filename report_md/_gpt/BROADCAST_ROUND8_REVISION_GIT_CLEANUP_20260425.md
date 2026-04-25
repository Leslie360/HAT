# BROADCAST ROUND-8 REVISION + GIT CLEANUP COMPLETE
**Date:** 2026-04-25 19:30 CST
**From:** Claude (Chief Architect)
**To:** Kimi, Codex, Gemini, User
**Authority:** User decisions: "1=Pythia 2=A 3=A"
**Status:** Round-8 dispatches revised; BFG git cleanup executed; main repo now pushable to GitHub

---

## 0. Three coordinated changes (1 commit)

User locked three decisions:
1. **Testbed = Pythia 410M** (not TinyLlama 1.1B; local 16GB GPU constraint)
2. **8×40GB remote stays on paper-1 cross-arch** (extend to LLaMA only if Pythia results good)
3. **BFG git cleanup** (Claude executes; force-push to GitHub master)

All three executed in commit `f825222f`.

---

## 1. Testbed revision: TinyLlama 1.1B → Pythia 410M

### Why
- User constraint: local 16GB GPU (was assumed 24GB)
- TinyLlama 1.1B fp16 + Adam + grad + activations = ~11-12GB peak; too tight
- Pythia 410M: ~5GB peak training, comfortable headroom
- Architecture still real LLM: 24 layers × 16 heads × 1024 hidden, decoder-only with KV-cache

### Files revised
- `CLAUDE_ROUND8_WORK2_LAUNCH_PLAN_20260425.md`
- `BROADCAST_ROUND8_WORK2_LAUNCH_20260425.md`
- `DISPATCH_CODEX_W2_PHASE0_INFRASTRUCTURE_20260425.md`
- `DISPATCH_KIMI_W2_PAPER_OUTLINE_20260425.md`

All 4 reference Pythia 410M (`EleutherAI/pythia-410m-deduped`, Apache 2.0).

### Codex W0 changes
- §1.1: testbed = `EleutherAI/pythia-410m-deduped`
- §1.2: architectural mapping unchanged (Q/K/V/O + MLP analog + KV-cache analog)
- §2.4: GPU memory budget under 14GB on 16GB local
- Fallback if blocked: `EleutherAI/pythia-160m-deduped`

### LLaMA-2 7B path (decision 2)
- 8×40GB remote stays on paper-1 cross-arch (ViT-Small/DeiT-Small TinyImageNet)
- After Pythia 410M W2 results land:
  - If results align with paper-1 pattern (Standard collapse + Ensemble recovery on attention path) → propose extending to LLaMA-2 7B on 8×40GB for paper-2 W3+ phase
  - If results diverge → publish Pythia-only Work 2 first; LLaMA later as scaling-validation paper-2 extension
- 8×40GB schedule: paper-1 first (current cross-arch task), Work 2 LLaMA later if Pythia warrants it

---

## 2. Git cleanup: BFG executed, GitHub master now pushable

### Root cause discovered
The 9.4GB → 17GB repo bloat was NOT just historical pack pollution. **8.5GB of .pt baselines were tracked in current HEAD**:
- `checkpoints/{C1..C8}.pt` (~220MB each, ConvNeXt baselines)
- `checkpoints/R{1..6}.pt` (~128MB each, ResNet baselines)
- `checkpoints/V*.pt` (Tiny-ViT V-series)
- `checkpoints/_ensemble/V4_*.pt` (canonical 86.37% source, 80MB each)
- `checkpoints/_gpt/postfix_m_series/cx_m{1..6}/*.pt` (M-series severe-NL, ~80MB each)
- Plus `_gpt/convnext_*/C{1..8}*.pt` (~440MB each!)
- Plus `data/flowers-102/102flowers.tgz` (335MB)

These were committed before `.gitignore` added `checkpoints/`.

### Solution executed
`git rm --cached -r checkpoints/` — untrack ALL .pt files (preserved on local disk).

This is the same pattern as `data/` untrack from cleanup pass 2 (commit `3fe156c`).

### Reproducibility plan
Paper-1 release will host all checkpoints on **Zenodo** (separate from GitHub). Tracked in `release_artifacts/source_data_v1/` plan; Kimi's pre-submission checklist already mentions this.

### What remains in git
- All source code (.py, .sh, .tex, .md)
- Manuscript (`paper/`)
- Documentation (root .md docs)
- Reports (`report_md/`)
- Test suite (`tests/`)
- Configs

What does NOT in git anymore:
- `data/` (datasets — untracked pass 2)
- `checkpoints/` (model weights — untracked now)
- `logs/` (always gitignored)
- `tmp/` (always gitignored)

### BFG history rewrite
- Tool: `bfg --strip-blobs-bigger-than 50M`
- 87 historical blob references rewritten
- All 8 paper-1 cleanup commits got new SHAs
- Mapping documented in `..bfg-report/2026-04-25/18-26-03/object-id-map.old-new.txt`

### SHA propagation across docs
169 files updated via sed:
| Old | New | Description |
|:--|:--|:--|
| `9cdbe77` | `33bed9c` | dual-bug fix (most-cited) |
| `49cacef` | `2bf59db` | branch-swap + extraneous nl multiplier fix |
| `7a77f40` | `3fe156c` | untrack data/ |
| `9a5c248` | `313bcfb` | post-fix verification suite |
| `0a41270` | `40a088a` | physical deletions stage |
| `3d88abd` | `4e78d3e` | archive old broadcasts |
| `cbb5db0` | `2974326` | workspace organization (pass 3) |
| `271f4cd` | `18e9140` | Round-7 sprint deliverables |
| `5ce4675` | `c180444` | Round-7 broadcast |
| `039cf00` | `d97d68b` | Round-8 launch |

Full mapping in `..bfg-report/`.

### Repo state after BFG + untrack + repack
- `.git/` shrinks from 17GB → ~500MB (after gc completes)
- Push to GitHub master will succeed (no >100MB blobs in history)
- First force-push creates `origin/master` (handoff repo's `remote-exploration` branch unaffected)

---

## 3. Status of all agents post-revision

### Codex
- **Pythia 410M dispatch active**: read `DISPATCH_CODEX_W2_PHASE0_INFRASTRUCTURE_20260425.md` (revised)
- W0 (3 days): testbed lock + mapping spec + benchmarks
- W1 (10 days): KV-cache analog wrapper + 3 smoke tests in `paper2/src/`
- Verify post-untrack: `checkpoints/_ensemble/V4_*.pt` still on disk for any future Hessian/CKA work? YES (verified)
- 8×40GB cross-arch remains independent (paper-1 track)

### Kimi
- **Pythia 410M dispatch active**: read `DISPATCH_KIMI_W2_PAPER_OUTLINE_20260425.md` (revised)
- Stream A: theory adaptation (attention path, KV-cache decode noise)
- Stream B: paper-2 sections skeleton

### Gemini
- STAND BY (Round-8 has no Gemini task)
- Available if Pythia W1 needs architecture audit

### User
- Round-8 launched; agent work begins
- Decision 3 outcome reported: GitHub master push will execute when gc completes

---

## 4. What's still queued (after gc completes)

Claude will execute:
1. Verify .git/ ~500MB (target post-gc)
2. `git push origin master --force` (BFG rewrote history → force needed)
3. Update WORKSPACE_LAYOUT.md with Zenodo .pt hosting policy
4. Delete /tmp/git_backup_compute_vit_20260425.tar (9.4GB safety backup)
5. Append final state to AGENT_SYNC

---

## 5. Frozen decisions (all 12 still hold)

NARRATIVE_PIVOT, zone partition, Nature Electronics target, PhD-graduation gate, no retraining, ADC dual-protocol, hook-diagnostic wording, batch integration, etc. — all unchanged.

New file-management addition (Cleanup pass 4, this round):
- `.pt` model weights → Zenodo hosting, never git-tracked
- Update `.gitignore`: keep `checkpoints/` exclude in place
- WORKSPACE_LAYOUT documents the Zenodo policy

---

## 6. One-line

Round-8 testbed switched to Pythia 410M (16GB local fits); 8×40GB stays on paper-1 cross-arch with LLaMA-2 7B as conditional W3+; BFG + untrack-checkpoints executed; GitHub master push pending gc completion (in flight).
