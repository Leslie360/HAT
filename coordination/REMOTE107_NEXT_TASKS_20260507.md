# Remote 107 Next Tasks — 2026-05-07

Owner: Remote 107 executor  
Dispatcher: Codex  
Deadline target: 2026-05-08, return all available results by GitHub commit  
Branch: `107-clean`

---

## 0. Pull This Task

```bash
git fetch origin
git checkout 107-clean
git pull --ff-only origin 107-clean
```

If local work is dirty, do not reset. Commit or copy out local results first, then pull.

---

## 1. Current Local Verdict

Remote 107 is now the highest-priority experimental line.

Current v2 result summary from local audit:

| Route | Eval D2D | Mean PPL | Std | Status |
|---|---:|---:|---:|---|
| last1 analog KV `[23]` | 0.02 | 18.42 | 0.02 | strongest |
| last1 analog KV `[23]` | 0.04 | 18.55 | 0.02 | robust |
| last1 analog KV `[23]` | 0.05 | 18.60 | 0.03 | robust |
| last2 analog KV `[22,23]` | 0.02 | 18.71 | 0.02 | second-best |
| last2 analog KV `[22,23]` | 0.04 | 19.07 | 0.04 | second-best |
| last2 analog KV `[22,23]` | 0.05 | 19.21 | 0.03 | second-best |

Digital Pythia-410m baseline: PPL `15.68`.

Key decision:

> Make selective terminal-layer analog KV-cache canonical if it survives train-seed replication, fresh-D2D seeds, full metadata, and retention stress.

All-layer analog KV remains stress/control, not deployment route.

---

## 2. P0 Before More Runs: Metadata Patch

Before launching large new sweeps, patch train/eval JSON writing so every new JSON includes:

- `git_commit`
- `git_status_short`
- `script`
- `command`
- `mode`: train/eval
- `model`: exact model id
- `dataset_train`
- `dataset_eval`
- `train_seed`
- `train_d2d_seed`
- `eval_d2d_seed`
- `n_states`
- `sigma_c2c`
- `sigma_d2d`
- `retention_step_time`
- `analog_layers`
- `ctx_len`
- `stride`
- `max_steps`
- `batch_size`
- `ppl_before`
- `ppl_after` or `ppl`
- wall-clock time
- GPU id/name

Return one example train JSON and one example eval JSON before expanding.

Output:

```text
coordination/REMOTE107_METADATA_PATCH_20260508.md
```

---

## 3. K107-A: Canonical Selective KV Re-run

Run a compact canonical re-run of the strongest routes.

| ID | Train analog layers | Train noise | Train seeds | Eval D2D seeds | Eval D2D levels | Purpose |
|---|---|---|---|---|---|---|
| K107-A1 | `[23]` last1 | D2D=0.02, C2C=0 | 42, 123, 456 | 42, 123, 456, 789, 1001 | 0.02, 0.04, 0.05 | canonical last1 stability |
| K107-A2 | `[22,23]` last2 | D2D=0.02, C2C=0 | 42, 123, 456 | 42, 123, 456, 789, 1001 | 0.02, 0.04, 0.05 | close last2 comparison |
| K107-A3 | all 24 | D2D=0.02, C2C=0 | 42 only | 42, 123, 456, 789, 1001 | 0.02, 0.04, 0.05 | stress/control anchor |

Kill criteria:

- If last1 train seed 123 or 456 gives PPL > 22 at eval D2D=0.02, pause and report; do not expand.
- If metadata fields are missing, result is not canonical even if numerically good.
- If Base+Patch no-noise PPL drifts far from known patched baseline, stop and investigate.

Output:

```text
deliverable/results_v3/k107_a/*.json
deliverable/results_v3/k107_a/summary.csv
coordination/REMOTE107_K107_A_RETURN_20260508.md
```

---

## 4. K107-B: Retention Stress For Last1 KV

Run only after K107-A last1 passes.

| ID | Checkpoint | Eval sigma_d2d | Retention step times | Purpose |
|---|---|---:|---|---|
| K107-B1 | last1 `[23]`, D2D=0.02 train | 0.02 | 0, 0.1, 1, 10 | retention curve under nominal D2D |
| K107-B2 | last1 `[23]`, D2D=0.02 train | 0.05 | 0, 0.1, 1, 10 | retention under high mismatch |
| K107-B3 | digital baseline | 0 | matched eval | sanity anchor |
| K107-B4 | all-layer D2D=0.02 train | 0.02 | 0, 0.1, 1, 10 | stress/control |

If material profile handling is ambiguous, do not improvise. Return code notes instead.

Output:

```text
deliverable/results_v3/k107_b/*.json
deliverable/results_v3/k107_b/summary.csv
coordination/REMOTE107_K107_B_RETURN_20260508.md
```

---

## 5. K107-C: State-Count Sweep For Last1

Run after K107-A and K107-B, or start only if spare GPU time remains.

| n_states | Approx bits | Analog layers | Noise | Train seed |
|---:|---:|---|---|---:|
| 16 | 4-bit | `[23]` | D2D=0.02 | 42 |
| 32 | 5-bit | `[23]` | D2D=0.02 | 42 |
| 64 | 6-bit | `[23]` | D2D=0.02 | 42 |
| 128 | 7-bit | `[23]` | D2D=0.02 | 42 |
| 256 | 8-bit | `[23]` | D2D=0.02 | 42 |

Evaluation:

- eval D2D = 0.02 and 0.05
- eval D2D seeds = 42, 123, 456

Kill criteria:

- If 16/32 states are catastrophic, do not expand them to more seeds.
- Expand only the best low-state point to seeds 123/456.

Output:

```text
deliverable/results_v3/k107_c/*.json
deliverable/results_v3/k107_c/summary.csv
coordination/REMOTE107_K107_C_RETURN_20260508.md
```

---

## 6. Required Final Return Summary

Please write:

```text
coordination/REMOTE107_20260508_FULL_RETURN.md
```

It must include:

1. Branch + full commit SHA.
2. `git status --short`.
3. Py-compile output for modified scripts.
4. Environment packet.
5. Exact launcher commands.
6. Metadata patch description.
7. K107-A aggregate table.
8. K107-B retention table if completed.
9. K107-C state-count table if completed.
10. One-line verdict: `LOCK`, `PROVISIONAL`, or `STOP`.

Use compact JSON/CSV/Markdown only. Do not push large checkpoints unless explicitly requested.

---

## 7. Push Back

```bash
git status --short
git add coordination/REMOTE107_*_20260508.md deliverable/results_v3/
git commit -m "remote107: return selective KV canonical results"
git push origin HEAD:107-clean
```

If some result folders do not exist, adjust `git add` narrowly. Do not use `git add .`.

---

## 8. Pull Safety Warning

Do **not** run this while staying on `main`, `master`, or `remote-exploration`:

```bash
git pull origin 107-clean
```

That merges this compact/clean 107 deliverable branch into a full project branch and may appear to delete many files.

Correct sequence:

```bash
git fetch origin
git switch 107-clean 2>/dev/null || git switch -c 107-clean --track origin/107-clean
git pull --ff-only origin 107-clean
```

If you already see many `D ...` lines in `git status`, stop and do not commit or push. Return:

```bash
git status --short --branch
git rev-parse --abbrev-ref HEAD
git log --oneline -5
```
