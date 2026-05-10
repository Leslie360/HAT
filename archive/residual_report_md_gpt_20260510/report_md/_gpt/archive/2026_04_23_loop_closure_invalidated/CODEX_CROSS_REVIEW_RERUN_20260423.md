# Codex Cross-Review: Post-Fix Rerun Setup

**Project:** `compute_vit`
**Audit time:** 2026-04-23 23:02 CST (+0800)
**Reviewer:** Codex independent cross-review
**Scope:** Kimi Code CLI post-fix rerun setup for V4 Ensemble HAT, `NL_LTP=2.0`, `NL_LTD=-2.0`, epoch-resampled D2D.

## Executive Verdict

The active post-fix V4 training setup is using the corrected `analog_layers.py`, not `analog_layers_ensemble.py`. The core STE branch mapping and second-order correction in `analog_layers.py` are correct at `HEAD=33bed9cbb8ade7676d71074490ad45e68347950e`.

Current checkpoint metadata in `checkpoints/_gpt/postfix_reruns/` confirms:

- `epoch=8` in `V4_hybrid_standard_noise_hat_last.pt` at audit time.
- `best_epoch=7`, `best_acc=80.19`.
- `exp_cfg.nl_ltp=2.0`, `exp_cfg.nl_ltd=-2.0`.
- `exp_cfg.noise_enabled=True`, `sigma_c2c=0.05`, `sigma_d2d=0.1`, `hat_training=True`.
- `amp_enabled=True`.
- `model_state_dict` contains 42 `d2d_noise` buffers, matching the 42 analog modules built by `train_tinyvit_ensemble.py`.

No evidence was found that this second attempt is warm-starting from a pre-fix checkpoint. The command omitted `--resume-existing`, `--warm-start-from`, and `--pretrained`; source code only loads checkpoints when those flags are set.

The highest remaining risks are operational, not the fixed STE math:

1. `eval_fresh_instances_postfix.py` does not automatically read NL values from checkpoint metadata. It evaluates with correct NL only if called with `--nl-ltp 2.0 --nl-ltd -2.0`.
2. `eval_fresh_instances_postfix.py` builds/evaluates via `train_tinyvit.py`, not `train_tinyvit_ensemble.py`. This currently loads the V4 checkpoint and uses corrected `analog_layers.py`, but it is a needless cross-path dependency.
3. There are many stale historical V4 checkpoints elsewhere under `checkpoints/`. The post-fix save directory itself is clean, but any command using default `checkpoints/` or the wrong `--checkpoint` can silently evaluate old data.
4. `run_ensemble_hat_fixed.py` is still present and imports deprecated `analog_layers_ensemble.py`; it must not be used for this rerun.
5. The default `python` visible in this Codex shell is not the training Python. Use the absolute LLM interpreter or an activated LLM shell for all future commands.

## Evidence Collected

Repository state:

- `git rev-parse HEAD`: `33bed9cbb8ade7676d71074490ad45e68347950e`.
- `git show --stat --oneline HEAD -- analog_layers.py test_dual_bug_fix.py`: `33bed9c fix(analog_layers): second-order branch mapping must match first-order`; only `analog_layers.py` changed in that commit.
- Worktree is very dirty with many unrelated tracked and untracked report/script changes. I did not modify anything except this audit report.

Relevant hashes at audit time:

- `analog_layers.py`: `5bfe5fc8a2ecd30c8c46464a8978b7193b9b13b47a5860f414d41864e397bdff`
- `train_tinyvit_ensemble.py`: `27fe05164cc2b8d113e3a457e3f0c6bc557d6a2a159e2b0c9162d3b260e3ac9f`
- `eval_fresh_instances_postfix.py`: `ed2a89e71ed7e811fee8e1c760c4d37bb305bc00fc26694d2e3d3ccd6ce2a463`
- `train_tinyvit.py`: `06c27e5e7b71368e964c246a0957dc06525f9ecc839bc3dc3c978649dc46dff8`
- `inference_analysis_utils.py`: `fd985343a7a6a395094e83dbef542ace44194b3e169679566216ac25b8b156aa`
- `test_dual_bug_fix.py`: `d8ce81f1fa47c949aac767d916bdf462935b263d9a43a206da36d1ac532e41fc`

Verification commands run:

- `/home/qiaosir/miniconda3/envs/LLM/bin/python test_dual_bug_fix.py`: all 5 tests passed.
- `/home/qiaosir/miniconda3/envs/LLM/bin/python -c "py_compile.compile(...)"`: `analog_layers.py`, `train_tinyvit_ensemble.py`, and `eval_fresh_instances_postfix.py` compile.
- Direct numerical STE checks for `NL_LTP=2.0`, `NL_LTD=-2.0` matched expected branch behavior.
- Direct model-build check from `train_tinyvit_ensemble.py` produced 42 analog modules, all with `(NL_LTP, NL_LTD)=(2.0, -2.0)`, `noise_enabled=True`, `sigma_c2c=0.05`, `sigma_d2d=0.1`, `noise_mode='uniform'`.
- Direct D2D resampling check changed all 42 buffers.

Limitation:

- The Codex tool sandbox uses a separate PID namespace. `ps` only showed the commands launched by this audit, not the host-side Kimi training process. Live process environment therefore could not be inspected directly. Runtime evidence below comes from logs and checkpoint files.

## 1. Code Correctness Audit: `analog_layers.py`

Inspected lines: `analog_layers.py:227-288`.

### First-order branch mapping

Current code:

- `nl_ltp = abs(ctx.nl_ltp)`, `nl_ltd = abs(ctx.nl_ltd)` at lines 232-233.
- LTP scale uses `ltp_ratio = (x_max - x_clamped) / conductance_span` and `torch.pow(ltp_ratio, nl_ltp - 1.0)` at lines 248-250.
- LTD scale uses `ltd_ratio = (x_clamped - x_min) / conductance_span` and `torch.pow(ltd_ratio, nl_ltd - 1.0)` at lines 254-256.
- Branch selection is line 260:
  - `grad_output >= 0 -> grad_output * ltd_scale`
  - `grad_output < 0 -> grad_output * ltp_scale`

This matches the required physical mapping under gradient descent:

- Positive gradient means optimizer decreases weight, therefore LTD.
- Negative gradient means optimizer increases weight, therefore LTP.

### No extraneous NL multiplier

First-order code has no `nl_ltp *` or `nl_ltd *` prefactor. It is exactly `pow(ratio, nl - 1.0)`.

Second-order code also has no extraneous `nl` multiplier:

- LTP correction at line 272: `-0.5 * (nl_ltp - 1.0) * pow(...) * delta_g`
- LTD correction at line 277: `-0.5 * (nl_ltd - 1.0) * pow(...) * delta_g`

There is no `-0.5 * nl_ltp * (nl_ltp - 1.0)` or `-0.5 * nl_ltd * (nl_ltd - 1.0)` in the active file.

### Second-order branch mapping

Current code at lines 281-284:

- `grad_output >= 0 -> grad_output * ltd_corr`
- `grad_output < 0 -> grad_output * ltp_corr`

This maps the second-order correction to the same physical direction as first-order.

Direct numerical sanity check with `x_min=0`, `x_max=1`, `NL_LTP=2.0`, `NL_LTD=-2.0`, `delta_g_eff=0.1`, `alpha=1.0`:

| x | second order | grad_output +1 | grad_output -1 |
|---:|:---:|---:|---:|
| 0.1 | off | 0.1000 | -0.9000 |
| 0.5 | off | 0.5000 | -0.5000 |
| 0.9 | off | 0.9000 | -0.1000 |
| 0.1 | on | 0.0500 | -0.8500 |
| 0.5 | on | 0.4500 | -0.4500 |
| 0.9 | on | 0.8500 | -0.0500 |

The correction acts as a brake in the same branch direction. This is consistent with the post-fix intent.

### Active second-order status

The current V4 rerun command does not enable second-order STE. `AnalogLinearConfig.use_second_order_ste` defaults to `False`, and `train_tinyvit_ensemble.py` does not expose a CLI flag for it in this command. Therefore, the active V4 rerun exercises the corrected first-order path, not the second-order correction.

## 2. Training Configuration Audit

### Does `train_tinyvit_ensemble.py` use `analog_layers.py`?

Yes. `train_tinyvit_ensemble.py:33-41` imports:

- `AnalogConv2d`
- `AnalogLinear`
- `AnalogLinearConfig`
- `convert_to_hybrid`

all from `analog_layers`.

It does not import `analog_layers_ensemble.py`.

Warning: `run_ensemble_hat_fixed.py` still imports `analog_layers_ensemble.py` at line 27. It has a deprecation warning at lines 4-8, but also still contains contradictory text at line 26 saying `CRITICAL: Use analog_layers_ensemble, NOT analog_layers`. This script is hazardous and must not be used for post-fix results.

### Does NL override reach analog layers during training?

Yes for the active training path.

Source path:

- CLI args `--nl-ltp` and `--nl-ltd` are defined at `train_tinyvit_ensemble.py:1456-1459`.
- All experiment configs are overwritten at `train_tinyvit_ensemble.py:1488-1492`.
- `build_model()` passes those values into `AnalogLinearConfig` at `train_tinyvit_ensemble.py:257-260`.
- `set_noise_for_train()` re-pushes `module.config.NL_LTP` and `module.config.NL_LTD` every epoch/batch path at `train_tinyvit_ensemble.py:309-310`.
- `set_noise_for_eval()` re-pushes them for test evaluation at `train_tinyvit_ensemble.py:286-287`.

Direct build check:

- 42 analog modules.
- Unique NL config across all analog modules: `[(2.0, -2.0)]`.
- Unique noise config across all analog modules: `[(True, 0.05, 0.1, 'uniform')]`.

Checkpoint metadata independently confirms the CLI override landed:

- `exp_cfg.nl_ltp=2.0`
- `exp_cfg.nl_ltd=-2.0`

### Is epoch-resampled D2D happening each epoch?

Yes by source logic.

- `resample_all_d2d_noise()` is defined at `train_tinyvit_ensemble.py:627-634`.
- Training loop calls it at the start of every epoch if `exp_cfg.hat_training` is true at `train_tinyvit_ensemble.py:703-708`.
- V4 config has `hat_training=True` at `train_tinyvit_ensemble.py:118-122`.
- The log at `2026-04-23 22:53:51` says: `Ensemble HAT active: Resampled D2D mismatch for 42 analog modules.`
- Direct resampling test changed all 42 D2D buffers.

Note: the logger only prints the resample count for the first epoch (`epoch == start_epoch`). Subsequent epoch resampling happens silently by source logic. For safety-critical monitoring, add a lightweight checkpoint-side or log-side counter in future runs if explicit per-epoch proof is required.

### From scratch or warm-start?

From source and logs, this run is from scratch.

Reasons:

- `--resume-existing` was not in the user-specified command.
- `--warm-start-from` was not in the user-specified command.
- `--pretrained` was not in the user-specified command.
- `maybe_resume_experiment()` only selects a resume checkpoint if `warm_start_from is not None` or `resume_existing=True` at `train_tinyvit_ensemble.py:551-563`.
- Log contains no `Resuming from:` line and no `Warm-start mode:` line.
- First crashed attempt failed before any checkpoint save; current post-fix directory contains only the two active files, now overwritten by the successful second attempt.

Residual risk:

- `checkpoint_is_compatible()` checks dataset and class count, but not `exp_cfg` values such as NL/noise/hat/second-order. If someone later uses `--resume-existing` in a mixed directory, a semantically wrong checkpoint can be resumed if shape-compatible.

### AMP status and custom autograd risk

AMP is enabled in the active run:

- Training log: `AMP requested: True, active: True`.
- Checkpoint metadata: `amp_enabled=True`.
- `create_grad_scaler()` is called at `train_tinyvit_ensemble.py:673`.
- `train_one_epoch()` uses `autocast_context()` for forward/loss and `GradScaler` for backward/step at `train_tinyvit_ensemble.py:424-434`.

Analog-layer AMP handling is reasonable:

- Quantization-sensitive weight-to-conductance code enters `autocast_disabled_context()` and casts weights to float32 in both `AnalogLinear` and `AnalogConv2d` (`analog_layers.py:471-491`, `analog_layers.py:712-723`).
- The custom autograd function receives scaled `grad_output` under GradScaler, applies deterministic scale factors, and returns only `grad_input`. This is compatible with loss scaling in principle.

Remaining AMP risks:

- I could not run a GPU/AMP micro-test inside this sandbox because CUDA is not visible here.
- The run has already produced epoch checkpoints through epoch 8 without an immediate AMP/autograd crash, which is practical evidence but not a proof of numerical safety.
- Monitor for NaN/Inf in losses, sudden accuracy collapse, or GradScaler instability. The current logs do not expose scaler values.

### `torch.compile` status

The first attempt failed with `torch.compile` due to a CUDAGraphs/attention bias cache error in `timm.models.tiny_vit.py`.

The second attempt log has no `torch.compile enabled` line, consistent with removing `--compile`. Keep `--compile` off for this model unless `timm` attention-bias caching is patched or CUDAGraph capture is explicitly disabled.

## 3. Evaluation Script Audit: `eval_fresh_instances_postfix.py`

### Does it load post-fix checkpoints?

It requires an explicit `--checkpoint` at line 61 and passes that path as the positional `checkpoint_path` argument to `load_model_bundle()` at lines 74-78. This is good. It will load the post-fix checkpoint if and only if the caller supplies the exact post-fix path.

Direct load check:

- Loaded `checkpoints/_gpt/postfix_reruns/V4_hybrid_standard_noise_hat_best.pt`.
- Bundle saw `checkpoint_epoch=7`, `checkpoint_best_acc=80.19` at the time of that test.
- Analog module count after load: 42.

### Does it use correct NL values?

Conditionally.

The script supports `--nl-ltp` and `--nl-ltd` at lines 67-68 and mutates `bundle.exp_cfg` at lines 18-22. During actual evaluation, `run_mc_eval()` calls `evaluate_once()`, which calls `train_tinyvit.evaluate()`, which calls `set_noise_for_eval()` and pushes `cfg.nl_ltp/cfg.nl_ltd` into every analog layer.

Direct check:

- Initial bundle modules after loading had NL `(1.0, -1.0)` because `inference_analysis_utils.py` builds the model from default `train_tinyvit.py` configs, not checkpoint metadata.
- After setting `bundle.exp_cfg.nl_ltp=2.0`, `bundle.exp_cfg.nl_ltd=-2.0`, and calling `set_noise_for_eval()`, all modules had `(2.0, -2.0)`.

Important risk:

- If `eval_fresh_instances_postfix.py` is run without `--nl-ltp 2.0 --nl-ltd -2.0`, it will evaluate the post-fix NL=2 checkpoint with default evaluator NL `(1.0, -1.0)`. That would be invalid.
- Safer fix for future: load `ckpt["exp_cfg"]["nl_ltp"]` and `ckpt["exp_cfg"]["nl_ltd"]` by default, then allow CLI overrides only if explicitly supplied.

### Does fresh D2D resampling work correctly?

Yes.

- For each instance, the script sets deterministic seeds at lines 31-33.
- It calls `set_uniform_noise(..., resample_d2d=True, noise_mode=cfg.noise_mode)` at lines 35-36.
- `set_uniform_noise()` calls `resample_d2d_buffers(model)` when `resample_d2d=True` (`inference_analysis_utils.py:162-173`).
- `resample_d2d_buffers()` iterates over `AnalogLinear` and `AnalogConv2d` only and calls `module.resample_d2d_noise()` (`analog_layers.py:1333-1344`).

This produces one fixed D2D realization per instance, then `mc_runs_per_instance` evaluations use C2C randomness per forward. That matches the intended 10 fresh D2D instances x 5 MC evaluations protocol.

### Evaluation path mismatch

`eval_fresh_instances_postfix.py` imports `load_model_bundle()` from `inference_analysis_utils.py`. For `model_type="tinyvit"`, that utility uses `train_tinyvit.py` for `build_model`, `evaluate`, and dataloaders (`inference_analysis_utils.py:45-50`, `326-373`), not `train_tinyvit_ensemble.py`.

Current impact:

- For V4, `train_tinyvit.py` also imports corrected `analog_layers.py` and successfully loads the post-fix checkpoint.
- The architecture and state_dict are compatible in the direct load check.

Risk:

- This is an unnecessary split-brain path for a safety-critical post-fix run. If `train_tinyvit_ensemble.py` and `train_tinyvit.py` diverge later, fresh evaluation can silently stop matching training.
- Recommended future hardening: make the post-fix evaluator import `build_model`, `evaluate`, `get_dataloaders`, and configs from `train_tinyvit_ensemble.py`, or add an explicit loader mode.

### Evaluation AMP

`eval_fresh_instances_postfix.py` has no `--amp` flag and does not pass `amp_enabled=True` into `load_model_bundle()`. Therefore fresh-instance evaluation defaults to full precision.

This is not inherently wrong, and may be safer for final reporting, but it means fresh eval will not exactly match the inline training-loop test evaluation, which used AMP. Record this distinction in result metadata.

## 4. Data Integrity Audit

### Post-fix save directory

`checkpoints/_gpt/postfix_reruns/` contained only:

- `V4_hybrid_standard_noise_hat_best.pt`
- `V4_hybrid_standard_noise_hat_last.pt`

At audit time, `last.pt` metadata:

- mtime: `2026-04-23 23:01:57 CST`
- `epoch=8`
- `best_epoch=7`
- `best_acc=80.19`
- history length: 9 epochs
- latest train acc: `85.916`
- latest test acc: `79.13`
- latest lr: `0.0004921457902821577`

This directory is clean.

### Stale checkpoints elsewhere

There are many older V4 checkpoint files under:

- `checkpoints/`
- `checkpoints/_ensemble/`
- `checkpoints/_gpt/...`
- `checkpoints/gm_e4_nl_scan/...`
- `checkpoints/_gpt/cx_k3_dgeff/...`
- `checkpoints/_gpt/cx_k4_alpha/...`
- multiple other historical experiment directories

These are not in the active save directory, but they are a major operational hazard if any command uses default `--save-dir checkpoints`, default `--checkpoint-dir checkpoints`, or a stale hard-coded path.

For post-fix evaluation, always use:

```bash
/home/qiaosir/miniconda3/envs/LLM/bin/python eval_fresh_instances_postfix.py \
  --checkpoint checkpoints/_gpt/postfix_reruns/V4_hybrid_standard_noise_hat_best.pt \
  --exp-id V4 \
  --model-type tinyvit \
  --nl-ltp 2.0 \
  --nl-ltd -2.0 \
  --num-instances 10 \
  --mc-runs 5
```

### Python bytecode cache

Relevant Python 3.11 bytecode status:

- `analog_layers.py` mtime: `2026-04-23 12:28:23 +0800`
- `__pycache__/analog_layers.cpython-311.pyc` mtime: `2026-04-23 12:29:27 +0800`
- `train_tinyvit_ensemble.py` source is older than its Python 3.11 pyc.
- `train_tinyvit.py` source is older than its Python 3.11 pyc.
- `inference_analysis_utils.py` source is older than its Python 3.11 pyc.

For the Python 3.11 LLM environment, cache state is not stale for the active files.

There are older Python 3.12/3.13 pyc files, including a stale-looking `analog_layers.cpython-312.pyc` and many historical pycache files. Standard Python timestamp invalidation should recompile them if those interpreters are used, but for safety-critical reproducibility, clearing `__pycache__/` before final archival evaluation is reasonable.

### Documentation discrepancy found

`report_md/_gpt/BROADCAST_RERUN_DECISION_20260423.md` lines 16-18 describe the branch-swap bug in wording that conflicts with the current verified mapping. The broadcast says the bug was `grad_output >= 0` mapped to `ltd_scale` instead of `ltp_scale`; the current required and tested mapping is `grad_output >= 0 -> LTD -> ltd_scale`.

This appears to be stale/incorrect explanatory wording in the broadcast, not an active code problem. It should be corrected or annotated to prevent future confusion.

## 5. Environment Verification

Training log evidence:

- Runtime device: `cuda`.
- AMP: requested and active.
- Traceback and warnings path: `/home/qiaosir/miniconda3/envs/LLM/lib/python3.11/site-packages/...`.
- This strongly indicates the Kimi-launched training used the LLM conda environment.

Codex shell evidence:

- `which python` in this audit shell: `/home/qiaosir/.hermes/hermes-agent/venv/bin/python`.
- That default Python has no `torch`.
- Direct LLM interpreter: `/home/qiaosir/miniconda3/envs/LLM/bin/python`.
- LLM interpreter version: Python 3.11.6.
- LLM torch version: `2.10.0+cu128`.
- In the Codex sandbox, `torch.cuda.is_available()` reports `False`; this is a sandbox visibility limitation, while the training log reports CUDA.
- Direct import from LLM interpreter resolves:
  - `analog_layers` -> `/home/qiaosir/projects/compute_vit/analog_layers.py`
  - `train_tinyvit_ensemble` -> `/home/qiaosir/projects/compute_vit/train_tinyvit_ensemble.py`

PATH risk:

- Do not rely on bare `python` unless the shell is known to have the LLM env activated.
- Prefer absolute interpreter paths in all rerun/eval commands:
  - `/home/qiaosir/miniconda3/envs/LLM/bin/python ...`

Conda env var caveat:

- When directly invoking the LLM interpreter from this shell, `sys.prefix` is the LLM env, but `CONDA_DEFAULT_ENV` and `CONDA_PREFIX` still reflect the outer shell (`base`/root conda). For provenance, record `sys.executable` and `sys.prefix`, not only conda env vars.

## 6. What Could Still Go Wrong

### High-risk operational issues

1. Fresh evaluation can silently use wrong NL values if `--nl-ltp 2.0 --nl-ltd -2.0` are omitted.
2. Future resume commands can load shape-compatible but semantically wrong checkpoints because compatibility checks do not validate NL/noise/HAT/second-order config.
3. Stale V4 checkpoints in other directories can be accidentally evaluated if an explicit checkpoint path is not used.
4. `run_ensemble_hat_fixed.py` remains a footgun because it imports `analog_layers_ensemble.py`.
5. `eval_fresh_instances_postfix.py` uses `train_tinyvit.py` rather than the training script path.

### Medium-risk technical issues

1. AMP appears configured correctly, but GPU AMP with the custom STE was not independently executable inside this sandbox.
2. `torch.compile` is known-bad for this setup due the TinyViT attention bias cache/CUDAGraphs issue. Keep it disabled.
3. Logs only report epochs 0, 19, 39, 59, 79, 99 with `--log-interval 20`. If the run degrades between log points, the checkpoint history is the only detailed record.
4. Checkpoint metadata stores `amp_enabled=True`, but fresh evaluator defaults to no AMP. This should be explicitly recorded when comparing inline test accuracy to fresh-instance evaluation.
5. The broadcast document contains branch-mapping wording that conflicts with the fixed code and tests.

### Low-risk/code hygiene issues

1. `eval_fresh_instances_postfix.py` imports `get_v_experiment_configs` but does not use it.
2. `analog_layers.py` has `from typing import Union` before the shebang. It is not operationally relevant because this file is imported, not executed.
3. Multiple old pycache files exist for other Python versions.

## 7. What To Monitor During The 100-Epoch Run

Monitor every few epochs by reading checkpoint metadata, not only logs:

- `last.pt` mtime should keep advancing.
- `epoch` should monotonically increase to 99.
- `history` list lengths should equal `epoch + 1`.
- `exp_cfg` must remain:
  - `nl_ltp=2.0`
  - `nl_ltd=-2.0`
  - `noise_enabled=True`
  - `sigma_c2c=0.05`
  - `sigma_d2d=0.1`
  - `hat_training=True`
  - `epochs=100`
  - `batch_size=64`
- `amp_enabled` should remain `True`.
- `model_state_dict` should continue to contain 42 `d2d_noise` buffers.
- Train/test loss must remain finite.
- Watch train/test gap. A rapidly rising train accuracy with falling test accuracy may indicate overfitting to the stochastic training distribution.
- Confirm no new `torch.compile` crash log appears.

Suggested lightweight monitor command:

```bash
/home/qiaosir/miniconda3/envs/LLM/bin/python - <<'PY'
import os, time, torch
path = "checkpoints/_gpt/postfix_reruns/V4_hybrid_standard_noise_hat_last.pt"
ckpt = torch.load(path, map_location="cpu", weights_only=False)
h = ckpt.get("history") or {}
print("mtime", time.strftime("%Y-%m-%d %H:%M:%S %Z %z", time.localtime(os.path.getmtime(path))))
print("epoch", ckpt.get("epoch"), "best_epoch", ckpt.get("best_epoch"), "best_acc", ckpt.get("best_acc"))
print("exp_cfg", {k: (ckpt.get("exp_cfg") or {}).get(k) for k in ["nl_ltp","nl_ltd","sigma_c2c","sigma_d2d","noise_enabled","hat_training","epochs","batch_size"]})
print("history_lengths", {k: len(v) for k, v in h.items() if isinstance(v, list)})
if h.get("test_acc"):
    print("last", {k: h[k][-1] for k in ["train_loss","train_acc","test_loss","test_acc","lr"]})
print("d2d_buffers", sum(1 for k in (ckpt.get("model_state_dict") or {}) if k.endswith("d2d_noise")))
PY
```

## 8. Immediate Post-Training Validation

Do these before any manuscript number is updated.

1. Freeze provenance:
   - Record `git rev-parse HEAD`.
   - Record `git status --short`.
   - Record SHA256 hashes for `analog_layers.py`, `train_tinyvit_ensemble.py`, `eval_fresh_instances_postfix.py`, `train_tinyvit.py`, `inference_analysis_utils.py`.
   - Archive the exact launch command and logs.

2. Verify checkpoint metadata:
   - `epoch=99`.
   - `best_epoch` and `best_acc` present.
   - `exp_cfg.nl_ltp=2.0`, `exp_cfg.nl_ltd=-2.0`.
   - `amp_enabled=True`.
   - 42 `d2d_noise` buffers.
   - All history values finite.

3. Re-run code tests in the LLM environment:
   - `/home/qiaosir/miniconda3/envs/LLM/bin/python test_dual_bug_fix.py`
   - Optional: a no-training model-build smoke check that all analog modules have `(2.0, -2.0)`.

4. Same-instance eval:
   - Run `train_tinyvit_ensemble.py --mode eval` against the post-fix `best.pt`, with explicit `--nl-ltp 2.0 --nl-ltd -2.0`.
   - Run once with no AMP and optionally once with `--amp` to quantify AMP/no-AMP eval drift.

5. Fresh-instance eval:
   - Use the explicit command in Section 4 with `--checkpoint checkpoints/_gpt/postfix_reruns/V4_hybrid_standard_noise_hat_best.pt --nl-ltp 2.0 --nl-ltd -2.0`.
   - Record `num_instances=10`, `mc_runs=5`, seed convention, checkpoint path, checkpoint epoch, code hashes, and whether eval used AMP.

6. Validate evaluator config before accepting results:
   - Print or assert module NL after `set_noise_for_eval()`.
   - Print or assert fresh D2D resample count is 42 per instance.
   - Ensure output JSON contains checkpoint path and NL values.

7. Only then compare against R1 standard HAT and any structural-limit reruns.

## Final Assessment

The current post-fix training run is valid to continue, provided the command truly remains the no-compile, no-resume V4 command and the checkpoint metadata continues to match the audited values.

The corrected STE math in `analog_layers.py` is not the weak point now. The weak points are provenance discipline and evaluation-path discipline. The final fresh-instance result is only valid if evaluated from the post-fix checkpoint with explicit `NL_LTP=2.0`, `NL_LTD=-2.0`, corrected `analog_layers.py`, fresh D2D resampling, and no accidental fallback to stale checkpoint directories or deprecated `analog_layers_ensemble.py` scripts.
