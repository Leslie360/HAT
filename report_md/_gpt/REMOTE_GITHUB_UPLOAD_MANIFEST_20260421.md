# Remote GitHub Upload Manifest — 2026-04-21

Purpose:
- Minimal, safe package for a remote GPU server to clone from GitHub.
- Enough to run exploratory experiments and inspect context.
- Avoid shipping obviously private or irrelevant trees.

## Must include

Repository root files:
- `README.md`
- `LICENSE`
- `environment.yml`
- `requirements.txt`
- `requirements-optional.txt`

Core code:
- `analog_layers.py`
- `analog_layers_ensemble.py`
- `inference_analysis_utils.py`
- `device_profile_utils.py`
- `physical_noise_pipeline.py`
- `train_tinyvit.py`
- `train_tinyvit_ensemble.py`
- `train_convnext.py`
- `train_resnet18.py`
- `eval_measured_profile.py`
- `eval_imagenet_analog.py`

Scripts:
- `scripts/_gpt/run_tinyvit_groupwise_nl_comp.py`
- `scripts/_gpt/eval_joint_fresh_instance.py`
- `scripts/_gpt/eval_spatially_correlated_d2d.py`
- `scripts/_gpt/eval_heavy_tailed_d2d.py`
- any helper script directly imported by these

Experiment context:
- `report_md/_gpt/INDEX.md`
- `report_md/_gpt/AGENT_SYNC_gpt.md`
- `report_md/_gpt/GPU_REMOTE_EXPLORATION_BRIEF_20260421.md`
- `report_md/_gpt/GPU_EXTERNAL_TASKLIST_20260421.md`
- `docs/REMOTE_SERVER_GITHUB_HANDOFF.md`

Small result priors:
- selected JSON only from `report_md/_gpt/json_gpt/`
- recommended:
  - `qkv_only_linearization.json`
  - `full_attn_linearization.json`
  - `joint_mlp_linear_ensemble_hat_full_fresh.json`
  - `cx_j2_results.json`
  - `cx_j3_results.json`
  - `cx_j4_results.json`
  - `cx_j5_results.json`
  - `cx_j6_results.json`
  - `cx_j7_results.json`
  - `cx_j8_results.json`

Optional but useful:
- `paper/paper2/skeleton_v0/`
- `paper/thesis_cn/` if the remote AI also helps with non-GPU thesis drafting

## Must exclude

Do not upload these to the remote GitHub repo/branch:
- `_archive/`
- `logs/`
- `outputs/`
- `数据_博士/`
- large local `checkpoints/`
- full `report_md/` if it contains bulky internal materials
- LaTeX build products

If checkpoints are needed:
- upload only the specific small subset the remote experiments require
- or instruct the remote AI to start from code-first exploration and return markdown-only guidance

## Minimal baseline statement to include in the repo description

> This repository is being mirrored to a remote GPU server for exploratory route-finding only. The remote side should use the included scripts and small prior-result JSON files to identify the most informative next experiments. Final locked manuscript numbers will be reproduced locally.

## Upload strategy

Recommended:
1. Create a dedicated GitHub branch or mirror for remote exploration.
2. Include only the allowlisted files above.
3. Point the remote AI first to:
   - `docs/REMOTE_SERVER_GITHUB_HANDOFF.md`
   - `report_md/_gpt/GPU_REMOTE_EXPLORATION_BRIEF_20260421.md`

## What the remote side should send back

Only small text artifacts:
- markdown experiment reports
- short diff snippets
- compact tables of key numbers

No need to send back:
- full checkpoints
- huge logs
- full datasets
