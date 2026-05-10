# Codex Dispatch #10 — NL closeout + fig10 caption + Dispatch #9 hygiene

**Date:** 2026-04-18
**From:** Claude
**To:** Codex
**Priority order:** CX-A (GPU, blocking) > CX-B (text, fast) > CX-C (hygiene, idle-time)

---

## CX-A — Finish NL mitigation queue (GPU, host-WSL only)

Active thread: `V4_hybrid_standard_noise_hat_nl2_mlp_linear_comp`, Epoch 4 = 50.24% vs 27.72% anchor.

**Complete the queued runs** (per your own `scripts/_gpt/run_nl_followup_queue_local.sh`):
1. Finish MLP-only (running) — let it reach `final_test_acc` and dump JSON.
2. QKV-only linear-surrogate control (`run_task_v4_nl2_qkv_linear_comp.sh`).
3. All-analog linear upper-bound control (`run_task_v4_nl2_all_linear_comp.sh`).
4. After queue drains, re-enable `fresh_instance_cadence_control` if user hasn't redirected.

**Deliverable:** refresh `report_md/_gpt/NL_MITIGATION_SUMMARY_20260418.md` + associated `.png`/`.csv`/`.json` as each run lands. Already-wired `scripts/_gpt/summarize_nl_mitigation.py` handles the table regen.

**Reporting:** one block per run to `AGENT_SYNC_gpt.md` with: best_acc, final_test_acc, epochs, log path, JSON path.

**Constraints:** host-WSL execution only (`run_host_wsl_gpu.sh`); snap-scoped CUDA is still broken. Do not resume cadence eval while NL queue is live.

---

## CX-B — Fix `fig10_zero_shot_transferability` caption mismatch

Per `BROADCAST_INVERSE_GAMMA_DEEPDIVE_20260418.md` Next Action #4: the caption claims "Ensemble HAT recovery" but the panel shows Standard HAT collapse. Either:
- (a) the caption text is wrong and needs rewording to match what the figure depicts, or
- (b) the figure panel is the wrong render and needs swapping to the Ensemble HAT version.

**Do both checks:**
1. Read `paper/latex_gpt/sections/05_results.tex` (or wherever Fig.10 is `\includegraphics`) + the caption in `paper/latex_gpt/sections/` / supplementary.
2. Compare to the source render in `paper/figures/fig10_zero_shot_transferability.{png,pdf}`.
3. Check `paper/FIGURE_CAPTION_LOCK_gpt.md` — that's the authoritative caption; if the lock file disagrees with `.tex`, `.tex` is wrong.
4. Pick the minimum-edit path (usually caption rewording) and fix. Recompile `main.pdf`.

**Do NOT** regenerate the figure itself unless the lock file explicitly demands it. If you determine the panel is wrong, STOP and file a note — Claude will route to replotting.

**Deliverable:** one-line entry in `AGENT_SYNC_gpt.md` stating: which mismatch was found, which side was wrong, what diff landed, recompile status.

---

## CX-C — Execute Dispatch #9 TX-31 / TX-32 / TX-33 (only when GPU-idle)

Dispatch #9 brief: `report_md/_gpt/CODEX_DISPATCH_20260417_index_gpt.md`. Three tasks:
- **TX-31** Audit `PROJECT_INDEX.md` §3-§12 against reality → write `PROJECT_INDEX_AUDIT_20260417.md` with ✅/⚠️/⛔ and recommended diffs (do not apply).
- **TX-32** Move remaining `paper/` draft-superseded `.md` (01-07, PAPER_OUTLINE, banana/nano/perplexity prompts, `FIG1_FIG2_BRIEF_gpt.md`, `FIGURE_CAPTION_DRAFTS_gpt.md`, `参考文献库.md`) to `_archive/paper-drafts/` with grep whitelist. KEEP `08_appendix.md`, `CANONICAL_RESULT_LOCK_gpt.md`, `FIGURE_CAPTION_LOCK_gpt.md`, `FIGURE_PLAN.md`.
- **TX-33** Classify the 252 untracked + 68 unstaged files into TRACK / IGNORE / ARCHIVE. **Report only** — no `git add`, no `.gitignore` edit, no commit. Write `GIT_HYGIENE_LEDGER_20260417.md`.

**Constraint:** no code edits outside the three deliverable files. No commits. All moves reversible via `mv`.

---

## Global constraints

- CX-A is the priority; CX-B and CX-C must not steal GPU from NL queue.
- Host-WSL wrapper for all GPU work.
- Append one block per completed task to `AGENT_SYNC_gpt.md`.
- Update `CLAUDE_TASK_gpt.md`: add CX-A/B/C rows and mark TX-31/32/33 from pending to in-progress.
