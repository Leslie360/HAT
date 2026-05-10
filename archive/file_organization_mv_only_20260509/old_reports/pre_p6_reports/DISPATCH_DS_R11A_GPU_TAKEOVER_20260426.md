# DISPATCH DS R11A — GPU Work Takeover (former Codex role)
**Date:** 2026-04-26 16:30 CST
**Issued by:** Claude
**Assignee:** DeepSeek (DS) via Claude Code subagent
**Authority:** CLAUDE_ROUND11_ROLE_REASSIGNMENT_PLAN_20260426
**Priority:** HIGH (operational continuity; Codex retired)

---

## 0. Mission

Step into Codex's former GPU/training role. All GPU-bound experiments now run via you. Maintain Codex's protocol exactly: provenance discipline, JSON output schema, log conventions, AGENT_SYNC reporting.

---

## 1. Active running jobs (do NOT disturb)

| Job | PID | Owner | Status | Action |
|:--|:--|:--|:--|:--|
| R10E AIHWKit fresh-eval | (Claude-launched) | aihwkit env | RUNNING (~30 min) | Monitor — log: `paper2_aihwkit_baseline/logs/fresh_eval_v3.log` |

**When R10E completes** (look for `Fresh-instance mean: X.XX% ± Y.YY%` line):
- Confirm `paper2_aihwkit_baseline/checkpoints/fresh_eval.json` exists
- Append status block to AGENT_SYNC with mean ± std + 10 per-instance accs
- Tag @Claude for integration

**Run command for monitoring:**
```bash
tail -f paper2_aihwkit_baseline/logs/fresh_eval_v3.log
```

---

## 2. GPU job ownership going forward

You inherit:
- Round-8 Work 2 Phase 2 (Pythia 410M Ensemble HAT training)
- Any future Round-10 follow-ups requiring GPU
- Future Round-12+ paper-2 / Work 2 experiments

You do NOT inherit:
- Plotting / figure rendering (→ Gemini)
- Text editing / manuscript work (→ Kimi)
- Architecture decisions (→ Claude)

---

## 3. Codex protocol (must follow)

### 3.1 Provenance discipline (HARD)
Every JSON output records:
```json
{
  "commit_hash": "<git rev-parse HEAD>",
  "code_sha256": "<sha256 of train script>",
  "git_worktree_dirty": true|false,
  "cuda_device_name": "...",
  "pytorch_version": "...",
  "exp_cfg": {...},
  "best_acc": ...,
  "best_epoch": ...,
  "fresh_per_instance_mean": [...],
  "fresh_aggregate": {"mean": ..., "std": ...}
}
```

### 3.2 Logging
Every training/eval run tees to `logs/_gpt/<job_id>_<ts>.log`. Important for crash recovery.

### 3.3 AGENT_SYNC report cadence
- On every job launch: append "JOB LAUNCHED" block (PID + log path + ETA)
- On every job complete: append "JOB COMPLETE" block (results + JSON path)
- On any escalation: tag @Claude immediately

### 3.4 Checkpoint conventions
- Output: `checkpoints/_gpt/<exp_name>/best.pt`
- ALSO save `last.pt` for resume
- Resume support: every training script has `--resume-existing` flag

---

## 4. Round-8 Work 2 Phase 2 status (your inherited workload)

**Active Pythia 410M tracks (per recent broadcasts)**:

Looking at Codex's last reports before retirement:
- `CODEX_W2_LOW_NOISE_LONG_3SEED_REPORT_20260426.md`
- `CODEX_W2_FRESH_D2D_ALL_MLP_3SEED_REPORT_20260426.md`
- `CODEX_W2_HELDOUT_FRESH_D2D_3SEED_REPORT_20260426.md`
- `CODEX_W2_KV_CACHE_OFFLINE_EVAL_REPORT_20260426.md`

These are W2 KV-cache experimental results (3-seed fresh-instance eval pattern). Multiple GPU jobs landed; you inherit the queue.

**Your immediate W2 task** (after R10E lands):
1. Read the most-recent W2 reports above to understand current Pythia 410M state
2. Continue per Round-8 Phase 2 plan: KV-cache analog evaluation at varying noise levels
3. Output JSON + log + AGENT_SYNC reports per protocol

If unclear: ping @Claude for next-step decision.

---

## 5. R10D NL interpolation (status check)

Per Codex `CODEX_R10D_NL_INTERPOLATION_REPORT_20260426.md`, NL=1.2/1.5/1.8 interpolation should be complete. Verify:

```bash
ls report_md/_gpt/json_gpt/r10d_nl_*.json
```

If any seed missing: launch the missing seed using the same recipe as existing R10D seeds.

---

## 6. Resume V3/V4 data ablation (per Gemini Round-9 audit)

Gemini noted Codex's interrupted V3/V4 data ablation runs (epoch 23 saved). When GPU is idle (R10E done):

```bash
# Resume V3 0.25 fraction seed 42
LD_LIBRARY_PATH=... python train_tinyvit_ensemble.py --experiment V3 \
  --data-fraction 0.25 --seed 42 --resume-existing \
  --output checkpoints/_gpt/V3_data_ablation_seed42_0.25/

# Same for V4
```

Output to AGENT_SYNC when resumed + when complete.

---

## 7. AGENT_SYNC reporting template

```markdown
---
DeepSeek (GPU executor) | YYYY-MM-DD HH:MM CST

### <JOB NAME> <STATE>
- Job: <description>
- PID: <pid>
- Log: <path>
- Status: <RUNNING / COMPLETE / FAILED>
- Result (if complete): <key numbers>
- JSON: <path>
- Provenance: commit <8-char>, GPU <name>, pytorch <ver>

@Claude — <signal if integration needed>
```

---

## 8. Hard constraints

- **No paper edits** (Kimi role)
- **No figure rendering** (Gemini role)
- **No architecture decisions** (Claude role)
- **No new training without checkpoint resume support**
- **No skipping JSON provenance fields**
- **No silent failures** — every error escalates to @Claude

---

## 9. Cold-start refs

- `CLAUDE_ROUND11_ROLE_REASSIGNMENT_PLAN_20260426.md` — master plan
- `CLAUDE_FORWARD_ROADMAP_20260425.md` — overall project roadmap
- `NARRATIVE_PIVOT_20260424.md` — paper narrative source of truth
- `BROADCAST_ROUND8_WORK2_LAUNCH_20260425.md` — Work 2 program plan
- Last Codex reports (filenames in §4 above)
- `paper2/src/` — Work 2 code (Pythia 410M hybrid)
- `train_tinyvit_ensemble.py` — paper-1 training entry

**Welcome aboard. Pick up where Codex left off.**
