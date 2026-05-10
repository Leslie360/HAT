# compute_vit 项目审计补充报告（第二卷）
**Date:** 2026-04-24
**Auditor:** Kimi
**Scope:** data/, scripts/（非 _gpt）, device_profiles/, logs/, checkpoints/, report_md/（非 _gpt）

---

## 一、数据目录（data/）

| # | 子目录 | 内容 | 大小估算 | 审查意见 |
|:-:|:-------|:-----|:---------|:---------|
| 1 | `cifar-10-batches-py/` | CIFAR-10 原始数据（5 train + 1 test） | ~170 MB | 标准数据集，保持 |
| 2 | `cifar-100-python/` | CIFAR-100 原始数据 | ~170 MB | 标准数据集，保持 |
| 3 | `flowers-102/` | Flowers-102 原始数据 + jpg | ~350 MB | 标准数据集，保持 |
| 4 | `imagenet/val/` | ImageNet 验证集 | ~6 GB | 标准数据集，保持 |
| 5 | `tiny-imagenet-200/` | Tiny-ImageNet-200 | ~250 MB | 标准数据集，保持 |

**建议：** data/ 目录管理良好，均为标准数据集。建议在 `data/` 下添加 `README.md` 说明各数据集来源和下载指令。

---

## 二、Device Profiles（device_profiles/）

| # | 文件 | 描述 | 状态 |
|:-:|:-----|:-----|:-----|
| 1 | `literature_profiles_gpt.json` | 文献锚定配置（OPECT Standard 等） | ✅ 当前 canonical |
| 2 | `synthetic_profiles_gpt.json` | 合成压力测试配置 | ✅ 当前 canonical |
| 3 | `example_measured_device_profile_gpt.json` | 实测设备占位模板 | ⚠️ 占位符，需替换 |

**建议：** `example_measured_device_profile_gpt.json` 明确标注为 placeholder，不应在论文中被引用为实测数据。

---

## 三、Scripts（非 _gpt/）

| # | 文件 | 描述 | 状态 |
|:-:|:-----|:-----|:-----|
| 1 | `append_ruling_sync.py` | AGENT_SYNC 追加工具 | ⚠️ 硬编码路径 |
| 2 | `export_remote_github_handoff.sh` | 远程 handoff 导出脚本 | — |
| 3 | `monitor_kimi_ablation_outputs.py` | Kimi 消融输出监控 | — |
| 4 | `public_release_export.sh` | 公开发布导出 | — |
| 5 | `run_public_smoke_test.sh` | 公开冒烟测试 | — |

**建议：** `append_ruling_sync.py` 硬编码了 `sync_file = 'compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md'`，路径假设项目名为 `compute_vit`，若目录重命名会失败。建议改为相对路径或 `Path(__file__).resolve()` 推导。

---

## 四、Logs 日志爆炸（logs/ 和 logs/_gpt/）

| 指标 | 数值 |
|:-----|:-----|
| `logs/` 总文件 | ~400 |
| `logs/_gpt/` 文件 | 373 |
| 4 月 20 日前旧日志 | 340 |
| 占比 | **91% 为过期日志** |

**问题：** 日志目录呈指数增长，旧日志占据绝大多数空间。当前无自动轮转机制。

**建议（不动手，仅建议）：**
1. 在 `logs/` 下按日期分子目录：`logs/2026-04-15/`, `logs/2026-04-20/`
2. 或添加 cron 脚本定期清理 >14 天的日志
3. 重要日志（如 cx_m 系列）应单独归档到 `logs/m_series/`

---

## 五、Checkpoints 检查点审计

### 5.1 目录总览

| 目录 | 大小 | 日期 | 状态 |
|:-----|:-----|:-----|:-----|
| `checkpoints/_gpt/` | ~26 GB | 04-24 | 🔄 当前 active（M-series） |
| `checkpoints/_gpt_badscale/` | 153 MB | 04-04 | ⚠️ Pre-fix suspect |
| `checkpoints/_gpt_v3_suspect/` | 153 MB | 04-04 | ⚠️ Pre-fix suspect |
| `checkpoints/_ensemble/` | 153 MB | 04-07 | ⚠️ 可能 pre-fix |
| `checkpoints/_ensemble_smoke/` | 153 MB | 04-07 | ⚠️ 可能 pre-fix |
| `checkpoints/gm_e4_nl_scan/` | 765 MB | 04-12 | ⚠️ Pre-fix sweep |
| `checkpoints/resnet18_cifar100/` | 343 MB | 04-14 | — ResNet-18 CIFAR-100 |
| `checkpoints/_cadence_control/` | 153 MB | 04-17 | — Cadence control |
| `checkpoints/_cadence_control_smoke/` | 153 MB | 04-17 | — Cadence smoke |
| `checkpoints/learnable_gamma_gpt/` | ? | 04-18 | — Learnable gamma |
| `checkpoints/C2-C8_*.pt` | 各 ~211 MB | 混合 | — ADC 消融检查点 |

### 5.2 风险发现

**`_gpt_badscale` 和 `_gpt_v3_suspect`**（04-04 日期）
- 目录名已暗示问题（"badscale", "suspect"）
- 可能是 pre-fix 训练且使用了错误的 scale recovery
- **建议：** 若确认无效，可安全删除以释放 306 MB

**`_ensemble` 和 `_ensemble_smoke`**（04-07 日期）
- 在 bug fix（33bed9c，约 04-23）之前
- 可能受 dual bug 污染
- **建议：** 用 `test_dual_bug_fix.py` 验证这些检查点的元数据 NL 值；若 NL=2.0 则标记为 pre-fix

### 5.3 根目录散落检查点

`checkpoints/C2_4bit_no_noise_best.pt` 到 `C8_6bit_noise_HAT_best.pt` 共 7 个 .pt 文件直接放在 `checkpoints/` 下。

**建议：** 移入子目录如 `checkpoints/adc_ablation/` 以保持整洁。

---

## 六、Report_md 非 _gpt/ 目录

### 6.1 实验报告

| 文件 | 描述 | 状态 |
|:-----|:-----|:-----|
| `a23_physical_compensation_report.md` | A2.3 前端物理补偿 | ✅ Bug-immune（NL=1.0） |
| `array_mapping_report.md` | 层映射与阵列需求 | ✅ Bug-immune |
| `physical_noise_report.md` | 物理噪声注入扫描 | ✅ Bug-immune |
| `resnet18_experiment_report.md` | ResNet-18 CIFAR-10 | ✅ Bug-immune |
| `convnext_experiment_report.md` | ConvNeXt-Tiny | ✅ Bug-immune |

### 6.2 审稿人意见（中文）

| 文件 | 行数 | 内容 |
|:-----|-----:|:-----|
| `审稿人意见-4.10.md` | 1298 | 4 月 10 日审稿意见 |
| `审稿人意见from_model.md` | 1026 | Model 生成审稿意见 |
| `审稿意见0412.md` | 646 | 4 月 12 日审稿意见 |
| `审稿意见model_0411.md` | 756 | Model 生成审稿意见 |

**建议：** 这些审稿意见文件含有 pre-fix 数字（27.72% 等），但它们是外部输入，不应被修改。建议在目录名或文件名中添加 `external_reviews/` 前缀以明确区分。

### 6.3 其他文件

| 文件 | 描述 |
|:-----|:-----|
| `Gemini.md` | Gemini 早期备忘录 |
| `claude-report.md` / `claude全栈参考手册.md` | Claude 参考文档 |
| `最佳json.md` / `查找数据.md` | 中文临时笔记 |

**建议：** `最佳json.md` 和 `查找数据.md` 为临时笔记，可归档到 `archive/notes/`。

---

## 七、根目录异常文件

| 文件 | 问题 | 建议 |
|:-----|:-----|:-----|
| `run_ensemble_hat_fixed.py.ORIGINAL` | 备份文件，不应在根目录 | 删除或移入 `archive/` |
| `simulate_final_rerun.py.SIMULATED` | 奇怪扩展名 | 删除或重命名 |
| `train_tinyvit_ensemble.py.bak_logfix` | 备份文件 | 删除或移入 `archive/` |
| `_gpu_monitor.sh` | 下划线前缀，隐藏文件风格 | 重命名为 `scripts/monitor_gpu.sh` |
| `_ckpt_monitor.sh` | 同上 | 重命名为 `scripts/monitor_checkpoint.sh` |
| `_rapid_monitor.py` | 同上 | 重命名为 `scripts/monitor_rapid.py` |

---

## 八、补充修改建议汇总

### 8.1 高优先级

| # | 建议 | 涉及文件 | 理由 |
|:-:|:-----|:---------|:-----|
| 1 | 删除/归档 3 个根目录备份文件 | `.ORIGINAL`, `.SIMULATED`, `.bak_logfix` | 根目录 clutter |
| 2 | 验证并标记 stale checkpoint 目录 | `_gpt_badscale`, `_gpt_v3_suspect` | 释放 306 MB，避免误用 |
| 3 | 重命名 3 个监控脚本 | `_gpu_monitor.sh` 等 | 下划线前缀不符合惯例 |

### 8.2 中优先级

| # | 建议 | 涉及文件 | 理由 |
|:-:|:-----|:---------|:-----|
| 4 | 日志目录按日期分区 | `logs/` | 管理 400+ 日志文件 |
| 5 | ADC 检查点移入子目录 | `checkpoints/C2-C8_*.pt` | 根目录 clutter |
| 6 | 添加 `data/README.md` | `data/` | 记录数据集来源 |
| 7 | 归档临时笔记 | `最佳json.md`, `查找数据.md` | 根目录 clutter |

### 8.3 低优先级

| # | 建议 | 涉及文件 | 理由 |
|:-:|:-----|:---------|:-----|
| 8 | 修复 `append_ruling_sync.py` 硬编码路径 | `scripts/append_ruling_sync.py` | 可维护性 |
| 9 | 为 `device_profiles/` 添加 README | `device_profiles/` | 文档完整性 |
| 10 | 统一 `report_md/` 外部审稿文件命名 | `审稿*.md` | 一致性 |

---

## 九、Sign-off

第二卷审计完成。覆盖范围：data/, device_profiles/, scripts/（非 _gpt）, logs/, checkpoints/, report_md/（非 _gpt）。

**关键发现：**
1. logs/_gpt/ 91% 为过期日志，建议轮转
2. checkpoints/ 存在 2 个明确标记为 suspect 的 pre-fix 目录（306 MB）
3. 根目录有 3 个备份文件和 3 个下划线前缀监控脚本需要清理
4. 所有实验报告（report_md/ 非 _gpt）均为 bug-immune

**不动手修改。所有建议仅为记录。**
