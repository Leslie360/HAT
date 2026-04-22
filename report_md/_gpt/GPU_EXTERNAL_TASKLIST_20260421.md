# GPU External Task List — 2026-04-21

Purpose:
- Offload the remaining or high-value GPU work to a faster external server (4x A100).
- Give an external coding agent enough detail to implement missing pieces, run the jobs, and return artifacts without reverse-engineering this repo.

Repo root:
- `/home/qiaosir/projects/compute_vit`

Ground rules:
- Do not edit frozen paper text while the live GPU loop is open:
  - `paper/00_abstract.md`
  - `paper/05_results.md`
  - `paper/06_discussion.md`
  - `paper/cover_letter*.md`
  - `report_md/_gpt/KIMI_REBUTTAL_MASTER_20260420.md`
  - `paper/thesis/chapter_5_*.tex`
- Put new GPU scripts under `scripts/_gpt/`
- Put logs under `logs/_gpt/`
- Put JSON under `report_md/_gpt/json_gpt/`
- Put CSV under `report_md/_gpt/csv_gpt/`
- Put short run summaries under `report_md/_gpt/`
- If code is changed, return a patch or git diff alongside the result files

Return package for every task:
- Exact command line used
- Full log file
- JSON result
- CSV result if applicable
- Short markdown summary
- Checkpoint path if training was involved
- Patch/diff if the agent wrote new code

Already completed locally — do not prioritize rerunning unless you want confirmation:
- `J1a` joint MLP-linear + Ensemble HAT full fresh-instance:
  - `report_md/_gpt/json_gpt/joint_mlp_linear_ensemble_hat_full_fresh.json`
  - result: `30.53 +/- 7.07%`
- `J1b` QKV-only linearization:
  - `report_md/_gpt/json_gpt/qkv_only_linearization.json`
  - result: best `26.37%`, final `10.18%`
- `J1c` full-attention linearization:
  - `report_md/_gpt/json_gpt/full_attn_linearization.json`
  - result: best `28.09%`, final `9.80%`
- `J2` heavy-tailed D2D preliminary summary exists:
  - `report_md/_gpt/json_gpt/cx_j2_results.json`
- `J3` temperature summary exists:
  - `report_md/_gpt/json_gpt/cx_j3_results.json`
- `J4` IR-drop summary exists:
  - `report_md/_gpt/json_gpt/cx_j4_results.json`
- `J5` cadence summary exists:
  - `report_md/_gpt/json_gpt/cx_j5_results.json`
- `J6` retention summary exists:
  - `report_md/_gpt/json_gpt/cx_j6_results.json`
- `J7` ADC floor summary exists:
  - `report_md/_gpt/json_gpt/cx_j7_results.json`
- `J8` ImageNet-100 pilot summary exists:
  - `report_md/_gpt/json_gpt/cx_j8_results.json`

## Tier A — Highest-value remaining GPU task

### A1. `CX-J1d-2` — second-order STE severe-NL diagnostic

Status:
- Currently running locally but slowly.
- This is the single most important unresolved GPU task.

Scientific question:
- Does a second-order surrogate break the severe-NL ceiling?
- Decision thresholds:
  - `< 35%`: structural-limit branch remains active
  - `35-50%`: ambiguous
  - `> 50%`: first-order surrogate is likely the bottleneck

Existing code:
- `scripts/_gpt/run_tinyvit_groupwise_nl_comp.py`
- This already supports:
  - `--use-second-order-ste`
  - `--delta-g-eff`
  - `--warm-start-from`

Canonical checkpoint:
- `checkpoints/V4_hybrid_standard_noise_hat_best.pt`

Recommended command:
```bash
python scripts/_gpt/run_tinyvit_groupwise_nl_comp.py \
  --protected-group mlp \
  --protected-nl-ltp 1.0 \
  --protected-nl-ltd -1.0 \
  --use-second-order-ste \
  --delta-g-eff 0.0 \
  --name-suffix _second_order_ste \
  --mode train \
  --dataset cifar10 \
  --experiments V4 \
  --epochs 100 \
  --batch-size 64 \
  --num-workers 0 \
  --device cuda \
  --pretrained \
  --amp \
  --nl-ltp 2.0 \
  --nl-ltd -2.0 \
  --warm-start-from checkpoints/V4_hybrid_standard_noise_hat_best.pt \
  --save-dir checkpoints/_gpt/second_order_ste \
  --log-interval 20 \
  --log-path logs/_gpt/cx_j1d_20260421.log \
  --results-json-path report_md/_gpt/json_gpt/second_order_ste.json \
  --results-csv-path report_md/_gpt/csv_gpt/second_order_ste.csv \
  --results-md-path report_md/_gpt/CODEX_SECOND_ORDER_20260421.md
```

Required outputs:
- `report_md/_gpt/json_gpt/second_order_ste.json`
- `report_md/_gpt/csv_gpt/second_order_ste.csv`
- `report_md/_gpt/CODEX_SECOND_ORDER_20260421.md`
- checkpoint best/last under `checkpoints/_gpt/second_order_ste/`

Required post-run interpretation:
- If possible, also run a 10x5 fresh-instance evaluation on the best checkpoint using the same protected-group config and return:
  - cross-instance mean
  - cross-instance std
  - per-instance raw accuracy list

## Tier B — High-value tasks that need code or extension

### B1. `CX-J1d-3` — third-order / cumulant surrogate

Status:
- Not implemented.
- This is the best follow-up if `J1d-2` is still ambiguous.

Theory reference:
- `report_md/_gpt/GEMINI_HIGHER_ORDER_NL_DESIGN_20260420.md`

What the external agent must do:
- Extend the analog-layer surrogate beyond the current second-order correction.
- Implement a third-order or cumulant-style correction in a new code path, not by overwriting the existing first/second-order behavior.

Suggested files:
- `analog_layers.py`
- `scripts/_gpt/run_tinyvit_groupwise_nl_comp.py`
- new report files under `_gpt/`

Expected deliverables:
- code diff
- training log
- JSON / CSV / MD summary
- best checkpoint
- fresh-instance evaluation summary

Success criterion:
- Clear answer to whether higher-order correction moves performance out of the `~30%` band.

### B2. `CX-J2` — heavy-tailed D2D full sweep

Status:
- Current script is only a stub:
  - `scripts/_gpt/eval_heavy_tailed_d2d.py`
- It explicitly raises `NotImplementedError`.

What the external agent must do:
- Implement `sample_heavy_tailed_d2d_mask()`
- Wire it into the same fresh-instance evaluation harness used for canonical V4 Ensemble HAT

Recommended scope:
- Families:
  - lognormal
  - student-t
  - truncated Pareto
- Suggested parameter sweep:
  - lognormal `sigma_log ∈ {0.1, 0.2, 0.3}`
  - Pareto `alpha ∈ {2.5, 3.0, 4.0}`
- Keep:
  - `fresh_instances = 10`
  - `eval_runs = 5`

Expected outputs:
- `report_md/_gpt/json_gpt/cx_j2_results_external.json`
- `report_md/_gpt/csv_gpt/cx_j2_results_external.csv`
- `report_md/_gpt/CODEX_CX_J2_EXTERNAL_SUMMARY.md`

### B3. `CX-J3` — temperature-drift Arrhenius full sweep

Status:
- We only have a lightweight summary JSON.
- No clean dedicated evaluation script is staged for external replay.

Existing code base to reuse:
- `train_tinyvit.py`
- `train_tinyvit_ensemble.py`
- retention and profile logic in `analog_layers.py`

Target protocol:
- Temperature set:
  - `-20, 0, 25, 50, 85 C`
- Activation energies:
  - `Ea ∈ {0.5, 0.8} eV`

What the external agent likely needs to write:
- a dedicated temperature-drift evaluator in `scripts/_gpt/`
- JSON/CSV/MD output layer matching the rest of the repo

Expected outputs:
- `report_md/_gpt/json_gpt/cx_j3_results_external.json`
- `report_md/_gpt/csv_gpt/cx_j3_results_external.csv`
- `report_md/_gpt/CODEX_CX_J3_EXTERNAL_SUMMARY.md`

### B4. `CX-J4` — IR-drop geometry full sweep

Status:
- We have summary numbers and legacy scripts.
- The clean rerun path is not standardized yet.

Existing code / references:
- `run_ir_drop_sensitivity_v3.py`
- archived references:
  - `_archive/scripts-versions/run_ir_drop_sensitivity.py`
  - `_archive/scripts-versions/run_ir_drop_sensitivity_v2.py`

Target protocol:
- Geometry:
  - `16x16`
  - `32x32`
- Same canonical Tiny-ViT V4 / CIFAR-10 evaluation basis

What the external agent should return:
- one clean, current script in `scripts/_gpt/`
- JSON / CSV / MD output
- exact mapping from geometry parameter to accuracy degradation

## Tier C — Code-ready but lower immediate priority

### C1. Joint warm-start full run (`CX-HB`)

Status:
- Optional, user-gated in the original plan.
- Worth running on 4xA100 only if you want a stronger answer on whether warm-start + joint mitigation can escape the `~30%` zone.

Existing artifacts:
- `report_md/_gpt/json_gpt/joint_mlp_linear_ensemble_hat_full.json`
- `report_md/_gpt/json_gpt/joint_mlp_linear_ensemble_hat_full_fresh.json`
- warm-start semantics were fixed in:
  - `train_tinyvit_ensemble.py`

Goal:
- Re-run or extend from the fixed warm-start path with more stable compute and clearer logging.

### C2. Retention-extended replay (`CX-J6` refinement)

Status:
- Existing summary exists, but an A100 box could cheaply rerun a denser time grid.

Existing code:
- `train_tinyvit_ensemble.py` already has retention sweep support
- `scripts/_gpt/retention_comparison_gpt.py` exists for uniform vs state-dependent comparison

Recommended added time grid:
- `0, 1s, 10s, 100s, 1e3s, 1e4s, 1e5s, 1 week, 1 month`

### C3. ADC floor refinement (`CX-J7` refinement)

Status:
- Existing summary exists.
- Lower value than `J1d/J2/J3/J4`.

Goal:
- Densify the bit sweep or add cross-instance uncertainty if needed.

## Tier D — Expensive optional work

### D1. ImageNet-100 pilot (`CX-HC` / `J8` refinement)

Status:
- Existing summary exists:
  - `report_md/_gpt/json_gpt/cx_j8_results.json`
- External 4xA100 box is a realistic place to do a cleaner rerun or small extension.

Existing code:
- `eval_imagenet_analog.py`
- `test_eval_imagenet_analog.py`
- `download_imagenet_val.py`
- `prepare_imagenet_val.py`

Recommended only if:
- `J1d` is finished
- and you want one more high-cost “future-facing” datapoint

Possible extensions:
- 2-3 seeds
- stronger logging
- split by top-1 / top-5 / calibration error

## What I would prioritize on the 4xA100 box

Priority 1:
- `A1` `CX-J1d-2` finish fast and clean

Priority 2:
- `B2` heavy-tailed D2D full implementation
- `B3` temperature-drift Arrhenius full evaluator
- `B4` IR-drop geometry clean rerun

Priority 3:
- `B1` third-order surrogate, but only if the external AI is strong enough to modify `analog_layers.py` safely

Priority 4:
- `D1` ImageNet-100 rerun

## Minimal package to send back to me

For each completed task, send:
- the exact command
- the new or modified script path
- the log path
- the JSON
- the CSV
- the short markdown summary
- the checkpoint path
- a unified diff if code was changed

That is enough for me to:
- verify correctness
- integrate the numbers
- update the reports and coordination ledger without rerunning the experiment locally
