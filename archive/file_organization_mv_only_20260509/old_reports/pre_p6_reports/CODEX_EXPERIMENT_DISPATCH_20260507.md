# CODEX Experiment Dispatch — 2026-05-07

Owner: Codex as experiment architect
Scope: experiment-first plan. Paper figure/layout polish is explicitly out of scope for this dispatch.
Current judgment: 107 KV-cache is the only line with clearly improving new signal; prioritize it.
Execution agents: Kimi = GPU/experiment executor, DS = code/protocol auditor, Gemini = hostile experimental reviewer.

---

## 0. Global Direction

### What changes now

We stop spending shared agent capacity on Paper-1 figure polish. The user and Gemini will handle main/SI visuals separately over a longer cycle.

The team focus moves to experiments:

1. Make Remote 107 KV-cache results canonical enough to trust.
2. Expand the selective terminal-layer KV route because it is the strongest current positive result.
3. Finish only the minimal local/105 experiments needed to close open questions.
4. Use Doctor EPSC data as a measured-profile/proxy calibration line, not as a Paper-1 headline claim.

### Current evidence base

Remote 107 v2 current best:

| Route | Eval D2D | Mean PPL | Std | Status |
|---|---:|---:|---:|---|
| last1 analog KV `[23]` | 0.02 | 18.42 | 0.02 | strongest |
| last1 analog KV `[23]` | 0.04 | 18.55 | 0.02 | robust |
| last1 analog KV `[23]` | 0.05 | 18.60 | 0.03 | robust |
| last2 analog KV `[22,23]` | 0.02 | 18.71 | 0.02 | second-best |
| last2 analog KV `[22,23]` | 0.04 | 19.07 | 0.04 | second-best |
| last2 analog KV `[22,23]` | 0.05 | 19.21 | 0.03 | second-best |

Reference:

- Digital Pythia-410m PPL: 15.68.
- All-layer analog KV is a stress/control route, not the deployment route.
- 107 v2 fixed a prior noise-algorithm bug; prefer `deliverable/results_v2`, not `p0_p3_archive`.
- Current 107 JSON metadata is still incomplete for paper-locking.

---

## 1. Priority Stack

### P0 — Remote 107 Canonical Selective-KV Experiments

This is the main experimental route.

Goal: turn the current positive 107 signal into a defensible experimental package.

### P1 — Local 5-bit PCM Multiseed Completion

Only continue if the pipeline is already alive or easy to resume. Do not start a large new R11D branch unless it directly resolves the 4/5/6/8-bit precision-retention frontier.

### P2 — Remote 105 Seed Completion

Wait for the server. When it returns, only run the minimal seed789 checks needed to resolve proportional-vs-digital ambiguity.

### P3 — Doctor EPSC Measured-Profile Calibration

Useful for thesis/defense/future hardware calibration. Not a replacement for Paper-1 main results and not a claim of full hardware validation.

---

## 2. Tasks For Kimi

Kimi owns GPU/experiment execution and result collation.

### K-107-A: Full-Metadata Re-run Of Selective KV Core

Run a small canonical re-run of the strongest 107 cases with full metadata embedded in every JSON.

Required fields in every JSON:

- `git_commit`
- `git_status_short`
- `script`
- `command`
- `mode`: train/eval
- `model`: Pythia-410m or exact model id
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
- wall-clock time and GPU id

Minimum re-run matrix:

| ID | Train analog layers | Train noise | Train seeds | Eval D2D seeds | Eval D2D levels | Purpose |
|---|---|---|---|---|---|---|
| K107-A1 | `[23]` last1 | D2D=0.02, C2C=0 | 42, 123, 456 | 42, 123, 456, 789, 1001 | 0.02, 0.04, 0.05 | canonical last1 stability |
| K107-A2 | `[22,23]` last2 | D2D=0.02, C2C=0 | 42, 123, 456 | 42, 123, 456, 789, 1001 | 0.02, 0.04, 0.05 | close last2 comparison |
| K107-A3 | all 24 | D2D=0.02, C2C=0 | 42 only | 42, 123, 456, 789, 1001 | 0.02, 0.04, 0.05 | stress/control anchor |

Kill criteria:

- If last1 train seed 123 or 456 gives PPL > 22 at eval D2D=0.02, pause and report; do not expand.
- If metadata fields are missing, result is not canonical even if numerically good.

Output:

- `results/K107_A_selective_kv_canonical/*.json`
- `results/K107_A_selective_kv_canonical/summary.csv`
- `report_md/_gpt/KIMI_K107_A_SELECTIVE_KV_CANONICAL_202605xx.md`

### K-107-B: Retention Stress For Last1 KV

Rationale: KV cache is memory-bound; retention is central. Current best result mostly validates noise robustness, not retention robustness.

Run only after K-107-A last1 passes.

Matrix:

| ID | Checkpoint | Eval sigma_d2d | Retention step times | Purpose |
|---|---|---:|---|---|
| K107-B1 | last1 `[23]`, D2D=0.02 train | 0.02 | 0, 0.1, 1, 10 | retention curve under nominal D2D |
| K107-B2 | last1 `[23]`, D2D=0.02 train | 0.05 | 0, 0.1, 1, 10 | retention under high mismatch |
| K107-B3 | digital baseline | 0 | matched eval | sanity anchor |
| K107-B4 | all-layer D2D=0.02 train | 0.02 | 0, 0.1, 1, 10 | stress/control |

If the code supports material profiles, evaluate both organic and PCM retention modes. If profile support is ambiguous, do not improvise; ask DS to audit first.

Kill criteria:

- If Base+Patch no-noise PPL is not within a small band of the known patched baseline, stop; likely patch/eval bug.
- If retention implementation cannot be explained in code, stop; do not produce uninterpretable numbers.

Output:

- `report_md/_gpt/KIMI_K107_B_KV_RETENTION_STRESS_202605xx.md`

### K-107-C: Bit-Depth / State-Count Sweep For Last1

Run after K-107-A and K-107-B.

Purpose: find whether last1 KV can use fewer states without large PPL loss.

Matrix:

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

- `report_md/_gpt/KIMI_K107_C_KV_STATE_SWEEP_202605xx.md`

### K-LOCAL-A: 5-bit PCM Multiseed Finish Only

Check whether current 5-bit PCM jobs are already running or easily resumable.

Allowed:

- finish seed456 and seed789 if already scheduled;
- summarize 4/5/6/8-bit source/fresh/drift in one table;
- stop if the run is stale or checkpoint provenance is unclear.

Do not launch new R11D variants beyond 5-bit without a separate dispatch.

Output:

- `outputs/R11D_5BIT_PCM_MULTI_SEED_SUMMARY_202605xx.md`
- `report_md/_gpt/KIMI_LOCAL_5BIT_PCM_FRONTIER_202605xx.md`

### K-105-A: Minimal Seed789 When Server Returns

105 server is currently delayed. When it returns, run only these first:

| Arch | HAT type | Seed | Purpose |
|---|---|---:|---|
| deit_small_patch16_224 | digital | 789 | same-arch baseline |
| deit_small_patch16_224 | proportional | 789 | check P>D trend |
| vit_small_patch16_224 | digital | 789 | resolve ViT ambiguity |
| vit_small_patch16_224 | proportional | 789 | resolve ViT ambiguity |

Fresh eval protocol must remain 10 instances x 5 MC.

Do not run ensemble/standard seed789 until these four are returned and reviewed.

Output:

- `report_md/_gpt/KIMI_105_SEED789_MINIMAL_202605xx.md`

---

## 3. Tasks For DS

DS owns code/protocol correctness. DS should not chase new algorithms until these audits are closed.

### DS-107-A: KV Noise/Retention Code Audit

Audit these files from the 107 clean snapshot or current 107 repo:

- `analog_kv_cache.py`
- `analog_layers.py`
- `p3_hat_train.py`
- `p3_hat_eval.py`
- `pipeline_runner.py`
- `pipeline_fresh_d2d.py`

Questions to answer:

1. Does C2C resample per forward pass?
2. Does D2D remain fixed per device instance/checkpoint unless eval seed override is passed?
3. Are train D2D seed and eval D2D seed semantically separated?
4. Does `analog_layers=[23]` only patch the terminal layer and not accidentally all layers?
5. Is retention applied in conductance domain or only as output perturbation?
6. Does the model use the same dataset split for all PPL comparisons?
7. Is `Base+Patch` still close enough to the digital baseline after the SDPA fix?
8. Are ctx_len, stride, and full WikiText-2 evaluation consistent across runs?

Output:

- `report_md/_gpt/DS_107_KV_PROTOCOL_AUDIT_202605xx.md`

### DS-107-B: Metadata Patch

If 107 code still does not write full metadata, patch the JSON writer or launcher so every train/eval JSON carries the required fields in §2 K-107-A.

Output:

- patch summary
- py_compile output
- example JSON with all metadata fields

### DS-EPSC-A: Measured EPSC Profile Conversion Design

Do not run GPU. Design the conversion from `数据_博士/EPSC_*` into a new measured-profile packet.

Inputs:

- `数据_博士/EPSC_ANALYSIS_READY.csv`
- `数据_博士/EPSC_DEVICE_SUMMARY_CODEX.csv`
- `数据_博士/EPSC_D9_REPEAT_SUMMARY_CODEX.csv`

Deliverables:

1. Define which statistic maps to C2C proxy.
2. Define which statistic maps to D2D proxy.
3. State explicitly why EPSC peak variation is only a proxy, not direct conductance D2D.
4. Produce a draft JSON schema named `Doctor_EPSC_20260501_proxy_profile.json` but do not claim it as canonical hardware profile.
5. Recommend a minimal eval matrix if Kimi later runs it.

Output:

- `report_md/_gpt/DS_EPSC_PROFILE_CONVERSION_DESIGN_202605xx.md`
- optional JSON draft under `数据_博士/derived_profiles/`

---

## 4. Tasks For Gemini

Gemini is no longer assigned main/SI figure polish under this dispatch. The user may still use Gemini separately for visuals.

Gemini's experiment role: hostile reviewer before and after expensive runs.

### G-107-A: Pre-Run Hostile Review

Review K-107-A/B/C and DS-107-A/B before large execution.

Questions:

1. Is the 107 matrix sufficient to prove last1 is genuinely robust rather than overfit to seed42?
2. Is retention stress designed correctly for KV-cache relevance?
3. Are any planned comparisons unfair due to different ctx_len, stride, n_states, or eval split?
4. What kill criteria should be stricter?
5. Which single result, if negative, should make us abandon 107 as a paper route?

Output:

- `report_md/_gpt/GEMINI_107_EXPERIMENT_HOSTILE_REVIEW_202605xx.md`

### G-107-B: Post-Run Claim Audit

After Kimi returns K-107-A/B/C, Gemini reviews only claims, not aesthetics.

Required verdicts:

- `LOCK`: safe to use as canonical.
- `PROVISIONAL`: numerically useful but metadata/protocol incomplete.
- `KILL`: contaminated, unfair, or uninterpretable.

Output:

- `report_md/_gpt/GEMINI_107_RESULTS_CLAIM_AUDIT_202605xx.md`

### G-105-A: Seed789 Interpretation Audit

When 105 seed789 returns, answer one question only:

Does proportional HAT genuinely beat digital on TinyImageNet across architecture/seed, or is the observed DeiT gain seed/architecture-specific?

Output:

- `report_md/_gpt/GEMINI_105_SEED789_INTERPRETATION_202605xx.md`

---

## 5. What Not To Do

- Do not spend shared agent time on Paper-1 figure aesthetics under this dispatch.
- Do not launch new M-series/NL/proportional-noise vision experiments unless they directly answer an active kill criterion.
- Do not merge 107-clean into the Paper-1 branch.
- Do not cite `/tmp/...` data paths; use stable snapshots under `docs/data/remote_snapshots_20260507/`.
- Do not claim Doctor EPSC data is full hardware validation.
- Do not use old 107 `p0_p3_archive` as current v2 evidence except for history comparison.

---

## 6. Operator Summary For User To Forward

Send this short instruction if needed:

```text
New direction from Codex: stop shared paper-figure polishing; focus on experiments.
Priority is 107 KV-cache because it is the only line with strong new signal.
Kimi: run K-107-A first (last1/last2/all24 canonical metadata rerun), then K-107-B retention stress, then K-107-C state-count sweep. Also finish only existing 5-bit PCM and wait for 105 seed789.
DS: audit 107 noise/retention code and patch metadata output before large runs; design Doctor EPSC measured-profile conversion but do not overclaim.
Gemini: hostile-review experiment design/results only, not aesthetics. First review whether K-107-A/B/C are sufficient and whether kill criteria are strict enough.
No new vision-side exploratory GPU jobs unless they answer the above kill criteria.
```

---

## 7. Success Criteria For This Round

This round succeeds if one of the following happens:

1. 107 last1 selective KV becomes canonical across train seeds and fresh D2D seeds, with retention stress characterized.
2. 107 fails under strict retest, so we stop spending time on it and preserve it as a negative/partial result.
3. 105 seed789 resolves whether proportional HAT is real cross-architecture signal or just DeiT/seed-specific.
4. Local 5-bit PCM closes the 4/5/6/8-bit precision-retention curve without spawning new uncontrolled experiments.

The best expected outcome is #1.
