# Claude Task Handoff — compute_vit Paper1–4 数据推进

更新时间：2026-05-11 22:05

本文件同步自 `/home/qiaosir/projects/compute_vit/task.md` 和当前广播。当前核心目标不是 thesis 定稿，而是持续获取实验数据与结果，支撑 Paper1/Paper2/Paper3/Paper4。执行新任务前优先读取根目录 `task.md`、`coordination/active/NEXT_WORK_MASTER_TASKLIST_20260510.md` 和 `/home/qiaosir/projects/BROADCAST.md`。

## 最高优先级

1. Retention × protection 10×3 expansion completed; GPU is free for the next lane only after a fresh `nvidia-smi` check.
2. 继续维护 canonical evidence ledger：`report_md/_gpt/CANONICAL_EVIDENCE_LEDGER_20260510.md`。
3. 保持 Paper2/107 evidence boundary：只用 2026-05-11 Remote107 claim-lock package 做 claim-bearing 表/图。
4. CIFAR-100 seed456/seed789 remain provisional multi-seed expansion evidence; current Paper3 wording should mention cross-seed variance and avoid a closed canonical mean.
5. 107-clean 最新推送已审阅：`origin/107-clean` 到 `19038b2`，Qwen3-VL/2.8B/6.9B 属于 active validation/scale-up lane；当前 Paper2 claim-bearing 仍只用 2026-05-11 Remote107 410M claim-lock package。

## 当前运行中 GPU 任务

None. Retention × protection 10×3 completed on 2026-05-11; run `nvidia-smi` before launching any new GPU lane.

## Completed GPU experiments and CPU review

### Retention × protection 10×3 expansion
- Completed on 2026-05-11 using CIFAR-100 Tiny-ViT V4 Ensemble HAT seed789 checkpoint, full test set, 10 fresh D2D instances × 3 MC, protected K in {0,30,42}, and retention times {0,1000,10000}s.
- Retention settings: `--recalibrate_scale --scale_d2d`.
- Summary: at 0s fresh/top30/top42 = `58.223±1.386%` / `62.051±0.587%` / `62.248±0.510%`; at 1000s = `55.596±1.229%` / `59.207±0.608%` / `59.392±0.605%`; at 10000s = `55.403±1.272%` / `59.223±0.606%` / `59.391±0.482%`.
- Outputs: `thesis/results/retention_protection/retention_protection_10x3_20260511_223530.tsv`, `thesis/results/retention_protection/retention_protection_summary_10x3_20260511_223530.tsv`, `thesis/results/retention_protection/retention_protection_plot_source_10x3_20260511_223530.tsv`, and `thesis/figures/retention_protection/fig_retention_protection_10x3_20260511.png/.pdf`.
- Script/log: `scripts/eval_retention_protection_sweep.py`, `scripts/plot_retention_protection.py`, `logs/local_gpu_retention_protection_10x3_20260511_223530.log`, `logs/plot_retention_protection_10x3_20260511_231000.log`.
- Evidence status: provisional simulator-default retention model only, not measured retention or refresh/energy/endurance closure.

### Retention × protection pilot
- Completed on 2026-05-11 using CIFAR-100 Tiny-ViT V4 Ensemble HAT seed789 checkpoint, full test set, 3 fresh D2D instances × 2 MC, protected K in {0,30,42}, and retention times {0,1000,10000}s.
- Retention settings: `--recalibrate_scale --scale_d2d`.
- Summary: at 0s fresh/top30/top42 = `59.035±1.101%` / `61.883±0.142%` / `62.028±0.272%`; at 1000s = `56.008±0.971%` / `59.180±0.149%` / `59.263±0.036%`; at 10000s = `56.298±0.748%` / `59.180±0.087%` / `59.360±0.194%`.
- Outputs: `thesis/results/retention_protection/retention_protection_pilot_20260511_222510.tsv`, `thesis/results/retention_protection/retention_protection_pilot_summary_20260511_222510.tsv`.
- Script/log: `scripts/eval_retention_protection_sweep.py`, `logs/local_gpu_retention_protection_pilot_20260511_222510.log`.
- Evidence status: provisional; simulator-default retention model only, not measured retention or refresh/energy closure.

## Completed GPU experiments and CPU review

### Spatial variance / floorplan-aware mapping 10×3 expansion
- Completed on 2026-05-11 using CIFAR-100 Tiny-ViT V4 Ensemble HAT seed789 checkpoint, full test set, batch size 128, 10 synthetic D2D instances × 3 C2C MC, and four mapping strategies: sequential, random, sensitivity-aware, worst-case.
- Summary: sensitivity-aware `50.9413±1.6904%`, random `46.7020±2.2885%`, worst-case `42.5790±3.5225%`, sequential `39.3353±2.9631%`.
- Interpretation: sensitivity-aware beats random by `+4.24` pp and worst-case by `+8.36` pp under this synthetic stress profile. Keep as provisional synthetic floorplan evidence, not measured floorplan evidence.
- Outputs: `thesis/results/spatial_variance/spatial_variance_mapping_10x3_20260511_220730.tsv`, `thesis/results/spatial_variance/spatial_variance_mapping_summary_10x3_20260511_220730.tsv`, `thesis/results/spatial_variance/tile_profiles_10x3_20260511_220730.json`, and `thesis/results/spatial_variance/mapping_specs_10x3_20260511_220730.tsv`.
- Log: `logs/local_gpu_spatial_variance_10x3_20260511_220730.log`.
- Note: this run was launched before the later metadata-only script refinement, so raw rows lack `strategy_seed`, `mapping_seed`, `noise_mode`, and `script` columns; the command/log/output paths still define the run, and future reruns include those columns.

## Recently completed

### Spatial variance / floorplan-aware mapping 3×2 pilot — 2026-05-11 22:02
- Pilot completed on CIFAR-100 seed789 Ensemble HAT with full test set, synthetic good/nominal/weak/bad tile profiles, and four layer-to-tile mapping strategies.
- Summary: sensitivity-aware `50.7067±0.2959%`, random `47.6683±0.5025%`, worst-case `43.9933±2.2602%`, sequential `37.7667±3.8579%`.
- Outputs: `thesis/results/spatial_variance/spatial_variance_mapping_pilot_20260511_220238.tsv`, `thesis/results/spatial_variance/spatial_variance_mapping_pilot_summary_20260511_220238.tsv`, `thesis/results/spatial_variance/tile_profiles_20260511_220238.json`, `thesis/results/spatial_variance/mapping_specs_20260511_220238.tsv`.
- Log: `logs/local_gpu_spatial_variance_pilot_20260511_220238.log`.
- Evidence status: provisional synthetic floorplan stress evidence; expand to 10×3 before thesis/Paper3 claim use.

### CIFAR-100 Ensemble HAT seed789 train + source + fresh-instance eval
- Training finished at 2026-05-11 21:35.
- Best checkpoint: `checkpoints/_ensemble/cifar100_seed789/V4_hybrid_standard_noise_hat_best.pt`.
- Training best accuracy: `65.05%` at epoch 88.
- Source-domain eval: `65.07±0.16%` over 3 eval runs.
- Fresh-instance 10×3 summary: `fresh_all_analog=58.002±1.686%`, `freeze_top20_d2d=61.822±0.859%`, `freeze_top30_d2d=62.037±0.926%`, `freeze_top42_d2d=62.131±0.985%`.
- Source eval outputs: `thesis/results/mixed_precision/cifar100_ensemble_hat_seed789_source_eval_20260511_213615.json/.csv` and `report_md/_gpt/CIFAR100_ENSEMBLE_HAT_SEED789_SOURCE_EVAL_20260511_213615.md`.
- Fresh-instance outputs: `thesis/results/mixed_precision/fresh_instance_protection_maps_cifar100_ensemble_hat_seed789_10x3_20260512.tsv`, `thesis/results/mixed_precision/fresh_instance_protection_maps_cifar100_ensemble_hat_seed789_combined_10x3_20260512.tsv`, and `thesis/results/mixed_precision/fresh_instance_protection_maps_cifar100_ensemble_hat_seed789_summary_10x3_20260512.tsv`.
- Logs: `logs/cifar100_ensemble_hat_seed789_20260511_202459.log`, `logs/cifar100_ensemble_hat_seed789_source_eval_20260511_213615.log`, `logs/cifar100_ensemble_seed789_fresh_instance_eval_20260511_213655.log`, `logs/cifar100_ensemble_seed789_summary_10x3_20260511_214930.log`.
- Evidence status: seed789 is provisional multi-seed expansion evidence. It remains far above fixed-mask fresh collapse but below seed456, so current Paper3 wording should mention cross-seed variance and avoid promoting a closed canonical mean.

### CIFAR-100 Ensemble HAT seed789 post-train eval plan
- Completed on 2026-05-11. Raw TSV has 120 rows plus header.
- Source-domain eval completed at `65.07±0.16%` over 3 runs.
- Corrected fresh-instance 10×3 completed with summary `fresh_all_analog=58.002±1.686%`, `freeze_top20_d2d=61.822±0.859%`, `freeze_top30_d2d=62.037±0.926%`, `freeze_top42_d2d=62.131±0.985%`.
- Evidence status after success: seed789 is multi-seed expansion evidence; do not promote to canonical until the agreed final seed count/protocol is closed.

## Recently completed

### Paper2 draft polish + XJTU format check — 2026-05-11 21:10
- Paper2 draft `paper2/manuscript/paper2_figure_led_draft_20260511.tex` has been tightened around a claim-first title/central claim, layer-scope framing, explicit evidence-boundary table, and bounded contributions/limits wording.
- Paper2 README now separately records the active draft and the claim-bearing source-data package `paper2/manuscript/source_data/remote107_selective_kv_claim_lock_20260511/`.
- XJTU submission lane `thesis/xjtu_submission/main.tex` no longer loads unused `subcaption`; `XJTU_FORMAT_AUDIT_20260510.md` records that the old `Unused \captionsetup[sub]` warning is cleared. Remaining warnings are font and bibliography/long-token line-breaking plus deferred formal metadata.
- No new GPU/Python job was started during this CPU-only polish/check pass.

### CIFAR-100 Ensemble HAT seed456 train + source + fresh-instance eval
- Training finished at 2026-05-11 18:54.
- Best checkpoint: `checkpoints/_ensemble/cifar100_seed456/V4_hybrid_standard_noise_hat_best.pt`.
- Training best accuracy: `66.69%` at epoch 94.
- Source-domain eval: `66.66±0.03%` over 3 eval runs.
- Fresh-instance 10×3 summary: `fresh_all_analog=63.744±0.514%`, `freeze_top20_d2d=64.786±0.483%`, `freeze_top30_d2d=64.829±0.531%`, `freeze_top42_d2d=64.974±0.538%`.
- Source eval outputs: `thesis/results/mixed_precision/cifar100_ensemble_hat_seed456_source_eval_20260511_195630.json/.csv` and `report_md/_gpt/CIFAR100_ENSEMBLE_HAT_SEED456_SOURCE_EVAL_20260511_195630.md`.
- Fresh-instance outputs: `thesis/results/mixed_precision/fresh_instance_protection_maps_cifar100_ensemble_hat_seed456_10x3_20260511.tsv`, `thesis/results/mixed_precision/fresh_instance_protection_maps_cifar100_ensemble_hat_seed456_combined_10x3_20260511.tsv`, and `thesis/results/mixed_precision/fresh_instance_protection_maps_cifar100_ensemble_hat_seed456_summary_10x3_20260511.tsv`.
- Logs: `logs/cifar100_ensemble_hat_seed456_20260511_174359.log`, `logs/cifar100_ensemble_hat_seed456_source_eval_20260511_195630.log`, `logs/cifar100_ensemble_seed456_fresh_instance_eval_20260511_195715.log`, `logs/cifar100_ensemble_seed456_summary_10x3_20260511_201015.log`.
- Evidence status: seed456 alone is provisional; seed123+seed456 together are still multi-seed expansion evidence, not canonical until the agreed final seed count is closed.

### CIFAR-100 Ensemble HAT seed456 post-eval summary plan
- Completed. Raw TSV has 120 rows plus header.
- Fresh-instance eval log: `logs/cifar100_ensemble_seed456_fresh_instance_eval_20260511_195715.log`.
- Summary log: `logs/cifar100_ensemble_seed456_summary_10x3_20260511_201015.log`.
- Best checkpoint: `checkpoints/_ensemble/cifar100_seed456/V4_hybrid_standard_noise_hat_best.pt`.
- Source-domain eval command family completed on 2026-05-11 19:56:
  - `src/compute_vit/train_tinyvit_ensemble.py --mode eval --experiment V4 --dataset cifar100 --checkpoint checkpoints/_ensemble/cifar100_seed456/V4_hybrid_standard_noise_hat_best.pt --batch-size 128 --data-root data --num-workers 4 --pin-memory auto --gpu-resize --amp --eval-runs 3`, teeing to `logs/cifar100_ensemble_hat_seed456_source_eval_20260511_195630.log` and writing JSON/CSV/MD under `thesis/results/mixed_precision/` and `report_md/_gpt/` with `seed456_source_eval` in the filename.
- Corrected fresh-instance eval command family completed on 2026-05-11 20:10:
  - `cli/eval_fresh_instance_protection_maps.py --model_type tinyvit --experiment V4 --dataset cifar100 --checkpoint_path checkpoints/_ensemble/cifar100_seed456/V4_hybrid_standard_noise_hat_best.pt --sensitivity_tsv thesis/results/mixed_precision/layer_sensitivity_full42_20260510.tsv --num_instances 10 --mc_runs 3 --batch_size 128 --device cuda --base_seed 20260511 --start_instance 1 --data_root data --tsv_out thesis/results/mixed_precision/fresh_instance_protection_maps_cifar100_ensemble_hat_seed456_10x3_20260511.tsv`, teeing to `logs/cifar100_ensemble_seed456_fresh_instance_eval_20260511_195715.log`.
- Summary command family:
  - `scripts/summarize_cifar100_protection_map.py --inputs thesis/results/mixed_precision/fresh_instance_protection_maps_cifar100_ensemble_hat_seed456_10x3_20260511.tsv --combined_out thesis/results/mixed_precision/fresh_instance_protection_maps_cifar100_ensemble_hat_seed456_combined_10x3_20260511.tsv --summary_out thesis/results/mixed_precision/fresh_instance_protection_maps_cifar100_ensemble_hat_seed456_summary_10x3_20260511.tsv`, teeing to `logs/cifar100_ensemble_seed456_summary_10x3_<STAMP>.log`.
- Evidence status after success: seed456 alone is provisional; seed123+seed456 together are still multi-seed expansion evidence, not canonical until the agreed final seed count is closed.

## 关键已锁数据

### CIFAR-100 corrected protection map 10×3
- Combined data: `thesis/results/mixed_precision/fresh_instance_protection_maps_cifar100_sharded_corrected_combined_10x3_20260510.tsv`
- Summary: `thesis/results/mixed_precision/fresh_instance_protection_maps_cifar100_sharded_corrected_summary_10x3_20260510.tsv`
- Numbers:
  - fresh_all_analog: `1.02±0.04%`
  - freeze_top20_d2d: `8.59±1.30%`
  - freeze_top30_d2d: `23.81±1.66%`
  - freeze_top42_d2d: `64.20±0.28%`
- Invalid old data: `thesis/results/mixed_precision/fresh_instance_protection_maps_cifar100_sharded_20260510.INVALID_DO_NOT_USE.tsv`

### CIFAR-10 corrected mixed-precision/source-D2D semantics
- Summary: `thesis/results/mixed_precision/mixed_precision_maps_cifar10_corrected_summary_20260511_145736.tsv`
- Main points:
  - `source_checkpoint_d2d`: `91.7167±0.0478%`
  - `all_source_d2d_8bit`: `91.1133±0.1190%`
  - `topk_source_d2d k=30`: `85.3267±0.2953%`
  - naive `all_8bit`, `topk_8bit`, and fake `topk_digital` stay near chance and are negative controls.

### Remote107 selective-KV claim-lock
- Source package: `paper2/manuscript/source_data/remote107_selective_kv_claim_lock_20260511/`
- Summary: `paper2/results/REMOTE107_SELECTIVE_KV_LOCK_SUMMARY_20260511.tsv`
- Protocol: Pythia-410M, WikiText-2 raw-v1 test, context 512, non-overlapping stride 512, batch size 1, digital PPL `23.30`, 41/41 JSON artifacts archived.
- Claim boundary: terminal-layer selectivity supported; all24 rejected as main route; no analog-over-digital superiority, energy/endurance, or local-probe pooling claims.

### 107-clean push review — 2026-05-11 20:45
- Reviewed `origin/107-clean` after user asked to check the push; no local push was performed.
- Latest observed remote commit: `19038b2` (`Add Qwen3-VL HAT training/eval scripts; fix eval filename to include n_states`). Recent supporting commit `5ebbcd6` records Qwen3-VL selective-last1 validation results.
- The 410M Remote107 claim-lock packet remains visible on the remote: `paper2/results/remote107/claim_lock_recovery_20260511/` has 41 JSON artifacts, and `REMOTE_107_SELECTIVE_KV_LOCK_REPORT_20260511.md` reports 41/41 claim-lockable rows.
- Boundary: Qwen3-VL and 2.8B/6.9B scale-up are promising validation/roadmap lanes, but do not become Paper2 claim-bearing until they have complete JSON manifests, checkpoint hashes, commands, and a source-data package comparable to the 410M Remote107 packet.


## Execution rules

- Always tee logs to `logs/` with timestamps.
- Check `nvidia-smi` before launching GPU jobs.
- Use GPU normally, but avoid parallel jobs that saturate VRAM.
- Keep data even if negative; route invalid data to `INVALID_DO_NOT_USE` rather than deleting.
- Update `/home/qiaosir/projects/BROADCAST.md` after each substantial phase.

Full plan: `/home/qiaosir/projects/compute_vit/task.md`
