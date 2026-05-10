# compute_vit 项目全量清单与审计报告
**Date:** 2026-04-24
**Auditor:** Kimi
**Scope:** 全项目核心文件（排除图像/检查点/归档副本）

---

## 一、项目概览

| 指标 | 数值 |
|:---|:---|
| 核心文件总数 | ~1,605 |
| Python 源码 | 94 |
| Markdown 文档 | 727 |
| LaTeX 论文 | 33 |
| JSON 数据 | 200 |
| Shell 脚本 | 69 |
| CSV 表格 | 70 |
| 已知 Bug 污染文件 | 97+ |

**关键事件：** `analog_layers.py` STE 反向传播存在双 bug（分支映射翻转 + 额外 nl 乘数），已于 commit `33bed9c` 修复。所有 NL≠1.0 的 severe-NL 结果（27.72%, 30.53%, 32.12%, 32.60%, 38.95% 等）均已失效。

---

## 二、核心代码文件（根目录 .py）

| # | 文件 | 一句话描述 | Bug 标记 | 修改建议 |
|:-:|:-----|:-----------|:---------|:---------|
| 1 | `analog_layers.py` | 核心模拟层：STE 量化 + 差分对 + 噪声注入 | ✅ FIXED at 33bed9c | 已修复，保持当前版本为 canonical |
| 2 | `analog_layers_ensemble.py` | 已弃用的 Ensemble 版本（被 analog_layers.py 取代） | ⚠️ DEPRECATED | 删除或移入 `archive/` |
| 3 | `train_tinyvit_ensemble.py` | Ensemble HAT 训练主循环（epoch 级 D2D 重采样） | — | 当前 canonical 训练脚本 |
| 4 | `train_tinyvit.py` | Standard HAT 训练主循环 | — | 当前 canonical 训练脚本 |
| 5 | `train_resnet18.py` | ResNet-18 训练脚本 | — | 保持 |
| 6 | `train_convnext.py` | ConvNeXt 训练脚本 | — | 保持 |
| 7 | `eval_fresh_instances_postfix.py` | Post-fix fresh-instance 评估（读取 checkpoint NL） | ✅ FIXED | 已修复 NL 来源验证 |
| 8 | `eval_fresh_instances.py` | 旧版 fresh-instance 评估 | — | 检查是否与 postfix 重复，考虑合并 |
| 9 | `inference_analysis_utils.py` | 推理工具：MC 评估 + device-profile sweep | — | 保持 |
| 10 | `device_profile_utils.py` | Device profile 加载器（文献 + 实测数据） | — | 保持 |
| 11 | `hybrid_calibration.py` | 混合校准：块输出仿射校正 | — | 保持 |
| 12 | `hybrid_runtime_compiler.py` | 混合部署运行时编译器 | — | 保持 |
| 13 | `lightweight_adapter.py` | 轻量级残差适配器 + TTT | — | 保持 |
| 14 | `tinyvit_hybrid_utils.py` | Tiny-ViT 混合映射工具 | — | 保持 |
| 15 | `amp_utils.py` | AMP 辅助函数 | — | 保持 |
| 16 | `test_dual_bug_fix.py` | 双 bug 修复单元测试（6 tests pass） | — | 保持，持续维护 |
| 17 | `debug_math_consistency.py` | 数学一致性调试（8/8 tests pass） | — | 保持 |
| 18 | `monitor_training_health.py` | 训练健康监控 | — | 保持 |
| 19 | `append_agent_sync.py` | AGENT_SYNC 追加脚本 | ⚠️ hardcodes 27.72 | 更新为 M-series 结果后修复 |
| 20 | `fix_drudge_wave.py` | Memo 修复脚本 | ⚠️ hardcodes pre-fix 数据 | 归档处理 |
| 21 | `fix_gemini_missing_tasks.py` | Gemini 任务修复脚本 | ⚠️ hardcodes pre-fix 数据 | 归档处理 |
| 22 | `generate_gemini_q.py` | Gemini memo 生成器 | ⚠️ hardcodes pre-fix 数据 | 归档处理 |
| 23 | `generate_gemini_q_phase2.py` | Gemini P2 memo 生成器 | ⚠️ hardcodes pre-fix 数据 | 归档处理 |
| 24 | `generate_drudge_wave.py` | Drudge wave 生成器 | ⚠️ hardcodes pre-fix 数据 | 归档处理 |
| 25 | `update_gemini_slim_empirical.py` | Gemini SLIM 更新 | ⚠️ hardcodes pre-fix 数据 | 归档处理 |
| 26 | `run_nl_layer_sensitivity.py` | NL 层敏感度分析 | ⚠️ hardcodes 27.72 | 更新 baseline 为 M1 结果 |
| 27-94 | 其他 run_*/test_*/plot_*/generate_* 脚本 | 各类实验、可视化、测试脚本 | 多数 clean | 详见下方整理建议 |

---

## 三、论文文件（paper/）

### 3.1 Live Paper .tex（Frozen until CLAUDE-FC）

| # | 文件 | 描述 | Bug 标记 |
|:-:|:-----|:-----|:---------|
| 1 | `main.tex` | 主文档 | — |
| 2 | `cover_letter.tex` | Cover letter v2（旧版） | — |
| 3 | `cover_letter_v3.tex` | Cover letter v3（含 30% structural ceiling） | 🔴 CONTAMINATED |
| 4 | `sections/00_abstract.tex` | 摘要 | — |
| 5 | `sections/01_introduction.tex` | 引言（含 27.72%） | 🔴 CONTAMINATED |
| 6 | `sections/02_related_work.tex` | 相关工作 | — |
| 7 | `sections/03_methodology.tex` | 方法论 | — |
| 8 | `sections/04_experimental_setup.tex` | 实验设置 | — |
| 9 | `sections/05_results.tex` | 结果（含 27.72%, 30.53%, structural ceiling） | 🔴 CONTAMINATED |
| 10 | `sections/06_discussion.tex` | 讨论（含 "collapse structurally"） | 🟡 措辞需弱化 |
| 11 | `sections/07_conclusion.tex` | 结论（含 27.72%） | 🔴 CONTAMINATED |
| 12 | `sections/08_appendix.tex` | 附录 | — |
| 13 | `supplementary.tex` | 补充材料（ablation 表含 27.72%） | 🟡 基线行污染 |
| 14 | `supplementary_main.tex` | 补充材料主文档 | — |

### 3.2 Kimi 草稿（.kimi_draft_v2）

| # | 文件 | 描述 | 状态 |
|:-:|:-----|:-----|:-----|
| 1 | `sections/05_results.tex.kimi_draft_v2` | §5.x severe-NL 重写 | ✅ Ready |
| 2 | `sections/00_abstract.tex.kimi_draft_v2` | 摘要重写 | ✅ Ready |
| 3 | `sections/06_discussion.tex.kimi_draft_v2` | Discussion 限制段落 | ✅ Ready |
| 4 | `cover_letter_v4.tex.kimi_draft_v2` | Cover letter v4 | ✅ Ready |

### 3.3 英文 Thesis（paper/thesis/）

| # | 文件 | 描述 | Bug 标记 |
|:-:|:-----|:-----|:---------|
| 1 | `main.tex` | 英文 thesis 主文档 | — |
| 2 | `chapter_1_hat_instance_overfitting.tex` | Ch.1 HAT 实例过拟合 | — |
| 3 | `chapter_2_framework.tex` | Ch.2 仿真框架 | — |
| 4 | `chapter_3_hat_taxonomy.tex` | Ch.3 HAT 分类学 | — |
| 5 | `chapter_4_failure_modes.tex` | Ch.4 失效模式（含 27.72%） | 🔴 CONTAMINATED（已加勘误） |
| 6 | `chapter_5_mitigation.tex` | Ch.5 缓解策略（含 30.53%） | 🔴 CONTAMINATED（已加勘误） |
| 7 | `chapter_6_physical_realism.tex` | Ch.6 物理真实感（含 27.72%） | 🔴 CONTAMINATED（已加勘误） |
| 8 | `chapter_7_deployment.tex` | Ch.7 部署（含 27.72%） | 🔴 CONTAMINATED（已加勘误） |
| 9 | `chapter_8_outlook.tex` | Ch.8 展望（含 27.72%, 32.12%） | 🔴 CONTAMINATED（已加勘误） |

### 3.4 中文 Thesis（paper/thesis_cn/）

| # | 文件 | 描述 | Bug 标记 |
|:-:|:-----|:-----|:---------|
| 1 | `chapter_1_introduction.tex` | 第1章 引言 | — |
| 2 | `chapter_2_related_work.tex` | 第2章 相关工作 | — |
| 3 | `chapter_3_methodology.tex` | 第3章 方法论 | — |
| 4 | `chapter_4_benchmarks.tex` | 第4章 基准实验 | — |
| 5 | `chapter_5_failure_modes.tex` | 第5章 失效模式（勘误已加） | 🟡 待重写 |
| 6 | `chapter_6_work2_scope.tex` | 第6章 Work 2 范围 | — |
| 7 | `chapter_7_deployment.tex` | 第7章 部署（含 27.72%, 30.53%） | 🔴 CONTAMINATED |

### 3.5 Work 2（paper/paper2/）

| # | 文件 | 描述 | Bug 标记 |
|:-:|:-----|:-----|:---------|
| 1 | `draft_v0/01_introduction.md` | Work 2 引言（含 27.72%, 30.53%） | ⚠️ Tagged |
| 2 | `draft_v0/02_related_work.md` | Work 2 相关工作 | ⚠️ Tagged |
| 3 | `draft_v0/SKELETON.md` | Work 2 骨架 | ⚠️ Tagged |
| 4 | `skeleton_v0/*.md` | Work 2 早期骨架 | ⚠️ Tagged |

---

## 四、关键脚本（scripts/_gpt/）

| # | 文件 | 描述 | Bug 标记 | 修改建议 |
|:-:|:-----|:-----|:---------|:---------|
| 1 | `check_locked_numbers.py` | 锁定数字守卫脚本 | 🔴 hardcodes 27.72 | 更新 H6 为 M1 结果 |
| 2 | `auto_finalize_nl_ablation.py` | NL 消融自动完成 | 🔴 hardcodes BASELINE=27.72 | 更新 baseline 为 M1 结果 |
| 3 | `analyze_cx_k2_bimodality.py` | K2 双峰分析 | 🟡 处理 pre-fix 数据 | 保留用于历史记录 |
| 4 | `run_hartigans_dip.py` | Hartigan dip 检验 | 🟡 处理 pre-fix 数据 | 保留用于历史记录 |
| 5 | `plot_structural_limit_signature.py` | 结构性极限签名图 | 🟡 处理 pre-fix 数据 | 保留用于历史记录 |
| 6 | `launch_cx_m_run.sh` | CX-M 系列启动脚本 | — | 当前 active |

---

## 五、项目文档（根目录 .md）

| # | 文件 | 描述 | Bug 标记 |
|:-:|:-----|:-----|:---------|
| 1 | `README.md` | 项目主页（已加勘误） | ✅ Erratum added |
| 2 | `REPRODUCIBILITY.md` | 可复现性说明 | ⚠️ 含 27.72% |
| 3 | `MASTER_PLAN.md` | 主计划 | ⚠️ 含 27.72% |
| 4 | `EXPERIMENT_PROTOCOL.md` | 实验协议 | ⚠️ 含 27.72% |
| 5 | `PROJECT_INDEX.md` | 项目索引 | ⚠️ 含 pre-fix 数据 |
| 6 | `AGENT_SYNC_gpt.md` | Agent 同步日志 | — |
| 7 | `CHECKPOINT_INVENTORY_20260418.md` | 检查点清单 | — |
| 8 | `BROADCAST_REBUILD_3WEEK_20260424.md` | 3周重建广播 | — |
| 9 | `BROADCAST_HALT_AND_REPLICATE_20260424.md` | 停机复制广播 | ✅ Tagged |
| 10 | `KIMI_FULL_REPORT_20260424.md` | Kimi 完整报告 | ✅ Tagged |
| 11 | `CODEX_FULL_REPORT_20260424.md` | Codex 完整报告 | — |
| 12 | `STATUS_DASHBOARD_20260424.md` | 状态仪表板 | — |
| 13 | `RELEASE_CHECKLIST.md` | 发布清单 | — |
| 14 | `TOMORNING_README.md` | 晨间状态 | — |
| 15-20 | Cross-review 文件 | 交叉审阅报告 | 多数 clean |

---

## 六、report_md/_gpt/ 关键文件速览

### 6.1 广播类（BROADCAST_*）

| 文件 | 描述 | Bug 标记 |
|:-----|:-----|:---------|
| `BROADCAST_REBUILD_3WEEK_20260424.md` | 3周重建计划（当前 canonical） | — |
| `BROADCAST_HALT_AND_REPLICATE_20260424.md` | 停机复制指令 | ✅ Tagged |
| `BROADCAST_ASSIGNMENT_20260423Q_SLIM.md` | Round Q SLIM 分配 | — |

### 6.2 Codex 实验报告（CODEX_CX_*）

| 文件 | 描述 | Bug 标记 |
|:-----|:-----|:---------|
| `CODEX_BUG_IMMUNITY_AUDIT_20260424.md` | Bug 免疫审计 | ✅ Valid |
| `CODEX_REGRESSION_TEST_20260424.md` | 回归测试文档 | ✅ Valid |
| `CODEX_CX_M1_TRAIN_RESULT.md` | M1 训练结果 | 🔄 Pending |
| `CODEX_CX_M2_TRAIN_RESULT.md` | M2 训练结果 | 🔄 Pending |
| `CODEX_CX_K2_SUMMARY.md` | K2 汇总（38.95%） | ⚠️ pre-fix data |
| `CODEX_CX_J1D_AMBIGUOUS_REPORT.md` | J1d 报告（41.53%） | ⚠️ pre-fix data |

### 6.3 Gemini 理论备忘录（GEMINI_*）

多数为理论分析，部分含 pre-fix 数据。已标记的不再重复。

### 6.4 Kimi 备忘录（KIMI_*）

78 个文件已批量标记 DEPRECATED。详见 `AGENT_SYNC_gpt.md`。

---

## 七、Bug 污染汇总

### 7.1 污染来源

| Bug | 位置 | 修复提交 | 影响 |
|:---|:-----|:---------|:-----|
| LTP/LTD 分支映射翻转 | `analog_layers.py:227-288` | `33bed9c` | NL≠1 时梯度方向错误 |
| 额外 nl 乘数 | `analog_layers.py:227-288` | `33bed9c` | 二阶修正幅度 2x |

### 7.2 失效数字清单

| 数字 | 来源实验 | 失效原因 |
|:---|:---------|:---------|
| 27.72 ± 0.82% | Standard HAT @ NL=2.0 | pre-fix baseline |
| 30.53 ± 7.07% | Joint MLP-linear + Ensemble HAT | pre-fix checkpoint |
| 32.12 ± 7.72% | MLP-only linearization fresh | pre-fix checkpoint |
| 32.60 ± 9.18% | All-linear fresh | pre-fix checkpoint |
| 38.95 ± 9.85% | J1d N=30 extension | pre-fix data |
| 41.53 ± 8.87% | J1d N=10 | pre-fix data |
| 90.88 ± 0.11% | Proportional HAT eval-only | train/eval NL mismatch |

### 7.3 有效（Bug-Immune）数字

| 数字 | 来源 | 验证状态 |
|:---|:-----|:---------|
| 86.37 ± 1.54% | Ensemble HAT @ NL=1.0 | ✅ Symbolic + empirical |
| 97.37 ± 0.05% | Proportional HAT @ NL=1.0 | ✅ Symbolic |
| 88.53 ± 0.08% | OPECT zero-shot | ✅ Symbolic |
| 10.00% | Standard HAT collapse @ NL=1.0 | ✅ Symbolic |
| 82.63 ± 0.56% | Post-fix Standard HAT @ NL=2.0 | 🔄 M-series pending |
| 81.69 ± 0.64% | Post-fix Ensemble HAT @ NL=2.0 | 🔄 M-series pending |

---

## 八、修改建议

### 8.1 高优先级（阻塞提交）

1. **`check_locked_numbers.py`** — 更新 H6 expected 值从 27.72 到 M1 结果
2. **`auto_finalize_nl_ablation.py`** — 更新 BASELINE 从 27.72 到 M1 结果
3. **Live `.tex` 文件** — 等待 CLAUDE-FC 用 Kimi 草稿替换
4. **`README.md`** — 待 M1 结果填入后更新 severe-NL 数字

### 8.2 中优先级（改善可维护性）

5. **`analog_layers_ensemble.py`** — 移入 `archive/` 或删除
6. **`append_agent_sync.py` 等生成脚本** — 归档到 `archive/scripts/` 或标记为 internal-only
7. **`REPRODUCIBILITY.md`, `MASTER_PLAN.md`, `EXPERIMENT_PROTOCOL.md`** — 更新 severe-NL 基线数字

### 8.3 低优先级（清理）

8. **`eval_fresh_instances.py` vs `eval_fresh_instances_postfix.py`** — 检查是否可合并
9. **`.bak_20260418` 文件** — 删除或移入 `archive/`
10. **`paper/paper2/`** — Work 2 已标记，保持现状直到 paper-1 提交

---

## 九、文件整理建议

### 9.1 当前目录结构问题

```
当前问题：
├── 94 个 .py 散落在根目录（难以导航）
├── 727 个 .md 在 report_md/_gpt/（过于庞大）
├── paper/ 同时包含 latex_gpt、thesis、thesis_cn、paper2（职责混杂）
├── 根目录 .md 文件 20+ 个（门面混乱）
└── outputs/、_archive/、release_artifacts/ 含大量冗余副本
```

### 9.2 建议的新结构

```
compute_vit/
├── README.md                    # 精简门面（已加勘误）
├── AGENTS.md                    # Agent 指引
├── LICENSE
├── requirements.txt
├── environment.yml
│
├── src/                         # ← 新建：核心源码
│   ├── analog_layers.py
│   ├── train_tinyvit_ensemble.py
│   ├── train_tinyvit.py
│   ├── eval_fresh_instances.py  # 合并 postfix 版本
│   ├── inference_analysis_utils.py
│   ├── device_profile_utils.py
│   ├── hybrid_*.py
│   └── tinyvit_hybrid_utils.py
│
├── tests/                       # ← 新建：测试集中
│   ├── test_dual_bug_fix.py
│   ├── test_analog_layers.py
│   └── test_*.py
│
├── experiments/                 # ← 新建：实验脚本
│   ├── run_nl_layer_sensitivity.py
│   ├── run_adc_*.py
│   ├── run_crosssim_*.py
│   └── run_*.py
│
├── scripts/                     # 保留：工具脚本
│   ├── _gpt/                    # Agent 专用脚本
│   └── utils/                   # 通用工具
│
├── paper/
│   ├── latex_gpt/               # Paper-1 LaTeX
│   ├── thesis/                  # 英文 thesis
│   ├── thesis_cn/               # 中文 thesis
│   └── paper2/                  # Work 2（deferred）
│
├── data/                        # 数据集 + 配置文件
│   ├── device_profiles/
│   └── configs/
│
├── results/                     # ← 新建：实验结果集中
│   ├── json/                    # 当前 json_gpt/
│   ├── csv/                     # 当前 csv_gpt/
│   └── checkpoints/             # 软链到 checkpoints/
│
├── docs/                        # ← 新建：文档集中
│   ├── BROADCAST_*.md           # 广播文件
│   ├── KIMI_*.md               # Kimi 报告
│   ├── CODEX_*.md              # Codex 报告
│   ├── GEMINI_*.md             # Gemini 报告
│   └── CLAUDE_*.md             # Claude 决策
│
├── archive/                     # 归档（已有）
│   ├── round_p_rescinded/
│   ├── old_audits/
│   └── pre_fix_memos/          # ← 新建：统一存放 pre-fix 污染 memo
│
└── outputs/                     # Remote handoff / reviewer archive
    └── ...                      # 保持现状，定期清理
```

### 9.3 具体整理动作

| # | 动作 | 涉及文件 | 优先级 |
|:-:|:-----|:---------|:------:|
| 1 | 新建 `src/` 目录，移动根目录 .py | 94 个 .py | 高 |
| 2 | 新建 `tests/` 目录，移动 test_*.py | 20+ 个 test | 高 |
| 3 | 新建 `experiments/` 目录，移动 run_*.py | 40+ 个 run | 高 |
| 4 | 新建 `docs/` 目录，集中根目录 .md | 20 个 .md | 中 |
| 5 | 在 `archive/` 下新建 `pre_fix_memos/` | 所有含 27.72% 的旧 memo | 中 |
| 6 | 清理 `.bak_20260418` 文件 | 5 个 .tex.bak | 低 |
| 7 | 删除/归档 `analog_layers_ensemble.py` | 1 个 .py | 低 |
| 8 | 定期清理 `outputs/` 和 `release_artifacts/` | 副本目录 | 低 |

### 9.4 为什么这样整理

1. **根目录减负：** 从 94 个 .py + 20 个 .md 减少到 5 个核心文件，新贡献者可快速定位
2. **职责分离：** `src/`（核心）、`experiments/`（可运行）、`tests/`（验证）、`docs/`（决策记录）
3. **污染隔离：** `archive/pre_fix_memos/` 明确标识不可引用文件，避免误用
4. **结果集中：** `results/json/` + `results/csv/` 替代分散的 `json_gpt/` / `csv_gpt/`
5. **兼容现有工作流：** 不改 `paper/`、`checkpoints/`、`data/` 的结构，最小化 disruption

---

## 十、Sign-off

**Kimi 全项目审计完成。**

- 扫描文件：~1,605 个核心文件
- 标记污染：97+ 个文件（78 个 Kimi memo + 5 个 thesis 章 + 8 个 Work 2 + 2 个脚本 + 2 个根文档 + 5 个 live .tex）
- 产出草稿：7 个 `.kimi_draft_v2`
- 产出报告：6 个审计 MD
- 阻塞项：CX-M1/M2/M3 结果

**下一步（M-series 到位后）：**
1. 填充所有 `[CX-M1 pending]` 占位符
2. 更新 `check_locked_numbers.py` H6 值
3. 更新 `README.md` severe-NL 数字
4. 执行 CLAUDE-FC 集成
