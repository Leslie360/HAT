# REMOTE A100 Dispatch — Post-Fix Cross-Host Replication
**Date:** 2026-04-24
**Issued by:** Claude (Architect)
**Target:** Remote A100 (NVIDIA Apamayo)
**Trigger:** User has remote A100 access; can fire commands to the remote machine which currently runs the most-recent-GitHub-pushed code.

---

## ⚠️ Prerequisite (MUST DO FIRST)

Local HEAD is `33bed9c` (bug fix). GitHub HEAD is `50863aa` (pre-fix). **The bug fix is not on GitHub yet.** Until pushed, remote runs bug-contaminated code and any NL≠1.0 result is invalid.

**User runs locally:**
```bash
cd /home/qiaosir/projects/compute_vit
git push origin master
```

**Then on remote (one of):**
```bash
cd <repo_path> && git fetch origin && git reset --hard 33bed9c
# OR
cd <repo_path> && git pull origin master
```

**Remote then verifies:**
```bash
git rev-parse HEAD          # must print 33bed9c...
python test_dual_bug_fix.py  # must pass 5/5
```

If remote's `HEAD != 33bed9c` after pull, **STOP**. Do not run any of the queue below until that is sorted.

---

## A100 advantage (why bother with remote)

A100 vs user's local card: roughly 1.5–3× faster training throughput depending on memory bandwidth utilization. This means:
- Single Tiny-ViT NL=2.0 run drops from ~10 GPU-h to ~3-5 GPU-h
- 5 seeds in parallel (different processes, single A100) ≈ 1.2× single-run time
- Cross-host parity check is decisive evidence against "local-machine-specific" artifacts

Remote should run **only** the queue below. No exploratory sweeps. No new recipes. No paper text.

---

## R-M priority queue (5 jobs)

All jobs use:
- Code at commit `33bed9c`
- Explicit `--nl-ltp` and `--nl-ltd` flags
- AMP enabled
- From scratch (no warm-start)
- Save to `checkpoints/_gpt/postfix_remote_m_series/r_m{N}_<config>_seed{S}/`
- Tee logs to `logs/_gpt/r_m{N}_<ts>.log`
- Fresh-eval 10×5 with explicit NL flags
- Output JSON to `report_md/_gpt/json_gpt/r_m{N}_fresh_eval.json`

### Job R-M0 — Sanity gate (~30 min, no real training)

Verify provenance before any real training:
```bash
git rev-parse HEAD                                  # must equal 33bed9c...
sha256sum analog_layers.py                          # record for provenance
python test_dual_bug_fix.py                         # 5/5 pass
python test_groupwise_nl_wrapper.py                 # 8/8 pass
python -c "import torch; print(torch.cuda.get_device_name(0))"  # must be A100
```

Output: `r_m0_sanity.json` with the four checks. If anything fails, halt remote queue and report.

### Job R-M1 — Standard HAT NL=2.0 cross-host replication (~3-5 GPU-h)

**Same config as local CX-M1 but seed 123 confirmed.** Cross-host parity for the 82.63% headline.

Train Standard HAT V3 from scratch:
- `--nl-ltp 2.0 --nl-ltd -2.0`
- `--noise-mode uniform`
- `--hat-training False` (Standard HAT is fixed-mask, not Ensemble)
- `--seed 123`
- `--epochs 100`, `--batch-size 64`, AMP on

Then fresh-eval:
- `--num-instances 10 --mc-runs 5`
- `--nl-ltp 2.0 --nl-ltd -2.0` (explicit; the post-fix eval script defaults are correct now per CX-REGRESSION but be explicit)

**Decision rule on landing:**
- If `r_m1_mean ∈ [80, 85]%`: cross-host agrees with local CX-M1. Strong evidence the 82% headline is real. Proceed to R-M2.
- If `r_m1_mean ∈ [75, 80] ∪ [85, 90]%`: 1–3pp off local. Probably fine but flag to Claude before continuing.
- If `r_m1_mean < 75%` or `> 90%`: significant divergence. **Halt queue.** Report `R_M1_HOST_DIVERGENCE.md` with full env diff (PyTorch version, CUDA version, AMP behavior, batch determinism flags).

### Job R-M2 — Proportional HAT NL=2.0 from scratch (~3-5 GPU-h)

**This is the proportional-90.88% claim's true test.** Trained from scratch at NL=2.0 with proportional noise, NOT the eval-only NL swap that produced the false headline.

Train Proportional HAT V4:
- `--nl-ltp 2.0 --nl-ltd -2.0`
- `--noise-mode proportional`
- `--hat-training True`
- `--seed 123`
- 100 epochs, AMP on

Fresh-eval same as R-M1.

**Decision rule on landing:**
- If `r_m2_mean > r_m1_mean + 5%`: proportional genuinely outperforms uniform under true NL=2.0. The proportional story survives. Run R-M3 to replicate.
- If `r_m2_mean ∈ [r_m1_mean - 3, r_m1_mean + 5]`: proportional ≈ uniform. Drop proportional from paper. Skip R-M3.
- If `r_m2_mean < r_m1_mean - 3%`: proportional under-performs. Drop. Skip R-M3.

### Job R-M3 — Proportional HAT seed B replication (~3-5 GPU-h, conditional on R-M2)

Only fire if R-M2 mean > R-M1 mean + 5%. Same as R-M2 with `--seed 456`.

If R-M3 lands within 2σ of R-M2: proportional story is paper-grade. Two seeds, two hosts agreeing — strong.

### Job R-M4 — Bug-immunity empirical confirmation (~1-2 GPU-h)

Re-eval the existing canonical Ensemble HAT @ NL=1.0 checkpoint with commit `33bed9c` code. This empirically validates the §1 scope claim in `BROADCAST_REBUILD_3WEEK_20260424.md`.

The checkpoint is already on GitHub repo (don't retrain). Path on remote: same as local `checkpoints/_gpt/.../V4_hybrid_ensemble_hat_<canonical>.pt` (Codex provides exact path).

Fresh-eval:
- `--nl-ltp 1.0 --nl-ltd -1.0`
- 10 instances × 5 MC

**Decision rule on landing:**
- If lands at `86.37 ± 1.54%` (within 2σ): **bug-immunity confirmed empirically**. The §1 claim in the rebuild broadcast is validated. Canonical paper figures stay as-is.
- If significantly different: **major escalation**. Halt all rewrites. Codex re-audits.

### Job R-M5 — Multi-seed reproducibility (5 seeds Standard HAT, ~15-25 GPU-h)

Fire only after R-M1 confirms the 82% headline.

Run 5 Standard HAT NL=2.0 from scratch, seeds {234, 345, 456, 567, 678}. Same config as R-M1 otherwise. This gives N=5 means → tighter CI on the headline number → much stronger paper claim.

If A100 has multi-process parallelism (e.g., one Tiny-ViT per ~4 GB VRAM), can run 4-5 seeds in parallel.

Fresh-eval each, output `r_m5_seed{S}_fresh_eval.json`. Aggregate to `r_m5_aggregate.json`.

---

## What remote returns

Compact JSON evidence only. **No checkpoint transfer back.** If we need the actual `.pt`, we ask separately.

Required JSON fields per run:
- `git_head` (commit hash)
- `code_sha256s` (analog_layers.py + train_tinyvit_ensemble.py + eval_fresh_instances_postfix.py)
- `exp_cfg` (NL, noise mode, sigma, hat, seed, epochs, batch_size, AMP)
- `best_acc`, `best_epoch`
- `fresh_per_instance_mean[]` (10 values)
- `fresh_aggregate.mean`, `.std`, `.median`, `.range`
- `cuda_device_name`, `pytorch_version`

---

## What remote does NOT do

- No paper text edits
- No new recipes beyond R-M{0..5}
- No exploratory sweeps
- No Work 2 / KV-cache work
- No file cleanup / archival
- No theory memos

If remote tries to do any of these: stop. Report.

---

## Coordination with local CX-M series

Local Codex is also running CX-M1 (Standard HAT seed 123) and queued M2/M3. Remote and local will produce **two parallel streams** of the same experiments. This is the point — cross-host parity.

**Comparison table will be:**

| Run | Local CX-M{N} | Remote R-M{N} | Verdict |
|:--|:--|:--|:--|
| Standard HAT NL=2.0 seed 123 | CX-M1 | R-M1 | Within 2σ → headline robust |
| Ensemble HAT NL=2.0 seed 123 | CX-M2 | (not on remote queue — local only) | Local-only confirmation |
| Proportional HAT NL=2.0 from scratch seed 123 | CX-M3 | R-M2 | Within 2σ → proportional story robust |
| Proportional seed 456 | CX-M4 | R-M3 (conditional) | Two-seed-two-host = paper grade |
| Multi-seed sweep | (not on local — too slow) | R-M5 | A100-only contribution |
| Canonical NL=1.0 recheck | CX-CANONICAL-RECHECK | R-M4 | Two-host bug-immunity proof |

---

## Timing estimate

If user pushes `33bed9c` to GitHub today and remote pulls:

| Day | Remote |
|:--|:--|
| Today (04-24) | R-M0 sanity (30 min) → R-M1 launches (~3-5 h) → R-M4 (~1-2 h) |
| Tomorrow (04-25) | R-M1 lands; R-M2 launches; R-M5 launches in parallel if A100 supports |
| Day 3 (04-26) | R-M2 lands; R-M3 fires conditionally; R-M5 finishes |
| Day 4 (04-27) | All evidence in. Cross-host comparison complete. |

This compresses local's 1-week M-series into 4 days of cross-host evidence, plus gives N=5 reproducibility. If user is OK with the push to GitHub, this materially shortens the rebuild.

---

## Decision the user must make right now

1. **Push commit `33bed9c` to GitHub?** (yes / no)
   - Yes → remote becomes useful immediately, dispatch R-M0 → R-M5 as above.
   - No → remote stays useless until pushed; no point firing any commands.
2. **Authorize R-M5 multi-seed sweep on A100?** (yes / no)
   - It uses 15-25 GPU-h on the A100. If billed, decide first.
3. **Want remote to run R-M4 canonical-recheck?**
   - Cheap (~1-2 GPU-h), strong evidence, recommended yes.

Default if user says nothing: push, run R-M0 → R-M1 → R-M4, await user signal before R-M2/M5.

---

## One-line summary

User pushes commit `33bed9c` to GitHub. Remote pulls. Remote sanity-checks (R-M0), then runs Standard HAT NL=2.0 seed 123 (R-M1, cross-host parity) and Ensemble HAT NL=1.0 recheck (R-M4, bug-immunity proof) within ~6 hours. If R-M1 confirms ~82%, fire Proportional NL=2.0 from-scratch (R-M2) — that's the kill-or-confirm test for the proportional story. If R-M2 wins, replicate (R-M3). Optional N=5 multi-seed (R-M5) for tight CI. All cross-checked against local CX-M series.
