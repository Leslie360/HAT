# 📢 广播：审稿人意见 0412 深度分析与行动建议

> **日期**: 2026-04-13  
> **来源**: 10位外部审稿人 (`审稿意见0412.md`, 646行)  
> **紧迫性**: CRITICAL — 需立即决策投稿策略

---

## 🚨 审稿人共识总览

| 审稿人 | 总体建议 | 方法学 | 贡献 | NC适合度 |
|:-------|:---------|:------:|:----:|:--------:|
| Sonar | Major Revision | 3.5/5 | 3/5 | 3/5 |
| Kimi | Minor Revision | 4/5 | 4/5 | 4/5 |
| DS-Tenxun | Major Revision | 4/5 | 3/5 | 4/5 |
| Doubao | Major Revision | 4/5 | 4/5 | 4/5 |
| Nemotron | Major Revision | 3.5/5 | 3.5/5 | 3/5 |
| Mimo | Minor Revision | 4/5 | 4/5 | 4/5 |
| Claude-Sonnet | Major Revision | 3/5 | 3.5/5 | 2.5/5 |
| GLM | Major Revision | 4/5 | 4/5 | 4/5 |
| GPT | Major Revision | 3.5/5 | 3/5 | 3/5 |
| Gemini | Major Revision | 3.5/5 | 3.8/5 | 3/5 |

**统计**: 8× Major Revision, 2× Minor Revision  
**平均分**: 方法学 3.7/5 | 贡献 3.6/5 | NC适合度 3.45/5

---

## 🔴 审稿人共识攻击点（TOP 5）

### 1. 代理参数的循环论证问题 (9/10 位审稿人提及)
**Sonar**: "你用不确定的输入，声称得出确定的系统级结论"  
**Nemotron**: "参数溯源的循环性与代理值的不可独立验证性"  
**GPT**: "用文献猜测定义了边界，又以仿真验证了这个边界"  
**Claude-Sonnet**: "代理参数链过长，'有机器件'主张缺乏物理闭合"

**攻击原话模拟**:
> "如果真实有机器件的NL实测值是1.3或2.8，这个'悬崖'会在哪里？"
> "C2C从1%变到8%对精度几乎无影响，那为什么要声称与具体有机器件相关？"

**缓解方案**: 
- ✅ 已在摘要添加"simulation-only"声明
- ✅ 已软化NL=2.0为"approximation-limit"
- 🔄 **新增任务**: Supplementary中加入"参数风险矩阵"(2页)

---

### 2. Ensemble HAT 新颖性边界模糊 (7/10 位审稿人提及)
**Sonar**: "与domain randomization高度相似，缺少中间baseline"  
**Nemotron**: "与robust optimization和randomized smoothing文献的关系未明确"  
**GPT**: "缺少关键对照：per-forward i.i.d. vs per-epoch D2D重采样"  
**Gemini**: "没有做控制实验排除'只是增强了数据增强量'这一解释"

**必须补充的对照实验**:
| 对照 | 目的 | 工作量 |
|:-----|:-----|:-------|
| i.i.d. C2C增强 (无spatial correlation) | 证明spatial correlation感知的必要性 | 1 GPU-hour |
| per-forward D2D扰动 vs per-epoch | 量化"结构化空间失配"的实际贡献 | 1 GPU-hour |
| 增强噪声强度的标准HAT (σD2D×2) | 排除"只是更强的噪声正则化" | 1 GPU-hour |

**文本防御**: Related Work新增段落区分domain randomization / minimax training / randomized smoothing

---

### 3. 能量模型可信度问题 (6/10 位审稿人提及)
**Nemotron**: "能量常数是'analytical placeholders'，11.45×缺乏电路级基础"  
**Gemini**: "buffer未建模、数字端用通用估算，会被降级为量级参考"  
**GLM**: "对于未经验证的有机工艺来说过于乐观"

**缓解方案**:
- 摘要中将"11.45×"改为"first-order upper-bound estimate"
- Supplementary补充buffer开销的参数化敏感性分析
- 明确声明："能量估算为行为级上界，非tape-out承诺"

---

### 4. NL=2.0 "硬边界"表述 (8/10 位审稿人提及) — ✅ 已处理
**状态**: 已在GM-X19中统一修改为"approximation-limit boundary"

**但仍需补充**:
- NL扫描曲线 (NL=1.0, 1.5, 1.8, 2.0) 以支持"极限"叙事

---

### 5. 缺乏真实器件验证 (5/10 位审稿人提及) — 战略问题
**分歧**: 
- **Kimi/Mimo/GLM**: 当前方法学定位清晰，无需推迟投稿
- **Sonar/DS-Tenxun/Claude-Sonnet**: 建议Revision阶段补充验证

**用户决策**: 使用自有数据，不联系外部团队 → **策略A确认**

---

## 🟢 审稿人共识优势（防御弹药）

1. **透明度诚实** (10/10 认可)
   - 参数溯源矩阵 Table S2
   - 明确列出IR drop、温度等out-of-scope效应
   - 这会在审稿时获得好感分

2. **Ensemble HAT发现真实** (9/10 认可)
   - 10% → 86.37% 的fresh-instance跳跃
   - 统计可信度高 (10实例×5MC评估)
   - 概念上连贯

3. **"6-bit ADC悬崖"可操作** (8/10 认可)
   - 直接约束前端电路规格
   - 跨架构佐证 (ResNet/ConvNeXt/ViT)

4. **三架构三数据集覆盖** (8/10 认可)
   - ResNet-18 / ConvNeXt-Tiny / Tiny-ViT-5M
   - CIFAR-10/100 / Flowers-102

---

## 🎯 紧急行动任务

### 任务1: 参数风险矩阵 [P0 — 2天内]
**执行者**: Codex/Kimi  
**交付**: Supplementary新增2页表格

| 参数 | 来源 | 物理合理范围 | 超出范围影响 | 结论鲁棒性 |
|:-----|:-----|:-------------|:-------------|:-----------|
| τ₁=140ms | Vincze 2025 | 50-300ms | retention失效 | ⭐⭐⭐⭐⭐ |
| σD2D=10% | Zhang 2025 | 5%-30% | Ensemble HAT失效 | ⭐⭐⭐⭐⭐ |
| NL=2.0 | 代理估计 | 1.5-3.0 | 精度崩溃 | ⭐⭐⭐⭐ |

### 任务2: Ensemble HAT对照实验 [P0 — 3天内]
**执行者**: 用户/实验团队  
**必须运行**:
1. i.i.d. C2C增强 baseline
2. per-forward D2D扰动
3. σD2D×2 增强HAT

### 任务3: NL扫描曲线 [P1 — 1周内]
**执行者**: 用户/实验团队  
**扫描点**: NL = 1.0, 1.5, 1.8, 2.0, 2.2

### 任务4: Related Work理论区分 [P0 — 2天内]
**执行者**: Gemini  
**内容**: 新增段落讨论与以下工作的关系：
- (a) Robust optimization (minimax training)
- (b) Randomized smoothing (Cohen et al., 2019)
- (c) Domain randomization (Tobin et al., 2017)

### 任务5: 能量模型敏感性分析 [P1 — 1周内]
**执行者**: Codex  
**内容**: 10%-50%互连开销下的效率变化

---

## 📊 投稿策略建议

### 推荐: 选项A+ — "带预加载弹药的Major Revision"

**时间线**:
- **本周**: 完成任务1、4 (文本防御)
- **下周**: 投稿NC
- **审稿期间**: 并行完成任务2、3、5 (实验补充)
- **Revision阶段**: 提交对照实验结果

**理由**:
1. 8/10审稿人预期Major Revision，直接投是合理选择
2. 核心实验(任务2)可在审稿期间并行完成
3. 预加载"参数风险矩阵"可将防御转为进攻

---

## 💬 审稿人原话精选

> "论文的实质够投NC，但若干结论表述的强度超过了仿真框架所能支撑的证据级别。"
> — Claude-Sonnet

> "这不是'没有硬件验证'本身的问题，而是参数代理链的脆弱性。"
> — Gemini

> "透明度诚实是论文最大的保护盾。"
> — Sonar

> "将叙事重心从'发现了有机器件的物理极限'转移到'提供了能够揭示部署风险的基准工具'。"
> — GLM

---

**广播完成。等待任务分配确认。**
