
# compute_vit 任务列表（Paper1–4 数据推进版）

更新时间：2026-05-11
负责人策略：Claude/CC 直接执行；其他代理只按明确任务接力。核心目标是持续获取实验数据与结果，支撑 Paper1/Paper2/Paper3/Paper4；硕士论文是后续下游整合，不作为当前收口约束。

---

## 总原则

1. 默认推进更多实验与数据，不以 thesis 冻结为目标。
2. 每个实验必须归属至少一个 paper lane：Paper1 / Paper2 / Paper3 / Paper4。
3. 所有实验必须保留：命令、日志、TSV/JSON 原始结果、summary、脚本版本、checkpoint 路径。
4. GPU 正常使用，但不并发打满显存；启动前看 `nvidia-smi`，优先单进程顺序跑。
5. batch size 根据显存和实验目的决定；默认从 128 尝试，OOM 或接近满显存则退到 64。
6. Kimi/旧自动结果不直接引用；先审脚本逻辑，再把数据升级为 canonical。
7. 错误数据不删除，改名 `INVALID_DO_NOT_USE` 并在 evidence ledger 标注。
8. 每阶段完成后写入 `BROADCAST.md`。

---

## P0：当前 corrected evidence 收口与防污染

### T0.1 锁定 corrected CIFAR-100 protection map 10×3
- **Lane**：Paper1 supplement / Paper3 seed / thesis downstream
- **状态**：已完成实验、已图表化并已 ledger 化；后续只在新实验完成后追加更新
- **Canonical data**：
  - `thesis/results/mixed_precision/fresh_instance_protection_maps_cifar100_sharded_corrected_combined_10x3_20260510.tsv`
  - `thesis/results/mixed_precision/fresh_instance_protection_maps_cifar100_sharded_corrected_summary_10x3_20260510.tsv`
- **Canonical numbers**：
  - fresh_all_analog: `1.02±0.04%`
  - freeze_top20_d2d: `8.59±1.30%`
  - freeze_top30_d2d: `23.81±1.66%`
  - freeze_top42_d2d: `64.20±0.28%`
- **Invalid data**：
  - `thesis/results/mixed_precision/fresh_instance_protection_maps_cifar100_sharded_20260510.INVALID_DO_NOT_USE.tsv`
- **当前状态**：CIFAR-100 Ensemble HAT seed456 和 seed789 均已闭环为 provisional expansion evidence。seed456 source-domain eval `66.66±0.03%`，fresh-instance 10×3 `fresh_all_analog=63.744±0.514%`、`freeze_top42_d2d=64.974±0.538%`。seed789 training best `65.05%` at epoch 88，source-domain eval `65.07±0.16%`，fresh-instance 10×3 `fresh_all_analog=58.002±1.686%`、`freeze_top20_d2d=61.822±0.859%`、`freeze_top30_d2d=62.037±0.926%`、`freeze_top42_d2d=62.131±0.985%`。seed789 低于 seed456 但远高于 fixed-mask fresh collapse；当前只作为多 seed 扩展证据，不替代最终约定的 canonical multi-seed protocol。

### T0.2 建立 canonical evidence ledger
- **Lane**：shared / all papers
- **状态**：已建立，当前作为持续更新的 claim-to-artifact 索引维护
- **输出**：`report_md/_gpt/CANONICAL_EVIDENCE_LEDGER_20260510.md`
- **内容**：
  - claim
  - value
  - protocol
  - data file
  - summary file
  - script
  - checkpoint
  - log
  - status: canonical / provisional / invalid
- **必须收录**：
  - CIFAR-10 protection map 10×3
  - CIFAR-100 corrected protection map 10×3
  - invalid CIFAR-100旧结果
  - CIFAR-100 batch64 control，仅标 sanity，不进叙事
  - Ensemble HAT 86.16±0.19
  - severe NL 32.60±9.18
  - Paper1 PCM precision ladder
  - Paper2/107 KV-cache pilot/canonical rows

### T0.3 画 CIFAR-10 vs CIFAR-100 protection curve
- **Lane**：Paper3 primary seed / Paper1 supplement / thesis downstream
- **状态**：已完成当前 10×3 对照图与源数据，后续随 Ensemble HAT seed456/seed789 评估追加
- **输入**：
  - CIFAR-10 10×3 summary
  - CIFAR-100 corrected 10×3 summary
- **输出**：
  - `thesis/figures/mixed_precision/fig_cifar10_cifar100_protection_comparison_20260510.png`
  - `thesis/figures/mixed_precision/fig_cifar10_cifar100_protection_comparison_20260510.pdf`
  - source CSV/TSV
- **叙事**：保护预算随任务难度上升；CIFAR-10 top30 可用，CIFAR-100 top30 仍远低于源域，top42 才接近源域。

---

## Paper1：ViT/HAT/PCM deployment frontier

### T1.1 Paper1 release consistency check
- **目标**：active manuscript 与 release bundle 同步。
- **检查项**：
  - no `TinyImageNet` stale reference
  - no `ion. n.` garbage
  - no KV-cache as Paper1 main claim
  - Fig1/Fig2 assets present
  - active/release `sections/06_discussion.tex` and `sections/07_conclusion.tex` aligned
- **输出**：`paper1/reports/PAPER1_RELEASE_CONSISTENCY_CHECK_20260510.md`

### T1.2 Paper1 clean-room build
- **目标**：确认投稿包仍可编译。
- **输入**：`paper1/release/paper1_submission_bundle_20260509_final/`
- **输出**：build log + PDF hash + missing file report
- **优先级**：中，高于补新实验但低于 canonical evidence ledger。

### T1.3 CIFAR-10 protection map 10×5 extension
- **目标**：增强统计置信度。
- **当前状态**：10×3 已足够；10×5 是增强项。
- **建议**：GPU 空档时后台跑，不阻塞 Paper2/Paper3 主实验。

---

## Paper2：107 selective analog KV-cache

### T2.1 107 corrected-noise canonical manifest
- **目标**：把 107 从 pilot 升级为 canonical。
- **状态**：已完成当前 Paper2 410M claim-lock packet；2026-05-11 package 有 41/41 JSON artifacts、manifest/report、summary TSV 和 regenerated figure。`origin/107-clean` 后续 Qwen3-VL/2.8B/6.9B 推送已审阅到 `19038b2`，但仍是 validation/scale-up lane，未升级为当前 claim-bearing source。
- **Canonical package**：`paper2/manuscript/source_data/remote107_selective_kv_claim_lock_20260511/`
- **Summary**：`paper2/results/REMOTE107_SELECTIVE_KV_LOCK_SUMMARY_20260511.tsv`
- **Protocol**：Pythia-410M, WikiText-2 raw-v1 test, context 512, non-overlapping stride 512, batch size 1, digital PPL `23.30`。
- **Claim boundary**：terminal-layer selectivity supported; all-layer analog KV rejected as main route; local cache-path/retention/offline probes and newer scale-up/Qwen3-VL pushes are engineering/provisional until packaged with full manifests, checkpoint hashes, commands, and source data.

### T2.2 last1/last2/all-layer scale ladder
- **模型规模**：125M → 410M → 1B/1.1B → 2.8B（按资源推进）
- **每个规模至少跑**：
  - digital baseline
  - all-layer analog stress
  - last1 selective
  - last2 selective
  - fresh-D2D seeds
- **目标结论**：all-layer abandoned，last1 是可行路线。

### T2.3 KV-cache context length sweep
- **上下文长度**：512 / 1024 / 2048 / 4096 / optional 8192
- **指标**：PPL、ΔPPL、D2D CV、内存节省估计
- **目的**：体现 KV-cache 作为 memory-bound inference 的独立价值。

### T2.4 KV-cache retention/refresh sweep
- **变量**：retention time、refresh interval、terminal-layer-only refresh、all-layer refresh
- **输出**：PPL vs refresh-cost curve
- **Paper2 价值**：从单纯 PPL 结果升级为系统设计论文。

---

## Paper3：cross-dataset / cross-architecture vision scaling

### T3.1 CIFAR-100 Ensemble HAT checkpoint 搜索/训练
- **最高优先级中型实验**。
- **问题**：CIFAR-100 fixed-mask fresh collapses，top42 才回源域；Ensemble HAT 能否恢复跨实例？
- **状态**：seed123 checkpoint 已存在；seed456 和 seed789 已完成训练、source-domain eval、corrected fresh-instance 10×3 summary，当前作为 provisional expansion evidence 进入 ledger。
- **seed456 outputs**：
  - checkpoints: `checkpoints/_ensemble/cifar100_seed456/`
  - train log: `logs/cifar100_ensemble_hat_seed456_20260511_174359.log`
  - source eval log: `logs/cifar100_ensemble_hat_seed456_source_eval_20260511_195630.log`
  - fresh-instance eval log: `logs/cifar100_ensemble_seed456_fresh_instance_eval_20260511_195715.log`
  - summary log: `logs/cifar100_ensemble_seed456_summary_10x3_20260511_201015.log`
  - train JSON/CSV: `thesis/results/mixed_precision/cifar100_ensemble_hat_seed456_train_20260511_174359.json/.csv`
  - source eval JSON/CSV: `thesis/results/mixed_precision/cifar100_ensemble_hat_seed456_source_eval_20260511_195630.json/.csv`
  - fresh-instance raw/combined/summary: `thesis/results/mixed_precision/fresh_instance_protection_maps_cifar100_ensemble_hat_seed456_10x3_20260511.tsv`, `thesis/results/mixed_precision/fresh_instance_protection_maps_cifar100_ensemble_hat_seed456_combined_10x3_20260511.tsv`, `thesis/results/mixed_precision/fresh_instance_protection_maps_cifar100_ensemble_hat_seed456_summary_10x3_20260511.tsv`
  - report: `report_md/_gpt/CIFAR100_ENSEMBLE_HAT_SEED456_TRAIN_20260511_174359.md`, `report_md/_gpt/CIFAR100_ENSEMBLE_HAT_SEED456_SOURCE_EVAL_20260511_195630.md`
	- **seed789 outputs**：
	  - checkpoint: `checkpoints/_ensemble/cifar100_seed789/V4_hybrid_standard_noise_hat_best.pt`
	  - train log: `logs/cifar100_ensemble_hat_seed789_20260511_202459.log`
	  - source eval log: `logs/cifar100_ensemble_hat_seed789_source_eval_20260511_213615.log`
	  - fresh-instance eval log: `logs/cifar100_ensemble_seed789_fresh_instance_eval_20260511_213655.log`
	  - summary log: `logs/cifar100_ensemble_seed789_summary_10x3_20260511_214930.log`
	  - train JSON/CSV: `thesis/results/mixed_precision/cifar100_ensemble_hat_seed789_train_20260511_202459.json/.csv`
	  - source eval JSON/CSV: `thesis/results/mixed_precision/cifar100_ensemble_hat_seed789_source_eval_20260511_213615.json/.csv`
	  - fresh-instance raw/combined/summary: `thesis/results/mixed_precision/fresh_instance_protection_maps_cifar100_ensemble_hat_seed789_10x3_20260512.tsv`, `thesis/results/mixed_precision/fresh_instance_protection_maps_cifar100_ensemble_hat_seed789_combined_10x3_20260512.tsv`, `thesis/results/mixed_precision/fresh_instance_protection_maps_cifar100_ensemble_hat_seed789_summary_10x3_20260512.tsv`
	  - report: `report_md/_gpt/CIFAR100_ENSEMBLE_HAT_SEED789_TRAIN_20260511_202459.md`, `report_md/_gpt/CIFAR100_ENSEMBLE_HAT_SEED789_SOURCE_EVAL_20260511_213615.md`


### T3.2 TinyImageNet / ImageNet-100 eval-only
- **目标**：不先 full training，先评估可迁移性。
- **配置**：digital baseline / standard HAT / fresh_all / topK protection
- **产物**：dataset ladder 表。

### T3.3 Architecture ladder
- **模型**：Tiny-ViT、DeiT-S、Swin-T、ConvNeXt-Tiny
- **问题**：敏感层是否集中于 MLP tail？protection ranking 是否跨架构有效？
- **输出**：architecture × protection budget matrix。

### T3.4 Sensitivity ranking transfer
- **问题**：CIFAR-10 full42 ranking 能否预测 CIFAR-100/TinyImageNet/DeiT？
- **实验**：
  - ranking from CIFAR-10
  - ranking from CIFAR-100
  - cross-apply ranking
  - compare topK rescue
- **Paper3 价值**：从经验保护图变成方法论文。

### T3.5 Spatial variance / floorplan-aware tile mapping
- **Lane**：Paper3/Paper4 bridge / thesis downstream
- **状态**：10×3 synthetic tile-mapping expansion completed on seed789; evidence remains provisional because the tile-quality profile is synthetic rather than measured.
- **Protocol**：CIFAR-100 Tiny-ViT V4 Ensemble HAT seed789 checkpoint, full test set, batch size 128, synthetic good/nominal/weak/bad tile profiles assigned to 42 analog layers by sequential, random, sensitivity-aware, and worst-case mapping.
- **10×3 outputs**：
  - raw TSV: `thesis/results/spatial_variance/spatial_variance_mapping_10x3_20260511_220730.tsv`（120 rows + header）
  - summary TSV: `thesis/results/spatial_variance/spatial_variance_mapping_summary_10x3_20260511_220730.tsv`
  - plot source TSV: `thesis/results/spatial_variance/spatial_variance_mapping_plot_source_10x3_20260511_220730.tsv`
  - figure: `thesis/figures/spatial_variance/fig_spatial_variance_mapping_10x3_20260511.png/.pdf`
  - tile profiles: `thesis/results/spatial_variance/tile_profiles_10x3_20260511_220730.json`
  - mapping specs: `thesis/results/spatial_variance/mapping_specs_10x3_20260511_220730.tsv`
  - scripts: `scripts/eval_spatial_variance_mapping.py`, `scripts/plot_spatial_variance_mapping.py`
  - logs: `logs/local_gpu_spatial_variance_10x3_20260511_220730.log`, `logs/plot_spatial_variance_mapping_*.log`
- **10×3 numbers**：sensitivity-aware `50.9413±1.6904%`, random `46.7020±2.2885%`, worst-case `42.5790±3.5225%`, sequential `39.3353±2.9631%`. Sensitivity-aware beats random by `+4.24` pp and worst-case by `+8.36` pp under this synthetic stress profile.
- **Pilot preview**：3×2 pilot remains sanity/protocol preview: sensitivity-aware `50.7067±0.2959%`, random `47.6683±0.5025%`, worst-case `43.9933±2.2602%`, sequential `37.7667±3.8579%`.
- **Evidence status**：provisional；do not present as measured floorplan evidence. Next CPU step: plot floorplan tradeoff and document synthetic-profile limits; next GPU lane may be drift-aware SAM or measured-profile/floorplan extension after fresh `nvidia-smi`.

---

## Paper4：organic device physics / DTCO

### T4.1 Retention × protection sweep
- **变量**：retention time、tau1/tau2/A0、protected K
- **状态**：10×3 expansion completed on seed789; evidence remains provisional because the retention model uses current simulator defaults rather than measured long-term drift.
- **Protocol**：CIFAR-100 Tiny-ViT V4 Ensemble HAT seed789 checkpoint, full test set, 10 fresh D2D instances × 3 MC, protected K={0,30,42}, retention={0,1000,10000}s, `--recalibrate_scale --scale_d2d`.
- **Outputs**：
  - raw TSV: `thesis/results/retention_protection/retention_protection_10x3_20260511_223530.tsv`（270 rows + header）
  - summary TSV: `thesis/results/retention_protection/retention_protection_summary_10x3_20260511_223530.tsv`
  - plot source TSV: `thesis/results/retention_protection/retention_protection_plot_source_10x3_20260511_223530.tsv`
  - figure: `thesis/figures/retention_protection/fig_retention_protection_10x3_20260511.png/.pdf`
  - scripts: `scripts/eval_retention_protection_sweep.py`, `scripts/plot_retention_protection.py`
  - logs: `logs/local_gpu_retention_protection_10x3_20260511_223530.log`, `logs/plot_retention_protection_10x3_20260511_231000.log`
- **Numbers**：0s fresh/top30/top42 = `58.223±1.386%` / `62.051±0.587%` / `62.248±0.510%`; 1000s = `55.596±1.229%` / `59.207±0.608%` / `59.392±0.605%`; 10000s = `55.403±1.272%` / `59.223±0.606%` / `59.391±0.482%`.
- **Interpretation**：retention drift under this model costs roughly `2.6–2.9` pp from 0s to 1000/10000s, while top30/top42 protection remains around `59.2–59.4%`. Do not cite as measured retention or refresh/energy closure.
- **Pilot preview**：3×2 pilot remains protocol preview only: 0s fresh/top30/top42 = `59.035±1.101%` / `61.883±0.142%` / `62.028±0.272%`; 1000s = `56.008±0.971%` / `59.180±0.149%` / `59.263±0.036%`; 10000s = `56.298±0.748%` / `59.180±0.087%` / `59.360±0.194%`.
- **Next**：GPU is free after this run; before any new GPU lane, rerun `nvidia-smi` and choose between drift-aware SAM, measured-profile/floorplan extension, or CNN-vs-ViT architecture comparison.


### T4.2 Optical front-end response sweep
- **变量**：inverse-gamma、shot noise、illumination variation、compensation on/off
- **目标**：有机光电前端是否引入独立 failure mode。
- **输出**：optical response deployment envelope。

### T4.3 Write nonlinearity grid
- **变量**：NL_LTP / NL_LTD、MLP-only compensation、all-linear compensation、fresh-instance
- **目标**：把 severe NL 负结果系统化。
- **输出**：NL generalization boundary。

### T4.4 Measured profile ingestion
- **前提**：有真实器件或文献 profile 数据。
- **目标**：profile fitting → simulation → task accuracy。
- **输出**：DTCO pipeline demo。

---

## GPU 队列建议

### 短任务（<1h）
1. evidence ledger 生成/校验
2. protection comparison plot
3. CIFAR-10 10×5 extension shard
4. summary/plot regeneration

### 中任务（1–8h）
1. CIFAR-100 Ensemble HAT seed1
2. TinyImageNet/ImageNet-100 eval-only
3. KV-cache 125M/410M corrected runs
4. retention × protection small grid

### 长任务（8h+）
1. CIFAR-100 Ensemble HAT multi-seed
2. ImageNet subset full protocol
3. LLM KV-cache scale ladder ≥1B
4. multi-architecture protection map

---

## 立即执行建议

1. **CIFAR-100 Ensemble HAT seed789 正在运行**，不要启动第二个 GPU/Python 任务；训练完成后跑 source-domain + corrected fresh-instance 10×3，并更新 ledger/broadcast。
2. **保持 evidence ledger 更新**，新实验完成后先写 claim/status/artifact 映射，再进入论文叙事。
3. **Paper2 正式稿转换**：把 figure-led draft 转成正式 manuscript template，但继续只用 Remote107 claim-lock rows 作为 claim-bearing evidence。
4. **GPU 空闲后继续实验队列**：优先 seed789 或 spatial variance / drift-aware SAM pilot，启动前必须重新 `nvidia-smi`。

---

## 当前不要做

1. 不要把硕士论文定稿当主线。
2. 不要为了叙事做 batch-size 对照扩展。
3. 不要继续引用未审脚本产出的 Kimi 结果。
4. 不要把 KV-cache 写进 Paper1 主 claim。
5. 不要删除错误数据；只隔离和标注。
