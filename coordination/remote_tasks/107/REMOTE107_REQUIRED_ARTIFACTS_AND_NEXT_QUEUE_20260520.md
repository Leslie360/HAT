# Remote107 Required Artifacts + Next Queue - 2026-05-20

Coordinator: Codex local
Remote branch observed: `origin/107-clean`
Observed commit: `c7dd17eb5fa862e4f2fb692ae983cd2ea32613c8`
Observed summary file: `paper2/results/remote107/paper2_results_summary.json`

## 0. Current Local Verdict

Codex fetched the 2026-05-20 Remote107 push and copied the summary JSON locally for review.

Local review artifacts:

- `compute_vit/report_md/_gpt/CODEX_REVIEW_REMOTE107_PUSH_20260520.md`
- `compute_vit/report_md/json/remote107_paper2_results_summary_20260520.json`
- `compute_vit/report_md/csv/remote107_paper2_results_summary_20260520.csv`

Verdict:

- The new summary is useful as a structured Remote107 evidence index.
- It is **not yet claim-locked** for new large-model Paper2 claims.
- Existing 410M claim-lock package remains the only locked Remote107 evidence lane.

Main blockers:

1. Commit message says `p69b adaptive_cosine_last2 PPL 11.29 vs 11.40 digital baseline`, but those numbers are not present in `paper2_results_summary.json`.
2. In the pushed summary JSON, p69b `adaptive_cosine_last2` Lambada is `clean_perplexity=5.175765` and `analog_perplexity=5.344261`, i.e. analog is worse on that metric.
3. Commit message says all 20 configs are included, but `meta.total_entries=19`.
4. `git_commit_hat` remains `unknown`.
5. Larger-model rows have summary fields and source filenames, but not a complete local source package manifest comparable to the 410M claim-lock package.

## 1. Required Upload Package From Remote107

Please create and push a package under:

```text
paper2/results/remote107/source_lock_20260520/
```

Minimum required files:

```text
paper2/results/remote107/source_lock_20260520/
  README_PROTOCOL.md
  PACKAGE_MANIFEST.json
  remote107_paper2_results_summary_20260520.json
  remote107_paper2_results_summary_20260520.csv
  source_json_inventory_20260520.csv
  checkpoint_inventory_20260520.csv
  raw_json/
    <all lm_eval_* JSON files referenced by paper2_results_summary.json>
  logs/
    <stdout logs if available>
```

If raw JSON files are large, still push the summary package first and list missing files explicitly in `PACKAGE_MANIFEST.json` with `status=missing_large_file`. Do not silently omit them.

## 2. README_PROTOCOL.md Requirements

`README_PROTOCOL.md` must include:

1. exact git commit of the Remote107 code repository,
2. exact git commit of the HAT base repository, replacing current `git_commit_hat=unknown`,
3. `git status --porcelain` at run time, or a statement that the run was from a clean tree,
4. Python/PyTorch/Transformers/lm-eval versions,
5. GPU model,
6. dataset/task names and split definitions,
7. metric definitions for each task,
8. exact train commands,
9. exact eval commands,
10. whether clean and analog evals share the same checkpoint,
11. whether `--analog` only changes inference path or also reloads any trained state,
12. whether `sigma_c2c`, `sigma_d2d`, and `n_states` are defaulted or explicitly passed during eval,
13. PPL formula and tokenization details for every perplexity field.

## 3. PACKAGE_MANIFEST.json Requirements

`PACKAGE_MANIFEST.json` must include SHA256 for:

- the summary JSON,
- the flattened summary CSV,
- every raw `lm_eval_*` JSON,
- every stdout log included,
- every checkpoint metadata file included.

Suggested schema:

```json
{
  "package": "remote107_source_lock_20260520",
  "created_at": "2026-05-20T...",
  "remote_commit": "c7dd17e...",
  "hat_base_commit": "...",
  "summary_file": "remote107_paper2_results_summary_20260520.json",
  "files": [
    {
      "path": "raw_json/lm_eval_...json",
      "sha256": "...",
      "role": "source_json",
      "referenced_by_config": "pythia-6.9b/adaptive_cosine_last2",
      "referenced_by_task": "lambada_openai",
      "status": "present"
    }
  ],
  "known_gaps": []
}
```

## 4. source_json_inventory_20260520.csv Requirements

One row per raw source JSON. Required columns:

```text
source_json,sha256,model,config_name,analog_layers,schedule,train_steps,seed,eval_mode,tasks,exact_command,status,notes
```

`eval_mode` must be one of:

```text
clean,analog,other
```

## 5. checkpoint_inventory_20260520.csv Requirements

One row per checkpoint. Required columns:

```text
checkpoint_path,checkpoint_sha256_or_lfs_oid,model,config_name,analog_layers,schedule,train_steps,seed,exact_train_command,train_log_path,status,notes
```

Important:

- If the checkpoint file itself cannot be pushed, provide the LFS OID or SHA256 and exact path on Remote107.
- If multiple configs share the same checkpoint SHA256, state whether this is intentional.

## 6. Specific Reconciliation Questions

Please answer these in `README_PROTOCOL.md` or a separate `RECONCILIATION_20260520.md`.

### Q1. Where are `p69b adaptive_cosine_last2 PPL 11.29 vs 11.40`?

The commit message mentions these numbers, but Codex did not find them in `paper2_results_summary.json`.

Required response:

- source JSON filename,
- exact metric key,
- exact task/dataset,
- exact command,
- whether this is clean vs analog, analog vs digital, or a different benchmark from Lambada,
- whether the number should replace or coexist with the current Lambada PPL `5.175765 -> 5.344261`.

### Q2. Why does the commit message say 20 configs but JSON says 19?

Required response:

- identify missing config, or
- correct the commit/README wording to 19 configs.

### Q3. Why is `git_commit_hat` unknown?

Required response:

- provide exact HAT base commit,
- if unavailable, state why and mark all affected rows `PROVISIONAL`.

### Q4. Are main-text rows improvement claims or parity claims?

Codex computed negative average analog-vs-clean `delta_acc` for all main-text candidate rows in the pushed JSON.

Required response:

- confirm that main text should frame these as low-overhead/parity/selective-deployment results, not accuracy improvement,
- or provide source evidence for a different improvement metric.

## 7. Next Experiment Queue After Source Package Repair

Do **not** start broad new sweeps until R0 source repair is done. The next queue should be executed in order.

### R0 - Evidence Repair And Source Lock

Priority: P0
GPU: none or minimal

Deliver:

- package under `paper2/results/remote107/source_lock_20260520/`,
- fixed `paper2_results_summary.json` if needed,
- reconciliation answers Q1-Q4.

Stop condition:

- If Q1 cannot be reconciled, remove the `11.29 vs 11.40` claim from all summaries.

### R1 - 410M Mechanism Controls

Priority: P0
GPU: medium

Purpose: decide whether the observed gains are caused by HAT fine-tuning, analog patching, zero-noise quantization, or actual inference-time physical noise.

Run first on Pythia-410M because the existing 410M package is closest to claim-lock.

Layer sets:

```text
digital, last1, last2, last4, all24
```

Conditions:

```text
base_clean
patched_zero_noise_no_hat
hat_no_analog
hat_quant_zero_noise
hat_d2d_0p02
hat_d2d_0p05
```

Required output CSV:

```text
condition,model,checkpoint_id,layer_set,analog_layers,n_states,sigma_c2c,sigma_d2d,seed,ppl,nll,tokens,command,json_path,log_path
```

Decision rule:

- If `hat_no_analog` or `hat_quant_zero_noise` explains nearly all improvement, claim HAT/quantization regularization, not physical-noise benefit.
- If inference-time D2D improves over zero-noise consistently, keep physical-noise regularization as an active hypothesis.

### R2 - Attention Entropy / Sink Tracking

Priority: P1, only after R1 begins to clarify mechanism
GPU: medium

Metrics:

```text
normalized_entropy,top1_mass,BOS_or_first_token_sink_mass,effective_support,KL_vs_digital
```

Minimum conditions:

```text
base_clean
hat_quant_zero_noise_last2
hat_d2d_0p02_last2
hat_d2d_0p05_last2
all24_d2d_0p02_negative_control
```

Decision rule:

- If terminal layers show no entropy/sink movement, do not claim attention-collapse rescue.
- If selective terminal KV restores entropy while all24 damages it, the depth-localized story remains viable.

### R3 - KV Sensitivity / Curvature Probe

Priority: P1
GPU: medium/high but sampled

Probe:

- layers: last1, last2, last4, and sampled all24,
- perturbation scales: `1e-4`, `3e-4`, `1e-3`,
- 8-32 random probes depending on cost.

Required output CSV:

```text
condition,layer_idx,kv_kind,perturb_scale,probe_id,delta_nll,sensitivity,ppl,seed
```

Decision rule:

- If HAT/noise does not reduce terminal-layer KV sensitivity, do not claim curvature regularization.

### R4 - Larger-Model Minimal Recheck

Priority: P2, only after R0 and at least provisional R1
GPU: high

For pythia-2.8b and pythia-6.9b, run only the minimal control set:

```text
digital baseline
best selective layer set zero-noise
best selective layer set D2D=0.02
best selective layer set D2D=0.05
all-layer negative control if affordable
```

Goal:

- determine whether 410M mechanism generalizes,
- avoid huge broad sweeps before the mechanism is known.

### R5 - Optional Tau/Temperature Proxy

Priority: P3
Run only if R1-R3 support a physical-noise mechanism.

Hard wording rule:

- Use `temperature-like` only.
- Do not write `mathematically identical to softmax temperature`.

## 8. Required Status Return Format

After each queue stage, return a short Markdown report with this structure:

```text
# Remote107 Return - <stage> - <date>

## One-line Verdict

## Files Pushed

## Commands Run

## Key Results Table

## Source Integrity

## Open Gaps

## Recommended Next Action
```

## 9. Claim Boundary Until This Is Done

Safe wording now:

> Remote A100 evaluations suggest that selective terminal-layer analog KV can preserve downstream accuracy within a small margin under HAT-trained checkpoints, while all-layer analog KV remains the negative-control route. Larger-model results are currently provisional pending source-package lock and mechanism controls.

Unsafe wording now:

- `p69b cosine last2 improves PPL to 11.29 vs 11.40 digital`, unless Q1 is reconciled.
- `hardware noise improves LLM accuracy`, unless R1 zero-noise controls prove inference-time noise helps.
- `depth-adaptive physical regularization law`, unless R2/R3 support the mechanism.
- `20 configs complete`, unless Q2 is fixed.
