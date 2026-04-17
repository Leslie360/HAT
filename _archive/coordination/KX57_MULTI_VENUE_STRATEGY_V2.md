# KX57: Multi-Venue Strategy Memo v2

> **Date**: 2026-04-13  
> **Status**: COMPLETED  
> **Goal**: 在"现在不锁定 NC"的前提下，给出更现实的 venue 分流建议

---

## 核心原则

**不锁定任何 venue**，保持多轨并行准备。根据实测数据到达时间和实验结果动态决策。

---

## Venue 对比矩阵

### Nature Communications

| 维度 | 评估 |
|:-----|:-----|
| **当前匹配卖点** | Ensemble HAT算法创新 + 跨学科方法学 |
| **还缺什么** | 实测设备闭环验证；ImageNet-scale结果 |
| **最能拉高性价比的实验** | 1. i.i.d. D2D对照 (GM-E1) 2. 实测profile替换Zhang案例 |
| **实测数据价值** | **极高** — 可能将Major转为Minor Revision |
| **风险** | 8/10审稿人预期Major Revision；代理参数质疑 |
| **决策触发** | 实测数据到达 + 愿意接受Major Revision周期 |

---

### npj Computational Materials

| 维度 | 评估 |
|:-----|:-----|
| **当前匹配卖点** | 材料-系统桥接方法学；器件物理敏感性分析 |
| **还缺什么** | 几乎完整；仅需 repositioning 强调 |
| **最能拉高性价比的实验** | 1. 实测数据整合 2. Parameter Risk Matrix |
| **实测数据价值** | **高** — 强化方法学可信度，非必需 |
| **风险** | 较低；IF~9-10可能被视为"降级" |
| **决策触发** | 快速高信心接受优先于最大影响 |

---

### Advanced Intelligent Systems (Wiley)

| 维度 | 评估 |
|:-----|:-----|
| **当前匹配卖点** | 边缘AI部署；系统级算法补偿 |
| **还缺什么** | 强调系统智能角度；弱化器件物理 |
| **最能拉高性价比的实验** | 1. 能效敏感性分析 2. 边缘部署场景讨论 |
| **实测数据价值** | **中** — 有则更好，无亦可 |
| **风险** | 最低；快速审稿；但影响力和认可度较低 |
| **决策触发** | 时间压力 > 影响追求；或NC/npj拒稿后快速转投 |

---

### IEEE TPDS (Systems/ML备选)

| 维度 | 评估 |
|:-----|:-----|
| **当前匹配卖点** | 算法贡献 (Ensemble HAT)；系统优化 |
| **还缺什么** | ImageNet-scale验证；去除器件物理细节 |
| **最能拉高性价比的实验** | 1. ImageNet-1K结果 2. 跨架构泛化验证 |
| **实测数据价值** | **低** — 算法 venue 不重实测 |
| **风险** | 需大幅重构论文；可能要求更多ML理论 |
| **决策触发** | ImageNet结果极佳 + 愿意 reposition 为纯算法贡献 |

---

## 动态决策树

```
实测数据到达？
├── 是 (2个月内)
│   ├── 数据质量高 → 优先 NC (Major→Minor潜在转换)
│   └── 数据质量一般 → npj (高信心)
├── 否
│   ├── 时间压力高 → AIS (最快)
│   ├── 接受 Major Rev → NC (最大影响)
│   └── 高信心优先 → npj (平衡)
```

---

## 实验性价比 by Venue

| 实验 | NC | npj | AIS | TPDS |
|:-----|:---|:----|:----|:-----|
| GM-E1 (i.i.d. D2D) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| GM-E2 (ADC digital) | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| 实测数据整合 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐ |
| ImageNet-1K | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| NL scan | ⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐ |
| Retention sensitivity | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐ |

---

## 推荐策略

### 策略 A: "影响最大化" (用户当前倾向)
- **首选**: NC
- **条件**: 等待实测数据；接受 Major Revision
- **备选**: npj (如果NC desk reject)

### 策略 B: "信心最大化"
- **首选**: npj Computational Materials
- **条件**: 可立即投稿；Minor Revision预期
- **实测数据**: Revision阶段添加

### 策略 C: "时间最大化"
- **首选**: Advanced Intelligent Systems
- **条件**: 资金/毕业时间压力
- **风险**: 长期影响力较低

---

## 并行准备清单

保持以下全部准备就绪，直到最终决策：

- [x] NC-ready manuscript (当前版本已够)
- [x] npj repositioning guide (KX45)
- [x] AIS fallback plan (最小改动)
- [ ] TPDS repositioning (仅当ImageNet结果极佳时启动)

---

## 决策触发器

| 触发事件 | 推荐 Action |
|:---------|:------------|
| 实测数据 1周内到达 | 等数据 → NC |
| 实测数据 1月+到达 | 当前版本 → npj；数据作为Revision |
| 资金/毕业截止 <3月 | 立即 → AIS |
| ImageNet结果 >80% | 评估 TPDS repositioning |
| NC desk reject | 1周内转 npj |

---

**状态**: 多轨并行准备中，不锁定任何 venue。
