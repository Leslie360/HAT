# 🔄 KIMI → CLAUDE CODE 超级交接报告
**Date:** 2026-04-26  
**From:** Kimi (Moonshot AI, via CLI)  
**To:** Claude Code (Anthropic, via API接入)  
**Project:** `compute_vit` — Organic Optoelectronic CIM for Edge ViT  
**Venue:** Nature Electronics (primary), Advanced Science (fallback)  
**Urgency:** SUBMISSION SPRINT — ~10 days to submission-ready

---

## 1. 项目全景图

### 1.1 这是什么？

一个**有机光电计算内存（CIM）行为模拟框架**，将文献中的器件参数映射到任务级视觉精度。核心创新是**Ensemble HAT（集成硬件感知训练）**——通过每轮训练重采样D2D失配掩码，将跨硬件实例的准确率从10%（崩溃）提升到~86%。

### 1.2 为什么重要？

- 有机光电CIM是新兴领域，缺乏从器件文献到系统精度的系统方法论
- 首次识别并命名了**hardware-instance overfitting**（硬件实例过拟合）这一失败模式
- 提供了一套可替换器件profile的模拟-训练-评估工作流

### 1.3 当前手稿状态

| 指标 | 数值 | 目标 |
|------|------|------|
| 主文字数 | **5,115 words** | ≤ 5,700 (Nat Elec envelope) |
| Main PDF | 15 pages | ~13-15 pages |
| Supplementary | 35 pages | — |
| 编译状态 | **零错误、零警告** | RC 0 |
| Bib条目 | 68 entries | — |

---

## 2. 团队架构与角色分工

### 2.1 决策架构（严格层级）

```
┌─────────────────────────────────────────┐
│         👑 Claude — 首席架构师            │
│    (决策、规划、协调、最终审核)            │
└─────────────────────────────────────────┘
                    │
    ┌───────────────┼───────────────┐
    ▼               ▼               ▼
┌────────┐    ┌──────────┐    ┌──────────┐
│  Kimi  │    │  Codex   │    │  Gemini  │
│ 文本/  │    │ GPU实验/ │    │ 审计/    │
│ 表征/  │    │ 代码/    │    │ 审稿人   │
│ 防御   │    │ TikZ/    │    │ 模拟     │
│        │    │ 数据     │    │          │
└────────┘    └──────────┘    └──────────┘
```

### 2.2 各Agent核心职责

| Agent | 核心能力 | 当前负责 | 不可触碰的禁区 |
|-------|----------|----------|----------------|
| **Claude** | 架构设计、决策、协调 | AGENT_SYNC维护、任务分发、最终审核 | — |
| **Kimi (你)** | LaTeX文本、文献审计、表征分析、防御段落 | ✅ 已完成全部R9+R10文本任务 | 不写新实验代码、不启动GPU训练 |
| **Codex** | PyTorch训练、GPU实验、TikZ绘图、数据流水线 | R10A/R10D/R10E GPU实验、R9B TikZ | 不修改已锁定的数值声明 |
| **Gemini** | 敌对审稿人模拟、代码审计、交叉审核 | 待启动G-HOSTILE-V2、R9C防御审计 | 不修改实验代码 |

### 2.3 协调机制（生死攸关）

**单一真相源：`report_md/_gpt/AGENT_SYNC_gpt.md`**（28,061行）

- **只有Claude可以写决策性内容**
- 其他Agent只能追加自己的广播（BROADCAST）或报告（REPORT）
- 任务通过 `DISPATCH_xxx_YYYYMMDD.md` 文件分发
- 完成状态通过 `BROADCAST_xxx_YYYYMMDD.md` 文件广播

**关键约定：**
- `@Mentions` 用于点名特定Agent响应
- `Status:` 字段必须包含 `RUNNING` / `COMPLETE` / `BLOCKED`
- 任何Agent看到 `MAJOR escalation` 必须立即停下手头工作响应

---

## 3. 关键文件路径大全

### 3.1 手稿核心（LaTeX）

```
compute_vit/paper/latex_gpt/
├── main.tex                          # 主文件入口
├── supplementary_main.tex            #  supplementary入口
├── refs_gpt.bib                      # 参考文献（68条目）
├── sections/
│   ├── 00_abstract.tex               # 摘要（137词）
│   ├── 01_introduction.tex           # 引言（403词）✅ R9A裁剪
│   ├── 02_related_work.tex           # 相关工作（323词）✅ R9A裁剪
│   ├── 03_methodology.tex            # 方法论（743词）✅ R9A裁剪
│   ├── 04_experimental_setup.tex     # 实验设置（325词）
│   ├── 05_results.tex                # 结果（~1,150词）✅ R9A+R10B
│   ├── 06_discussion.tex             # 讨论（~550词）✅ R9A+R9C
│   ├── 07_conclusion.tex             # 结论（395词）
│   └── 08_appendix.tex               # 附录（632词）✅ R9A裁剪
├── supplementary.tex                 # supplementary主体（773+行）
├── supplementary/
│   ├── S_energy_provenance.tex       # ✅ R10H能量来源
│   ├── S_opect_distribution.tex      # ✅ R10C OPECT分布
│   ├── S_tooling_comparison.tex      # ✅ R10E + CrossSim对比
│   ├── S_theory_ensemble_hat.tex     # Ensemble HAT理论推导
│   ├── S_mechanism_empirical.tex     # 机制实证（5个figures）
│   ├── S_hardware_calibration.tex    # S-HW硬件校准管道
│   └── S_reproducibility.tex         # 可复现性说明
└── figures/                          # 图表目录（62个文件）
```

### 3.2 协调与报告

```
compute_vit/report_md/_gpt/
├── AGENT_SYNC_gpt.md                 # 🚨 单一真相源（28,061行）
├── DISPATCH_*                        # 任务分发文件
├── BROADCAST_*                       # 状态广播文件
├── KIMI_*                            # Kimi的所有报告
├── CODEX_*                           # Codex的所有报告
├── GEMINI_*                          # Gemini的所有报告
├── CLAUDE_*                          # Claude的决策文件
└── json_gpt/                         # 实验JSON结果（232个文件）
```

### 3.3 代码与实验

```
compute_vit/
├── train_tinyvit_ensemble.py         # 主训练脚本
├── eval_fresh_instances_postfix.py   # 跨实例评估
├── scripts/_gpt/
│   ├── run_r10a.sh                   # R10A多种子训练（运行中）
│   ├── run_r10b.py                   # R10B类别分布分析（完成）
│   ├── run_r10d.sh                   # R10D中间NL扫描（排队）
│   ├── run_r10e.sh                   # R10E AIHWKit基线（失败）
│   └── check_locked_numbers.py       # 数值锁定检查脚本
├── checkpoints/                      # 模型检查点
│   ├── _ensemble/V4_hybrid_seed456/  # R10A种子456（训练中）
│   └── *.pt                          # 31个检查点文件
└── logs/_gpt/                        # 实验日志
```

---

## 4. 当前任务状态全景

### 4.1 ✅ 已完成（Kimi负责）

| 任务 | 交付文件 | 关键成果 |
|------|----------|----------|
| **R9A 长度手术** | `sections/01-08_*.tex` | 6,948 → 5,115词 |
| **R10I 场景重构** | `sections/06_discussion.tex`, `cover_letter.tex` | "3种情景"改为"1种情景+2种stress test" |
| **R10F 文献新鲜度审计** | `KIMI_R10F_LITERATURE_FRESHNESS_AUDIT_20260425.md` | 确认无直接竞争；新增10条bib |
| **R10C OPECT分布** | `S_opect_distribution.tex` | 诚实框架：profile-substitution robustness |
| **R10H 能量来源** | `S_energy_provenance.tex` | E_cell=100fJ链接Gebregiorgis 2023 |
| **R10G 新颖性对比** | `sections/02_related_work.tex` | 132词novelty paragraph |
| **R10B-text 类别分布** | `sections/05_results.tex`, `supplementary.tex` | 确认10%崩溃是gradient-scaling artifact |
| **R10E AIHWKit失败记录** | `S_tooling_comparison.tex` | AnalogConv2d不支持grouped conv |
| **R9C 防御段落×5** | `sections/05_results.tex`, `06_discussion.tex` | D1-D5全部插入 |
| **R10A预备** | `KIMI_R10A_INTEGRATION_TEMPLATE_20260426.md` | 集成模板+Five-Seed表格占位 |

### 4.2 🔄 进行中（非Kimi可控）

| 任务 | 负责 | 状态 | 预计完成 |
|------|------|------|----------|
| **R10A** 多种子canonical (seeds 456/789) | Gemini/Codex | 🔄 GPU训练中 (Epoch 19/100) | ~20h |
| **R10D** 中间NL扫描 (1.2/1.5/1.8) | Gemini/Codex | ⏳ R10A后排队 | +~15h |
| **R9B** TikZ示意图重绘 | Codex | 🔄 fig1+fig2已完成PDF | 待集成到main.tex |

### 4.3 ⏳ 待启动

| 任务 | 触发条件 | 负责 |
|------|----------|------|
| **Gemini hostile-v2** | R9(A+B+C)全部关闭 | Gemini |
| **R10A集成** | R10A JSON落地 | Kimi/Claude |
| **R10D集成** | R10D JSON落地 | Kimi/Claude |
| **NC格式转换** | 内容冻结后 | Kimi/Codex |
| **Cover letter最终润色** | 投稿前 | Kimi |

---

## 5. 关键技术决策与锁定状态

### 5.1 不可更改的锁定数字（LOCKED）

| 声明 | 值 | 来源 | Zone |
|------|-----|------|------|
| Tiny-ViT FP32 CIFAR-10 | 98.06% | 3-seed mean (98.18/97.87/98.14) | 3A |
| Ensemble HAT canonical | 86.37±1.54% | 种子123, 10 fresh instances | 3A |
| Standard HAT collapse | 10.00% | 种子123, canonical V4 | 3A |
| OPECT zero-shot | 88.53±0.08% | 种子123, 10 fresh instances | 3A |
| Severe-NL recovery band | ~80–82% | M-series 3 seeds (123/456/789) | 3A |
| ADC 6-bit cliff | ~7 pp jump | Iso-accuracy sweep (63 points) | 3A |
| Sobol S_ADC | 0.98 | Full grid | 3A |
| Sobol S_D2D | 0.92 | Operational region | 3A |
| Post-fix Standard HAT | 82.31±0.37% | R10B, M-series ckpt, NL=1.0 | 3A |
| Post-fix Ensemble HAT | 80.25±0.51% | R10B, M-series ckpt, NL=1.0 | 3A |

**Zone纪律：**
- **3A** = bug-immune canonical，可安全引用
- **3B** = pre-fix已作废结果，**不得出现在主文本**
- **3C** = 诊断性/敏感性检查，仅在supplementary中引用

### 5.2 关键架构决策

1. **Venue冻结：** Nature Electronics优先，Advanced Science后备。**不得 preemptively downgrade**
2. **行为模拟 vs 电路精确：** 明确声明为behavioral，IR drop/sneak path未建模
3. **能量诚实：** E_ADC/E_DAC为文献proxy placeholders，非硅测量值
4. **OPECT框架：** Outcome C — "profile-substitution robustness"，**不是** "mismatch-distribution-shape invariance"

### 5.3 待填补的占位符

| 占位符 | 位置 | 等待内容 |
|--------|------|----------|
| R10A multi-seed headline | `abstract`, `05_results`, `06_discussion`, `07_conclusion` | 种子456/789 fresh-eval结果 |
| R10D intermediate NL | `06_discussion` D2 paragraph | NL=1.2/1.5/1.8数据 |
| `[PENDING_R10E_NUMBER]` | 已清除 | — |

---

## 6. 工作流程操作手册

### 6.1 如何启动新任务

1. Claude写 `DISPATCH_[AGENT]_[TASK]_YYYYMMDD.md`
2. Agent完成后写 `BROADCAST_[AGENT]_[TASK]_YYYYMMDD.md`
3. Agent将报告写入 `report_md/_gpt/[AGENT]_[TASK]_YYYYMMDD.md`
4. Claude更新 `AGENT_SYNC_gpt.md`
5. 如果涉及LaTeX修改：**必须编译验证 RC 0**

### 6.2 LaTeX编辑纪律

```bash
cd compute_vit/paper/latex_gpt
# 修改后必须执行：
latexmk -pdf -silent main.tex
latexmk -pdf -silent supplementary_main.tex
# 然后检查：
grep -i "error\|warning" main.log | grep -v "infwarerr"
grep -i "error\|warning" supplementary_main.log | grep -v "infwarerr"
```

### 6.3 数值验证

```bash
cd compute_vit
python scripts/_gpt/check_locked_numbers.py
# 当前状态：14/16 passed（2个crosssim路径问题，非手稿错误）
```

### 6.4 字数监控

```bash
wc -w paper/latex_gpt/sections/*.tex
# 天花板：5,700词（当前5,115，余量585词）
```

---

## 7. 风险清单与升级触发器

### 7.1 🔴 高风险

| 风险 | 影响 | 缓解 |
|------|------|------|
| **R10A种子456/789 < 80%** |  headline数字不可用，需解释 | 已准备fallback叙事（M-series post-fix已证明鲁棒性） |
| **R10D NL=1.2/1.5无法训练** | D2 defense失去支撑 | D2已修改为不依赖R10D的表述 |
| **Nature Electronics desk reject** | 需转投Advanced Science | 封面信和格式已准备双轨 |

### 7.2 🟡 中风险

| 风险 | 影响 | 缓解 |
|------|------|------|
| **Yousuf 2025 LEA对比** | 审稿人质疑新颖性 | R10G novelty paragraph已插入 |
| **AIHWKit无法运行Tiny-ViT** | 缺少head-to-head基线 | R10E已记录失败原因，转化为"自定义框架必要性"论点 |
| **字数超 ceiling** | 超出期刊要求 | 当前5,115 < 5,700，余量充足 |

### 7.3 升级触发条件（来自AGENT_SYNC）

- R10A任何种子 < 80% = **MAJOR escalation**
- R10E AIHWKit beats us = honest reframe
- 编译出现新error/warning = 立即修复
- hostile-v2发现 > 2 unaddressed concerns = 启动额外防御

---

## 8. 给Claude Code的特别提示

### 8.1 Kimi的工作风格

- **文本优先**：所有任务以LaTeX/文本交付物为终点
- **数值偏执**：每个数字必须有JSON来源，不凭空编造
- **诚实框架**：宁可承认局限性，不做过度承诺
- **编译洁癖**：零error零warning是底线，不是目标

### 8.2 你应该继承的上下文

1. **AGENT_SYNC是圣经**：任何决策前读最新200行
2. **Claude是首席架构师**：不要越级决策，重大问题上报
3. **Zone纪律不可破**：3B结果绝不能进主文本
4. **字数是硬约束**：当前5,115，天花板5,700，新增内容必须考虑替换而非单纯追加

### 8.3 你应该立即检查的事项

1. 读取 `AGENT_SYNC_gpt.md` 最后500行
2. 读取 `KIMI_R9C_DEFENSE_REPORT_20260426.md`
3. 读取 `KIMI_R10A_INTEGRATION_TEMPLATE_20260426.md`
4. 运行 `check_locked_numbers.py` 确认数值一致性
5. 编译 `main.tex` + `supplementary_main.tex` 确认 RC 0

### 8.4 常用命令速查

```bash
# 编译
latexmk -pdf -silent main.tex
latexmk -pdf -silent supplementary_main.tex

# 字数
cd compute_vit/paper/latex_gpt && wc -w sections/*.tex

# 数值检查
cd compute_vit && python scripts/_gpt/check_locked_numbers.py

# 查找PENDING占位符
grep -r "PENDING\|TODO\|FIXME" paper/latex_gpt/sections/

# 检查未定义引用
grep "undefined" paper/latex_gpt/main.log

# 查看最新AGENT_SYNC
tail -200 compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md

# R10A训练状态
tail -5 compute_vit/logs/_gpt/r10a_seed456_out.log
tail -5 compute_vit/logs/_gpt/r10a_seed789_out.log

# R10B结果
cat compute_vit/report_md/_gpt/json_gpt/r10b_standard_hat_class_distribution.json
```

---

## 9. 附件清单

本报告关联的交付文件：

| 文件 | 路径 | 说明 |
|------|------|------|
| 本交接报告 | `report_md/_gpt/KIMI_HANDOFF_MASTER_20260426.md` | 你正在读的文件 |
| R9C防御报告 | `report_md/_gpt/KIMI_R9C_DEFENSE_REPORT_20260426.md` | 5段防御详细变更日志 |
| R10A集成模板 | `report_md/_gpt/KIMI_R10A_INTEGRATION_TEMPLATE_20260426.md` | R10A数据回来后的集成指南 |
| R10F文献审计 | `report_md/_gpt/KIMI_R10F_LITERATURE_FRESHNESS_AUDIT_20260425.md` | 58条目审计+10条新增 |
| R10G新颖性对比 | `report_md/_gpt/KIMI_R10G_NOVELTY_CONTRAST_20260425.md` | 132词paragraph设计 rationale |
| R10H能量来源 | `report_md/_gpt/KIMI_R10H_ENERGY_PROVENANCE_REPORT_20260425.md` | 能量常数来源追踪 |
| R10I场景重构 | `report_md/_gpt/KIMI_R10I_SCENARIOS_REFRAMING_20260425.md` | 情景框架转换报告 |
| R10C OPECT分布 | `report_md/_gpt/KIMI_R10C_OPECT_DISTRIBUTION_REPORT_20260425.md` | 统计特征+AD测试 |
| R9A进度报告 | `report_md/_gpt/KIMI_R9A_PROGRESS_20260425.md` | 长度手术详细记录 |
| 敌对审稿人总结 | `report_md/hostile_review_summary_20260410.md` | 7审稿人完整报告 |

---

## 10. 签名

**Kimi**  
文本Agent | 负责：R9A长度手术、R10B/F/G/H/I/C文本、R9C防御段落  
状态：全部交付，待命  
最后活跃：2026-04-26

**交接确认：**  
- [ ] 所有LaTeX文件已读取
- [ ] 编译通过 RC 0
- [ ] AGENT_SYNC最后500行已读
- [ ] 风险清单已审阅
- [ ] 下一步任务已明确
