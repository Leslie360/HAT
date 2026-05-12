# Remote107 Next Tasks — Post Extended Eval & Retention Sweep

Date: 2026-05-12
From: Remote107 agent
To: Codex coordinator
Branch: `107-clean`

## 0. Situation

All prior P0/P1/P2/P3 tasks from 2026-05-08 are completed and locked. Extended eval and retention sweep are also complete. Layer ablation training is running on GPUs 4/5/6/7.

Locked achievements since 2026-05-08:
- p28b/p69b robustness sweep: 26/26 configs each, claim-lock manifest committed.
- Extended downstream eval: MMLU/Winogrande/PIQA/BoolQ completed for p28b clean/analog and p69b analog; p69b clean completed (no MMLU).
- Retention noise sweep: 8/8 configs completed for p28b/p69b (0.001, 0.01, 0.1, 1.0).
- Qwen3-VL HAT training: 5000 steps completed on GPU 3 (last1 analog KV).
- Layer ablation training: 4 jobs running (p28b last2/last4, p69b last2/last4), 500 steps each.

## 1. Hard Rules (unchanged)

1. Do not mix evaluator protocols. Every table must state `ctx_len`, `stride`, `batch_size`.
2. Do not push checkpoints or large weights.
3. Push only code, JSON/CSV summaries, logs small enough for GitHub, and coordination MD.
4. Every new result must include exact command, git SHA, environment, checkpoint source, and JSON path.
5. If a task is expected to exceed 8 GPU-hours, first write a short plan/estimate MD and stop.

## 2. Current Task Inventory

| # | Task | Status | GPU | Blocker / Note |
|---|---|---|---|---|
| 66 | Extended downstream eval | **Completed** | — | 4/4 done, results saved. |
| 67 | Retention noise sweep | **Completed** | — | 8/8 done, results saved. |
| 68 | Layer ablation training (last2/last4 on p28b/p69b) | **In Progress** | 4/5/6/7 | Running since ~13:26. ETA 1-2h. |
| 69 | Cross-device eval (RRAM/PCM/FeFET) | **Pending** | 2/3 | No retraining; eval existing checkpoints under device-specific params. Ready to launch. |
| 70 | Energy profiling (analog vs digital KV cache) | **Pending** | — | No GPU. Pure analysis. Can start anytime. |
| 71 | Adaptive noise schedule HAT training | **Pending** | TBD | Requires algorithm design + training. Blocked by #68. |
| 72 | Theoretical justification (PAC-Bayes bound / implicit regularization) | **Pending** | — | No GPU. Math derivation. Can start anytime. |
| — | p69b clean MMLU eval | **Blocked** | — | datasets cache corruption. Need clean cache env or workaround. |
| — | Qwen3-VL 5000-step checkpoint eval | **Pending** | — | Can run on GPU 3 in parallel. |
| — | Qwen3-VL claim-lock metadata | **Pending** | — | Depends on Qwen3-VL eval. |
| 61 | Generate Paper 2 figures and update conclusions | **Pending** | — | User deferred. |

## 3. Execution Order (revised for innovation boost)

User directive: "最好都补上" — add theoretical, adaptive, cross-device, and energy dimensions.

**Phase A: Finish current batch (today)**
1. Wait for #68 (layer ablation training) to finish.
2. Immediately launch #69 (cross-device eval) on GPUs 2/3 (currently idle).
3. In parallel: start #70 (energy profiling) and #72 (theory) — no GPU needed.

**Phase B: New algorithm experiments (next batch)**
4. Design adaptive noise schedule strategies (#71). Requires short proposal MD per Hard Rule 5.
5. Train adaptive vs fixed baseline on 410M and 2.8B to prove improvement.

**Phase C: Cleanup**
6. p69b clean MMLU (if cache fix found).
7. Qwen3-VL eval + claim-lock.

## 4. Required Scripts

- `/tmp/run_layer_ablation_training.py` — layer ablation training automation (currently running)
- `/tmp/run_cross_device_eval.py` — cross-device eval (to be created)
- `scripts/energy_profile_kv_cache.py` — energy profiling (to be created)

## 5. Innovation Gap Analysis

| Dimension | Current State | Target | How to Close |
|---|---|---|---|
| Algorithm | Fixed noise injection | Adaptive schedule (cosine/layer-wise/step-wise) | Design + train #71 |
| Theory | Empirical only | PAC-Bayes bound / implicit regularization proof | Derive #72 |
| System | Single-device params | RRAM/PCM/FeFET cross-device validation | Eval #69 |
| Impact | PPL only | End-to-end energy/area/latency quantification | Analyze #70 |

## 6. Return Format

For each completed task, push one return file:

- `coordination/REMOTE107_<TASK>_RETURN_YYYYMMDD.md`

Each return must start with:

| Task | Status | GPU-hours | Changed locked claim? | Verdict |
|---|---:|---:|---:|---|

## 7. Acceptance Criteria for Full Closure

- #68 layer ablation checkpoints saved and eval'd.
- #69 cross-device eval JSONs for at least 3 device families.
- #70 energy profiling table with analog vs digital breakdown.
- #71 adaptive schedule shows PPL improvement over fixed noise on at least one scale.
- #72 theoretical framework document (even if preliminary).
- p69b clean MMLU result exists (even if run manually).
- Qwen3-VL 5000-step checkpoint has eval JSONs.
