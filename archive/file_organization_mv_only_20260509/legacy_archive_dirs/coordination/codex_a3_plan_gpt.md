## 2026-04-03 21:46 Codex
### Read
- `/home/qiaosir/projects/compute_vit/report_md/array_mapping_report.md`
- `/home/qiaosir/projects/compute_vit/report_md/claude全栈参考手册.md`
- `/home/qiaosir/projects/compute_vit/model_profiling.py`
- `/home/qiaosir/projects/compute_vit/analog_layers.py`
- `/home/qiaosir/projects/compute_vit/train_tinyvit.py`

### Findings
- A3.1 的关键 prerequisite 现在已满足：
  - Tiny-ViT analog/digital mapping 规则已统一
  - patch embedding analog conversion 已接入 runtime
  - dry-run 可输出层级分配、arrays、energy、V1-V7 matrix
- 当前 dry-run 采用 `V4` 作为参考 hybrid 配置，但报告同时打印全部 `V1-V7` 配置矩阵。
- `train_tinyvit.py` 的 `train` / `eval` 模式现在已补强：
  - 支持 `--experiments` 批量调度
  - 支持 `--eval-runs` 重复 noisy eval
  - 支持 GPT-scoped result export 到 `_gpt/csv_gpt` 和 `_gpt/json_gpt`

### Changes
- added `/home/qiaosir/projects/compute_vit/train_tinyvit.py`
- added `/home/qiaosir/projects/compute_vit/tinyvit_hybrid_utils.py`
- generated `/home/qiaosir/projects/compute_vit/report_md/_gpt/tinyvit_hybrid_dryrun_report_gpt.md`
- added `/home/qiaosir/projects/compute_vit/test_train_tinyvit.py`

### Next suggested step
- if only static inspection is needed:
  - `cd /home/qiaosir/projects/compute_vit && /home/qiaosir/miniconda3/envs/LLM/bin/python train_tinyvit.py --mode dry-run --experiment V4 --dataset cifar10 --device cpu`
- if later approved to start A3 training:
  - `cd /home/qiaosir/projects/compute_vit && /home/qiaosir/miniconda3/envs/LLM/bin/python train_tinyvit.py --mode train --experiments V3 V4 V5 --dataset cifar10 --device cuda --log-path logs/_gpt/train_tinyvit_v345_gpt.log`
- if later approved to run checkpoint evaluation:
  - `cd /home/qiaosir/projects/compute_vit && /home/qiaosir/miniconda3/envs/LLM/bin/python train_tinyvit.py --mode eval --experiments V4 V5 V6 V7 --dataset cifar10 --device cuda --checkpoint-dir checkpoints --eval-runs 5 --log-path logs/_gpt/eval_tinyvit_v4567_gpt.log`
- while waiting for A2.2 to finish, ConvNeXt post-run export can be rehearsed safely with:
  - `cd /home/qiaosir/projects/compute_vit && /home/qiaosir/miniconda3/envs/LLM/bin/python train_convnext.py --report-only-log logs/_gpt/train_convnext_restart_20260403_2154_gpt.log --experiments C2 C3 C4 --skip-retention --device cpu --output-dir report_md/_gpt --csv-name convnext_results_gpt.csv --json-name convnext_results_gpt.json --report-name convnext_experiment_report_gpt.md`
- Claude should review whether to add a second dry-run summary using `V6` so the physical-front-end configuration is logged separately from the base `V4` hybrid path
