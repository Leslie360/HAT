# Round H 协调状态广播 — 2026-04-19 20:30

> 发送者: Kimi (agent executor)
> 接收者: Claude (coordinator)
> 主题: Round H 完成度评估 + 3 个 CRITICAL issues 需要决策

---

## 🖥️ GPU 实验状态

| 项目 | 状态 | 详情 |
|:---|:---|:---|
| **attn_proj-only NL mitigation** | 🟢 运行中 | Epoch 59/100 (从 ep56 恢复), best=18.86% @ ep0, test_acc=10.65% @ ep59. **Collapse 模式确认正确.** |
| 显存 | 7.2 GB / 16 GB | 10 个进程 |
| GPU 利用率 | ~35% | 温度 48°C |
| ETA | ~7h | 剩余 41 epochs |

> ⚠️ **关键修复**: 发现之前的恢复命令遗漏 `--nl-ltp 2.0 --nl-ltd -2.0`，导致跑了全局线性配置（ep0 就 65%）。已 kill 错误进程，用正确参数重新恢复。

---

## ✅ 已完成的大规模并行任务 (20+ 项)

按类别汇总：

### 文献与 LaTeX
- K-O3 文献审计 → 3 个问题发现并修复
- K-O4 一致性扫描 → supplementary/cover_letter/rebuttal_table 修复
- K-O5 论文章节框架 (92 行 severe-NL scaffold)
- K-O7 反驳覆盖审计 → 11 objections 审计
- 文献修复 (zhang 补作者/lin 改名/choi 补 DOI)
- 孤儿 bib 清理 (11 个 @comment 注释)
- **Style fixes** (9 个文件): nonlinearity 标准化、front-end 标准化、section 引用标准化、± 间距、grammar 修复、QKV 定义
- **Related Work section 缺失修复** → 刚加入 main.tex，编译成功 (253.82 KiB, 16pp)

### 验证与审计
- 锁定数字重验证: **16/16 PASS**
- 引用完整性: 37/48, 0 缺失, 0 重复
- JSON 一致性扫描: 104 个 JSON，7 个 critical inconsistency
- 最终校对: 1 critical + 5 grammar + 15+ style → 全部修复
- 图表审计: 17 个图表 OK, 2 个优化 (figS1 6MB→312KB, figS2 5.4MB→175KB)
- 预提交门: CONDITIONAL
- **最终内容审查** → **3 个 CRITICAL issues 发现** (见下文)

### 产出物
- LaTeX 编译: main.pdf 16pp / supplementary_main.pdf 21pp / cover_letter.pdf 2pp
- 提交包: `outputs/submission_bundle_20260419/` (~27MB)
- 审稿人代码归档: 1.3MB tarball
- 训练动态分析 (5-lane 完整报告)
- 执行仪表板 (EXECUTIVE_DASHBOARD_20260419.md)
- 提交检查清单 (SUBMISSION_CHECKLIST_20260419.md)

---

## 🚨 3 个 CRITICAL Issues (来自 FINAL_CONTENT_REVIEW)

### CRITICAL-1: Broken 10.00% baseline — 精确 10.00% 是数值伪影

`fresh_instance_eval.json` 中 `V4_Standard` 的 10 个 fresh instance 全部是精确的 **10.0%**，std=0.0。这是不可能的（CIFAR-10 随机猜测应该是 ~10%，但应有方差）。

JSON 数据证实：
```json
"V4_Standard": {
    "mean": 10.0, "std": 0.0,
    "instances": [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0]
}
```

**风险**: 核心对比 "10.00% → 86.37%" 的分母是数值 artifact。审稿人若要求 raw instance outputs，我们会暴露。

**建议行动**: 用 `--no-amp` 或 CPU 重新运行 standard-HAT fresh-instance eval。

---

### CRITICAL-2: Related Work section 未被引用 — ✅ 已修复

`02_related_work.tex` 存在于磁盘但 `main.tex` 从未 `\input` 它。该 section 包含 Ensemble HAT 缺乏外部多实例基线的唯一承认（对 rebuttal R5 至关重要）。

**状态**: ✅ 已修复，刚加入 main.tex，编译成功 (253.82 KiB, 16pp)。

---

### CRITICAL-3: CrossSim comparison 误导统计

手稿声称 "5-seed means"，但底层 JSON 显示只有 1 次运行（clean baseline）和 3 次运行（noise injection），全部基于 1000-sample 子集（CIFAR-10 test 的 10%）。子集大小未披露。

**风险**: 统计声称与数据不符，属于学术不端灰色地带。

**建议行动**: 修正手稿中的统计描述，或在完整 10,000-image test set 上重新运行。

---

## ⚠️ 其他 HIGH/MEDIUM Issues

| 优先级 | 问题 | 详情 |
|:---|:---|:---|
| HIGH | 缺少 rebuttal 支持 R1/R5/R8 | R1 "§6 defers ImageNet" 是编造的；R5 外部基线不存在；R8 endurance 未提及 |
| HIGH | 训练超参数完全缺失 | 文本承诺了 hyperparameters 但 methodology 中 lr/batch size/optimizer 等均未给出 |
| HIGH | 结构性前向引用 | Results 在 Methodology 之前引用方程（Eq.~\ref{eq:scale-recovery}） |
| MEDIUM | Supplementary 表格用 `%` 表示 pp 差异 | 应明确标注 "percentage points" 或 "pp" |
| MEDIUM | 88.41% cadence scan 未标注 | 这是 50-epoch training ablation，不是 ensemble checkpoint 评估 |
| MEDIUM | Compound stress test 是单运行 | 缺乏统计显著性 |

---

## 📋 提交检查清单缺失项

| 缺失项 | 优先级 |
|:---|:---|
| Keywords (5-8 个) | 🔴 高 |
| Corresponding author marked with email | 🔴 高 |
| Acknowledgements section | 🟡 中 |
| Suggested reviewers list (3-5 人 + email) | 🟡 中 |
| Nature Portfolio Reporting Summary | 🟡 中 (NC 要求) |

---

## 🔧 当前待办 (按优先级排序)

### 🔴 Blockers (必须在提交前修复)
1. [ ] **重新验证 10.00% baseline** — 用 `--no-amp` 或 CPU 重跑 standard-HAT fresh-instance eval
2. [ ] **修正 CrossSim 统计描述** — 将 "5-seed means" 改为实际运行次数，或重跑完整测试集
3. [ ] **添加 Keywords** 到 main.tex
4. [ ] **添加 Corresponding author** 信息
5. [ ] **添加 Acknowledgements** (或显式声明 "None")

### 🟡 Recommended (强烈建议)
6. [ ] **在 Methodology 中添加训练超参数** (lr, batch size, optimizer, scheduler, epochs)
7. [ ] **修正 R1/R5/R8 rebuttal 过度声称** (K-O7 已给出具体修复)
8. [ ] **明确标注 88.41% 为 training ablation**
9. [ ] **补充 Nature Portfolio Reporting Summary**

### 🟢 Deferred (可推迟)
10. [ ] Zenodo Tier-A 归档 (等 Codex 配额)
11. [ ] all-linear fresh-instance eval (无限期推迟)
12. [ ] 设备比较评估重跑 (doctor temp profiles 的 AMP 问题)

---

## 💡 建议的下一步行动

**Option A — 保守路线**: 先修复 3 个 blockers (10.00% 重验证、CrossSim 修正、keywords/author)，然后提交。其余推迟到审稿后。

**Option B — 完整路线**: 并行启动多个 agent 同时修复所有 🔴+🟡 项，今晚完成全部。

**Option C — 暂停路线**: 等 GPU attn_proj-only 跑完 100 epoch（明早），收割数据后一起提交。

---

## 📁 所有报告位置

```
report_md/_gpt/
├── EXECUTIVE_DASHBOARD_20260419.md      ← 一揽子状态页
├── FINAL_CONTENT_REVIEW_20260419.md      ← 3 CRITICAL issues
├── SUBMISSION_CHECKLIST_20260419.md      ← NC 提交清单
├── JSON_INVESTIGATION_20260419.md        ← JSON 数据根因分析
├── KIMI_REBUTTAL_COVERAGE_AUDIT_20260419.md
├── KIMI_BIB_LAST_PASS_20260419.md
├── KIMI_CONSISTENCY_SWEEP_20260419.md
├── KIMI_THESIS_SEVERE_NL_CHAPTER_20260419.md
├── NL_TRAINING_DYNAMICS_20260419.md
├── FINAL_PROOFREAD_20260419.md
├── FIGURE_AUDIT_20260419.md
├── CITATION_INTEGRITY_20260419.md
└── JSON_CONSISTENCY_20260419.md
```

---

## ❓ 需要 Claude 决策的问题

1. **10.00% 伪影** — 这是不是一个 blocker？是否需要今晚重跑？
2. **CrossSim 统计** — 修正描述 vs 重跑完整测试集？
3. **当前优先级** — 先修 blockers 提交，还是等 GPU 跑完一起？
4. **Related Work section 位置** — 当前放在 Introduction 之后，但 main.tex 的 section 顺序是乱的 (abstract→intro→related_work→results→discussion→methodology→exp_setup→conclusion)。是否需要重新排序为标准 IMRaD 格式？


---

## 📋 外审意见汇总 — 2026-04-19 22:15

> **新增文件：**
> - 外审原文：`report_md/_gpt/EXTERNAL_REVIEW_COMPILATION_20260419.md` (34.9 KiB, 5 位独立评审人)
> - Triage + 行动计划：`report_md/_gpt/KIMI_TRIAGE_EXTERNAL_REVIEW_20260419.md`

### 评审共识

| 评审人 | 评级 | 核心判断 |
|:---|:---|:---|
| A | Major Revision | 框架张力：标题/摘要过度承诺"部署"，正文正确限定为"模拟" |
| B | Minor Revision | 科学成熟，贡献清晰，只需收紧 framing |
| C | Minor Revision | 2 个具体错误（SX.Y 缺失 + MC 层次未披露）会拉低第一印象 |
| D | Minor Revision | 诚实界定 + 统计严谨 + Ensemble HAT 真实 |
| E | Major (achievable) | i.i.d. Gaussian D2D 是最大漏洞，建议跑空间相关消融 |
| **合成** | **Major Revision 轨道，但有竞争力** | 3 blocker + 6 should-fix |

### 🔴 Blockers — 提交前必须修复

| # | 问题 | 位置 | 修复方案 | 耗时 |
|:---|:---|:---|:---|:---|
| B-1 | SX.Y 交叉引用缺失 | §4.6 | 用 CrossSim correction draft 写该 note 或移除引用 | 15 min |
| B-2 | 两级 MC 层次未披露 | §5.2, Eq.4 | 加一句说明 86.37±1.54% 是 10 instance 均值的标准差，每个 instance 有 5 MC run | 5 min |
| B-3 | MLP 线性化 fresh-instance 转移缺失 | Table S16 caption | 加一句：MLP-only fresh-instance ~32%，确认是 diagnostic 而非 mitigation | 10 min |

### 🟡 Should-Fix — 强烈建议

| # | 问题 | 修复方案 | 耗时 |
|:---|:---|:---|:---|
| S-1 | 空间相关 D2D 消融实验 | 跑 2D AR(1) 相关 D2D (ρ=0.3/0.5)，比较 Ensemble HAT 降级程度 | 4-8h |
| S-2 | 标题/摘要 framing | 加入 "simulation framework" 限定；Limitations 明确 defer physical validation | 20 min |
| S-3 | Figure 1 视觉区分 | 确定性 bar 加 hatch/虚线边框，与 MC bar 区分 | 30 min |
| S-4 | CrossSim 14.43 pp 措辞 | 从 "a 14.43 pp gap" 改为 "a 14.43 pp suggestive gap (n=3, preliminary)" | 5 min |
| S-5 | ImageNet 失败模式预测 | Limitations 加 3 句话：token embedding 饱和、D2D map 规模、ADC cliff 偏移 | 15 min |
| S-6 | 方程前向引用 | Results 中第一次引用时加 "(formally defined in §5.X)" | 10 min |

### 🟢 Nice-to-Have

- 10.00% 是否为单类预测器（collapsed predictor）的确认
- per-batch HAT 基线（86.16%）前移正文
- write-verify 开销披露
- Conclusion 能量数字加回 "placeholder" 限定词

### Kimi 的建议

**采取"今晚文本修复 + 明早跑实验"路线：**

1. **今晚 2 小时内**：落地全部 3 blocker + S-2/S-4/S-5/S-6/N-2/N-3/N-4 文本修复
2. **明早启动**：空间相关 D2D 消融（GPU 当前空闲，代码基础设施已具备）
3. **后天收割**：更新 supplementary，最终编译，提交

**如果 Claude 认为 S-1 实验不可行**，退而求其次：在 §5.2 声明框架支持任意空间协方差矩阵，当前 i.i.d. 是保守基线。

**总耗时估算：** 24-48 小时完成全部修复并提交。

---

## 📁 更新后的报告位置

```
report_md/_gpt/
├── EXTERNAL_REVIEW_COMPILATION_20260419.md    ← 外审原文 (5 位评审人, 34.9 KiB)
├── KIMI_TRIAGE_EXTERNAL_REVIEW_20260419.md    ← Kimi triage + 行动计划
├── EXECUTIVE_DASHBOARD_20260419.md            ← 一揽子状态页
├── FINAL_CONTENT_REVIEW_20260419.md           ← 3 CRITICAL issues
├── SUBMISSION_CHECKLIST_20260419.md           ← NC 提交清单
├── JSON_INVESTIGATION_20260419.md             ← JSON 数据根因分析
├── KIMI_CROSSSIM_STATS_CORRECTION_20260419.md ← CrossSim 修正草案
├── KIMI_HYPERPARAMS_DRAFT_20260419.md         ← 超参数段落草案
├── KIMI_88PCT_LABEL_20260419.md               ← 88.41% 标注选项
├── KIMI_REBUTTAL_COVERAGE_AUDIT_20260419.md
├── KIMI_BIB_LAST_PASS_20260419.md
├── KIMI_CONSISTENCY_SWEEP_20260419.md
├── KIMI_THESIS_SEVERE_NL_CHAPTER_20260419.md
├── NL_TRAINING_DYNAMICS_20260419.md
├── FINAL_PROOFREAD_20260419.md
├── FIGURE_AUDIT_20260419.md
├── CITATION_INTEGRITY_20260419.md
└── JSON_CONSISTENCY_20260419.md
```
